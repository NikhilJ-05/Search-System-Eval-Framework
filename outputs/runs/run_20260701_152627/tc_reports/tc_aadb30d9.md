# Test Case Report: tc_aadb30d9 (🔴 FAILED)

## Metadata
- **Query**: `USPTO patent term adjustment rules 2026 PTAB trials`
- **Category**: structured_data_extraction
- **Intent**: data_extraction
- **Difficulty**: hard
- **Overall Score**: 0.645

## Cache Behavior
- **Query Cache**: miss
- **Content Cache Per Result**:
  - `https://data.uspto.gov/ptab/trials/documents/details/PGR2026-00017/171325310/18645205/patent-term-adjustment`: miss
  - `https://patentlyo.com/patent/2026/03/pta-keeps-score-patent-term-adjustment-as-a-measure-of-the-uspto-backlog.html`: miss
  - `https://ipwatchdog.com/2026/06/24/uspto-clarifies-approach-to-double-patenting-and-patent-term-adjustment-in-continuation-families/`: miss
  - `https://data.uspto.gov/ptab/trials/documents/details/PGR2025-00025/171313432/18103234/patent-term-adjustment`: miss
  - `https://www.bipc.com/patent-term-adjustment,-idss-and-the-30-day-rule`: miss

## Judge Evaluation Details
### 1. Coverage (Score: 1.00)
- **Must Mention Found**: USPTO, patent_term_adjustment, PTAB_trial
- **Must Mention Missed**: None
- **Judge Reasoning**: Found 'USPTO' in multiple titles, snips, and previews (e.g., 'USPTO.gov account' in result 1 content_preview). Found 'patent_term_adjustment' and 'PTAB_trial' ('PTAB Information Trial') in result 1 snippet. 'Terminal_disclaimer' and 'request_for_continued_examination' are not mentioned in any field of any result.

### 2. Ranking (Score: 0.92)
- **Firecrawl Ranking**: [1, 2, 3, 4, 5]
- **LLM Ideal Ranking**: [1, 4, 5, 3, 2]
- **Judge Reasoning**: Swapped 4 up to rank2 (uspto.gov), 5 up to rank3 (law firm), 3 down to rank4 (IPWatchdog), 2 down to rank5 (PatentlyO) to prioritize official sources and law firm content over blog posts.
- **Ranking Suggestions**:
  - Include authoritative law firm site like foley.com to strengthen mid-tier results
  - Ensure USPTO rules page (not just data portal) is available for more direct relevance

### 3. Scrape Quality Per Result
| URL | Noise Score | Structure Score | Completeness | Overall Quality | Issues Found |
|-----|-------------|-----------------|--------------|-----------------|--------------|
| https://data.uspto.gov/ptab/trials/documents/details/PGR2026-00017/171325310/18645205/patent-term-adjustment | 1.00 | 0.00 | 0.00 | **0.00** | missing_element (high), noise_leak (high), noise_leak (medium), structure_issue (high), completeness_issue (high) |
| https://patentlyo.com/patent/2026/03/pta-keeps-score-patent-term-adjustment-as-a-measure-of-the-uspto-backlog.html | 0.20 | 0.30 | 0.20 | **0.20** | missing_element (high), missing_element (medium), structure_issue (high), completeness_issue (high) |
| https://ipwatchdog.com/2026/06/24/uspto-clarifies-approach-to-double-patenting-and-patent-term-adjustment-in-continuation-families/ | 0.30 | 0.80 | 0.70 | **0.70** | missing_element (medium), noise_leak (low), completeness_issue (low) |
| https://data.uspto.gov/ptab/trials/documents/details/PGR2025-00025/171313432/18103234/patent-term-adjustment | 1.00 | 0.00 | 0.00 | **0.00** | missing_element (high), noise_leak (high), noise_leak (medium), structure_issue (high), completeness_issue (high) |
| https://www.bipc.com/patent-term-adjustment,-idss-and-the-30-day-rule | 1.00 | 0.00 | 0.00 | **0.00** | missing_element (high), noise_leak (high), structure_issue (high), completeness_issue (high) |

## Failure Diagnosis & Recovery Roadmap
- **Failure Dimensions**: `scrape`
- **Root Cause**: Scraped pages suffer from login walls, paywalls, and errors, blocking extraction of required structured data (tables, citations), despite near-perfect search result relevance and ranking.

### Diagnostic Breakdown
- **Coverage Diagnosis**: Coverage was perfect (1.0) with all expected terms found across results.
- **Ranking Diagnosis**: Ranking score is high (0.924) but diverged from ideal by placing official USPTO pages and law firm analysis lower than blog posts, reducing prioritization of authoritative sources.
- **Scrape Diagnosis**: Scrapes are heavily degraded: USPTO portal results (1,4) are behind login, PatentlyO (2) is paywalled, IPWatchdog (3) missing data tables and truncated, and bipc.com (5) completely failed (Cloudflare error). Consequently, expected elements 'data_tables' and 'statutory_regulatory_citations' are missing from all results, and noise from banners/overlays dominates the extracted markdown.

### Recommended Fix Actions
- Deploy login-aware crawling for USPTO portals to fetch actual data beyond registration banners, or use pre-authenticated sessions.
- Improve content extraction on semi-accessible pages: for IPWatchdog and similar sites, attempt advanced rendering to capture tabular data and avoid truncation; for paywalled content, extract available snippets cleanly.
- Adjust ranking to boost .gov and law firm domains (e.g., uspto.gov, bipc.com) over blog platforms when extracting regulatory data, using domain authority signals.
