import json
import logging
import re
import uuid
import asyncio
import random
import copy
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any
from models.test_case import TestCase, VALID_INTENTS, AGENT_CHAOS_ARCHETYPES, RubricDimension, EvalRubric
from eval.test_case_history import TestCaseHistory
from clients.openrouter import OpenRouterClientPool
from config import EvalConfig

logger = logging.getLogger(__name__)

DOMAINS = [
    "Healthcare & Medical",
    "Finance & Investing",
    "Legal & Regulatory",
    "Travel & Geography",
    "Science & Academia",
    "Food & Nutrition",
    "Sports & Entertainment",
    "Education & Academia",
    "E-Commerce & Products",
    "Government & Public Policy",
    "Environment & Climate",
    "History & Humanities",
    "Technology & Software",
    "Cybersecurity",
    "Pharmaceuticals & Drug Information",
    "Real Estate & Property",
]

AGENT_CHAOS_DESCRIPTIONS = {
    "none": {
        "description": "A well-structured, clear, and direct query reflecting standard search intent.",
        "failure_mode": "Baseline behavior, standard search response expected."
    },
    "over_decomposed": {
        "description": "An agent broke a complex query into too simple or narrow search steps, losing the overall goal.",
        "failure_mode": "Loses essential comparative context or surrounding constraints, returning generic, single-topic results."
    },
    "keyword_stuffed": {
        "description": "The agent dumped all context tags, synonyms, and criteria directly into the query instead of phrasing it naturally.",
        "failure_mode": "Search engine matches irrelevant terms, diluting target relevance and bringing noisy aggregator blogs."
    },
    "reformulation_drift": {
        "description": "After a previous search returned sub-optimal results, the agent reformulates a query that drifts from the user's original objective.",
        "failure_mode": "Successive search runs yield increasingly unrelated or tangential information."
    },
    "multi_hop_compressed": {
        "description": "A query that attempts to resolve a multi-hop reasoning chain in a single search, expecting the search engine to perform synthesis.",
        "failure_mode": "Zero or highly generic search results because no single page contains all layers of the reasoning path."
    },
    "temporal_ambiguity": {
        "description": "The query uses relative words like 'latest', 'current', or 'recent' without specific years or dates.",
        "failure_mode": "Search results show outdated pages that use marketing language like 'latest updates' from prior years."
    },
    "copy_paste_artifact": {
        "description": "The query contains leftovers from prompt templates, JSON structural parameters, or tool call syntax.",
        "failure_mode": "Bizarre keyword matches on technical artifacts (e.g. key names, quotes, parameter brackets) in documents."
    }
}

def _robust_parse_json(raw: str) -> dict:
    text = raw.strip()
    # Strip thinking blocks if model outputs them
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    
    m = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if m:
        text = m.group(1).strip()
        
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
        
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end+1])
        except json.JSONDecodeError:
            pass
            
    raise ValueError(f"Could not extract a valid JSON object. Response snippet: {raw[:200]}")

ARCHETYPE_EXAMPLES = {
    "keyword_stuffed": {
        "good": {
            "query": "best over-the-counter pain relief for chronic back pain adults 2026",
            "rubric_criteria_example": "Results identify specific OTC analgesic categories and contraindications."
        },
        "bad": {
            "query": "pain relief OTC analgesics NSAIDs acetaminophen ibuprofen adults chronic back 2026 treatment",
            "rubric_criteria_example": "Results mention pain relief."
        }
    },
    "temporal_ambiguity": {
        "good": {
            "query": "current EU AI Act compliance requirements enterprise software",
            "rubric_criteria_example": "Results discuss compliance obligations without specifying a year anchor."
        },
        "bad": {
            "query": "latest AI regulations",
            "rubric_criteria_example": "Results are recent."
        }
    },
    "over_decomposed": {
        "good": {
            "query": "how to build a CI/CD pipeline",
            "rubric_criteria_example": "Results explain the steps for continuous integration and delivery."
        },
        "bad": {
            "query": "what is continuous",
            "rubric_criteria_example": "Results explain continuous."
        }
    },
    "reformulation_drift": {
        "good": {
            "query": "alternative treatments for severe migraines besides triptans",
            "rubric_criteria_example": "Results must list non-triptan interventions for severe migraines."
        },
        "bad": {
            "query": "why do people get headaches",
            "rubric_criteria_example": "Results explain headache causes."
        }
    },
    "multi_hop_compressed": {
        "good": {
            "query": "CEO of company that acquired Github in 2018 age",
            "rubric_criteria_example": "Results must mention Satya Nadella and his age."
        },
        "bad": {
            "query": "Github Microsoft Satya Nadella age",
            "rubric_criteria_example": "Results mention Satya Nadella."
        }
    },
    "copy_paste_artifact": {
        "good": {
            "query": "{\\\"query\\\": \\\"how to learn python\\\"}",
            "rubric_criteria_example": "Results ignore the JSON formatting and provide Python tutorials."
        },
        "bad": {
            "query": "how to learn python JSON format",
            "rubric_criteria_example": "Results teach Python and JSON."
        }
    },
    "none": {
        "good": {
            "query": "how to properly insulate a residential attic",
            "rubric_criteria_example": "Results provide step-by-step instructions and R-value recommendations for attic insulation."
        },
        "bad": {
            "query": "attic",
            "rubric_criteria_example": "Results mention attics."
        }
    }
}

def _jaccard_similarity(q1: str, q2: str) -> float:
    s1, s2 = set(q1.lower().split()), set(q2.lower().split())
    if not s1 and not s2: return 1.0
    return len(s1 & s2) / len(s1 | s2)


class TestGenerator:
    def __init__(self, config: EvalConfig, or_pool: OpenRouterClientPool):
        self.config = config
        self.or_pool = or_pool
        self.model = config.generator_model
        gen_concurrency = getattr(config, 'max_concurrent_tcs', 8)
        self._semaphore = asyncio.Semaphore(gen_concurrency)

    def _validate_rubric_claims(self, rubric: dict, query: str) -> List[str]:
        warnings = []
        query_lower = query.lower()
        for d in rubric.get("dimensions", []):
            criteria = d.get("criteria", "").lower()
            import re
            numbers = re.findall(r'\b(20\d{2}|\d{4,})\b', criteria)
            for num in numbers:
                if num not in query_lower:
                    warnings.append(f"Dimension '{d.get('name')}' criteria contains specific number '{num}' not in query.")
        return warnings

    def _validate_test_case(self, tc_data: dict) -> Tuple[bool, List[str]]:
        warnings = []
        query = tc_data.get("query", "")
        if len(query.split()) < 4:
            return False, ["Query too short (< 4 words)"]
        
        if tc_data.get("intent") not in VALID_INTENTS:
            warnings.append(f"Unknown intent '{tc_data.get('intent')}', defaulting to 'exploratory'")
            tc_data["intent"] = "exploratory"
            
        rubric = tc_data.get("rubric", {})
        if not rubric:
            return False, ["Missing 'rubric' object"]
            
        dimensions = rubric.get("dimensions", [])
        if not isinstance(dimensions, list) or len(dimensions) < 2:
            return False, ["Rubric must contain at least 2 dimensions"]
            
        for idx, d in enumerate(dimensions):
            if not isinstance(d, dict):
                return False, [f"Dimension index {idx} is not a valid dictionary"]
            if not d.get("name"):
                return False, [f"Dimension index {idx} missing 'name'"]
            if not d.get("criteria"):
                return False, [f"Dimension index {idx} missing 'criteria'"]
            if not d.get("contrastive_fail"):
                return False, [f"Dimension index {idx} missing 'contrastive_fail'"]
            try:
                d["weight"] = float(d.get("weight", 0.0))
            except (ValueError, TypeError):
                return False, [f"Dimension index {idx} has invalid weight value"]
                
        total_weight = sum(float(d.get("weight", 0.0)) for d in dimensions)
        if abs(total_weight - 1.0) > 0.05:
            return False, [f"Rubric dimension weights must sum to approximately 1.0 (got {total_weight})"]

        claim_warnings = self._validate_rubric_claims(rubric, query)
        if claim_warnings:
            return False, claim_warnings
            
        return True, warnings

    def _validate_generated_tc(self, tc_data: dict) -> Tuple[bool, List[str]]:
        """Post-schema semantic checks the model frequently violates."""
        warnings = []
        dimensions = tc_data.get("rubric", {}).get("dimensions", [])
        for d in dimensions:
            criteria = d.get("criteria", "")
            cf = d.get("contrastive_fail", "")
            if _jaccard_similarity(criteria, cf) > 0.70:
                return False, [f"Dimension '{d.get('name')}': contrastive_fail is too similar to criteria (Jaccard > 0.70)"]
            if len(cf.split()) < 10:
                return False, [f"Dimension '{d.get('name')}': contrastive_fail is too short (< 10 words)"]
        return True, warnings

    async def generate_novel(self, num_cases: int, history: TestCaseHistory) -> List[TestCase]:
        today = datetime.now().strftime("%Y-%m-%d")
        current_year = datetime.now().strftime("%Y")
        
        MAX_AVOID_QUERIES = 30
        all_past_queries = history.all_queries()
        avoid_queries = all_past_queries[-MAX_AVOID_QUERIES:] if len(all_past_queries) > MAX_AVOID_QUERIES else all_past_queries
        avoid_queries_str = json.dumps(avoid_queries, indent=2) if avoid_queries else "None"
        
        system_prompt = f"""You are a Red-Team AI Evaluation Architect specializing in testing search and scraping pipelines for agentic workflows.
Your role is to author a challenging Test Case representing an agent-generated search query, along with a multi-dimensional Evaluation Rubric for grading search & scrape results.

Today is {today}. Use year {current_year} for temporal constraints/anchors.

VALID INTENTS:
{json.dumps(VALID_INTENTS, indent=2)}

AGENT CHAOS ARCHETYPES:
{json.dumps(AGENT_CHAOS_DESCRIPTIONS, indent=2)}

AVOID DUPLICATE QUERIES:
Do NOT generate queries semantically similar to any of these:
{avoid_queries_str}

GUARDRAILS (non-obvious conventions — apply carefully):
- criteria must describe OBSERVABLE search/scrape output behaviors, not internal system
  state. "Results contain X" is valid. "The system retrieves X" is not.
- criteria must NOT embed specific facts, numbers, years, or named entities unless they
  appear verbatim in the query string. The judge validates this.
- contrastive_fail must be an observable output pattern — never a copy-paste of criteria.
  A contrastive_fail that repeats the criteria will cause scoring contradictions.
- temporal queries: use `current_year` ({current_year}) for explicit temporal anchors
  in queries. Do not use "latest" or "recent" in the query itself (that is the
  temporal_ambiguity archetype, use it only when that archetype is selected).
- query length: aim for 7–15 words. Fewer than 5 words fails validation and wastes a retry.

RUBRIC SCHEMA INSTRUCTIONS:
- You must define 2 to 4 Rubric Dimensions. The weights of the dimensions MUST sum up exactly to 1.0.
- Each dimension must have:
  1. `name`: unique identifier (e.g., "coverage", "source_authority", "structural_fidelity").
  2. `weight`: numeric score weight.
  3. `criteria`: explicit instructions on what the scraped/retrieved content must satisfy. DO NOT include specific facts, numbers, or entities in the criteria unless they are explicitly part of the query.
  4. `contrastive_fail`: a concrete description/example of a failure mode for this dimension to calibrate the judge.
- `grading_notes`: general guidance for the judge on how to evaluate the overall response, handle edge cases, or prioritize content.

OUTPUT SCHEMA:
Your entire response must be a single, valid JSON object matching the following structure:
{{
  "query": "<5+ words query reflecting the chosen chaos archetype>",
  "intent": "<one of VALID INTENTS>",
  "difficulty": "<easy|medium|hard>",
  "rubric": {{
    "dimensions": [
      {{
        "name": "<dimension_name>",
        "weight": <float between 0.1 and 0.8>,
        "criteria": "<specific search/scrape criteria>",
        "contrastive_fail": "<what failure looks like>"
      }}
    ],
    "grading_notes": "<free text instructions>"
  }}
}}
"""
        
        async def fetch_case(domain: str, archetype: str) -> Optional[TestCase]:
            archetype_info = AGENT_CHAOS_DESCRIPTIONS[archetype]
            prompt = f"""Target Domain: {domain}
Chaos Archetype: {archetype}
Archetype Description: {archetype_info['description']}
Archetype Expected Failure Mode: {archetype_info['failure_mode']}

QUALITY REFERENCE (for calibration — do not copy, use as style guide):
  Good example query: {ARCHETYPE_EXAMPLES.get(archetype, ARCHETYPE_EXAMPLES["none"])['good']['query']}
  Good rubric criteria style: {ARCHETYPE_EXAMPLES.get(archetype, ARCHETYPE_EXAMPLES["none"])['good']['rubric_criteria_example']}
  Bad query (avoid this pattern): {ARCHETYPE_EXAMPLES.get(archetype, ARCHETYPE_EXAMPLES["none"])['bad']['query']}
  Bad criteria (avoid this): {ARCHETYPE_EXAMPLES.get(archetype, ARCHETYPE_EXAMPLES["none"])['bad']['rubric_criteria_example']}

Generate exactly ONE novel Test Case JSON object.
Enforce the chosen chaos archetype characteristics into the query. It must read like an agent query suffering from this exact flaw.
Ensure the rubric criteria is tailored to grade whether a search/scrape pipeline successfully overcomes this archetype's challenge.
Output ONLY the JSON object. Do not include markdown wraps or commentary.
"""
            last_error: Optional[str] = None
            for attempt in range(3):
                try:
                    # On retry, inject an explicit correction message so the model
                    # understands why the previous response was rejected.
                    retry_prefix = ""
                    if attempt > 0 and last_error:
                        retry_prefix = (
                            f"Your previous response was rejected for this reason: {last_error}\n"
                            "Try again. Output ONLY a valid JSON object — no markdown, no commentary, starting with '{' and ending with '}'. \n\n"
                        )
                    raw, _ = await self.or_pool.generate(
                        prompt=retry_prefix + prompt,
                        model=self.model,
                        temperature=0.8,
                        system_prompt=system_prompt,
                        max_tokens=None,
                        providers=self.config.generator_providers
                    )
                    
                    data = _robust_parse_json(raw)
                    if isinstance(data, dict):
                        is_valid, warnings = self._validate_test_case(data)
                        if is_valid:
                            is_sem_valid, sem_warnings = self._validate_generated_tc(data)
                            if not is_sem_valid:
                                is_valid = False
                                warnings.extend(sem_warnings)
                                
                        if is_valid:
                            too_similar = False
                            for past_q in all_past_queries:
                                if _jaccard_similarity(data.get("query", ""), past_q) > 0.65:
                                    last_error = f"Generated query too similar to existing: '{past_q}'"
                                    too_similar = True
                                    break
                            
                            if too_similar:
                                continue
                                
                            dimensions = data["rubric"]["dimensions"]
                            total_w = sum(d["weight"] for d in dimensions)
                            if total_w == 0:
                                equal_w = round(1.0 / len(dimensions), 4)
                                for d in dimensions:
                                    d["weight"] = equal_w
                                total_w = 1.0
                            if abs(total_w - 1.0) > 0.001:
                                for d in dimensions:
                                    d["weight"] = round(d["weight"] / total_w, 2)
                                diff = round(1.0 - sum(d["weight"] for d in dimensions[:-1]), 2)
                                dimensions[-1]["weight"] = diff
                            
                            rubric_dims = [RubricDimension(**d) for d in dimensions]
                            rubric = EvalRubric(
                                dimensions=rubric_dims,
                                grading_notes=data["rubric"].get("grading_notes", "")
                            )
                            return TestCase(
                                id=f"tc_{uuid.uuid4().hex[:8]}",
                                query=data["query"],
                                domain=domain,
                                intent=data["intent"],
                                difficulty=data["difficulty"],
                                chaos_archetype=archetype,
                                cache_relationship="novel",
                                category=domain,
                                parent_case_id=None,
                                rubric=rubric,
                                cache_intent="novel"
                            )
                        else:
                            last_error = f"Validation failed: {'; '.join(warnings)}"
                            logger.warning(f"Invalid generated test case: {warnings}. Response raw: {raw[:200]}")
                except json.JSONDecodeError as e:
                    last_error = f"Response was not valid JSON: {e}"
                    logger.warning(f"JSON parse error on attempt {attempt+1}: {e}")
                except Exception as e:
                    if "client has been closed" in str(e):
                        logger.debug("OpenRouter client closed during generation (likely pipeline shutdown).")
                        break
                    last_error = str(e)
                    logger.warning(f"Error generating test case on attempt {attempt+1}: {e}")
            return None

        async def bounded_fetch(domain: str, archetype: str) -> Optional[TestCase]:
            async with self._semaphore:
                return await fetch_case(domain, archetype)

        archetypes = list(self.config.archetype_weights.keys())
        weights = list(self.config.archetype_weights.values())

        tasks = []
        for _ in range(num_cases):
            domain = random.choice(DOMAINS)
            archetype = random.choices(archetypes, weights=weights, k=1)[0]
            tasks.append(bounded_fetch(domain, archetype))

        results = await asyncio.gather(*tasks)
        cases = [c for c in results if c is not None]
        return cases

    async def _fetch_variant(self, parent: TestCase, relationship: str) -> Optional[TestCase]:
        if relationship == "exact_duplicate":
            rubric_copy = copy.deepcopy(parent.rubric)
            return TestCase(
                id=f"tc_{uuid.uuid4().hex[:8]}",
                query=parent.query,
                domain=parent.domain,
                intent=parent.intent,
                difficulty=parent.difficulty,
                chaos_archetype=parent.chaos_archetype,
                cache_relationship="exact_duplicate",
                category=parent.domain,
                parent_case_id=parent.id,
                rubric=rubric_copy,
                cache_intent="exact_duplicate"
            )
            
        parent_dict = {
            "id": parent.id,
            "query": parent.query,
            "intent": parent.intent,
            "domain": parent.domain,
            "difficulty": parent.difficulty,
            "rubric": {
                "dimensions": [
                    {
                        "name": d.name,
                        "weight": d.weight,
                        "criteria": d.criteria,
                        "contrastive_fail": d.contrastive_fail
                    } for d in parent.rubric.dimensions
                ] if parent.rubric else [],
                "grading_notes": parent.rubric.grading_notes if parent.rubric else ""
            }
        }
        
        system_prompt = f"""You are a Red-Team AI Evaluation Architect.
Your task is to generate a cache-testing variant query derived from a parent TestCase.

VALID INTENTS (intent field MUST be one of these exact strings):
{json.dumps(VALID_INTENTS, indent=2)}

TARGET CACHE RELATIONSHIPS:
- same_source_different_angle: The variant query must seek a completely different set of information from the same target source material. The rubric MUST be completely rewritten to assess the new angle.
- rephrased_same_intent: The variant query must be a natural, distinct rephrasing of the parent query, with the same core intent. The rubric should be similar but adapted if needed.
- subset_of_parent: The variant query must target a subset or specific sub-detail of the parent query's scope. The rubric should be narrower.

RUBRIC REQUIREMENTS:
- 2 to 4 dimensions, weights must sum to exactly 1.0.
- Each dimension needs: name, weight (float), criteria (what success looks like), contrastive_fail (what failure looks like). DO NOT include specific facts, numbers, or entities in the criteria unless they are explicitly part of the query.

OUTPUT SCHEMA:
Your entire response must be a single, valid JSON object. Start with '{{' and end with '}}'. No markdown, no commentary.
{{
  "query": "<variant query string>",
  "intent": "<one of the VALID INTENTS above>",
  "difficulty": "<easy|medium|hard>",
  "rubric": {{
    "dimensions": [
      {{
        "name": "<dimension_name>",
        "weight": <float>,
        "criteria": "<specific search/scrape criteria>",
        "contrastive_fail": "<what failure looks like>"
      }}
    ],
    "grading_notes": "<free text instructions>"
  }}
}}
"""
        
        prompt = f"""Parent Test Case:
{json.dumps(parent_dict, indent=2)}

Requested Cache Relationship: {relationship}

Generate exactly ONE variant Test Case JSON object.
Output ONLY the JSON object. Do not include markdown wraps or commentary.
"""
        last_error: Optional[str] = None
        for attempt in range(3):
            try:
                retry_prefix = ""
                if attempt > 0 and last_error:
                    retry_prefix = (
                        f"Your previous response was rejected for this reason: {last_error}\n"
                        "Try again. Output ONLY a valid JSON object — no markdown, no commentary, starting with '{' and ending with '}'. \n\n"
                    )
                raw, _ = await self.or_pool.generate(
                    prompt=retry_prefix + prompt,
                    model=self.model,
                    temperature=0.7,
                    system_prompt=system_prompt,
                    max_tokens=None,
                    providers=self.config.generator_providers
                )
                
                data = _robust_parse_json(raw)
                if isinstance(data, dict):
                    is_valid, warnings = self._validate_test_case(data)
                    if is_valid:
                        dimensions = data["rubric"]["dimensions"]
                        total_w = sum(d["weight"] for d in dimensions)
                        if total_w == 0:
                            equal_w = round(1.0 / len(dimensions), 4)
                            for d in dimensions:
                                d["weight"] = equal_w
                            total_w = 1.0
                        if abs(total_w - 1.0) > 0.001:
                            for d in dimensions:
                                d["weight"] = round(d["weight"] / total_w, 2)
                            diff = round(1.0 - sum(d["weight"] for d in dimensions[:-1]), 2)
                            dimensions[-1]["weight"] = diff
                        
                        rubric_dims = [RubricDimension(**d) for d in dimensions]
                        rubric = EvalRubric(
                            dimensions=rubric_dims,
                            grading_notes=data["rubric"].get("grading_notes", "")
                        )
                        return TestCase(
                            id=f"tc_{uuid.uuid4().hex[:8]}",
                            query=data["query"],
                            domain=parent.domain,
                            intent=data["intent"],
                            difficulty=data["difficulty"],
                            chaos_archetype=parent.chaos_archetype,
                            cache_relationship=relationship,
                            category=parent.domain,
                            parent_case_id=parent.id,
                            rubric=rubric,
                            cache_intent=relationship
                        )
                    else:
                        last_error = f"Validation failed: {'; '.join(warnings)}"
                        logger.warning(f"Invalid cache variant test case: {warnings}. Raw: {raw[:200]}")
            except json.JSONDecodeError as e:
                last_error = f"Response was not valid JSON: {e}"
                logger.warning(f"JSON parse error on cache variant attempt {attempt+1}: {e}")
            except Exception as e:
                if "client has been closed" in str(e):
                    logger.debug("OpenRouter client closed during cache variant generation.")
                    break
                last_error = str(e)
                logger.warning(f"Error generating cache variant on attempt {attempt+1}: {e}")
        return None

    async def _fetch_variant_bounded(self, parent: TestCase, relationship: str) -> Optional[TestCase]:
        async with self._semaphore:
            return await self._fetch_variant(parent, relationship)

    async def generate_cache_variants(self, num_cases: int, history: TestCaseHistory) -> List[TestCase]:
        # Weighted relationship pool: exact_duplicate is cheap/trivial (always hits cache)
        # and provides minimal signal — downweight it. Upweight the harder, more informative cases.
        relationship_weights = {
            "exact_duplicate": 0.10,
            "same_source_different_angle": 0.35,
            "rephrased_same_intent": 0.30,
            "subset_of_parent": 0.25,
        }
        relationships = list(relationship_weights.keys())
        rel_weights = list(relationship_weights.values())

        parents = history.sample(num_cases)
        if not parents:
            return []
            
        tasks = []
        for idx in range(num_cases):
            parent = parents[idx % len(parents)]
            rel = random.choices(relationships, weights=rel_weights, k=1)[0]
            tasks.append(self._fetch_variant_bounded(parent, rel))
            
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]

    async def generate(self, num_cases: int) -> List[TestCase]:
        """Main entry point. Loads history internally and decides novel vs. cache variant mode."""
        logger.info(f"Generating {num_cases} test cases via dynamic rubric-first model...")
        history = TestCaseHistory()
        
        history_count = history.count()
        if history_count < self.config.cache_variant_min_history:
            logger.info(
                f"[TestGenerator] History size {history_count} < minimum {self.config.cache_variant_min_history}. "
                f"Generating all {num_cases} as novel cases."
            )
            generate_variants = False
        else:
            generate_variants = random.random() < 0.35
            mode = "cache variants" if generate_variants else "novel cases"
            logger.info(
                f"[TestGenerator] History available ({history_count} cases). "
                f"This round: {num_cases} {mode}."
            )
            
        if generate_variants:
            variants = await self.generate_cache_variants(num_cases, history)
            needed = num_cases - len(variants)
            if needed > 0:
                logger.warning(
                    f"[TestGenerator] Generated only {len(variants)}/{num_cases} valid cache variants. "
                    f"Filling {needed} remainder with novel cases."
                )
                novel_cases = await self.generate_novel(needed, history)
                variants.extend(novel_cases)
            return variants
        else:
            return await self.generate_novel(num_cases, history)
