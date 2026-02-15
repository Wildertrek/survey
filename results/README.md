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
| Categories | 7 |
| Total trait rows | 6,694 |
| Unique factors | 316 |
| Embedding dimensions | 1,536 |
| PCA components computed | 50 |

## Atlas Taxonomy (7 Categories, 44 Models)

| # | Category | Models | Rows | Description |
|---|----------|--------|------|-------------|
| 1 | **Trait-Based** | OCEAN, HEXACO, EPM, 16PF, MBTI, FTM | 692 | General personality structure (Big Five, HEXACO, temperaments) |
| 2 | **Narcissism-Based** | NPI, PNI, FFNI, FFNI-SF, NARQ, HSNS, IPN, MCMI-N, DT3, DT4 | 1,170 | Narcissism subtypes and dark personality traits |
| 3 | **Motivational & Value** | STBV, MST, RFT, SDT, AAM, CS | 508 | Drives, values, regulatory focus, strengths |
| 4 | **Cognitive & Learning** | PCT, SCM, CEST, FSLS | 1,511 | Cognitive styles, learning preferences, personal constructs |
| 5 | **Clinical & Health** | MMPI, TCI, TMP, BDI, GAD-7, SCID, MCMI, RIT, TAT, WAIS | 2,259 | Psychopathology, clinical syndromes, diagnostic instruments, cognitive assessment |
| 6 | **Interpersonal & Conflict** | TKI, DISC | 51 | Conflict resolution styles, workplace interaction patterns |
| 7 | **Application & Holistic** | RIASEC, BT, TEI, EM, PAPC, CMOA | 503 | Vocational interests, emotional intelligence, affect models |

Clinical & Health is the largest category by both model count (10) and row count (2,259), reflecting the granularity of DSM-based instruments (SCID alone has 401 rows across 16 diagnostic categories). Cognitive & Learning ranks second by rows (1,511) despite having only 4 models, driven by PCT's 899-row construct repertoire. Narcissism-Based has 10 instruments, reflecting the field's sustained effort to differentiate grandiose, vulnerable, pathological, and dark personality constructs.

## Computational Profile

All artifacts were generated on a single machine with no GPU required.

| Component | Details |
|-----------|---------|
| **Embedding model** | OpenAI `text-embedding-3-small` (1,536 dimensions) |
| **Embedding cost** | ~$0.27 total for all 6,694 rows (~$0.006/model) |
| **Embedding latency** | ~5-7 minutes for all 44 models (sequential API calls) |
| **PCA runtime** | < 10 seconds (scikit-learn, single CPU core) |
| **RF classifier training** | < 2 seconds per model (100-tree Random Forest) |
| **Total RF models** | 88 files (44 classifiers + 44 label encoders) |
| **RF model sizes** | 20 KB-12 MB per model (median ~130 KB) |
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
| PC1-5 | 15.5% |
| PC1-10 | 25.2% |
| PC1-20 | 37.1% |
| PC1-50 | 56.9% |

The high dimensionality required to capture variance confirms that personality models occupy meaningfully distinct regions of semantic space — they are not redundant repackagings of the same constructs.

![Scree Plot](pca_scree_plot.png)

## Model Similarity

### Most Similar Pairs

| Model A | Model B | Category | Cosine Similarity |
|---------|---------|----------|------------------|
| IPN | PNI | Narcissism-Based | 0.959 |
| DT4 | DT3 | Narcissism-Based | 0.955 |
| FFNI | PNI | Narcissism-Based | 0.950 |
| FFNI | NPI | Narcissism-Based | 0.940 |
| FFNI | IPN | Narcissism-Based | 0.918 |

All five most-similar pairs are within the Narcissism-Based category — instruments that share overlapping construct definitions (exploitativeness, entitlement, grandiosity). DT4 and DT3 are near-identical by design (the tetrad extends the triad with sadism). These overlaps serve as a **sanity check**: the embedding space faithfully preserves known theoretical relationships.

### Least Similar Pairs

| Model A | Model B | Categories | Cosine Similarity |
|---------|---------|-----------|------------------|
| PAPC | TKI | App/Holistic vs. Interpersonal | 0.343 |
| FFNI-SF | WAIS | Narcissism vs. Clinical | 0.309 |
| NARQ | WAIS | Narcissism vs. Clinical | 0.301 |
| TAT | WAIS | Clinical vs. Clinical | 0.301 |
| TKI | WAIS | Interpersonal vs. Clinical | 0.268 |

The lowest similarities involve WAIS (cognitive intelligence) paired with personality/narcissism models — confirming that cognitive ability and personality trait constructs occupy fundamentally different semantic regions, consistent with decades of differential psychology research.

![Model Centroids in PCA Space](pca_model_centroids_2d.png)

## Category Variance Contribution

| Category | Models | Total Variance | Variance/Model |
|----------|--------|---------------|----------------|
| **Narcissism-Based** | 10 | 350.2 | 35.0 |
| **Clinical & Health** | 10 | 347.9 | 34.8 |
| **Trait-Based** | 6 | 337.0 | 56.2 |
| **Cognitive & Learning** | 4 | 307.7 | 76.9 |
| **Motivational & Value** | 6 | 277.9 | 46.3 |
| **Application & Holistic** | 6 | 258.8 | 43.1 |
| **Interpersonal & Conflict** | 2 | 183.9 | 92.0 |

**Total variance** ranks Narcissism-Based first (350.2), driven by 10 instruments differentiating grandiose, vulnerable, pathological, and dark personality constructs.

But **variance per model** tells a different story — and is the more actionable metric for practitioners deciding which categories to include:

1. **Interpersonal & Conflict** (92.0/model) — just 2 models (TKI, DISC), each highly distinctive
2. **Cognitive & Learning** (76.9/model) — 4 instruments covering personal constructs, social cognition, learning styles
3. **Trait-Based** (56.2/model) — OCEAN, HEXACO, MBTI, 16PF rank third, not first
4. **Motivational & Value** (46.3/model) — drives, values, and regulatory focus
5. **Application & Holistic** (43.1/model) — vocational interests, emotional intelligence, affect

Despite being the most widely used in NLP applications, Trait-Based models rank only 3rd in per-model discriminative power. Researchers building personality-aware AI systems should look **beyond Big Five** — adding even one Cognitive or Interpersonal model provides more marginal information than adding another trait-based instrument.

## Top Factors by Variance

The five highest-variance factors across all models:

| Model | Category | Factor | Variance | Rows |
|-------|----------|--------|----------|------|
| SCM | Cognitive | Environment | 222.3 | 36 |
| SCM | Cognitive | Interpersonal | 203.7 | 36 |
| SCM | Cognitive | Affective | 199.2 | 36 |
| SCM | Cognitive | Behavior | 195.7 | 36 |
| MCMI | Clinical | Personality Patterns | 187.6 | 45 |

SCM (Social-Cognitive Model) dominates the top-4, suggesting that cognitive-social constructs (how people process their environment, relate to others, regulate affect, and behave) provide the broadest semantic coverage. The 5th slot goes to MCMI's Personality Patterns — clinical psychopathology dimensions that span a wide range of human dysfunction.

## Visualizations

| File | Description |
|------|-------------|
| [`pca_scree_plot.png`](pca_scree_plot.png) | Variance explained by each principal component |
| [`pca_2d_all_models.png`](pca_2d_all_models.png) | 2D PCA projection of all 6,694 trait rows, colored by category |
| [`pca_model_centroids_2d.png`](pca_model_centroids_2d.png) | Model centroid positions in PCA space |
| [`pca_factor_loadings_heatmap.png`](pca_factor_loadings_heatmap.png) | Top-20 factor loadings on PC1-PC5 |

![All Models in PCA Space](pca_2d_all_models.png)

![Factor Loadings Heatmap](pca_factor_loadings_heatmap.png)

## Data Files

| File | Description |
|------|-------------|
| [`pca_variance_explained.csv`](pca_variance_explained.csv) | Variance explained by top-50 components |
| [`pca_top_factors_by_variance.csv`](pca_top_factors_by_variance.csv) | All factors ranked by variance contribution |
| [`pca_model_overlap_matrix.csv`](pca_model_overlap_matrix.csv) | 44x44 cosine similarity matrix between model centroids |
| [`pca_summary_report.json`](pca_summary_report.json) | Machine-readable summary of all metrics |

## Model Row Counts

| Model | Category | Rows | | Model | Category | Rows |
|-------|----------|------|-|-------|----------|------|
| PCT | Cognitive | 899 | | OCEAN | Trait-Based | 120 |
| BDI | Clinical | 756 | | RIASEC | Application | 120 |
| SCID | Clinical | 401 | | TMP | Clinical | 108 |
| FFNI | Narcissism | 360 | | DT4 | Narcissism | 96 |
| MMPI | Clinical | 360 | | EPM | Trait-Based | 90 |
| FSLS | Cognitive | 360 | | MCMI | Clinical | 84 |
| TCI | Clinical | 252 | | SDT | Motivational | 84 |
| GAD-7 | Clinical | 252 | | EM | App/Holistic | 81 |
| 16PF | Trait-Based | 192 | | FTM | Trait-Based | 80 |
| SCM | Cognitive | 180 | | IPN | Narcissism | 80 |
| NPI | Narcissism | 168 | | CEST | Cognitive | 72 |
| PNI | Narcissism | 168 | | MCMI-N | Narcissism | 72 |
| MBTI | Trait-Based | 144 | | PAPC | App/Holistic | 72 |
| CS | Motivational | 136 | | HEXACO | Trait-Based | 66 |
| STBV | Motivational | 128 | | BT | App/Holistic | 64 |
| WAIS | Clinical | 60 | | MST | Motivational | 64 |
| FFNI-SF | Narcissism | 60 | | RFT | Motivational | 56 |
| DT3 | Narcissism | 54 | | NARQ | Narcissism | 48 |
| HSNS | Narcissism | 48 | | TEI | App/Holistic | 48 |
| RIT | Clinical | 45 | | AAM | Motivational | 40 |
| TAT | Clinical | 39 | | CMOA | App/Holistic | 36 |
| DISC | Interpersonal | 31 | | TKI | Interpersonal | 20 |

---

## Implications for AI Personality Modeling

### Why 44 Models?

Current AI systems that model personality almost exclusively use OCEAN (Big Five) — a single model occupying 120 of 6,694 rows (1.8%) and ranked 17th by row count. The PCA results show that OCEAN captures only a narrow slice of the personality space. The atlas provides 43 additional models spanning clinical psychopathology, narcissism subtypes, motivational orientations, cognitive styles, and interpersonal dynamics — all of which encode semantically distinct constructs that OCEAN cannot represent.

### Practical Implications

1. **For LLM personality prompting:** The 316 unique factors provide a structured vocabulary for fine-grained character specification far beyond "high openness, low neuroticism." A game NPC can be specified using Bartle Types (Killer/Explorer/Achiever/Socializer), a clinical simulation agent using MCMI personality patterns, or an adversarial red-team agent using Dark Tetrad traits.

2. **For AI safety and red-teaming:** The 10 narcissism models and 10 clinical models provide the construct granularity needed to stress-test LLM behavior under pathological personality conditions (e.g., distinguishing grandiose vs. vulnerable narcissism responses).

3. **For cross-model transfer:** The 44x44 cosine similarity matrix enables researchers to identify which models provide redundant vs. complementary information for a given task, avoiding unnecessary computational overhead.

4. **For benchmarking:** The trained RF classifiers (one per model) can classify any new text embedding into the appropriate personality factor, enabling automated personality annotation of LLM outputs at scale.

### What the PCA Does Not Show

This analysis operates on the **lexical embedding space** of trait descriptors. It validates that the atlas's 44 models encode diverse constructs, but it does not measure how well LLMs can *use* these constructs to produce behaviorally distinct agents. That empirical validation — applying the atlas to multi-agent personality inference — is the subject of the companion PRISM protocol and MindBench benchmark (separate work).

---

*Generated by [`notebooks/01_cross_model_pca_analysis.py`](../notebooks/01_cross_model_pca_analysis.py)*
