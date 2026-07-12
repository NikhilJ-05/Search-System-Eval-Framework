# Test Case Report: tc_11afc8cd (🟢 PASSED)

## Metadata
- **Query**: `Singapore Airlines A380 vs Emirates A380 vs Qatar A350 economy seat size chart 2026`
- **Category**: structured_data_extraction
- **Intent**: comparative_research
- **Difficulty**: hard
- **Overall Score**: 0.753

## Cache Behavior
- **Query Cache**: miss
- **Content Cache Per Result**:
  - `https://simpleflying.com/the-airlines-with-the-worlds-most-spacious-economy-seats-in-2026/`: miss
  - `https://www.qatarairways.com/en/fleet/airbus-a350.html`: miss
  - `https://www.reddit.com/r/qatarairways/comments/1qy09s0/is_it_worth_taking_a_very_early_flight_just_to/`: miss
  - `https://seatcompare.ai/insights/qatar-airways-a380-seat-guide`: miss
  - `https://www.facebook.com/simpleflyingnews/posts/2026s-thickest-a380-routes-are-dominated-by-emirates-with-singapore-airlines-and/1546137390864387/`: miss

## Judge Evaluation Details
### 1. Coverage (Score: 1.00)
- **Must Mention Found**: Singapore_Airlines, Emirates, Qatar_Airways
- **Must Mention Missed**: None
- **Judge Reasoning**: Found Singapore_Airlines in result 1 snippet ('Singapore Airlines A380'), Emirates in result 5 title, and Qatar_Airways in result 2 title and content preview.

### 2. Ranking (Score: 0.90)
- **Firecrawl Ranking**: [1, 2, 3, 4, 5]
- **LLM Ideal Ranking**: [2, 4, 1, 3, 5]
- **Judge Reasoning**: Swap 1: result 2 (qatarairways.com, official) should be first per source priority. Swap 2: result 4 (seatcompare.ai, relevant seat guide) over result 1 (simpleflying.com, news) because it's more specific to seat charts. Swap 3: result 1 over result 3 (reddit) because it provides actual seat dimensions. Swap 4: result 3 over result 5 (facebook) due to slightly better relevance.
- **Ranking Suggestions**:
  - Add results from seatguru.com for comprehensive seat size comparison
  - Include official seat maps from singaporeair.com and emirates.com
  - Ensure recent 2026 data is available from official sources

### 3. Scrape Quality Per Result
| URL | Noise Score | Structure Score | Completeness | Overall Quality | Issues Found |
|-----|-------------|-----------------|--------------|-----------------|--------------|
| url_1 | 0.90 | 0.00 | 0.00 | **0.00** | missing_element (high), missing_element (high), missing_element (high) |
| url_2 | 0.60 | 0.80 | 1.00 | **0.70** | missing_element (medium), noise_risk (medium), noise_risk (medium) |
| url_3 | 0.10 | 0.90 | 0.70 | **0.70** | missing_element (low), completeness_issue (medium) |
