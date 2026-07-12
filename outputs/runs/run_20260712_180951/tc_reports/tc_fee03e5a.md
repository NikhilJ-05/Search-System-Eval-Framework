# Test Case Report: tc_fee03e5a (🔴 FAILED)

## Metadata
- **Query**: `average PhD stipend amounts in STEM fields`
- **Category**: Education & Academia
- **Intent**: comparative_research
- **Difficulty**: medium
- **Overall Score**: 0.492
- **Floor Failures**: _baseline_ranking, multi_constraint_coverage, _baseline_fidelity, source_quality, _baseline_authority, _baseline_fidelity (Score < 0.40)

## Cache Behavior
- **Query Cache**: miss
- **Content Cache Per Result**:
  - `https://www.reddit.com/r/gradadmissions/comments/10n8k77/acceptable_stipend_for_stem_phds/`: miss
  - `https://www.phdstipends.com/results`: miss
  - `https://www.applykite.com/blog/phd-student-salary`: miss
  - `https://www.quora.com/Does-a-PhD-in-STEM-field-from-one-of-the-top-universities-from-the-USA-guarantee-starting-annual-compensation-of-250K`: miss
  - `https://imba.missouri.edu/how-much-are-phd-stipends-1020625809.html`: miss

## Judge Evaluation Details
### 1. _baseline_ranking (Score: 0.30, Level: L2) ❌
- **Weight**: 0.12
- **Reasoning**: The ranking fails to prioritize higher-authority and more relevant sources. The most relevant document (applykite) is ranked third, while a low-authority Reddit post ranks first. This constitutes a major ranking deficiency.
- **Level Justification**: The ranking order significantly violates the criteria. The highest authority/relevance source (applykite, authority 0.6, relevance 0.95) is placed third, while lower-quality sources (Reddit, authority 0.15, relevance 0.7) occupy the top position. This indicates a major deficiency in ranking quality.
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: The most relevant and relatively authoritative source (applykite blog, rank 3) is buried behind lower-authority and less relevant sources (Reddit and phdstipends.com). This matches the contrastive fail condition of 'most relevant result is buried.'

### 2. contextual_breadth (Score: 0.55, Level: L3) ⚠️
- **Weight**: 0.22
- **Reasoning**: Doc3 provides the main breadth expansion with field-by-field stipend ranges, country comparisons, and funding-type discussion, while Doc2 offers a dataset with cost-of-living normalization. However, the set fails to address university-tier differences, comprehensive compensation packages, or broader program selection criteria, leaving the overall contextual breadth at a partial level.
- **Level Justification**: The set provides moderate expansion beyond the literal query: field-level and country-level stipend context (Doc3) and a raw database for comparison (Doc2). But lacks university-tier differences, explicit total compensation breakdowns (tuition, health insurance), and program selection guidance. The contrastive fail is not fully triggered because more than a single average is present, but the breadth is insufficient for an 'adequate' rating (L4). The strong signals from Doc3 (field breakdowns, funding types) lift it from 'major deficiency' but not to 'adequate' due to missing tier/prestige context.
- **Contrastive Fail Triggered**: No

### 3. multi_constraint_coverage (Score: 0.35, Level: L2) ❌
- **Weight**: 0.19
- **Reasoning**: Only Doc3 introduces any multi-constraint content (funding types, country benefits), but it omits critical components like tuition waivers, health insurance, and funding duration. The remainder of the set (Doc1, Doc2, Doc5, Doc4) provides only stipend amounts. The overall coverage of multiple funding and program attributes is severely lacking, earning a major deficiency rating.
- **Level Justification**: The set fails to cover multiple essential compensation components (tuition remission, health insurance, duration guarantees). Only Doc3 partially addresses funding types, but without specific detail on availability or typical packages. The other documents are purely stipend amounts. This constitutes a major deficiency in multi-constraint coverage. The score is at the high end of L2 because at least one document (Doc3) introduces some breadth beyond stipend amounts.
- **Contrastive Fail Triggered**: No

### 4. _baseline_fidelity (Score: 0.30, Level: L2) ❌
- **Weight**: 0.12
- **Reasoning**: Only Doc2 and Doc3 have reasonably complete scrapes; Doc1 and Doc5 are truncated to only 28 words, and Doc4 is an error page. The collective fidelity is poor, with three out of five documents failing to preserve page structure or content. This triggers the contrastive failure condition for truncation.
- **Level Justification**: Two documents (Doc2, Doc3) have acceptable scrape fidelity with minor issues, but three documents (Doc1, Doc4, Doc5) are either truncated or contain no usable content. This constitutes a major deficiency in baseline fidelity, as the pipeline retrieved multiple documents with critical scrape failures. The level is at the high end of L2 because the two good scrapes provide some usable data, but the overall quality is compromised.
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: The contrastive fail condition 'content is truncated' is triggered because Doc1, Doc5, and Doc4 (error) have significant truncation or complete failure, meaning a majority of retrieved documents lack complete content. The set fails the baseline fidelity requirement overall.

### 5. source_quality (Score: 0.30, Level: L2) ❌
- **Weight**: 0.09
- **Reasoning**: The retrieved documents are predominantly aggregator, forum, or blog content with no primary institutional sources. The contrastive fail condition is met, resulting in a score of 0.30 (L2 Major Deficiency).
- **Level Justification**: The sources lack authoritative primary origins. The highest authority scores are 0.6 (partial, truncated) and 0.6 (commercial blog), but the top-ranked documents (Reddit 0.15, phdstipends 0.3) are low-credibility. This constitutes a major deficiency for source quality.
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: The portfolio is dominated by anonymous listicles (Reddit), crowd-sourced aggregators (phdstipends), and content-farm blogs (ApplyKite) that recycle generic averages without attribution to primary institutional data. No official university or federal agency pages are present.

### 6. _baseline_authority (Score: 0.35, Level: L2) ❌
- **Weight**: 0.07
- **Reasoning**: The portfolio includes two moderately authoritative sources (ApplyKite, Missouri.edu) but they are outweighed by the low-credibility Reddit and phdstipends entries given top ranking. The contrastive fail is triggered, leading to a score of 0.35 (L2 Major Deficiency).
- **Level Justification**: While there are some moderately credible sources later in the ranking, the prominence of untrustworthy sources (anonymous forum, crowd-sourced database) at ranks 1 and 2 makes the portfolio as a whole lack baseline authority for a research query. This is a major deficiency.
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: Low-credibility sources (Reddit authority 0.15, phdstipends authority 0.3) are given undue weight as the top-ranked results, undermining the overall credibility of the portfolio.

### 7. _baseline_freshness (Score: 0.70, Level: L4) ✅
- **Weight**: 0.07
- **Reasoning**: The retrieved documents collectively meet temporal appropriateness: the two most substantial sources (Docs 2 and 3) are current, covering 2025-2026 data. No clearly outdated information is present. The minor deficiencies from documents without dates keep the score from reaching 'Excellent', but the evidence supports an 'Adequate' rating.
- **Level Justification**: Two of the five documents (Docs 2 and 3) provide strong evidence of temporal freshness with explicit 2025-2026 data. The remaining documents lack clear dates but do not undermine recency. Overall, the collection satisfies the freshness criterion at an adequate level, though not all documents are independently temporally verified.
- **Contrastive Fail Triggered**: No

### 8. comparative_specificity (Score: 0.75, Level: L4) ✅
- **Weight**: 0.12
- **Reasoning**: The evaluation dimension is comparative_specificity. The evidence shows that Documents 2 and 3 provide specific, distinguishable comparisons across universities and fields of study. Document 1 adds a location-based distinction. The contrastive fail (flat average only) is not triggered. The checklist confirms that university and field comparisons are met; tier comparisons are partially met. Given the richness of data but lack of explicit tier categorization and aggregation, the score is 0.75 (Adequate).
- **Level Justification**: The retrieved documents collectively provide strong comparative specificity: Document 2 offers per-university stipend entries (though not aggregated) and Document 3 gives field-level and international breakdowns. These go well beyond a single undifferentiated average. However, the content is not fully comprehensive: Document 2 lacks STEM-field filtering and aggregation, Document 3 lacks STEM-specific averages across all fields, and institutional tier comparisons are only implicit. Hence the level is Adequate (L4) rather than Excellent (L5). The score of 0.75 reflects solid comparative detail with minor room for improvement.
- **Contrastive Fail Triggered**: No

### 9. _baseline_fidelity (Score: 0.34, Level: L2) ❌
- **Weight**: 0.12
- **Reasoning**: Aggregated fidelity score from 5 pages.
- **Level Justification**: Computed average score is 0.34
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: Average scrape quality is poor

### Document Profiles Evaluated
| Rank | URL | Domain Type | Words | Headings | Tables | Completeness |
|------|-----|-------------|-------|----------|--------|--------------|
| 1 | https://www.reddit.com/r/gradadmissions/comments/10n8k77/acceptable_stipend_for_stem_phds/ | N/A | 0 | 0 | 0 | unknown |
| 2 | https://www.phdstipends.com/results | N/A | 0 | 0 | 0 | unknown |
| 3 | https://www.applykite.com/blog/phd-student-salary | N/A | 0 | 0 | 0 | unknown |
| 4 | https://www.quora.com/Does-a-PhD-in-STEM-field-from-one-of-the-top-universities-from-the-USA-guarantee-starting-annual-compensation-of-250K | N/A | 0 | 0 | 0 | unknown |
| 5 | https://imba.missouri.edu/how-much-are-phd-stipends-1020625809.html | N/A | 0 | 0 | 0 | unknown |


## Failure Diagnosis & Recovery Roadmap
- **Failure Dimensions**: `_baseline_ranking, contextual_breadth, multi_constraint_coverage, _baseline_fidelity, source_quality, _baseline_authority, _baseline_fidelity (Critical: _baseline_ranking, multi_constraint_coverage, _baseline_fidelity, source_quality, _baseline_authority, _baseline_fidelity)`
- **Root Cause**: The primary failure mechanism is a ranking inversion: applykite.com (relevance 0.95, authority 0.6) was placed at rank 3 behind Reddit (relevance 0.7, authority 0.15) and phdstipends.com (relevance 0.8, authority 0.3), as cited in the _baseline_ranking evidence. This was compounded by critical scrape failures on 3 of 5 documents — Reddit truncated to 28 words, Quora returning an error page, and Missouri truncated to 28 words — which destroyed fidelity, source quality, and multi-constraint coverage since the truncated documents could not contribute tuition remission, health insurance, or funding duration data.

### Diagnostic Breakdown
- **Coverage Diagnosis**: The document profiles show no coverage of tuition remission, health insurance, or funding duration guarantees across any of the 5 retrieved documents. Only Doc3 (applykite.com) partially covers funding types (fellowships, TAs, RAs) but without specific details on availability or duration. No document systematically compares stipends by university tier (R1 vs. teaching-focused). The truncated Missouri.edu page (28 words) likely contained tier-relevant context that was lost.
- **Ranking Diagnosis**: Rank 3 (applykite.com, relevance 0.95, authority 0.6) should have been Rank 1. Rank 1 (Reddit, relevance 0.7, authority 0.15) and Rank 4 (Quora, relevance 0.0, authority 0.0, error page) should not have appeared in the top results at all. The ranking model gave undue weight to forum/aggregator content over a structured blog with field-by-field and country-level stipend tables.
- **Scrape Diagnosis**: Three of five documents have critical scrape failures: Reddit (scrape_score 0.6, truncated to 28 words, missing all comments), Quora (scrape_score 0.2, error page with 11 words), and Missouri (scrape_score 0.6, truncated to 28 words). Doc2 (phdstipends.com) has scrape_score 0.2 with nav_link_ratio 0.923, suggesting excessive navigation noise. Only Doc3 (applykite.com, scrape_score 0.4, word_count 2798) has reasonably complete content.

### Recommended Fix Actions
- Adjust the ranking model's authority and relevance weighting to penalize forum threads (Reddit, Quora) and crowd-sourced aggregators when a structured blog or academic-domain source with higher relevance and authority scores exists in the candidate set — specifically, boost results with query_relevance_score >= 0.9 and authority_score >= 0.5 above any result with authority_score < 0.3.
- Add a scrape retry with exponential backoff and alternate user-agent for domains that return error pages (e.g., Quora's 'Something went wrong' response), and add a content-length validation gate that re-scrapes or discards any document with word_count < 100 that was expected to be a full article page.
- Add domain-type boosting for .edu and government domains in the search pipeline for education/academia queries, and add a query expansion step that appends terms like 'tuition waiver' 'health insurance' 'funding guarantee' to ensure multi-constraint coverage in retrieved snippets.
