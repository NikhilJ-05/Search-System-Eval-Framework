# Test Case Report: tc_bd1bd260 (🔴 FAILED)

## Metadata
- **Query**: `global average temperature anomaly 2026 year to date NOAA NASA GISS Berkeley Earth`
- **Category**: rapidly_changing
- **Intent**: real_time
- **Difficulty**: easy
- **Overall Score**: 0.649

## Cache Behavior
- **Query Cache**: miss
- **Content Cache Per Result**:
  - `https://berkeleyearth.org/march-2026-temperature-update/`: miss
  - `https://science.nasa.gov/earth/earth-observatory/world-of-change/global-temperatures/`: miss
  - `https://berkeleyearth.org/data/`: miss
  - `https://psl.noaa.gov/data/timeseries/month/DS/BERKELEYGLBLT/`: miss
  - `https://berkeleyearth.org/global-temperature-report-for-2025/`: miss

## Judge Evaluation Details
### 1. Coverage (Score: 0.67)
- **Must Mention Found**: NOAA, Berkeley_Earth
- **Must Mention Missed**: NASA_GISS
- **Judge Reasoning**: Found 'NOAA' in result 4 snippet: 'NOAA Global Temperature dataset'. Found 'Berkeley_Earth' in results 1,3,4,5. 'NASA_GISS' not found exactly in any result.

### 2. Ranking (Score: 0.60)
- **Firecrawl Ranking**: [1, 4, 5, 2, 3]
- **LLM Ideal Ranking**: [4, 1, 5, 2, 3]
- **Judge Reasoning**: Source priority places NASA GISS and NOAA first, but no GISS results appear. Berkeley Earth should rank after official sources. Result 2 (NASA) is out of date for 2026; Result 1 (Berkeley Earth) is the only one with 2026 data but from a secondary source. Ideal: First, the NOAA PSL Berkeley Earth anomaly dataset (Result 4) because it directly provides NOAA-official data for 2026 although tied to Berkeley Earth; then Result 1 (independent 2026 update); then Result 5 (2025 report). Result 3 is a data overview page, less relevant. Result 2 is outdated (2025).
- **Ranking Suggestions**:
  - Add direct NASA GISS global temperature anomaly page for 2026
  - Include NOAA NCEI global climate report for 2026 year-to-date

### 3. Scrape Quality Per Result
| URL | Noise Score | Structure Score | Completeness | Overall Quality | Issues Found |
|-----|-------------|-----------------|--------------|-----------------|--------------|
| https://berkeleyearth.org/march-2026-temperature-update/ | 0.00 | 0.90 | 0.60 | **0.70** | missing_element (high), truncation (medium) |
| https://science.nasa.gov/earth/earth-observatory/world-of-change/global-temperatures/ | 0.10 | 0.70 | 0.20 | **0.30** | missing_element (high), irrelevant_content (high) |
| https://berkeleyearth.org/data/ | 0.00 | 0.90 | 0.90 | **0.80** | missing_element (medium) |
| https://psl.noaa.gov/data/timeseries/month/DS/BERKELEYGLBLT/ | 0.00 | 0.90 | 0.90 | **0.85** | missing_element (medium) |
| https://berkeleyearth.org/global-temperature-report-for-2025/ | 0.00 | 0.90 | 0.60 | **0.75** | missing_element (high), truncation (medium) |

## Failure Diagnosis & Recovery Roadmap
- **Failure Dimensions**: `coverage, ranking, scrape`
- **Root Cause**: The search missed the NASA GISS source required by the query, and ranking over‑prioritized a secondary Berkeley Earth update over the official NOAA‑hosted dataset, while scraping failed to extract structured data tables from most pages.

### Diagnostic Breakdown
- **Coverage Diagnosis**: Expected source 'NASA_GISS' was not found in any result. Only NOAA and Berkeley Earth were covered. Result 2 (NASA) is outdated (2025) and not from GISS, while the query explicitly asks for NASA GISS 2026 anomaly data.
- **Ranking Diagnosis**: Firecrawl ranked the recent Berkeley Earth update (result 1) first, but the ideal ranking places the NOAA PSL dataset (result 4) first because it represents an official source. The query prioritizes official NOAA/NASA data, yet the ranking favored a secondary analysis over the official NOAA repository.
- **Scrape Diagnosis**: Results 1, 4, 5 lacked expected data tables; truncation cut off content in results 1 and 5; result 2 contained mostly navigation and irrelevant highlights. Scraped markdown failed to capture structured numerical data and time‑series charts, reducing informativeness for the query.

### Recommended Fix Actions
- Include NASA GISS global temperature anomaly page (e.g., data.giss.nasa.gov/gistemp/) in the index to cover the missing source.
- Boost ranking of official data repositories (NOAA PSL, NASA GISS) when query contains explicit organization names like 'NOAA' or 'NASA GISS'.
- Enhance scraping to retain data tables, increase truncation limits, and better parse pages to capture structured numerical content.
