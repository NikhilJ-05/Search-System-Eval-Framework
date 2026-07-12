# Test Case Report: tc_ec3ed7e2 (🔴 FAILED)

## Metadata
- **Query**: `Largest sovereign wealth fund by AUM 2026 and its top holdings with allocation percentages`
- **Category**: Finance & Investing
- **Intent**: data_extraction
- **Difficulty**: hard
- **Overall Score**: 0.568
- **Floor Failures**: multi_hop_synthesis, data_completeness, _baseline_fidelity (Score < 0.40)

## Cache Behavior
- **Query Cache**: miss
- **Content Cache Per Result**:
  - `https://www.swfinstitute.org/fund-rankings/sovereign-wealth-fund`: miss
  - `https://www.ssga.com/us/en/institutional/insights/trends-among-sovereign-wealth-funds`: miss
  - `https://globalswf.com/ranking`: miss
  - `https://praxisrock.com/resources/investors/sovereign-wealth-funds`: miss
  - `https://www.bain.com/insights/the-future-of-sovereign-wealth-funds-four-imperatives-for-the-next-decade/`: miss

## Judge Evaluation Details
### 1. _baseline_ranking (Score: 0.75, Level: L4) ✅
- **Weight**: 0.12
- **Reasoning**: The baseline ranking is adequate. The highest-authority and most relevant source (SWFI, rank 1) is correctly placed. A minor reordering between ranks 2 and 3 (SSGA blog vs Global SWF) is slightly suboptimal but not a critical error. The most relevant results are not buried, and no blog ranks above an official source. Overall, the ranking satisfies the criteria at an adequate level.
- **Level Justification**: The ranking broadly follows authority and relevance ordering: the top source has the highest authority and good relevance; lower-ranked sources decrease in relevance and authority. A slight misplacement (Document 2 at rank 2 over Document 3) does not degrade the overall order enough to fall below 'Adequate'. The contrastive fail condition is not triggered, so L4 is appropriate.
- **Contrastive Fail Triggered**: No

### 2. multi_hop_synthesis (Score: 0.30, Level: L2) ❌
- **Weight**: 0.28
- **Reasoning**: The documents successfully identify Norway's Government Pension Fund Global as the largest SWF by AUM in 2026 (from SWF Institute, Global SWF, and Praxis Rock). However, none of the documents provide any list of top holdings or allocation percentages for that fund. The query's multi-hop synthesis requirement is only one-third fulfilled, resulting in a major deficiency.
- **Level Justification**: Only one of three reasoning layers is covered (identifying the largest fund). The critical layers of top holdings and allocation percentages are completely absent from all documents. This constitutes a major deficiency, not a critical failure because the first layer is well-supported by multiple authoritative sources.
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: The documents collectively identify the largest fund (layer 1 completed) but provide no holdings list (layer 2) or allocation percentages (layer 3). This matches the contrastive fail condition: 'Results identify the largest fund but provide no holdings list'.

### 3. _baseline_fidelity (Score: 0.70, Level: L4) ✅
- **Weight**: 0.12
- **Reasoning**: The scraped markdown across all documents is largely faithful to the original pages. Structural elements like tables and headings are preserved. Minor boilerplate and hidden interactive elements exist in some documents but do not significantly impair content extraction or interpretation. No critical scraping failures are present.
- **Level Justification**: The scraping quality is generally adequate across the document set. Most documents (2,3,4) have high-fidelity scrapes with minor issues. Doc1 and Doc5 have moderate issues but still preserve the main content. The contrastive failure condition is not triggered. Overall, the baseline fidelity is adequate for coverage evaluation.
- **Contrastive Fail Triggered**: No

### 4. source_authority (Score: 0.75, Level: L4) ✅
- **Weight**: 0.21
- **Reasoning**: The retrieved documents come from authoritative sources like the Sovereign Wealth Fund Institute, State Street Global Advisors, and Global SWF, which are recognized in the SWF data space. Two additional sources (Praxis Rock, Bain) have moderate authority but are not low-quality. No SEO listicles or content farms are present. The absence of official fund disclosures prevents a higher score, but the overall authority is solidly adequate for the query.
- **Level Justification**: The collection includes highly authoritative sources (SWF Institute authority_score=0.9, SSGA authority_score=0.9, Global SWF authority_score=0.85) that are recognized for SWF data. Two moderately authoritative sources (Praxis Rock 0.7, Bain 0.7) are present but do not dominate the results. No official fund disclosures are provided, which would be needed for the highest level of authority on holdings and allocations. The overall authority is adequate but not excellent due to the lack of official disclosures and the inclusion of moderate-authority commercial sources.
- **Contrastive Fail Triggered**: No

### 5. _baseline_freshness (Score: 0.90, Level: L5) ✅
- **Weight**: 0.07
- **Reasoning**: The majority of documents are explicitly dated to 2026, and all documents contain data that is current for the 2026 query time frame. The query's time-sensitivity is fully satisfied by the retrieved content, with no evidence of outdated information.
- **Level Justification**: The collection includes several documents with explicit 2026 dates (State Street March 2026, Global SWF July 2026, Praxis Rock April 2026) and the remaining documents cover recent 2025-2026 data. No temporally inappropriate or outdated content is present. The temporal freshness is excellent across the set.
- **Contrastive Fail Triggered**: No

### 6. data_completeness (Score: 0.30, Level: L2) ❌
- **Weight**: 0.21
- **Reasoning**: The retrieved documents collectively identify the largest sovereign wealth fund (Norway Government Pension Fund Global / NBIM) and provide its AUM in multiple sources (ranging from $2.048 trillion to $2.1 trillion). However, no document includes any information about the fund's top holdings (individual securities or asset classes) with allocation percentages. This critical gap means the query's data completeness requirement is not met. The contrastive fail is triggered because the results mention the fund name and vague allocation categories but lack the specific named holdings list and percentages required.
- **Level Justification**: The collective evidence partially satisfies the query by identifying the largest sovereign wealth fund and providing its AUM, but critically fails to deliver the required top holdings list with allocation percentages. This constitutes a major deficiency (L2) because the core requirement—specific numerical data on holdings and allocations—is entirely missing. The presence of the fund name and AUM prevents this from being a critical failure (L1), but the absence of holdings data means it cannot reach even a partial level (L3).
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: The results identify the fund name (Norway GPFG/NBIM) and reference broad asset categories (e.g., alternatives allocation of 2% from Document 3), but fail to provide a specific named holdings list with concrete percentage figures, which is exactly the contrastive fail scenario.

### 7. _baseline_fidelity (Score: 0.26, Level: L2) ❌
- **Weight**: 0.12
- **Reasoning**: Aggregated fidelity score from 5 pages.
- **Level Justification**: Computed average score is 0.26
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: Average scrape quality is poor

### Document Profiles Evaluated
| Rank | URL | Domain Type | Words | Headings | Tables | Completeness |
|------|-----|-------------|-------|----------|--------|--------------|
| 1 | https://www.swfinstitute.org/fund-rankings/sovereign-wealth-fund | N/A | 0 | 0 | 0 | unknown |
| 2 | https://www.ssga.com/us/en/institutional/insights/trends-among-sovereign-wealth-funds | N/A | 0 | 0 | 0 | unknown |
| 3 | https://globalswf.com/ranking | N/A | 0 | 0 | 0 | unknown |
| 4 | https://praxisrock.com/resources/investors/sovereign-wealth-funds | N/A | 0 | 0 | 0 | unknown |
| 5 | https://www.bain.com/insights/the-future-of-sovereign-wealth-funds-four-imperatives-for-the-next-decade/ | N/A | 0 | 0 | 0 | unknown |


## Failure Diagnosis & Recovery Roadmap
- **Failure Dimensions**: `multi_hop_synthesis, data_completeness, _baseline_fidelity (Critical: multi_hop_synthesis, data_completeness, _baseline_fidelity)`
- **Root Cause**: All five retrieved documents (swfinstitute.org, ssga.com, globalswf.com, praxisrock.com, bain.com) identify Norway's GPFG as the largest SWF but none contain its top holdings or allocation percentages, as evidenced by Doc1's critical content gap 'Top holdings and allocation percentages for the largest fund are not provided' and Doc3's gap 'No specific top holdings or allocation percentages beyond alternatives and domestic categories.' The retrieval system failed to surface NBIM's official holdings report at nbim.no, which is the only authoritative source for this data.

### Diagnostic Breakdown
- **Coverage Diagnosis**: Two of three query components are completely uncovered: (1) top holdings of the largest fund and (2) allocation percentages for those holdings. All five document profiles show coverage_level=tangential or partial with answers_query=false. The system retrieved SWF ranking pages and trend analyses but missed the official fund disclosure page that lists individual holdings with percentages.
- **Ranking Diagnosis**: N/A — ranking scored 0.75 (L4) with no contrastive fail; the issue is coverage, not ordering.
- **Scrape Diagnosis**: Doc1 (swfinstitute.org, scrape_score=0.4) has asset values hidden behind interactive 'View Total Assets' elements, and Doc2 (ssga.com, scrape_score=0.2) has chart data not extracted as text. These are secondary issues; the aggregated fidelity score of 0.256 reflects generally poor scrape quality across the set but does not account for the primary coverage failure.

### Recommended Fix Actions
- Add nbim.no and its holdings report subpages (e.g., nbim.no/en/the-fund/holdings/holdings-and-equity-trades/) to the crawl seed list and boost their domain authority weight in the ranking model for queries mentioning 'holdings' or 'allocation percentages' alongside sovereign wealth fund names.
- Implement a query decomposition step that splits multi-hop queries into sub-queries (e.g., 'largest sovereign wealth fund by AUM 2026' AND 'Norway GPFG top holdings allocation percentages') and merges results, ensuring the second hop retrieves official fund disclosure pages rather than only ranking databases.
- Configure the scraper to execute JavaScript interactions on swfinstitute.org fund-ranking pages to expand hidden 'View Total Assets' cells, and add OCR/chart-extraction for ssga.com embedded infographics to improve scrape fidelity from 0.2-0.4 to acceptable levels.
