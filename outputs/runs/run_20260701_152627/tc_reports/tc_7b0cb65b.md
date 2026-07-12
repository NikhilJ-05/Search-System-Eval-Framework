# Test Case Report: tc_7b0cb65b (🔴 FAILED)

## Metadata
- **Query**: `what vaccines do adults need in 2026 according to the CDC schedule and how many doses each`
- **Category**: structured_data_extraction
- **Intent**: factual_lookup
- **Difficulty**: easy
- **Overall Score**: 0.650

## Cache Behavior
- **Query Cache**: miss
- **Content Cache Per Result**:
  - `https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-notes.html`: stale
  - `https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-age.html`: stale
  - `https://www.cdc.gov/vaccines/hcp/imz-schedules/child-adolescent-notes.html`: miss
  - `https://www.cdc.gov/vaccines/imz-schedules/adult-easyread.html`: stale
  - `https://www.cidrap.umn.edu/childhood-vaccines/hhs-announces-unprecedented-overhaul-us-childhood-vaccine-schedule`: miss

## Judge Evaluation Details
### 1. Coverage (Score: 1.00)
- **Must Mention Found**: CDC, adult immunization schedule, vaccine doses
- **Must Mention Missed**: None
- **Judge Reasoning**: Found 'CDC' in title and content of multiple results, e.g., result 1 title 'Adult Immunization Schedule Notes | Vaccines & Immunizations - CDC'. Found 'adult immunization schedule' in result 1 title and content preview. Found 'vaccine doses' in result 1 snippet '1 dose'. All must_mention items present.

### 2. Ranking (Score: 0.87)
- **Firecrawl Ranking**: [1, 2, 3, 4, 5]
- **LLM Ideal Ranking**: [1, 2, 4, 3, 5]
- **Judge Reasoning**: The first two results are from the primary authoritative source (cdc.gov) and directly address adult schedules; the third result is also cdc.gov but for children, which is off-topic; the fourth is CDC adult easy-read, still relevant; the fifth is from non-authoritative cidrap.umn.edu and not a primary source. According to source priority, all CDC.gov pages should rank before non-CDC domains. The child schedule (rank 3) should be deprioritized below adult-focused CDC pages. Muninn.edu with HHS news should be last.
- **Ranking Suggestions**:
  - Filter or demote non-adult CDC pages (e.g. child schedule) when query asks for adult vaccines.
  - Boost pages explicitly matching 'adult immunization schedule' in the title.
  - Ensure non-authoritative news articles (e.g. cidrap.umn.edu) are ranked below official sources.

### 3. Scrape Quality Per Result
| URL | Noise Score | Structure Score | Completeness | Overall Quality | Issues Found |
|-----|-------------|-----------------|--------------|-----------------|--------------|
| https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-notes.html | 0.30 | 0.20 | 0.20 | **0.20** | missing_element (high), truncation (high) |
| https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-age.html | 0.40 | 0.50 | 0.15 | **0.30** | formatting_issue (medium), truncation (high) |
| https://www.cdc.gov/vaccines/hcp/imz-schedules/child-adolescent-notes.html | 0.30 | 0.30 | 0.05 | **0.10** | irrelevant_content (high), truncation (high) |
| https://www.cdc.gov/vaccines/imz-schedules/adult-easyread.html | 0.20 | 0.70 | 0.10 | **0.40** | truncation (high) |
| https://www.cidrap.umn.edu/childhood-vaccines/hhs-announces-unprecedented-overhaul-us-childhood-vaccine-schedule | 0.50 | 0.60 | 0.90 | **0.20** | irrelevant_content (high) |

## Failure Diagnosis & Recovery Roadmap
- **Failure Dimensions**: `scrape`
- **Root Cause**: Heavy truncation and missing structured content in scraped pages prevented extraction of vaccine names and doses, despite good coverage and acceptable ranking.

### Diagnostic Breakdown
- **Coverage Diagnosis**: All must-mention terms (CDC, adult immunization schedule, vaccine doses) were found in the search results; coverage is not the issue.
- **Ranking Diagnosis**: The child immunization schedule page was ranked above the adult easy-read CDC page, which is suboptimal for an adult-focused query. Otherwise, official CDC sources were prioritized over non-authoritative domains.
- **Scrape Diagnosis**: Scraped markdown suffered from severe truncation (documents end abruptly), missing vaccine tables, and malformed table rows, especially on CDC schedule pages. The most relevant pages lacked complete structured data on vaccine names and dose counts.

### Recommended Fix Actions
- Enhance scraping of CDC immunization pages to handle dynamic content, long pages, and table extraction, preventing truncation and ensuring full capture of schedule data.
- Implement query-aware result reranking: demote child-related CDC pages when the query explicitly mentions 'adults' to keep adult-focused pages higher.
- Improve markdown conversion fidelity for complex tables on CDC pages to preserve structured vaccine name and dose information, possibly using AI-driven table extraction.
