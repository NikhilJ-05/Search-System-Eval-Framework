# Firecrawl Eval Report: run_20260712_154927
Generated: 2026-07-12 15:59:33

## Run Configuration
| Setting | Value |
|---|---|
| Generator Model | minimax/minimax-m3 |
| P1 Model (Extraction) | deepseek/deepseek-v4-flash |
| P2 Model (Reasoning)  | deepseek/deepseek-v4-flash |
| Improvement Agent | z-ai/glm-5.2 |
| Pass Threshold | 0.65 (floor: 0.4) |
| Test Cases | 3 |
| Duration | 10m 5s |

## Executive Summary
- **Overall Score**: 0.75 🟡
- **Test Cases**: 3 | Passed: 0 | Failed: 3

### Floor Failures (Dimension Score < 0.40)
- **TCs with floor failures**: 3 / 3
- **Most common floor dimension**: `_baseline_fidelity` (4 TCs)

## Dimension Performance Breakdown
| Dimension | Weight (avg) | Avg Score | Pass Rate | Floor Fails | Histogram |
|-----------|-------------|-----------|-----------|-------------|-----------|
| _baseline_fidelity | 0.12 | 0.41 | 16.7% | 4 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  4<br>  0.4-0.6  ▓▓▓▓▓░░░░░░░░░░░░░░░  1<br>  0.6-0.8  ▓▓▓▓▓░░░░░░░░░░░░░░░  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| _baseline_ranking | 0.12 | 0.43 | 0.0% | 1 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| content_specificity | 0.19 | 0.55 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| _baseline_coverage | 0.12 | 0.55 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| temporal_accuracy | 0.21 | 0.55 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| actionable_clinical_detail | 0.21 | 0.72 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| _baseline_freshness | 0.07 | 0.75 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| coverage_completeness | 0.17 | 0.85 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| source_authority | 0.20 | 0.87 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br></pre> |
| temporal_relevance | 0.26 | 0.90 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| quantitative_specificity | 0.17 | 0.90 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| treatment_modality_coverage | 0.28 | 0.93 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |

## Most Frequently Unmet Rubric Criteria
| Condition (truncated) | Times Not Met |
|---|---|
| Results are ordered by decreasing relevance and authority. | 1 |
| No high-relevance, high-authority result is placed after a low-relevance or low-... | 1 |
| Include referral criteria | 1 |
| URL rank 1: https://www.cdc.gov/long-covid/hcp/clinical-guidance/index.html | 1 |
| URL rank 2: https://www.uptodate.com/contents/covid-19-management-of-adults-with... | 1 |
| Higher-authority and more relevant sources appear before lower-quality ones. | 1 |
| Irrelevant or low-quality results do not occupy top positions. | 1 |
| Scraped markdown preserves the page's structural elements and content is complet... | 1 |

### Executive Diagnosis
This run achieved a pass rate of **0%** across 3 test cases. The primary bottleneck identified is **Scrape quality not factored into ranking — empty/placeholder content occupies top positions**, impacting 1/3 TCs (33%) of the evaluated queries. Addressing the key root causes could yield a significant boost in performance, particularly on the **ranking** dimension.

## Batch Progression (KB Build)
| Round | TCs | New Indexed | Deduped (Hits) |
|-------|-----|-------------|----------------|
| 1 | 1 | 0 | 0 |
| 2 | 1 | 0 | 0 |
| 3 | 1 | 0 | 0 |

## Two-Layer Cache Analytics
- **Layer 1 (Query) Cache Hit Rate**: 0.0% (0/3)
- **Layer 2 (Content) Cache Hit Rate**: 0.0% (0/14)

### Cache Intent Validation
*(Did the generator successfully trick the cache?)*
| Generator Intent | Count | Query Hit % | Content Hit % |
|------------------|-------|-------------|---------------|
| `novel` | 2 | 0.0% | 0.0% |
| `same_source_different_angle` | 1 | 0.0% | 0.0% |

## Chaos Archetype Analysis
| Archetype | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| temporal_ambiguity ⚠️ | 2 | 0.72 | 0.0% |
| none ⚠️ | 1 | 0.80 | 0.0% |

## Intent × Difficulty Analysis

### By Intent
| Intent | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| real_time | 1 | 0.70 | 0.0% |
| factual_lookup | 2 | 0.77 | 0.0% |

### By Difficulty
| Difficulty | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| medium | 3 | 0.75 | 0.0% |

## Retrieval Comparison: Firecrawl vs KB vs Ideal
*(Evaluates if our RRF Hybrid KB outperforms Firecrawl's native ranking)*

| Metric | Firecrawl | Internal KB | Winner |
|--------|-----------|-------------|--------|
| Kendall's τ (vs Ideal, normalized 0→1) | 0.700 | 0.556 | Firecrawl 🏆 |
| Overlap@3 (vs Ideal) | 0.778 | 0.222 | Firecrawl 🏆 |
| Overlap@5 (vs Ideal) | 1.000 | 0.533 | Firecrawl 🏆 |
| KB Outperforms FC | - | - | 33.3% of TCs |

## Improvement Roadmap

### Root Causes (ranked by severity)
| # | Dimension | Issue | Severity | Confidence | Affected TCs | Frequency |
|---|-----------|-------|----------|------------|--------------|-----------|
| 1 | ranking | Scrape quality not factored into ranking — empty/placeholder content occupies top positions | high | high | tc_07387cb6 | 1/3 TCs (33%) |
| 2 | fidelity | Scrape scoring pipeline assigns floor score of 0.20 to pages with confirmed complete extraction | high | high | tc_4e35a808, tc_336bac9a, tc_07387cb6 | 3/3 TCs (100%) |
| 3 | ranking | Domain authority signal overrides semantic relevance — high-authority low-relevance pages outrank high-relevance pages | high | high | tc_336bac9a, tc_07387cb6 | 2/3 TCs (67%) |
| 4 | ranking | Geographic intent not resolved — US-focused page ranks #1 for Japan-specific query | high | medium | tc_4e35a808 | 1/3 TCs (33%) |
| 5 | fidelity | Boilerplate and navigation elements leak into scraped markdown, depressing fidelity scores | medium | high | tc_336bac9a, tc_07387cb6, tc_4e35a808 | 3/3 TCs (100%) |

### Proposals (ranked by priority)
| # | Targets | Proposal | Expected Impact | Effort | Priority |
|---|---------|----------|-----------------|--------|----------|
| 1 | rc_003 | Introduce relevance floor gate in ranking function | +0.20 on _baseline_ranking (UC Davis promoted from rank 5 to rank 1-2 in tc_336bac9a; ERS promoted in tc_07387cb6) | low | 6.0 |
| 2 | rc_002 | Audit and fix scrape_score calculation pipeline — floor score bug for complete extractions | +0.25 on _baseline_fidelity (all 3 TCs would move from L2 to L4-L5) | medium | 4.5 |
| 3 | rc_001 | Implement scrape-quality-aware ranking penalty | +0.15 on _baseline_ranking (ERS guideline promoted from rank 5 to rank 2-3 in tc_07387cb6) | medium | 3.0 |
| 4 | rc_005 | Enhance boilerplate stripping with site-specific rules and structural element preservation | +0.15 on _baseline_fidelity across all TCs | medium | 2.0 |
| 5 | rc_004 | Add geographic intent detection and destination-country boosting | +0.15 on _baseline_ranking for tc_4e35a808 (cbp.gov demoted, Japan embassy/JAL promoted to ranks 1-2) | medium | 1.0 |

### Quick Wins
| # | Action | Description | Expected Impact |
|---|--------|-------------|-----------------|
| 1 | Add content_length threshold filter to ranking | If scraped content_length < 100 characters, apply a 0.1x penalty multiplier to the ranking score. This would immediately fix tc_07387cb6 where UpToDate (20 chars, 'Loading') is at rank 2, requiring only a single conditional in the post-scrape ranking step. | +0.10 on _baseline_ranking for tc_07387cb6 |
| 2 | Switch ranking from additive to multiplicative relevance×authority | Change the ranking formula from (α·relevance + β·authority) to (relevance^γ × authority^δ) with γ=1.0, δ=0.5. This one-line change ensures relevance=0.1 can never outrank relevance=0.95 regardless of authority, fixing tc_336bac9a and tc_07387cb6 simultaneously. | +0.15 on _baseline_ranking across 2/3 TCs |
| 3 | Add 'Skip to' and '.gov website' patterns to boilerplate blocklist | Add regex patterns for '[Skip to.*content]', 'Official websites use .gov', 'A .gov website belongs to', and cookie/login notices to the existing boilerplate stripper. Low effort, immediately improves fidelity signal for all .gov pages. | +0.05 on _baseline_fidelity across all TCs |

### Cross-Dimension Failure Patterns
| Pattern | Hypothesis / Context |
|---------|----------------------|
| Scrape fidelity failure cascades into ranking degradation | When scrape_score is low (0.20) due to boilerplate leakage or placeholder content, the ranking system does not penalize these results, allowing low-quality scrapes to occupy top positions. This creates a compounding failure: poor extraction → poor content signal → poor ranking → poor fidelity score. The _baseline_fidelity dimension (avg 0.407, all L2) and _baseline_ranking dimension (avg 0.433, all L2-L3) are correlated because the ranking function lacks a scrape-quality input. |
| High source_authority masks low _baseline_ranking across all TCs | source_authority averages 0.867 (L4-L5) while _baseline_ranking averages 0.433 (L2-L3). The system successfully retrieves authoritative domains (CDC, NIH, .gov) but fails to order them by query relevance. This suggests the retrieval stage (surfacing authoritative sources) is functioning, but the ranking stage (ordering by relevance) is broken — the authority signal dominates the relevance signal in the final sort. |
| Temporal relevance is high but temporal accuracy is low — system finds recent content but misattributes dates | temporal_relevance averages 0.9 (L5) but temporal_accuracy averages 0.55 (L3). In tc_4e35a808, the Japan embassy page shows '2026/4/15' but temporal_accuracy=0.55, suggesting the system may not be correctly parsing or validating publication dates from scraped content, or the judge is penalizing for missing date metadata even when content is current. |

### Judge Bias Warnings
- ⚠️ Potential systematic under-scoring of _baseline_fidelity: In tc_4e35a808, the judge's own scrape_reasoning confirms 'The markdown preserves all textual content' and 'faithfully reproduces all content' with content_completeness='complete', yet assigns scrape_score=0.20. This is not a dimension scoring HIGH while root causes show FAILING — rather, it is the opposite: the fidelity dimension consistently scores LOW (all L2) while the judge's own reasoning evidence supports higher scores. This suggests the scrape_score calculation function (not the LLM judge) has a floor-score bug that systematically deflates fidelity regardless of actual extraction quality.

## RL Training Signals
| Signal Type | Count | Output File |
|-------------|-------|-------------|
| DPO Pairs | 1 | dpo_pairs.jsonl |
| Reward Signals | 15 | rewards.jsonl |
| Listwise Rankings | 3 | listwise_rankings.jsonl |
| Contrastive Fail Pairs | 2 | contrastive_fail_pairs.jsonl |
| Query Reformulations | 3 | query_reformulations.jsonl |
| SFT Gold Examples | 0 | sft_gold.jsonl |
| Scrape Quality Labels | 15 | scrape_quality_labels.jsonl |

### Improvement Taxonomy (Micro-Patterns)
| Issue | Severity | Frequency | Description |
|-------|----------|-----------|-------------|
| empty_scrape_rank_inflation |  | 33% | Pages with placeholder or navigation-only content (content_length < 100, e.g., 'Loading\n\nPlease wait') occupy top-3 ranking positions, displacing highly relevant results. The ranking function has no scrape-quality awareness. |
| authority_overrides_relevance |  | 67% | High-authority domains (CDC, IDSA with authority=1.0) outrank semantically superior results (UC Davis, ERS with relevance=0.9+) when their query_relevance is 0.1 or below. The additive ranking formula allows authority to compensate for near-zero relevance. |
| scrape_score_floor_bug |  | 100% | Pages with confirmed complete extraction (content_completeness='complete', reasoning confirms faithful reproduction) receive scrape_score=0.20 instead of a passing score, systematically deflating _baseline_fidelity to L2 across all TCs. |
| geographic_intent_misresolution |  | 33% | Queries with explicit geographic destination ('entering Japan') surface origin-country government pages (cbp.gov) at rank 1, because keyword matching on 'customs' and 'duty-free' overrides geographic scope detection. |
| boilerplate_leakage |  | 100% | Government website banners ('Official websites use .gov'), accessibility skip-links ('[Skip to main content]'), cookie notices, and social share buttons leak into scraped markdown, depressing fidelity scores and polluting content signals. |

## Regression vs Previous Run
- Trend: Stable ➡️
- Difference: +0.01

## Appendix: Failed Test Cases Detail
*(Showing only test cases that failed the pass threshold or hit a dimension floor)*

### tc_07387cb6 (Score: 0.74) ❌
**Query**: `latest clinical guidelines for managing long COVID symptoms in adults`
**Category**: Healthcare & Medical | **Intent**: novel

**Root Cause**: The ranking model failed to demote a non-functional UpToDate scrape (scrape_score=0.2, content='Loading' placeholder only, query_relevance_score=0.0) from rank 2, and placed an off-topic IDSA acute COVID guideline (query_relevance_score=0.1) at rank 4, while the highly relevant ERS long COVID guideline (query_relevance_score=0.9, publication_date=2026-03-05) was buried at rank 5. Additionally, scrape failures on UpToDate (empty content) and ERS (abstract-only, PDF not extracted) degraded fidelity and coverage.

- **Coverage Diagnosis**: The document profiles show that only CDC (full) and ERS (partial — abstract only) directly address long COVID management guidelines. ACP is tangential (resource listing, not guidelines), IDSA covers acute COVID only, and UpToDate has zero content. Critical gaps include no referral criteria in any profile, no step-by-step symptom management pathways, and no coverage of cognitive symptoms or dysautonomia management.
- **Ranking Diagnosis**: ERS (rank 5, relevance 0.9, authority 0.95) is placed after UpToDate (rank 2, relevance 0.0) and IDSA (rank 4, relevance 0.1), violating decreasing relevance ordering. The contrastive fail was triggered because the most relevant non-CDC result is buried behind two irrelevant results.
- **Scrape Diagnosis**: UpToDate (scrape_score=0.2) returned only 'Loading' and 'Please wait' placeholder text — a JavaScript-rendered page that was not executed. ERS (scrape_score=0.4) captured only the abstract; the full guideline PDF was not fetched or extracted. IDSA (scrape_score=0.6) lost all table data because tables were embedded as images without text extraction.

**Fix Actions**:
- Add a post-scrape content validation gate that demotes or removes results where word_count < 50 or content_completeness='navigation_only', preventing empty UpToDate-style pages from occupying top ranks.
- Enable JavaScript rendering (headless browser) for known SPA-heavy domains like uptodate.com, or add domain-specific scrape rules that wait for dynamic content load completion before extracting.
- Implement PDF auto-fetch and extraction for academic journal landing pages (e.g., ersnet.org) where the full text is linked as a PDF, so the complete guideline content is included in the markdown rather than only the abstract.
- Add a relevance-aware re-ranking pass that penalizes results whose query_relevance_score is below 0.3 when higher-relevance results exist at lower ranks, specifically preventing off-topic results like IDSA acute COVID guidelines from appearing above directly relevant long COVID guidelines.


---
### tc_4e35a808 (Score: 0.70) ❌
**Query**: `what customs duty-free allowances and import restrictions apply to US citizens entering Japan - alcohol, tobacco, currency declaration thresholds, and prohibited or restricted items`
**Category**: Travel & Geography | **Intent**: same_source_different_angle

**Root Cause**: Rank 1 (cbp.gov) has query_relevance_score=0.0 and answers_query=false yet occupies the top position, while Ranks 1-3 all received scrape_score=0.20 despite scrape_reasoning stating 'The markdown preserves all textual content' (Rank 1) and 'faithfully reproduces all content' (Rank 3), indicating a systemic scrape scoring defect that artificially deflated fidelity from what the actual extraction quality warrants.

- **Coverage Diagnosis**: The document profiles at Ranks 2, 3, and 5 collectively cover alcohol, tobacco, currency declaration (¥1,000,000), and prohibited items, but the official Japan Customs portal (customs.go.jp) is entirely absent from the result set, leaving a gap in primary-source coverage.
- **Ranking Diagnosis**: Rank 1 (cbp.gov, query_relevance_score=0.0) is placed above Rank 2 (denver.us.emb-japan.go.jp, relevance 0.85) and Rank 3 (jal.co.jp, relevance 1.0), a critical position deviation where a zero-relevance page outranks two highly relevant pages. Rank 4 (Facebook, relevance 0.0) also occupies a position that should have gone to a relevant result.
- **Scrape Diagnosis**: Ranks 1-3 all have scrape_score=0.20 with scrape_reasoning confirming complete content ('preserves all textual content, headings, lists, tables, and navigation elements without any apparent loss or truncation' for Rank 1; 'faithfully reproduces all content' for Rank 3), revealing a disconnect between the scoring logic and the actual extraction quality. Rank 4 (Facebook) is severely truncated to 27 words with 'Content truncated to a single incomplete sentence' and 'Entire article body likely missing'.

**Fix Actions**:
- Add a query-intent classifier gate that detects destination-country entities (e.g., 'Japan') in the query and penalizes or filters results whose primary_topic does not mention that country, preventing cbp.gov (US-focused) from ranking for Japan-specific queries.
- Fix the scrape_score computation pipeline: investigate why pages with scrape_reasoning='preserves all textual content' and content_completeness='complete' receive scrape_score=0.20 — likely a normalization bug or a missing feature signal causing all 'clean' pages to default to a floor score.
- Add customs.go.jp to the retrieval seed-URL allowlist or boost its domain authority weight for queries containing 'Japan customs' or 'Japan duty-free' to ensure the official source is retrieved.
- Add a Facebook/social-media URL pattern filter that either skips these domains entirely or applies a heavy relevance penalty, preventing truncated social posts from consuming result slots.


---
### tc_336bac9a (Score: 0.80) ❌
**Query**: `evidence based treatment options for adult ADHD management`
**Category**: Healthcare & Medical | **Intent**: novel

**Root Cause**: The ranking algorithm places Rank 4 (https://www.cdc.gov/adhd/treatment/index.html, query_relevance=0.1, authority=1.0) and Rank 3 (https://www.adhdevidence.org/blog/evidence-based-interventions-for-adhd, query_relevance=0.4) above Rank 5 (https://health.ucdavis.edu/mind-institute/resources/understanding-adhd/adhd-treatment, query_relevance=0.95, authority=0.95), indicating the ranker is weighting domain authority over semantic relevance to the 'adult ADHD' query. Additionally, the aggregated scrape fidelity is 0.284 (L2) because every page scores 0.20-0.40 due to boilerplate leakage (PMC gov banner, ADDA share buttons/comment sections) and missing structural elements (H1 titles, embedded images).

- **Coverage Diagnosis**: No significant coverage gap — treatment_modality_coverage is 0.93 (L5). However, Rank 5 (UC Davis) has a critical content gap: 'Missing pharmacological treatment options (e.g., stimulants, non-stimulants) which are first-line evidence-based treatments for adult ADHD,' meaning its individual coverage is partial despite high relevance.
- **Ranking Diagnosis**: Rank 5 (UC Davis, relevance 0.95, authority 0.95) is buried behind Rank 3 (ADHD Evidence, relevance 0.4) and Rank 4 (CDC, relevance 0.1). The CDC page is entirely about child/adolescent ADHD treatment and should not appear in the top 5 for an adult-specific query. The ranker appears to boost high-authority government domains regardless of query-relevance signals.
- **Scrape Diagnosis**: All five pages have scrape_score ≤ 0.40. Rank 1 (PMC, scrape_score=0.20) retains gov banner and NLM disclaimer boilerplate. Rank 2 (ADDA, scrape_score=0.40) is missing H1 and includes share buttons, comment sections, and refund popups. Rank 4 (CDC, scrape_score=0.20) has no listed issues yet scores 0.20, suggesting the scoring heuristic may be overly punitive for government pages with standard navigation chrome.

**Fix Actions**:
- Adjust the ranking scoring function to apply a query-relevance penalty multiplier (e.g., relevance^2) so that pages with relevance < 0.3 cannot outrank pages with relevance > 0.9, regardless of authority score — this would push the CDC child-ADHD page (relevance 0.1) below the UC Davis page (relevance 0.95).
- Add a query-term-matching filter that demotes pages whose primary_topic or key_claims do not contain the query's key entity ('adult') — the CDC page's section summaries explicitly reference 'children younger than 6 years' and 'children 6 years and older,' which should trigger a demotion for an adult-focused query.
- Enhance the scraper's boilerplate removal pipeline to strip gov banners, NLM disclaimers, cookie consent overlays, share-button clusters, comment sections, and 'related posts' blocks before markdown conversion, and inject a synthetic H1 from the page title field when no H1 is detected in the body.


---
