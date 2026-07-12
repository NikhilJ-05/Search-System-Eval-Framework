# Firecrawl Eval Report: run_20260712_173638
Generated: 2026-07-12 17:48:27

## Run Configuration
| Setting | Value |
|---|---|
| Generator Model | minimax/minimax-m3 |
| P1 Model (Extraction) | deepseek/deepseek-v4-flash |
| P2 Model (Reasoning)  | deepseek/deepseek-v4-flash |
| Improvement Agent | z-ai/glm-5.2 |
| Pass Threshold | 0.65 (floor: 0.4) |
| Test Cases | 3 |
| Duration | 11m 48s |

## Executive Summary
- **Overall Score**: 0.75 🟡
- **Test Cases**: 3 | Passed: 0 | Failed: 3

### Floor Failures (Dimension Score < 0.40)
- **TCs with floor failures**: 3 / 3
- **Most common floor dimension**: `_baseline_fidelity` (3 TCs)

## Dimension Performance Breakdown
| Dimension | Weight (avg) | Avg Score | Pass Rate | Floor Fails | Histogram |
|-----------|-------------|-----------|-----------|-------------|-----------|
| _baseline_ranking | 0.13 | 0.38 | 0.0% | 1 | <pre>  0.0-0.2  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| _baseline_fidelity | 0.13 | 0.44 | 16.7% | 3 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  3<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░  2<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓░░░░░░░░░░░░░░  1<br></pre> |
| temporal_currency | 0.22 | 0.55 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| content_specificity | 0.16 | 0.55 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| _baseline_coverage | 0.14 | 0.60 | 50.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| policy_specificity | 0.16 | 0.85 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| source_credibility | 0.16 | 0.85 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| diagnostic_criteria_coverage | 0.19 | 0.85 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| adult_specific_considerations | 0.17 | 0.85 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| assessment_tool_coverage | 0.17 | 0.90 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| source_authority | 0.16 | 0.91 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br></pre> |
| ai_focus_clarity | 0.10 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| _baseline_freshness | 0.07 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| temporal_relevance | 0.21 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |

## Most Frequently Unmet Rubric Criteria
| Condition (truncated) | Times Not Met |
|---|---|
| Higher-authority and more relevant sources appear before lower-quality ones. | 1 |
| The most relevant result is not buried. | 1 |
| Publication or last-updated dates should be verifiable and reflect the current a... | 1 |
| URL rank 2: https://oaisc.fas.harvard.edu/academic-integrity-and-teaching-withou... | 1 |
| URL rank 4: https://pmc.ncbi.nlm.nih.gov/articles/PMC11540794/ | 1 |
| Includes minimum duration requirements | 1 |
| URL rank 1: https://pmc.ncbi.nlm.nih.gov/articles/PMC11327143/ | 1 |
| URL rank 2: https://www.cdc.gov/adhd/diagnosis/index.html | 1 |

### Executive Diagnosis
This run achieved a pass rate of **0%** across 3 test cases. The primary bottleneck identified is **Broken or empty content not penalized in ranking signal**, impacting 2/3 TCs of the evaluated queries. Addressing the key root causes could yield a significant boost in performance, particularly on the **ranking** dimension.

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
| `novel` | 1 | 0.0% | 0.0% |
| `same_source_different_angle` | 1 | 0.0% | 0.0% |
| `exact_duplicate` | 1 | 0.0% | 0.0% |

## Chaos Archetype Analysis
| Archetype | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| temporal_ambiguity ⚠️ | 2 | 0.69 | 0.0% |
| none ⚠️ | 1 | 0.87 | 0.0% |

## Intent × Difficulty Analysis

### By Intent
| Intent | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| exploratory | 1 | 0.67 | 0.0% |
| factual_lookup | 2 | 0.80 | 0.0% |

### By Difficulty
| Difficulty | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| medium | 3 | 0.75 | 0.0% |

## Retrieval Comparison: Firecrawl vs KB vs Ideal
*(Evaluates if our RRF Hybrid KB outperforms Firecrawl's native ranking)*

| Metric | Firecrawl | Internal KB | Winner |
|--------|-----------|-------------|--------|
| Kendall's τ (vs Ideal, normalized 0→1) | 0.567 | 0.222 | Firecrawl 🏆 |
| Overlap@3 (vs Ideal) | 0.556 | 0.444 | Firecrawl 🏆 |
| Overlap@5 (vs Ideal) | 1.000 | 0.467 | Firecrawl 🏆 |
| KB Outperforms FC | - | - | 0.0% of TCs |

## Improvement Roadmap

### Root Causes (ranked by severity)
| # | Dimension | Issue | Severity | Confidence | Affected TCs | Frequency |
|---|-----------|-------|----------|------------|--------------|-----------|
| 1 | ranking | Broken or empty content not penalized in ranking signal | high | high | tc_44abe090, tc_52bd80e1 | 2/3 TCs |
| 2 | ranking | Authority × relevance composite signal absent — low-authority or irrelevant sources outrank high-relevance ones | high | high | tc_52bd80e1, tc_17585c39, tc_44abe090 | 3/3 TCs |
| 3 | scraping | JS-rendered and PDF-locked academic pages yield near-zero usable text | high | high | tc_44abe090 | 1/3 TCs (2 URLs within that TC) |
| 4 | ranking | Snippet collision causes low-authority mirror to outrank original source | high | medium | tc_52bd80e1 | 1/3 TCs |
| 5 | evaluation_harness | Duplicate _baseline_fidelity dimension inverts scrape_score scale (L1=best treated as 0.2/1.0=worst) | medium | high | tc_17585c39, tc_52bd80e1, tc_44abe090 | 3/3 TCs |

### Proposals (ranked by priority)
| # | Targets | Proposal | Expected Impact | Effort | Priority |
|---|---------|----------|-----------------|--------|----------|
| 1 | rc_001 | Add content-emptiness penalty to ranking pipeline | +0.15 on _baseline_ranking (tc_44abe090 UpToDate demoted, tc_52bd80e1 Facebook demoted) | low | 6.0 |
| 2 | rc_002 | Implement authority × query_relevance composite as final ranking signal | +0.20 on _baseline_ranking across all 3 TCs (Cornell promoted, CDC child demoted, ERS promoted) | medium | 4.5 |
| 3 | rc_003 | Two-stage scrape pipeline with headless browser fallback and PDF extraction | +0.15 on _baseline_fidelity, +0.10 on content_specificity (tc_44abe090 UpToDate and ERS full text captured) | medium | 3.0 |
| 4 | rc_005 | Unify _baseline_fidelity to single dimension instance with scale-mapping guard | +0.15 on _baseline_fidelity (tc_17585c39 false contrastive_fail eliminated, overall score +0.05) | low | 2.0 |
| 5 | rc_004 | Snippet-hash deduplication with authority-based collapse | +0.10 on _baseline_ranking (tc_52bd80e1 Facebook deduplicated, Harvard promoted to rank 1) | medium | 1.5 |

### Quick Wins
| # | Action | Description | Expected Impact |
|---|--------|-------------|-----------------|
| 1 | Filter out zero-content results before ranking | Add a post-scrape filter that removes any result with content_length < 50 characters or snippet matching loading-placeholder regex ('Loading|Please wait|Page content not loaded|Enable JavaScript') from the candidate pool before RRF fusion. This requires ~10 lines of code and directly fixes tc_52bd80e1 (Facebook 0 chars) and tc_44abe090 (UpToDate 20 chars). | +0.10 on _baseline_ranking |
| 2 | Remove duplicate _baseline_fidelity dimension from evaluation harness | Delete the second _baseline_fidelity dimension instance from the test configuration. The first instance correctly interprets the scrape_score scale. This is a config change, not a code change. | +0.05 overall (tc_17585c39 passes, false contrastive_fail removed) |
| 3 | Add .edu/.gov/.org domain authority boost for academic and medical queries | For queries containing 'guidelines', 'academic integrity', 'diagnostic criteria', or 'clinical', apply a 1.5x multiplier to results from .edu, .gov, .org domains and a 0.3x penalty to social media domains (facebook.com, reddit.com, twitter.com). Simple domain-suffix check, minimal effort. | +0.08 on _baseline_ranking (Facebook demoted, Cornell/Harvard promoted) |

### Cross-Dimension Failure Patterns
| Pattern | Hypothesis / Context |
|---------|----------------------|
| Scrape failures cascade into ranking failures across _baseline_fidelity and _baseline_ranking | When the scraper returns empty or placeholder content (UpToDate: 20 chars, Facebook: 0 chars), the ranking pipeline has no content-quality signal to penalize these results. The broken content occupies high ranks (rank 1-2), which simultaneously tanks _baseline_fidelity (content not captured) and _baseline_ranking (most relevant result buried). This is observed in tc_44abe090 (UpToDate rank 2 → fidelity 0.4, ranking 0.45) and tc_52bd80e1 (Facebook rank 1 → fidelity 0.5, ranking 0.15). |
| Duplicate _baseline_fidelity dimension creates systematic score deflation across all TCs | Every TC has two _baseline_fidelity entries with divergent scores (tc_52bd80e1: 0.5 vs 0.3386; tc_17585c39: 0.95 vs 0.2; tc_44abe090: 0.4 vs 0.256). The second instance consistently scores lower due to scale inversion (treating L1 scrape_score=0.2 as 20% quality). This artificially deflates the _baseline_fidelity average from a potential ~0.78 to 0.441, and triggers false contrastive_fail flags that cause all 3 TCs to fail overall. |
| Temporal_currency and content_specificity co-fail for factual lookup queries | Factual lookup queries (tc_44abe090, tc_17585c39) show degraded content_specificity (avg 0.275) and temporal_relevance (avg 0.475) compared to exploratory queries. When the scraper fails to extract full-text from clinical guideline pages (UpToDate, ERS, ScienceDirect PDF), the remaining content is either abstracts or navigation chrome, which lacks the specific clinical details (drug names, dosages, diagnostic thresholds) needed for high content_specificity scores. |

### Judge Bias Warnings
- ⚠️ The duplicate _baseline_fidelity dimension in tc_17585c39 scores 0.2 (L2) while the first instance scores 0.95 (L5) for the exact same scrape results — this is a systematic scale-interpretation contradiction where the same evidence produces scores differing by 0.75 points. The second instance's contrastive_fail=true directly contradicts the first instance's 'All five documents have scrape scores of 0.2 (L1 level), indicating high-fidelity markdown' assessment. This is not a scoring disagreement but a dimension-configuration bug in the judge harness.

## RL Training Signals
| Signal Type | Count | Output File |
|-------------|-------|-------------|
| DPO Pairs | 1 | dpo_pairs.jsonl |
| Reward Signals | 15 | rewards.jsonl |
| Listwise Rankings | 3 | listwise_rankings.jsonl |
| Contrastive Fail Pairs | 4 | contrastive_fail_pairs.jsonl |
| Query Reformulations | 3 | query_reformulations.jsonl |
| SFT Gold Examples | 0 | sft_gold.jsonl |
| Scrape Quality Labels | 15 | scrape_quality_labels.jsonl |

### Improvement Taxonomy (Micro-Patterns)
| Issue | Severity | Frequency | Description |
|-------|----------|-----------|-------------|
| empty_content_ranking_inflation |  | 67% (2/3 TCs) | Results with 0-20 characters of scraped content (Facebook: 0 chars, UpToDate: 20 chars) are ranked in positions 1-2, indicating the ranking pipeline does not incorporate content-availability as a signal. Broken results should be filtered or heavily penalized before RRF fusion. |
| authority_relevance_disjoint |  | 100% (3/3 TCs) | In every TC, at least one low-authority or query-irrelevant source outranks a high-relevance source. Facebook (auth=0.2) above Cornell (rel=0.95); CDC child ADHD (rel=0.2) above ScienceDirect (rel=0.95); IDSA acute COVID (rel=0.0) above ERS long COVID (rel=1.0). The ranking signal does not combine authority and relevance into a composite. |
| snippet_collision_mirror_inversion |  | 33% (1/3 TCs) | When a low-authority page mirrors the snippet of a high-authority page (Facebook copying Harvard's 'Strict AI Policies' text), the ranker treats both as equally relevant and may place the mirror first due to tie-breaking by recency or other secondary signals. |
| js_paywall_content_loss |  | 33% (1/3 TCs, 2 URLs) | JS-rendered pages (UpToDate) return loading placeholders and PDF-locked academic pages (ERS) return only abstracts. These are often the most content-rich sources for medical queries, so their loss disproportionately impacts content_specificity and diagnostic_criteria_coverage. |
| duplicate_dimension_scale_inversion |  | 100% (3/3 TCs) | A duplicate _baseline_fidelity dimension inverts the scrape_score scale (L1=best interpreted as 0.2/1.0=worst), creating false contrastive_fail flags and deflating fidelity scores by ~0.3 points across all TCs. |

## Regression vs Previous Run
- Trend: Stable ➡️
- Difference: +0.00

## Appendix: Failed Test Cases Detail
*(Showing only test cases that failed the pass threshold or hit a dimension floor)*

### tc_52bd80e1 (Score: 0.67) ❌
**Query**: `latest academic integrity guidelines for AI tools in college classrooms`
**Category**: Education & Academia | **Intent**: novel

**Root Cause**: The primary failure is a ranking inversion where a Facebook post (authority_score=0.2, query_relevance_score=0.3) was placed at rank 1 while the most relevant source, Cornell (authority_score=0.9, query_relevance_score=0.95), was buried at rank 5. Compounding this, Harvard (rank 2) and PMC (rank 4) received scrape_scores of 0.20 despite their scrape_reasoning claiming faithful content capture, and both Harvard and Cornell lack publication dates, failing the 'latest' temporal requirement.

- **Coverage Diagnosis**: The document set covers policy-specific content well (Harvard syllabus strategies, Cornell AI policy icons, APA AI Assessment Scale) but fails the temporal 'latest' requirement: Harvard has publication_date='' and temporal_markers=[], Cornell has publication_date='' with only 2023 temporal markers, leaving only APA (2025-08-14) as a verifiably current source.
- **Ranking Diagnosis**: Rank 1 (Facebook, authority 0.2, relevance 0.3) outranks all institutional sources; Rank 5 (Cornell, authority 0.9, relevance 0.95) is the most relevant but appears last. The identical snippets between rank 1 and rank 2 suggest snippet collision or content mirroring that misled the retrieval ranker.
- **Scrape Diagnosis**: Harvard (scrape_score=0.20, issues=[]) and PMC (scrape_score=0.20, issues=[]) have critically low scores with empty issue lists, contradicting their scrape_reasoning which claims 'faithfully captures all visible content.' Cornell (0.40) and APA (0.40) have moderate scores with boilerplate noise. Facebook (0.79) scored highest despite being truncated — the scoring appears inverted relative to actual content utility.

**Fix Actions**:
- Add an authority-weighted reranking pass that penalizes commercial/forum domain_types (e.g., facebook.com) and boosts academic domain_types when query category is 'Education & Academia', ensuring authority_score and query_relevance_score are used as primary sort keys before snippet-match signals.
- Fix the scrape_score calculation for pages where scrape_issues=[] and content_completeness='complete' but score is 0.20 — investigate whether word_count thresholds or HTML structure heuristics are incorrectly penalizing pages with low nav_link_ratio or missing tables/images; Harvard (1333 words) and PMC (8458 words) should not receive L1 scores.
- Implement a snippet deduplication check in the retrieval pipeline to detect when two results share identical snippet text (as seen between rank 1 Facebook and rank 2 Harvard), and collapse or penalize the lower-authority duplicate to prevent content mirroring from inflating a low-quality source's rank.
- Add a temporal metadata extraction pass that checks for <meta> tags (article:published_time, og:updated_time) or visible 'last updated' text on institutional pages, and boost ranking for results with verifiable recent dates when the query contains 'latest'.


---
### tc_17585c39 (Score: 0.87) ❌
**Query**: `evidence based diagnostic criteria and assessment methods for adult ADHD`
**Category**: Healthcare & Medical | **Intent**: same_source_different_angle

**Root Cause**: The second _baseline_fidelity dimension (score=0.2, contrastive_fail=true) misinterprets scrape_score=0.2 as poor quality when it actually represents L1 (highest fidelity), as correctly identified by the first _baseline_fidelity dimension (score=0.95, 'All five documents have scrape scores of 0.2 (L1 level), indicating high-fidelity markdown'). This duplicate dimension's false contrastive fail is the primary driver of the test failure. Additionally, the CDC child ADHD page at Rank 2 (query_relevance_score=0.2, answers_query=false) is ranked above ScienceDirect at Rank 4 (query_relevance_score=0.95), causing the _baseline_ranking dimension to score only 0.55.

- **Coverage Diagnosis**: Document profiles show strong coverage of adult ADHD diagnostic criteria, assessment tools, and adult-specific considerations — all scoring L5. The only critical coverage gap is the CDC page (Rank 2), whose profile explicitly lists 'Lack of content on adult ADHD diagnostic criteria and assessment methods' as a critical content gap and rates answers_query=false.
- **Ranking Diagnosis**: Rank 2 (CDC, relevance=0.2, child-focused) is positioned above Rank 4 (ScienceDirect, relevance=0.95, adult ADHD screening tools) and Rank 5 (TherapyLab, relevance=0.8), violating the ordering principle that higher-relevance sources should appear before lower-relevance ones of comparable authority.
- **Scrape Diagnosis**: All five documents have scrape_score=0.2 and scrape_level=L1, indicating high-fidelity markdown. The second _baseline_fidelity dimension incorrectly averages these 0.2 values as raw quality scores (0.2/1.0) rather than recognizing them as L1-level indicators, producing a false 'poor' verdict.

**Fix Actions**:
- Deduplicate the _baseline_fidelity dimension evaluation or fix the second instance's scoring logic to correctly interpret scrape_score=0.2 as L1 (highest fidelity) rather than as a raw 0.2/1.0 quality score, preventing the false contrastive fail.
- Add a query-relevance weighting factor to the ranking algorithm so that high-authority but low-relevance pages (e.g., CDC child ADHD, relevance=0.2) cannot outrank high-relevance pages (e.g., ScienceDirect, relevance=0.95) when authority scores are within 0.1 of each other.
- Implement a query-intent filter that demotes pages whose primary_topic and content_gaps indicate topical mismatch (e.g., CDC page with 'critical' gap for adult ADHD) below pages with full query coverage.


---
### tc_44abe090 (Score: 0.72) ❌
**Query**: `latest clinical guidelines for managing long COVID symptoms in adults`
**Category**: Healthcare & Medical | **Intent**: exact_duplicate

**Root Cause**: The ERS long COVID guideline (query_relevance=1.0, scrape_score=0.40) was buried at rank 5 behind a broken UpToDate page (scrape_score=0.20, no content captured) at rank 2 and an irrelevant IDSA acute COVID-19 guideline (query_relevance=0.0) at rank 4. Additionally, the scraper failed to extract full text from the two most content-rich sources: UpToDate returned only a loading placeholder and ERS returned only an abstract with the full text locked behind a PDF.

- **Coverage Diagnosis**: The correct authoritative sources were found (CDC, ERS), but the most specific guideline (ERS, Doc5) only yielded an abstract — its 10 evidence-based recommendations, detailed treatment pathways, and referral criteria were not extracted from the PDF. Doc1 (CDC) also lacks specific medication algorithms, leaving referral criteria entirely absent across all profiles.
- **Ranking Diagnosis**: The most relevant result (ERS, query_relevance=1.0) is at rank 5, while a broken page (UpToDate, query_relevance=0.0) occupies rank 2 and an irrelevant page (IDSA, query_relevance=0.0 for long COVID) occupies rank 4. This violates the expectation that relevant sources precede irrelevant or broken ones.
- **Scrape Diagnosis**: UpToDate (scrape_score=0.20) captured only a 3-word loading placeholder due to JS/auth requirements. ERS (scrape_score=0.40) captured only abstract metadata with full text locked in PDF. CDC (scrape_score=0.20) has complete text but images not rendered. IDSA (scrape_score=0.40) has tables as image links. Average scrape quality is 0.256 (L2), dragging overall fidelity to failure.

**Fix Actions**:
- Add a JavaScript-rendering fallback (e.g., headless browser via Playwright/Puppeteer) for pages that return loading placeholders on initial fetch, specifically targeting commercial clinical reference sites like uptodate.com that require client-side rendering.
- Add a PDF extraction pipeline step that detects PDF-only academic pages (e.g., ersnet.org) and downloads + parses the linked PDF to extract full-text recommendations, evidence tables, and discussion sections into the markdown profile.
- Implement a post-retrieval re-ranking penalty: any result with scrape_score < 0.3 or content_completeness='error_page' should be demoted below all results with content_completeness='complete' or 'partial', and results with query_relevance=0.0 should not appear above results with query_relevance > 0.5.
- Add image-to-table OCR extraction for pages where tables are rendered as images (e.g., idsociety.org) to preserve structured data in markdown.


---
