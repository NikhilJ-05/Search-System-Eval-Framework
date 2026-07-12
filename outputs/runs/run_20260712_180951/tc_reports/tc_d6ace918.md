# Test Case Report: tc_d6ace918 (🔴 FAILED)

## Metadata
- **Query**: `latest research findings on long COVID neurological symptoms mechanisms`
- **Category**: Science & Academia
- **Intent**: exploratory
- **Difficulty**: medium
- **Overall Score**: 0.875
- **Floor Failures**: _baseline_fidelity, _baseline_fidelity (Score < 0.40)

## Cache Behavior
- **Query Cache**: miss
- **Content Cache Per Result**:
  - `https://pmc.ncbi.nlm.nih.gov/articles/PMC10901563/`: miss
  - `https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2024.1465787/full`: miss
  - `https://nyulangone.org/news/long-covid-linked-alzheimers-disease-mechanisms`: miss
  - `https://www.facebook.com/nih.gov/posts/research-supported-by-nih-suggests-that-some-neurological-symptoms-of-long-covid/1448300100674753/`: miss
  - `https://www.nature.com/articles/s41579-022-00846-2`: miss

## Judge Evaluation Details
### 1. _baseline_ranking (Score: 0.90, Level: L5) ✅
- **Weight**: 0.12
- **Reasoning**: The baseline ranking is excellent: recent peer-reviewed reviews from reputable journals (PMC, Frontiers) appear first, followed by a high-authority news article from NYU Langone, and lower-quality truncated or less relevant content appears later. No blogs or low-authority sources exceed official/peer-reviewed sources. The pipeline effectively surfaces genuinely recent research, meeting the temporal test with bonus credit for clustering authoritative 2024-2025 dates.
- **Level Justification**: The ranking correctly places highly authoritative and relevant peer-reviewed articles (2024, 2025) at the top, followed by a reputable institutional news article, then lower-quality or truncated sources. The temporal requirement is satisfied (recent research surfaces prominently). No contrastive fail triggered. The ordering reflects sound prioritization of quality and utility for the query.
- **Contrastive Fail Triggered**: No

### 2. _baseline_fidelity (Score: 0.30, Level: L2) ❌
- **Weight**: 0.12
- **Reasoning**: While three documents (the PMC review, Frontiers review, and NYU news article) have complete and well-structured scrapes, two documents (the NIH Facebook post and the Nature Reviews article) are severely truncated, missing the majority of their content. This mixed outcome results in a major deficiency overall.
- **Level Justification**: The majority of documents (3 of 5) have well-preserved markdown with complete content and minimal boilerplate. However, two documents are critically truncated, representing a major deficiency in the collective fidelity. The contrastive fail is triggered, preventing a higher score, but not all documents fail, so L2 (MAJOR DEFICIENCY) is appropriate.
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: Content truncation is present in two of the five documents (rank4 and rank5), which matches the contrastive failure condition 'content is truncated'.

### 3. _baseline_coverage (Score: 0.95, Level: L5) ✅
- **Weight**: 0.12
- **Reasoning**: The retrieved results collectively satisfy the query's need for latest research findings on long COVID neurological symptom mechanisms. Documents 1, 2, and 3 provide extensive, recent, and authoritative coverage of mechanisms (e.g., immune dysregulation, endothelial dysfunction, Alzheimer's pathway, structural imaging changes). Even the truncated documents hint at additional angles. No critical aspect is missing, and the temporal requirement is met with publications from 2024 and 2025.
- **Level Justification**: The collection includes three strong, recent, peer-reviewed or authoritative sources (2024 narrative review, 2025 comprehensive review, and a 2025/2026 news article on a specific study) that together thoroughly address neurological symptom mechanisms. The content is timely, diverse, and highly relevant, meeting the exploratory intent and earning the highest level.
- **Contrastive Fail Triggered**: No

### 4. source_authority (Score: 0.95, Level: L5) ✅
- **Weight**: 0.19
- **Reasoning**: The retrieved documents collectively demonstrate excellent source authority. They are drawn from peer-reviewed journals (Dementia & Neuropsychologia, Frontiers in Neurology, Nature Reviews Microbiology), a major academic medical center news release (NYU Langone Health), and an official government health agency post (NIH). No low-authority or marketing content is present. The contrastive failure condition is not triggered.
- **Level Justification**: All five documents exceed the authority threshold significantly. Ranks 1, 2, 3, and 5 are directly from peer-reviewed journals or major academic medical centers with high authority scores (0.9–0.95). Rank 4 (NIH Facebook post) carries government authority, though its content is truncated; nonetheless, the source is a recognized health organization. No document originates from low-authority sources. The collective evidence strongly meets the criteria for excellent source authority.
- **Contrastive Fail Triggered**: No

### 5. temporal_relevance (Score: 0.95, Level: L5) ✅
- **Weight**: 0.26
- **Reasoning**: The top results are dominated by genuinely recent, high-authority sources (2024–2025) that directly address long COVID neurological mechanisms. No contrastive fail applies. The temporal relevance is excellent.
- **Level Justification**: All top results are from recent years (2023–2025), dominated by peer-reviewed reviews and a news report on a 2024 study. No stale content or misleading titles. The set reflects strong ongoing research momentum. Score 0.95 for near-perfect temporal relevance.
- **Contrastive Fail Triggered**: No

### 6. recency_signals (Score: 0.50, Level: L3) ⚠️
- **Weight**: 0.06
- **Reasoning**: Recency signals are mixed: the top two results have explicit dates, but three results (including a news article and a high-impact review) show no captured publication date. This partially undermines a user's ability to assess recency from snippets, landing in the 'partial' range.
- **Level Justification**: Only two of five documents provide a clear publication date in the profile (and presumably in search snippets). The other three have missing dates, which partially triggers the contrastive fail. This is a significant deficiency but not a complete failure because the top results (which carry more weight) do have visible dates. Score 0.50 reflects partial adequacy.
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: Three of the five results lack visible publication dates, making it impossible to assess temporal relevance from the snippet alone for those documents. Though the top two have clear dates, the overall set does not meet the 'each result' criterion.

### 7. topic_precision (Score: 0.95, Level: L5) ✅
- **Weight**: 0.13
- **Reasoning**: The retrieved documents collectively demonstrate strong topic precision for 'latest research findings on long COVID neurological symptoms mechanisms.' The top-ranked documents specifically cover neurological manifestations (cognitive, sleep, neuropsychiatric, olfactory) and mechanistic pathways (biomarkers, imaging, Alzheimer's links, immune dysregulation). No documents veer into acute COVID treatment or vaccine efficacy. Minor limitations from truncated content in ranks 4 and 5 do not diminish the overall precision of the set.
- **Level Justification**: The top three documents (ranks 1, 2, 3) are highly precise, directly addressing the query's focus on neurological symptoms and underlying mechanisms of long COVID. They come from authoritative peer-reviewed sources or reputable medical institutions. The lower-ranked documents (4 and 5) are less complete but still relevant to the topic. Overall, the collection strongly satisfies the criteria with no contrastive failure. The precision is excellent.
- **Contrastive Fail Triggered**: No

### 8. _baseline_fidelity (Score: 0.31, Level: L2) ❌
- **Weight**: 0.12
- **Reasoning**: Aggregated fidelity score from 5 pages.
- **Level Justification**: Computed average score is 0.31
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: Average scrape quality is poor

### Document Profiles Evaluated
| Rank | URL | Domain Type | Words | Headings | Tables | Completeness |
|------|-----|-------------|-------|----------|--------|--------------|
| 1 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10901563/ | N/A | 0 | 0 | 0 | unknown |
| 2 | https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2024.1465787/full | N/A | 0 | 0 | 0 | unknown |
| 3 | https://nyulangone.org/news/long-covid-linked-alzheimers-disease-mechanisms | N/A | 0 | 0 | 0 | unknown |
| 4 | https://www.facebook.com/nih.gov/posts/research-supported-by-nih-suggests-that-some-neurological-symptoms-of-long-covid/1448300100674753/ | N/A | 0 | 0 | 0 | unknown |
| 5 | https://www.nature.com/articles/s41579-022-00846-2 | N/A | 0 | 0 | 0 | unknown |


## Failure Diagnosis & Recovery Roadmap
- **Failure Dimensions**: `_baseline_fidelity, recency_signals, _baseline_fidelity (Critical: _baseline_fidelity, _baseline_fidelity)`
- **Root Cause**: The scrape_score values are inverted: ranks 1-3 with content_completeness='complete' and scrape_reasoning confirming faithful preservation receive scrape_score=0.20 (L1), while ranks 4-5 with content_completeness='appears_truncated' and critical truncation issues receive scrape_score=0.60 (L3/L4). This inversion drives _baseline_fidelity to 0.30-0.312, failing the test. A secondary issue is that 3 of 5 documents (ranks 3, 4, 5) have empty publication_date fields, causing recency_signals to trigger a contrastive fail at score 0.50, which contradicts the expected <=0.40 threshold.

### Diagnostic Breakdown
- **Coverage Diagnosis**: N/A — coverage scored 0.95 (L5); documents collectively address neurological symptoms, mechanisms, biomarkers, imaging, and therapeutic approaches.
- **Ranking Diagnosis**: N/A — ranking scored 0.90 (L5); peer-reviewed articles correctly rank above truncated social media and incomplete content.
- **Scrape Diagnosis**: Scrape scores are inverted: Rank 1 (https://pmc.ncbi.nlm.nih.gov/articles/PMC10901563/) has scrape_score=0.20 with content_completeness='complete' and scrape_reasoning='faithfully preserves the full text', while Rank 4 (https://www.facebook.com/nih.gov/posts/...) has scrape_score=0.60 with content_completeness='appears_truncated' and word_count=23. Complete documents should score >=0.8 and truncated documents should score <=0.4. Additionally, Rank 5 (https://www.nature.com/articles/s41579-022-00846-2) is truncated mid-sentence but scores 0.60, higher than any complete document.

### Recommended Fix Actions
- Fix the scrape_score computation logic to invert or correct the scoring: complete documents (content_completeness='complete') should receive scrape_score >= 0.80, while truncated documents (content_completeness='appears_truncated') should receive scrape_score <= 0.40. The current mapping appears reversed.
- Add a publication_date extraction step for news articles and social media posts: parse date metadata from OpenGraph tags, JSON-LD structured data, or visible date strings. For Rank 3 (nyulangone.org), Rank 4 (facebook.com/nih.gov), and Rank 5 (nature.com), the temporal_markers field contains date information (e.g., '17 April 2023' for Rank 5) that should be normalized into publication_date.
- Add a validation guard in the recency_signals scoring function: when contrastive_fail_triggered is true, enforce score <= 0.40 to prevent the contradiction flagged in warnings.
