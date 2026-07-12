# Test Case Report: tc_5ac84dfe (🟢 PASSED)

## Metadata
- **Query**: `list of recommended vaccines for adults in 2026 from CDC with number of doses`
- **Category**: structured_data_extraction
- **Intent**: factual_lookup
- **Difficulty**: easy
- **Overall Score**: 0.781

## Cache Behavior
- **Query Cache**: hit
- **Content Cache Per Result**:
  - `https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-notes.html`: stale
  - `https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-age.html`: stale
  - `https://www.cdc.gov/vaccines/hcp/imz-schedules/child-adolescent-notes.html`: kb_semantic_hit
  - `https://www.cdc.gov/vaccines/imz-schedules/adult-easyread.html`: stale
  - `https://www.cidrap.umn.edu/childhood-vaccines/hhs-announces-unprecedented-overhaul-us-childhood-vaccine-schedule`: kb_semantic_hit

## Judge Evaluation Details
### 1. Coverage (Score: 1.00)
- **Must Mention Found**: CDC, adult_immunization_schedule, vaccine_doses
- **Must Mention Missed**: None
- **Judge Reasoning**: Found 'CDC' in title and snippet of result 1, and 'adult_immunization_schedule' as 'Adult Immunization Schedule Notes' and 'Adult Immunization Schedule by Age' in titles and content_previews. Found 'vaccine_doses' in snippets: '1 dose', '2 doses', '3-dose series'. Not explicitly 'recommended_ages' but ages are implied in the schedule context.

### 2. Ranking (Score: 0.90)
- **Firecrawl Ranking**: [1, 2, 3, 4, 5]
- **LLM Ideal Ranking**: [2, 4, 1, 3, 5]
- **Judge Reasoning**: Swap rank 2 with rank 1 because rank 2 is the adult schedule by age, directly relevant. Swap rank 4 with rank 3 to move the easy-read adult list to second. Rank 1 (notes) is supplementary, so third. Rank 3 (child schedule) is less relevant. Rank 5 (non-CDC) is lowest priority.
- **Ranking Suggestions**:
  - Prioritize adult-specific CDC pages over notes and child schedules.
  - Exclude non-CDC sources for queries specifically requesting CDC information.

### 3. Scrape Quality Per Result
| URL | Noise Score | Structure Score | Completeness | Overall Quality | Issues Found |
|-----|-------------|-----------------|--------------|-----------------|--------------|
| https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-notes.html | 0.00 | 0.90 | 0.30 | **0.50** | truncation (high) |
| https://www.cdc.gov/vaccines/hcp/imz-schedules/adult-age.html | 0.00 | 1.00 | 0.90 | **0.90** | None |
| https://www.cdc.gov/vaccines/hcp/imz-schedules/child-adolescent-notes.html | 0.00 | 0.90 | 0.40 | **0.40** | irrelevant_content (high), truncation (medium) |
| https://www.cdc.gov/vaccines/imz-schedules/adult-easyread.html | 0.00 | 0.90 | 0.60 | **0.70** | truncation (medium) |
| https://www.cidrap.umn.edu/childhood-vaccines/hhs-announces-unprecedented-overhaul-us-childhood-vaccine-schedule | 0.00 | 0.90 | 1.00 | **0.20** | irrelevant_content (high) |
