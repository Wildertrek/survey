# Cross-Model PCA Analysis Results

Principal Component Analysis across all 44 personality models (6,694 trait rows, 1536-dim embeddings).

**Reproduce:** `python notebooks/01_cross_model_pca_analysis.py`

---

## Key Finding

The 44-model atlas is **not redundant**. PCA over the unified 1,536-dimensional embedding space shows that 50 components capture only 56.9% of variance, and no single component exceeds 4.5%. This high intrinsic dimensionality proves that the models encode genuinely distinct psychological constructs — they are not repackagings of the same latent factors. This directly validates the atlas's breadth: practitioners need access to multiple model families (trait-based, clinical, narcissism, motivational, etc.) because no single model captures the full personality space.

---

## Summary

| Metric | Value |
|--------|-------|
| Models analyzed | 44 |
| Total trait rows | 6,694 |
| Unique factors | 313 |
| Embedding dimensions | 1,536 |
| PCA components computed | 50 |

## Computational Profile

All artifacts were generated on a single machine with no GPU required.

| Component | Details |
|-----------|---------|
| **Embedding model** | OpenAI `text-embedding-3-small` (1,536 dimensions) |
| **Embedding cost** | ~$0.27 total for all 6,694 rows (~$0.006/model) |
| **Embedding latency** | ~5–7 minutes for all 44 models (sequential API calls) |
| **PCA runtime** | < 10 seconds (scikit-learn, single CPU core) |
| **RF classifier training** | < 2 seconds per model (100-tree Random Forest) |
| **Total RF models** | 88 files (44 classifiers + 44 label encoders) |
| **RF model sizes** | 20 KB–12 MB per model (median ~130 KB) |
| **Dataset storage** | 520 KB (44 CSV files) |
| **Embedding storage** | 224 MB (44 embedding CSVs, 1,536 floats/row) |
| **RF model storage** | 31 MB (88 pickle files) |
| **Total footprint** | ~256 MB (datasets + embeddings + models) |
| **Dependencies** | pandas, scikit-learn, numpy, matplotlib, openai |
| **Hardware** | Any machine with Python 3.12; no GPU required |

The entire pipeline — from raw CSV datasets to trained classifiers and PCA visualizations — runs end-to-end in under 10 minutes on commodity hardware. The dominant cost is embedding generation via the OpenAI API ($0.27 total), which is a one-time expense. All downstream analysis (PCA, similarity, visualization) is CPU-only and completes in seconds.

## Variance Explained

| Components | Cumulative Variance |
|-----------|-------------------|
| PC1 | 4.5% |
| PC1–5 | 15.5% |
| PC1–10 | 25.2% |
| PC1–20 | 37.1% |
| PC1–50 | 56.9% |

The high dimensionality required to capture variance confirms that personality models occupy meaningfully distinct regions of semantic space — they are not redundant repackagings of the same constructs.

![Scree Plot](pca_scree_plot.png)

## Model Similarity

### Most Similar Pairs

| Model A | Model B | Cosine Similarity |
|---------|---------|------------------|
| IPN | PNI | 0.959 |
| DT4 | DT3 | 0.955 |
| FFNI | PNI | 0.950 |
| FFNI | NPI | 0.940 |
| FFNI | IPN | 0.918 |

The highest-similarity cluster is among narcissism instruments (IPN, PNI, FFNI, NPI), which share overlapping construct definitions (exploitativeness, entitlement, grandiosity). DT4 and DT3 are near-identical by design (the tetrad extends the triad with sadism). These overlaps are expected and serve as a **sanity check** — the embedding space faithfully preserves known theoretical relationships.

### Least Similar Pairs

| Model A | Model B | Cosine Similarity |
|---------|---------|------------------|
| PAPC | TKI | 0.343 |
| FFNI-SF | WAIS | 0.309 |
| NARQ | WAIS | 0.301 |
| TAT | WAIS | 0.301 |
| TKI | WAIS | 0.268 |

The lowest similarities involve WAIS (cognitive intelligence) paired with personality/narcissism models — confirming that cognitive ability and personality trait constructs occupy fundamentally different semantic regions, consistent with decades of differential psychology research.

![Model Centroids in PCA Space](pca_model_centroids_2d.png)

## Category Variance Contribution

| Category | Variance |
|----------|---------|
| Narcissism | 352.5 |
| Clinical | 347.9 |
| Trait-Based | 337.0 |
| Cognitive | 307.7 |
| Motivational | 277.9 |
| Application | 272.6 |
| Dark Personality | 255.8 |
| Holistic | 209.1 |
| Interpersonal | 183.9 |

Narcissism-based models contribute the most variance, reflecting the granular differentiation between grandiose, vulnerable, and pathological narcissism constructs. Clinical models rank second due to the wide range of psychopathology dimensions (depression, anxiety, psychopathy, personality disorders). Trait-Based models (OCEAN, HEXACO, MBTI, 16PF) rank third — despite being the most widely used in NLP applications, they do not dominate the variance, underscoring the value of looking beyond Big Five for AI personality modeling.

## Top Factors by Variance

The five highest-variance factors across all models:

| Model | Factor | Variance | Rows |
|-------|--------|----------|------|
| SCM | Environment | 222.3 | 36 |
| SCM | Interpersonal | 203.7 | 36 |
| SCM | Affective | 199.2 | 36 |
| SCM | Behavior | 195.7 | 36 |
| MCMI | Personality Patterns | 187.6 | 45 |

## Visualizations

| File | Description |
|------|-------------|
| [`pca_scree_plot.png`](pca_scree_plot.png) | Variance explained by each principal component |
| [`pca_2d_all_models.png`](pca_2d_all_models.png) | 2D PCA projection of all 6,694 trait rows, colored by model |
| [`pca_model_centroids_2d.png`](pca_model_centroids_2d.png) | Model centroid positions in PCA space |
| [`pca_factor_loadings_heatmap.png`](pca_factor_loadings_heatmap.png) | Top-20 factor loadings on PC1–PC5 |

![All Models in PCA Space](pca_2d_all_models.png)

![Factor Loadings Heatmap](pca_factor_loadings_heatmap.png)

## Data Files

| File | Description |
|------|-------------|
| [`pca_variance_explained.csv`](pca_variance_explained.csv) | Variance explained by top-50 components |
| [`pca_top_factors_by_variance.csv`](pca_top_factors_by_variance.csv) | All factors ranked by variance contribution |
| [`pca_model_overlap_matrix.csv`](pca_model_overlap_matrix.csv) | 44×44 cosine similarity matrix between model centroids |
| [`pca_summary_report.json`](pca_summary_report.json) | Machine-readable summary of all metrics |

## Model Row Counts

| Model | Rows | | Model | Rows |
|-------|------|-|-------|------|
| PCT | 899 | | OCEAN | 120 |
| BDI | 756 | | RIASEC | 120 |
| SCID | 401 | | TMP | 108 |
| FFNI | 360 | | DT4 | 96 |
| MMPI | 360 | | EPM | 90 |
| FSLS | 360 | | MCMI | 84 |
| TCI | 252 | | SDT | 84 |
| GAD-7 | 252 | | EM | 81 |
| 16PF | 192 | | FTM | 80 |
| SCM | 180 | | IPN | 80 |
| NPI | 168 | | CEST | 72 |
| PNI | 168 | | MCMI-Narc | 72 |
| MBTI | 144 | | PAPC | 72 |
| CS | 136 | | HEXACO | 66 |
| STBV | 128 | | BT | 64 |
| WAIS | 60 | | MST | 64 |
| FFNI-SF | 60 | | RFT | 56 |
| DT3 | 54 | | NARQ | 48 |
| HSNS | 48 | | TEI | 48 |
| RIT | 45 | | AAM | 40 |
| TAT | 39 | | CMOA | 36 |
| DISC | 31 | | TKI | 20 |

---

## Implications for AI Personality Modeling

### Why 44 Models?

Current AI systems that model personality almost exclusively use OCEAN (Big Five) — a single model occupying 120 of 6,694 rows (1.8%) and ranked 17th by row count. The PCA results show that OCEAN captures only a narrow slice of the personality space. The atlas provides 43 additional models spanning clinical psychopathology, narcissism subtypes, motivational orientations, cognitive styles, and interpersonal dynamics — all of which encode semantically distinct constructs that OCEAN cannot represent.

### Practical Implications

1. **For LLM personality prompting:** The 313 unique factors provide a structured vocabulary for fine-grained character specification far beyond "high openness, low neuroticism." A game NPC can be specified using Bartle Types (Killer/Explorer/Achiever/Socializer), a clinical simulation agent using MCMI personality patterns, or an adversarial red-team agent using Dark Tetrad traits.

2. **For AI safety and red-teaming:** The 10 narcissism models and 9 clinical models provide the construct granularity needed to stress-test LLM behavior under pathological personality conditions (e.g., distinguishing grandiose vs. vulnerable narcissism responses).

3. **For cross-model transfer:** The 44x44 cosine similarity matrix enables researchers to identify which models provide redundant vs. complementary information for a given task, avoiding unnecessary computational overhead.

4. **For benchmarking:** The trained RF classifiers (one per model) can classify any new text embedding into the appropriate personality factor, enabling automated personality annotation of LLM outputs at scale.

### What the PCA Does Not Show

This analysis operates on the **lexical embedding space** of trait descriptors. It validates that the atlas's 44 models encode diverse constructs, but it does not measure how well LLMs can *use* these constructs to produce behaviorally distinct agents. That empirical validation — applying the atlas to multi-agent personality inference — is the subject of the companion PRISM protocol and MindBench benchmark (separate work).

---

*Generated by [`notebooks/01_cross_model_pca_analysis.py`](../notebooks/01_cross_model_pca_analysis.py)*
