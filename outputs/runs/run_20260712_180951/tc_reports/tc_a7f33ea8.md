# Test Case Report: tc_a7f33ea8 (🔴 FAILED)

## Metadata
- **Query**: `current recommended daily added sugar limit for adults`
- **Category**: Food & Nutrition
- **Intent**: factual_lookup
- **Difficulty**: medium
- **Overall Score**: 0.859
- **Floor Failures**: _baseline_fidelity (Score < 0.40)

## Cache Behavior
- **Query Cache**: miss
- **Content Cache Per Result**:
  - `https://nutritionsource.hsph.harvard.edu/carbohydrates/added-sugar-in-the-diet/`: kb_semantic_hit
  - `https://www.cdc.gov/nutrition/php/data-research/added-sugars.html`: kb_semantic_hit
  - `https://www.nhs.uk/live-well/eat-well/food-types/how-does-sugar-in-our-diet-affect-our-health/`: miss
  - `https://www.facebook.com/FDA/posts/the-new-dietary-guidelines-for-americans-recommend-limiting-added-sugars-to-supp/1322126489944706/`: miss
  - `https://www.fda.gov/food/nutrition-facts-label/added-sugars-nutrition-facts-label`: kb_semantic_hit

## Judge Evaluation Details
### 1. _baseline_ranking (Score: 0.55, Level: L3) ⚠️
- **Weight**: 0.12
- **Reasoning**: Baseline ranking is generally good with top results from Harvard, CDC, and NHS—all highly authoritative and relevant. However, the inclusion of a truncated Facebook post at rank 4 ahead of a more authoritative FDA page at rank 5 constitutes a ranking inversion that partially satisfies the criteria. The contrastive failure condition is met, so the dimension receives a partial (L3) score of 0.55.
- **Level Justification**: The ranking is largely strong: the top three results are authoritative and highly relevant. However, a clear ranking error exists where a truncated, low-quality Facebook post (rank 4) is placed before a comprehensive FDA official page (rank 5). This triggers the contrastive failure condition and prevents scoring in L4 or L5. The error is isolated, so partial (L3) is appropriate rather than major deficiency (L2) or critical failure (L1).
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: A low-quality social media post (rank 4) ranks above a high-authority official government page (rank 5) from the same agency. This violates the principle that official sources should appear before lower-quality ones, and the most relevant result (FDA page) is preceded by a less relevant source.

### 2. completeness (Score: 0.85, Level: L5) ✅
- **Weight**: 0.15
- **Reasoning**: The result set comprehensively covers daily added sugar limits from multiple authoritative bodies (DGA, AHA, NHS), explains the difference between added and natural sugars, identifies common dietary sources, and includes health risk information. Minor depth in health risks prevents a perfect score, but overall coverage is excellent.
- **Level Justification**: All four required aspects are addressed, with strong coverage from authoritative sources (Harvard, CDC, NHS, FDA). The only partial gap is health risks, but Doc3 provides direct coverage of tooth decay and weight gain. The set presents a range of current guidelines (2020-2025 DGA, 2023 NHS) and properly attributes them to authoritative bodies. The scoring range L5 (0.80–1.00) is appropriate for excellent coverage.
- **Contrastive Fail Triggered**: No

### 3. _baseline_fidelity (Score: 0.50, Level: L3) ⚠️
- **Weight**: 0.12
- **Reasoning**: While most documents (Doc1, Doc2, Doc3, Doc5) have acceptable scrape quality with minor issues, Doc4 is critically truncated, undermining overall baseline fidelity. The set as a whole is partially satisfactory, with the truncation preventing a higher score.
- **Level Justification**: The presence of a severely truncated document (Doc4, Facebook post) triggers the contrastive fail, so score cannot exceed L3. However, the other four documents have minor scrape issues only (repeated lines, boilerplate leakage) and no significant truncation or structural loss. Thus the overall fidelity is partial, not a major deficiency. L3 (0.40–0.60) is appropriate.
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: Doc4 is severely truncated, meeting the 'content is truncated' condition for contrastive failure. This prevents the dimension from scoring in L4 or L5.

### 4. source_authority (Score: 0.95, Level: L5) ✅
- **Weight**: 0.19
- **Reasoning**: All top results are from highly authoritative academic and government institutions (Harvard, CDC, NHS, FDA). They cite official dietary guidelines and peer-reviewed research. No commercial or aggregator content dominates. The Facebook post from FDA is less complete but still from an official source. The overall source authority is excellent.
- **Level Justification**: The retrieved documents are overwhelmingly from highly authoritative academic and government sources (Harvard T.H. Chan School of Public Health, CDC, NHS, FDA). They cite official dietary guidelines and peer-reviewed literature. The contrastive fail condition is not triggered. The set satisfies the criteria at an excellent level, warranting the top level.
- **Contrastive Fail Triggered**: No

### 5. temporal_currency (Score: 0.90, Level: L5) ✅
- **Weight**: 0.23
- **Reasoning**: Overall, the search results successfully resolve the temporal ambiguity in the query by returning genuinely current sources. The top results from Harvard, CDC, and NHS are all recently published or reviewed and present current guidelines (DGA 2020-2025, NHS 2023 recommendations, CDC per-meal limits). No outdated recommendations are passed off as current, and no misleading temporal language is used. The evidence strongly supports a score in the Excellent range.
- **Level Justification**: The top three results (Harvard, CDC, NHS) all have recent temporal markers (2022–2026) and reflect current dietary guidance from official bodies. The FDA page, though undated, aligns with current labeling rules and DGA. No document presents decade-old recommendations as current. The Facebook post is truncated and undated but does not contradict the overall temporal currency. The set collectively meets all criteria for temporal currency, with no contrastive fail triggered.
- **Contrastive Fail Triggered**: No

### 6. quantitative_specificity (Score: 0.95, Level: L5) ✅
- **Weight**: 0.19
- **Reasoning**: The retrieved documents collectively provide extensive and precise numerical thresholds for daily added sugar intake, including 50g (FDA, DGA), 30g (NHS), and 24-36g (AHA), as well as teaspoon equivalents and percent-of-calorie recommendations. No document relies on vague advice. The contrastive fail is not triggered. The specificity is excellent across multiple authoritative sources, earning a score in the upper L5 range.
- **Level Justification**: The collective results exceed the criteria for excellent quantitative specificity. Multiple authoritative bodies (Harvard/CDC, NHS, FDA) offer precise, well-attributed numerical daily added sugar limits in grams, teaspoons, and as a percentage of daily calories. The CDC per-meal limit (10g) adds context. The only minor weakness is the truncated Facebook post, but it still provides teaspoons values. Overall, the evidence is rich, diverse, and fully satisfies the need for concrete thresholds.
- **Contrastive Fail Triggered**: No

### 7. _baseline_fidelity (Score: 0.31, Level: L2) ❌
- **Weight**: 0.12
- **Reasoning**: Aggregated fidelity score from 5 pages.
- **Level Justification**: Computed average score is 0.31
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: Average scrape quality is poor

### Document Profiles Evaluated
| Rank | URL | Domain Type | Words | Headings | Tables | Completeness |
|------|-----|-------------|-------|----------|--------|--------------|
| 1 | https://nutritionsource.hsph.harvard.edu/carbohydrates/added-sugar-in-the-diet/ | N/A | 0 | 0 | 0 | unknown |
| 2 | https://www.cdc.gov/nutrition/php/data-research/added-sugars.html | N/A | 0 | 0 | 0 | unknown |
| 3 | https://www.nhs.uk/live-well/eat-well/food-types/how-does-sugar-in-our-diet-affect-our-health/ | N/A | 0 | 0 | 0 | unknown |
| 4 | https://www.facebook.com/FDA/posts/the-new-dietary-guidelines-for-americans-recommend-limiting-added-sugars-to-supp/1322126489944706/ | N/A | 0 | 0 | 0 | unknown |
| 5 | https://www.fda.gov/food/nutrition-facts-label/added-sugars-nutrition-facts-label | N/A | 0 | 0 | 0 | unknown |


## Failure Diagnosis & Recovery Roadmap
- **Failure Dimensions**: `_baseline_ranking, _baseline_fidelity, _baseline_fidelity (Critical: _baseline_fidelity)`
- **Root Cause**: The primary failure is a ranking inversion where a severely truncated Facebook post (rank 4, 25 words, scrape_score 0.79, authority 0.7, relevance 0.6) is placed above the FDA official page (rank 5, authority 0.95, relevance 1.0, scrape_score 0.40). This is compounded by inverted scrape scores: Harvard, CDC, and NHS pages with complete content all received scrape_score=0.20 despite their scrape_reasoning stating 'faithfully captures all textual content,' while the 25-word truncated Facebook post received scrape_score=0.79.

### Diagnostic Breakdown
- **Coverage Diagnosis**: No significant coverage gap — all required aspects (daily limits, sugar type distinctions, health risks, dietary sources) are covered across Harvard, NHS, CDC, and FDA documents. The only partial gap is health risk depth, but Doc3 covers tooth decay and weight gain.
- **Ranking Diagnosis**: Rank 4 (Facebook/FDA post, authority 0.7, relevance 0.6, 25 words) is incorrectly placed above Rank 5 (FDA official page, authority 0.95, relevance 1.0, 1681 words). The Facebook post should either be excluded or ranked last, as it is a truncated social media snippet that duplicates information already available from the official FDA page at rank 5.
- **Scrape Diagnosis**: Scrape scores are inverted: Harvard (scrape_score=0.20, scrape_reasoning='faithfully captures all textual content'), CDC (scrape_score=0.20, scrape_reasoning='faithfully reproduces the original page content with high fidelity'), and NHS (scrape_score=0.20, scrape_reasoning='faithfully preserves all substantive content') all received L1 scores despite complete content, while the severely truncated Facebook post (25 words, 'ends mid-sentence') received scrape_score=0.79 (L4). The FDA page (scrape_score=0.40) has nav_link_ratio=0.80 indicating excessive boilerplate contamination.

### Recommended Fix Actions
- Add a domain-type penalty in the ranking pipeline for social media domains (facebook.com, twitter.com, instagram.com) so that truncated social media posts cannot outrank official government pages on the same topic — specifically, demote any result with word_count < 100 and domain_type='commercial' below any result with domain_type='authoritative' and query_relevance_score >= 0.9.
- Fix the scrape_score calibration logic: pages where scrape_reasoning states 'faithfully captures' or 'faithfully preserves' should not receive scrape_score=0.20 (L1). The scoring function appears to be inverting quality — investigate whether the scrape_score computation is using an inverted scale or incorrectly weighting minor issues (e.g., duplicated lines) as critical failures.
- Add a nav_link_ratio threshold check to the scrape pipeline: the FDA page has nav_link_ratio=0.80, meaning 80% of links are navigation/boilerplate. Implement a content extraction step that strips navigation elements before scoring, or apply a penalty when nav_link_ratio > 0.5.
