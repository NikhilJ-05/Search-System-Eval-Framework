# Test Case Report: tc_1beb2c2f (🔴 FAILED)

## Metadata
- **Query**: `current university policies and honor code updates addressing generative AI use in higher education`
- **Category**: Education & Academia
- **Intent**: exploratory
- **Difficulty**: medium
- **Overall Score**: 0.772
- **Floor Failures**: _baseline_ranking, _baseline_fidelity (Score < 0.40)

## Cache Behavior
- **Query Cache**: miss
- **Content Cache Per Result**:
  - `https://www.asccc.org/papers/academic-integrity-policies-in-the-age-of-ai`: miss
  - `https://www.sciencedirect.com/science/article/pii/S2666920X24001292`: miss
  - `https://www.facebook.com/groups/higheredlearningcollective/posts/1893379737959382/`: miss
  - `https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1610836/full`: miss
  - `https://aiinaction.pressbooks.sunycreate.cloud/chapter/examples-of-institutional-policies-guidelines-that-address-ai-use/`: miss

## Judge Evaluation Details
### 1. _baseline_ranking (Score: 0.30, Level: L2) ❌
- **Weight**: 0.12
- **Reasoning**: The ranking starts well with two highly authoritative and relevant sources (ASCCC guidance and ScienceDirect paper). However, the third position is occupied by a severely truncated Facebook post with low authority and relevance, which should be ranked far lower. Two strong academic and official sources appear at ranks 4 and 5. Since a low-quality blog-like source ranks above official/academic sources, the contrastive fail is triggered. The overall ranking is not completely broken but has a clear order inversion that constitutes a major deficiency, resulting in an L2 score of 0.30.
- **Level Justification**: The ranking order has a major deficiency: a low-quality, largely irrelevant Facebook post (authority 0.2, relevance 0.5) is placed at rank 3, above two higher-quality documents (rank 4: authority 0.8, relevance 0.95; rank 5: authority 0.7, relevance 0.8). The first two positions are correctly high, but the intrusion of a clearly inferior source in the top half substantially undermines the baseline ranking quality. This aligns with L2 (major deficiency) because the contrastive failure is clearly triggered, yet the top two are appropriate.
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: A low-authority, low-relevance social media post (Facebook) ranks at position 3, above official documentation (SUNY, rank 5) and a peer-reviewed academic paper (rank 4). This matches the contrastive failure: 'blogs rank above official sources' (social media post analogous to a blog). Also, the most relevant results are not all at the top; rank 4 (relevance 0.95) and rank 5 (relevance 0.8) are buried below the Facebook post.

### 2. policy_specificity (Score: 0.95, Level: L5) ✅
- **Weight**: 0.16
- **Reasoning**: Multiple high-quality sources (ASCCC resource, Elsevier paper, Frontiers article, SUNY guide) provide concrete policy details from numerous universities, covering syllabus statements, detection tools, honor code guidance, and policy development frameworks. The set fully satisfies the specificity requirement.
- **Level Justification**: The collective results contain rich, specific policy information including sample syllabus language, decision trees, detection tool analysis, coding schemes, and multi-institutional examples. This exceeds the criteria for specific policy frameworks and enforcement mechanisms.
- **Contrastive Fail Triggered**: No

### 3. _baseline_fidelity (Score: 0.55, Level: L3) ⚠️
- **Weight**: 0.12
- **Reasoning**: While most documents preserve their main content, Document 3 is truncated, Document 2 loses table formatting, and Document 1 has substantial navigation noise. This places the set in the 'partial' range, with significant but not catastrophic deficiencies.
- **Level Justification**: The set includes one document with severe truncation and two others with moderate scrape issues (navigation noise, table formatting loss). However, four out of five documents have usable content, and Document 5 has excellent fidelity. The overall fidelity is partially acceptable but not adequate due to the truncated document and formatting losses.
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: The contrastive failure condition 'content is truncated' is met: Document 3 (Facebook post) has only an introductory sentence captured, with the rest of the post missing. This is a clear truncation.

### 4. _baseline_coverage (Score: 0.95, Level: L5) ✅
- **Weight**: 0.12
- **Reasoning**: The set thoroughly covers the query topic: specific institutional policies (Stanford, ASU, Boise State, etc.), honor code updates (Stanford's policy guidance), systematic analysis of top 100 universities, and a conceptual framework for academic integrity. The only gap is the irrelevant Facebook post, but the remaining documents collectively contain all required information.
- **Level Justification**: The collective results provide comprehensive coverage of current university policies and honor code updates addressing generative AI. Multiple high-authority sources cover policy examples, enforcement mechanisms, detection tools, and honor code language. The temporal markers are recent, satisfying the 'current' anchor. No critical information gaps are present.
- **Contrastive Fail Triggered**: No

### 5. source_credibility (Score: 0.75, Level: L4) ✅
- **Weight**: 0.16
- **Reasoning**: Source credibility is strong overall: the top two results and the fourth result are highly authoritative (official organization or peer-reviewed). The fifth result is a credible SUNY guide. The only weak link is the Facebook post (rank 3), which has low authority and truncated content. This prevents a perfect score but still achieves an adequate-to-good rating given the preponderance of authoritative, non-commercial sources.
- **Level Justification**: The document set includes three high-authority sources (ASCCC official document, Elsevier peer-reviewed paper, Frontiers peer-reviewed opinion) and one moderately authoritative source (SUNY guide). The Facebook post (rank 3) has very low authority and partially detracts from overall credibility, but does not dominate the set. Sources are academic or official rather than commercial marketing content. This places overall source credibility in the 'Adequate' range, not reaching 'Excellent' due to the inclusion of the low-authority social media result.
- **Contrastive Fail Triggered**: No

### 6. temporal_currency (Score: 0.65, Level: L4) ✅
- **Weight**: 0.22
- **Reasoning**: Temporal currency is adequate: the results include a recent systematic study (Dec 2024) and a 2025 compilation, but none are explicitly from the current academic year. The evidence does not trigger the contrastive fail, but the overall set is not fully current.
- **Level Justification**: The dimension is ADEQUATE (L4, score 0.65). While no document perfectly reflects the current academic year, Doc 2 (Dec 2024) provides a recent, authoritative overview of policies up to April 2024, and Doc 5 (2025) offers relevant examples. However, Doc 1 (April 2024) is older and Doc 4 (future) does not report current policies. The collection partially meets the requirement for current information, falling short of excellence.
- **Contrastive Fail Triggered**: No

### 7. ai_focus_clarity (Score: 0.95, Level: L5) ✅
- **Weight**: 0.10
- **Reasoning**: AI focus clarity is excellent. All relevant documents specifically address generative AI tools within the context of university policies and honor codes, avoiding broad or traditional academic integrity topics.
- **Level Justification**: The dimension is EXCELLENT (L5, score 0.95). Every substantive document directly and clearly addresses generative AI tools as the central subject of integrity guidelines. The specificity is high across documents, with detailed references to tools like ChatGPT, Bard, DALL-E, and image generators.
- **Contrastive Fail Triggered**: No

### 8. _baseline_fidelity (Score: 0.39, Level: L2) ❌
- **Weight**: 0.12
- **Reasoning**: Aggregated fidelity score from 5 pages.
- **Level Justification**: Computed average score is 0.39
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: Average scrape quality is poor

### Document Profiles Evaluated
| Rank | URL | Domain Type | Words | Headings | Tables | Completeness |
|------|-----|-------------|-------|----------|--------|--------------|
| 1 | https://www.asccc.org/papers/academic-integrity-policies-in-the-age-of-ai | N/A | 0 | 0 | 0 | unknown |
| 2 | https://www.sciencedirect.com/science/article/pii/S2666920X24001292 | N/A | 0 | 0 | 0 | unknown |
| 3 | https://www.facebook.com/groups/higheredlearningcollective/posts/1893379737959382/ | N/A | 0 | 0 | 0 | unknown |
| 4 | https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1610836/full | N/A | 0 | 0 | 0 | unknown |
| 5 | https://aiinaction.pressbooks.sunycreate.cloud/chapter/examples-of-institutional-policies-guidelines-that-address-ai-use/ | N/A | 0 | 0 | 0 | unknown |


## Failure Diagnosis & Recovery Roadmap
- **Failure Dimensions**: `_baseline_ranking, _baseline_fidelity, _baseline_fidelity (Critical: _baseline_ranking, _baseline_fidelity)`
- **Root Cause**: The primary failure is a ranking inversion: a truncated Facebook post (facebook.com, authority_score 0.2, query_relevance_score 0.5, word_count 21) was placed at rank 3, above frontiersin.org (authority 0.8, relevance 0.95) at rank 4 and pressbooks.sunycreate.cloud (authority 0.7, relevance 0.8) at rank 5, triggering contrastive failure in _baseline_ranking (score 0.3). This was compounded by poor aggregate scrape fidelity (0.3946, L2) driven by navigation noise on asccc.org (scrape_score 0.6, nav_link_ratio 0.4), table formatting loss on sciencedirect.com (scrape_score 0.4), and severe truncation on the Facebook post (21 words captured).

### Diagnostic Breakdown
- **Coverage Diagnosis**: No observable coverage gap — _baseline_coverage scored 0.95 (L5) with documents 1, 2, 4, and 5 collectively covering specific institutional policies, honor code updates, detection tools, and policy frameworks. The Facebook post at rank 3 is irrelevant but does not create a critical information gap.
- **Ranking Diagnosis**: Rank 3 (facebook.com, authority 0.2, relevance 0.5) is positioned above Rank 4 (frontiersin.org, authority 0.8, relevance 0.95) and Rank 5 (pressbooks.sunycreate.cloud, authority 0.7, relevance 0.8), violating both authority and relevance ordering. The contrastive fail was triggered because a social media post (analogous to a blog) ranks above official/academic sources.
- **Scrape Diagnosis**: Four of five documents have significant scrape issues: asccc.org (scrape_score 0.6, ~40% navigation/boilerplate), sciencedirect.com (scrape_score 0.4, table formatting lost, images not extracted), facebook.com (severely truncated, 21 words), frontiersin.org (scrape_score 0.4, boilerplate and navigation links). Only pressbooks.sunycreate.cloud has clean fidelity (scrape_score 0.2, no issues). Aggregate fidelity is 0.3946 (L2).

### Recommended Fix Actions
- Add a domain-authority-based reranking filter that demotes social media domains (facebook.com, twitter.com, linkedin.com) below academic/organization domains when the authority_score differential exceeds 0.3, preventing low-authority forum_thread page_types from appearing in top-3 positions for exploratory academic queries.
- Implement a content-completeness gate in the scrape pipeline that flags documents with word_count < 100 as 'appears_truncated' and excludes them from ranking consideration or re-queues them for re-scrape with JavaScript rendering enabled (critical for Facebook posts which require JS to render body content).
- Add a boilerplate-stripping post-processing step that removes navigation menus, share/citation toolbars, and action links from scraped markdown before scoring, targeting the specific patterns seen on asccc.org (nav_link_ratio 0.4) and frontiersin.org (citation tools, 'View details' links).
