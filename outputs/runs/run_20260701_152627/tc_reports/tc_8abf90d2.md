# Test Case Report: tc_8abf90d2 (🟢 PASSED)

## Metadata
- **Query**: `2026 Human Development Index country rankings life expectancy education and GNI per capita`
- **Category**: structured_data_extraction
- **Intent**: data_extraction
- **Difficulty**: easy
- **Overall Score**: 0.733

## Cache Behavior
- **Query Cache**: miss
- **Content Cache Per Result**:
  - `https://en.wikipedia.org/wiki/Human_Development_Index`: miss
  - `https://worldpopulationreview.com/country-rankings/hdi-by-country`: miss
  - `https://hdr.undp.org/data-center/human-development-index`: miss
  - `https://ourworldindata.org/grapher/human-development-index`: miss
  - `https://www.facebook.com/TheEconomist/posts/after-two-years-at-the-top-switzerland-has-been-edged-out-in-the-human-developme/1157865899705262/`: miss

## Judge Evaluation Details
### 1. Coverage (Score: 1.00)
- **Must Mention Found**: UNDP, Human Development Index, GNI per capita
- **Must Mention Missed**: None
- **Judge Reasoning**: Must-mention 'UNDP': found in result 3, content_preview 'https://hdr.undp.org'. 'Human Development Index': found in multiple titles and snippets. 'GNI per capita': found in result 1 snippet 'gross national income GNI (PPP) per capita'. All must-mention items are present, meeting the min expected of 2.

### 2. Ranking (Score: 0.81)
- **Firecrawl Ranking**: [1, 2, 3, 4, 5]
- **LLM Ideal Ranking**: [3, 2, 1, 4, 5]
- **Judge Reasoning**: Moved hdr.undp.org (result 3) to rank 1 due to official source priority. Moved worldpopulationreview.com (result 2) to rank 2 for its explicit 2026 data. Wikipedia and Our World in Data follow as secondary sources; Facebook post is least relevant.
- **Ranking Suggestions**:
  - Prioritize official UNDP HDR page
  - Consider World Bank or other authoritative aggregators for HDI data
  - Check date freshness for 2026 projection accuracy

### 3. Scrape Quality Per Result
| URL | Noise Score | Structure Score | Completeness | Overall Quality | Issues Found |
|-----|-------------|-----------------|--------------|-----------------|--------------|
| https://en.wikipedia.org/wiki/Human_Development_Index | 0.20 | 0.70 | 0.30 | **0.40** | missing_element (high), missing_element (high), truncation (medium) |
| https://worldpopulationreview.com/country-rankings/hdi-by-country | 0.00 | 0.80 | 0.50 | **0.70** | truncation (medium) |
| https://hdr.undp.org/data-center/human-development-index | 0.10 | 0.50 | 0.40 | **0.30** | missing_element (high), missing_element (high), noise (low) |
| https://ourworldindata.org/grapher/human-development-index | 0.00 | 0.80 | 0.40 | **0.60** | missing_element (medium), truncation (medium) |
