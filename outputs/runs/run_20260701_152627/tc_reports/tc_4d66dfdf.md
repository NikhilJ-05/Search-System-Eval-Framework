# Test Case Report: tc_4d66dfdf (🟢 PASSED)

## Metadata
- **Query**: `CDC adult immunization schedule 2026 table vaccine names doses`
- **Category**: structured_data_extraction
- **Intent**: data_extraction
- **Difficulty**: hard
- **Overall Score**: 0.789

## Cache Behavior
- **Query Cache**: miss
- **Content Cache Per Result**:
  - `https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-age.html`: miss
  - `https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-notes.html`: miss
  - `https://www.cdc.gov/vaccines/imz-schedules/adult-easyread.html`: miss
  - `https://www.cdc.gov/vaccines/hcp/imz-schedules/downloads/adult/adult-combined-schedule.pdf`: miss
  - `https://www.immunize.org/official-guidance/cdc/rec-schedules/`: miss

## Judge Evaluation Details
### 1. Coverage (Score: 0.67)
- **Must Mention Found**: CDC, Tdap
- **Must Mention Missed**: influenza
- **Judge Reasoning**: CDC is found in the snippet and content preview of result 1 (content_preview: 'current CDC Adult Immunization Schedule...'). Tdap is found in the snippet of result 3 ('Tdap every pregnancy. Td/Tdap every 10 years...'). Influenza is not found in any title, snippet, or content preview across all results.

### 2. Ranking (Score: 1.00)
- **Firecrawl Ranking**: [1, 2, 3, 4, 5]
- **LLM Ideal Ranking**: [1, 2, 3, 4, 5]
- **Judge Reasoning**: Results 1-4 are all from cdc.gov (highest priority source), so they should remain at the top. Among them, rank 1 is the most targeted table by age with dose info, rank 2 provides detailed notes, rank 3 is a less detailed easy-read, and rank 4 is a PDF. Rank 5 is from immunize.org (secondary source) and should be moved to last.  Result 2 should be swapped with result 3 because the schedule notes (rank 2) are more relevant than the easy-read (rank 3) for a detailed schedule table query.

### 3. Scrape Quality Per Result
| URL | Noise Score | Structure Score | Completeness | Overall Quality | Issues Found |
|-----|-------------|-----------------|--------------|-----------------|--------------|
| https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-age.html | 0.10 | 0.80 | 0.70 | **0.80** | missing_element (medium), truncation (medium) |
| https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-notes.html | 0.10 | 0.90 | 1.00 | **0.60** | missing_element (high) |
| https://www.cdc.gov/vaccines/imz-schedules/adult-easyread.html | 0.10 | 0.80 | 0.60 | **0.80** | truncation (medium) |
| https://www.cdc.gov/vaccines/hcp/imz-schedules/downloads/adult/adult-combined-schedule.pdf | 0.00 | 0.80 | 0.80 | **0.80** | formatting (low), truncation (low) |
| https://www.immunize.org/official-guidance/cdc/rec-schedules/ | 0.00 | 0.90 | 1.00 | **0.40** | missing_element (high) |
