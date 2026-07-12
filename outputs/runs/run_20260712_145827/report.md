# Firecrawl Eval Report: run_20260712_145827
Generated: 2026-07-12 15:13:32

## Run Configuration
| Setting | Value |
|---|---|
| Generator Model | minimax/minimax-m3 |
| P1 Model (Extraction) | deepseek/deepseek-v4-flash |
| P2 Model (Reasoning)  | deepseek/deepseek-v4-pro |
| Improvement Agent | z-ai/glm-5.2 |
| Pass Threshold | 0.65 (floor: 0.4) |
| Test Cases | 3 |
| Duration | 15m 4s |

## Executive Summary
- **Overall Score**: 0.74 🟡
- **Test Cases**: 3 | Passed: 1 | Failed: 2

### Floor Failures (Dimension Score < 0.40)
- **TCs with floor failures**: 2 / 3
- **Most common floor dimension**: `_baseline_fidelity` (2 TCs)

## Dimension Performance Breakdown
| Dimension | Weight (avg) | Avg Score | Pass Rate | Floor Fails | Histogram |
|-----------|-------------|-----------|-----------|-------------|-----------|
| _baseline_fidelity | 0.12 | 0.44 | 0.0% | 2 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  2<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  4<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| temporal_accuracy | 0.30 | 0.50 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| coverage_completeness | 0.19 | 0.55 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| _baseline_ranking | 0.12 | 0.57 | 33.3% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| coverage | 0.28 | 0.71 | 50.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| _baseline_freshness | 0.07 | 0.72 | 50.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| source_authority | 0.18 | 0.83 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br></pre> |
| actionability | 0.17 | 0.85 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| technical_accuracy | 0.21 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |

## Most Frequently Unmet Rubric Criteria
| Condition (truncated) | Times Not Met |
|---|---|
| Content is complete without truncation | 2 |
| Higher-authority and more relevant sources appear before lower-quality ones. | 1 |
| Contrastive fail not triggered (no blog above official sources; most relevant no... | 1 |
| Boilerplate leakage is minimal (navigation noise does not dominate) | 1 |
| URL rank 4: https://istio.io/latest/docs/tasks/security/authentication/mtls-migr... | 1 |
| URL rank 5: https://stackoverflow.com/questions/70944846/how-to-provide-mutual-t... | 1 |
| Boilerplate leakage (navigation noise, cookie banners) is absent | 1 |
| Content addresses any current policy changes such as updated tax-free shopping t... | 1 |

### Executive Diagnosis
This run achieved a pass rate of **33%** across 3 test cases. The primary bottleneck identified is **Authority-relevance inversion: snippet keyword match over-weighted vs. domain authority and content completeness**, impacting 2/3 TCs of the evaluated queries. Addressing the key root causes could yield a significant boost in performance, particularly on the **ranking** dimension.

## Batch Progression (KB Build)
| Round | TCs | New Indexed | Deduped (Hits) |
|-------|-----|-------------|----------------|
| 1 | 1 | 0 | 0 |
| 2 | 1 | 0 | 0 |
| 3 | 1 | 0 | 0 |

## Two-Layer Cache Analytics
- **Layer 1 (Query) Cache Hit Rate**: 0.0% (0/3)
- **Layer 2 (Content) Cache Hit Rate**: 0.0% (0/13)

### Cache Intent Validation
*(Did the generator successfully trick the cache?)*
| Generator Intent | Count | Query Hit % | Content Hit % |
|------------------|-------|-------------|---------------|
| `novel` | 2 | 0.0% | 0.0% |
| `rephrased_same_intent` | 1 | 0.0% | 0.0% |

## Chaos Archetype Analysis
| Archetype | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| temporal_ambiguity ⚠️ | 1 | 0.66 | 0.0% |
| none | 2 | 0.78 | 50.0% |

## Intent × Difficulty Analysis

### By Intent
| Intent | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| real_time | 1 | 0.66 | 0.0% |
| tutorial_howto | 2 | 0.78 | 50.0% |

### By Difficulty
| Difficulty | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| medium | 2 | 0.68 | 0.0% |
| easy | 1 | 0.86 | 100.0% |

## Retrieval Comparison: Firecrawl vs KB vs Ideal
*(Evaluates if our RRF Hybrid KB outperforms Firecrawl's native ranking)*

| Metric | Firecrawl | Internal KB | Winner |
|--------|-----------|-------------|--------|
| Kendall's τ (vs Ideal, normalized 0→1) | 0.667 | 0.611 | Firecrawl 🏆 |
| Overlap@3 (vs Ideal) | 0.778 | 0.444 | Firecrawl 🏆 |
| Overlap@5 (vs Ideal) | 1.000 | 0.467 | Firecrawl 🏆 |
| KB Outperforms FC | - | - | 33.3% of TCs |

## Improvement Roadmap

### Root Causes (ranked by severity)
| # | Dimension | Issue | Severity | Confidence | Affected TCs | Frequency |
|---|-----------|-------|----------|------------|--------------|-----------|
| 1 | ranking | Authority-relevance inversion: snippet keyword match over-weighted vs. domain authority and content completeness | high | high | tc_95709ac0, tc_44c68246 | 2/3 TCs |
| 2 | _baseline_fidelity | Boilerplate/navigation noise dominance inflates document length and degrades scrape fidelity | high | high | tc_f6176000, tc_95709ac0 | 2/3 TCs |
| 3 | _baseline_fidelity | Scrape fidelity scorer inverts quality: short-but-complete pages penalized, long-but-truncated pages rewarded | high | medium | tc_95709ac0 | 1/3 TCs (but 2/5 pages within that TC) |
| 4 | coverage_completeness | Content truncation on key tutorial pages fragments end-to-end coverage | medium | high | tc_95709ac0, tc_f6176000, tc_44c68246 | 3/3 TCs |
| 5 | temporal_accuracy | Missing publication-date extraction and stale-cache serving for real-time queries | medium | medium | tc_f6176000 | 1/3 TCs |

### Proposals (ranked by priority)
| # | Targets | Proposal | Expected Impact | Effort | Priority |
|---|---------|----------|-----------------|--------|----------|
| 1 | rc_001 | Add authority-weighted composite reranking with hard contrastive constraint | +0.20 on _baseline_ranking (tc_95709ac0: Istio promoted to rank 1-2; tc_44c68246: Serious Eats promoted to rank 1-2), +0.05 overall | medium | 4.5 |
| 2 | rc_002 | DOM-based boilerplate removal with link-density thresholding before markdown serialization | +0.15 on _baseline_fidelity (japan.travel nav_link_ratio 0.85→<0.3, jp.usembassy.gov template placeholders resolved), +0.04 overall | medium | 3.0 |
| 3 | rc_003 | Fix scrape fidelity scorer to reward completeness over raw length | +0.15 on _baseline_fidelity for tc_95709ac0 (Istio 0.20→0.75, SO 0.20→0.60), +0.03 overall | low | 3.0 |
| 4 | rc_004 | Implement pagination-aware content extraction and template-placeholder detection | +0.10 on coverage_completeness (Buoyant installation step recovered, jp.usembassy.gov placeholders resolved), +0.03 overall | medium | 2.0 |
| 5 | rc_005 | Add publication-date extraction and cache-freshness enforcement for real-time intent queries | +0.15 on temporal_accuracy (tc_f6176000: 0.50→0.65), +0.10 on coverage_completeness (tax-free shopping pages surfaced), +0.04 overall | medium | 1.33 |

### Quick Wins
| # | Action | Description | Expected Impact |
|---|--------|-------------|-----------------|
| 1 | Strip cookie consent and language selector HTML before scoring | Add a regex/DOM filter removing elements matching common cookie-banner and language-selector patterns (e.g., 'Cookie Settings', 'Select Language', cookie consent divs) before markdown serialization — directly fixes the AWS docs and japan.travel boilerplate leakage with minimal engineering effort. | +0.08 on _baseline_fidelity |
| 2 | Cap scrape_score at 0.5 for pages with unresolved template placeholders | Add a simple regex check for '{variable_name}' patterns in scraped content; if found, cap scrape_score at 0.5 and flag for re-scrape — fixes jp.usembassy.gov fidelity score in tc_f6176000. | +0.05 on _baseline_fidelity |
| 3 | Demote zero-content pages (content_length=0) in ranking | Reddit (rank 2) and Facebook (rank 4) in tc_44c68246 both have content_length=0 and has_content=false — add a hard rank penalty (drop to bottom or filter) for pages where scraping returned no content, preventing empty pages from outranking complete editorial sources. | +0.10 on _baseline_ranking for tc_44c68246 |
| 4 | Add minimum scrape_score floor of 0.6 for content_completeness='complete' pages | One-line change in the fidelity scorer: if content_completeness='complete', set scrape_score = max(scrape_score, 0.6). This immediately fixes the Istio (0.20→0.60) and Stack Overflow (0.20→0.60) inversion in tc_95709ac0. | +0.10 on _baseline_fidelity for tc_95709ac0 |

### Cross-Dimension Failure Patterns
| Pattern | Hypothesis / Context |
|---------|----------------------|
| Boilerplate noise degrades both _baseline_fidelity and coverage_completeness simultaneously | When navigation/cookie-banner HTML dominates the scraped content (nav_link_ratio > 0.5), the fidelity scorer penalizes the page AND the substantive content is effectively buried, causing coverage_completeness to drop because key subtopics are lost in noise. This is observed in tc_f6176000 (japan.travel: nav_link_ratio=0.85 → both fidelity and coverage fail) and tc_95709ac0 (AWS docs: cookie banner leaks → fidelity degraded, coverage fragmented). |
| Authority-relevance ranking inversion co-occurs with scrape fidelity inversion on the same TC | In tc_95709ac0, the ranking algorithm places low-authority commercial blogs above official docs (ranking failure), AND the scrape scorer gives L1 scores to the clean official docs while rewarding the truncated commercial tutorial (fidelity failure). Both stem from the same root issue: the system over-weights surface-level signals (keyword match in snippets, raw content length) over deeper quality signals (domain authority, content completeness, code-block presence). |
| Real-time intent queries fail temporal_accuracy AND coverage_completeness but NOT _baseline_ranking | tc_f6176000 (real_time intent) has ranking=0.75 (L4, passing) but temporal_accuracy=0.50 and coverage_completeness=0.55 (both failing). The ranker correctly identifies authoritative travel sources but doesn't enforce freshness or subtopic completeness. This suggests the ranking signal is authority-aware but time-blind — the recency/temporal signal is either absent or too weak for real-time intent classification. |
| Zero-content pages (scrape failures) are not demoted in ranking, creating a ranking-fidelity compound failure | In tc_44c68246, Reddit (rank 2, content_length=0) and Facebook (rank 4, content_length=0) are scraped as empty but retain their ranking positions. The ranking algorithm doesn't consume scrape-quality feedback — if a page returns zero content, it should be demoted or filtered, but instead the empty page occupies a top position, simultaneously failing _baseline_ranking (low-authority page in top position) and _baseline_fidelity (no content to score). |

### Judge Bias Warnings
- ⚠️ Potential judge inconsistency in technical_accuracy aggregation: the summary reports avg_technical_accuracy=0.95 (from tc_95709ac0 only), but the intent_breakdown for tutorial_howto (which includes both tc_95709ac0 and tc_44c68246) reports avg_technical_accuracy=0.475. Since tc_44c68246 has no technical_accuracy dimension in its per-TC breakdown, the 0.475 average cannot be derived from the available scores — this suggests either the judge is silently assigning a default/zero technical_accuracy to TCs where the dimension is not explicitly evaluated, or the aggregation pipeline has a bug. This should be investigated before trusting technical_accuracy trends.

## RL Training Signals
| Signal Type | Count | Output File |
|-------------|-------|-------------|
| DPO Pairs | 3 | dpo_pairs.jsonl |
| Reward Signals | 15 | rewards.jsonl |
| Listwise Rankings | 3 | listwise_rankings.jsonl |
| Contrastive Fail Pairs | 7 | contrastive_fail_pairs.jsonl |
| Query Reformulations | 2 | query_reformulations.jsonl |
| SFT Gold Examples | 1 | sft_gold.jsonl |
| Scrape Quality Labels | 15 | scrape_quality_labels.jsonl |

### Improvement Taxonomy (Micro-Patterns)
| Issue | Severity | Frequency | Description |
|-------|----------|-----------|-------------|
| authority_inversion_in_ranking |  | 67% (2/3 TCs) | Low-authority pages (commercial blogs, forum threads, social media) with keyword-matching snippets consistently outrank high-authority official documentation and editorial sources. The ranker over-weights snippet relevance and under-weights domain authority and content completeness (word count, code block presence). |
| boilerplate_noise_dominance |  | 67% (2/3 TCs) | Navigation menus, cookie consent banners, language selectors, and social-media icon clusters dominate scraped content, inflating document length with non-substantive HTML and degrading fidelity scores. nav_link_ratio reaches 0.85 on affected pages. |
| scrape_fidelity_length_bias |  | 40% of scraped pages (2/5 in tc_95709ac0) | The scrape fidelity scorer rewards raw content length over completeness — short-but-complete pages (Istio: 8026 chars, 10 code blocks) receive L1 scores (0.20) while long-but-truncated pages (Buoyant: 33616 chars, installation step missing) receive higher scores (0.60). |
| zero_content_ranking_retention |  | 33% (1/3 TCs, 2/5 pages) | Pages where scraping returns zero content (content_length=0, has_content=false) retain their ranking positions — Reddit at rank 2 and Facebook at rank 4 in tc_44c68246. The ranker does not consume scrape-quality feedback to demote or filter empty pages. |
| temporal_blindness_for_realtime_intent |  | 100% of real_time intent TCs (1/1) | Real-time intent queries receive stale cached pages (3/5 pages from stale cache in tc_f6176000) and pages without extractable publication dates. The ranking signal is authority-aware but time-blind — no recency decay or date-extraction pipeline exists. |

## Regression vs Previous Run
- Trend: No previous evaluation scores

## Appendix: Failed Test Cases Detail
*(Showing only test cases that failed the pass threshold or hit a dimension floor)*

### tc_95709ac0 (Score: 0.70) ❌
**Query**: `how to configure mutual TLS authentication between microservices in Kubernetes`
**Category**: Cybersecurity | **Intent**: novel

**Root Cause**: The ranking algorithm placed a low-authority commercial blog (appviewx.com, authority_score=0.4, query_relevance_score=0.4) at rank 2, above official AWS documentation (rank 3, authority_score=0.95) and the most relevant Istio documentation (rank 4, authority_score=1.0, query_relevance_score=1.0), triggering a contrastive ranking failure. Additionally, the scrape_score is inverted for clean pages — Istio (scrape_score=0.2) and Stack Overflow (scrape_score=0.2) both have complete, faithful content but receive L1 scores, while the Buoyant tutorial (scrape_score=0.6) suffers critical truncation of its installation step, fragmenting end-to-end coverage.

- **Coverage Diagnosis**: No single document provides a complete end-to-end tutorial for microservice-to-microservice mTLS in Kubernetes: AWS covers only ingress-level mTLS, Istio assumes a pre-existing CA, and the Buoyant/Linkerd tutorial is incomplete due to a truncated CLI installation step (content_gap severity='critical').
- **Ranking Diagnosis**: Istio official docs (authority=1.0, relevance=1.0) buried at rank 4 while AppViewX blog (authority=0.4, relevance=0.4) occupies rank 2 — a direct authority/relevance inversion affecting positions 2-4.
- **Scrape Diagnosis**: Three distinct scrape issues: (1) Buoyant tutorial truncated — 'Tutorial Step 1 (installation script for Buoyant Enterprise for Linkerd CLI) is missing' at scrape_score=0.6; (2) AppViewX boilerplate-dominated with nav_link_ratio=0.95 and 12 boilerplate patterns at scrape_score=0.6; (3) scrape_score inverted for clean pages — Istio and Stack Overflow both scored 0.2 (L1) despite scrape_reasoning confirming faithful, complete content with zero issues.

**Fix Actions**:
- Adjust the ranking scoring weights to multiply authority_score and query_relevance_score so that official documentation (authority >= 0.9) with high relevance (>= 0.85) always outranks commercial blogs (authority <= 0.5) with low relevance (<= 0.5), preventing the appviewx.com > docs.aws.amazon.com > istio.io ordering failure.
- Fix the scrape_score calculation logic: pages with zero scrape_issues and scrape_reasoning confirming faithful reproduction (e.g., istio.io with 'faithfully reproduces the original page content including all code blocks, headings, lists, and links') should receive a high score (>= 0.9), not 0.2; the current formula appears to invert the quality signal for low-boilerplate pages.
- Add a content-extraction rule for buoyant.io that captures dynamically-loaded CLI installation code blocks (the missing 'Tutorial Step 1' installation script), and add a boilerplate-stripping pass for appviewx.com pages with nav_link_ratio > 0.8 to remove sidebar/promotional elements before scoring.


---
### tc_f6176000 (Score: 0.66) ❌
**Query**: `what do US passport holders need to enter Japan right now - visa rules, passport validity, and border procedures`
**Category**: Travel & Geography | **Intent**: rephrased_same_intent

**Root Cause**: Three of five scraped pages received scrape_score=0.20 (travel.state.gov, us.emb-japan.go.jp, klook.com), and Document 2 (jp.usembassy.gov) contains unresolved template placeholders '{title}, {vendor_count}' with content_completeness='appears_truncated', while Document 3 (japan.travel) has nav_link_ratio=0.85. This systemic scrape quality failure, combined with missing publication dates on Documents 2 and 3 and no coverage of tax-free shopping thresholds across the entire set, drove the overall score to 0.664.

- **Coverage Diagnosis**: No document in the result set addresses updated tax-free shopping thresholds, which is explicitly required by the coverage_completeness criteria. Additionally, Document 3 (japan.travel) has three critical content gaps: no US-specific visa information, no passport validity requirements, and no border procedures details, yet it ranks above the most relevant page.
- **Ranking Diagnosis**: Rank 3 (japan.travel, query_relevance_score=0.6) outranks Rank 4 (us.emb-japan.go.jp, query_relevance_score=0.98), placing the most relevant authoritative document below a less relevant tourism page.
- **Scrape Diagnosis**: Document 1 (travel.state.gov) scored 0.20 due to a broken virtual assistant widget; Document 4 (us.emb-japan.go.jp) scored 0.20 with an empty issues list (anomalous — likely a scoring bug or unreported extraction failure); Document 5 (klook.com) scored 0.20 due to base64 image placeholder removal; Document 2 has unresolved JS template placeholders and appears_truncated; Document 3 has nav_link_ratio=0.85 with boilerplate_pattern_count=5.

**Fix Actions**:
- Add a post-scrape boilerplate stripping pass that removes navigation menus, cookie consent blocks, language selectors, and promotional banners before computing scrape_score, targeting pages like japan.travel (nav_link_ratio=0.85) and jp.usembassy.gov (nav_link_ratio=0.6).
- Implement a template placeholder detection regex filter that identifies and removes unresolved JavaScript placeholders (e.g., {title}, {vendor_count}) from scraped markdown before content_completeness evaluation.
- Add a relevance-weighted reranking step in the ranking pipeline that penalizes pages with query_relevance_score below 0.7 when higher-relevance alternatives exist, preventing japan.travel (0.6) from outranking us.emb-japan.go.jp (0.98).


---
