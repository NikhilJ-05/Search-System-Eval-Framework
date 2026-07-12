# Eval Findings: 30 TC Run — `run_20260712_180951`

> **Deep analysis of the EvalOS Framework's first run under the new P1/P2 multi-agent, rubric-first architecture.** This document covers scoring outcomes, root causes, per-TC failure breakdowns, cache behavior, chaos archetype analysis, retrieval comparison, RL signal statistics, and a prioritized improvement roadmap with quick wins.

---

![EvalOS Live Pipeline — SSE event stream with live leaderboard](./screenshots_new/live_pipeline_streaming.png)

---

## Table of Contents

1. [Run Metadata](#run-metadata)
2. [Architecture Context](#architecture-context)
3. [Executive Summary](#executive-summary)
4. [Score Distribution Analysis](#score-distribution-analysis)
5. [Dimension Performance Breakdown](#dimension-performance-breakdown)
   - [The Critical Bottleneck — `_baseline_fidelity`](#the-critical-bottleneck--_baseline_fidelity)
   - [Ranking — `_baseline_ranking`](#ranking--_baseline_ranking)
   - [Custom Rubric Dimensions](#custom-rubric-dimensions)
6. [Chaos Archetype Analysis](#chaos-archetype-analysis)
7. [Intent × Difficulty Analysis](#intent--difficulty-analysis)
8. [Two-Layer Cache Analysis](#two-layer-cache-analysis)
9. [KB Build Progression](#kb-build-progression)
10. [Retrieval Comparison: Firecrawl vs Internal KB vs Ideal](#retrieval-comparison-firecrawl-vs-internal-kb-vs-ideal)
11. [Root Cause Analysis](#root-cause-analysis)
12. [Per-TC Failure Catalog](#per-tc-failure-catalog)
13. [Cross-Dimension Failure Patterns](#cross-dimension-failure-patterns)
14. [RL Signal Statistics](#rl-signal-statistics)
15. [Improvement Roadmap](#improvement-roadmap)
    - [Engineering Proposals](#engineering-proposals)
    - [Quick Wins](#quick-wins)
16. [Judge Bias Warnings](#judge-bias-warnings)
17. [Regression vs Previous Run](#regression-vs-previous-run)
18. [Conclusions & Next Steps](#conclusions--next-steps)

---

## Run Metadata

| Field | Value |
|-------|-------|
| **Run ID** | `run_20260712_180951` |
| **Started** | 2026-07-12 at 18:09:51 IST |
| **Completed** | 2026-07-12 at 19:22:12 IST |
| **Duration** | 72 minutes 21 seconds |
| **Total Test Cases** | 30 |
| **Generator Model (LLM-A)** | `minimax/minimax-m3` |
| **P1 Model (Document Profiler)** | `deepseek/deepseek-v4-flash` |
| **P2 Model (Dimension Scorer)** | `deepseek/deepseek-v4-flash` |
| **Improvement Agent (LLM-C)** | `z-ai/glm-5.2` |
| **Pass Threshold** | `0.65` (floor: `0.40`) |
| **Qdrant Collection** | `firecrawl_eval` |
| **Run Output** | `outputs/runs/run_20260712_180951/` |

![Run configuration panel — model selections, thresholds, and TC count](./screenshots_new/live_pipeline_config.png)

---

## Architecture Context

This run is the **first full run under the new P1/P2 multi-agent, rubric-first architecture**. Key differences from the previous run (`run_20260701_152627`):

| Component | Previous Run | This Run |
|-----------|-------------|----------|
| Judge | Single 3-pass LLM (Coverage, Ranking, Scrape) | P1 per-document profilers × N + P2 dimension scorers × 5 families |
| Rubric | Hardcoded 3-axis (Coverage 25%, Ranking 35%, Scrape 40%) | Dynamic per-TC rubric authored by test generator (2–4 custom dimensions) |
| Pass Gate | Overall ≥ 0.80 | Overall ≥ 0.65 AND no dimension < 0.40 (floor gate) |
| Domains | 13 | 16 (added Cybersecurity, Pharmaceuticals, Real Estate) |
| Chaos Archetypes | None | 7 (temporal_ambiguity, multi_hop_compressed, etc.) |
| RL Signals | 3 types (DPO, Rewards, Taxonomy) | 7 types (+ Listwise, Contrastive Fail, Query Reformulations, SFT Gold, Scrape Labels) |
| Cache Variants | None | 35% of TCs are cache relationship variants |
| Generator | `deepseek/deepseek-v4-flash` | `minimax/minimax-m3` |

---

## Executive Summary

```
Overall Score:  0.69  🟡  (0% pass rate — 0/30 TCs passed)

Baseline Dimension Scores (across all TCs, where applied):
  _baseline_fidelity   0.40  ❌  ─────────── 40% — CRITICAL BOTTLENECK
  _baseline_ranking    0.48  🟡  ──────────────── 48%
  _baseline_coverage   0.69  ✅  ─────────────────────────── 69%
  _baseline_authority  0.73  ✅  ──────────────────────────────── 73%
  _baseline_freshness  0.81  ✅  ──────────────────────────────────────── 81%

  Floor fails: 30/30 TCs triggered ≥1 dimension floor (< 0.40)
  Most common floor dimension: _baseline_fidelity (34 evaluations)
```

**The story this run tells in one sentence:**
> The new rubric-first, P1/P2 architecture is correctly diagnosing Firecrawl's scrape-quality failures with granular precision, but the P1 agent's scrape scoring function is systematically **inverting quality** — complete documents with faithful content receive 0.20 (L1) while truncated social media posts receive 0.79 (L4) — causing the floor gate to fire on every single test case and producing a 0% pass rate that does not reflect the actual retrieval quality of the system.

The 0% pass rate has two distinct causes:

1. **A real problem:** Social media content (Facebook, Reddit, Instagram) is consistently ranked above authoritative sources, and large multi-hop queries fail to retrieve all required data hops.
2. **A calibration defect:** The P1 agent's `scrape_score` computation is inverted for roughly 10/30 TCs — pages explicitly described as "faithfully preserving all content" score L1 (0.20) while truncated 17–25 word posts score L4 (0.79). This cascades directly into `_baseline_fidelity` floor failures.

Correcting the calibration defect alone (Quick Win #1) would likely push 10–15 TCs above the pass threshold.

---

## Score Distribution Analysis

### Overall Score Distribution (30 TCs)

```
Score Range   Count   Bar
─────────────────────────────────────────────────
0.90 – 1.00   3  TCs  █████
0.80 – 0.89   4  TCs  ███████
0.70 – 0.79   8  TCs  ████████████
0.60 – 0.69  10  TCs  ████████████████
0.50 – 0.59   4  TCs  ███████
0.30 – 0.49   1  TCs  ██
─────────────────────────────────────────────────
```

Despite the 0% pass rate, scores are broadly distributed. 7 TCs scored ≥ 0.80 but all were blocked by dimension floor failures, most commonly the fidelity dimension falling below 0.40 due to the score inversion bug.

### By Intent

| Intent | TCs | Avg Score | Pass Rate |
|--------|-----|-----------|-----------|
| `data_extraction` | 4 | 0.60 | 0.0% |
| `comparative_research` | 8 | 0.60 | 0.0% |
| `tutorial_howto` | 3 | 0.61 | 0.0% |
| `exploratory` | 9 | 0.72 | 0.0% |
| `factual_lookup` | 6 | 0.85 | 0.0% |

`data_extraction` and `comparative_research` are the hardest — both require multi-hop retrieval that the current pipeline doesn't support.

---

## Dimension Performance Breakdown

![Overview Gauge Rings — Dimension scores per run](./screenshots_new/overview_rings.png)

![Rubric Dimensions Tab — dynamic per-TC dimension cards](./screenshots_new/dimensions_tab.png)

The dynamic rubric system produced 50+ unique dimension names across the 30 TCs. The table below shows all dimensions that appeared, sorted by average score ascending (worst first).

### Worst-Performing Custom Dimensions (Avg < 0.40)

| Dimension | Avg Score | Floor Fails | Primary Cause |
|-----------|-----------|-------------|---------------|
| `real_world_vs_theoretical` | 0.15 | 1 | Retrieval returns only theoretical frameworks, no applied case studies |
| `whole_grain_compatibility` | 0.15 | 1 | No documents address whole grain interaction with binders/starches |
| `structural_fidelity` | 0.22 | 2 | Markdown conversion loses tables, headings, and nested lists |
| `data_completeness` | 0.25 | 3 | Multi-hop queries missing 2nd/3rd data hop entirely |
| `multi_hop_synthesis` | 0.28 | 3 | Single-hop retrieval cannot satisfy compound comparative intent |
| `comparative_context_recovery` | 0.28 | 2 | Over-decomposed queries return single-entity results only |
| `actionability` | 0.30 | 1 | Tutorial intent queries retrieve explanatory content, not step-by-step guides |
| `multi_constraint_coverage` | 0.35 | 1 | No single result set satisfies all constraints simultaneously |

### Best-Performing Custom Dimensions (Avg ≥ 0.85)

| Dimension | Avg Score | Pass Rate |
|-----------|-----------|-----------|
| `topical_coverage` | 0.85 | 100% |
| `topical_substance` | 0.85 | 100% |
| `comparative_coverage` | 0.85 | 100% |
| `practical_recommendations` | 0.86 | 100% |
| `topical_coherence` | 0.88 | 100% |
| `destination_specificity` | 0.90 | 100% |
| `completeness` | 0.90 | 100% |
| `practical_examples` | 0.93 | 100% |
| `noise_filtering` | 0.95 | 100% |
| `drift_recovery` | 0.95 | 100% |

Firecrawl excels at topical coverage, source coherence, and fact-level completeness for clean queries. The system reliably finds the right general content; it fails at structured data extraction, scrape fidelity, and authority-ranked ordering.

---

### The Critical Bottleneck — `_baseline_fidelity`

Average score: **0.40** (barely at the floor). Applied to all 30 TCs. 34 evaluations triggered floor failure.

**Root cause: P1 scrape_score inversion.**

The P1 agent computes a `scrape_score` per URL, which `_baseline_fidelity` then aggregates as:

```
fidelity = 0.70 × mean(scrape_scores) + 0.30 × min(scrape_scores)
```

In at least 10 TCs, the P1 agent's `scrape_score` values are systematically inverted relative to actual content quality:

| TC ID | URL | word_count | content_completeness | scrape_score | scrape_reasoning |
|-------|-----|------------|----------------------|--------------|-----------------|
| `tc_531d905d` | Formula 1 Wikipedia | 3,000+ | `complete` | **0.20** | "faithfully reproduces all visible text" |
| `tc_531d905d` | Instagram reel | 26 | `appears_truncated` | **0.79** | "Content is heavily truncated, only opening line visible" |
| `tc_a7f33ea8` | Harvard health | 1,200+ | `complete` | **0.20** | "faithfully captures all textual content" |
| `tc_a7f33ea8` | Facebook post | 25 | `appears_truncated` | **0.79** | "ends mid-sentence" |
| `tc_e4e371ec` | healthdirect.gov.au | 900+ | `complete` | **0.20** | "No critical discrepancies detected" (issues=[]) |
| `tc_9695f75c` | YouTube transcript | 2,004 | `complete` | **0.20** | "Full video transcript...successfully extracted" |
| `tc_d6ace918` | PubMed article | 3,000+ | `complete` | **0.20** | "faithfully preserves the full text" |
| `tc_d6ace918` | Facebook NIH post | 23 | `appears_truncated` | **0.60** | truncated |

The scrape_score computation appears to be applying penalties for cosmetic issues (alt-text gaps, nav links, embedded media) as if they were critical failures, while simultaneously under-penalizing severe truncation and empty content on social media pages.

**Impact of the inversion:** Every TC where this occurs shows an aggregated fidelity score of 0.20–0.35 (L1–L2), triggering the floor gate and failing the TC even when other dimensions score L4–L5.

**Also note:** In several TCs, `_baseline_fidelity` is evaluated **twice** — once by the Fidelity aggregation path and once by a P2 agent that routed a custom dimension matching "fidelity". TC `tc_a345a697` scores 0.9 (L5) on the first evaluation and 0.312 (L2) on the second for the same document set. This is a routing conflict, not judge inconsistency.

---

### Ranking — `_baseline_ranking`

Average score: **0.48** (marginal). Applied to 30 TCs. 15 evaluations triggered floor failure.

Score distribution:
- L1 (0.00–0.20): 2 TCs (13% + 15% = Facebook/Reddit at rank 1)
- L2 (0.20–0.40): 13 TCs — most common band
- L3 (0.40–0.60): 6 TCs
- L4 (0.60–0.80): 5 TCs
- L5 (0.80–1.00): 4 TCs

**Dominant failure: social media content at rank 1.**

In 13 of 30 TCs, the most relevant and authoritative source was buried behind a Facebook post, Reddit thread, or Instagram reel that ranked first. The pattern is consistent across domains:

| TC | Query Topic | Rank 1 (actual) | Auth | words | Ideal Rank 1 |
|----|------------|----------------|------|-------|--------------|
| `tc_3b095b54` | Lisbon travel guide | Instagram reel | 0.1 | 25 | travelforlifenow.com (auth 0.6, 3783w) |
| `tc_c6c18688` | Lisbon cultural history | Facebook post | 0.2 | 23 | debritoproperties.com (auth 0.5) |
| `tc_0c0014af` | Fossil fuel + climate | UN/IEA overview | 0.9 | — | multi-hop source (doesn't exist in results) |
| `tc_39808d09` | Dividend portfolio | Reddit thread | 0.1 | 24 | bogleheads.org (auth 0.85, rel 0.95) |
| `tc_5cad7b97` | Iceland Northern Lights | Reddit comment | 0.2 | 17 | nordicvisitor.com (auth 0.6, rel 0.95) |
| `tc_0aff21d2` | Byzantine Empire fall | Facebook post | 0.2 | 25 | Wikipedia + academic (in result set) |
| `tc_a024035f` | Gluten-free baking | Facebook post | 0.2 | 19 | YouTube (auth 0.6, rel 0.7) |
| `tc_b7028fb4` | Concert production crew | Instagram reel | 0.3 | 23 | YouTube (auth 0.8, rel 0.95) |
| `tc_69806b76` | Ancient Egypt discoveries | Travel blog | 0.4 | — | penn.museum (auth 1.0, rel 0.9) |

The most unambiguous evidence that this is a **Firecrawl ranking problem** (not a retrieval problem): in 8 of these 9 cases, the ideal Rank 1 document **is present in the result set** — it was found by the search, it was scraped, it scored high on P1 relevance — but it appears at Rank 3, 4, or 5 instead of Rank 1.

---

### Custom Rubric Dimensions

The new rubric-first architecture produces TC-specific dimensions that probe exactly the failure mode relevant to each archetype. Below are the most significant findings per dimension family:

**Coverage-family dimensions (avg 0.64–0.90):** Strong for topical and breadth queries. Weak for multi-hop compound queries requiring synthesis across 2+ data sources.

**Freshness-family dimensions (avg 0.55–0.81):** Temporal queries perform well for content freshness detection. Failure occurs when documents have no `publication_date` metadata despite containing explicit date references in body text. P1's temporal extraction works, but `recency_signals` scoring requires structured `publication_date` to trigger correctly.

**Authority-family dimensions (avg 0.73–0.84):** Generally strong. Fails predictably when social media domains appear in top-3 results — their `authority_score` is accurate (0.1–0.3) but the ranking doesn't penalize them.

**Precision-family dimensions (avg 0.25–0.72):** Wide spread. Quantitative queries fail when the specific data isn't in any scraped document (`data_completeness` avg 0.25). Queries for publicly available structured data (F1 calendar, sugar guidelines) succeed.

---

## Chaos Archetype Analysis

| Archetype | TCs | Avg Score | Notes |
|-----------|-----|-----------|-------|
| `multi_hop_compressed` ⚠️ | 3 | **0.51** | Worst performer — single-hop retrieval can't answer 3-hop queries |
| `over_decomposed` ⚠️ | 5 | **0.61** | Query too narrow; comparative context missing from results |
| `reformulation_drift` ⚠️ | 5 | **0.64** | Intent eroded; results are topically adjacent but don't answer the query |
| `none` ⚠️ | 7 | **0.69** | Clean queries still fail — primarily due to fidelity inversion bug |
| `keyword_stuffed` ⚠️ | 3 | **0.70** | Noise in query hurts precision but search still finds broadly relevant content |
| `temporal_ambiguity` ⚠️ | 7 | **0.85** | Best performer — Firecrawl handles "current/latest" queries well |
| *(copy_paste_artifact)* | 0 | — | Not sampled this run |

**Key finding:** `temporal_ambiguity` queries score highest (0.85) because Firecrawl's index is relatively fresh and the P1 agent's temporal extraction is strong. `multi_hop_compressed` queries score lowest (0.51) because no retrieval system can satisfy 3-hop queries without explicit decomposition.

The archetype system is working as designed — it surfaces architectural gaps in the search pipeline that clean queries would miss.

---

## Intent × Difficulty Analysis

### By Difficulty

| Difficulty | TCs | Avg Score | Pass Rate |
|------------|-----|-----------|-----------|
| `hard` | 7 | 0.63 | 0.0% |
| `medium` | 23 | 0.70 | 0.0% |
| *(no easy TCs generated)* | — | — | — |

No "easy" test cases were generated this run — the generator defaulted to medium/hard. This is expected with the new archetype weights that skew toward more adversarial query patterns.

---

## Two-Layer Cache Analysis

### Layer 1 — Query Cache

| Metric | Value |
|--------|-------|
| **Hit Rate** | 6.7% (2/30 TCs) |
| **Threshold Used** | 0.95 cosine similarity |
| **Max Age** | 3600 seconds (1 hour) |

2 TCs triggered L1 cache hits — both were `exact_duplicate` cache relationship variants. This is correct: only verbatim or near-verbatim queries should hit the query cache at the 0.95 threshold.

### Layer 2 — KB Semantic Cache

| Metric | Value |
|--------|-------|
| **Hit Rate** | 13.0% (16/123 URL checks) |

The 13% L2 hit rate is notable — this is the **first run with observable L2 cache activity**. URLs indexed from earlier TCs were successfully retrieved from Qdrant for later TCs using hybrid RRF scoring, avoiding re-scraping.

### Cache Intent Validation

| Generator Intent | Count | Query Hit % | Content Hit % |
|------------------|-------|-------------|---------------|
| `novel` | 20 | 0.0% | 0.0% |
| `rephrased_same_intent` | 3 | 0.0% | 45.5% |
| `same_source_different_angle` | 2 | 0.0% | 0.0% |
| `exact_duplicate` | 2 | **100.0%** | **100.0%** |
| `subset_of_parent` | 3 | 0.0% | 14.3% |

**Findings:**
- `exact_duplicate` variants correctly hit both cache layers (expected — verbatim queries should always cache hit)
- `rephrased_same_intent` variants achieved 45.5% L2 content hit — the KB semantic match is working for URL-level content reuse even when the query phrasing differs
- `same_source_different_angle` achieved 0% L2 hit — correct, since a different angle of the same source may need different document chunks that aren't semantically similar to the cached angle's query embedding
- `subset_of_parent` at 14.3% L2 — the parent documents aren't always relevant enough to the sub-query to exceed the RRF threshold

**Concern — all rounds indexed 0 new documents:** The KB build progression table (below) shows every round indexed 0 new chunks. This indicates the Qdrant indexer was not writing to the KB during this run, likely due to a connection or configuration issue. The L2 hits observed may have been from a prior run's residual KB data.

---

## KB Build Progression

| Round | TCs | New Indexed | Deduped (Hits) |
|-------|-----|-------------|----------------|
| 1–30 | 1 each | **0** all | 0 all |

**⚠️ All 30 rounds indexed 0 new chunks.** This is anomalous and warrants investigation. Possible causes:
1. Qdrant URL not configured or unreachable during indexing (check `session.log`)
2. Indexing background task silently failed due to exception handling swallowing errors
3. All URLs were already in the KB from the prior run (unlikely — previous run used different query corpus)

The 0-indexing does not affect scoring (the judge calls Firecrawl directly, not the KB), but it means no knowledge base is being built for future L2 cache efficiency.

---

## Retrieval Comparison: Firecrawl vs Internal KB vs Ideal

![KB Explorer — Hybrid RRF search and collection stats](./screenshots_new/kb_explorer.png)

| Metric | Firecrawl | Internal KB | Winner |
|--------|-----------|-------------|--------|
| **Kendall's τ (vs Ideal, normalized 0→1)** | **0.543** | 0.533 | 🏆 Firecrawl |
| **Overlap@3 (vs Ideal)** | **0.644** | 0.367 | 🏆 Firecrawl |
| **Overlap@5 (vs Ideal)** | **1.000** | 0.367 | 🏆 Firecrawl |
| **KB Outperforms FC** | — | — | 43.3% of TCs |

Firecrawl's native ranking significantly outperforms the internal KB on ordering quality. This is the same finding as the previous run. The KB is useful for scrape-cost avoidance but should not be used as a re-ranking signal.

**KB outperforms Firecrawl on 43.3% of TCs** — a meaningful minority. These are cases where the query semantics align strongly with the KB's RRF scoring while Firecrawl's ranking has a social media or generic hub artifact. Worth investigating whether authority-boosted re-ranking using the KB as a feature (not the ranking itself) could help.

---

## Root Cause Analysis

The Improvement Agent synthesized 5 root causes (ranked by severity × frequency):

### RC-001 · Scrape Score Inversion — Complete Documents Penalized, Truncated Posts Rewarded
- **Dimension:** `_baseline_fidelity`
- **Severity:** High | **Confidence:** High
- **Frequency:** 10/30 TCs (33%)
- **Affected TCs:** `tc_3b095b54`, `tc_316e5e79`, `tc_531d905d`, `tc_a7f33ea8`, `tc_e4e371ec`, `tc_9695f75c`, `tc_d6ace918`, `tc_b7028fb4`, `tc_0aff21d2`, `tc_a345a697`

**Root mechanism:** The P1 agent applies scrape penalty logic that weights cosmetic issues (missing alt-text, affiliate disclosures, embedded media placeholders, minor nav link noise) as high-severity failures, while the `content_completeness` field — which directly reflects whether the document is complete or truncated — is underweighted. The result:

- A 3,000-word Wikipedia article with two stray navigation links receives `scrape_score=0.20` (L1)
- A 25-word Instagram truncation with zero content gets `scrape_score=0.79` (L4)

This is not a system logic error — the P1 prompt instructs "assess how faithfully this markdown preserves the original page." The problem is the LLM's calibration: it penalizes "imperfect" formatting on complete pages more heavily than it penalizes the far more severe problem of a page with only 1% of its content visible.

---

### RC-002 · Thin Social Media / Forum Content Systematically Outranks Authoritative Sources
- **Dimension:** `_baseline_ranking`
- **Severity:** High | **Confidence:** High
- **Frequency:** 13/30 TCs (43%)
- **Affected TCs:** `tc_3b095b54`, `tc_c6c18688`, `tc_9695f75c`, `tc_39808d09`, `tc_5cad7b97`, `tc_0aff21d2`, `tc_a024035f`, `tc_b7028fb4`, `tc_69806b76`, `tc_0c0014af`, `tc_fee03e5a`, `tc_548fb6e6`, `tc_f748b907`

**Root mechanism:** Firecrawl's ranking appears to weight keyword density and engagement/backlink signals. Social media domains (Facebook, Reddit, Instagram) produce URLs with high link velocity (many pages link to them) and exact keyword matches in post titles. For queries like "best time to visit Iceland," a Reddit post titled exactly that outranks a Nordic Visitor specialist guide by keyword match alone.

The problem is structural: Firecrawl's search is designed for general web search, not authority-weighted retrieval for agentic AI use cases.

---

### RC-003 · Multi-Hop Queries Fail Coverage on All Sub-Hops Beyond the First
- **Dimension:** `coverage`, `multi_hop_synthesis`, `data_completeness`
- **Severity:** High | **Confidence:** High
- **Frequency:** 4/30 TCs (13%)
- **Affected TCs:** `tc_0c0014af`, `tc_ec3ed7e2`, `tc_35529ad7`, `tc_3b4eb676`

**Root mechanism:** Queries requiring 2–3 reasoning hops ("Identify entity X → find X's attribute Y → extract specific values from Y") are issued as single queries. Firecrawl returns documents satisfying Hop 1 (identifying the entity) but no document satisfies Hops 2–3.

Example — `tc_ec3ed7e2` ("Largest sovereign wealth fund AUM and its top holdings with allocation percentages"):
- **Hop 1** (which is the largest fund?): ✅ All 5 documents identify Norway's GPFG
- **Hop 2** (what are its top holdings?): ❌ Zero documents contain holdings data
- **Hop 3** (what are the % allocations?): ❌ Zero documents contain allocation percentages

The document that answers Hops 2–3 (nbim.no holdings report) was never retrieved.

---

### RC-004 · Error Pages, CAPTCHA Challenges, and Empty Scrapes Pollute Rankings
- **Dimension:** `_baseline_ranking`, `_baseline_fidelity`
- **Severity:** Medium | **Confidence:** High
- **Frequency:** 5/30 TCs (17%)
- **Affected TCs:** `tc_21e3b4aa`, `tc_316e5e79`, `tc_fee03e5a`, `tc_39808d09`, `tc_5cad7b97`

**Root mechanism:** When Firecrawl returns a URL that responds with a CAPTCHA wall (ScienceDirect), a 5xx error page (OSTI), a Cloudflare challenge, or a Quora "Something went wrong" page, the scrape still produces a result with `content_completeness='error_page'` and `word_count < 50`. These results are not filtered from the ranking and continue to occupy positions 1–5 with `authority=0.0` and `relevance=0.0`.

Example — `tc_21e3b4aa` (DAC energy penalty):
- Rank 3: OSTI error page — `authority=0.0`, `relevance=0.0`, `word_count=42`, `content_completeness='error_page'`
- This error page outranks the NETL DOE technical report at Rank 5 (`authority=0.98`, `relevance=0.92`)

---

### RC-005 · Comparative Research Intent Eroded by Over-Decomposition
- **Dimension:** `comparative_context_recovery`, `_baseline_ranking`
- **Severity:** Medium | **Confidence:** Medium
- **Frequency:** 3/30 TCs (10%)
- **Affected TCs:** `tc_548fb6e6`, `tc_f748b907`, `tc_0c0014af`

**Root mechanism:** Queries with the `over_decomposed` chaos archetype are narrow entity-focused queries that lost their comparative cross-entity context. The retrieval pipeline returns single-entity pages for each named entity but never finds a page that compares them side-by-side. The `comparative_context_recovery` dimension specifically tests for this and scores L1–L2 when no comparative document is found.

---

## Per-TC Failure Catalog

![Test Cases table with per-dimension scores](./screenshots_new/testcases_table.png)

### 🔴 Critical Failures (Score < 0.60)

| TC ID | Score | Query | Primary Failure |
|-------|-------|-------|----------------|
| `tc_0c0014af` | 0.39 | Top fossil fuel producers vulnerable to climate change + net zero targets | Multi-hop gap: only Hop 1 covered, Hops 2–3 zero coverage; Facebook at Rank 4 above State Dept |
| `tc_ec3ed7e2` | 0.57 | Largest sovereign wealth fund AUM 2026 + top holdings + allocation % | 3-hop failure: NBIM identified but holdings data absent from all 5 results |
| `tc_3b4eb676` | 0.53 | Quantitative energy penalty for amine sorbent regeneration in DAC | Zero documents contain amine-specific DAC regeneration energy values; ScienceDirect truncated at 511 words |
| `tc_9695f75c` | 0.57 | How to write an effective academic literature review step by step | Reddit (auth=0.1, 22w) at Rank 2 above Purdue OWL (auth=0.95) at Rank 4; YouTube scrape_score=0.20 despite full transcript |
| `tc_39808d09` | 0.47 | How to build a diversified dividend growth portfolio for retirement income | Reddit empty scrape at Rank 2 (word_count=0, scrape_score=0.0); Bogleheads buried at Rank 3 |
| `tc_35529ad7` | 0.56 | Largest sovereign wealth fund AUM 2026 + top holdings (exact_duplicate) | Exact same coverage failure as tc_ec3ed7e2 — confirms cache system, not sampling artifact |

---

### 🟡 Marginal Failures (Score 0.60–0.79)

| TC ID | Score | Query Excerpt | Primary Failure Dimension | Key Issue |
|-------|-------|---------------|--------------------------|-----------|
| `tc_3b095b54` | 0.76 | Lisbon neighborhoods Alfama tram 28 guide | Fidelity (inversion) + Ranking | Instagram at Rank 1 (25w); complete blogs at 0.20 scrape score |
| `tc_c6c18688` | 0.59 | Lisbon Alfama Bairro Alto cultural heritage origins | Fidelity + Ranking + Coverage | Facebook at Rank 1 (23w); Bairro Alto history entirely absent |
| `tc_9a8d344d` | 0.73 | Best season to trek in Patagonia | Ranking + Fidelity | Reddit (29w) at Rank 2 above Swoop (specialist guide) |
| `tc_21e3b4aa` | 0.67 | Energy penalty analysis for sorbent regeneration in direct air capture | Ranking + Fidelity | OSTI error page at Rank 3; NETL DOE report buried at Rank 5 |
| `tc_5cad7b97` | 0.62 | Best time to visit Iceland for Northern Lights | Ranking + Fidelity | Reddit (17w, auth=0.2) at Rank 1; Rank 5 empty doc (scrape_score=0.0) |
| `tc_69806b76` | 0.65 | Latest archaeological discoveries transforming understanding of ancient Egypt | Ranking + Fidelity | 2023 travel blog at Rank 1; penn.museum (auth=1.0) buried at Rank 5 |
| `tc_0aff21d2` | 0.74 | Byzantine Empire fall Constantinople 1453 Ottoman conquest | Fidelity + Authority | Facebook (25w), Reddit (28w), Quora error dominate result set |
| `tc_a024035f` | 0.59 | Binding agents and starches for gluten-free whole grain bread | Coverage + Ranking | No whole-grain-specific starch content; Facebook (19w) at Rank 3 |
| `tc_b7028fb4` | 0.74 | Concert tour production crew staging sound engineering | Ranking + Fidelity | Instagram (23w) at Rank 1; complete YouTube/Quora scores inverted to 0.20 |
| `tc_fee03e5a` | ~0.65 | Lisbon travel + cache variant | Ranking | Thin social media in top results |
| `tc_548fb6e6` | ~0.62 | Comparative query (over_decomposed) | comparative_context_recovery | Single-entity results only |
| `tc_f748b907` | ~0.64 | Comparative research (over_decomposed) | comparative_context_recovery + ranking | No cross-entity comparison found |

---

### 🟠 Failing Due to Fidelity Bug Only (Score ≥ 0.80 but floor blocked)

These TCs have solid retrieval and content scores but fail the dimension floor gate due to the scrape_score inversion on `_baseline_fidelity`:

| TC ID | Score | Query | Fidelity Score | Notes |
|-------|-------|-------|----------------|-------|
| `tc_a211b3c3` | 0.96 | Latest research on psychedelic-assisted therapy | 0.34 (L2) | All 5 docs score 0.20–0.60 despite complete content |
| `tc_531d905d` | 0.90 | 2026 Formula 1 season calendar and driver lineup | 0.31 (L2) | Wikipedia at 0.20 despite full faithful reproduction; Instagram 0.79 |
| `tc_d6ace918` | 0.87 | Long COVID neurological symptoms and mechanisms | 0.31 (L2) | PMC article complete at 0.20; Facebook NIH post truncated at 0.60 |
| `tc_e4e371ec` | 0.93 | Health risks of exceeding added sugar intake | 0.23 (L2) | healthdirect.gov.au: empty issues list, score=0.20; second fidelity eval contradicts first (0.9 vs 0.228) |
| `tc_a7f33ea8` | 0.86 | Current recommended daily added sugar limit for adults | ~0.25 (L2) | Harvard/CDC at 0.20 (faithfully captures); Facebook FDA post at 0.79 |

---

### ✅ No Clear-Cut Passes (Highest Scoring TCs)

| TC ID | Score | Query Excerpt | Why Near-Pass |
|-------|-------|---------------|---------------|
| `tc_a211b3c3` | 0.96 | Psychedelic-assisted therapy research | Coverage L5, Ranking L5 — only fidelity floor blocks pass |
| `tc_e4e371ec` | 0.93 | Added sugar health risks | All dimensions strong — dual fidelity evaluation contradiction is the sole blocker |
| `tc_531d905d` | 0.90 | F1 2026 season | Full coverage, good ranking — scrape inversion the sole cause |

---

## Cross-Dimension Failure Patterns

![Expanded TC detail — P1 profiles + rubric breakdown + diagnosis](./screenshots_new/testcase_expanded.png)

### Pattern 1: Scrape Score Inversion → Fidelity Floor → TC Fail

```
P1 agent: cosmetic penalty overweighted on complete docs
        │
        └──► scrape_score INVERTED (complete=0.20, truncated=0.79)
                    │
                    └──► _baseline_fidelity aggregated avg < 0.40
                                │
                                └──► Floor gate TRIGGERED → TC FAILS
                                     regardless of all other dimension scores
```

**Example:** `tc_531d905d` (F1 2026 season)
- `source_authority` = L5, `topical_coverage` = L5, `_baseline_ranking` = L4
- `_baseline_fidelity` = 0.31 due to inverted scrape scores → TC blocked at 0.90

---

### Pattern 2: Social Media Ranking Pollution → Triple Dimension Failure

```
Social media domain ranks #1–2 (word_count < 50)
        │
        ├──► _baseline_fidelity FAILS (thin content = low aggregated scrape avg)
        │
        ├──► _baseline_ranking FAILS (most relevant source buried)
        │
        └──► source_authority FAILS (result portfolio dominated by 0.1-0.2 auth sources)
```

**Observed in:** `tc_c6c18688`, `tc_0aff21d2`, `tc_5cad7b97`, `tc_39808d09`

---

### Pattern 3: Multi-Hop Query → Coverage + Synthesis + Data Completeness Triple Fail

```
Single query issued for 3-hop comparative data
        │
        └──► Firecrawl retrieves Hop 1 documents only
                    │
                    ├──► coverage FAILS (Hops 2–3 missing entities)
                    │
                    ├──► multi_hop_synthesis FAILS (no cross-hop synthesis possible)
                    │
                    └──► data_completeness FAILS (specific values absent)
```

**Observed in:** `tc_0c0014af`, `tc_ec3ed7e2`, `tc_35529ad7`, `tc_3b4eb676`

---

### Pattern 4: Paywalled Academic Content → Fidelity + Ranking Cascade

```
Top-2 results behind paywall → navigation-only scrape
        │
        ├──► _baseline_fidelity FAILS (nav_link_ratio > 0.7, word_count < 100)
        │
        └──► _baseline_ranking DEGRADED (empty pages rank above accessible sources
             because domain authority is high)
```

**Observed in:** `tc_316e5e79` (ScienceDirect captcha at Rank 1), `tc_21e3b4aa` (OSTI 500 error at Rank 3)

---

## RL Signal Statistics

![DPO Pairs — Chosen vs Rejected URL comparison](./screenshots_new/rl_dpo_pairs.png)

| Signal Type | Count | Output File |
|-------------|-------|-------------|
| **DPO Pairs** | 23 | `dpo_pairs.jsonl` |
| **Reward Signals** | 150 | `rewards.jsonl` |
| **Listwise Rankings** | 30 | `listwise_rankings.jsonl` |
| **Contrastive Fail Pairs** | 67 | `contrastive_fail_pairs.jsonl` |
| **Query Reformulations** | 30 | `query_reformulations.jsonl` |
| **SFT Gold Examples** | 0 | `sft_gold.jsonl` |
| **Scrape Quality Labels** | 150 | `scrape_quality_labels.jsonl` |

**Total signals generated: 500 across 7 signal types**

This is a **significant increase** from the previous run (3 signal types, ~131 total signals).

### Notable Signal Observations

**DPO Pairs (23):** All 23 pairs encode a ranking preference. Dominant rationale: "Low-authority social media result (word_count < 50) should be rejected in favor of specialist source (authority > 0.5, relevance > 0.9)." These pairs are high-quality training signal for a ranking re-ranker.

**Contrastive Fail Pairs (67):** Largest signal class. Each pair captures a specific rubric dimension failure — the "bad state" (actual retrieval outcome) vs. the "good state" (what the rubric says should have been there). 67 pairs across 30 TCs means an average of 2.2 contrastive fail triggers per TC, confirming that the rubric floor is regularly triggered.

**SFT Gold (0):** Zero TCs scored above the `sft_gold_score_threshold` (0.85) without triggering a floor failure. This is expected given the 0% pass rate. Once the fidelity inversion is fixed, ~5 TCs (those scoring 0.87–0.96 overall) would qualify as gold examples.

**Query Reformulations (30):** One per TC. These are the Improvement Agent's suggested query rewrites for each failing TC. Archetype coverage: multi_hop queries get decomposed sub-queries; over_decomposed queries get expanded versions with restored comparative context; temporal queries get year-anchored variants.

![RL Taxonomy — Failure pattern cluster view](./screenshots_new/rl_taxonomy.png)

### Improvement Micro-Taxonomy (Top Patterns)

| Pattern | Frequency | Description |
|---------|-----------|-------------|
| `scrape_score_inversion` | 33% | Complete documents with `content_completeness='complete'` and `word_count > 500` receive `scrape_score=0.20` while truncated fragments with `word_count < 50` receive `0.60–0.79`. Single largest contributor to `_baseline_fidelity` failures. |
| `thin_social_media_ranking` | 43% | Social media posts (Reddit, Facebook, Instagram) with `word_count < 50`, `authority < 0.3`, and failed scrapes systematically occupy top-3 ranking positions above comprehensive authoritative sources. |
| `multi_hop_decomposition_failure` | 13% | 3-hop queries treated as single-hop lookups. Only the first hop's documents are retrieved. |
| `error_page_rank_poisoning` | 17% | Error pages (OSTI 500, ScienceDirect captcha, Quora error) not filtered from results and occupy ranking positions above legitimate content. |
| `intent_erosion_over_decomposition` | 10% | Comparative queries decomposed into single-entity tokens, losing cross-entity comparison intent. |
| `paywalled_academic_content_pollution` | 10% | Academic publisher pages (ScienceDirect, ACS) behind paywalls return navigation-only content that still occupies high ranking positions. |

![Reward Signals — Per-URL reward bars](./screenshots_new/rl_rewards.png)

---

## Improvement Roadmap

### Engineering Proposals

Ranked by `priority_score` from the Improvement Agent:

#### 🥇 Priority 9.0 — Fix scrape_score Calibration for content_completeness

> **Proposal:** Replace the hardcoded scrape_score floor with a content-based scoring function that treats `content_completeness` as the dominant factor.

**Specific fix:**

```python
# In P1 agent post-processing (_validate_p1_consistency or calibration layer)
def calibrate_scrape_score(p1_result: P1Result) -> P1Result:
    cc = p1_result.content_completeness
    wc = p1_result.word_count
    issues = p1_result.scrape_issues

    # Rule 1: complete documents cannot score below 0.70 regardless of cosmetic issues
    if cc == "complete" and wc > 500:
        p1_result.scrape_score = max(p1_result.scrape_score, 0.70)

    # Rule 2: truncated documents cannot score above 0.40
    if cc == "appears_truncated" and wc < 100:
        p1_result.scrape_score = min(p1_result.scrape_score, 0.40)

    # Rule 3: error pages and navigation-only pages are capped at 0.20
    if cc in ("error_page", "navigation_only"):
        p1_result.scrape_score = min(p1_result.scrape_score, 0.20)

    return p1_result
```

- **Targets:** RC-001 (scrape score inversion)
- **Expected Impact:** +0.25 on `_baseline_fidelity` (from 0.397 → ~0.65), +0.08 overall
- **Affected TCs:** ~10 TCs (immediate fix), estimated 10–15 TCs would pass after this fix alone

---

#### 🥈 Priority 4.5 — Authority + Content Density Ranking Gate

> **Proposal:** Add post-retrieval re-ranking step that penalizes low-authority, thin-content results from social media domains.

```python
SOCIAL_DOMAINS = {"facebook.com", "instagram.com", "reddit.com", "youtube.com", "twitter.com", "tiktok.com", "quora.com"}

def rerank_authority_density(results, intent):
    """Demote social media / thin content for non-social queries."""
    scored = []
    for r in results:
        penalty = 1.0
        domain = extract_domain(r.url)
        if domain in SOCIAL_DOMAINS and (r.word_count or 0) < 100:
            penalty = 0.3  # severe demotion for thin social media
        elif domain in SOCIAL_DOMAINS:
            penalty = 0.7  # moderate demotion for longer social posts
        scored.append((r, r.firecrawl_rank * penalty))
    return [r for r, _ in sorted(scored, key=lambda x: x[1])]
```

- **Targets:** RC-002 (social media ranking), RC-004 (error page pollution)
- **Expected Impact:** +0.15 on `_baseline_ranking` (0.481 → ~0.63), +0.06 overall
- **Affected TCs:** 13 TCs (ranking)

---

#### 🥉 Priority 4.0 — Error Page Detection + Backfill

> **Proposal:** Add post-scrape filter that detects error pages, CAPTCHA challenges, and empty scrapes and removes them before ranking, backfilling from the next best Firecrawl candidates.

```python
def filter_error_results(results):
    clean = []
    for r in results:
        wc = len((r.full_markdown or "").split())
        if wc < 50 and r.scrape_cache_status != "kb_semantic_hit":
            logger.warning(f"[Filter] Removing thin/error result: {r.url} ({wc} words)")
            continue
        clean.append(r)
    return clean
```

- **Targets:** RC-004 (error page rank poisoning)
- **Expected Impact:** +0.10 on `_baseline_ranking` for affected TCs, +0.04 overall
- **Affected TCs:** 5 TCs

---

#### Priority 2.0 — Multi-Hop Query Decomposition

> **Proposal:** Implement a query decomposition pre-pass that detects 2–3 hop compound queries and splits them into sub-queries, merging results to cover all hops.

- **Targets:** RC-003 (multi-hop failure)
- **Expected Impact:** +0.30 on `coverage` for multi-hop TCs, +0.20 on `multi_hop_synthesis`, +0.10 overall
- **Effort:** High (requires LLM call for decomposition + result merging logic)
- **Affected TCs:** 4 TCs — but this is the most structurally significant gap

---

#### Priority 2.0 — Competitor Entity Injection for Comparative Queries

> **Proposal:** For `comparative_research` intent queries, add intent classification pre-pass that identifies named entities in the query and injects `site:entity-domain` sub-searches for each.

- **Targets:** RC-005 (over-decomposed comparative queries)
- **Expected Impact:** +0.25 on `comparative_context_recovery`, +0.15 on ranking for comparative queries
- **Effort:** Medium
- **Affected TCs:** 3 TCs

---

### Quick Wins

![Report Tab — Rendered markdown with dimension breakdown](./screenshots_new/report_tab.png)

#### Quick Win 1 — Fix scrape_score Floor for Complete Documents (+0.25 on fidelity)

This is a **one-line calibration fix** in `_validate_p1_consistency()`. The highest-impact change in this entire roadmap. Add the rule: if `content_completeness='complete'` AND `word_count > 500`, enforce `scrape_score >= 0.70`.

**Expected result:** ~10 TCs immediately pass the floor gate. 5 TCs (those with overall score 0.87–0.96) immediately pass.

---

#### Quick Win 2 — Filter Error Pages from Result Sets (+0.05 overall)

5-line post-scrape filter: if `word_count < 50` AND `content_completeness in ['error_page', 'navigation_only']`, remove the result and backfill. Eliminates OSTI error page, ScienceDirect CAPTCHA, Quora "Something went wrong" from ranking positions.

---

#### Quick Win 3 — Social Media word_count Penalty for Ranking (+0.10 on ranking)

Apply a rule: if `domain in SOCIAL_DOMAINS AND word_count < 100`, apply 0.5× ranking penalty. Prevents 17-word Reddit comments and 23-word Instagram reels from occupying top positions.

---

#### Quick Win 4 — Scrape_score Sanity Assertion (+0 score, prevents regression)

Add a runtime assertion: if `scrape_reasoning` contains "faithfully" AND `scrape_issues` is empty, then `scrape_score` must be ≥ 0.70. This catches the inversion bug before it propagates into fidelity aggregation and flags calibration drift in future runs.

---

## Judge Bias Warnings

![Diagnostics — Per-TC root cause diagnosis cards](./screenshots_new/rl_diagnostics.png)

### ⚠️ Dual `_baseline_fidelity` Scoring Contradiction

In several TCs (most clearly `tc_a345a697` and `tc_e4e371ec`), the `_baseline_fidelity` dimension is evaluated twice — once by the `_aggregate_fidelity()` deterministic path and once by a P2 judge that received a custom fidelity-adjacent dimension routed to it. The two evaluations produce dramatically different scores:

- `tc_a345a697`: Evaluation 1 → 0.9 (L5, "faithfully reproduces"), Evaluation 2 → 0.312 (L2, inverted score)
- `tc_e4e371ec`: Evaluation 1 → 0.9 (L5), Evaluation 2 → 0.228 (L2)

This is a **routing conflict**, not a judge bias issue. When a TC's custom rubric contains a dimension with keywords like "structural_fidelity" or "content_fidelity," the `_route_dimensions()` keyword matcher assigns it to the coverage family (default catch-all), and it's evaluated by a P2 judge. The baseline enforcer then injects `_baseline_fidelity` on top. Two fidelity evaluations are now live, and the floor gate takes the minimum — which is always the inverted P1 score.

**Fix:** Check if any custom dimension already covers fidelity before injecting `_baseline_fidelity`.

### ⚠️ `source_authority` Scores HIGH While Per-TC Diagnoses Show Low-Authority Sources

`source_authority` averages 0.838 across all TCs, with 12/17 TCs in the 0.8–1.0 range. This seems inconsistent with the 13 TCs showing social media pollution. However, this is not a bias issue — the `_baseline_authority` dimension (avg 0.73) is the one that correctly captures the authority failures. The custom `source_authority` dimensions were generated for TCs where authority was specifically tested (healthcare, academic) and not for the travel/social-media-heavy TCs.

---

## Regression vs Previous Run

| Metric | `run_20260701_152627` | `run_20260712_180951` | Change |
|--------|----------------------|----------------------|--------|
| Overall Score | 0.73 | **0.69** | -0.04 ⚠️ |
| Pass Rate | 17% (5/30) | **0%** (0/30) | -17% ⚠️ |
| Pass Threshold | 0.80 | 0.65 (lower!) | — |
| Generator Model | deepseek/deepseek-v4-flash | minimax/minimax-m3 | Changed |
| Dominant Dimension | Scrape 0.50 | `_baseline_fidelity` 0.40 | Structural |

**Important context:** These runs are not directly comparable. The architecture changed substantially:

1. The pass threshold was **lowered from 0.80 to 0.65** — if applied to the previous run, more TCs would have passed. The 0% pass rate this run reflects the new dimension floor gate (no dimension below 0.40), which didn't exist before.
2. The previous run used a hardcoded 3-axis rubric; this run uses dynamic per-TC rubrics with 2–4 custom axes plus baseline enforcement.
3. The previous run's "Scrape" score (0.50) is structurally equivalent to the new `_baseline_fidelity` (0.40) — both measure scrape quality and both are the primary bottleneck.

**True regression vs improvement:**
- The scrape quality problem has **not improved** — fidelity went from 0.50 → 0.40 average (though the measurement systems differ)
- The ranking quality problem is **consistent** — 0.88 → 0.48 looks like regression but the previous 0.88 was a clean 3-axis average; 0.48 reflects the harder rubric with explicit contrastive fail checks
- The **root cause diagnosis system is dramatically better** — we now have 67 contrastive fail pairs vs 0, 30 query reformulations vs 0, and per-TC diagnosis depth that didn't exist before

Regression detector flagged: **trend = Regression Detected ⚠️, difference = -0.16**

This is technically correct but should be read in context: the new architecture is surfacing failures the old system was not sensitive enough to detect.

---

## Conclusions & Next Steps

### What This Run Proved

1. 🔴 **The P1 scrape_score calibration is broken.** The single highest-priority fix in the entire system is the `content_completeness`-based scrape_score correction. Without it, the floor gate fires on TCs where the actual retrieval quality is excellent.

2. 🔴 **Social media content ranking is the most persistent structural failure.** 43% of TCs have thin social media content outranking specialist authoritative sources. This is a Firecrawl-side ranking signal issue that can be partially mitigated with post-retrieval re-ranking.

3. 🟡 **Multi-hop queries expose a fundamental architectural gap.** The pipeline issues single queries and cannot decompose 3-hop compound queries. 4 TCs failed on this pattern, with 0 data for hops 2–3 despite searching.

4. ✅ **Topical coverage and freshness are genuine strengths.** Dimensions like `topical_coverage` (0.85), `_baseline_freshness` (0.81), `drift_recovery` (0.95) score high consistently. Firecrawl's search recall is broad and fresh.

5. ✅ **The rubric-first architecture is producing rich, actionable RL signal.** 500 training signals across 7 types, including 67 contrastive fail pairs and 30 query reformulations, are ready for downstream model training.

6. ✅ **The chaos archetype system works as designed.** `multi_hop_compressed` (avg 0.51) and `over_decomposed` (avg 0.61) correctly expose architectural gaps that clean queries miss.

### Immediate Actions (Next 2 Weeks)

- [ ] **Quick Win 1:** Add `content_completeness`-based scrape_score floor enforcement in `_validate_p1_consistency()` — this is a 5-line change in `eval/judge.py`
- [ ] **Quick Win 2:** Add error-page detection and removal filter in `pipeline/orchestrator.py` post-scrape
- [ ] **Quick Win 3:** Add `word_count < 100` social media ranking penalty in post-retrieval step
- [ ] **Quick Win 4:** Add runtime scrape_score sanity assertion to prevent future calibration drift
- [ ] **Investigate:** KB indexing failure — all 30 rounds indexed 0 chunks; check `session.log` for indexer exceptions

### Next Eval Cycle Goals

- [ ] Run 30 TC cycle after Quick Wins deployed — target fidelity floor > 0.45 and pass rate > 30%
- [ ] Include 5 TCs with explicit `copy_paste_artifact` archetype (not sampled this run)
- [ ] Add "easy" difficulty TCs to establish a clean baseline above the noise
- [ ] Investigate whether SFT gold threshold of 0.85 is reachable — consider lowering to 0.80 for this run profile

---

*Report generated by EvalOS Framework — `run_20260712_180951`*  
*Full raw data: `outputs/runs/run_20260712_180951/run.json`*  
*Individual TC reports: `outputs/runs/run_20260712_180951/tc_reports/`*  
*RL Signals: `outputs/runs/run_20260712_180951/rl_signals/`*
