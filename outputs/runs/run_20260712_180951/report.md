# Firecrawl Eval Report: run_20260712_180951
Generated: 2026-07-12 19:22:12

## Run Configuration
| Setting | Value |
|---|---|
| Generator Model | minimax/minimax-m3 |
| P1 Model (Extraction) | deepseek/deepseek-v4-flash |
| P2 Model (Reasoning)  | deepseek/deepseek-v4-flash |
| Improvement Agent | z-ai/glm-5.2 |
| Pass Threshold | 0.65 (floor: 0.4) |
| Test Cases | 30 |
| Duration | 72m 21s |

## Executive Summary
- **Overall Score**: 0.69 🟡
- **Test Cases**: 30 | Passed: 0 | Failed: 30

### Floor Failures (Dimension Score < 0.40)
- **TCs with floor failures**: 30 / 30
- **Most common floor dimension**: `_baseline_fidelity` (34 TCs)

## Dimension Performance Breakdown
| Dimension | Weight (avg) | Avg Score | Pass Rate | Floor Fails | Histogram |
|-----------|-------------|-----------|-----------|-------------|-----------|
| real_world_vs_theoretical | 0.10 | 0.15 | 0.0% | 1 | <pre>  0.0-0.2  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| whole_grain_compatibility | 0.15 | 0.15 | 0.0% | 1 | <pre>  0.0-0.2  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| structural_fidelity | 0.12 | 0.22 | 0.0% | 2 | <pre>  0.0-0.2  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| data_completeness | 0.15 | 0.25 | 0.0% | 3 | <pre>  0.0-0.2  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| multi_hop_synthesis | 0.24 | 0.28 | 0.0% | 3 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  3<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| comparative_context_recovery | 0.21 | 0.28 | 0.0% | 2 | <pre>  0.0-0.2  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| actionability | 0.24 | 0.30 | 0.0% | 1 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| multi_constraint_coverage | 0.19 | 0.35 | 0.0% | 1 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| _baseline_fidelity | 0.12 | 0.40 | 7.3% | 34 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  1<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  33<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  17<br>  0.6-0.8  ▓░░░░░░░░░░░░░░░░░░░  3<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  1<br></pre> |
| technical_depth | 0.15 | 0.45 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| _baseline_ranking | 0.12 | 0.48 | 30.0% | 15 | <pre>  0.0-0.2  ▓▓▓░░░░░░░░░░░░░░░░░  2<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  13<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓░░░░░░░░░░░  6<br>  0.6-0.8  ▓▓▓▓▓▓▓░░░░░░░░░░░░░  5<br>  0.8-1.0  ▓▓▓▓▓▓░░░░░░░░░░░░░░  4<br></pre> |
| angle_separation | 0.12 | 0.50 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| practical_bridge | 0.12 | 0.50 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| recency_signals | 0.06 | 0.50 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| temporal_anchor_fidelity | 0.35 | 0.55 | 50.0% | 1 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| regional_distinction | 0.15 | 0.55 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| historical_depth | 0.12 | 0.55 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| temporal_freshness | 0.26 | 0.55 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| contextual_breadth | 0.22 | 0.55 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| technical_accuracy | 0.22 | 0.55 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| bread_baking_functionality | 0.19 | 0.55 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| practical_usage | 0.15 | 0.55 | 0.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| seasonal_coverage | 0.26 | 0.62 | 50.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| coverage | 0.24 | 0.64 | 66.7% | 1 | <pre>  0.0-0.2  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br></pre> |
| source_quality | 0.11 | 0.69 | 75.0% | 1 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br></pre> |
| _baseline_coverage | 0.12 | 0.69 | 75.0% | 1 | <pre>  0.0-0.2  ▓▓▓▓░░░░░░░░░░░░░░░░  1<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓░░░░░░░░░░░░  2<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  5<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░  4<br></pre> |
| cultural_specificity | 0.12 | 0.70 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| source_credibility | 0.19 | 0.70 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| amine_specific_focus | 0.15 | 0.70 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| guideline_treatment | 0.11 | 0.70 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| structural_function | 0.15 | 0.70 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| multi_source_breadth | 0.15 | 0.72 | 50.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| quantitative_specificity | 0.18 | 0.72 | 66.7% | 1 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br></pre> |
| temporal_relevance | 0.19 | 0.72 | 66.7% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| anchor_recovery | 0.20 | 0.72 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| clinical_specificity | 0.17 | 0.72 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| _baseline_authority | 0.07 | 0.73 | 83.3% | 2 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓▓▓▓▓▓▓▓░░░░░░░░░░░░  2<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  5<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  5<br></pre> |
| practical_actionability | 0.17 | 0.75 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| practical_trekking_factors | 0.15 | 0.75 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| source_alignment | 0.12 | 0.75 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| comparative_specificity | 0.12 | 0.75 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| fiber_focus | 0.12 | 0.75 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| examples_specificity | 0.14 | 0.75 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| dimensional_coverage | 0.24 | 0.78 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br>  0.8-1.0  ░░░░░░░░░░░░░░░░░░░░  0<br></pre> |
| temporal_currency | 0.23 | 0.79 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  1<br></pre> |
| _baseline_freshness | 0.07 | 0.81 | 95.5% | 1 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ▓░░░░░░░░░░░░░░░░░░░  1<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░  9<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  12<br></pre> |
| source_authority | 0.19 | 0.84 | 88.2% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ▓▓▓░░░░░░░░░░░░░░░░░  2<br>  0.6-0.8  ▓▓▓▓▓░░░░░░░░░░░░░░░  3<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  12<br></pre> |
| topical_coverage | 0.26 | 0.85 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| topical_substance | 0.19 | 0.85 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| comparative_coverage | 0.28 | 0.85 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| practical_recommendations | 0.22 | 0.86 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  2<br></pre> |
| topical_coherence | 0.24 | 0.88 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| destination_specificity | 0.17 | 0.90 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| completeness | 0.14 | 0.90 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  3<br></pre> |
| definitional_clarity | 0.17 | 0.90 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| practical_examples | 0.15 | 0.93 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| noise_filtering | 0.15 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| seasonal_specificity | 0.20 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| stem_undergraduate_specificity | 0.21 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| health_risk_specificity | 0.23 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| drift_recovery | 0.23 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| domain_alignment | 0.15 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| driver_lineup_info | 0.24 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| race_calendar_coverage | 0.28 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |
| topic_precision | 0.13 | 0.95 | 100.0% | 0 | <pre>  0.0-0.2  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.2-0.4  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.4-0.6  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.6-0.8  ░░░░░░░░░░░░░░░░░░░░  0<br>  0.8-1.0  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  1<br></pre> |

## Most Frequently Unmet Rubric Criteria
| Condition (truncated) | Times Not Met |
|---|---|
| Higher-authority and more relevant sources appear before lower-quality ones. | 6 |
| Content is complete without truncation | 4 |
| Higher-authority sources appear before lower-quality ones | 3 |
| More relevant sources appear before less relevant ones | 2 |
| No boilerplate leakage | 2 |
| Most relevant result is not buried | 2 |
| List its top holdings | 2 |
| Provide percentage allocations for each holding | 2 |

### Executive Diagnosis
This run achieved a pass rate of **0%** across 30 test cases. The primary bottleneck identified is **Scrape score inversion: complete documents receive 0.20 while truncated fragments receive 0.60-0.79**, impacting 10/30 TCs of the evaluated queries. Addressing the key root causes could yield a significant boost in performance, particularly on the **_baseline_fidelity** dimension.

## Batch Progression (KB Build)
| Round | TCs | New Indexed | Deduped (Hits) |
|-------|-----|-------------|----------------|
| 1 | 1 | 0 | 0 |
| 2 | 1 | 0 | 0 |
| 3 | 1 | 0 | 0 |
| 4 | 1 | 0 | 0 |
| 5 | 1 | 0 | 0 |
| 6 | 1 | 0 | 0 |
| 7 | 1 | 0 | 0 |
| 8 | 1 | 0 | 0 |
| 9 | 1 | 0 | 0 |
| 10 | 1 | 0 | 0 |
| 11 | 1 | 0 | 0 |
| 12 | 1 | 0 | 0 |
| 13 | 1 | 0 | 0 |
| 14 | 1 | 0 | 0 |
| 15 | 1 | 0 | 0 |
| 16 | 1 | 0 | 0 |
| 17 | 1 | 0 | 0 |
| 18 | 1 | 0 | 0 |
| 19 | 1 | 0 | 0 |
| 20 | 1 | 0 | 0 |
| 21 | 1 | 0 | 0 |
| 22 | 1 | 0 | 0 |
| 23 | 1 | 0 | 0 |
| 24 | 1 | 0 | 0 |
| 25 | 1 | 0 | 0 |
| 26 | 1 | 0 | 0 |
| 27 | 1 | 0 | 0 |
| 28 | 1 | 0 | 0 |
| 29 | 1 | 0 | 0 |
| 30 | 1 | 0 | 0 |

## Two-Layer Cache Analytics
- **Layer 1 (Query) Cache Hit Rate**: 6.7% (2/30)
- **Layer 2 (Content) Cache Hit Rate**: 13.0% (16/123)

### Cache Intent Validation
*(Did the generator successfully trick the cache?)*
| Generator Intent | Count | Query Hit % | Content Hit % |
|------------------|-------|-------------|---------------|
| `novel` | 20 | 0.0% | 0.0% |
| `rephrased_same_intent` | 3 | 0.0% | 45.5% |
| `same_source_different_angle` | 2 | 0.0% | 0.0% |
| `exact_duplicate` | 2 | 100.0% | 100.0% |
| `subset_of_parent` | 3 | 0.0% | 14.3% |

## Chaos Archetype Analysis
| Archetype | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| multi_hop_compressed ⚠️ | 3 | 0.51 | 0.0% |
| over_decomposed ⚠️ | 5 | 0.61 | 0.0% |
| reformulation_drift ⚠️ | 5 | 0.64 | 0.0% |
| none ⚠️ | 7 | 0.69 | 0.0% |
| keyword_stuffed ⚠️ | 3 | 0.70 | 0.0% |
| temporal_ambiguity ⚠️ | 7 | 0.85 | 0.0% |

## Intent × Difficulty Analysis

### By Intent
| Intent | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| data_extraction | 4 | 0.60 | 0.0% |
| comparative_research | 8 | 0.60 | 0.0% |
| tutorial_howto | 3 | 0.61 | 0.0% |
| exploratory | 9 | 0.72 | 0.0% |
| factual_lookup | 6 | 0.85 | 0.0% |

### By Difficulty
| Difficulty | TCs | Avg Score | Pass Rate |
|---|---|---|---|
| hard | 7 | 0.63 | 0.0% |
| medium | 23 | 0.70 | 0.0% |

## Retrieval Comparison: Firecrawl vs KB vs Ideal
*(Evaluates if our RRF Hybrid KB outperforms Firecrawl's native ranking)*

| Metric | Firecrawl | Internal KB | Winner |
|--------|-----------|-------------|--------|
| Kendall's τ (vs Ideal, normalized 0→1) | 0.543 | 0.533 | Firecrawl 🏆 |
| Overlap@3 (vs Ideal) | 0.644 | 0.367 | Firecrawl 🏆 |
| Overlap@5 (vs Ideal) | 1.000 | 0.367 | Firecrawl 🏆 |
| KB Outperforms FC | - | - | 43.3% of TCs |

## Improvement Roadmap

### Root Causes (ranked by severity)
| # | Dimension | Issue | Severity | Confidence | Affected TCs | Frequency |
|---|-----------|-------|----------|------------|--------------|-----------|
| 1 | _baseline_fidelity | Scrape score inversion: complete documents receive 0.20 while truncated fragments receive 0.60-0.79 | high | high | tc_3b095b54, tc_316e5e79, tc_531d905d... | 10/30 TCs |
| 2 | _baseline_ranking | Thin social media/forum content (word_count < 50, authority < 0.3) systematically outranks comprehensive authoritative sources | high | high | tc_3b095b54, tc_c6c18688, tc_9695f75c... | 13/30 TCs |
| 3 | coverage | Multi-hop query decomposition failure: retrieval returns only single-hop results, leaving critical data dimensions uncovered | high | high | tc_0c0014af, tc_ec3ed7e2, tc_35529ad7... | 4/30 TCs |
| 4 | _baseline_ranking | Error pages, captcha challenges, and empty scrapes are not filtered from result sets and pollute ranking positions | medium | high | tc_21e3b4aa, tc_316e5e79, tc_fee03e5a... | 5/30 TCs |
| 5 | comparative_context_recovery | Comparative research intent eroded by over-decomposition into narrow entity-specific tokens, losing cross-entity comparison context | medium | medium | tc_548fb6e6, tc_f748b907, tc_0c0014af | 3/30 TCs |

### Proposals (ranked by priority)
| # | Targets | Proposal | Expected Impact | Effort | Priority |
|---|---------|----------|-----------------|--------|----------|
| 1 | rc_001 | Replace hardcoded scrape_score floor with content-based scoring function | +0.25 on _baseline_fidelity dimension (from 0.397 to ~0.65), +0.08 overall | low | 9.0 |
| 2 | rc_002 | Implement content-density and authority composite ranking gate | +0.15 on _baseline_ranking dimension (from 0.481 to ~0.63), +0.06 overall | medium | 4.5 |
| 3 | rc_004 | Add error-page detection and content-completeness gate before final ranking | +0.10 on _baseline_ranking for affected TCs, +0.05 on _baseline_fidelity, +0.04 overall | low | 4.0 |
| 4 | rc_003 | Implement multi-hop query decomposition with cross-hop coverage re-ranking | +0.30 on coverage dimension for multi-hop queries, +0.20 on multi_hop_synthesis, +0.10 overall | high | 2.0 |
| 5 | rc_005 | Add intent-classification pre-pass with competitor entity injection for comparative queries | +0.25 on comparative_context_recovery, +0.15 on _baseline_ranking for comparative queries, +0.05 overall | medium | 2.0 |

### Quick Wins
| # | Action | Description | Expected Impact |
|---|--------|-------------|-----------------|
| 1 | Fix scrape_score default floor from 0.20 to 0.85 for complete documents | The single highest-impact fix: change the hardcoded 0.20 floor to a computed score where content_completeness='complete' with word_count > 500 maps to scrape_score >= 0.85. This is a one-line formula change that would immediately fix 10+ TCs where the scrape scoring is inverted. | +0.25 on _baseline_fidelity, +0.08 overall |
| 2 | Filter error pages and empty scrapes from result sets | Add a 5-line post-scrape filter: if has_content=false OR content_length=0 OR content_completeness in ['error_page', 'navigation_only'], remove the result and backfill. This eliminates error pages, captcha challenges, and empty social media scrapes from polluting rankings. | +0.05 overall, eliminates 5 TC ranking poisonings |
| 3 | Add word_count < 50 ranking penalty for social media domains | Apply a simple rule: if domain is in [reddit.com, facebook.com, instagram.com, tiktok.com, quora.com] AND word_count < 50, apply a 0.5x ranking penalty. This prevents 17-word Reddit comments and 23-word Instagram reels from occupying top positions. | +0.10 on _baseline_ranking, +0.04 overall |
| 4 | Add scrape_score sanity assertion: complete docs must score higher than truncated docs | Add a unit test / runtime assertion that rejects any scoring profile where content_completeness='complete' with word_count > 500 receives a lower scrape_score than content_completeness='appears_truncated' with word_count < 100. This catches the inversion bug before it propagates. | Prevents regression of the scrape_score inversion bug across all future TCs |

### Cross-Dimension Failure Patterns
| Pattern | Hypothesis / Context |
|---------|----------------------|
| Scrape score inversion cascades into ranking failures: inverted scrape_scores mask content quality from ranking algorithm | When truncated social media posts receive scrape_score=0.79 and complete articles receive scrape_score=0.20, the ranking pipeline (which may use scrape_score as a feature) is fed inverted quality signals. This causes thin content to rank above comprehensive sources, simultaneously failing _baseline_fidelity AND _baseline_ranking. Observed in tc_3b095b54, tc_a7f33ea8, tc_531d905d, tc_b7028fb4 where both dimensions fail together. |
| Social media domain pollution causes compounding failures across _baseline_fidelity, _baseline_ranking, and source_authority | Social media domains (reddit.com, facebook.com, instagram.com) consistently fail to scrape (has_content=false in 11/14 appearances), yet occupy top ranking positions. This creates a triple failure: (1) _baseline_fidelity fails because the scraped content is empty/truncated, (2) _baseline_ranking fails because the empty result outranks complete authoritative sources, and (3) source_authority fails because the portfolio is dominated by low-credibility forum content. Observed in tc_c6c18688, tc_0aff21d2, tc_5cad7b97, tc_f44db2a2. |
| Multi-hop coverage gaps in data_extraction and comparative_research intents cause simultaneous failures in coverage, multi_hop_synthesis, and data_completeness | Queries requiring multi-hop reasoning (e.g., 'largest SWF by AUM AND its top holdings with allocation percentages') are treated as single-hop lookups by the retrieval pipeline. The system retrieves documents satisfying only the first hop (identifying the entity) but not subsequent hops (holdings, allocations). This causes coverage, multi_hop_synthesis, and data_completeness to all score at L1-L2 simultaneously. Observed in tc_0c0014af (coverage=0.1, multi_hop_synthesis=0.25, data_completeness=0.1), tc_ec3ed7e2 (all three at 0.3), tc_35529ad7 (all three at 0.3-0.35). |
| Intent erosion from over-decomposition causes comparative_context_recovery and _baseline_ranking to fail together | Comparative research queries are decomposed into narrow entity-specific tokens, causing the retrieval pipeline to return only single-entity results. This simultaneously kills comparative_context_recovery (no cross-entity comparison content) and degrades _baseline_ranking (the most relevant comparative sources are never retrieved). Observed in tc_548fb6e6 (comparative_context_recovery=0.05, _baseline_ranking=0.15) and tc_f748b907 (comparative_context_recovery=0.25, _baseline_ranking=0.25). |
| Paywalled academic content causes _baseline_fidelity and _baseline_ranking to fail together via navigation-only capture | Academic publisher pages (ScienceDirect, AJC Online) behind paywalls return navigation-only content (nav_link_ratio > 0.7, word_count < 100) when scraped. These near-empty pages sometimes rank highly due to high domain authority, simultaneously failing _baseline_fidelity (poor scrape) and _baseline_ranking (empty content occupying positions above complete sources). Observed in tc_087d6cbc (ajconline.org rank 1, scrape_score=0.20, nav_link_ratio=0.9) and tc_316e5e79 (ScienceDirect captcha page at rank 1). |

### Judge Bias Warnings
- ⚠️ Dual _baseline_fidelity scoring contradiction: The same _baseline_fidelity dimension is evaluated twice per TC with drastically different results — e.g., tc_a345a697 scores 0.9 (L5) on the first evaluation and 0.312 (L2) on the second for the same documents; tc_e4e371ec shows the same pattern. The first evaluator correctly recognizes faithful content preservation while the second applies a hardcoded 0.20 floor. This is not judge bias per se but a pipeline calibration defect where one scorer is broken and the other is correct — the broken scorer's low scores are dragging overall TC scores below pass thresholds despite the correct scorer giving high marks.
- ⚠️ source_authority scores HIGH (avg 0.838, 12/17 TCs in 0.8-1.0) while per_tc_diagnoses show FAILING root causes in source authority for tc_c6c18688 (0.35, L2), tc_fee03e5a (0.35, L2), and tc_0aff21d2 (0.50, L3). The high average is inflated by TCs where authority was not evaluated (scored as 0 in intent_breakdown but not counted in the distribution). No systematic judge bias detected — the low scores for these TCs are consistent with the documented presence of low-credibility forum/social media sources.

## RL Training Signals
| Signal Type | Count | Output File |
|-------------|-------|-------------|
| DPO Pairs | 23 | dpo_pairs.jsonl |
| Reward Signals | 150 | rewards.jsonl |
| Listwise Rankings | 30 | listwise_rankings.jsonl |
| Contrastive Fail Pairs | 67 | contrastive_fail_pairs.jsonl |
| Query Reformulations | 30 | query_reformulations.jsonl |
| SFT Gold Examples | 0 | sft_gold.jsonl |
| Scrape Quality Labels | 150 | scrape_quality_labels.jsonl |

### Improvement Taxonomy (Micro-Patterns)
| Issue | Severity | Frequency | Description |
|-------|----------|-----------|-------------|
| scrape_score_inversion |  | 33% | Complete documents with content_completeness='complete' and word_count > 500 receive scrape_score=0.20 (L1) while truncated fragments with word_count < 50 receive scrape_score=0.60-0.79. This inversion is systematic across 10 of 30 TCs and is the single largest contributor to _baseline_fidelity failures. |
| thin_social_media_ranking |  | 43% | Social media posts (Reddit, Facebook, Instagram) with word_count < 50, authority < 0.3, and failed scrapes (has_content=false) systematically occupy top-3 ranking positions above comprehensive authoritative sources with word_count > 1000 and authority > 0.6. The ranking model lacks a content-density floor and does not penalize failed scrapes. |
| multi_hop_decomposition_failure |  | 13% | Queries requiring multi-hop reasoning (identify entity → retrieve entity-specific data → extract quantitative values) are treated as single-hop lookups. The retrieval pipeline returns documents satisfying only the first hop, leaving subsequent hops completely uncovered. This pattern affects all data_extraction and comparative_research queries with multi-hop structure. |
| error_page_rank_poisoning |  | 17% | Error pages (OSTI 500 error, ScienceDirect captcha, Quora 'Something went wrong'), empty scrapes (has_content=false, content_length=0), and navigation-only captures (nav_link_ratio > 0.7) are not filtered from result sets and occupy ranking positions above legitimate content. These results have authority=0.0 and relevance=0.0 yet appear at ranks 1-5. |
| intent_erosion_over_decomposition |  | 10% | Comparative research queries are decomposed into narrow entity-specific tokens, losing the cross-entity comparison intent. The pipeline retrieves only single-entity results (e.g., NBA-only pages for a sports streaming comparison query) with zero comparative context, causing comparative_context_recovery to score at L1 (0.05-0.25). |
| paywalled_academic_content_pollution |  | 10% | Academic publisher pages behind paywalls (ScienceDirect, AJC Online) return navigation-only content when scraped, yet their high domain authority causes them to rank above complete open-access sources. The scraper does not detect paywall blocks and the ranking model does not penalize navigation-only captures. |

## Regression vs Previous Run
- Trend: Regression Detected ⚠️
- Difference: -0.16

## Appendix: Failed Test Cases Detail
*(Showing only test cases that failed the pass threshold or hit a dimension floor)*

### tc_3b095b54 (Score: 0.76) ❌
**Query**: `Lisbon Portugal neighborhoods Alfama Bairro Alto Belem tram 28 transit accommodation restaurants itinerary guide`
**Category**: Travel & Geography | **Intent**: novel

**Root Cause**: Two compounding failures drive the test case failure: (1) the ranking model places three low-authority, truncated social media posts (authority 0.1–0.2, relevance 0.3–0.5) at ranks 1, 2, and 4 above two comprehensive travel blogs (relevance 0.95, authority 0.4–0.6) at ranks 3 and 5, and (2) the scrape scoring model assigns scrape_score=0.20 to complete blog posts (ranks 3 and 5) whose only issues are minor alt-text gaps and affiliate disclosures, while assigning scrape_score=0.79 to a severely truncated Facebook post (rank 4) that captures only a single sentence — this inversion drags the aggregated fidelity score to 0.2946.

- **Coverage Diagnosis**: Coverage is not a gap — document profiles for ranks 3 and 5 collectively cover all named neighborhoods, tram 28, transit, accommodation, restaurants, and itinerary. The only minor gap is thin accommodation listings (one specific hotel in Doc 3, neighborhood-level only in Doc 5).
- **Ranking Diagnosis**: Ranks 1, 2, and 4 are occupied by social media posts (Instagram reel, two Facebook posts) with authority_score 0.1–0.2 and query_relevance_score 0.3–0.5, while the two most relevant and authoritative sources (travelforlifenow.com at authority 0.6/relevance 0.95 and roamwithross.com at authority 0.4/relevance 0.95) are buried at ranks 3 and 5. This is a clear authority-and-relevance signal inversion in the ranking pipeline.
- **Scrape Diagnosis**: Scrape scores are inverted relative to content completeness: Rank 3 (travelforlifenow.com, 3783 words, content_complete='complete') receives scrape_score=0.20 for minor alt-text and affiliate disclosure issues, while Rank 4 (Facebook, 25 words, content_complete='appears_truncated') receives scrape_score=0.79 despite capturing only one sentence. Rank 5 (roamwithross.com, 2494 words, complete) also receives 0.20 for embedded media and boilerplate repetition. The scoring model over-weights cosmetic issues on complete pages and under-weights critical truncation on social media pages.

**Fix Actions**:
- Add a domain-type authority boost in the ranking config: down-rank commercial social media domains (instagram.com, facebook.com) by a minimum penalty factor when page_type is 'other' or 'forum_thread' and content_complete is 'appears_truncated', ensuring travel blog posts with authority_score >= 0.4 and query_relevance_score >= 0.9 always rank above truncated social media posts.
- Fix the scrape_score calculation to weight content_completeness as a dominant factor: if content_completeness='appears_truncated' and word_count < 100, cap scrape_score at 0.30 regardless of other issues; conversely, if content_completeness='complete' and word_count > 1000, floor scrape_score at 0.70 even when minor issues (missing alt text, affiliate disclosures, embedded media) are present.
- Add a social-media-specific scraper fallback: when scraping instagram.com or facebook.com URLs, if the initial scrape yields word_count < 50, mark the result as low-fidelity and trigger a re-scrape with JavaScript rendering enabled or exclude the URL from the result set entirely.


---
### tc_a211b3c3 (Score: 0.96) ❌
**Query**: `latest research on psychedelic assisted therapy for mental health conditions`
**Category**: Science & Academia | **Intent**: novel

**Root Cause**: The test case failed because scrape fidelity is critically low across all five documents: Rank 5 (https://medicine.utah.edu/psychiatry/research/labs/upsi) has scrape_score=0.20 with unresolved relative image paths, Ranks 1-3 each have scrape_score=0.40 with boilerplate/navigation contamination and missing media, and Rank 4 has scrape_score=0.60 with unextracted tables. This triggered the contrastive fail ('Average scrape quality is poor') on the second temporal_anchor_fidelity dimension, scoring 0.34 at L2 and dragging the overall weighted score below the pass threshold.

- **Coverage Diagnosis**: No observable coverage gap; topical_coverage scored L5 with all five criteria MET, covering clinical trial phases, regulatory developments, multiple compounds (MDMA, psilocybin, ketamine, LSD, ibogaine), and multiple conditions (PTSD, depression, substance use disorders, cancer distress).
- **Ranking Diagnosis**: Minor temporal ordering deviation: the 2018 PMC article (https://pmc.ncbi.nlm.nih.gov/articles/PMC6041963/) at rank 2 precedes more recent sources at ranks 3-5 for a 'latest research' query, but this is a minor issue (PARTIALLY_MET on one checklist item) and not the primary failure driver.
- **Scrape Diagnosis**: Systemic scrape quality failure: all five documents score below 0.7 on scrape_score. Specific issues include unresolved relative image paths (public://) at Rank 5, unextracted table contents at Rank 4, missing figures at Rank 2, excessive navigation/boilerplate contamination at Ranks 2-3, and non-functional interactive elements (video, forms) at Rank 1. The average scrape_score of 0.40 triggered the contrastive fail condition.

**Fix Actions**:
- Implement a boilerplate and navigation removal pass in the scrape pipeline using DOM-based content extraction (e.g., Readability-style main-content detection) to strip nav menus, footers, and sidebar elements before markdown conversion, targeting the 'Excessive navigation menu included' and 'Boilerplate footer included' issues at Ranks 2-3.
- Add a table-to-markdown extraction step that parses HTML <table> elements and converts them to GitHub-flavored markdown tables, resolving the 'Table contents not extracted into markdown; only placeholder links present' issue at Rank 4 (https://www.ccjm.org/content/92/3/171).
- Add a URL resolver for relative image paths (e.g., public://, /sites/default/files/) that converts them to absolute URLs or downloads and embeds images as base64, fixing the scrape_score=0.20 at Rank 5 (https://medicine.utah.edu/psychiatry/research/labs/upsi).


---
### tc_9a8d344d (Score: 0.73) ❌
**Query**: `When is the best season to go trekking in Patagonia?`
**Category**: Travel & Geography | **Intent**: rephrased_same_intent

**Root Cause**: The primary failure is a ranking inversion where a truncated Reddit post (rank 2, authority 0.05, relevance 0.4) outranks high-authority sources like Swoop (rank 4) and Aurora (rank 5, relevance 1.0), compounded by the Reddit post's severe truncation causing a fidelity contrastive fail.

- **Coverage Diagnosis**: The document profiles lack sub-regional variation in optimal trekking timing, treating Patagonia as a single homogeneous destination despite mentioning multiple locations like Torres del Paine and El Chalten.
- **Ranking Diagnosis**: Rank 2 (reddit.com) is positioned above Rank 4 (swoop-patagonia.com) and Rank 5 (aurora-expeditions.com), inverting the expected authority and relevance order.
- **Scrape Diagnosis**: Rank 2 (reddit.com) has a scrape_score of 0.6 with content truncated after the first sentence (word_count 29), triggering a contrastive fail in fidelity.

**Fix Actions**:
- Adjust the ranking algorithm to penalize forum threads with low word counts or truncated content, ensuring commercial/expert guides with high relevance are ranked above them.
- Implement a scrape fallback or wait-for-selector configuration for Reddit threads to capture the full post body and comments instead of just the first sentence.
- Add a query expansion or reranking signal that boosts documents containing sub-regional comparisons (e.g., 'Torres del Paine vs El Chalten weather') to improve regional distinction coverage.


---
### tc_c6c18688 (Score: 0.59) ❌
**Query**: `Lisbon Alfama Bairro Alto Belem history cultural heritage origins fado maritime discoveries evolution architecture neighborhood identity`
**Category**: Travel & Geography | **Intent**: same_source_different_angle

**Root Cause**: The ranking inverts quality: Rank 5 (https://www.debritoproperties.com/en-gb/alfama, auth=0.5, rel=0.65) is buried last while Rank 1 (https://www.facebook.com/groups/lisbontraveltips/posts/968175351757056/, auth=0.2, word_count=23) is promoted to the top. Simultaneously, two Facebook pages (Doc1 at 23 words, Doc2 at 22 words) are severely truncated, and no document in the set provides historical origins or evolution for Bairro Alto, creating a critical coverage gap.

- **Coverage Diagnosis**: Bairro Alto is mentioned substantively only in Doc4 (https://www.insidelisbon.com/en/blogpost/lisbon-neighborhoods-guide) and solely as a nightlife area ('over 200 bars and restaurants') with zero historical origins, evolution, or architectural context. The query explicitly requests 'Bairro Alto history cultural heritage origins' but no retrieved document satisfies this sub-intent.
- **Ranking Diagnosis**: Rank 5 (auth=0.5, rel=0.65) is placed last while Rank 1 (auth=0.2, rel=0.6, truncated to 23 words) is first. Rank 2 (official Visit Lisboa, auth=0.5, rel=0.3, truncated to 22 words) is second despite having the lowest relevance score. The ranking is non-monotonic on both authority and relevance, triggering the contrastive fail.
- **Scrape Diagnosis**: Doc1 (https://www.facebook.com/groups/lisbontraveltips/posts/968175351757056/) scraped only 23 words ending with ellipsis; Doc2 (https://www.facebook.com/visitlisboa/posts/...) scraped only 22 words with no structural elements. Doc5 (https://www.debritoproperties.com/en-gb/alfama) has duplicated content blocks repeated 3-4 times and an irrelevant Campo de Ourique paragraph inserted mid-content. Doc3 (https://angiesweb.com/lisbon-portugal/) has scrape_score=0.20 with images not embedded and comment section placeholders.

**Fix Actions**:
- Add a Facebook-specific scrape handler that expands collapsed 'See more' content and waits for dynamic post body rendering, preventing the 23-word and 22-word truncations seen in Doc1 and Doc2.
- Implement a deduplication pass in the scrape pipeline that detects and collapses repeated content blocks (as seen in Doc5 where history and 'Why choose' sections repeat 3-4 times) before outputting markdown.
- Adjust the retrieval ranking signal to penalize severely truncated documents (word_count < 100) by demoting them below complete documents, ensuring Rank 5-quality content is not buried beneath 23-word fragments.
- Add a query expansion step that decomposes multi-entity queries (e.g., 'Alfama Bairro Alto Belém') into per-entity sub-queries and merges results, ensuring each named entity receives at least one dedicated result.


---
### tc_0c0014af (Score: 0.39) ❌
**Query**: `top fossil fuel producers most vulnerable to climate change and their net zero target years`
**Category**: Environment & Climate | **Intent**: novel

**Root Cause**: The retrieval pipeline returned generic climate policy overviews (UN net-zero coalition, IEA global pathway, US State Department) that each cover one isolated aspect of the query but none intersect fossil-fuel-producer rankings with climate-vulnerability rankings. As evidenced by Doc1's critical content gap 'No discussion of vulnerability of fossil fuel producers to climate change impacts' and Doc5's gap 'No net zero target years for any fossil-fuel-producing countries except the United States,' the query formulation and ranking logic failed to retrieve comparative country-level data bridging all three required hops.

- **Coverage Diagnosis**: All five documents are rated tangential or partial; zero documents identify specific countries appearing on both fossil-fuel-producer and climate-vulnerability rankings, and only one country's net-zero target year (US, 2050) appears across the entire set.
- **Ranking Diagnosis**: The Facebook post (https://www.facebook.com/groups/environmentandclimatenews/posts/2330673597128951/, authority_score=0.1, query_relevance_score=0.1) is ranked 4th, ahead of the U.S. State Department page (https://2021-2025.state.gov/climate-crisis/, authority_score=0.9, query_relevance_score=0.2) at rank 5, violating authority-based ordering for a low-quality social media result.
- **Scrape Diagnosis**: Ranks 1, 2, and 5 all have scrape_score=0.20 due to unextracted video/media elements and boilerplate navigation; Rank 4 (Facebook) is severely truncated with only 25 words scraped and content_completeness='appears_truncated', making it unusable.

**Fix Actions**:
- Add a domain blocklist filter to exclude social media platforms (facebook.com, twitter.com, x.com, reddit.com) from search results for comparative_research intent queries, preventing low-authority truncated content from occupying result slots.
- Implement a query expansion pipeline for multi-hop comparative queries that decomposes the query into sub-queries (e.g., 'top fossil fuel producing countries ranking', 'climate vulnerability index by country', 'net zero target year by country') and merges results to ensure coverage of each hop before final ranking.
- Add a scrape post-processing step that strips login/signup popups, video player error messages, and modal dialogs from government and organizational pages (un.org, iea.org, state.gov) to improve scrape_score above 0.40 for text-complete pages.


---
### tc_69806b76 (Score: 0.65) ❌
**Query**: `latest archaeological discoveries transforming scholarly understanding of ancient Egypt`
**Category**: History & Humanities | **Intent**: novel

**Root Cause**: The ranking model placed a 2023 travel blog (insightvacations.com, authority_score=0.4, scrape_score=0.2) at rank 1 while burying the most authoritative and fully relevant result (penn.museum press release, authority_score=1.0, query_relevance=0.9, coverage_level=full) at rank 5. This authority inversion cascaded into failures across temporal_freshness (stale 2023 top result), _baseline_ranking (contrastive fail: blog above official sources), and _baseline_fidelity (3 of 5 documents at scrape_score=0.2).

- **Coverage Diagnosis**: Only 1 of 5 documents (Doc5, penn.museum) achieves full query coverage; Doc1, Doc2, Doc3 all explicitly miss the 'transforming scholarly understanding' aspect, and Doc4 (qz.com) covers only 18th–20th century discoveries despite the query requesting 'latest' findings. The result set lacks analytical depth on scholarly impact.
- **Ranking Diagnosis**: The most relevant and authoritative result (penn.museum, authority=1.0, relevance=0.9) is at rank 5, while the least authoritative (insightvacations.com, authority=0.4) is at rank 1. PBS (authority=0.9) is at rank 3, below both the travel blog and a YouTube video (authority=0.5, relevance=0.4). This is a clear authority-weighting failure.
- **Scrape Diagnosis**: Three documents (Doc1 insightvacations.com, Doc4 qz.com, Doc5 penn.museum) have scrape_score=0.2 (L1) with issues including generic image alt text, duplicated social share markup, and unrendered images. Doc2 (youtube.com) has a 403 Forbidden error with scrape_score=0.6. The aggregated fidelity score of 0.284 (L2) confirms systemic scrape degradation.

**Fix Actions**:
- Increase authority_score weight in the ranking model by at least 2x relative to query_relevance_score so that domains with authority_score >= 0.9 (penn.museum, pbs.org) outrank domains with authority_score <= 0.5 (insightvacations.com, youtube.com) when query_relevance differentials are < 0.3.
- Add a temporal recency boost penalty: documents with publication_date older than 12 months relative to the current date should receive a 0.3 multiplicative penalty to their final ranking score when the query contains 'latest' or 'recent' temporal intent markers.
- Fix the scraper's image rendering pipeline for press release and blog page types: extract and inline image URLs as markdown image tags with descriptive alt text from the page's <img> elements and their aria-label or title attributes, targeting scrape_score improvement from 0.2 to >= 0.5 for pages like penn.museum and qz.com.


---
### tc_ec3ed7e2 (Score: 0.57) ❌
**Query**: `Largest sovereign wealth fund by AUM 2026 and its top holdings with allocation percentages`
**Category**: Finance & Investing | **Intent**: novel

**Root Cause**: All five retrieved documents (swfinstitute.org, ssga.com, globalswf.com, praxisrock.com, bain.com) identify Norway's GPFG as the largest SWF but none contain its top holdings or allocation percentages, as evidenced by Doc1's critical content gap 'Top holdings and allocation percentages for the largest fund are not provided' and Doc3's gap 'No specific top holdings or allocation percentages beyond alternatives and domestic categories.' The retrieval system failed to surface NBIM's official holdings report at nbim.no, which is the only authoritative source for this data.

- **Coverage Diagnosis**: Two of three query components are completely uncovered: (1) top holdings of the largest fund and (2) allocation percentages for those holdings. All five document profiles show coverage_level=tangential or partial with answers_query=false. The system retrieved SWF ranking pages and trend analyses but missed the official fund disclosure page that lists individual holdings with percentages.
- **Ranking Diagnosis**: N/A — ranking scored 0.75 (L4) with no contrastive fail; the issue is coverage, not ordering.
- **Scrape Diagnosis**: Doc1 (swfinstitute.org, scrape_score=0.4) has asset values hidden behind interactive 'View Total Assets' elements, and Doc2 (ssga.com, scrape_score=0.2) has chart data not extracted as text. These are secondary issues; the aggregated fidelity score of 0.256 reflects generally poor scrape quality across the set but does not account for the primary coverage failure.

**Fix Actions**:
- Add nbim.no and its holdings report subpages (e.g., nbim.no/en/the-fund/holdings/holdings-and-equity-trades/) to the crawl seed list and boost their domain authority weight in the ranking model for queries mentioning 'holdings' or 'allocation percentages' alongside sovereign wealth fund names.
- Implement a query decomposition step that splits multi-hop queries into sub-queries (e.g., 'largest sovereign wealth fund by AUM 2026' AND 'Norway GPFG top holdings allocation percentages') and merges results, ensuring the second hop retrieves official fund disclosure pages rather than only ranking databases.
- Configure the scraper to execute JavaScript interactions on swfinstitute.org fund-ranking pages to expand hidden 'View Total Assets' cells, and add OCR/chart-extraction for ssga.com embedded infographics to improve scrape fidelity from 0.2-0.4 to acceptable levels.


---
### tc_21e3b4aa (Score: 0.67) ❌
**Query**: `energy penalty analysis for sorbent regeneration in direct air capture systems`
**Category**: Environment & Climate | **Intent**: novel

**Root Cause**: The test case fails primarily due to two compounding issues: (1) a severe ranking inversion where the OSTI error page (authority=0.0, relevance=0.0) sits at rank 3 and the PatSnap blog (authority=0.6) at rank 4, both above the NETL DOE report (authority=0.98, relevance=0.92) buried at rank 5; and (2) critical scrape truncation of the rank-1 ScienceDirect article (scrape_score=0.60, main body missing after 'Loading...' placeholder). These two failures drag _baseline_ranking to 0.3 (L2) and _baseline_fidelity to 0.284 (L2), which together with a partial technical_depth score of 0.45 (L3, missing thermodynamic minimum work comparison) produce an overall score of 0.6701 below the pass threshold.

- **Coverage Diagnosis**: Coverage is strong (0.85, L5) — the four content-bearing documents collectively provide quantitative energy penalty data (0.5–18.75 GJ/t-CO2, 4.3 GJ/t-CO2, 1,500–2,500 kWh/t), regeneration methods, cost analysis, and policy context. The only coverage gap is the missing thermodynamic minimum work comparison noted in technical_depth, which no document addresses.
- **Ranking Diagnosis**: The ranking is severely inverted: NETL (authority=0.98, relevance=0.92) is at rank 5 while an error page (OSTI, authority=0.0) is at rank 3 and a commercial blog (PatSnap, authority=0.6) is at rank 4. The contrastive fail was explicitly triggered: 'A blog (PatSnap, rank 4) ranks above an official government source (NETL, rank 5)' and 'the most relevant result is buried'. The ideal order would place NETL at rank 1 or 2, remove or demote the OSTI error page, and place PatSnap below all government/academic sources.
- **Scrape Diagnosis**: Two critical scrape failures: (1) ScienceDirect (rank 1, scrape_score=0.60) has its entire main article body missing — content truncated at a 'Loading...' placeholder, leaving only metadata, abstract, highlights, and keywords (word_count=460); (2) OSTI (rank 3, scrape_score=0.20) returned an error page with zero substantive content (word_count=42, content_completeness='error_page'). The remaining three documents (ORNL, PatSnap, NETL) have acceptable scrape quality (scores 0.20–0.40 with only minor issues).

**Fix Actions**:
- Implement a post-scrape error-page detector that checks for boilerplate error patterns (e.g., 'An unexpected error has occurred', HTTP 4xx/5xx status codes, word_count < 100 with nav_link_ratio > 0.8) and either triggers a re-scrape with alternate rendering (e.g., headless browser with JavaScript enabled) or removes the URL from the result set and backfills from a fallback candidate — this would have caught the OSTI error page at rank 3.
- Add a JavaScript-rendering fallback for ScienceDirect/Elsevier pages that detect 'Loading...' placeholder text in the scraped markdown, triggering a wait-for-network-idle or explicit selector-wait for the article body container before extracting content — this would have recovered the truncated main body of the rank-1 article.
- Introduce an authority-weighted re-ranking pass that demotes URLs with scrape_level='L1' and content_completeness='error_page' to the bottom of results, and boosts .gov and national-lab domains above commercial blogs when relevance scores are within 0.1 of each other — this would have moved NETL (authority=0.98) above PatSnap (authority=0.6) and the OSTI error page.


---
### tc_9695f75c (Score: 0.57) ❌
**Query**: `how to write an effective academic literature review step by step`
**Category**: Education & Academia | **Intent**: novel

**Root Cause**: The primary failure is a ranking defect where the Reddit thread at rank 2 (authority=0.1, relevance=0.2, word_count=22) outranks Purdue OWL (authority=0.95, relevance=1.0) at rank 4 and University of Arizona (authority=0.9, relevance=1.0) at rank 5, triggering the contrastive fail. A secondary failure is in scrape fidelity scoring: the YouTube page (rank 3) received scrape_score=0.20 despite its scrape_reasoning confirming 'Full video transcript and all metadata were successfully extracted,' and the Arizona page (rank 5) received scrape_score=0.20 for a single stray icon text artifact despite reasoning stating 'faithfully preserves the original page content and structure.'

- **Coverage Diagnosis**: N/A — coverage scored L5 (0.88); all five pipeline stages (scope definition, search strategy, source evaluation, synthesis, writing structure) are covered by at least two documents.
- **Ranking Diagnosis**: Reddit (rank 2, auth=0.1, rel=0.2) is positioned above YouTube/Smart Student (rank 3, auth=0.7, rel=1.0), Purdue OWL (rank 4, auth=0.95, rel=1.0), and University of Arizona (rank 5, auth=0.9, rel=1.0). The ideal order would be Purdue OWL → Arizona → UCSD → YouTube → Reddit, or similar with Reddit demoted to last.
- **Scrape Diagnosis**: YouTube (rank 3) has scrape_score=0.20 with empty issues list and reasoning confirming complete extraction — this is a scoring anomaly. Arizona (rank 5) has scrape_score=0.20 for a single minor icon artifact ('keyboard_arrow_up') despite reasoning confirming faithful preservation. UCSD (rank 1) and Purdue OWL (rank 4) both scored 0.40 for interactive widget and formatting artifacts. The aggregate average of 0.34 triggers the contrastive fail, but at least two of the five scores appear mis-calibrated relative to their stated reasoning.

**Fix Actions**:
- Add a domain-authority and query-relevance boost factor to the ranking model so that academic domains (authority ≥0.9, relevance ≥0.95) are always ranked above commercial forum threads (authority ≤0.2, relevance ≤0.3), preventing the Reddit-at-rank-2 contrastive fail pattern.
- Audit and recalibrate the scrape_score computation for video transcript pages: the YouTube result (https://www.youtube.com/watch?v=Vc_Yu_61Ymg) received score=0.20 with an empty issues list and reasoning stating complete extraction, indicating the scorer may be penalizing video content type or nav_link_ratio (0.95) rather than actual content loss.
- Adjust the scrape_score penalty for minor UI artifacts: the Arizona page (https://lib.arizona.edu/research/sources/lit-review) received 0.20 for a single stray 'keyboard_arrow_up' icon text, which is disproportionate — implement a tiered penalty where cosmetic artifacts (stray icon text, empty table artifacts) cap at a 0.1 deduction rather than dropping the score to L1.


---
### tc_39808d09 (Score: 0.47) ❌
**Query**: `how to build a diversified dividend growth portfolio for retirement income`
**Category**: Finance & Investing | **Intent**: novel

**Root Cause**: The primary failure is a ranking inversion: the most relevant and authoritative document (https://www.bogleheads.org/forum/viewtopic.php?t=269179, query_relevance_score=0.95, authority_score=0.85) was placed at rank 3 while two Reddit threads with relevance scores of 0.3 and 0.0 occupied ranks 1-2, one of which (https://www.reddit.com/r/dividends/comments/1rvc5cb/...) completely failed to scrape (scrape_score=0.0, 'Empty document content'). A secondary failure is that no retrieved document provides tutorial-structured content with screening criteria or step-by-step portfolio construction methodology, causing actionability (0.30) and structural_fidelity (0.25) to score at L2.

- **Coverage Diagnosis**: Only Doc3 (Bogleheads) substantively answers the query with full coverage, but it lacks stock selection criteria and sector diversification principles. Doc4 (HumbleDollar) and Doc5 (Fidelity) are tangential (relevance 0.2 and 0.3 respectively). The result set has no document covering all three required components: stock selection criteria, diversification principles, and retirement income considerations.
- **Ranking Diagnosis**: Rank 3 (Bogleheads, relevance 0.95, authority 0.85) should be rank 1. Rank 1 (Reddit, relevance 0.3, authority 0.1, truncated to 24 words) and Rank 2 (Reddit, relevance 0.0, authority 0.0, empty content) should not appear in the top results at all. This is a contrastive fail: the most relevant result is buried below two useless results.
- **Scrape Diagnosis**: Rank 1 (https://www.reddit.com/r/dividends/comments/1gy0el0/...) is critically truncated at 24 words with scrape_score=0.79, missing the entire post body and comments. Rank 2 (https://www.reddit.com/r/dividends/comments/1rvc5cb/...) completely failed with scrape_score=0.0 and 'Empty document content'. Ranks 3-5 all have scrape_score=0.20 with issues including unrendered images, boilerplate contamination, and duplicated navigation text.

**Fix Actions**:
- Add a post-retrieval reranker that boosts results with high query_relevance_score and authority_score while penalizing results with content_completeness='appears_truncated' or 'error_page', so that a Bogleheads thread (relevance 0.95, authority 0.85) outranks truncated Reddit posts (relevance 0.3, authority 0.1).
- Add a scrape-failure fallback mechanism: when a URL returns empty content or scrape_score < 0.3, automatically trigger a re-scrape with alternate extraction strategies (e.g., JavaScript rendering, different selectors) or replace it with the next-best candidate from the candidate pool rather than surfacing an empty document.
- Add a domain-type and page-type boost for tutorial_howto queries: prioritize results from educational domains and pages typed as 'article' or 'guide' over 'forum_thread' and 'product_page', and inject query expansion terms like 'screening criteria', 'step by step', and 'allocation framework' to improve retrieval of tutorial-structured content.


---
### tc_35529ad7 (Score: 0.56) ❌
**Query**: `Largest sovereign wealth fund by AUM 2026 and its top holdings with allocation percentages`
**Category**: Finance & Investing | **Intent**: exact_duplicate

**Root Cause**: The primary failure is a coverage gap: all five retrieved documents identify NBIM/GPFG as the largest SWF by AUM but none provide its top holdings or per-holding allocation percentages, as explicitly noted in document profiles for ranks 1, 3, and 4 ('No information about top holdings, allocation percentages, or any fund portfolio composition'). A secondary failure is ranking: the SSGA blog post at rank 2 (query_relevance_score=0.05, scrape_score=0.20, scrape_level=L1) was placed above Global SWF at rank 3 (query_relevance_score=0.65, authority_score=0.9), triggering the contrastive fail for blogs ranking above specialized reference databases.

- **Coverage Diagnosis**: All five document profiles list 'top holdings' and 'allocation percentages' as critical content gaps. The query requires a three-hop chain (identify fund → list holdings → provide percentages), but only the first hop is covered. No retrieved document contains portfolio-level holdings data for any specific fund, let alone NBIM/GPFG.
- **Ranking Diagnosis**: Rank 2 (SSGA, relevance 0.05, authority 0.65, scrape_level L1) appears above Rank 3 (Global SWF, relevance 0.65, authority 0.9, scrape_level L3), violating both relevance and authority monotonicity. The contrastive fail was triggered: 'A blog/low-quality publication (SSGA, Rank 2) ranks above a specialized reference database (Global SWF, Rank 3).'
- **Scrape Diagnosis**: Rank 2 (SSGA) has scrape_score=0.20 with duplicated paragraphs, repeated boilerplate footers, and missing figure alt text. Rank 1 (SWF Institute) has scrape_score=0.60 with duplicate table rows, fragmented text ('iew Total Assets' mid-row), and missing line breaks causing cell concatenation. Rank 4 (PraxisRock) has mid-sentence truncation ('irect.') and repeated boilerplate blocks.

**Fix Actions**:
- Add a query expansion / multi-hop retrieval stage that decomposes the query into sub-queries (e.g., 'NBIM GPFG top holdings 2026', 'Norway Government Pension Fund Global portfolio allocation percentages') and retrieves documents specifically about NBIM's portfolio holdings, such as NBIM's official quarterly reports at nbim.no or their holdings database.
- Adjust the ranking scoring function to apply a penalty multiplier when query_relevance_score < 0.1 and scrape_level == 'L1', ensuring that near-irrelevant pages with critical scrape issues (like SSGA at rank 2) cannot outrank highly relevant reference databases (like Global SWF at rank 3).
- Add a deduplication and table-repair post-processing step in the scrape pipeline to fix missing leading pipe symbols in markdown tables (affecting globalswf.com/ranking) and remove duplicated table rows (affecting swfinstitute.org/fund-rankings), improving scrape_score from 0.60 toward 0.80+ for reference database pages.


---
### tc_3b4eb676 (Score: 0.53) ❌
**Query**: `quantitative energy penalty values for amine-based sorbent regeneration in direct air capture systems`
**Category**: Environment & Climate | **Intent**: subset_of_parent

**Root Cause**: The primary failure is a coverage gap: no retrieved document contains the specific target data (quantitative energy penalty for amine-based sorbent regeneration in DAC). Rank 1 (sciencedirect.com, scrape_score=0.20) provides 2.46 GJ/tCO2 but only for post-combustion PEI/silica and is truncated to 511 words. Rank 2 (eureka.patsnap.com) gives total DAC energy of 1,500-2,000 kWh/ton but not regeneration-specific values. Ranks 3-5 either lack quantitative energy penalties entirely or address post-combustion systems. This is compounded by scrape failures on Rank 1 (truncated) and Rank 4 (paywalled abstract only, scrape_score=0.60).

- **Coverage Diagnosis**: Critical gap: zero documents provide a quantitative energy penalty value for amine-based sorbent regeneration specifically in DAC systems. The closest values are either post-combustion regeneration heats (Rank 1: 2.46 GJ/tCO2 for PEI/silica; Rank 5: 3800-4000 kJ/kg for MEA) or total DAC process energy (Rank 2: 1,500-2,000 kWh/ton). No document bridges the gap between amine regeneration energy and DAC-specific conditions (~400 ppm CO2).
- **Ranking Diagnosis**: N/A — ranking scored 0.72 (L4, adequate). The most relevant document (Rank 2, query_relevance_score=0.6) is at position 2, not buried. The failure is in coverage, not ordering.
- **Scrape Diagnosis**: Rank 1 (https://www.sciencedirect.com/science/article/pii/S0306261916300290) has scrape_score=0.20 with content_completeness='appears_truncated' and only 511 words for an open-access academic paper, missing the full methods, data, and discussion sections. Rank 4 (https://pubs.acs.org/doi/10.1021/acssuschemeng.0c03800) has scrape_score=0.60 with only abstract available due to paywall, and high boilerplate density (boilerplate_pattern_count=8). Rank 3 (https://www.pnnl.gov/main/publications/external/technical_reports/PNNL-36148.pdf) has scrape_score=0.40 with missing images and chemical formula formatting loss.

**Fix Actions**:
- Reformulate the search query to include DAC-specific regeneration energy terms (e.g., 'temperature swing adsorption amine DAC regeneration energy GJ/tCO2' or 'solid amine sorbent direct air capture heat of regeneration') to retrieve documents that explicitly quantify regeneration energy under DAC conditions (~400 ppm CO2).
- Fix the ScienceDirect scraper to extract full open-access article content; Rank 1 (https://www.sciencedirect.com/science/article/pii/S0306261916300290) is CC-licensed open access but only 511 words were scraped, indicating the scraper is stopping at the abstract/highlights boundary and not following the full-text HTML.
- Add paywall detection logic for ACS publications (pubs.acs.org) and automatically fall back to preprint repositories (ChemRxiv, arXiv) or institutional repository mirrors when full text is inaccessible, to avoid including abstract-only pages that cannot answer quantitative queries.


---
### tc_5cad7b97 (Score: 0.62) ❌
**Query**: `best time of year to visit Iceland for Northern Lights and sightseeing`
**Category**: Travel & Geography | **Intent**: novel

**Root Cause**: The primary failure is a ranking inversion: a 17-word Reddit comment (https://www.reddit.com/r/VisitingIceland/comments/1gcuaxh/best_months_to_go_to_iceland_best_months_to_see/, authority_score=0.2, query_relevance_score=0.6) was ranked #1 over the Nordic Visitor guide (https://www.nordicvisitor.com/blog/best-time-place-see-northern-lights-iceland/, authority_score=0.6, query_relevance_score=0.95), triggering the contrastive fail in _baseline_ranking. Additionally, rank 5 (https://www.reddit.com/r/VisitingIceland/comments/1sqdp3s/best_singular_month_to_visit_iceland_for_the/) returned an empty document (scrape_score=0.0, P1 failed), and rank 2 had nav_link_ratio=0.65 with 7 boilerplate patterns, collectively dragging the aggregated _baseline_fidelity score to 0.14 (L1).

- **Coverage Diagnosis**: Seasonal coverage is partial (L3, 0.55): multiple seasons and aurora visibility are covered, but road accessibility across seasons is entirely absent (NOT_MET), and trade-offs for daylight, weather, and crowd levels are only PARTIALLY_MET. No document provides a comprehensive synthesis of sightseeing feasibility versus aurora conditions across seasons.
- **Ranking Diagnosis**: Rank 1 (Reddit, relevance 0.6, authority 0.2) is placed above Rank 2 (Nordic Visitor, relevance 0.95, authority 0.6), violating both authority and relevance ordering criteria. The contrastive fail 'most relevant result is buried' was triggered. Rank 5 is an empty fallback page that should not have been included or should have been replaced.
- **Scrape Diagnosis**: Rank 2 (nordicvisitor.com) has scrape_score=0.40 with nav_link_ratio=0.65 and 7 boilerplate patterns, indicating navigation/boilerplate heavily interleaved with main content. Rank 5 (reddit.com) has scrape_score=0.0 with P1 evaluation failure and empty content. The aggregated fidelity average of 0.14 reflects these two degraded documents pulling down the otherwise clean scrapes at ranks 1, 3, and 4 (all scrape_score=0.20, no issues).

**Fix Actions**:
- Adjust the ranking scoring function to apply a stronger penalty for forum_thread page_type with word_count < 100 and authority_score < 0.3, ensuring such results cannot outrank blog_post results with relevance > 0.9 and authority > 0.5.
- Add a post-retrieval filter that excludes or re-fetches any result with scrape_score=0.0 or content_completeness='error_page' before final ranking, replacing it with the next available search result rather than including an empty fallback.
- Enhance the scraper's boilerplate removal for commercial travel blog domains (e.g., nordicvisitor.com) by adding domain-specific selectors to strip navigation menus, footer links, and promotional CTAs before markdown conversion, targeting nav_link_ratio < 0.20.


---
### tc_316e5e79 (Score: 0.80) ❌
**Query**: `active learning effectiveness undergraduate STEM courses research`
**Category**: Education & Academia | **Intent**: novel

**Root Cause**: The scrape scoring algorithm assigned scrape_score=0.20 to ranks 2–4 despite their scrape_reasoning explicitly stating faithful content preservation (e.g., Rank 3 at https://tll.mit.edu: 'faithfully preserves all textual content'; Rank 4 at https://education.umd.edu: 'faithfully captures the full article content'), while the search ranking placed a captcha-blocked ScienceDirect page (word_count=25, content_completeness=error_page) at Rank 1, causing both the _baseline_fidelity and _baseline_ranking dimensions to fail.

- **Coverage Diagnosis**: Ranks 3–5 provide full query coverage with quantitative comparative data, but ranks 1–2 contribute zero and tangential coverage respectively, leaving the top of the result set devoid of substantive content.
- **Ranking Diagnosis**: Rank 1 (ScienceDirect, relevance=0.0, authority=0.0) and Rank 2 (foundationccc.org, relevance=0.6, authority=0.7) occupy the top two positions while ranks 3–5 (relevance=0.95, authority≥0.85) are buried, directly triggering the contrastive_fail for 'most relevant result is buried.'
- **Scrape Diagnosis**: scrape_score=0.20 is assigned to ranks 2–4 despite complete content and no scrape_issues (ranks 3–4 have empty issues arrays), indicating the scoring function applies a fixed floor rather than evaluating actual content quality; Rank 1 is a genuine captcha failure (word_count=25, content_completeness=error_page).

**Fix Actions**:
- Replace the fixed 0.20 scrape_score floor with a content-aware scoring function that evaluates word_count, heading_count, content_completeness, and scrape_issues length, so that pages with complete content and zero issues (e.g., ranks 3–4 with empty issues arrays) receive scores ≥0.7.
- Add a post-scrape demotion filter that re-ranks or removes results where content_completeness=error_page, preventing captcha-blocked pages like the ScienceDirect result (word_count=25) from occupying rank 1.
- Implement a captcha-detection retry pipeline for commercial academic domains (e.g., sciencedirect.com) that falls back to a headless browser renderer or alternative access method when the initial scrape returns content_completeness=error_page.


---
### tc_fee03e5a (Score: 0.49) ❌
**Query**: `average PhD stipend amounts in STEM fields`
**Category**: Education & Academia | **Intent**: novel

**Root Cause**: The primary failure mechanism is a ranking inversion: applykite.com (relevance 0.95, authority 0.6) was placed at rank 3 behind Reddit (relevance 0.7, authority 0.15) and phdstipends.com (relevance 0.8, authority 0.3), as cited in the _baseline_ranking evidence. This was compounded by critical scrape failures on 3 of 5 documents — Reddit truncated to 28 words, Quora returning an error page, and Missouri truncated to 28 words — which destroyed fidelity, source quality, and multi-constraint coverage since the truncated documents could not contribute tuition remission, health insurance, or funding duration data.

- **Coverage Diagnosis**: The document profiles show no coverage of tuition remission, health insurance, or funding duration guarantees across any of the 5 retrieved documents. Only Doc3 (applykite.com) partially covers funding types (fellowships, TAs, RAs) but without specific details on availability or duration. No document systematically compares stipends by university tier (R1 vs. teaching-focused). The truncated Missouri.edu page (28 words) likely contained tier-relevant context that was lost.
- **Ranking Diagnosis**: Rank 3 (applykite.com, relevance 0.95, authority 0.6) should have been Rank 1. Rank 1 (Reddit, relevance 0.7, authority 0.15) and Rank 4 (Quora, relevance 0.0, authority 0.0, error page) should not have appeared in the top results at all. The ranking model gave undue weight to forum/aggregator content over a structured blog with field-by-field and country-level stipend tables.
- **Scrape Diagnosis**: Three of five documents have critical scrape failures: Reddit (scrape_score 0.6, truncated to 28 words, missing all comments), Quora (scrape_score 0.2, error page with 11 words), and Missouri (scrape_score 0.6, truncated to 28 words). Doc2 (phdstipends.com) has scrape_score 0.2 with nav_link_ratio 0.923, suggesting excessive navigation noise. Only Doc3 (applykite.com, scrape_score 0.4, word_count 2798) has reasonably complete content.

**Fix Actions**:
- Adjust the ranking model's authority and relevance weighting to penalize forum threads (Reddit, Quora) and crowd-sourced aggregators when a structured blog or academic-domain source with higher relevance and authority scores exists in the candidate set — specifically, boost results with query_relevance_score >= 0.9 and authority_score >= 0.5 above any result with authority_score < 0.3.
- Add a scrape retry with exponential backoff and alternate user-agent for domains that return error pages (e.g., Quora's 'Something went wrong' response), and add a content-length validation gate that re-scrapes or discards any document with word_count < 100 that was expected to be a full article page.
- Add domain-type boosting for .edu and government domains in the search pipeline for education/academia queries, and add a query expansion step that appends terms like 'tuition waiver' 'health insurance' 'funding guarantee' to ensure multi-constraint coverage in retrieved snippets.


---
### tc_548fb6e6 (Score: 0.47) ❌
**Query**: `NBA League Pass subscription cost 2026 annual monthly pricing`
**Category**: Sports & Entertainment | **Intent**: novel

**Root Cause**: The query 'NBA League Pass subscription cost 2026 annual monthly pricing' was treated as a narrow pricing lookup rather than a comparative_research intent, causing the pipeline to retrieve only NBA-specific pages (ranks 1, 2, 5) with zero comparative sports streaming context. The most relevant source — https://ca.sports.yahoo.com/news/nba-league-pass-explained-plans-173703943.html (query_relevance_score=0.9, authority_score=0.7, published 2025-10-07) — was buried at rank 4 behind a 27-word Reddit post (authority_score=0.2, outdated pricing) and an NBA FAQ page with no pricing data (query_relevance_score=0.4).

- **Coverage Diagnosis**: All five retrieved documents focus exclusively on NBA League Pass; none compare it against competing sports streaming services (ESPN+, NFL Sunday Ticket, MLB.TV, Peacock). Rank 5 (wnba.com/leaguepass) is entirely irrelevant (query_relevance_score=0.1, content_gap severity 'critical' for wrong league). The comparative_research intent is completely unaddressed.
- **Ranking Diagnosis**: Rank 4 (Yahoo/Sporting News, relevance=0.9, authority=0.7) is placed behind rank 3 (Reddit, relevance=0.7, authority=0.2, 27 words, outdated pricing) and rank 2 (NBA FAQ, relevance=0.4, no pricing data). The ranking model failed to weight query_relevance_score and authority_score appropriately, allowing a low-quality forum post to outrank a comprehensive, timely news article.
- **Scrape Diagnosis**: Scrape scores for nba.com pages (ranks 1, 2, 5) are 0.20 (L1) despite scrape_reasoning confirming complete content with no truncation — indicating a scrape_score calibration issue for JS-rendered or SPA-style pages. Rank 4 (scrape_score=0.40) has 6 boilerplate ad blocks and missing image alt text, adding noise but not blocking content extraction. The aggregate fidelity score of 0.312 is artificially depressed by the miscalibrated low scores on complete pages.

**Fix Actions**:
- Add query-expansion logic for comparative_research intent that appends competitor terms (e.g., 'vs ESPN+ NFL Sunday Ticket MLB.TV Peacock') to the search query, ensuring retrieval of cross-service comparison articles.
- Adjust the ranking model to apply a penalty multiplier when authority_score < 0.4 and word_count < 100, demoting low-content forum posts below comprehensive news articles with authority_score >= 0.6.
- Recalibrate scrape_score computation for SPA/JS-rendered pages (nba.com, wnba.com) where scrape_reasoning confirms complete content — if content_completeness='complete' and no critical scrape_issues are flagged, floor the scrape_score at 0.5 minimum.
- Add a relevance-filter step to exclude results with query_relevance_score < 0.2 from the final result set, preventing irrelevant pages like wnba.com/leaguepass from occupying a slot.


---
### tc_e5d1629f (Score: 0.80) ❌
**Query**: `how to set up a CI/CD pipeline with GitHub Actions for a Node.js project`
**Category**: Technology & Software | **Intent**: novel

**Root Cause**: Two compounding failures drive the test case: (1) the ranking model places LogRocket (authority_score=0.8, query_relevance_score=1.0) at rank 4 below Medium (0.6) and W3Schools (0.7), violating descending-authority ordering as explicitly cited in the _baseline_ranking evidence; and (2) the scrape pipeline yields an aggregate fidelity of 0.284 (L2) because ranks 2–4 each carry scrape_score=0.4 with boilerplate, image-placeholder, and promotional-content issues, while ranks 1 and 5 sit at 0.20. Additionally, W3Schools at rank 3 promotes deprecated actions/checkout@v2 and actions/setup-node@v2, triggering the technical_accuracy contrastive fail.

- **Coverage Diagnosis**: N/A — coverage scored 0.92 (L5); all seven sub-conditions are MET with strong evidence across docs 1–4.
- **Ranking Diagnosis**: Rank 4 (blog.logrocket.com, authority_score=0.8, query_relevance_score=1.0) should appear at rank 2, ahead of rank 2 (medium.com, authority_score=0.6) and rank 3 (w3schools.com, authority_score=0.7). The current ordering 0.6 → 0.7 → 0.8 is ascending rather than descending in authority among equally relevant results.
- **Scrape Diagnosis**: Average scrape_score across 5 pages is 0.284 (L2). Ranks 2–4 each score 0.4 with issues: rank 2 has 'Images replaced with alt text or placeholders' and 'Excessive navigation/boilerplate elements retained'; rank 3 has 'Interactive exercise not preserved' and 'Minor formatting details lost'; rank 4 has 'Promotional content interspersed with tutorial'. Ranks 1 and 5 score 0.20 but with minimal issues. The nav_link_ratio for ranks 3 and 4 is 0.6, indicating significant boilerplate leakage.

**Fix Actions**:
- Add a post-retrieval authority-sorting pass: after pinning the top official-doc result, re-rank remaining results by descending authority_score × query_relevance_score so that LogRocket (0.8) precedes W3Schools (0.7) and Medium (0.6).
- Enhance the scrape boilerplate filter to strip promotional blocks (e.g., LogRocket product CTAs) and navigation chrome on sites with nav_link_ratio > 0.4, targeting a scrape_score >= 0.5 for tutorial/blog page types.
- Add a content-freshness/version-recency signal to the ranking scorer that penalizes pages containing deprecated action references (e.g., actions/checkout@v2, actions/setup-node@v2) when newer major versions (v4) are documented in the official source, demoting W3Schools below LogRocket.


---
### tc_f748b907 (Score: 0.59) ❌
**Query**: `NBA League Pass subscription cost 2026 annual monthly pricing`
**Category**: Sports & Entertainment | **Intent**: exact_duplicate

**Root Cause**: The query 'NBA League Pass subscription cost 2026 annual monthly pricing' lacks competitor terms, so retrieval returned only NBA/WNBA pages — evidence: 'No document mentions any sports streaming service other than NBA and WNBA' (comparative_context_recovery, score 0.25). Additionally, the ranking algorithm placed Reddit (rank3, authority 0.2, scrape_score=0.40, outdated $14.99 pricing) above Yahoo Sports (rank4, authority 0.8, relevance 0.95, current $16.99/$109.99 pricing), triggering contrastive fails in both _baseline_ranking (0.25) and temporal_relevance (0.50).

- **Coverage Diagnosis**: All 5 retrieved documents cover only NBA League Pass and tangentially WNBA League Pass. Zero documents mention NFL+, MLB.TV, ESPN+, NHL.tv, or any other competing sports streaming service, leaving the comparative_research intent entirely unmet.
- **Ranking Diagnosis**: Yahoo Sports (relevance 0.95, authority 0.8, full pricing data) is buried at rank4 behind Reddit (relevance 0.7, authority 0.2, outdated pricing) at rank3 and two official NBA pages (relevance 0.6 each) at ranks 1-2 that lack annual pricing entirely.
- **Scrape Diagnosis**: Rank 2 (nba.com/nba-league-pass-faqs) has scrape_score=0.20 with duplicate paragraph fragments and missing navigation links; Rank 1 (nba.com/league-pass-purchase) has scrape_score=0.60 with truncated 'More Plans' section and duplicate text fragments ('ames.' standalone); Rank 4 (Yahoo) has 8 boilerplate patterns and repeated formatting artifacts.

**Fix Actions**:
- Add intent-aware query expansion for comparative_research category: when the query mentions a single sports streaming product, automatically append competitor terms (e.g., 'NFL+ MLB.TV ESPN+ NHL.tv') to the retrieval query to ensure cross-service comparison documents are surfaced.
- Adjust the ranking scoring function to apply an authority floor penalty: sources with authority_score < 0.3 should not outrank sources with authority_score > 0.7 AND higher query_relevance_score in the same candidate set.
- Fix the nba.com scraper to resolve duplicate paragraph fragments and preserve navigation link structure; add a truncation detector for dynamically-loaded 'More Plans' sections that require scroll-triggered content fetching.


---
### tc_f44db2a2 (Score: 0.75) ❌
**Query**: `When is the ideal season to plan an Iceland trip for seeing the Northern Lights and exploring the country?`
**Category**: Travel & Geography | **Intent**: rephrased_same_intent

**Root Cause**: The primary failure is a ranking inversion: the Reddit post at rank 1 has authority_score 0.2, query_relevance_score 0.6, and scrape_score 0.20 with only 18 words, while Guide to Iceland at rank 4 has authority_score 0.7, query_relevance_score 0.95, scrape_score 0.40, and 4187 words covering both Northern Lights and country exploration. Secondary failures include scrape pipeline issues—Nordic Visitor (rank 2) has nav_link_ratio 0.85 and boilerplate_pattern_count 8, Aurora Expeditions (rank 3) has duplicated text and truncation, and Facebook (rank 5) is truncated mid-sentence—collectively dragging the aggregated fidelity score to 0.4226.

- **Coverage Diagnosis**: No retrieved document addresses road accessibility (winter road closures, highland route feasibility) or tourist crowd levels across seasons, both of which are critical to the 'exploring the country' aspect of the query. The seasonal_coverage dimension scored 0.7 (L4) with these two checklist items marked NOT_MET.
- **Ranking Diagnosis**: Guide to Iceland (authority 0.7, relevance 0.95, full coverage) should occupy rank 1 but sits at rank 4 behind Reddit (authority 0.2, relevance 0.6), Nordic Visitor (authority 0.5, relevance 0.95), and Aurora Expeditions (authority 0.5, relevance 1.0). The contrastive fail was triggered because the highest-authority source is buried behind three lower-authority sources.
- **Scrape Diagnosis**: Reddit (rank 1) has scrape_score 0.20 (L1) despite no listed issues, suggesting the page is too thin to score well. Nordic Visitor (rank 2) has nav_link_ratio 0.85 and boilerplate_pattern_count 8, overwhelming main content. Aurora Expeditions (rank 3) has duplicated text fragments and content_completeness='appears_truncated'. Facebook (rank 5) is truncated mid-sentence with only 28 words captured. Guide to Iceland (rank 4) has scrape_score 0.40 with minor multimedia rendering issues.

**Fix Actions**:
- Increase the ranking weight multiplier on authority_score and content_completeness so that sources with authority_score >= 0.7 and full query coverage are promoted above sources with authority_score <= 0.2 and word_count < 50.
- Add a nav_link_ratio threshold filter (e.g., > 0.6) in the scrape pipeline that triggers aggressive boilerplate removal or re-scrape with a content-focused extraction strategy for pages like nordicvisitor.com.
- Add a query expansion term set including 'road conditions', 'highland roads', 'crowd levels', and 'tourist season' to the retrieval query to surface sources covering road accessibility and crowd dynamics for Iceland travel.


---
### tc_087d6cbc (Score: 0.70) ❌
**Query**: `semaglutide efficacy for sustained weight loss in non-diabetic obese adults`
**Category**: Healthcare & Medical | **Intent**: novel

**Root Cause**: Rank 1 (https://www.ajconline.org/article/S00029149(24)00319-9/fulltext) has scrape_score=0.20 with nav_link_ratio=0.9 and no substantive content, yet occupies the top position, while Rank 5 (https://www.sciencedirect.com/science/article/abs/pii/S0014299926000695, authority_score=0.9, query_relevance_score=0.98) is buried below Rank 4 (https://commons.lib.jmu.edu/cgi/viewcontent.cgi?article=1083&context=pacapstones202029, authority_score=0.5). The scrape pipeline also systematically fails across all pages: Rank 1 captures only navigation, and Ranks 2-5 are capped at scrape_score=0.40 due to unrendered images, collapsed 'Show more' sections, PDF extraction artifacts, and boilerplate leakage.

- **Coverage Diagnosis**: Core efficacy coverage is adequate (L4) but comparative context is incomplete: only Rank 2 (dom-pubs) provides meaningful comparisons to other antiobesity medications, while no document includes head-to-head trial data, clinical guideline recommendations, or contraindication details — three checklist items in clinical_specificity and comparative_context_recovery are NOT_MET.
- **Ranking Diagnosis**: Rank 1 (query_relevance_score=0.1, effectively irrelevant due to scrape failure) is placed above Rank 2 (query_relevance_score=0.97) and Rank 3 (query_relevance_score=0.98). Rank 5 (authority_score=0.9, query_relevance_score=0.98) is placed below Rank 4 (authority_score=0.5, query_relevance_score=1.0), violating the 'high-authority sources before lower-quality ones' criterion.
- **Scrape Diagnosis**: Rank 1 (ajconline.org) completely failed with scrape_score=0.20, capturing only navigation elements (nav_link_ratio=0.9) due to paywall/dynamic loading. Ranks 2-5 all scored 0.40 with recurring issues: Rank 2 missing figure images and blocked third-party widget; Rank 3 missing figure images and supplementary tables; Rank 4 has PDF extraction artifacts (repeated lines, misformatted superscripts, stray markup like '$$'); Rank 5 has collapsed 'Show more' content not expanded and reference links without text.

**Fix Actions**:
- Add a post-scrape relevance filter that demotes or removes results with scrape_score < 0.25 and nav_link_ratio > 0.8 before ranking, preventing inaccessible paywalled pages like ajconline.org from occupying top positions.
- Integrate a ranking authority-weighted reranker that penalizes results where authority_score < 0.6 when higher-authority alternatives (authority_score ≥ 0.85) with comparable query_relevance_score exist in the result set, ensuring meta-analyses from ScienceDirect/Elsevier rank above student capstones.
- Add JavaScript-rendered expansion for collapsed content sections (e.g., 'Show more' links on ScienceDirect) and improve PDF-to-markdown extraction to handle superscript formatting and eliminate line repetition artifacts.


---
### tc_a345a697 (Score: 0.89) ❌
**Query**: `latest dietary guidelines for added sugar intake adults`
**Category**: Food & Nutrition | **Intent**: novel

**Root Cause**: The test case failed primarily because the second _baseline_fidelity dimension scored 0.312 (L2) with contrastive_fail_triggered=true, citing 'Average scrape quality is poor.' This is traceable to scrape_scores of 0.20 for cdc.gov (rank 2) and harvard.edu (rank 4) with no documented issues, plus 0.40 for dietaryguidelines.gov (rank 1, image placeholder) and ncbi.nlm.nih.gov (rank 5, boilerplate/navigation), and 0.60 for heart.org (rank 3, script errors and broken images). The temporal_currency dimension (0.75, L4) is a secondary contributor due to the 2015 WHO guideline at rank 5 being outdated for a 'latest' query.

- **Coverage Diagnosis**: N/A — completeness scored 0.9 (L5) with all four required rubric aspects (daily intake limits, added vs. naturally occurring sugar distinction, health risks, common dietary sources) comprehensively covered across multiple authoritative documents.
- **Ranking Diagnosis**: N/A — _baseline_ranking scored 0.95 (L5); the official DGA fact sheet is correctly at rank 1, followed by CDC, AHA, Harvard, and WHO in a sensible authority-relevance order with no contrastive fail triggered.
- **Scrape Diagnosis**: Critical scrape quality issues across all five documents: (1) Rank 1 dietaryguidelines.gov PDF has an unresolved image placeholder '[Image: Im0]' (scrape_score=0.40); (2) Rank 2 cdc.gov has scrape_score=0.20 with no listed issues, suggesting an unreported extraction or scoring problem; (3) Rank 3 heart.org has broken image placeholders ('Base64-Image-Removed'), a leaked script error block ('a25670000279.cdn.optimizely.com is blocked'), and boilerplate subscription/social sections (scrape_score=0.60); (4) Rank 4 harvard.edu has scrape_score=0.20 with no listed issues, another anomalous low score; (5) Rank 5 ncbi.nlm.nih.gov has preserved navigation/UI links and NCBI header/footer boilerplate (scrape_score=0.40). The aggregate average of 0.312 triggered the contrastive fail.

**Fix Actions**:
- Add a post-scrape boilerplate and navigation removal pass that strips subscription forms, social sharing sections, script error blocks (e.g., 'cdn.optimizely.com is blocked'), and NCBI header/footer chrome using DOM selector-based filtering before markdown conversion.
- Implement PDF image-to-text extraction (OCR fallback) for government PDF documents like the DGA fact sheet at rank 1, so image placeholders such as '[Image: Im0]' are resolved into text content rather than left as unresolved markers.
- Investigate and fix the scrape scoring pipeline for pages like cdc.gov (rank 2) and harvard.edu (rank 4) that received scrape_score=0.20 with empty scrape_issues arrays — either the scoring heuristic is penalizing content characteristics not captured in the issues list, or there are silent extraction failures (e.g., JavaScript-rendered content not captured) that need a headless-browser rendering fallback.


---
### tc_b6971b6c (Score: 0.67) ❌
**Query**: `list of high fiber gluten free grains suitable for homemade bread baking`
**Category**: Food & Nutrition | **Intent**: novel

**Root Cause**: The test fails primarily because Rank 3 (nutrimill.com, scrape_score=0.6) — the sole document directly addressing bread-baking functionality — is truncated by browser extension blocking, losing its latter half including practical mixing guidance. Simultaneously, Ranks 1 and 2 (gluten.org and celiacselfcare.christinaheiser.com, both scrape_score=0.2/L1) have critically poor image handling and structural fidelity. This compounds into L3 scores on bread_baking_functionality (0.55) and practical_bridge (0.5), and an aggregate _baseline_fidelity of 0.34 (L2) with contrastive_fail triggered.

- **Coverage Diagnosis**: No single document provides a unified list of high-fiber gluten-free grains with bread-baking suitability ratings. Fiber data lives in WebMD (Rank 5) and Christina Heiser (Rank 2), baking functionality lives in NutriMill (Rank 3, truncated), and broad grain lists live in gluten.org (Rank 1). The portfolio covers the query only in fragmented pieces across truncated or low-fidelity sources.
- **Ranking Diagnosis**: Rank 4 (Facebook post, authority_score=0.2, word_count=24, content_completeness='appears_truncated') occupies a position that should belong to a more substantive source. Rank 5 (WebMD, authority_score=0.8, query_relevance_score=0.6) is placed below lower-authority blogs (Ranks 2 and 3) — while partially justified by baking relevance, WebMD's comprehensive fiber data table would better serve the 'high fiber' aspect of the query if ranked higher.
- **Scrape Diagnosis**: Rank 3 (nutrimill.com) is truncated by browser extension blocking ('nutrimill.com is blocked' repeated messages), losing the 'Tips for Mixing and Matching Grains' section's full content. Rank 4 (facebook.com) retains only 24 words. Ranks 1 and 2 both have scrape_score=0.2 (L1) with images rendered as raw URLs and missing alt text. Rank 5 (WebMD) has scrape_score=0.4 (L2) with blocked external resources and Base64 image removal.

**Fix Actions**:
- Add nutrimill.com and facebook.com to the scrape exclusion list for browser-extension-based blocking, or configure the scraper to use a headless mode that disables ad-blocker extensions during content extraction to prevent truncation on e-commerce and social media domains.
- Implement a post-scrape truncation detector that flags pages where word_count < 100 or where repeated error-message patterns (e.g., 'X is blocked') appear, triggering a re-scrape with alternative rendering settings before accepting the result.
- Upgrade image extraction for organization and blog domains (gluten.org, Substack-hosted sites) to resolve CDN image URLs into proper markdown image tags with alt text fallbacks, raising scrape_score from L1 to at least L3 for these high-authority sources.


---
### tc_5f802f87 (Score: 0.78) ❌
**Query**: `difference between added sugars and naturally occurring sugars in current dietary guidelines`
**Category**: Food & Nutrition | **Intent**: subset_of_parent

**Root Cause**: The test fails primarily due to two compounding issues: (1) ranking misplaces FDA (query_relevance_score=0.95, authority_score=1.0) at rank 3 behind CDC (query_relevance_score=0.6) at rank 1, and (2) aggregated scrape fidelity is critically low at 0.3666 (L2) because CDC has scrape_score=0.40 with truncated link text and repetitive markers, AHA has scrape_score=0.60 with duplicated paragraph fragments, and the Facebook post at rank 4 is severely truncated to 23 words ending mid-sentence. The inclusion of a near-empty Facebook post (23 words) as a search result further wastes a result slot that could have held a more complete source.

- **Coverage Diagnosis**: No document in the result set explicitly states that naturally occurring sugars are not subject to limits in current dietary guidelines — this is only implied. The guideline_treatment dimension scored 0.70 (L4) with the checklist condition 'Explains that naturally occurring sugars are not specifically limited in the guidelines' marked PARTIALLY_MET. Additionally, examples of naturally occurring sugars remain generic ('milk, fruits, vegetables') without naming specific foods.
- **Ranking Diagnosis**: CDC (relevance 0.6, authority 0.95) at rank 1 outranks FDA (relevance 0.95, authority 1.0) at rank 3 and AHA (relevance 0.9, authority 0.95) at rank 2. The most relevant and authoritative source should be rank 1. The Facebook post (relevance 0.6, authority 0.7, 23 words) at rank 4 occupies a slot that should go to a more complete source.
- **Scrape Diagnosis**: Three of five documents have significant scrape issues: CDC scrape_score=0.40 (truncated link text, repetitive 'Expand All' markers, duplicate boilerplate), AHA scrape_score=0.60 (duplicated paragraph fragments, blocked optimizely.com extension, repeated alt text), and Facebook scrape_score=0.79 but content is only 23 words ending mid-sentence. The aggregated fidelity score of 0.3666 triggered a contrastive fail.

**Fix Actions**:
- Adjust the ranking scoring formula to weight query_relevance_score more heavily than domain authority when relevance scores diverge by >0.3, ensuring FDA (relevance 0.95) outranks CDC (relevance 0.6) despite comparable authority scores.
- Add a post-scrape content length filter that demotes or excludes results with word_count < 50 from the final ranked list, replacing them with the next available candidate — this would remove the 23-word truncated Facebook post from rank 4.
- Improve the scraper's handling of interactive page elements (CDC 'Expand All' accordions, AHA optimizely.com scripts) by adding site-specific extraction rules that strip accordion UI markers and blocked third-party script URLs from the markdown output.


---
### tc_a7f33ea8 (Score: 0.86) ❌
**Query**: `current recommended daily added sugar limit for adults`
**Category**: Food & Nutrition | **Intent**: rephrased_same_intent

**Root Cause**: The primary failure is a ranking inversion where a severely truncated Facebook post (rank 4, 25 words, scrape_score 0.79, authority 0.7, relevance 0.6) is placed above the FDA official page (rank 5, authority 0.95, relevance 1.0, scrape_score 0.40). This is compounded by inverted scrape scores: Harvard, CDC, and NHS pages with complete content all received scrape_score=0.20 despite their scrape_reasoning stating 'faithfully captures all textual content,' while the 25-word truncated Facebook post received scrape_score=0.79.

- **Coverage Diagnosis**: No significant coverage gap — all required aspects (daily limits, sugar type distinctions, health risks, dietary sources) are covered across Harvard, NHS, CDC, and FDA documents. The only partial gap is health risk depth, but Doc3 covers tooth decay and weight gain.
- **Ranking Diagnosis**: Rank 4 (Facebook/FDA post, authority 0.7, relevance 0.6, 25 words) is incorrectly placed above Rank 5 (FDA official page, authority 0.95, relevance 1.0, 1681 words). The Facebook post should either be excluded or ranked last, as it is a truncated social media snippet that duplicates information already available from the official FDA page at rank 5.
- **Scrape Diagnosis**: Scrape scores are inverted: Harvard (scrape_score=0.20, scrape_reasoning='faithfully captures all textual content'), CDC (scrape_score=0.20, scrape_reasoning='faithfully reproduces the original page content with high fidelity'), and NHS (scrape_score=0.20, scrape_reasoning='faithfully preserves all substantive content') all received L1 scores despite complete content, while the severely truncated Facebook post (25 words, 'ends mid-sentence') received scrape_score=0.79 (L4). The FDA page (scrape_score=0.40) has nav_link_ratio=0.80 indicating excessive boilerplate contamination.

**Fix Actions**:
- Add a domain-type penalty in the ranking pipeline for social media domains (facebook.com, twitter.com, instagram.com) so that truncated social media posts cannot outrank official government pages on the same topic — specifically, demote any result with word_count < 100 and domain_type='commercial' below any result with domain_type='authoritative' and query_relevance_score >= 0.9.
- Fix the scrape_score calibration logic: pages where scrape_reasoning states 'faithfully captures' or 'faithfully preserves' should not receive scrape_score=0.20 (L1). The scoring function appears to be inverting quality — investigate whether the scrape_score computation is using an inverted scale or incorrectly weighting minor issues (e.g., duplicated lines) as critical failures.
- Add a nav_link_ratio threshold check to the scrape pipeline: the FDA page has nav_link_ratio=0.80, meaning 80% of links are navigation/boilerplate. Implement a content extraction step that strips navigation elements before scoring, or apply a penalty when nav_link_ratio > 0.5.


---
### tc_e4e371ec (Score: 0.93) ❌
**Query**: `health risks of exceeding recommended added sugar intake for adults`
**Category**: Food & Nutrition | **Intent**: subset_of_parent

**Root Cause**: The scrape_score field is systematically set to 0.20 for four of five documents despite scrape_reasoning confirming faithful content preservation and scrape_issues being minor or empty (Rank 4 at https://www.healthdirect.gov.au/sugar has an empty issues list yet still receives 0.20). This calibration mismatch causes the second _baseline_fidelity dimension to compute an average of 0.228 (L2) and trigger a contrastive fail, directly contradicting the first _baseline_fidelity dimension which scored the same documents at 0.9 (L5).

- **Coverage Diagnosis**: Document profiles show excellent coverage — all five documents address health risks of exceeding added sugar intake with specific conditions (cardiovascular disease, diabetes, obesity, fatty liver, dental problems) and quantitative thresholds (WHO <10%, AHA 6%, 100/150 kcal). No observable coverage gap exists.
- **Ranking Diagnosis**: N/A — _baseline_ranking scored 0.95 (L5) with no contrastive fail; the most relevant and authoritative sources appear at ranks 1-2, and no low-quality source outranks a high-quality one.
- **Scrape Diagnosis**: Scrape_score values are miscalibrated: Rank 4 (https://www.healthdirect.gov.au/sugar) has scrape_issues=[] and scrape_reasoning='No critical discrepancies or missing content detected' yet receives scrape_score=0.20. Ranks 1, 2, and 5 similarly receive 0.20 despite reasoning confirming full content preservation. Only Rank 3 (https://www.heart.org/...) scores 0.40. The low scores appear to be a default-floor or penalty-miscalibration issue rather than a reflection of actual scrape quality.

**Fix Actions**:
- Recalibrate the scrape_score assignment logic so that documents with empty or minor-only scrape_issues and scrape_reasoning confirming faithful preservation receive scores >= 0.8 (L4/L5), not a default floor of 0.20 (L1).
- Add a validation guard that flags contradictions between scrape_score and scrape_reasoning — if reasoning contains 'faithfully preserves' or 'no critical discrepancies' and scrape_issues is empty, the score should not be below 0.8.
- Deduplicate the _baseline_fidelity dimension evaluation to prevent two conflicting scores (0.9 vs 0.228) for the same set of documents, which inflates the penalty and creates an internally inconsistent evaluation.


---
### tc_a024035f (Score: 0.59) ❌
**Query**: `best binding agents and starches for structure in gluten-free whole grain bread baking`
**Category**: Food & Nutrition | **Intent**: same_source_different_angle

**Root Cause**: All five retrieved documents treat binders in generic gluten-free contexts with zero coverage of whole grain flour interactions (whole_grain_compatibility=0.15, L1), and starches appear only once via a 19-word Facebook post (Rank 3, authority=0.2). The ranking further compounds this by burying the most relevant result (YouTube, query_relevance_score=0.7) at Rank 5 while placing the low-authority Facebook post at Rank 3 above Cultures for Health (authority=0.5) and YouTube (authority=0.6).

- **Coverage Diagnosis**: The document profiles show a critical gap: no document addresses whole grain flour absorption, density management, or bran interference. Starches are nearly absent — only tapioca flour is mentioned, and only in the 19-word Facebook post (Doc 3). Every document's query_coverage_assessment lists 'whole grain' and 'starches' as missing aspects.
- **Ranking Diagnosis**: Rank 3 (Facebook post, authority=0.2, relevance=0.5, 19 words) outranks Rank 4 (Cultures for Health, authority=0.5, relevance=0.6) and Rank 5 (YouTube, authority=0.6, relevance=0.7). The most relevant result is buried at position 5, triggering the contrastive fail for 'most relevant result is buried' and 'social media above commercial blogs.'
- **Scrape Diagnosis**: Two documents have critically low scrape scores: Rank 2 (artofglutenfreebaking.com, scrape_score=0.20) with boilerplate/navigation leakage, and Rank 5 (YouTube, scrape_score=0.20) with non-clickable links as text. Rank 4 (culturesforhealth.com, scrape_score=0.60) has ERR_BLOCKED_BY_CLIENT error messages and base64 image placeholders interspersed in content. Average scrape score is 0.34.

**Fix Actions**:
- Add a query expansion/reformulation layer that decomposes multi-aspect queries ('binding agents AND starches AND whole grain') into sub-queries and merges results, ensuring each aspect is represented in the final result set.
- Implement an authority-content-density penalty in the ranking model: demote results with word_count < 50 and authority_score < 0.3 below results with authority_score > 0.5, preventing 19-word social media posts from outranking substantive commercial blog content.
- Update the scraper's boilerplate removal filter to strip navigation menus, cookie consent banners, and sidebar elements before emitting markdown, and add a post-processing step to remove ERR_BLOCKED_BY_CLIENT artifacts and base64 image placeholders from culturesforhealth.com and similar e-commerce domains.


---
### tc_b7028fb4 (Score: 0.74) ❌
**Query**: `live concert tour production crew staging sound engineering behind the scenes`
**Category**: Sports & Entertainment | **Intent**: novel

**Root Cause**: The primary failure is a critical ranking inversion: the Instagram reel (authority_score=0.3, query_relevance_score=0.5, 23 words, severely truncated) was placed at Rank 1, while the YouTube video (authority_score=0.8, query_relevance_score=0.95, full coverage) and Quora thread (authority_score=0.7, query_relevance_score=0.95) were buried at Ranks 4–5. This triggered the contrastive fail condition in _baseline_ranking (score 0.15, L1). A secondary failure is in _baseline_fidelity where pages with good content capture (MediaTech scrape_reasoning: 'faithfully preserves all visible text content', YouTube scrape_reasoning: 'All expected YouTube page elements preserved faithfully') received scrape_scores of 0.20 (L1), creating a contradiction that depressed the aggregated fidelity score to 0.284.

- **Coverage Diagnosis**: Coverage is adequate (L4, 0.7) — sound engineering is well-covered across results 2–5, staging appears in result 3, and crew roles appear in result 5. No single document is comprehensive, but the collective set addresses the exploratory intent. The gap is not coverage itself but that the most comprehensive documents (YouTube rank 4, Quora rank 5) are buried.
- **Ranking Diagnosis**: Critical inversion: Rank 1 (Instagram, authority 0.3, relevance 0.5) outranks Rank 4 (YouTube, authority 0.8, relevance 0.95) and Rank 5 (Quora, authority 0.7, relevance 0.95). The ideal order would place YouTube and Quora in positions 1–2, MediaTech and Stages at 3–4, and Instagram at 5 or excluded. The contrastive fail was triggered because the lowest-quality source is first and the highest-quality sources are last.
- **Scrape Diagnosis**: Two distinct scrape issues: (1) Rank 1 Instagram reel is severely truncated (23 words, single sentence) due to dynamic content not rendered — scrape_score=0.60 with issues 'Content severely truncated' and 'Likely dynamic content not rendered by scraper'. (2) Ranks 2–4 (MediaTech, Stages, YouTube) have scrape_score=0.20 (L1) despite their scrape_reasoning text confirming faithful content preservation with no issues — this is a scoring calibration anomaly. Rank 5 Quora (scrape_score=0.40) has Cloudflare challenge artifacts and duplicate content from a transient page load error.

**Fix Actions**:
- Add a relevance-and-authority-weighted reranking pass that demotes results with query_relevance_score < 0.6 or authority_score < 0.4 from the top 3 positions, preventing low-quality social media posts from outranking expert sources.
- Fix the scrape_score calibration for pages where scrape_issues=[] and scrape_reasoning confirms faithful capture — the current logic assigns 0.20 (L1) to well-scraped pages like MediaTech and YouTube, contradicting their own reasoning text; the scoring function should derive score from scrape_issues severity and content_completeness, not default to 0.20.
- Add Instagram-specific scraper handling with JavaScript rendering or API-based extraction to capture full reel descriptions, captions, and metadata instead of returning a 23-word truncated snippet.


---
### tc_531d905d (Score: 0.90) ❌
**Query**: `2026 Formula 1 season race calendar and driver lineup changes`
**Category**: Sports & Entertainment | **Intent**: novel

**Root Cause**: The scrape_score assignments are inverted relative to content quality: Rank 1 (scrape_score=0.20, issues=[], reasoning='faithfully reproduces all visible text') and Rank 2 (scrape_score=0.20, reasoning='faithfully preserves the original Wikipedia page structure') receive critically low scores despite confirmed faithful reproduction, while Rank 4 (Instagram, scrape_score=0.79, 'Content is heavily truncated, only the opening line is visible', word_count=26) receives the highest score. This inversion drives the aggregated _baseline_fidelity to 0.3106 (L2), which is the primary cause of the overall test failure.

- **Coverage Diagnosis**: Coverage is excellent — Wikipedia (rank 2) provides full coverage of both calendar and driver lineup changes (query_coverage_assessment.coverage_level='full'), and multiple official F1 sources cover the calendar. No observable coverage gap exists.
- **Ranking Diagnosis**: Minor misranking — Wikipedia (query_relevance_score=1.0, full coverage) is at rank 2 while the partial-coverage F1 beginner's guide (query_relevance_score=0.5) is at rank 1. This is a slight deviation but not the primary failure cause.
- **Scrape Diagnosis**: Critical scrape_score inversion across the document set: Ranks 1, 2, and 5 have scrape_score=0.20 despite complete content and faithful reproduction per scrape_reasoning; Rank 4 (Instagram) has scrape_score=0.79 despite heavy truncation (26 words, content_completeness='appears_truncated'). Additionally, Rank 5's scrape_issues contain Chinese text ('无重大缺失') in an English-language document profile.

**Fix Actions**:
- Add a post-scrape validation gate that cross-checks scrape_score against content_completeness and word_count: if content_completeness='complete' and word_count > 500, enforce minimum scrape_score of 0.6; if content_completeness='appears_truncated' and word_count < 100, cap scrape_score at 0.3.
- Fix the scrape_score computation to align with scrape_reasoning text — when reasoning contains 'faithfully reproduces' or 'faithfully preserves' and issues list is empty or only contains 'Minor' entries, the score should be >= 0.7, not 0.20.
- Enforce language consistency in scrape_issues and scrape_reasoning output: if detected_language='en', all generated issue descriptions and reasoning text must be in English — add a language guardrail that rejects or translates non-English strings like '无重大缺失'.


---
### tc_d6ace918 (Score: 0.87) ❌
**Query**: `latest research findings on long COVID neurological symptoms mechanisms`
**Category**: Science & Academia | **Intent**: novel

**Root Cause**: The scrape_score values are inverted: ranks 1-3 with content_completeness='complete' and scrape_reasoning confirming faithful preservation receive scrape_score=0.20 (L1), while ranks 4-5 with content_completeness='appears_truncated' and critical truncation issues receive scrape_score=0.60 (L3/L4). This inversion drives _baseline_fidelity to 0.30-0.312, failing the test. A secondary issue is that 3 of 5 documents (ranks 3, 4, 5) have empty publication_date fields, causing recency_signals to trigger a contrastive fail at score 0.50, which contradicts the expected <=0.40 threshold.

- **Coverage Diagnosis**: N/A — coverage scored 0.95 (L5); documents collectively address neurological symptoms, mechanisms, biomarkers, imaging, and therapeutic approaches.
- **Ranking Diagnosis**: N/A — ranking scored 0.90 (L5); peer-reviewed articles correctly rank above truncated social media and incomplete content.
- **Scrape Diagnosis**: Scrape scores are inverted: Rank 1 (https://pmc.ncbi.nlm.nih.gov/articles/PMC10901563/) has scrape_score=0.20 with content_completeness='complete' and scrape_reasoning='faithfully preserves the full text', while Rank 4 (https://www.facebook.com/nih.gov/posts/...) has scrape_score=0.60 with content_completeness='appears_truncated' and word_count=23. Complete documents should score >=0.8 and truncated documents should score <=0.4. Additionally, Rank 5 (https://www.nature.com/articles/s41579-022-00846-2) is truncated mid-sentence but scores 0.60, higher than any complete document.

**Fix Actions**:
- Fix the scrape_score computation logic to invert or correct the scoring: complete documents (content_completeness='complete') should receive scrape_score >= 0.80, while truncated documents (content_completeness='appears_truncated') should receive scrape_score <= 0.40. The current mapping appears reversed.
- Add a publication_date extraction step for news articles and social media posts: parse date metadata from OpenGraph tags, JSON-LD structured data, or visible date strings. For Rank 3 (nyulangone.org), Rank 4 (facebook.com/nih.gov), and Rank 5 (nature.com), the temporal_markers field contains date information (e.g., '17 April 2023' for Rank 5) that should be normalized into publication_date.
- Add a validation guard in the recency_signals scoring function: when contrastive_fail_triggered is true, enforce score <= 0.40 to prevent the contradiction flagged in warnings.


---
### tc_0aff21d2 (Score: 0.74) ❌
**Query**: `Byzantine Empire fall Constantinople 1453 Ottoman conquest causes decline significance medieval eastern roman history`
**Category**: History & Humanities | **Intent**: novel

**Root Cause**: The pipeline retrieved a result set dominated by low-authority commercial/forum sources (Facebook authority=0.2, Reddit authority=0.3, YouTube authority=0.35, Quora authority=0.0) where three of five documents suffered critical scrape failures — Facebook truncated to 25 words, Reddit truncated to 28 words, and Quora returned only an error message (scrape_score=0.0). This caused both _baseline_fidelity (0.35/0.3052, L2) and source_authority (0.50, L3 with contrastive_fail) to fall below passing thresholds, dragging the overall score to 0.7396.

- **Coverage Diagnosis**: Coverage is adequate on paper (0.78, L4) because Wikipedia alone covers all four query dimensions (causes, siege, decline, significance). However, the supporting documents that should deepen coverage on causes (Fourth Crusade, religious schism) and broader significance are either truncated (Facebook, Reddit) or empty (Quora), leaving Wikipedia as the sole substantive source.
- **Ranking Diagnosis**: YouTube (query_relevance_score=0.95, authority_score=0.35) is ranked at position 4, behind Facebook (relevance=0.8, authority=0.2) at rank 2 and Reddit (relevance=0.3, authority=0.3) at rank 3. This violates both authority and relevance ordering, as a more relevant and higher-authority source is buried below less relevant, lower-authority ones.
- **Scrape Diagnosis**: Three critical scrape failures: (1) Facebook truncated after first sentence (scrape_score=0.79 but word_count=25, content_completeness='appears_truncated'); (2) Reddit truncated after first two sentences (scrape_score=0.79 but word_count=28); (3) Quora returned only error message 'Something went wrong' (scrape_score=0.0, word_count=11). Additionally, YouTube has a contradictory scrape_score=0.2 (L1) despite scrape_reasoning stating content was faithfully captured with a 2004-word transcript.

**Fix Actions**:
- Add domain authority boosting in the ranking config to penalize commercial/forum domains (facebook.com, reddit.com, quora.com) for academic/history queries, promoting scholarly sources (university presses, JSTOR, museum sites, academic blogs) above user-generated content.
- Implement a scrape retry with JavaScript rendering fallback for dynamic-content domains (facebook.com, quora.com) where initial scrape returns <50 words or error messages, and exclude results with scrape_score=0.0 from the final result set rather than serving error pages.
- Fix the YouTube scrape_score calculation: the scrape_reasoning confirms faithful capture of transcript and metadata (word_count=2004, content_completeness='complete'), yet scrape_score=0.2 (L1) — correct the scoring logic so complete transcripts with minor transcription errors score at least L3 (0.5+).


---
