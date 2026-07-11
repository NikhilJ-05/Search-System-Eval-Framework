import json
import logging
import asyncio
import hashlib
import os
import re
from typing import Dict, Any, List, Optional
from collections import Counter

from models.test_case import TestCase, RubricDimension, EvalRubric
from models.eval_result import (
    FirecrawlSearchResult,
    CriteriaCheck,
    DimensionEval,
    EvalResult
)
from clients.openrouter import OpenRouterClientPool
from config import EvalConfig

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)

QUALITY_KEYWORDS = ["coverage", "content", "accuracy", "relevance", "completeness", "information"]
RANKING_KEYWORDS = ["ranking", "authority", "source", "ordering", "priority", "domain"]
FIDELITY_KEYWORDS = ["fidelity", "structure", "scrape", "noise", "markdown", "formatting", "table"]

BASELINE_DIMENSIONS = {
    "quality": RubricDimension(
        name="_baseline_coverage",
        weight=0.15,
        criteria="Search results contain content directly relevant to the query intent. Key factual claims addressing the query are present across the returned results.",
        contrastive_fail="Fails if no result addresses the core question, or all results are tangential/off-topic."
    ),
    "ranking": RubricDimension(
        name="_baseline_ranking",
        weight=0.15,
        criteria="Higher-authority and more relevant sources appear before lower-quality ones. Official or primary sources should rank above blogs and aggregators.",
        contrastive_fail="Fails if blog posts or aggregator pages rank above official/primary sources, or if the most relevant result is buried below rank 3."
    ),
    "fidelity": RubricDimension(
        name="_baseline_fidelity",
        weight=0.15,
        criteria="Scraped markdown preserves the page's structural elements (tables, headings, code blocks, lists) and content is complete without navigation noise or boilerplate leakage.",
        contrastive_fail="Fails if tables are flattened to plain text, content is truncated mid-section, or navigation/cookie banners dominate the markdown."
    ),
}


def extract_structure_profile(markdown: str, url: str = "", title: str = "") -> dict:
    """
    Full programmatic document analysis. No LLM. No truncation.
    Returns a complete structural fingerprint of the markdown.
    """
    if not markdown:
        markdown = ""
    lines = markdown.split("\n")
    total_chars = len(markdown)
    total_lines = len(lines)
    total_words = len(markdown.split())

    headings = []
    for i, line in enumerate(lines):
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            headings.append({
                "level": len(m.group(1)),
                "text": m.group(2).strip(),
                "line": i + 1
            })

    tables = []
    in_table = False
    table_start = 0
    table_rows = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if "|" in stripped and not in_table:
            in_table = True
            table_start = i + 1
            table_rows = 1
        elif in_table and "|" in stripped:
            table_rows += 1
        elif in_table:
            header_line = lines[table_start - 1]
            col_count = len([c for c in header_line.split("|") if c.strip()]) if header_line else 0
            tables.append({
                "start_line": table_start,
                "end_line": i,
                "row_count": table_rows,
                "col_count": col_count,
                "position_pct": round(table_start / max(total_lines, 1) * 100, 1)
            })
            in_table = False
            table_rows = 0

    code_blocks = []
    in_code = False
    code_lang = ""
    code_start = 0
    for i, line in enumerate(lines):
        if line.startswith("```") and not in_code:
            in_code = True
            code_lang = line[3:].strip()
            code_start = i + 1
        elif line.startswith("```") and in_code:
            code_blocks.append({
                "language": code_lang or "unknown",
                "start_line": code_start,
                "end_line": i,
                "line_count": i - code_start
            })
            in_code = False

    bullet_list_items = sum(1 for l in lines if re.match(r'^\s*[-*+]\s', l))
    numbered_list_items = sum(1 for l in lines if re.match(r'^\s*\d+\.\s', l))

    all_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', markdown)
    images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', markdown)
    external_links = [l for l in all_links if l[1].startswith("http")]

    nav_link_lines = sum(1 for l in lines if len(re.findall(r'\[.*?\]\(.*?\)', l)) >= 2)
    cookie_banner = bool(re.search(
        r'(cookie|consent|accept.*decline|we use cookies|privacy policy.*accept)',
        markdown, re.I
    ))
    boilerplate_patterns = [
        r'(copyright|©|\ball rights reserved\b)',
        r'(subscribe to our newsletter)',
        r'(follow us on|share this article)',
        r'(terms of service|terms and conditions)',
        r'(advertisement|sponsored content)',
    ]
    boilerplate_hits = sum(1 for p in boilerplate_patterns if re.search(p, markdown, re.I))

    line_counts = Counter(l.strip() for l in lines if len(l.strip()) > 20)
    repeated_blocks = [text for text, count in line_counts.items() if count >= 3]

    q = total_chars // 4
    quarters = [
        markdown[0:q], markdown[q:2*q],
        markdown[2*q:3*q], markdown[3*q:]
    ]
    content_density = {
        "q1_words": len(quarters[0].split()),
        "q2_words": len(quarters[1].split()),
        "q3_words": len(quarters[2].split()),
        "q4_words": len(quarters[3].split()),
        "q1_tables": sum(1 for t in tables if t["position_pct"] <= 25),
        "q2_tables": sum(1 for t in tables if 25 < t["position_pct"] <= 50),
        "q3_tables": sum(1 for t in tables if 50 < t["position_pct"] <= 75),
        "q4_tables": sum(1 for t in tables if t["position_pct"] > 75),
    }

    last_500 = markdown.rstrip()[-500:]
    appears_truncated = not any(
        last_500.endswith(end) for end in ['.', '!', '?', '```', '---', '|', '\n\n']
    )

    domain_type = "unknown"
    if url:
        if any(tld in url for tld in [".gov", ".edu", ".mil"]):
            domain_type = "authoritative"
        elif any(tld in url for tld in [".org"]):
            domain_type = "organization"
        elif any(tld in url for tld in [".ac.", ".edu."]):
            domain_type = "academic"
        else:
            domain_type = "commercial"

    return {
        "url": url,
        "title": title,
        "domain_type": domain_type,
        "size": {
            "total_chars": total_chars,
            "total_lines": total_lines,
            "total_words": total_words,
        },
        "structure": {
            "heading_count": len(headings),
            "heading_tree": headings[:15],  # top 15 for conciseness
            "table_count": len(tables),
            "tables": tables,
            "code_block_count": len(code_blocks),
            "code_blocks": code_blocks,
            "bullet_list_items": bullet_list_items,
            "numbered_list_items": numbered_list_items,
            "external_link_count": len(external_links),
            "image_count": len(images),
        },
        "noise": {
            "nav_link_density_lines": nav_link_lines,
            "nav_link_ratio": round(nav_link_lines / max(total_lines, 1), 3),
            "cookie_banner_present": cookie_banner,
            "boilerplate_pattern_count": boilerplate_hits,
            "repeated_blocks": repeated_blocks[:5],
        },
        "content_density": content_density,
        "completeness": {
            "appears_truncated": appears_truncated,
            "last_200_chars": markdown.rstrip()[-200:],
        },
    }


def extract_spot_check_samples(markdown: str) -> dict:
    """Extract 3 raw samples from different positions for formatting verification."""
    if not markdown:
        return {"beginning_sample": "", "middle_sample": "", "structural_sample": ""}
    total = len(markdown)
    if total < 500:
        return {"beginning_sample": markdown, "middle_sample": markdown, "structural_sample": markdown}

    first_heading_end = markdown.find("\n", markdown.find("#"))
    start_sample = markdown[max(0, first_heading_end):first_heading_end + 500] if first_heading_end > 0 else markdown[:500]

    mid = total // 2
    mid_sample = markdown[mid - 250:mid + 250]

    table_match = re.search(r'(\|.+\|[\s\S]{0,300})', markdown)
    structural_sample = table_match.group(0)[:500] if table_match else markdown[3 * total // 4: 3 * total // 4 + 500]

    return {
        "beginning_sample": start_sample,
        "middle_sample": mid_sample,
        "structural_sample": structural_sample,
    }


def detect_result_overlap(profiles: list) -> dict:
    """Detect when multiple search results contain the same information."""
    all_claims = []
    for p in profiles:
        all_claims.extend(p.get("content", {}).get("key_claims", []))

    if not all_claims:
        return {"unique_claim_ratio": 0.0, "duplicated_claims": [], "result_diversity": "low"}

    claim_counts = Counter(all_claims)
    duplicated = [c for c, count in claim_counts.items() if count > 1]

    unique_ratio = round(len(set(all_claims)) / len(all_claims), 3)
    return {
        "unique_claim_ratio": unique_ratio,
        "duplicated_claims": duplicated[:10],
        "result_diversity": "high" if len(duplicated) < 2 else "low" if len(duplicated) > 5 else "medium"
    }


def is_profile_viable(profile: dict) -> bool:
    """Check if a profile has enough content to be worth judging."""
    content = profile.get("content", {})
    structure = profile.get("structure", {})

    has_claims = len(content.get("key_claims", [])) > 0
    has_sections = len(content.get("section_summaries", [])) > 0
    is_error = content.get("content_completeness") in ("error_page", "navigation_only")
    has_substance = structure.get("size", {}).get("total_words", 0) > 50

    return (has_claims or has_sections) and not is_error and has_substance


def enforce_baseline_dimensions(rubric: Optional[EvalRubric]) -> EvalRubric:
    """Ensure all 3 axes (Quality, Ranking, Fidelity) are represented in the rubric."""
    if not rubric or not rubric.dimensions:
        dims = [
            BASELINE_DIMENSIONS["quality"],
            BASELINE_DIMENSIONS["ranking"],
            BASELINE_DIMENSIONS["fidelity"],
        ]
        dims[0].weight = 0.4
        dims[1].weight = 0.3
        dims[2].weight = 0.3
        return EvalRubric(dimensions=dims, grading_notes="Default baseline rubric applied.")

    existing_names_and_criteria = " ".join(
        f"{d.name} {d.criteria}" for d in rubric.dimensions
    ).lower()

    missing_axes = []
    for axis, keywords in [("quality", QUALITY_KEYWORDS), ("ranking", RANKING_KEYWORDS), ("fidelity", FIDELITY_KEYWORDS)]:
        if not any(kw in existing_names_and_criteria for kw in keywords):
            missing_axes.append(axis)

    if not missing_axes:
        return rubric

    new_dims = list(rubric.dimensions)
    total_baseline_weight = len(missing_axes) * 0.15
    scale_factor = (1.0 - total_baseline_weight) / 1.0

    for d in new_dims:
        d.weight = round(d.weight * scale_factor, 3)

    for axis in missing_axes:
        new_dims.append(BASELINE_DIMENSIONS[axis])

    total = sum(d.weight for d in new_dims)
    if total > 0:
        for d in new_dims:
            d.weight = round(d.weight / total, 3)
        new_dims[-1].weight = round(1.0 - sum(d.weight for d in new_dims[:-1]), 3)

    return EvalRubric(dimensions=new_dims, grading_notes=rubric.grading_notes)


def sanity_check(dimension_evals: List[DimensionEval]) -> List[str]:
    warnings = []
    scores = [d.score for d in dimension_evals]
    level_ranges = {
        "L1": (0.0, 0.2), "L2": (0.2, 0.4), "L3": (0.4, 0.6),
        "L4": (0.6, 0.8), "L5": (0.8, 1.0)
    }

    if len(scores) > 1 and len(set(round(s, 1) for s in scores)) == 1:
        warnings.append(f"SUSPICIOUS: All {len(scores)} dimensions scored identically ({scores[0]:.2f})")

    if len(scores) > 1 and all(0.5 <= s <= 0.7 for s in scores):
        warnings.append("SUSPICIOUS: Score compression — all scores in 0.5-0.7 range, full scale unused")

    for d in dimension_evals:
        if d.contrastive_fail_triggered and d.score > 0.4:
            warnings.append(
                f"CONTRADICTION: '{d.dimension_name}' triggered contrastive_fail "
                f"but scored {d.score:.2f} — expected <= 0.40 (L1 or L2)"
            )

    for d in dimension_evals:
        if d.assigned_level in level_ranges:
            lo, hi = level_ranges[d.assigned_level]
            if not (lo - 0.01 <= d.score <= hi + 0.01):
                warnings.append(
                    f"MISMATCH: '{d.dimension_name}' assigned {d.assigned_level} "
                    f"(range {lo:.1f}-{hi:.1f}) but scored {d.score:.2f}"
                )

    return warnings


class Judge:
    def __init__(self, config: EvalConfig, or_pool: OpenRouterClientPool):
        self.config = config
        self.or_pool = or_pool
        self.judge_model = config.judge_model
        self.extraction_model = getattr(config, "extraction_model", "") or config.judge_model
        self._profile_cache: Dict[str, dict] = {}
        self._judge_cache: Dict[str, EvalResult] = {}

    def _parse_json(self, clean_response: str) -> dict:
        clean_response = clean_response.strip()
        if not clean_response:
            return {}

        try:
            return json.loads(clean_response)
        except Exception:
            pass

        first_brace = clean_response.find('{')
        last_brace = clean_response.rfind('}')
        if first_brace != -1 and last_brace > first_brace:
            try:
                return json.loads(clean_response[first_brace:last_brace+1])
            except Exception:
                pass

        json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', clean_response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1).strip())
            except Exception:
                pass

        logger.error(f"[Judge] Failed to parse JSON from response. First 300 chars: {clean_response[:300]}")
        return {}

    async def _extract_content_profile(self, url: str, title: str, full_markdown: str) -> dict:
        if not full_markdown:
            return {
                "primary_topic": "Empty document",
                "page_type": "other",
                "authority_signals": [],
                "key_claims": [],
                "data_points": [],
                "named_entities": {},
                "temporal_markers": [],
                "section_summaries": [],
                "table_contents": [],
                "code_block_purposes": [],
                "content_gaps_or_issues": ["No markdown scraped."],
                "content_completeness": "error_page"
            }

        cache_key = hashlib.sha256(full_markdown.encode("utf-8")).hexdigest()
        if cache_key in self._profile_cache:
            return self._profile_cache[cache_key]

        system_prompt = """You are a Document Intelligence Extractor. Read the document and produce a complete, structured JSON profile.
RULES:
1. Extract ONLY what is explicitly stated in the document. Do NOT infer or paraphrase beyond what is written.
2. Do NOT evaluate quality, relevance, or usefulness.
3. If a field has no applicable content, output an empty list [] or null.
4. For key_claims: each claim must be a single self-contained factual statement that could be verified independently.
5. Extract ALL significant factual claims. Do not cap arbitrarily.
6. Output ONLY a JSON object matching the requested schema."""

        user_prompt = f"""Document URL: {url}
Document Title: {title}

FULL DOCUMENT CONTENT:
{full_markdown}

Extract a complete content profile. Output ONLY a JSON object matching this schema exactly:
{{
  "primary_topic": "<one precise sentence describing what this page is about>",
  "page_type": "<one of: official_documentation | news_article | blog_post | academic_paper | government_page | product_page | forum_thread | reference_database | tutorial | legal_document | other>",
  "authority_signals": ["<observable signal of authority or lack thereof>"],
  "key_claims": ["<atomic factual statement 1>", "<atomic factual statement 2>"],
  "data_points": ["<exact number/measurement/threshold as it appears>"],
  "named_entities": {{
    "people": [],
    "organizations": [],
    "products_drugs_chemicals": [],
    "locations": [],
    "laws_standards_regulations": []
  }},
  "temporal_markers": ["<dates, years, or temporal references found>"],
  "section_summaries": [
    {{"section_heading": "<heading text>", "key_point": "<summary sentence>"}}
  ],
  "table_contents": [
    {{"description": "<table purpose>", "key_data": "<most important row/data>"}}
  ],
  "code_block_purposes": ["<purpose of code block>"],
  "content_gaps_or_issues": ["<any observable issue or cut off content>"],
  "content_completeness": "<one of: complete | appears_truncated | partial | navigation_only | error_page>"
}}"""

        try:
            resp = await self.or_pool.generate(
                prompt=user_prompt,
                model=self.extraction_model,
                temperature=0.0,
                max_tokens=8192,
                system_prompt=system_prompt,
                response_format={"type": "json_object"}
            )
            parsed = self._parse_json(resp)
            if parsed:
                self._profile_cache[cache_key] = parsed
                return parsed
        except Exception as e:
            logger.warning(f"[Judge] Profile extraction failed for {url}: {e}")

        fallback = {
            "primary_topic": title or "Unknown document",
            "page_type": "other",
            "authority_signals": [],
            "key_claims": [],
            "data_points": [],
            "named_entities": {},
            "temporal_markers": [],
            "section_summaries": [],
            "table_contents": [],
            "code_block_purposes": [],
            "content_gaps_or_issues": ["Profile extraction error fallback."],
            "content_completeness": "partial"
        }
        self._profile_cache[cache_key] = fallback
        return fallback

    async def _build_document_profile(self, sr: FirecrawlSearchResult) -> dict:
        md = sr.full_markdown or sr.snippet or ""
        structure = extract_structure_profile(md, sr.url, sr.title)
        spot_checks = extract_spot_check_samples(md)
        content = await self._extract_content_profile(sr.url, sr.title, md)
        return {
            "rank": sr.firecrawl_rank,
            "url": sr.url,
            "title": sr.title,
            "structure": structure,
            "content": content,
            "spot_check_samples": spot_checks
        }

    async def _evaluate_dimension(
        self,
        test_case: TestCase,
        dimension: RubricDimension,
        profiles: List[dict],
        diversity_info: dict
    ) -> DimensionEval:
        viable_profiles = [p for p in profiles if is_profile_viable(p)]
        if not viable_profiles:
            return DimensionEval(
                dimension_name=dimension.name,
                weight=dimension.weight,
                evidence_found=["No viable document profiles found — all pages empty or error pages."],
                criteria_checklist=[CriteriaCheck(condition=dimension.criteria, status="NOT_MET", evidence="No content scraped.")],
                contrastive_fail_triggered=True,
                contrastive_fail_explanation="All scraped pages were empty or unviable.",
                assigned_level="L1",
                level_justification="L1 because zero viable content was retrieved.",
                score=0.1,
                reasoning="Failed because no viable content was scraped across any result."
            )

        system_prompt = """You are a SEARCH & SCRAPE EVALUATION JUDGE. You evaluate one specific rubric dimension at a time.
YOUR RULES:
1. Base every statement on evidence from the Document Profiles.
2. Follow all 5 steps IN ORDER before outputting the final JSON.
3. Assign a level (L1-L5) before picking a score. The score MUST fall within the level's range.
4. The Contrastive Fail Check is MANDATORY. If contrastive_fail triggers, level CANNOT be L4 or L5.
5. You MUST justify why you chose your level and not adjacent ones.
6. Output ONLY a valid JSON object."""

        is_ranking_dim = any(kw in dimension.name.lower() for kw in RANKING_KEYWORDS)

        profiles_context = json.dumps(profiles, indent=2)
        if is_ranking_dim:
            ranking_table = "RESULTS IN FIRECRAWL'S ORIGINAL ORDER (evaluate optimal ordering):\n"
            for p in sorted(profiles, key=lambda x: x.get("rank", 99)):
                c = p.get("content", {})
                s = p.get("structure", {})
                ranking_table += f"[RANK {p.get('rank', '-')}] {p.get('url', 'N/A')}\n"
                ranking_table += f"  Domain type:       {p.get('domain_type', 'unknown')}\n"
                ranking_table += f"  Page type:         {c.get('page_type', 'other')}\n"
                ranking_table += f"  Authority signals: {c.get('authority_signals', [])}\n"
                ranking_table += f"  Claims extracted:  {len(c.get('key_claims', []))}\n"
                ranking_table += f"  Data points:       {len(c.get('data_points', []))}\n"
                ranking_table += f"  Tables:            {s.get('table_count', 0)}\n"
                ranking_table += f"  Noise ratio:       {s.get('noise', {}).get('nav_link_ratio', 0.0)}\n"
                ranking_table += f"  Completeness:      {c.get('content_completeness', 'unknown')}\n"
                ranking_table += f"  Primary topic:     {c.get('primary_topic', '')}\n\n"
            profiles_context = ranking_table + "\nDETAILED DOCUMENT PROFILES:\n" + profiles_context

        difficulty_context = f"""DIFFICULTY CONTEXT:
  Difficulty: {test_case.difficulty} | Chaos Archetype: {getattr(test_case, 'chaos_archetype', 'none')}
  - For hard queries: L3 (Partial) may represent genuinely good system performance.
  - Calibrate expectations but do NOT inflate scores."""

        user_prompt = f"""EVALUATION CONTEXT
Query:           {test_case.query}
Intent:          {test_case.intent}
Difficulty:      {test_case.difficulty}
Result Diversity: {diversity_info.get('result_diversity')} ({diversity_info.get('unique_claim_ratio')} unique claim ratio)

DIMENSION TO EVALUATE:
  Name:             {dimension.name}
  Weight in Rubric: {dimension.weight}
  Criteria:
    {dimension.criteria}
  Contrastive Fail (calibration anchor):
    {dimension.contrastive_fail}

GRADING NOTES FROM TEST AUTHOR:
  {getattr(test_case.rubric, 'grading_notes', '') if test_case.rubric else ''}

{difficulty_context}

DOCUMENT PROFILES:
{profiles_context}

SCORING LEVELS:
  L1 [0.00–0.20] CRITICAL FAILURE  -> Criteria almost entirely unmet. contrastive_fail matches.
  L2 [0.20–0.40] MAJOR DEFICIENCY  -> Some relevance, but core requirement unmet.
  L3 [0.40–0.60] PARTIAL           -> Most important condition met, but notable gaps.
  L4 [0.60–0.80] ADEQUATE          -> Mostly met, minor gaps. contrastive_fail does NOT match.
  L5 [0.80–1.00] EXCELLENT         -> Fully or near-fully met. Strong evidence.

EXECUTE THESE 5 STEPS AND OUTPUT JSON:
{{
  "step1_evidence_found": ["<exact quote or structural fact from profiles>"],
  "step2_criteria_checklist": [
    {{"condition": "<condition text>", "status": "MET|PARTIALLY_MET|NOT_MET", "evidence": "<supporting quote>"}}
  ],
  "step3_contrastive_fail_triggered": true,
  "step3_contrastive_fail_explanation": "<specific explanation citing evidence>",
  "step4_assigned_level": "L1|L2|L3|L4|L5",
  "step4_level_justification": "<why this level AND NOT adjacent level(s)>",
  "step5_score": 0.75,
  "summary_reasoning": "<1-2 sentence plain-English summary of decision>"
}}"""

        try:
            resp = await self.or_pool.generate(
                prompt=user_prompt,
                model=self.judge_model,
                temperature=0.0,
                max_tokens=3500,
                system_prompt=system_prompt,
                response_format={"type": "json_object"}
            )
            data = self._parse_json(resp)
            if data and "step5_score" in data:
                level = data.get("step4_assigned_level", "L3")
                score = float(data.get("step5_score", 0.5))
                # Ensure score is within range [0.0, 1.0]
                score = max(0.0, min(1.0, score))
                checks = [
                    CriteriaCheck(
                        condition=c.get("condition", ""),
                        status=c.get("status", "PARTIALLY_MET"),
                        evidence=c.get("evidence", "")
                    )
                    for c in data.get("step2_criteria_checklist", [])
                ]
                return DimensionEval(
                    dimension_name=dimension.name,
                    weight=dimension.weight,
                    evidence_found=data.get("step1_evidence_found", []),
                    criteria_checklist=checks,
                    contrastive_fail_triggered=bool(data.get("step3_contrastive_fail_triggered", False)),
                    contrastive_fail_explanation=data.get("step3_contrastive_fail_explanation", ""),
                    assigned_level=level,
                    level_justification=data.get("step4_level_justification", ""),
                    score=score,
                    reasoning=data.get("summary_reasoning", f"Scored {score:.2f} on {dimension.name}")
                )
        except Exception as e:
            logger.warning(f"[Judge] Dimension evaluation failed for {dimension.name}: {e}")

        # Fallback evaluation
        return DimensionEval(
            dimension_name=dimension.name,
            weight=dimension.weight,
            evidence_found=["Fallback evaluation used due to LLM parsing/generation error."],
            criteria_checklist=[CriteriaCheck(condition=dimension.criteria, status="PARTIALLY_MET", evidence="Fallback")],
            contrastive_fail_triggered=False,
            contrastive_fail_explanation="Fallback triggered.",
            assigned_level="L3",
            level_justification="Fallback default L3.",
            score=0.5,
            reasoning=f"Default score assigned for {dimension.name} due to evaluation error."
        )

    async def evaluate(self, test_case: TestCase, search_results: list[FirecrawlSearchResult]) -> EvalResult:
        logger.info(f"Evaluating tc: {test_case.id} with Extract-then-Evaluate two-phase Judge...")

        rubric_str = str([(d.name, d.weight) for d in test_case.rubric.dimensions]) if getattr(test_case, "rubric", None) else ""
        content_str = "|".join(sorted([hashlib.sha256((r.full_markdown or "").encode()).hexdigest()[:16] for r in search_results]))
        cache_str = f"{test_case.query}|{rubric_str}|{content_str}"
        cache_key = hashlib.sha256(cache_str.encode("utf-8")).hexdigest()
        if cache_key in self._judge_cache:
            logger.info(f"[Judge] Cache hit for {test_case.id}")
            return self._judge_cache[cache_key]

        # Phase 1: Build Document Profiles in parallel across URLs
        profiles = await asyncio.gather(*(self._build_document_profile(sr) for sr in search_results))
        diversity_info = detect_result_overlap(profiles)

        # Enforce baseline dimensions on rubric
        rubric = enforce_baseline_dimensions(getattr(test_case, "rubric", None))

        # Phase 2: Evaluate each Rubric Dimension in parallel
        dim_evals = await asyncio.gather(*(
            self._evaluate_dimension(test_case, dim, profiles, diversity_info)
            for dim in rubric.dimensions
        ))

        # Phase 3: Aggregation using rubric weights
        total_score = sum(de.weight * de.score for de in dim_evals)
        total_score = round(max(0.0, min(1.0, total_score)), 4)

        warnings = sanity_check(dim_evals)
        for w in warnings:
            logger.warning(f"[Judge] TC {test_case.id} — {w}")

        result = EvalResult(
            test_case_id=test_case.id,
            dimension_evals=list(dim_evals),
            overall_score=total_score,
            document_profiles=list(profiles),
            warnings=warnings,
            result_diversity=diversity_info
        )

        self._judge_cache[cache_key] = result
        return result
