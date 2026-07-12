# Firecrawl Eval Report: run_20260712_175653
Generated: 2026-07-12 18:05:18

## Run Configuration
| Setting | Value |
|---|---|
| Generator Model | minimax/minimax-m3 |
| P1 Model (Extraction) | deepseek/deepseek-v4-flash |
| P2 Model (Reasoning)  | deepseek/deepseek-v4-flash |
| Improvement Agent | z-ai/glm-5.2 |
| Pass Threshold | 0.65 (floor: 0.4) |
| Test Cases | 3 |
| Duration | 8m 24s |

## Executive Summary
- **Overall Score**: 0.85 🟢
- **Test Cases**: 3 | Passed: 0 | Failed: 3

### Floor Failures (Dimension Score < 0.40)
- **TCs with floor failures**: 3 / 3
- **Most common floor dimension**: `_baseline_ranking` (2 TCs)

## Dimension Performance Breakdown
| Dimension | Weight (avg) | Avg Score | Pass Rate | Floor Fails | Histogram |
|-----------|-------------|-----------|-----------|-------------|-----------|
| _baseline_ranking | 0.12 | 0.37 | 33.3% | 2 | <pre>  0.0-0.2  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| _baseline_fidelity | 0.12 | 0.53 | 25.0% | 1 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| structural_fidelity | 0.17 | 0.60 | 50.0% | 1 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| temporal_currency | 0.22 | 0.65 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| _baseline_authority | 0.07 | 0.75 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| source_credibility | 0.16 | 0.75 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| _baseline_freshness | 0.07 | 0.80 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| source_authority | 0.28 | 0.85 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| regional_distinction | 0.15 | 0.90 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| practical_trekking_factors | 0.15 | 0.92 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| _baseline_coverage | 0.12 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  3<br></pre> |
| seasonal_specificity | 0.20 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| topical_precision | 0.24 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| policy_specificity | 0.16 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| ai_focus_clarity | 0.10 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |

## Most Frequently Unmet Rubric Criteria
| Condition (truncated) | Times Not Met |
|---|---|
| Higher-authority sources appear before lower-quality ones. | 1 |
| More relevant sources appear before less relevant ones. | 1 |
| URL rank 2: https://www.swoop-patagonia.com/visit/when | 1 |
| URL rank 1: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framewo... | 1 |
| URL rank 3: https://www.snowflake.com/en/artificial-intelligence/ai-governance/e... | 1 |
| URL rank 5: https://www.aoshearman.com/en/insights/ao-shearman-on-tech/zooming-i... | 1 |
| No low-quality sources interleaved before high-quality ones | 1 |
| Content is complete without truncation | 1 |

### Executive Diagnosis
This run achieved a pass rate of **0%** across 3 test cases. The primary bottleneck identified is **Low-authority social media/forum content ranking above high-authority sources**, impacting 2/3 TCs of the evaluated queries. Addressing the key root causes could yield a significant boost in performance, particularly on the **ranking** dimension.

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
| temporal_ambiguity ⚠️ | 1 | 0.77 | 0.0% |
| none ⚠️ | 1 | 0.85 | 0.0% |
| keyword_stuffed ⚠️ | 1 | 0.92 | 0.0% |

## Intent × Difficulty Analysis

### By Intent
| Intent | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| exploratory | 1 | 0.77 | 0.0% |
| factual_lookup | 2 | 0.88 | 0.0% |

### By Difficulty
| Difficulty | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| medium | 2 | 0.81 | 0.0% |
| hard | 1 | 0.92 | 0.0% |

## Retrieval Comparison: Firecrawl vs KB vs Ideal
*(Evaluates if our RRF Hybrid KB outperforms Firecrawl's native ranking)*

| Metric | Firecrawl | Internal KB | Winner |
|--------|-----------|-------------|--------|
| Kendall's τ (vs Ideal, normalized 0→1) | 0.567 | 0.889 | KB 🏆 |
| Overlap@3 (vs Ideal) | 0.556 | 0.444 | Firecrawl 🏆 |
| Overlap@5 (vs Ideal) | 1.000 | 0.467 | Firecrawl 🏆 |
| KB Outperforms FC | - | - | 66.7% of TCs |

## Improvement Roadmap

### Root Causes (ranked by severity)
| # | Dimension | Issue | Severity | Confidence | Affected TCs | Frequency |
|---|-----------|-------|----------|------------|--------------|-----------|
| 1 | ranking | Low-authority social media/forum content ranking above high-authority sources | high | high | tc_8713c71c, tc_1beb2c2f | 2/3 TCs |
| 2 | fidelity | Scrape pipeline returns empty or severely truncated content for social media and video-heavy pages | high | high | tc_8713c71c, tc_1beb2c2f, tc_0d25db52 | 3/3 TCs |
| 3 | structural_fidelity | Scrape scoring assigns L1 floor (0.20) to pages with only cosmetic issues or no reported issues | high | high | tc_0d25db52 | 1/3 TCs |
| 4 | fidelity | Boilerplate and navigation noise leaking into scraped markdown content | medium | high | tc_8713c71c, tc_1beb2c2f, tc_0d25db52 | 3/3 TCs |
| 5 | freshness | Recency signal insufficient for queries with explicit future-date temporal anchors | medium | medium | tc_0d25db52, tc_1beb2c2f | 2/3 TCs |

### Proposals (ranked by priority)
| # | Targets | Proposal | Expected Impact | Effort | Priority |
|---|---------|----------|-----------------|--------|----------|
| 1 | rc_001 | Implement authority-relevance ranking floor for top-3 positions | +0.35 on _baseline_ranking dimension (would move tc_8713c71c from 0.1 to ~0.7 and tc_1beb2c2f from 0.3 to ~0.7) | medium | 4.5 |
| 2 | rc_003 | Re-calibrate scrape scoring thresholds to distinguish cosmetic from substantive issues | +0.40 on structural_fidelity for tc_0d25db52 (moving from 0.256 to ~0.65) | low | 4.0 |
| 3 | rc_002 | Add social media and video content extraction adapters | +0.15 on _baseline_fidelity dimension across all TCs | high | 3.0 |
| 4 | rc_004 | Deploy boilerplate detection and content extraction de-noising | +0.10 on _baseline_fidelity across all 3 TCs | medium | 3.0 |
| 5 | rc_005 | Add temporal anchor extraction and recency-decay ranking boost | +0.15 on temporal_currency and +0.10 on _baseline_freshness | medium | 2.0 |

### Quick Wins
| # | Action | Description | Expected Impact |
|---|--------|-------------|-----------------|
| 1 | Fix silent L1 scoring bug for no-issue pages | Debug and patch the scrape scoring logic that assigned scrape_score=0.20 to aoshearman.com despite an empty issues list. This is likely a default/fallback value being applied when the scoring function receives an unexpected input state. Add a guard clause: if issues list is empty and content_length > 1000, minimum score should be 0.80. | +0.40 on structural_fidelity for tc_0d25db52, +0.05 overall |
| 2 | Exclude empty-content URLs from top-3 ranking positions | Add a post-retrieval filter: any URL where scrape has_content=false or content_length < 50 should be automatically demoted to position 4 or below, regardless of its retrieval score. This immediately fixes the Reddit rank-1 and Facebook rank-3 inversions without requiring full social media extraction adapters. | +0.30 on _baseline_ranking for tc_8713c71c and tc_1beb2c2f |
| 3 | Strip cookie consent and navigation boilerplate from snippet previews | Apply a regex-based pre-processing step to remove common boilerplate patterns ('Skip to content', cookie consent text, Trustpilot widgets, GDPR banners) from the first 500 characters of scraped markdown. This is a 1-2 hour fix that improves fidelity scores across all TCs. | +0.05 on _baseline_fidelity across all TCs |

### Cross-Dimension Failure Patterns
| Pattern | Hypothesis / Context |
|---------|----------------------|
| Empty-content social media pages fail both scrape fidelity and ranking simultaneously | When the scrape pipeline returns has_content=false (Reddit, Facebook), the empty content is still passed to the ranking model. The ranking model, lacking content signals, falls back to URL-level features (domain popularity, link signals) which over-weight social media domains. This creates a cascading failure: poor scrape → degraded content signals → ranking model relies on domain popularity → social media intrudes into top positions → ranking dimension fails AND fidelity dimension fails. The fix should be at the scrape-ranking interface: empty-content pages should be either excluded or heavily penalized before ranking. |
| Boilerplate leakage degrades both _baseline_fidelity and structural_fidelity | Pages with high nav_link_ratio (asccc.org at 0.4) or cookie-consent-heavy headers (Wilderness Travel, Snowflake) lose structural fidelity because the extracted markdown is dominated by non-content elements. This same boilerplate also dilutes the content-to-noise ratio measured by _baseline_fidelity. The root cause is shared: the extraction pipeline lacks a main-content detection step (readability-style) that isolates the primary article body from chrome/navigation. Fixing content extraction would improve both dimensions simultaneously. |
| Temporal currency and ranking interact: stale high-authority sources outrank fresh high-authority sources | In tc_0d25db52, A&O Shearman (auth=0.9, rel=0.98, 2026 content) was ranked at position 5 while Snowflake (auth=0.6, rel=0.85, 2024 content) was at position 3. The ranking model appears to weight topical relevance and authority but not publication date, even when the query explicitly references a future year. This suggests the freshness signal is either absent or too weak in the ranking function, causing temporal_currency and _baseline_ranking to co-fail on time-sensitive queries. |

### Judge Bias Warnings
- ⚠️ Duplicate dimension scoring inconsistency: tc_0d25db52 has structural_fidelity scored at both 0.95 (L5) and 0.256 (L2), and tc_1beb2c2f has _baseline_fidelity scored at both 0.55 (L3) and 0.3946 (L2). The same dimension receiving two different scores for the same test case suggests the judge may be applying two different rubrics or there is a scoring aggregation bug. The lower score appears to be scrape-based while the higher appears to be content-based — the judge should reconcile these into a single coherent score per dimension.
- ⚠️ _baseline_coverage consistently scores 0.95 (L5) across all 3 TCs despite critical ranking failures and content extraction failures. While coverage (URL presence in result set) and ranking (URL ordering) are conceptually distinct, scoring coverage at L5 when the most relevant URLs are buried behind empty-content social media posts may overstate system performance. The coverage dimension may need to weight position-dependent coverage (e.g., coverage in top-3 vs. top-10) rather than binary presence.

## RL Training Signals
| Signal Type | Count | Output File |
|-------------|-------|-------------|
| DPO Pairs | 1 | dpo_pairs.jsonl |
| Reward Signals | 15 | rewards.jsonl |
| Listwise Rankings | 3 | listwise_rankings.jsonl |
| Contrastive Fail Pairs | 1 | contrastive_fail_pairs.jsonl |
| Query Reformulations | 3 | query_reformulations.jsonl |
| SFT Gold Examples | 0 | sft_gold.jsonl |
| Scrape Quality Labels | 15 | scrape_quality_labels.jsonl |

### Improvement Taxonomy (Micro-Patterns)
| Issue | Severity | Frequency | Description |
|-------|----------|-----------|-------------|
| social_media_ranking_intrusion |  | 67% (2/3 TCs) | Low-authority social media/forum posts (Reddit, Facebook) with authority_score < 0.3 and content_length = 0 consistently rank in top-3 positions above high-authority academic and guide sources. This occurs across both factual_lookup and exploratory intents, and across Travel and Education categories. |
| scrape_score_floor_anomaly |  | 33% (1/3 TCs) but 60% of scraped pages in that TC | The scrape scoring function assigns L1 floor (0.20) to pages with substantial extracted content (content_length > 20,000) when only cosmetic issues are present, and even to pages with no reported issues at all. This systematically underestimates scrape quality and triggers false contrastive failures on structural_fidelity. |
| boilerplate_contamination |  | 100% (3/3 TCs) | All 3 TCs show scraped markdown beginning with cookie consent banners, navigation links, 'Skip to content' accessibility text, or promotional widgets rather than article content. This degrades both fidelity and structural dimensions and inflates nav_link_ratio. |
| temporal_anchor_mismatch |  | 67% (2/3 TCs) | Queries containing explicit temporal references ('2026', 'current') retrieve documents that are 2+ years stale or undated, and the ranking model does not penalize this mismatch. Fresh, highly-relevant sources are buried behind stale, lower-relevance sources. |
| empty_content_ranking |  | 67% (2/3 TCs) | URLs where the scrape pipeline returned has_content=false and content_length=0 were still included in ranking and placed in top-3 positions. The ranking model has no mechanism to detect and penalize empty-content candidates. |

## Regression vs Previous Run
- Trend: Significant Improvement 🚀
- Difference: +0.09

## Appendix: Failed Test Cases Detail
*(Showing only test cases that failed the pass threshold or hit a dimension floor)*

### tc_8713c71c (Score: 0.85) ❌
**Query**: `best time of year to visit Patagonia for trekking`
**Category**: Travel & Geography | **Intent**: novel

**Root Cause**: The primary failure is a critical ranking inversion: Reddit (authority_score=0.2, query_relevance_score=0.6, 28 words, tangential coverage) is placed at Rank 1 while Swoop Patagonia (authority_score=0.7, query_relevance_score=0.95, 3616 words, full coverage) is at Rank 2 and Aurora Expeditions (authority_score=0.7, query_relevance_score=0.95) at Rank 4. A secondary contributor is low aggregate fidelity (0.438) driven by Swoop's scrape_score=0.20 (video content not captured) and boilerplate leakage on Extraordinary Journeys (scrape_score=0.40).

- **Coverage Diagnosis**: No observable coverage gap — the document profiles collectively provide full coverage of seasonal timing, regional distinctions, and practical trekking factors. The Reddit post at Rank 1 contributes only tangential coverage (28 words) and does not fill any information gap.
- **Ranking Diagnosis**: Rank 1 (Reddit, relevance 0.6, authority 0.2) should be demoted below all four commercial guides (relevance 0.9–0.95, authority 0.65–0.7). The ideal order would place Swoop or Aurora at Rank 1, followed by Wilderness Travel, then Extraordinary Journeys, with Reddit at Rank 5 or excluded.
- **Scrape Diagnosis**: Swoop Patagonia (scrape_score=0.20) lost video content and image alt text despite having 3616 words of complete textual content; Extraordinary Journeys (scrape_score=0.40) has boilerplate leakage (share buttons, recaptcha, Prismatic toolbar, duplicate author box); Wilderness Travel (scrape_score=0.40) has table icons not transcribed as text.

**Fix Actions**:
- Adjust the ranking scoring function to apply a stronger penalty multiplier for page_type=forum_thread when authority_score < 0.4 and query_relevance_score < 0.7, ensuring such results cannot outrank page_type=blog_post or page_type=other results with authority_score >= 0.6 and query_relevance_score >= 0.9.
- Add a boilerplate-stripping post-processing step to the scraper that removes share-button containers, recaptcha iframes, Prismatic toolbar elements, and duplicate author bio boxes before computing scrape_score.
- Enhance the scraper's video-content handler to extract a text transcript or descriptive placeholder block for embedded video elements, preventing scrape_score from dropping to 0.20 when textual content is otherwise complete.


---
### tc_0d25db52 (Score: 0.92) ❌
**Query**: `EU AI Act compliance requirements high-risk systems provider deployer obligations prohibited practices transparency 2026`
**Category**: Legal & Regulatory | **Intent**: novel

**Root Cause**: The scrape pipeline produced uniformly poor markdown extractions across all five retrieved documents, with Rank 1 (digital-strategy.ec.europa.eu) at scrape_score=0.20, Rank 3 (snowflake.com) at scrape_score=0.20, and Rank 5 (aoshearman.com) at scrape_score=0.20 despite having no identified issues, yielding an average of 0.28 that triggered the contrastive fail on the scrape-based structural_fidelity dimension (score=0.256, L2). Secondary failures include ranking misordering where A&O Shearman (auth=0.9, rel=0.98) was placed at rank 5 below lower-authority vendor blogs, and freshness gaps where 4 of 5 documents are from 2024 or undated.

- **Coverage Diagnosis**: No observable coverage gap — all six query aspects are covered by at least one authoritative source, with _baseline_coverage scoring 0.95 (L5).
- **Ranking Diagnosis**: A&O Shearman (rank 5, authority_score=0.9, query_relevance_score=0.98) is unjustifiably placed below Snowflake (rank 3, authority_score=0.7, query_relevance_score=0.95) and Hyperproof (rank 4, authority_score=0.6, query_relevance_score=0.95), indicating the ranking algorithm under-weights authority and relevance in favor of other signals for commercial/vendor domains.
- **Scrape Diagnosis**: Three of five documents received scrape_score=0.20 (L1): Rank 1 (EC page) lost image embedding and retained boilerplate navigation; Rank 3 (Snowflake) lost YouTube thumbnails and had incomplete author bio link rendering; Rank 5 (A&O Shearman) scored 0.20 with an empty issues list, suggesting either a default-floor scoring bug or an unreported extraction deficiency. Rank 2 (artificialintelligenceact.eu) at 0.40 suffered from duplicated cookie consent boilerplate, unresolved {title} placeholders in navigation links, and UI elements (buttons, toggles) leaking into text.

**Fix Actions**:
- Add a cookie-consent and modal-UI stripping pass to the scrape pipeline that removes cookie banners, preference toggles, and form-field boilerplate before markdown conversion, targeting the issues seen on artificialintelligenceact.eu (scrape_score=0.40) and hyperproof.io (scrape_score=0.40).
- Investigate and fix the scrape scoring logic for pages like aoshearman.com (scrape_score=0.20, issues=[]) where no issues are detected yet the score remains at the L1 floor — either the score floor is too aggressive or an unreported extraction problem (e.g., JavaScript-rendered content not captured) needs to be addressed.
- Adjust the ranking re-ranker to apply an authority-weighted tiebreaker so that sources with authority_score >= 0.9 and query_relevance_score >= 0.98 (e.g., A&O Shearman) are promoted above sources with authority_score <= 0.7 and query_relevance_score <= 0.95 (e.g., Snowflake, Hyperproof).


---
### tc_1beb2c2f (Score: 0.77) ❌
**Query**: `current university policies and honor code updates addressing generative AI use in higher education`
**Category**: Education & Academia | **Intent**: rephrased_same_intent

**Root Cause**: The primary failure is a ranking inversion: a truncated Facebook post (facebook.com, authority_score 0.2, query_relevance_score 0.5, word_count 21) was placed at rank 3, above frontiersin.org (authority 0.8, relevance 0.95) at rank 4 and pressbooks.sunycreate.cloud (authority 0.7, relevance 0.8) at rank 5, triggering contrastive failure in _baseline_ranking (score 0.3). This was compounded by poor aggregate scrape fidelity (0.3946, L2) driven by navigation noise on asccc.org (scrape_score 0.6, nav_link_ratio 0.4), table formatting loss on sciencedirect.com (scrape_score 0.4), and severe truncation on the Facebook post (21 words captured).

- **Coverage Diagnosis**: No observable coverage gap — _baseline_coverage scored 0.95 (L5) with documents 1, 2, 4, and 5 collectively covering specific institutional policies, honor code updates, detection tools, and policy frameworks. The Facebook post at rank 3 is irrelevant but does not create a critical information gap.
- **Ranking Diagnosis**: Rank 3 (facebook.com, authority 0.2, relevance 0.5) is positioned above Rank 4 (frontiersin.org, authority 0.8, relevance 0.95) and Rank 5 (pressbooks.sunycreate.cloud, authority 0.7, relevance 0.8), violating both authority and relevance ordering. The contrastive fail was triggered because a social media post (analogous to a blog) ranks above official/academic sources.
- **Scrape Diagnosis**: Four of five documents have significant scrape issues: asccc.org (scrape_score 0.6, ~40% navigation/boilerplate), sciencedirect.com (scrape_score 0.4, table formatting lost, images not extracted), facebook.com (severely truncated, 21 words), frontiersin.org (scrape_score 0.4, boilerplate and navigation links). Only pressbooks.sunycreate.cloud has clean fidelity (scrape_score 0.2, no issues). Aggregate fidelity is 0.3946 (L2).

**Fix Actions**:
- Add a domain-authority-based reranking filter that demotes social media domains (facebook.com, twitter.com, linkedin.com) below academic/organization domains when the authority_score differential exceeds 0.3, preventing low-authority forum_thread page_types from appearing in top-3 positions for exploratory academic queries.
- Implement a content-completeness gate in the scrape pipeline that flags documents with word_count < 100 as 'appears_truncated' and excludes them from ranking consideration or re-queues them for re-scrape with JavaScript rendering enabled (critical for Facebook posts which require JS to render body content).
- Add a boilerplate-stripping post-processing step that removes navigation menus, share/citation toolbars, and action links from scraped markdown before scoring, targeting the specific patterns seen on asccc.org (nav_link_ratio 0.4) and frontiersin.org (citation tools, 'View details' links).


---
