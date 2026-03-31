# Research Question Summary

Consolidated findings from all 14 research questions, PCA, and knowledge graph analyses.

**Paper:** "A Survey and Computational Atlas of Personality Models"

## Experiment 1: Classification Validation

| RQ | Question | Key Finding |
|----|----------|-------------|
| 1 | Discriminant validity on novel items | Mean accuracy 58.6% (95% CI: [52.8%, 64.4%]); 68.6% on human items |
| 2 | Factor count vs. accuracy | r = -0.67 (95% CI: [-0.83, -0.49], p < 0.001) |
| 3 | Cross-provider judge agreement | Inter-judge kappa = 0.99; expected-factor agreement 95.7% |
| 4 | RF vs. LLM judge gap | 66.7% RF-judge agreement; judges correct 95.7% |
| 5 | Cross-model convergent validity | 3072-dim retrieves 23% more models per query |
| 6 | Category-level patterns | Motivational (74.5%) > Narcissism (68.3%) > Trait-Based (64.0%) > Cognitive (51.8%) > App/Holistic (50.9%) > Clinical (50.6%) > Interpersonal (23.7%) |
| PCA | Atlas dimensionality | 50 PCs capture only 56.9% variance; Trait-Based ranks 3rd in per-model contribution |
| KG | Knowledge graph validation | Mantel r = 0.66 (p < 0.001); graph density predicts accuracy (delta R^2 = 0.11) |

## Experiment 2: Model Improvement Cycle

| RQ | Question | Key Finding |
|----|----------|-------------|
| 7 | Embedding upgrade (3072-dim) | +5.1% mean; 28/44 improved, 13 decreased |
| 8 | Data augmentation (14 models) | +25.9% on targeted models; all 14 improved |
| 9 | Hierarchical classification | +4.8% on targeted models; 1/8 won in ablation |
| -- | Combined best-per-model | 58.7% to 71.5% (95% CI: [67.4%, 75.6%]); paired Cohen's d = 1.03 |
| -- | Recommended default pipeline | 69.5% (3072-dim + augmented where available); only 2.1pp below oracle |

## Experiment 3: External Validation

| RQ | Question | Key Finding |
|----|----------|-------------|
| 10 | Multi-generator consistency | GPT-4o 58.7% vs. Opus 55.5% (delta = 3.3pp, p = .041) |
| 11 | Human item classification | 83.5% kNN on 418 items from 22 instruments (oracle 86.8%) |
| 12 | Cross-instrument convergence | 100% model/category hit rate in top-20 (n = 418) |

## Semantic Personality Index (SPI)

| RQ | Question | Key Finding |
|----|----------|-------------|
| 13 | Embedding space topology | 7 categories: silhouette ~ 0 (0.0002); data-driven k=15: 0.098 |
| 14 | Semantic reorganization | 15 SPI clusters; Clinical splits into 4, Narcissism into 3; four clusters (Dominance, Activation, Withdrawal, Self-Direction) span all 7 categories, Warmth spans 6 |

## Supplementary Experiments (Reviewer Responses)

| Experiment | Finding |
|-----------|---------|
| Open-source embeddings (MiniLM) | 50.9% accuracy (vs 58.6% OpenAI); Spearman r_s = 0.748 |
| Classifier ablation | RF/LR/SVM/kNN all near-ceiling on CV; Friedman p < 0.001 |
| Trait-3rd bootstrap | Rank 3 in 100% of 10K bootstraps (p = 0.99) |
| Circumplex orthogonality | C0-C1 cosine = 0.091 (84.8 degrees); near-orthogonality expected in 50-dim |
| K-means stability | Mean ARI = 0.710; 6/15 stable, 6 moderate, 3 unstable |
| Cosine calibration | Random = 0.262, within-model = 0.430, within-category = 0.700 |

## Data Files

- `validation/individual_model_results.csv` — Per-model accuracy for all 44 models
- `validation/category_results.csv` — Category-level aggregates
- `validation/experiment2_comparison.csv` — Exp 1 vs Exp 2 per-model comparison
- `validation/factor_complexity.csv` — Factor count vs accuracy data
- `pca_summary_report.json` — PCA variance explained, top components
- `reviewer_experiments/` — All supplementary experiment JSON results
