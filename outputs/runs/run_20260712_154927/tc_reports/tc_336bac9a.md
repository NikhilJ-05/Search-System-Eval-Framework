# Test Case Report: tc_336bac9a (🔴 FAILED)

## Metadata
- **Query**: `evidence based treatment options for adult ADHD management`
- **Category**: Healthcare & Medical
- **Intent**: factual_lookup
- **Difficulty**: medium
- **Overall Score**: 0.802
- **Floor Failures**: _baseline_ranking, _baseline_fidelity (Score < 0.40)

## Cache Behavior
- **Query Cache**: miss
- **Content Cache Per Result**:
  - `https://pmc.ncbi.nlm.nih.gov/articles/PMC10730462/`: miss
  - `https://add.org/adhd-therapies/`: miss
  - `https://www.adhdevidence.org/blog/evidence-based-interventions-for-adhd`: miss
  - `https://www.cdc.gov/adhd/treatment/index.html`: miss
  - `https://health.ucdavis.edu/mind-institute/resources/understanding-adhd/adhd-treatment`: miss

## Judge Evaluation Details
### 1. _baseline_ranking (Score: 0.35, Level: L2) ❌
- **Weight**: 0.12
- **Reasoning**: The ranking fails the baseline ordering test because the most relevant and authoritative source (UC Davis MIND Institute) is placed last, while an irrelevant CDC page on child ADHD is ranked higher. Although the first two results are strong, the violation of 'most relevant result buried' triggers the contrastive fail and leads to a major deficiency score of L2.
- **Level Justification**: While the top two results (Ranks 1 and 2) are highly relevant and authoritative, the ranking order has major deficiencies: an irrelevant CDC page about children outranks a highly relevant academic source for adults, and a moderately relevant blog post outranks a highly authoritative and relevant academic page. The burial of the most relevant source (Rank 5) is a clear violation of the ranking principle, making the overall ranking inadequate. This aligns with L2 (Major Deficiency, 0.20–0.40) rather than L3 (Partial) because the error is systematic and undermines the user's ability to find key evidence for the query.
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: The most relevant result (Rank 5, UC Davis MIND Institute, relevance 0.95, authority 0.95) is buried at rank 5, behind a moderately relevant blog post (Rank 3, relevance 0.4) and a completely irrelevant government page (Rank 4, relevance 0.1). This matches the contrastive fail description 'most relevant result is buried.'

### 2. treatment_modality_coverage (Score: 0.93, Level: L5) ✅
- **Weight**: 0.28
- **Reasoning**: The retrieved documents collectively address all required treatment modalities: pharmacological (stimulants and non-stimulants from document 1), behavioral/psychotherapy (CBT, DBT, mindfulness from documents 1, 2, 5), and lifestyle/psychosocial strategies (exercise, coaching, holistic approaches from documents 2 and 5). No single-modality bias is present.
- **Level Justification**: All three sub-criteria are met with strong evidence from multiple authoritative and relevant sources. The coverage spans stimulants, non-stimulants, multiple therapy modalities, and lifestyle/neurostimulation options. The overall collection provides comprehensive multimodal coverage for adult ADHD.
- **Contrastive Fail Triggered**: No

### 3. actionable_clinical_detail (Score: 0.72, Level: L4) ✅
- **Weight**: 0.21
- **Reasoning**: The documents collectively name specific stimulant and non-stimulant medications and describe multiple therapy approaches with outcome evidence. However, they lack detailed monitoring recommendations, titration guidance, or treatment sequencing steps that would make the information fully actionable for clinical decision-making.
- **Level Justification**: Two of three sub-criteria are fully met (specific medication classes and therapy modalities). The third (monitoring/sequencing) is only partially met, as document 1 offers some first-line recommendations but lacks detailed clinical protocols. This is adequate for an evidence overview but falls short of full clinical actionability.
- **Contrastive Fail Triggered**: No

### 4. _baseline_fidelity (Score: 0.68, Level: L4) ✅
- **Weight**: 0.12
- **Reasoning**: The scraped markdown from all documents preserves the essential content, headings, lists, and tables (where present) without truncation. Some boilerplate and minor formatting issues exist (missing H1, alt text for images, typo), but these do not significantly impair the ability to extract treatment information.
- **Level Justification**: All three conditions are at least partially met. Structural elements are intact, content is complete. Boilerplate is present but not dominating. The scrape scores (L1–L2) indicate minor issues but overall fidelity is adequate for extracting evidence.
- **Contrastive Fail Triggered**: No

### 5. source_authority (Score: 0.90, Level: L5) ✅
- **Weight**: 0.21
- **Reasoning**: All five documents are from authoritative origins: a peer-reviewed systematic review (PMC), a reputable nonprofit with citations (ADDA), an evidence synthesis project referencing BMJ (ADHD Evidence), a government health agency (CDC), and an academic medical institute (UC Davis). Each either is a primary peer-reviewed source or cites recognized clinical guidelines, peer-reviewed journals, or authoritative organizations. No generic wellness blogs, testimonials, or unsupported claims are present. The collective authority is excellent, warranting an L5 score of 0.90.
- **Level Justification**: The set of documents collectively demonstrates high source authority. The majority are from peer-reviewed academic journals (PMC), government agencies (CDC), reputable medical nonprofits (ADDA, ADHD Evidence Project), or academic medical centers (UC Davis). All provide citations to recognized medical sources. No contrastive fail indicators (e.g., personal blogs, unsupported testimonials) are present. The slight variation in authority (e.g., ADDA blog with no individual author credentials) does not detract from the overall strong authority profile, as the blog still cites evidence and comes from a credible organization.
- **Contrastive Fail Triggered**: No

### 6. _baseline_freshness (Score: 0.75, Level: L4) ✅
- **Weight**: 0.07
- **Reasoning**: The retrieved documents collectively meet the baseline freshness requirement. The key evidence documents are from 2023 (Rank 1) and 2023 (Rank 2), with a 2025 umbrella review (Rank 3) adding recent context. No critical outdatedness is present. The set is temporally appropriate for an evidence-based clinical query, scoring in the Adequate range (L4, 0.75).
- **Level Justification**: The most relevant documents (Ranks 1, 2, 5) have publication or update dates in 2023 or later, satisfying the temporal appropriateness criterion. Rank 1's systematic review covers studies up to 2019 but is itself from late 2023. Rank 3 (2025) is recent but less relevant. No document is clearly outdated. However, the set does not achieve 'excellent' because Rank 1 only covers literature up to 2019 and Rank 5 lacks explicit freshness markers. Therefore, the freshness is adequate (L4, score 0.75).
- **Contrastive Fail Triggered**: No

### 7. _baseline_fidelity (Score: 0.28, Level: L2) ❌
- **Weight**: 0.12
- **Reasoning**: Aggregated fidelity score from 5 pages.
- **Level Justification**: Computed average score is 0.28
- **Contrastive Fail Triggered**: YES ⚠️
- **Failure Explanation**: Average scrape quality is poor

### Document Profiles Evaluated
| Rank | URL | Domain Type | Words | Headings | Tables | Completeness |
|------|-----|-------------|-------|----------|--------|--------------|
| 1 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10730462/ | N/A | 0 | 0 | 0 | unknown |
| 2 | https://add.org/adhd-therapies/ | N/A | 0 | 0 | 0 | unknown |
| 3 | https://www.adhdevidence.org/blog/evidence-based-interventions-for-adhd | N/A | 0 | 0 | 0 | unknown |
| 4 | https://www.cdc.gov/adhd/treatment/index.html | N/A | 0 | 0 | 0 | unknown |
| 5 | https://health.ucdavis.edu/mind-institute/resources/understanding-adhd/adhd-treatment | N/A | 0 | 0 | 0 | unknown |


## Failure Diagnosis & Recovery Roadmap
- **Failure Dimensions**: `_baseline_ranking, _baseline_fidelity (Critical: _baseline_ranking, _baseline_fidelity)`
- **Root Cause**: The ranking algorithm places Rank 4 (https://www.cdc.gov/adhd/treatment/index.html, query_relevance=0.1, authority=1.0) and Rank 3 (https://www.adhdevidence.org/blog/evidence-based-interventions-for-adhd, query_relevance=0.4) above Rank 5 (https://health.ucdavis.edu/mind-institute/resources/understanding-adhd/adhd-treatment, query_relevance=0.95, authority=0.95), indicating the ranker is weighting domain authority over semantic relevance to the 'adult ADHD' query. Additionally, the aggregated scrape fidelity is 0.284 (L2) because every page scores 0.20-0.40 due to boilerplate leakage (PMC gov banner, ADDA share buttons/comment sections) and missing structural elements (H1 titles, embedded images).

### Diagnostic Breakdown
- **Coverage Diagnosis**: No significant coverage gap — treatment_modality_coverage is 0.93 (L5). However, Rank 5 (UC Davis) has a critical content gap: 'Missing pharmacological treatment options (e.g., stimulants, non-stimulants) which are first-line evidence-based treatments for adult ADHD,' meaning its individual coverage is partial despite high relevance.
- **Ranking Diagnosis**: Rank 5 (UC Davis, relevance 0.95, authority 0.95) is buried behind Rank 3 (ADHD Evidence, relevance 0.4) and Rank 4 (CDC, relevance 0.1). The CDC page is entirely about child/adolescent ADHD treatment and should not appear in the top 5 for an adult-specific query. The ranker appears to boost high-authority government domains regardless of query-relevance signals.
- **Scrape Diagnosis**: All five pages have scrape_score ≤ 0.40. Rank 1 (PMC, scrape_score=0.20) retains gov banner and NLM disclaimer boilerplate. Rank 2 (ADDA, scrape_score=0.40) is missing H1 and includes share buttons, comment sections, and refund popups. Rank 4 (CDC, scrape_score=0.20) has no listed issues yet scores 0.20, suggesting the scoring heuristic may be overly punitive for government pages with standard navigation chrome.

### Recommended Fix Actions
- Adjust the ranking scoring function to apply a query-relevance penalty multiplier (e.g., relevance^2) so that pages with relevance < 0.3 cannot outrank pages with relevance > 0.9, regardless of authority score — this would push the CDC child-ADHD page (relevance 0.1) below the UC Davis page (relevance 0.95).
- Add a query-term-matching filter that demotes pages whose primary_topic or key_claims do not contain the query's key entity ('adult') — the CDC page's section summaries explicitly reference 'children younger than 6 years' and 'children 6 years and older,' which should trigger a demotion for an adult-focused query.
- Enhance the scraper's boilerplate removal pipeline to strip gov banners, NLM disclaimers, cookie consent overlays, share-button clusters, comment sections, and 'related posts' blocks before markdown conversion, and inject a synthetic H1 from the page title field when no H1 is detected in the body.
