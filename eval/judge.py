import json
import logging
import asyncio
import hashlib
import os
import re
import copy
from typing import Dict, Any, List, Optional
from collections import Counter

from models.test_case import TestCase, RubricDimension, EvalRubric
from models.eval_result import (
    FirecrawlSearchResult,
    CriteriaCheck,
    DimensionEval,
    EvalResult,
    P1Result
)
from clients.openrouter import OpenRouterClientPool
from config import EvalConfig

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)

# Numeric band for each scoring level
LEVEL_RANGES: dict[str, tuple[float, float]] = {
    "L1": (0.00, 0.20),
    "L2": (0.20, 0.40),
    "L3": (0.40, 0.60),
    "L4": (0.60, 0.80),
    "L5": (0.80, 1.00),
}

BASELINE_DIMENSIONS = {
    "fidelity": RubricDimension(
        name="_baseline_fidelity",
        weight=0.12,
        criteria="Scraped markdown preserves the page's structural elements and content is complete without boilerplate leakage.",
        contrastive_fail="Fails if tables are flattened, content is truncated, or navigation noise dominates."
    ),
    "ranking": RubricDimension(
        name="_baseline_ranking",
        weight=0.12,
        criteria="Higher-authority and more relevant sources appear before lower-quality ones.",
        contrastive_fail="Fails if blogs rank above official sources, or if most relevant result is buried."
    ),
    "coverage": RubricDimension(
        name="_baseline_coverage",
        weight=0.12,
        criteria="Search results collectively contain the information the query requires and address the intent.",
        contrastive_fail="Fails if critical information gaps exist across all results."
    ),
    "authority": RubricDimension(
        name="_baseline_authority",
        weight=0.07,
        criteria="The portfolio of sources is credible and appropriate for this query type.",
        contrastive_fail="Fails if untrustworthy or low-credibility sources are given undue weight."
    ),
    "freshness": RubricDimension(
        name="_baseline_freshness",
        weight=0.07,
        criteria="Content is temporally appropriate for the query.",
        contrastive_fail="Fails if results are outdated for a time-sensitive query."
    ),
}

AUTHORITATIVE_TLDS = [
    ".gov", ".mil", ".go.jp", ".lg.jp", ".gc.ca",
    ".gov.uk", ".mod.uk", ".nhs.uk", ".gouv.fr",
    ".gob.mx", ".gob.es", ".gob.ar", ".gov.au", ".csiro.au",
    ".govt.nz", ".gov.in", ".admin.ch", ".bund.de",
    ".europa.eu", ".un.org", ".who.int", ".ilo.org",
    ".nato.int", ".imf.org", ".worldbank.org",
]
ACADEMIC_TLDS = [".edu", ".ac.uk", ".ac.jp", ".edu.au", ".ac.nz"]
ORG_TLDS = [".org"]

def _classify_domain_type(url: str) -> str:
    if not url:
        return "unknown"
    url_lower = url.lower()
    if any(tld in url_lower for tld in AUTHORITATIVE_TLDS):
        return "authoritative"
    if any(tld in url_lower for tld in ACADEMIC_TLDS):
        return "academic"
    if any(tld in url_lower for tld in ORG_TLDS):
        return "organization"
    return "commercial"

def _clamp_score_to_level(level: str, score: float) -> float:
    score = max(0.0, min(1.0, score))
    if level in LEVEL_RANGES:
        lo, hi = LEVEL_RANGES[level]
        if not (lo - 0.01 <= score <= hi + 0.01):
            clamped = max(lo, min(hi, score))
            logger.warning(
                f"[Judge] Level/score mismatch: level={level} ({lo:.1f}–{hi:.1f}) but score={score:.2f}. "
                f"Clamping to {clamped:.2f}."
            )
            return clamped
    return score

def _validate_p1_consistency(result: P1Result) -> P1Result:
    """
    Deterministic post-processor. Enforces logical constraints the model should uphold
    from goal-framing alone, but may occasionally violate. Does not substitute for
    prompt quality — it's the hard backstop only.
    """
    if result.content_completeness in ("navigation_only", "error_page"):
        result.key_claims = []
        result.data_points = []
        result.scrape_score = min(result.scrape_score, 0.20)
        result.scrape_level = "L1" if result.scrape_score <= 0.20 else result.scrape_level
        result.query_relevance_score = min(result.query_relevance_score, 0.10)

    if result.word_count < 150:
        result.key_claims = result.key_claims[:2]
        result.section_summaries = result.section_summaries[:1]

    if result.authority_score > 0.7 and not result.authority_assessment.strip():
        result.authority_score = 0.5

    if result.scrape_level == "L5" and result.content_completeness in ("appears_truncated", "partial"):
        result.scrape_level = "L4"
        result.scrape_score = min(result.scrape_score, 0.79)

    if result.detected_language not in ("en", "mixed", "en-US", "en-GB", ""):
        result.query_relevance_score = 0.0

    return result

def enforce_baseline_dimensions(rubric: Optional[EvalRubric]) -> EvalRubric:
    if not rubric or not rubric.dimensions:
        dims = [
            copy.deepcopy(BASELINE_DIMENSIONS["fidelity"]),
            copy.deepcopy(BASELINE_DIMENSIONS["ranking"]),
            copy.deepcopy(BASELINE_DIMENSIONS["coverage"]),
            copy.deepcopy(BASELINE_DIMENSIONS["authority"]),
            copy.deepcopy(BASELINE_DIMENSIONS["freshness"]),
        ]
        # weights sum to 0.5; normalize to 1.0
        for d in dims:
            d.weight = d.weight * 2
        return EvalRubric(dimensions=dims, grading_notes="Default baseline rubric applied.")

    existing_names = [d.name.lower() for d in rubric.dimensions]
    
    missing_axes = []
    if not any("fidelity" in n or "scrape" in n for n in existing_names):
        missing_axes.append("fidelity")
    if not any("ranking" in n or "ordering" in n for n in existing_names):
        missing_axes.append("ranking")
    if not any("coverage" in n or "completeness" in n for n in existing_names):
        missing_axes.append("coverage")
    if not any("authority" in n or "credibility" in n for n in existing_names):
        missing_axes.append("authority")
    if not any("freshness" in n or "temporal" in n for n in existing_names):
        missing_axes.append("freshness")

    if not missing_axes:
        return rubric

    new_dims = list(rubric.dimensions)
    total_baseline_weight = sum(BASELINE_DIMENSIONS[axis].weight for axis in missing_axes)
    scale_factor = (1.0 - total_baseline_weight) / 1.0

    for d in new_dims:
        d.weight = round(d.weight * scale_factor, 3)

    for axis in missing_axes:
        new_dims.append(copy.deepcopy(BASELINE_DIMENSIONS[axis]))

    total = sum(d.weight for d in new_dims)
    if total > 0:
        for d in new_dims:
            d.weight = round(d.weight / total, 3)
        new_dims[-1].weight = round(1.0 - sum(d.weight for d in new_dims[:-1]), 3)

    return EvalRubric(dimensions=new_dims, grading_notes=rubric.grading_notes)

def sanity_check(dimension_evals: List[DimensionEval]) -> List[str]:
    warnings = []
    scores = [d.score for d in dimension_evals if not d.is_fallback]
    
    if any(d.is_fallback for d in dimension_evals):
        warnings.append("WARNING: One or more dimensions used a fallback evaluation due to errors.")

    if len(scores) > 1 and len(set(round(s, 1) for s in scores)) == 1:
        warnings.append(f"SUSPICIOUS: All {len(scores)} valid dimensions scored identically ({scores[0]:.2f})")

    if len(scores) > 1 and all(0.5 <= s <= 0.7 for s in scores):
        warnings.append("SUSPICIOUS: Score compression — all scores in 0.5-0.7 range, full scale unused")

    for d in dimension_evals:
        if d.is_fallback:
            continue
        if d.contrastive_fail_triggered and d.score > 0.4:
            warnings.append(
                f"CONTRADICTION: '{d.dimension_name}' triggered contrastive_fail "
                f"but scored {d.score:.2f} — expected <= 0.40 (L1 or L2)"
            )
        if d.assigned_level in LEVEL_RANGES:
            lo, hi = LEVEL_RANGES[d.assigned_level]
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
        self.p1_model = config.p1_model
        self.p2_model = config.p2_model
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

        repaired = self._repair_truncated_json(clean_response)
        if repaired:
            logger.warning("[Judge] Recovered JSON via truncation repair.")
            return repaired

        logger.error(f"[Judge] Failed to parse JSON from response. First 300 chars: {clean_response[:300]}")
        return {}

    def _repair_truncated_json(self, s: str) -> dict:
        first_brace = s.find('{')
        if first_brace == -1:
            return {}
        s = s[first_brace:]

        depth_brace = 0
        depth_bracket = 0
        in_string = False
        escape_next = False

        for ch in s:
            if escape_next:
                escape_next = False
                continue
            if ch == '\\' and in_string:
                escape_next = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == '{':
                depth_brace += 1
            elif ch == '}':
                depth_brace = max(0, depth_brace - 1)
            elif ch == '[':
                depth_bracket += 1
            elif ch == ']':
                depth_bracket = max(0, depth_bracket - 1)

        if in_string:
            s += '"'
        s += ']' * depth_bracket + '}' * depth_brace

        try:
            return json.loads(s)
        except Exception:
            return {}

    async def _run_p1_agent(self, sr: FirecrawlSearchResult, query: str, intent: str, domain_type: str) -> P1Result:
        full_markdown = sr.full_markdown or sr.snippet or ""
        word_count = len(full_markdown.split())
        
        fallback = P1Result(
            rank=sr.firecrawl_rank,
            url=sr.url,
            domain_type=domain_type,
            scrape_score=0.0,
            scrape_level="L1",
            scrape_issues=["P1 evaluation failed"],
            scrape_reasoning="Failed to execute P1 agent.",
            primary_topic=sr.title or "Unknown",
            page_type="other",
            authority_assessment="Unknown",
            author_credentials="",
            key_claims=[],
            data_points=[],
            named_entities={},
            temporal_markers=[],
            section_summaries=[],
            table_contents=[],
            content_completeness="error_page",
            content_gaps=[],
            word_count=word_count,
            is_fallback=True,
            fallback_reason="Exception or parsing error in P1 agent"
        )
        
        if not full_markdown:
            fallback.fallback_reason = "Empty document content"
            return fallback

        system_prompt = """You are a document analyst for a search evaluation pipeline. A user searched for a specific query.
One of the scraped results has been given to you. Your job is to produce two things:

1. SCRAPE QUALITY VERDICT: An honest assessment of how faithfully this markdown preserves the
   original page. Think: would someone reading this markdown get the same information as someone
   reading the live page? Score 0.0–1.0 with a level (L1–L5) and count the structural elements
   you observe (tables, headings, lists, code blocks, navigation links, boilerplate blocks).

2. CONTENT INTELLIGENCE PROFILE: A factual evidence record of what this document contains — for
   use by downstream judges who will cite your extraction verbatim. Be thorough on facts and
   disciplined about what you claim to know. Extract only what is explicitly present in the text.
   If a field has no evidence, return empty — never infer or fabricate.

GUARDRAILS (non-obvious conventions, apply carefully):
- key_claims: Extract a MINIMUM of 5 atomic factual statements per document if the content 
  supports it. Each claim must be a self-contained sentence with a subject, predicate, and 
  specific object — never a topic label.
- temporal_markers: Extract ALL explicit, specific date references from the full body text 
  (e.g. "Q3 2026", "March 15 2026", "as of 2025-04-01"). Do not restrict to headings. 
  If you find a date in a table row, a footnote, or a citation, include it.
- publication_date: If the page has no explicit publish date in metadata, check for 
  "Last updated:", "Published on:", or date strings adjacent to the byline or article header.
- detected_language: If content is mixed-language, return "mixed" regardless of which language
  dominates. Do not default to the majority language."""

        user_prompt = f"""Document URL: {sr.url}
Document Title: {sr.title}
Query/Intent Context: '{query}' ({intent})

FULL DOCUMENT CONTENT:
{full_markdown}

---
CLASSIFICATION CONTEXT (reference only — your content reading takes precedence):
Pre-classified domain type: {domain_type}

Output ONLY a JSON object matching this schema exactly:
{{
  "scrape_score": <float 0.0-1.0>,
  "scrape_level": "<L1|L2|L3|L4|L5>",
  "scrape_issues": ["<specific issue 1>", "<specific issue 2>"],
  "scrape_reasoning": "<1-2 sentences explaining score>",
  "nav_link_ratio": <float 0.0-1.0>,
  "boilerplate_pattern_count": <int 0-10>,
  "table_count": <int>,
  "heading_count": <int>,
  "list_count": <int>,
  "code_block_count": <int>,
  "primary_topic": "<one precise sentence describing what this page is about>",
  "page_type": "<one of: official_documentation | news_article | blog_post | academic_paper | government_page | product_page | forum_thread | reference_database | tutorial | legal_document | other>",
  "publication_date": "<YYYY-MM-DD or YYYY-MM or YYYY or ''>",
  "query_relevance_score": <float 0.0-1.0>,
  "detected_language": "<ISO 639-1 code or 'mixed'>",
  "authority_assessment": "<narrative assessment of credibility>",
  "authority_score": <float 0.0-1.0>,
  "author_credentials": "<any professional credentials visible>",
  "key_claims": ["<atomic factual statement 1>", "<atomic factual statement 2>"],
  "data_points": ["<exact number/measurement/threshold as it appears>"],
  "named_entities": {{
    "people": [],
    "organizations": [],
    "products_drugs_chemicals": [],
    "locations": [],
    "laws_standards_regulations": []
  }},
  "temporal_markers": ["<dates, years, or explicit temporal references>"],
  "section_summaries": [
    {{"section_heading": "<heading text>", "key_point": "<summary sentence>"}}
  ],
  "table_contents": [
    {{"description": "<table purpose>", "key_data": "<most important row/data>"}}
  ],
  "content_completeness": "<one of: complete | appears_truncated | partial | navigation_only | error_page>",
  "content_gaps": [
    {{"gap": "<what is missing>", "severity": "critical|moderate|minor"}}
  ],
  "query_coverage_assessment": {{
    "answers_query": true,
    "coverage_level": "<full | partial | tangential | none>",
    "missing_aspects": ["<what the query asks for that this doc doesn't address>"]
  }}
}}"""

        max_retries = getattr(self.config, 'judge_max_retries', 2)
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                retry_prefix = ""
                if attempt > 0 and last_error:
                    logger.warning(f"[Judge] P1 Agent retrying (attempt {attempt+1}/{max_retries+1}) due to: {last_error}")
                    retry_prefix = (
                        f"Your previous response was rejected for this reason: {last_error}\n"
                        "Try again. Output ONLY a valid JSON object — no markdown, no commentary. \n\n"
                    )
                    
                resp, was_truncated = await self.or_pool.generate(
                    prompt=retry_prefix + user_prompt,
                    model=self.p1_model,
                    temperature=0.0,
                    max_tokens=None,
                    system_prompt=system_prompt,
                    response_format={"type": "json_object"},
                    providers=self.config.p1_providers
                )
                
                if was_truncated:
                    logger.warning(f"[Judge] P1 Agent output was truncated for {sr.url}")

                data = self._parse_json(resp)
                if not data:
                    last_error = "Response could not be parsed as valid JSON."
                    continue # Retry on empty data
                    
                score = _clamp_score_to_level(data.get("scrape_level", "L3"), float(data.get("scrape_score", 0.5)))
                res = P1Result(
                    rank=sr.firecrawl_rank,
                    url=sr.url,
                    domain_type=domain_type,
                    scrape_score=score,
                    scrape_level=data.get("scrape_level", "L3"),
                    scrape_issues=data.get("scrape_issues", []),
                    scrape_reasoning=data.get("scrape_reasoning", ""),
                    nav_link_ratio=float(data.get("nav_link_ratio", 0.0)),
                    boilerplate_pattern_count=int(data.get("boilerplate_pattern_count", 0)),
                    table_count=int(data.get("table_count", 0)),
                    heading_count=int(data.get("heading_count", 0)),
                    list_count=int(data.get("list_count", 0)),
                    code_block_count=int(data.get("code_block_count", 0)),
                    primary_topic=data.get("primary_topic", sr.title or "Unknown"),
                    page_type=data.get("page_type", "other"),
                    publication_date=data.get("publication_date", ""),
                    query_relevance_score=float(data.get("query_relevance_score", 0.0)),
                    detected_language=data.get("detected_language", "en"),
                    authority_assessment=data.get("authority_assessment", "Unknown"),
                    authority_score=float(data.get("authority_score", 0.0)),
                    author_credentials=data.get("author_credentials", ""),
                    key_claims=data.get("key_claims", []),
                    data_points=data.get("data_points", []),
                    named_entities=data.get("named_entities", {}),
                    temporal_markers=data.get("temporal_markers", []),
                    section_summaries=data.get("section_summaries", []),
                    table_contents=data.get("table_contents", []),
                    content_completeness=data.get("content_completeness", "partial"),
                    content_gaps=data.get("content_gaps", []),
                    word_count=word_count,
                    query_coverage_assessment=data.get("query_coverage_assessment", None),
                    is_fallback=False
                )
                return _validate_p1_consistency(res)
            except Exception as e:
                logger.warning(f"[Judge] P1 Agent exception for {sr.url}: {e}")
                last_error = str(e)
                # We do not continue here if it's a structural exception that might not resolve,
                # but since we are wrapping in retry loop, we might as well let it loop.
                if attempt == max_retries:
                    fallback.fallback_reason = str(e)
            
        return fallback

    def _route_dimensions(self, rubric: EvalRubric) -> Dict[str, List[RubricDimension]]:
        routes = {
            "ranking": [],
            "coverage": [],
            "authority": [],
            "freshness": [],
            "precision": []
        }
        
        for dim in rubric.dimensions:
            text = f"{dim.name} {dim.criteria}".lower()
            if any(kw in text for kw in ["ranking", "ordering", "priority", "position", "result order", "rank"]):
                routes["ranking"].append(dim)
            elif any(kw in text for kw in ["authority", "credibility", "trustworthy", "source quality", "expert", "official", "credentials"]):
                routes["authority"].append(dim)
            elif any(kw in text for kw in ["temporal", "freshness", "recency", "current", "recent", "date", "latest", "updated", "real.time"]):
                routes["freshness"].append(dim)
            elif any(kw in text for kw in ["accuracy", "numerical", "factual", "precision", "statistics", "data", "measurement", "consistent"]):
                routes["precision"].append(dim)
            else:
                routes["coverage"].append(dim)
                
        return routes

    def _aggregate_fidelity(self, p1_results: List[P1Result], rubric: EvalRubric) -> Optional[DimensionEval]:
        fid_dim = next((d for d in rubric.dimensions if d.name == "_baseline_fidelity" or "fidelity" in d.name.lower() or "scrape" in d.name.lower()), None)
        if not fid_dim:
            return None
            
        if not p1_results:
            return DimensionEval(
                dimension_name=fid_dim.name,
                weight=fid_dim.weight,
                evidence_found=["No results to evaluate"],
                criteria_checklist=[CriteriaCheck(condition=fid_dim.criteria, status="NOT_MET", evidence="Empty results")],
                contrastive_fail_triggered=True,
                contrastive_fail_explanation="No results provided",
                assigned_level="L1",
                level_justification="No content",
                score=0.0,
                reasoning="No results scraped"
            )
            
        scores = [p.scrape_score for p in p1_results]
        mean_score = sum(scores) / len(scores)
        floor_score = min(scores)
        avg_score = round(0.70 * mean_score + 0.30 * floor_score, 4)
        
        assigned_level = "L1"
        for lvl, (lo, hi) in LEVEL_RANGES.items():
            if lo <= avg_score < hi:
                assigned_level = lvl
                break
        if avg_score >= 1.0:
            assigned_level = "L5"
                
        evidence_found = []
        for p in p1_results:
            if p.is_fallback:
                evidence_found.append(f"Rank {p.rank}: {p.url} — P1 evaluation failed ({p.fallback_reason})")
            else:
                evidence_found.append(f"Rank {p.rank}: {p.url} — scrape_score={p.scrape_score:.2f}, issues={p.scrape_issues}")
                
        checks = []
        for p in p1_results:
            status = "MET" if p.scrape_score >= 0.6 else ("PARTIALLY_MET" if p.scrape_score >= 0.3 else "NOT_MET")
            checks.append(CriteriaCheck(
                condition=f"URL rank {p.rank}: {p.url}",
                status=status,
                evidence=f"score={p.scrape_score:.2f}, issues={p.scrape_issues[:2]}"
            ))
                
        return DimensionEval(
            dimension_name=fid_dim.name,
            weight=fid_dim.weight,
            evidence_found=evidence_found,
            criteria_checklist=checks,
            contrastive_fail_triggered=(avg_score < 0.4),
            contrastive_fail_explanation="Average scrape quality is poor" if avg_score < 0.4 else "",
            assigned_level=assigned_level,
            level_justification=f"Computed average score is {avg_score:.2f}",
            score=avg_score,
            reasoning=f"Aggregated fidelity score from {len(p1_results)} pages."
        )

    async def _run_p2_judge(self, judge_type: str, p1_results: List[P1Result], test_case: TestCase, dims: List[RubricDimension]) -> List[DimensionEval]:
        if not dims:
            return []
            
        system_prompt = f"""You are a specialized search result evaluator focused on {judge_type.upper()} quality.

You have been given verified content profiles for each retrieved document (extracted by a P1 agent),
and a set of rubric dimensions that define what "good" looks like for this specific query.

Your task: make calibrated, evidence-based judgments on each dimension. For each one, decide
whether the retrieved documents collectively satisfy it, partially satisfy it, or fail it — then
express that as a precise score and level. Cite the specific evidence from the profiles that
drove your decision.

The scoring levels (L1–L5) are ranges, not labels. Choose the level that best describes the
quality, then pick the most precise score within that range. If the contrastive_fail description
matches what you observe, the result cannot score in L4 or L5 — but make that determination
from reading the evidence, not as a rule to follow mechanically.

A key signal in each profile: query_relevance_score. A document scoring < 0.3 was assessed
by the P1 agent as largely irrelevant to the query — weight evidence from such documents
accordingly when judging coverage and precision dimensions.

When document profiles contain conflicting signals on the same dimension (e.g., one
document has authority_score=0.9 while another has 0.2), do not average them silently.
Identify the conflict in step1_evidence_found, state which document you are deferring to
and why, and reflect the conflict in step4_level_justification.

Output ONLY a valid JSON object in the format below."""

        import dataclasses
        profiles_json = json.dumps([dataclasses.asdict(p) for p in p1_results], indent=2)
        dims_json = json.dumps([{"name": d.name, "weight": d.weight, "criteria": d.criteria, "contrastive_fail": d.contrastive_fail} for d in dims], indent=2)

        user_prompt = f"""EVALUATION CONTEXT
Query:           {test_case.query}
Intent:          {test_case.intent}
Difficulty:      {test_case.difficulty}

DIMENSIONS TO EVALUATE:
{dims_json}

GRADING NOTES FROM TEST AUTHOR:
  {getattr(test_case.rubric, 'grading_notes', '') if test_case.rubric else ''}

DOCUMENT PROFILES (from P1 Agents):
{profiles_json}

SCORING LEVELS:
  L1 [0.00–0.20] CRITICAL FAILURE
  L2 [0.20–0.40] MAJOR DEFICIENCY
  L3 [0.40–0.60] PARTIAL
  L4 [0.60–0.80] ADEQUATE
  L5 [0.80–1.00] EXCELLENT

OUTPUT FORMAT:
{{
  "evaluations": [
    {{
      "dimension_name": "<name>",
      "step1_evidence_found": ["<quote>"],
      "step2_criteria_checklist": [
        {{"condition": "<condition text>", "status": "MET|PARTIALLY_MET|NOT_MET", "evidence": "<supporting quote>"}}
      ],
      "step3_contrastive_fail_triggered": true|false,
      "step3_contrastive_fail_explanation": "<explanation>",
      "step4_assigned_level": "L1|L2|L3|L4|L5",
      "step4_level_justification": "<justification>",
      "step5_score": 0.75,
      "summary_reasoning": "<summary>"
    }}
  ]
}}"""

        results = []
        max_retries = getattr(self.config, 'judge_max_retries', 2)
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                retry_prefix = ""
                if attempt > 0 and last_error:
                    logger.warning(f"[Judge] P2 Judge '{judge_type}' retrying (attempt {attempt+1}/{max_retries+1}) due to: {last_error}")
                    retry_prefix = (
                        f"Your previous response was rejected for this reason: {last_error}\n"
                        "Try again. Output ONLY a valid JSON object — no markdown, no commentary. \n\n"
                    )

                resp, was_truncated = await self.or_pool.generate(
                    prompt=retry_prefix + user_prompt,
                    model=self.p2_model,
                    temperature=0.0,
                    max_tokens=None,
                    system_prompt=system_prompt,
                    response_format={"type": "json_object"},
                    providers=self.config.p2_providers
                )
                
                if was_truncated:
                    logger.warning(f"[Judge] P2 Judge '{judge_type}' output was truncated.")

                data = self._parse_json(resp)
                if not data:
                    last_error = "Response could not be parsed as valid JSON."
                    continue
                    
                evals = data.get("evaluations", [])
                for e in evals:
                    dim_name = e.get("dimension_name")
                    dim = next((d for d in dims if d.name == dim_name), None)
                    if not dim:
                        continue
                    level = e.get("step4_assigned_level", "L3")
                    score = _clamp_score_to_level(level, float(e.get("step5_score", 0.5)))
                    
                    checks = [
                        CriteriaCheck(
                            condition=c.get("condition", ""),
                            status=c.get("status", "PARTIALLY_MET"),
                            evidence=c.get("evidence", "")
                        )
                        for c in e.get("step2_criteria_checklist", [])
                    ]
                    
                    results.append(DimensionEval(
                        dimension_name=dim.name,
                        weight=dim.weight,
                        evidence_found=e.get("step1_evidence_found", []),
                        criteria_checklist=checks,
                        contrastive_fail_triggered=bool(e.get("step3_contrastive_fail_triggered", False)),
                        contrastive_fail_explanation=e.get("step3_contrastive_fail_explanation", ""),
                        assigned_level=level,
                        level_justification=e.get("step4_level_justification", ""),
                        score=score,
                        reasoning=e.get("summary_reasoning", "")
                    ))
                # Success, break out of retry loop
                return results
            except Exception as ex:
                logger.warning(f"[Judge] {judge_type} evaluation exception: {ex}")
                last_error = str(ex)
                if attempt == max_retries:
                    # After all retries have failed, yield fallbacks
                    for dim in dims:
                        results.append(DimensionEval(
                            dimension_name=dim.name,
                            weight=dim.weight,
                            evidence_found=["P2 Judge failure"],
                            criteria_checklist=[],
                            contrastive_fail_triggered=False,
                            contrastive_fail_explanation="",
                            assigned_level="L1",
                            level_justification="Error",
                            score=0.0,
                            reasoning=f"Error in P2 judge: {ex}",
                            is_fallback=True
                        ))
                    return results

    async def _run_p2_ranking(self, p1_results, test_case, dims):
        return await self._run_p2_judge("Ranking", p1_results, test_case, dims)

    async def _run_p2_coverage(self, p1_results, test_case, dims):
        return await self._run_p2_judge("Coverage", p1_results, test_case, dims)

    async def _run_p2_authority(self, p1_results, test_case, dims):
        return await self._run_p2_judge("Authority", p1_results, test_case, dims)

    async def _run_p2_freshness(self, p1_results, test_case, dims):
        return await self._run_p2_judge("Freshness", p1_results, test_case, dims)

    async def _run_p2_precision(self, p1_results, test_case, dims):
        return await self._run_p2_judge("Precision", p1_results, test_case, dims)

    async def evaluate(self, test_case: TestCase, search_results: list[FirecrawlSearchResult]) -> EvalResult:
        logger.info(f"Evaluating tc: {test_case.id} with P1/P2 Multi-Agent Architecture...")

        rubric_str = str([(d.name, d.weight) for d in test_case.rubric.dimensions]) if getattr(test_case, "rubric", None) else ""
        content_str = "|".join(sorted([hashlib.sha256((r.full_markdown or "").encode()).hexdigest()[:16] for r in search_results]))
        cache_str = f"{test_case.query}|{rubric_str}|{content_str}"
        cache_key = hashlib.sha256(cache_str.encode("utf-8")).hexdigest()
        if cache_key in self._judge_cache:
            logger.info(f"[Judge] Cache hit for {test_case.id}")
            return self._judge_cache[cache_key]

        domain_types = {sr.url: _classify_domain_type(sr.url) for sr in search_results}

        p1_results = await asyncio.gather(*(
            self._run_p1_agent(sr, test_case.query, test_case.intent, domain_types[sr.url])
            for sr in search_results
        ))

        rubric = enforce_baseline_dimensions(getattr(test_case, "rubric", None))

        dim_routes = self._route_dimensions(rubric)

        p2_coros = {}
        if dim_routes["ranking"]:
            p2_coros["ranking"] = self._run_p2_ranking(p1_results, test_case, dim_routes["ranking"])
        if dim_routes["coverage"]:
            p2_coros["coverage"] = self._run_p2_coverage(p1_results, test_case, dim_routes["coverage"])
        if dim_routes["authority"]:
            p2_coros["authority"] = self._run_p2_authority(p1_results, test_case, dim_routes["authority"])
        if dim_routes["freshness"]:
            p2_coros["freshness"] = self._run_p2_freshness(p1_results, test_case, dim_routes["freshness"])
        if dim_routes["precision"]:
            p2_coros["precision"] = self._run_p2_precision(p1_results, test_case, dim_routes["precision"])

        p2_results = await asyncio.gather(*p2_coros.values())
        all_evals = [eval_res for result_list in p2_results for eval_res in result_list]

        fidelity_eval = self._aggregate_fidelity(p1_results, rubric)
        if fidelity_eval:
            all_evals.append(fidelity_eval)

        for de in all_evals:
            if not de.is_fallback:
                de.score = _clamp_score_to_level(de.assigned_level, de.score)

        total_score = round(sum(de.weight * de.score for de in all_evals), 4)

        warnings = sanity_check(all_evals)
        for w in warnings:
            logger.warning(f"[Judge] TC {test_case.id} — {w}")

        import dataclasses
        result = EvalResult(
            test_case_id=test_case.id,
            dimension_evals=all_evals,
            overall_score=total_score,
            document_profiles=[dataclasses.asdict(p) for p in p1_results],
            warnings=warnings,
            result_diversity={}
        )

        self._judge_cache[cache_key] = result
        return result
