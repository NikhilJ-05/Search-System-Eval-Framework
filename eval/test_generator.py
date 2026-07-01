import json
import logging
import re
import uuid
import asyncio
import random
from datetime import datetime
from typing import List, Optional, Tuple
from models.test_case import TestCase, VALID_INTENTS
from clients.openrouter import OpenRouterClientPool
from config import EvalConfig

logger = logging.getLogger(__name__)

DOMAIN_BUCKETS = [
    {"name": "Healthcare & Medical",      "family": "health",    "structural_categories": ["structured_data_extraction", "pdf_document", "long_form_article"],       "example_queries": ["FDA drug approval list with dosage table", "WHO ICD-11 disease classification codes"]},
    {"name": "Finance & Investing",       "family": "finance",   "structural_categories": ["structured_data_extraction", "rapidly_changing", "paywalled_content"],  "example_queries": ["Roth IRA contribution limits 2026", "S&P 500 sector weights breakdown table"]},
    {"name": "Legal & Regulatory",        "family": "legal",     "structural_categories": ["pdf_document", "nav_heavy_portal", "structured_data_extraction"],      "example_queries": ["GDPR Article 17 right to erasure requirements", "US visa types and eligibility table"]},
    {"name": "Travel & Geography",        "family": "travel",    "structural_categories": ["structured_data_extraction", "dynamic_spa_content", "nav_heavy_portal"], "example_queries": ["visa free travel countries for Indian passport", "JFK airport terminal map gates"]},
    {"name": "Science & Academia",        "family": "science",   "structural_categories": ["long_form_article", "pdf_document", "structured_data_extraction"],       "example_queries": ["periodic table element properties with electronegativity", "James Webb telescope infrared discoveries 2026"]},
    {"name": "Food & Nutrition",          "family": "food",      "structural_categories": ["structured_data_extraction", "long_form_article", "minimal_content"],      "example_queries": ["USDA protein content per 100g food table", "sourdough bread fermentation time temperature chart"]},
    {"name": "Sports & Entertainment",    "family": "sports",    "structural_categories": ["rapidly_changing", "dynamic_spa_content", "structured_data_extraction"],  "example_queries": ["Formula 1 2026 driver standings table", "NBA all-time scoring leaders list"]},
    {"name": "Education & Academia",      "family": "education", "structural_categories": ["structured_data_extraction", "nav_heavy_portal", "pdf_document"],         "example_queries": ["SAT score percentiles 2026 table", "Harvard admission statistics by major"]},
    {"name": "E-Commerce & Products",     "family": "commerce",  "structural_categories": ["structured_data_extraction", "nav_heavy_portal", "dynamic_spa_content"],  "example_queries": ["iPhone 16 Pro vs Samsung S25 specs comparison", "mattress firmness comparison chart brands"]},
    {"name": "Government & Public Policy","family": "government","structural_categories": ["pdf_document", "nav_heavy_portal", "long_form_article"],               "example_queries": ["US federal minimum wage history table", "Medicare Part D drug coverage tiers 2026"]},
    {"name": "Environment & Climate",     "family": "science",   "structural_categories": ["structured_data_extraction", "long_form_article", "rapidly_changing"],    "example_queries": ["CO2 emissions by country ranking table", "current AQI levels major US cities"]},
    {"name": "History & Humanities",      "family": "humanities","structural_categories": ["long_form_article", "pdf_document", "nav_heavy_portal"],               "example_queries": ["causes of World War 1 timeline key events", "Roman Empire decline fall major reasons list"]},
    # Technology capped to ≤1 per batch via family="tech" uniqueness constraint
    {"name": "Technology & Software",     "family": "tech",      "structural_categories": ["code_documentation", "structured_data_extraction", "multi_language"],     "example_queries": ["pandas dataframe merge vs join syntax", "SQLAlchemy async session configuration", "Python asyncio gather vs wait difference with code example", "implement binary search tree insertion deletion Python", "Node.js 20 vs Deno 2 HTTP server benchmark", "gradient descent convergence conditions learning rate"]},
]

def _robust_parse_json_list(raw: str) -> list:
    text = raw.strip()

    m = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    if m:
        text = m.group(1).strip()

    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for val in data.values():
                if isinstance(val, list):
                    return val
    except json.JSONDecodeError:
        pass

    arr_start = text.find('[')
    if arr_start != -1:
        arr_end = text.rfind(']')
        if arr_end > arr_start:
            try:
                return json.loads(text[arr_start:arr_end + 1])
            except json.JSONDecodeError:
                pass

    objects = []
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(text):
        while pos < len(text) and text[pos] in ' \t\r\n,':
            pos += 1
        if pos >= len(text):
            break
        if text[pos] != '{':
            pos += 1
            continue
        try:
            obj, end_idx = decoder.raw_decode(text, pos)
            objects.append(obj)
            pos = end_idx
        except json.JSONDecodeError:
            pos += 1

    if objects:
        logger.info(f"[TestGenerator] NDJSON fallback: collected {len(objects)} objects")
        return objects

    raise ValueError(f"Could not extract a JSON list from LLM response. First 200 chars: {raw[:200]}")


class TestGenerator:
    def __init__(self, config: EvalConfig, or_pool: OpenRouterClientPool):
        self.config = config
        self.or_pool = or_pool
        self.model = config.generator_model

    def _validate_test_case(self, tc_data: dict) -> Tuple[bool, List[str]]:
        warnings = []
        if len(tc_data.get("query", "").split()) < 4:
            return False, ["Query too short (< 4 words)"]
        if len(tc_data.get("expected_coverage", {}).get("must_mention", [])) < 2:
            return False, ["must_mention has < 2 items"]
        if not tc_data.get("expected_scrape_challenges", {}).get("expected_elements"):
            return False, ["expected_elements is empty"]
        
        if tc_data.get("intent") not in VALID_INTENTS:
            warnings.append(f"Unknown intent '{tc_data.get('intent')}', defaulting to 'exploratory'")
            tc_data["intent"] = "exploratory"
            
        if tc_data.get("difficulty") == "medium":
            warnings.append("Difficulty is 'medium' — LLM may be defaulting")
        if not tc_data.get("expected_ranking", {}).get("expected_source_priority"):
            warnings.append("No expected_source_priority — ranking judge will have less signal")
            tc_data.setdefault("expected_ranking", {})["expected_source_priority"] = []
            
        return True, warnings

    async def _generate_novel_anchors(self, domains: List[dict], previous_queries: List[str], previous_urls: List[str]) -> List[TestCase]:
        today = datetime.now().strftime("%Y-%m-%d")
        current_year = datetime.now().strftime("%Y")
        
        # Stratified history sample: always include the last 5 for recency, then
        # randomly sample up to 10 more from the older history for diversity.
        RECENT_N = 5
        SAMPLE_N = 10
        recent = previous_queries[-RECENT_N:] if previous_queries else []
        older = previous_queries[:-RECENT_N] if len(previous_queries) > RECENT_N else []
        sampled_older = random.sample(older, min(SAMPLE_N, len(older)))
        avoid_queries = list(dict.fromkeys(recent + sampled_older))  # deduplicated, order preserved
        avoid_queries_str = json.dumps(avoid_queries, indent=2) if avoid_queries else "None"
        system_prompt_base = f"""You are a red-team engineer finding failure modes in a web scraping pipeline. 
Design a query that exposes weaknesses in search coverage, ranking, and markdown extraction.
IMPORTANT: Today is {today}. Use {current_year} for current events.

AVOID DUPLICATES: Do NOT generate queries that are semantically similar to any of these already-used queries:
{avoid_queries_str}

AUTHENTICITY RULE: The query MUST sound like natural, authentic search terms typed into Google (e.g. "celiac disease gluten free diet food list"). No robotic boilerplate ("Comprehensive guide to...").

QUALITY RULES:
1. `must_mention` MUST contain >=3 specific named entities.
2. `expected_elements` MUST list >=2 concrete HTML structures to preserve (e.g. "data_tables", "code_blocks").
3. `noise_risks` MUST cite specific website patterns (e.g. "cookie_consent_banner").
4. `query` MUST be >=5 words.
5. `intent` MUST be one of: factual_lookup, comparative_research, tutorial_howto, data_extraction, navigational, exploratory, real_time.
6. `cache_intent` MUST be "novel".

Output exactly ONE JSON object (NOT an array). Do not use markdown wrappers if possible."""

        anchors = []
        
        async def fetch_anchor(domain: dict):
            prompt = f"""
Target Domain: {domain['name']}
Allowed Categories: {', '.join(domain['structural_categories'])}
Example queries in this domain: {', '.join(f'"{q}"' for q in domain['example_queries'])}

Generate EXACTLY ONE novel test case object in this domain.
You MUST follow this EXACT nested JSON schema — do NOT flatten fields to the top level:

{{
  "id": "tc_placeholder",
  "query": "<5+ word natural search query>",
  "intent": "<one of: factual_lookup|comparative_research|tutorial_howto|data_extraction|navigational|exploratory|real_time>",
  "difficulty": "<easy|hard>",
  "category": "<one of the Allowed Categories above>",
  "cache_intent": "novel",
  "expected_coverage": {{
    "must_mention": ["<entity1>", "<entity2>", "<entity3>"],
    "should_mention": ["<optional1>", "<optional2>"],
    "min_relevant_results": 2
  }},
  "expected_ranking": {{
    "ranking_signals": ["<signal1>", "<signal2>"],
    "ideal_ranking_rationale": "<why source A beats source B>",
    "expected_source_priority": ["<domain1.com>", "<domain2.com>"]
  }},
  "expected_scrape_challenges": {{
    "likely_page_types": ["<page_type>"],
    "expected_elements": ["<html_element1>", "<html_element2>"],
    "noise_risks": ["<specific_site_pattern1>", "<specific_site_pattern2>"]
  }}
}}

ONE-SHOT EXAMPLE (for the Finance domain):
{{
  "id": "tc_placeholder",
  "query": "Roth IRA maximum contribution limits 2026 income phase out thresholds",
  "intent": "factual_lookup",
  "difficulty": "easy",
  "category": "structured_data_extraction",
  "cache_intent": "novel",
  "expected_coverage": {{
    "must_mention": ["IRS", "Roth_IRA", "modified_adjusted_gross_income"],
    "should_mention": ["catch_up_contribution", "traditional_IRA"],
    "min_relevant_results": 2
  }},
  "expected_ranking": {{
    "ranking_signals": ["official_source", "date_freshness"],
    "ideal_ranking_rationale": "IRS.gov should rank first for authoritative dollar limits",
    "expected_source_priority": ["irs.gov", "nerdwallet.com"]
  }},
  "expected_scrape_challenges": {{
    "likely_page_types": ["government_portal", "financial_guide"],
    "expected_elements": ["data_tables", "income_threshold_lists"],
    "noise_risks": ["nerdwallet_sticky_nav", "cookie_consent_overlay"]
  }}
}}

Output ONLY the JSON object for the {domain['name']} domain. No markdown fences, no commentary.
"""
            for attempt in range(3):
                try:
                    raw = await self.or_pool.generate(
                        prompt=prompt,
                        model=self.model,
                        temperature=0.8,
                        system_prompt=system_prompt_base,
                        max_tokens=16000,
                        providers=self.config.generator_providers
                    )
                    
                    text = raw.strip()
                    m = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
                    if m:
                        text = m.group(1).strip()
                    
                    data = None
                    try:
                        data = json.loads(text)
                    except json.JSONDecodeError:
                        start = text.find('{')
                        end = text.rfind('}')
                        if start != -1 and end > start:
                            data = json.loads(text[start:end+1])
                            
                    if isinstance(data, dict):
                        is_valid, warnings = self._validate_test_case(data)
                        if is_valid:
                            data['id'] = f"tc_{uuid.uuid4().hex[:8]}"
                            data['cache_intent'] = "novel"
                            if data.get('category') not in domain['structural_categories']:
                                data['category'] = random.choice(domain['structural_categories'])
                            return TestCase.from_dict(data)
                        else:
                            logger.warning(f"Invalid anchor generated: {warnings}")
                except Exception as e:
                    logger.warning(f"Error generating anchor: {e}")
            return None

        sem = asyncio.Semaphore(8)
        async def bounded_fetch(domain):
            async with sem:
                return await fetch_anchor(domain)

        tasks = [bounded_fetch(d) for d in domains]
        results = await asyncio.gather(*tasks)
        
        for res in results:
            if res:
                anchors.append(res)
                
        return anchors

    async def _generate_cache_variants(self, anchors: List[TestCase], previous_queries: List[str], previous_urls: List[str], num_variants: int) -> List[TestCase]:
        if num_variants <= 0:
            return []
            
        today = datetime.now().strftime("%Y-%m-%d")
        current_year = datetime.now().strftime("%Y")
        
        ref_pool = []
        for a in anchors:
            ref_pool.append({"query": a.query, "category": a.category})
        # Stratified reference pool: all current anchors + a representative sample
        # of history (recent 5 always included, up to 10 more sampled from older rounds).
        RECENT_N = 5
        SAMPLE_N = 10
        recent_hist = previous_queries[-RECENT_N:] if previous_queries else []
        older_hist = previous_queries[:-RECENT_N] if len(previous_queries) > RECENT_N else []
        sampled_hist = random.sample(older_hist, min(SAMPLE_N, len(older_hist)))
        selected_hist = list(dict.fromkeys(recent_hist + sampled_hist))

        for pq in selected_hist:
            if pq not in [r["query"] for r in ref_pool]:
                ref_pool.append({"query": pq, "category": "historical"})
                
        system_prompt = f"""You are a red-team engineer generating cache-testing queries.
IMPORTANT: Today is {today}. Use {current_year}.
AUTHENTICITY RULE: Queries MUST sound like natural, authentic search terms typed into a search engine.

We are testing a search cache. Given a REFERENCE POOL of recent queries, generate EXACTLY {num_variants} cache-variant test cases.
Each generated test case MUST derive from one of the reference queries, using one of these `cache_intent` values:
- `exact_duplicate`: EXACT same query string as a reference query.
- `semantic_near_miss`: EXACT same semantic intent as a reference query, but different phrasing.
- `shared_url`: A related query that would likely return the same authoritative URL/document.
- `semantic_far_miss`: A query in the same general domain but distinctly different intent.

CRITICAL: You MUST use this EXACT nested JSON schema — do NOT flatten fields to the top level:

{{
  "id": "tc_placeholder",
  "query": "<5+ word natural search query>",
  "intent": "<factual_lookup|comparative_research|tutorial_howto|data_extraction|navigational|exploratory|real_time>",
  "difficulty": "<easy|hard>",
  "category": "<structured_data_extraction|dynamic_spa_content|pdf_document|code_documentation|rapidly_changing|long_form_article|minimal_content|nav_heavy_portal|multi_language|paywalled_content>",
  "cache_intent": "<exact_duplicate|semantic_near_miss|shared_url|semantic_far_miss>",
  "derived_from_query": "<query string from reference pool this was derived from>",
  "expected_coverage": {{
    "must_mention": ["<entity1>", "<entity2>", "<entity3>"],
    "should_mention": ["<optional1>"],
    "min_relevant_results": 2
  }},
  "expected_ranking": {{
    "ranking_signals": ["<signal1>"],
    "ideal_ranking_rationale": "<reasoning>",
    "expected_source_priority": ["<domain1.com>", "<domain2.com>"]
  }},
  "expected_scrape_challenges": {{
    "likely_page_types": ["<page_type>"],
    "expected_elements": ["<element1>", "<element2>"],
    "noise_risks": ["<site_pattern1>", "<site_pattern2>"]
  }}
}}

ONE-SHOT EXAMPLE (semantic_near_miss of "Roth IRA contribution limits 2026"):
{{
  "id": "tc_placeholder",
  "query": "how much can I put in a Roth IRA this year income limits",
  "intent": "factual_lookup",
  "difficulty": "easy",
  "category": "structured_data_extraction",
  "cache_intent": "semantic_near_miss",
  "derived_from_query": "Roth IRA contribution limits 2026",
  "expected_coverage": {{
    "must_mention": ["IRS", "Roth_IRA", "modified_adjusted_gross_income"],
    "should_mention": ["catch_up_contribution"],
    "min_relevant_results": 2
  }},
  "expected_ranking": {{
    "ranking_signals": ["official_source", "date_freshness"],
    "ideal_ranking_rationale": "IRS.gov should rank first",
    "expected_source_priority": ["irs.gov", "nerdwallet.com"]
  }},
  "expected_scrape_challenges": {{
    "likely_page_types": ["government_portal", "financial_guide"],
    "expected_elements": ["data_tables", "income_threshold_lists"],
    "noise_risks": ["nerdwallet_sticky_nav", "cookie_consent_overlay"]
  }}
}}

Output EXACTLY a JSON array [ ... ] containing {num_variants} objects. No markdown fences, no commentary."""

        prompt = f"""
REFERENCE POOL:
{json.dumps(ref_pool, indent=2)}

Generate {num_variants} cache-variant test cases derived from the reference pool. Output ONLY the JSON array.
"""

        for attempt in range(3):
            try:
                raw = await self.or_pool.generate(
                    prompt=prompt,
                    model=self.model,
                    temperature=0.7,
                    system_prompt=system_prompt,
                    max_tokens=16000,
                    providers=self.config.generator_providers
                )
                
                data = _robust_parse_json_list(raw)
                if not data:
                    continue
                    
                variants = []
                for item in data:
                    if len(variants) >= num_variants:
                        break
                    is_valid, warnings = self._validate_test_case(item)
                    if is_valid:
                        item.pop("derived_from_query", None)
                        item['id'] = f"tc_{uuid.uuid4().hex[:8]}"
                        if item.get("cache_intent") not in ["exact_duplicate", "semantic_near_miss", "shared_url", "semantic_far_miss"]:
                            item["cache_intent"] = "semantic_near_miss"
                        variants.append(TestCase.from_dict(item))
                
                if len(variants) > 0:
                    return variants
            except Exception as e:
                logger.warning(f"Error generating cache variants: {e}")
                
        return []

    async def generate(self, num_cases: int, previous_queries: Optional[List[str]] = None, previous_urls: Optional[List[str]] = None) -> List[TestCase]:
        logger.info(f"Generating {num_cases} test cases via two-phase domain-bucket sampling...")
        previous_queries = previous_queries or []
        previous_urls = previous_urls or []

        has_history = len(previous_queries) >= 3  # Need at least 3 past queries for a meaningful variant

        if not has_history:
            # No (or too little) history: generate all cases as novel anchors.
            # Cache is empty so variants would derive from nothing meaningful.
            logger.info(f"[TestGenerator] No history (or < 3 queries) — generating all {num_cases} as novel anchors.")
            generate_variants = False
        else:
            # With history: each call independently decides novel vs. variant.
            # 65/35 split: 65% novel anchors, 35% cache variants.
            generate_variants = random.random() < 0.35
            mode = "cache variants" if generate_variants else "novel anchors"
            logger.info(f"[TestGenerator] History available ({len(previous_queries)} past queries). "
                        f"This round: {num_cases} {mode} (coin flip).")

        if generate_variants:
            # Variant-only round: skip Phase 1, derive all cases from history reference pool
            num_anchors = 0
            num_variants = num_cases
            anchors = []
        else:
            # Anchor-only round: all cases are novel domain-bucket anchors
            num_anchors = num_cases
            num_variants = 0

            # Sample domain buckets with family uniqueness constraint:
            # at most one bucket per family group can be selected per batch.
            sampled_buckets = []
            used_families = set()
            shuffled = list(DOMAIN_BUCKETS)
            random.shuffle(shuffled)
            for bucket in shuffled:
                if len(sampled_buckets) >= num_anchors:
                    break
                family = bucket.get("family", bucket["name"])
                if family not in used_families:
                    sampled_buckets.append(bucket)
                    used_families.add(family)
            # If still short (very large num_anchors), fill remainder without family constraint
            remaining = [b for b in DOMAIN_BUCKETS if b not in sampled_buckets]
            random.shuffle(remaining)
            for bucket in remaining:
                if len(sampled_buckets) >= num_anchors:
                    break
                sampled_buckets.append(bucket)

            anchors = await self._generate_novel_anchors(sampled_buckets, previous_queries, previous_urls)

        if generate_variants:
            variants = await self._generate_cache_variants(anchors, previous_queries, previous_urls, num_variants)
        else:
            variants = []

        all_cases = anchors + variants

        if len(all_cases) < num_cases:
            logger.warning(f"Only generated {len(all_cases)}/{num_cases} valid test cases.")

        random.shuffle(all_cases)
        return all_cases[:num_cases]
