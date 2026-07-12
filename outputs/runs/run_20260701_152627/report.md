# Firecrawl Eval Report: run_20260701_152627
Generated: 2026-07-01 16:29:04

## Executive Summary
- **Overall Score**: 0.73 🟡
- **Test Cases**: 30 | Passed: 5 | Failed: 25
- **Coverage**: 0.92 | **Ranking**: 0.88 | **Scrape Quality**: 0.50

### Executive Diagnosis
This run achieved a pass rate of **17%** across 30 test cases. The primary bottleneck identified is **JavaScript-rendered data tables and structured content not captured**, impacting 15/30 TCs of the evaluated queries. Addressing the key root causes could yield a significant boost in performance, particularly on the **scrape** dimension.

## Batch Progression (KB Build)
| Round | TCs | New Indexed | Deduped (Hits) |
|-------|-----|-------------|----------------|
| 1 | 1 | 20 | 0 |
| 2 | 1 | 20 | 0 |
| 3 | 1 | 16 | 0 |
| 4 | 1 | 0 | 0 |
| 5 | 1 | 18 | 0 |
| 6 | 1 | 19 | 0 |
| 7 | 1 | 11 | 0 |
| 8 | 1 | 15 | 0 |
| 9 | 1 | 0 | 0 |
| 10 | 1 | 7 | 0 |
| 11 | 1 | 0 | 20 |
| 12 | 1 | 19 | 0 |
| 13 | 1 | 0 | 0 |
| 14 | 1 | 22 | 0 |
| 15 | 1 | 22 | 0 |
| 16 | 1 | 25 | 0 |
| 17 | 1 | 0 | 19 |
| 18 | 1 | 25 | 0 |
| 19 | 1 | 20 | 0 |
| 20 | 1 | 10 | 15 |
| 21 | 1 | 16 | 0 |
| 22 | 1 | 11 | 0 |
| 23 | 1 | 18 | 0 |
| 24 | 1 | 0 | 15 |
| 25 | 1 | 15 | 0 |
| 26 | 1 | 0 | 25 |
| 27 | 1 | 21 | 0 |
| 28 | 1 | 20 | 0 |
| 29 | 1 | 0 | 19 |
| 30 | 1 | 22 | 0 |

## Two-Layer Cache Analytics
- **Layer 1 (Query) Cache Hit Rate**: 26.7% (8/30)
- **Layer 2 (Content) Cache Hit Rate**: 0.0% (0/128)

### Cache Intent Validation
*(Did the generator successfully trick the cache?)*
| Generator Intent | Count | Query Hit % | Content Hit % |
|------------------|-------|-------------|---------------|
| `novel` | 21 | 0.0% | 0.0% |
| `semantic_near_miss` | 9 | 88.9% | 0.0% |

## Retrieval Comparison: Firecrawl vs KB vs Ideal
*(Evaluates if our RRF Hybrid KB outperforms Firecrawl's native ranking)*

| Metric | Firecrawl | Internal KB | Winner |
|--------|-----------|-------------|--------|
| Kendall's τ (vs Ideal) | 0.453 | -0.367 | Firecrawl 🏆 |
| Overlap@3 (vs Ideal) | 0.711 | 0.322 | Firecrawl 🏆 |

## Improvement Roadmap

### Root Causes (ranked by severity)
| # | Dimension | Issue | Severity | Confidence | Affected TCs | Frequency |
|---|-----------|-------|----------|------------|--------------|-----------|
| 1 | scrape | JavaScript-rendered data tables and structured content not captured | high | high | tc_91464a3b, tc_de5e4df4, tc_bd1bd260... | 15/30 TCs |
| 2 | scrape | Content truncation prevents complete data extraction from long pages | high | high | tc_7b0cb65b, tc_5ac84dfe, tc_107f793b... | 12/30 TCs |
| 3 | coverage | Search index lacks official/authoritative domains for explicitly named entities | high | medium | tc_6b53cb03, tc_bd1bd260, tc_02b1edeb... | 6/30 TCs |
| 4 | ranking | Ranking model undervalues official/high-authority sources and overweights social media/forums for data queries | high | high | tc_688a509c, tc_74ceb664, tc_bd1bd260... | 11/30 TCs |
| 5 | scrape | Inaccessible content due to blocks, paywalls, or server errors | medium | medium | tc_aadb30d9, tc_6b53cb03, tc_91464a3b... | 4/30 TCs |

### Proposals (ranked by priority)
| # | Targets | Proposal | Expected Impact | Effort | Priority |
|---|---------|----------|-----------------|--------|----------|
| 1 | rc_003 | Add automatic site: search for explicitly named entities in queries | +0.08 on coverage dimension | low | 9.0 |
| 2 | rc_002 | Increase maximum scrape length and implement chunked/multi-pass extraction | +0.10 on overall score | medium | 8.0 |
| 3 | rc_001 | Implement headless browser rendering with wait mechanisms for data tables | +0.15 on scrape dimension | high | 7.0 |
| 4 | rc_004 | Retrain ranking model with strong authority signals and source demotion for data intents | +0.10 on ranking dimension | medium | 7.0 |
| 5 | rc_005 | Implement access strategies and fallbacks for blocked/inaccessible pages | +0.03 on scrape dimension | high | 4.0 |

### Quick Wins
| # | Action | Description | Expected Impact |
|---|--------|-------------|-----------------|
| 1 | Demote social media platforms (Facebook, Instagram, Reddit, YouTube) for data extraction and factual lookup queries | Apply a heuristic post-retrieval filter: if intent is data_extraction or factual_lookup, push social-media results to the bottom of the list. | +0.05 on ranking |
| 2 | Increase truncation limit for markdown conversion | Adjust a configuration parameter to raise the maximum character count per page scrape, significantly reducing truncation on long pages. | +0.03 overall |
| 3 | For queries containing explicit organization names, use site: query expansion | Before the main search, add a parallel search with site:domain for each named entity and merge results, ensuring official sources are captured. | +0.04 on coverage |

### Cross-Dimension Failure Patterns
| Pattern | Hypothesis / Context |
|---------|----------------------|
| Missing authoritative domains cascades to ranking and scrape failures | When official sites are absent from search results, the system cannot rank them first, forcing reliance on lower-quality pages that often lack structured data. This causes both low ranking scores and poor scrape quality. |
| Dynamic content issues degrade both scrape and ranking simultaneously | JavaScript-rendered tables are not captured, making the scraped markdown appear thin and unstructured. This poor content quality then feeds back into ranking signals, causing even well-chosen pages to be demoted because they appear data-poor. |

### Judge Bias Warnings
- ⚠️ Potential over-reliance on exact presence of structured table data in markdown; pages that embed critical data in images or interactive JavaScript may be penalized even when the content is present in a non-text format, which is more a scraper limitation than a true quality failure.

## RL Training Signals
- **DPO Pairs Generated**: 11
- **Reward Signals**: 112

## Regression vs Previous Run
- Trend: No previous data

## Appendix: Failed Test Cases Detail
*(Showing only test cases with Overall Score < 0.8)*

### tc_f0d17d75 (Score: 0.76) ❌
**Query**: `Goldman Sachs top stock picks July 2026 with tickers and price targets`
**Category**: paywalled_content | **Intent**: novel

**Root Cause**: Despite perfect coverage and ranking, overall score is low because scrapes of the top two results—Yahoo Finance and Goldman Sachs.com—failed to capture the required tickers and price targets due to missing JavaScript-rendered tables and page mismatches.

- **Coverage Diagnosis**: All expected terms were present across results; no coverage gaps.
- **Ranking Diagnosis**: Firecrawl ranking matched the ideal ranking exactly; no divergence.
- **Scrape Diagnosis**: Rank 1 (Yahoo Finance) scrape missed the stock selection table because dynamic JavaScript content was not rendered, and the markdown was truncated mid-sentence. Rank 2 (Goldman Sachs) pointed to a generic markets hub lacking any stock pick tables. Rank 3 (Forbes) had no price targets, Rank 4 (MarketBeat) had broken table rows and heavy noise, and only Rank 5 (Instagram) was scraped cleanly but is a low-credibility source.

**Fix Actions**:
- Enable full JavaScript rendering with a 5–10 second delay for dynamic tables on financial sites like Yahoo Finance.
- Target the specific Goldman Sachs article URL for stock picks (e.g., insights page with the report) rather than the general /markets endpoint.
- Increase markdown truncation limit and use table‑aware parsing to capture complete ticker/price‑target data from scraped content.


---
### tc_89639350 (Score: 0.79) ❌
**Query**: `Apple Q2 2026 revenue breakdown iPhone services Mac vs Wall Street consensus`
**Category**: rapidly_changing | **Intent**: novel

**Root Cause**: Scraped markdown lacks structured financial data tables, with many pages providing only bullet lists or truncated text, making precise data extraction difficult.

- **Coverage Diagnosis**: All must-mention terms (Apple, Q2_2026, iPhone_revenue, Wall_Street_consensus) were found across search results; coverage is perfect.
- **Ranking Diagnosis**: Ranking matches ideal priority with Apple official press release first; no divergence from expected source importance.
- **Scrape Diagnosis**: Multiple pages lack expected data tables (only bullet lists), CNBC content is truncated mid-sentence, Yahoo Finance shows formatting issues, Apple page provides only text and a PDF link, and YouTube result is a transcript. These factors degrade scraped content quality.

**Fix Actions**:
- Enhance scraper to detect and extract HTML tables into structured markdown tables or JSON.
- Implement truncation handling: retry full-page loads, increase wait times, or use headless browser rendering to capture complete content.
- For sources like Apple that link to PDFs, add PDF extraction capability or flag such links for alternative structured data retrieval.


---
### tc_15278c17 (Score: 0.77) ❌
**Query**: `Python 3.13 typing syntax updates compared to 3.12 ParamSpec and TypeVarTuple`
**Category**: code_documentation | **Intent**: semantic_near_miss

**Root Cause**: The ranking under-prioritized the most relevant version-specific article (rank 5) and scraping produced incomplete or poorly structured markdown missing clear version comparison tables, reducing the answer's completeness.

- **Coverage Diagnosis**: All expected terms (Python_3.13, ParamSpec, TypeVarTuple) were found, but the diagnostic note mentions PEP_646 not found, which may be a minor gap for a truly comprehensive comparison.
- **Ranking Diagnosis**: The ideal ranking (1,2,5,3,4) puts the focused article (5) higher than generic Reddit/YouTube content (3,4). Firecrawl demoted it, likely due to lower domain/signal weight for a personal blog compared to high-engagement community platforms.
- **Scrape Diagnosis**: Multiple results lacked a dedicated version comparison table, essential for the query. Truncation (e.g., mid-word, mid-section) and poor structure (YouTube transcript) further degrade markdown utility for downstream comparison.

**Fix Actions**:
- Boost content with explicit version comparison indicators (e.g., 'vs', 'compared to', side-by-side tables) for queries containing 'compared to' or 'vs'.
- Enhance scraping to preserve table structure and implement adaptive truncation that avoids cutting off comparative examples or sections.
- Apply a site-quality boost for official documentation (docs.python.org, typing.python.org) and authoritative technical blogs when the query is code_documentation and comparative.


---
### tc_688a509c (Score: 0.74) ❌
**Query**: `2026 state privacy law comparison chart CCPA California vs Colorado CPA vs Virginia VCDPA key requirements`
**Category**: structured_data_extraction | **Intent**: novel

**Root Cause**: The main issue is poor scrape quality: top results fail to capture complete side-by-side comparison tables due to truncation, paywalls, or missing structured data, making it impossible to extract key requirements for all three states.

- **Coverage Diagnosis**: All expected state law names (California, Colorado, Virginia) were found in titles/snippets, resulting in perfect coverage. However, specific details like 'consumer rights to opt-out' and 'sensitive data processing' were missing entirely, indicating scraped content lacks depth.
- **Ranking Diagnosis**: Ranking was near-ideal (score 0.96); minor divergence occurred because khlaw.com was ranked first due to its comparison-chart mention, but actual scrape missed large portions of the table. Bloomberg Law ranked second as an authoritative source, but its page lacked a direct comparison table. Ideal ranking correctly prioritized authoritative, structured sources.
- **Scrape Diagnosis**: Scrape quality is critically low: khlaw.com truncated table, Bloomberg Law missing comparison table altogether, Osano only covers California, Practical Law behind paywall, and only LinkedIn provided complete content but with low authority. These issues prevent extraction of a full CCPA/CPA/VCDPA comparison.

**Fix Actions**:
- Increase scrape depth and render JavaScript to capture full comparison tables, especially on sites like khlaw.com that explicitly offer side-by-side charts.
- Boost or directly query authoritative privacy domains (iapp.org, bakerlaw.com) known for structured comparison charts, even if they are not organically top-ranked.
- Implement smart retry with table detection: if expected state names are not found in tabular format, attempt alternative extraction methods or fallback to secondary sources.


---
### tc_aadb30d9 (Score: 0.65) ❌
**Query**: `USPTO patent term adjustment rules 2026 PTAB trials`
**Category**: structured_data_extraction | **Intent**: novel

**Root Cause**: Scraped pages suffer from login walls, paywalls, and errors, blocking extraction of required structured data (tables, citations), despite near-perfect search result relevance and ranking.

- **Coverage Diagnosis**: Coverage was perfect (1.0) with all expected terms found across results.
- **Ranking Diagnosis**: Ranking score is high (0.924) but diverged from ideal by placing official USPTO pages and law firm analysis lower than blog posts, reducing prioritization of authoritative sources.
- **Scrape Diagnosis**: Scrapes are heavily degraded: USPTO portal results (1,4) are behind login, PatentlyO (2) is paywalled, IPWatchdog (3) missing data tables and truncated, and bipc.com (5) completely failed (Cloudflare error). Consequently, expected elements 'data_tables' and 'statutory_regulatory_citations' are missing from all results, and noise from banners/overlays dominates the extracted markdown.

**Fix Actions**:
- Deploy login-aware crawling for USPTO portals to fetch actual data beyond registration banners, or use pre-authenticated sessions.
- Improve content extraction on semi-accessible pages: for IPWatchdog and similar sites, attempt advanced rendering to capture tabular data and avoid truncation; for paywalled content, extract available snippets cleanly.
- Adjust ranking to boost .gov and law firm domains (e.g., uspto.gov, bipc.com) over blog platforms when extracting regulatory data, using domain authority signals.


---
### tc_6b53cb03 (Score: 0.44) ❌
**Query**: `Japan Rail Pass July 2026 price comparison JR East vs JR West vs JR Kyushu green car ordinary`
**Category**: structured_data_extraction | **Intent**: novel

**Root Cause**: Search missed official regional JR company sites (JR East, West, Kyushu) entirely, causing zero coverage of critical entities and depriving the LLM of authoritative price data for the desired comparison.

- **Coverage Diagnosis**: The query explicitly requests price comparison for JR East, JR West, and JR Kyushu, but these terms ('JR_East', 'JR_West', 'JR_Kyushu') were absent from all result titles, snippets, and content_preview.
- **Ranking Diagnosis**: Ideal ranking would place regional JR official sites near the top, but since they were never retrieved, the available results are ranked only by general relevance, leading to divergence from the ideal order.
- **Scrape Diagnosis**: Scraped pages lack structured comparison tables or charts. Result 1 has broken table formatting; Result 2 lacks price data; Result 4 is inaccessible (403); Result 5 truncated and noisy. No page provides the expected comparative data for the three regional passes.

**Fix Actions**:
- Expand search with explicit queries for 'JR East pass price 2026', 'JR West pass price 2026', 'JR Kyushu pass price 2026' alongside the national pass.
- Improve scraping to robustly extract tabular price data from official pages and implement fallback (e.g., cached versions) for blocked content like the Japan Travel guide.
- Add entity-pair detection to ensure comparative queries like 'A vs B vs C' trigger focused retrieval on each entity’s official domain.


---
### tc_91464a3b (Score: 0.66) ❌
**Query**: `UC Berkeley UCLA San Diego 2026 freshman admit rates by major`
**Category**: structured_data_extraction | **Intent**: novel

**Root Cause**: Scraping failed to extract tables from the official UC dashboard (dynamic content) and an important news source returned 406, while ranking over-prioritized social media over authoritative sources.

- **Coverage Diagnosis**: All required entities (UC Berkeley, UCLA, UC San Diego) were present; no coverage issues.
- **Ranking Diagnosis**: Firecrawl ranked Facebook (low authority, no major‑split data) at position 2, while ideal ranking placed it last. The SFChronicle news article (potentially with 2026 data) was ranked 4 instead of 2. The ranking lacks source‑priority logic for data‑extraction queries.
- **Scrape Diagnosis**: Official UC page (result 1) requires JavaScript to render tables, so only descriptive text was scraped (score 0.55). SFChronicle (result 4) returned error 406, preventing any content extraction (score 0.05). Blog (result 5) included social‑media noise and missing interactive element (score 0.7).

**Fix Actions**:
- Enable JavaScript rendering and wait for interactive elements to load on official dashboards to extract data tables.
- Adjust ranking to strongly boost .edu and reputable news domains, and demote social media except official accounts, for data‑extraction queries.
- Handle HTTP errors (e.g., 406) with retries or fallback user‑agents, and strip social‑link noise from scraped markdown.


---
### tc_74ceb664 (Score: 0.64) ❌
**Query**: `What stocks does Goldman Sachs say to buy in July 2026 with target prices`
**Category**: paywalled_content | **Intent**: semantic_near_miss

**Root Cause**: The ranking prioritized a news article over the official Goldman Sachs insights page, despite the query asking for what Goldman Sachs itself says. The official page, while less specific to July 2026, is more authoritative, causing a ranking mismatch. Also, none of the results perfectly matched the July 2026 timeframe, indicating a temporal relevance gap.

- **Coverage Diagnosis**: Coverage was perfect with all expected terms present. No missing terms.
- **Ranking Diagnosis**: LLM ideal ranking placed Goldman Sachs' own insights page (rank 2) first due to higher authority, while Firecrawl ranked Yahoo Finance (rank 1) first because it contained more explicit match with stock picks and target prices. The query intent is to hear from Goldman itself, so the official source should be boosted. Also, the Instagram result (rank 5) has low authority and should be demoted.
- **Scrape Diagnosis**: All results had perfect scrape quality with no issues. No paywall or formatting problems detected.

**Fix Actions**:
- Boost official domain authority for queries asking what a specific entity says, giving preference to the entity's own pages.
- Implement stricter temporal filtering to ensure results explicitly match the requested month/year (July 2026) when specified.
- Demote or remove low-authority domains like Instagram from financial data extraction queries.


---
### tc_dd4f5459 (Score: 0.55) ❌
**Query**: `ECMAScript 2025 vs 2026 finalized features stage 4 proposal list`
**Category**: structured_data_extraction | **Intent**: novel

**Root Cause**: The search failed to return authoritative sources (tc39.es, MDN) and lacked a page directly containing a structured comparison of ES2025 vs ES2026 stage 4 features, leading to poor extraction of the desired comparative list despite good coverage and scrape quality.

- **Coverage Diagnosis**: All expected terms (ECMAScript_2025, ECMAScript_2026, TC39_proposals) were found in the search results, but none of the retrieved pages explicitly listed and compared the finalized stage 4 proposals for both versions side by side.
- **Ranking Diagnosis**: Ranking diverged from the ideal because authoritative sources like tc39.es and MDN were completely missing, while less authoritative blogs and Reddit were ranked above the more reliable Wikipedia. The ideal ranking prioritizes official ECMA resources and reputable secondary sources.
- **Scrape Diagnosis**: Scrape quality was perfect for all results, but the raw markdown did not contain a ready-to-extract comparative list. The necessary details were scattered across prose, tables, and different sections, making synthesis into a clean structured comparison difficult.

**Fix Actions**:
- Include official ECMAScript specification pages (e.g., tc39.es/ecma262/) and the finished proposals page (https://tc39.es/process-document/) in search results.
- Adjust ranking weights to strongly favor authoritative domains (tc39.es, developer.mozilla.org, ecma-international.org) and reliable secondary sources (Wikipedia) over social media and personal blogs.
- Enhance extraction to detect and reconcile structured data from multiple sources, such as parsing Wikipedia's version history table and aligning it with proposal lists from the TC39 GitHub repository.


---
### tc_04205a98 (Score: 0.77) ❌
**Query**: `how many grams of sugar should an adult eat per day according to new FDA guidelines in 2026`
**Category**: structured_data_extraction | **Intent**: semantic_near_miss

**Root Cause**: The system missed the key phrase 'daily limit' present in result 3's snippet, and the ranking did not prioritize the FDA's official communication over a CDC page, causing a drop in coverage and a minor ranking error.

- **Coverage Diagnosis**: The phrase 'daily limit' appears in the snippet of result 3 (FDA Facebook post) but was not detected by the coverage evaluator; other results discuss limits without using the exact term, leading to a missed hit for the 'daily_limit' expected term.
- **Ranking Diagnosis**: Result 3 (FDA Facebook post) should rank above result 2 (CDC) because the query specifically requests FDA guidelines, but the ranking algorithm did not boost official social media channels from the target agency.
- **Scrape Diagnosis**: Scraped content consistently lacks the explicit requested information: the FDA page gives a calorie percentage, not grams; the CDC page gives a per-meal limit; the Facebook post cites AHA, not FDA, limits; no result provides a sex-specific table or 2026-specific guideline.

**Fix Actions**:
- Ensure exact phrase matching across all result snippets and titles during coverage evaluation, not just the top result.
- Boost ranking for official social media posts (e.g., Facebook) when the queried authority is explicitly named, treating them as authoritative sources.
- Enhance scraping to extract numeric daily limits in grams and sex-specific recommendations from unstructured text, and add a flag when a page does not directly answer with the required authority.


---
### tc_4d66dfdf (Score: 0.79) ❌
**Query**: `CDC adult immunization schedule 2026 table vaccine names doses`
**Category**: structured_data_extraction | **Intent**: novel

**Root Cause**: Coverage score dropped because the critical term 'influenza' was absent from all snippets and content previews due to incomplete scraping of the primary CDC schedule table, which was truncated and missing many vaccine rows.

- **Coverage Diagnosis**: Expected vaccine names like 'influenza' were missing because the scraped markdown of the main schedule page (rank 1) ended prematurely, omitting rows for Influenza and other vaccines. Other results either lacked the table entirely or had similar truncation.
- **Ranking Diagnosis**: Ranking aligned perfectly with the ideal order; all CDC sources were prioritized correctly, and the notes page was ranked before the easy-read version as intended.
- **Scrape Diagnosis**: Result 1 truncated mid-table, missing Influenza, Pneumococcal, Hepatitis, Meningococcal, Hib, Mpox, and IPV rows. Result 3 also truncated. Result 4 had garbled PDF text and truncation. Result 5 contained no table. These issues combined prevented the target term from appearing in any scraped content.

**Fix Actions**:
- Use a full-page capture with headless browser and wait for dynamic content to ensure the entire immunization table is loaded and extracted, including all rows.
- Implement a dedicated table extraction algorithm that identifies all <tr> elements and does not cut off, even if the page uses lazy loading or large tables.
- For PDFs, switch to a dedicated PDF parser (e.g., PyMuPDF) that preserves text integrity and handles multi-page documents without truncation.


---
### tc_921d35c4 (Score: 0.76) ❌
**Query**: `EU Digital Services Act 2026 deadline for very large online platforms risk assessments`
**Category**: structured_data_extraction | **Intent**: novel

**Root Cause**: Search coverage and ranking were adequate, but all scraped results suffered from missing structured data (e.g., compliance deadlines tables) and content truncation, preventing extraction of the exact 2026 deadline for VLOP risk assessments.

- **Coverage Diagnosis**: All must‑mention terms ('EU_Digital_Services_Act', 'very_large_online_platforms', 'risk_assessment') were present across results; no coverage gaps.
- **Ranking Diagnosis**: Firecrawl ranking differed slightly from the LLM ideal (e.g., result 2 should be lower to prioritize official EU sources), but the given ranking score is 1.0, indicating no critical ranking failure.
- **Scrape Diagnosis**: Every scraped page was truncated at the end and lacked essential structured data: a compliance deadlines table and a legal definitions list. Additionally, result 1 contained noise from an EU cookie consent banner. These issues prevented reliable extraction of the specific 2026 deadline.

**Fix Actions**:
- Add custom extraction rules (CSS/XPath) to capture the compliance deadlines table and legal definitions list from known DSA pages.
- Filter out boilerplate noise (e.g., cookie consent banners) during HTML‑to‑markdown conversion.
- Increase the maximum scrape depth or disable content truncation for factual lookup queries to ensure complete page capture.


---
### tc_08a1ff59 (Score: 0.78) ❌
**Query**: `Federal Reserve dot plot June 2026 FOMC interest rate projections table`
**Category**: structured_data_extraction | **Intent**: novel

**Root Cause**: Despite perfect coverage and ranking, the overall score of 0.784 indicates a failure in structured data extraction, likely due to the top result being a PDF, which poses challenges for accurate table parsing.

- **Coverage Diagnosis**: All expected terms ('Federal Reserve', 'dot plot', 'federal funds rate') were found across the results; coverage score is 1.0 with no misses.
- **Ranking Diagnosis**: Ranking is perfect (score 1.0) with the official source PDF ranked first as desired; no ranking divergence.
- **Scrape Diagnosis**: The top result is a PDF, which can introduce noise, formatting irregularities, and table parsing errors compared to HTML. While individual scrape quality scores are 1.0, the overall extraction of the precise projection table likely suffered, reducing the final score.

**Fix Actions**:
- Enhance PDF table extraction logic to accurately parse structured economic projections from official PDF documents.
- Introduce a structured data extraction quality metric that directly evaluates the integrity and completeness of extracted tables.
- Prefer HTML-format official sources when available to avoid PDF parsing overhead; monitor alternative sources like FRED for machine-readable data.


---
### tc_bd1bd260 (Score: 0.65) ❌
**Query**: `global average temperature anomaly 2026 year to date NOAA NASA GISS Berkeley Earth`
**Category**: rapidly_changing | **Intent**: novel

**Root Cause**: The search missed the NASA GISS source required by the query, and ranking over‑prioritized a secondary Berkeley Earth update over the official NOAA‑hosted dataset, while scraping failed to extract structured data tables from most pages.

- **Coverage Diagnosis**: Expected source 'NASA_GISS' was not found in any result. Only NOAA and Berkeley Earth were covered. Result 2 (NASA) is outdated (2025) and not from GISS, while the query explicitly asks for NASA GISS 2026 anomaly data.
- **Ranking Diagnosis**: Firecrawl ranked the recent Berkeley Earth update (result 1) first, but the ideal ranking places the NOAA PSL dataset (result 4) first because it represents an official source. The query prioritizes official NOAA/NASA data, yet the ranking favored a secondary analysis over the official NOAA repository.
- **Scrape Diagnosis**: Results 1, 4, 5 lacked expected data tables; truncation cut off content in results 1 and 5; result 2 contained mostly navigation and irrelevant highlights. Scraped markdown failed to capture structured numerical data and time‑series charts, reducing informativeness for the query.

**Fix Actions**:
- Include NASA GISS global temperature anomaly page (e.g., data.giss.nasa.gov/gistemp/) in the index to cover the missing source.
- Boost ranking of official data repositories (NOAA PSL, NASA GISS) when query contains explicit organization names like 'NOAA' or 'NASA GISS'.
- Enhance scraping to retain data tables, increase truncation limits, and better parse pages to capture structured numerical content.


---
### tc_02b1edeb (Score: 0.55) ❌
**Query**: `compare inside balcony cabin sizes 2026 Royal Caribbean Carnival Norwegian`
**Category**: structured_data_extraction | **Intent**: novel

**Root Cause**: Search failed to retrieve pages comparing inside balcony cabin sizes across all three cruise lines (especially missing Norwegian), ranking favored low-authority social media over official sites, and scrape quality suffered from missing structured data like comparison tables and dimensions.

- **Coverage Diagnosis**: Expected to find mentions of Norwegian Cruise Line in the context of inside balcony cabin sizes, but no result included NCL. Royal Caribbean and Carnival were partially covered but not in a comparative format.
- **Ranking Diagnosis**: The ideal ranking placed the official Royal Caribbean site and the comparative Cruise Critic forum first, but the system ranked a Facebook post highest due to possibly matching keywords without considering authority and comparative depth. The blog and forum with more comparative content were pushed down.
- **Scrape Diagnosis**: Multiple pages lacked comparison tables and cabin dimension measurements, reducing extraction quality. The Royal Caribbean official page lacked comparative tables, and the cruise blog and forum failed to produce structured data despite being relevant.

**Fix Actions**:
- Expand search sources to definitively include official deck plan and cabin spec pages from Norwegian Cruise Line and Carnival to cover all three lines.
- Adjust ranking to prioritize official cruise line websites and dedicated comparison forums (e.g., Cruise Critic) over social media posts for comparative queries.
- Enhance scraping to target pages with explicit dimension tables and structured specifications, and flag or fallback when such data is absent.


---
### tc_7b0cb65b (Score: 0.65) ❌
**Query**: `what vaccines do adults need in 2026 according to the CDC schedule and how many doses each`
**Category**: structured_data_extraction | **Intent**: semantic_near_miss

**Root Cause**: Heavy truncation and missing structured content in scraped pages prevented extraction of vaccine names and doses, despite good coverage and acceptable ranking.

- **Coverage Diagnosis**: All must-mention terms (CDC, adult immunization schedule, vaccine doses) were found in the search results; coverage is not the issue.
- **Ranking Diagnosis**: The child immunization schedule page was ranked above the adult easy-read CDC page, which is suboptimal for an adult-focused query. Otherwise, official CDC sources were prioritized over non-authoritative domains.
- **Scrape Diagnosis**: Scraped markdown suffered from severe truncation (documents end abruptly), missing vaccine tables, and malformed table rows, especially on CDC schedule pages. The most relevant pages lacked complete structured data on vaccine names and dose counts.

**Fix Actions**:
- Enhance scraping of CDC immunization pages to handle dynamic content, long pages, and table extraction, preventing truncation and ensuring full capture of schedule data.
- Implement query-aware result reranking: demote child-related CDC pages when the query explicitly mentions 'adults' to keep adult-focused pages higher.
- Improve markdown conversion fidelity for complex tables on CDC pages to preserve structured vaccine name and dose information, possibly using AI-driven table extraction.


---
### tc_121ff7e0 (Score: 0.78) ❌
**Query**: `ENSO status July 2026 NOAA Climate Prediction Center sea surface temperature anomalies forecast table`
**Category**: rapidly_changing | **Intent**: novel

**Root Cause**: Relevant pages were found, but the most authoritative and table-rich CPC advisory page (result 3) was not ranked first, and critical forecast tables and charts are embedded as images, preventing extraction of structured data.

- **Coverage Diagnosis**: Coverage is perfect: all expected terms ('El Niño Southern Oscillation', 'NOAA', 'Climate Prediction Center') were found in titles, snippets, or content previews.
- **Ranking Diagnosis**: Firecrawl ranked the CPC PDF (result 1) highest, but the official advisory discussion page (result 3) is more specific, up-to-date, and directly contains (image-based) forecast tables. The CPC homepage (result 4) should rank above IRI (result 2), and the Facebook post (result 5) should be last due to low authority.
- **Scrape Diagnosis**: Key CPC pages (results 1,3,4) and IRI (result 2) present critical forecast tables and probability charts only as images or links, resulting in missing structured data, truncation, and low scrape quality scores (0.4–0.6). The Facebook post (result 5) has perfect scrape quality but is irrelevant.

**Fix Actions**:
- Adjust ranking signals to boost 'ENSO Diagnostic Discussion' pages and demote PDF snapshots and low-authority social media for data extraction queries.
- Implement OCR or image-table extraction in the scraper to parse embedded images into structured data (tables, charts) on CPC and IRI pages.
- Add domain-specific parsing for NOAA CPC to follow links to text versions or downloadable data files (e.g., CSV, Excel) when direct table extraction from the page fails.


---
### tc_11afc8cd (Score: 0.75) ❌
**Query**: `Singapore Airlines A380 vs Emirates A380 vs Qatar A350 economy seat size chart 2026`
**Category**: structured_data_extraction | **Intent**: novel

**Root Cause**: Search results lacked pages containing a direct seat size comparison chart for the three airlines, relying on news articles and partial official pages that do not provide structured data, leading to poor extraction despite high coverage and scrape quality.

- **Coverage Diagnosis**: Airline brand terms were present, but no result included the expected comprehensive comparison table with seat pitch, width, and layout for all three aircraft, leaving the structured data intent unmet.
- **Ranking Diagnosis**: The SeatCompare.ai guide (ranked 4th) was more specific to seat selection but ranked below general news; the absence of dedicated comparison sites like SeatGuru caused the overall ranking to miss the most relevant sources.
- **Scrape Diagnosis**: All markdown outputs were clean with no formatting or noise issues, but they lacked the necessary structured seat dimension data for a comparative chart.

**Fix Actions**:
- Integrate seatguru.com and similar comparison databases that offer tabular seat size data across multiple airlines.
- Boost official airline seat map and fleet detail pages (e.g., singaporeair.com, emirates.com) to surface authoritative seat dimensions.
- Adjust ranking to prefer pages with clear tabulated data and comparative analytics over general news articles.


---
### tc_8abf90d2 (Score: 0.73) ❌
**Query**: `2026 Human Development Index country rankings life expectancy education and GNI per capita`
**Category**: structured_data_extraction | **Intent**: novel

**Root Cause**: Search ranking did not prioritize the official UNDP HDR page, and scraping failed to extract expected data tables and country rankings from top results, reducing overall quality for structured data extraction.

- **Coverage Diagnosis**: All required terms (UNDP, Human Development Index, GNI per capita) were found across results, so coverage is not an issue.
- **Ranking Diagnosis**: Firecrawl ranked Wikipedia first (general reference) and worldpopulationreview.com second (explicit 2026 data), whereas the ideal ranking places the official UNDP HDR page first and the 2026-specific page second, prioritizing authority and temporal relevance.
- **Scrape Diagnosis**: Multiple top results are missing expected data tables and country ranking lists, with truncation (e.g., Wikipedia cut off at 'New method (2010 HDI o...', worldpopulationreview at 'Andorra ... Very H'), and noise (video embed on UNDP page), preventing extraction of structured HDI data.

**Fix Actions**:
- Adjust ranking signals to boost official sources (e.g., undp.org) for authoritative data queries like HDI, and consider temporal signals for explicit year mentions (2026).
- Enhance scraper to detect and extract structured tables (HTML <table>) as markdown tables or JSON arrays when data extraction intent is detected, avoiding reliance on raw markdown conversion.
- Increase scraping depth or use dynamic content rendering to capture full page content and avoid truncation for data-heavy pages (e.g., paginated lists).


---
### tc_5ac84dfe (Score: 0.78) ❌
**Query**: `list of recommended vaccines for adults in 2026 from CDC with number of doses`
**Category**: structured_data_extraction | **Intent**: semantic_near_miss

**Root Cause**: Ranking prioritized supplementary notes and an irrelevant child schedule over the most direct adult vaccine lists, and truncation on the best easy-read list obscured complete dose information.

- **Coverage Diagnosis**: Coverage was perfect; all expected terms (CDC, adult immunization schedule, vaccine doses) were present in the results.
- **Ranking Diagnosis**: The ideal ranking places the adult schedule by age first and the easy-read adult list second, as they directly answer the query with vaccine doses. Firecrawl ranked the notes page first (supplementary) and the child schedule third (irrelevant), while the easy-read list was fourth despite being highly relevant.
- **Scrape Diagnosis**: Multiple pages suffered from truncation, particularly the easy-read adult list (rank 4) which missed the end of the HPV row, reducing its completeness for extracting all doses. The notes page (rank 1) was also truncated, missing end of content. The child schedule was truncated but less relevant.

**Fix Actions**:
- Adjust ranking to boost pages that combine 'adult' with 'schedule' or 'recommended vaccinations' in titles, especially the easy-read and by-age pages, to top positions.
- Implement domain filtering to exclude non-CDC sources when the query explicitly requests CDC information.
- Increase the scraping character limit or use chunked scraping to prevent truncation of long pages containing vaccine lists.


---
### tc_eb136550 (Score: 0.76) ❌
**Query**: `Amazon deforestation rate 2026 INPE PRODES vs GLAD University of Maryland hectares per year`
**Category**: rapidly_changing | **Intent**: novel

**Root Cause**: Search results missed the critical term 'PRODES', the INPE program specifically tracking deforestation, preventing a complete comparative analysis.

- **Coverage Diagnosis**: Expected term 'PRODES' not found in any snippet or content; only 'INPE' appeared, without its specific deforestation monitoring program.
- **Ranking Diagnosis**: Ranking was ideal (score 1.0) based on source priority and freshness, so no divergence from ideal ranking.
- **Scrape Diagnosis**: Several results had missing data tables, charts, or truncation, limiting extraction of exact deforestation rates, but coverage was the primary failure.

**Fix Actions**:
- Enhance query expansion to explicitly map 'INPE' to synonyms like 'PRODES' for deforestation searches.
- Add official INPE PRODES dashboard and GLAD data portals to the crawl index with high priority.
- Improve scraping of tabular data and image-based charts to extract precise hectare figures.


---
### tc_107f793b (Score: 0.74) ❌
**Query**: `what are the recommended adult vaccines for 2026 and how many doses do you need`
**Category**: structured_data_extraction | **Intent**: semantic_near_miss

**Root Cause**: Firecrawl's ranking model failed to prioritize the authoritative adult immunization schedule by age (result 2) over supplementary notes (result 1) and did not adequately demote off-topic child content (result 3), leading to suboptimal ordering.

- **Coverage Diagnosis**: Coverage was perfect; all expected terms (CDC, adult immunization schedule, vaccine names) were present in the results.
- **Ranking Diagnosis**: The ideal ranking places the age-based schedule first, as it directly answers the query with structured dose information, while the notes page is supplementary. Firecrawl incorrectly ranked the notes first. Additionally, the child immunization schedule and a news article were not sufficiently demoted, allowing them to appear above the more relevant adult easy-read page.
- **Scrape Diagnosis**: Result 1 had severe scrape issues (missing data tables, truncation), and result 4 had truncation. These quality signals may not have been effectively used to adjust rankings, contributing to the notes page outranking the cleaner, more relevant age-based schedule.

**Fix Actions**:
- Enhance the ranking model to prioritize primary authoritative schedule pages (e.g., by age) over secondary notes for queries seeking immunization schedules.
- Improve query intent detection to filter out content focused on child immunization when the query explicitly specifies 'adult'.
- Incorporate scrape quality signals (completeness, presence of expected tables) more aggressively to demote pages with missing elements or truncation.


---
### tc_de5e4df4 (Score: 0.70) ❌
**Query**: `QS World University Rankings 2026 engineering top 50 list`
**Category**: structured_data_extraction | **Intent**: novel

**Root Cause**: Scraping failed to extract ranking data from dynamic pages, resulting in incomplete or missing content despite high relevance of search results.

- **Coverage Diagnosis**: All expected terms ('QS_World_University_Rankings', 'engineering_and_technology', 'MIT') were found, so coverage is not an issue.
- **Ranking Diagnosis**: Ranking diverged because result 1 (general subject rankings) ranked above result 2 (specific engineering-technology page), and result 3 (Times Higher Education) ranked above result 4 (QS sub-discipline), which is more specific and from the preferred source. Result 5 (Wikipedia) was included but is not an official QS source and lacks the requested ranking list.
- **Scrape Diagnosis**: All scrapes suffered from missing elements due to lazy-loaded ranking tables, truncated markdown (incomplete content), and noise from filter UI and repeated content, severely limiting extractable data.

**Fix Actions**:
- Enable JavaScript rendering for known dynamic sites like topuniversities.com and timeshighereducation.com to load full ranking tables.
- Increase scrape depth and implement pagination handling to capture complete top-50 lists without truncation.
- Adjust ranking to prioritize pages with more specific query matches (e.g., 'engineering-technology' over 'subject-rankings') and demote non-authoritative sources like Wikipedia for data extraction tasks.


---
### tc_f7ea9535 (Score: 0.74) ❌
**Query**: `Rust async runtime tokio vs monoio vs smol performance benchmark 2026`
**Category**: structured_data_extraction | **Intent**: novel

**Root Cause**: The failure resulted from suboptimal ranking that prioritized a casual Reddit discussion over a dedicated benchmark article and a GitHub issue, combined with poor scrape quality that omitted structured elements like benchmark tables and code snippets across most results.

- **Coverage Diagnosis**: Coverage was perfect; all expected entities (tokio, smol, monoio) were found, and no key terms were missed.
- **Ranking Diagnosis**: Firecrawl ranked the Reddit thread first, but ideal ranking places the Rustify article (rank 2) and GitHub issue (rank 4) higher due to better alignment with benchmark methodology and source priorities. The ranking model undervalued content authority and structural relevance for comparative research.
- **Scrape Diagnosis**: Scrape issues affected four of five results: Rustify article truncated, corrode.dev and GitHub issue missing expected benchmark tables, YouTube video offering only transcript text, and GitHub issue lacking proper code snippets. These omissions degraded structured data extraction.

**Fix Actions**:
- Tune ranking to prioritize dedicated benchmark articles and GitHub issues/discussions over forums and videos for comparative research queries.
- Enhance scraping fidelity to capture full article content, preserve table structures, and retain code blocks with correct formatting.
- Implement content-type signals to demote casual discussion and video sources when structured data extraction is intended.


---
### tc_9222e13d (Score: 0.73) ❌
**Query**: `California Advanced Clean Fleets regulation 2026 compliance deadlines for public fleet zero-emission vehicle purchase requirements`
**Category**: pdf_document | **Intent**: novel

**Root Cause**: The overall score is reduced primarily due to poor scrape quality across multiple results, including missing data tables, charts, footnotes, and noise like cookie banners, despite near-perfect coverage and ranking.

- **Coverage Diagnosis**: All required terms ('California Air Resources Board', 'Advanced Clean Fleets', 'zero-emission vehicle') were present in the search results, so no coverage issues detected.
- **Ranking Diagnosis**: A minor swap occurred between positions 3 and 4; the ideal ranking prioritized pages with explicit 2026 deadlines (RMI and TerraVerde) over TRC, which listed more generic dates. Firecrawl's ranking nearly matched, but TRC was placed slightly too high.
- **Scrape Diagnosis**: Multiple scrape issues degraded quality: missing data tables, compliance schedule charts, and footnote definitions in all results; noise from cookie consent banners; and content truncation (e.g., RMI snippet cut off). This limits the ability to extract precise 2026 compliance deadlines.

**Fix Actions**:
- Enhance table and chart extraction from PDF/HTML to capture structured compliance data, including embedded images with text alternative parsing.
- Implement content completeness checks to prevent truncation and ensure full document scraping, especially for long regulatory pages.
- Add post-processing to filter out noise elements like cookie consent banners and improve markdown cleanliness for downstream extraction.


---
