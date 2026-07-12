# Test Case Report: tc_8ad5c14e (🟢 PASSED)

## Metadata
- **Query**: `how many grams of added sugar per day does FDA recommend in 2026 for adults`
- **Category**: structured_data_extraction
- **Intent**: factual_lookup
- **Difficulty**: easy
- **Overall Score**: 0.876

## Cache Behavior
- **Query Cache**: hit
- **Content Cache Per Result**:
  - `https://www.fda.gov/food/nutrition-facts-label/added-sugars-nutrition-facts-label`: kb_semantic_hit
  - `https://www.cdc.gov/nutrition/php/data-research/added-sugars.html`: kb_semantic_hit
  - `https://www.facebook.com/FDA/posts/the-new-dietary-guidelines-for-americans-recommend-limiting-added-sugars-to-supp/1322126489944706/`: miss
  - `https://nutritionsource.hsph.harvard.edu/carbohydrates/added-sugar-in-the-diet/`: kb_semantic_hit
  - `https://www.heart.org/en/healthy-living/healthy-eating/eat-smart/sugar/how-much-sugar-is-too-much`: kb_semantic_hit

## Judge Evaluation Details
### 1. Coverage (Score: 1.00)
- **Must Mention Found**: FDA, added_sugar, daily_limit
- **Must Mention Missed**: None
- **Judge Reasoning**: First result title and snippet contain 'added sugars', content_preview includes FDA. Snippet mentions 'limiting calories from added sugars to less than 10 percent per day' which implies daily limit. All must_mention items found.

### 2. Ranking (Score: 0.86)
- **Firecrawl Ranking**: [1, 2, 3, 4, 5]
- **LLM Ideal Ranking**: [1, 5, 2, 4, 3]
- **Judge Reasoning**: The primary query intent is to find the FDA's 2026 recommendation for added sugar grams per day. According to expected_source_priority, fda.gov must be first. Rank 1 (fda.gov) is from the official source and most current, so it is the ideal top result. Rank 2 (cdc.gov) is a secondary reliable government source, while Rank 5 (heart.org) is a relevant but non-governmental expert source; heart.org has more direct specific gram recommendations (36g men, 25g women) than cdc.gov's generic '10 grams per meal' phrasing. Therefore, to match source priority, we swap rank 5 to position 2 and rank 2 to position 3.
- **Ranking Suggestions**:
  - Boost fda.gov results when query mentions 'FDA' or 'recommendation'.
  - Downgrade social media (facebook.com) as it is not an authoritative source.

### 3. Scrape Quality Per Result
| URL | Noise Score | Structure Score | Completeness | Overall Quality | Issues Found |
|-----|-------------|-----------------|--------------|-----------------|--------------|
| https://www.fda.gov/food/nutrition-facts-label/added-sugars-nutrition-facts-label | 0.00 | 1.00 | 1.00 | **0.90** | missing_element (medium) |
| https://www.cdc.gov/nutrition/php/data-research/added-sugars.html | 0.00 | 1.00 | 1.00 | **0.85** | missing_element (high), missing_element (high) |
| https://nutritionsource.hsph.harvard.edu/carbohydrates/added-sugar-in-the-diet/ | 0.00 | 0.80 | 0.50 | **0.70** | missing_element (medium), truncation (high) |
| https://www.heart.org/en/healthy-living/healthy-eating/eat-smart/sugar/how-much-sugar-is-too-much | 0.20 | 1.00 | 1.00 | **0.80** | missing_element (high), missing_element (high), noise (low) |
