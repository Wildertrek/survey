# Glossary of Terms

Every technical term used in the paper, defined in plain language.

> Raetano, J., Gregor, J., & Tamang, S. (2026). *A Survey and Computational Atlas of Personality Models.* ACM Transactions on Intelligent Systems and Technology (TIST). Under review.

---

## The Problem

| Term | What it means |
|------|---------------|
| **OCEAN (Big Five)** | The dominant personality model: **O**penness, **C**onscientiousness, **E**xtraversion, **A**greeableness, **N**euroticism. Nearly every AI personality paper uses only this one model, ignoring 43 others. |
| **Seven traditions** | The 44 models are organized by disciplinary origin: **Clinical** (MMPI, BDI, GAD-7, diagnostic instruments), **Motivational** (Self-Determination Theory, Maslow, why people act), **Interpersonal** (Attachment Theory, IPC, how people relate), **Cognitive** (MBTI, WAIS, how people think), **Narcissism-Based** (NPI, Dark Triad, PNI, narcissism-specific), **App/Holistic** (Holland RIASEC, DISC, career/work), **Trait-Based** (OCEAN, HEXACO, 16PF, general trait models). |
| **Computable** | Translated from PDF manuals and textbook descriptions into machine-readable formats that software can process, search, and classify automatically. |

## The Encoding

| Term | What it means |
|------|---------------|
| **Factor chain** | The paper's core encoding. Each trait (factor) is expanded into a structured 5-word tuple: *(Factor, Adjective, Synonym, Verb, Noun)*. Example: `(Openness, Artistic, Creative, Create, Creativity)`. |
| **Lexical tuple** | An ordered set of words following a fixed schema. "Lexical" = word-based; "tuple" = a fixed-length ordered sequence (from mathematics/computer science). |
| **6,694 chains / 358 factors** | 44 models contain 358 total factors (traits, scales, subscales). Each factor has multiple chains capturing different word combinations for the same trait. Total: 6,694 chains across all models. |
| **Neural embedding** | Each chain is converted to a 1,536-dimensional numerical vector (via OpenAI text-embedding-3-small). Similar concepts produce similar vectors, putting all 44 models into one shared mathematical space. |
| **Embedding space** | The shared 1,536-dimensional mathematical space where all factor chains live as vectors. Distance between vectors reflects semantic similarity; traits that mean similar things are close together regardless of which model they come from. |
| **Trained classifiers** | Four classifiers per model (RF, SVC, LR, kNN), 176 total. Given a new sentence describing a personality trait, they predict which factor of that model the sentence belongs to. SVC and kNN are recommended for deployment; RF is retained as a conservative baseline. |
| **Random Forest (RF)** | An ensemble machine learning method that aggregates predictions from many decision trees. Each tree votes on the answer; the majority wins. Robust and interpretable, but the weakest of the four classifiers on novel items. |
| **Oracle ceiling** | The accuracy attainable when each model is retrospectively assigned its single best-performing classifier. Represents the practical upper bound of the current classifier suite (86.8% on human items). |

## The Validation

| Term | What it means |
|------|---------------|
| **Classification accuracy (71.5%)** | When classifiers are tested on held-out items, they correctly identify the right factor 71.5% of the time on average across all 44 models. Chance would be ~6-12% depending on model size. |
| **Cohen's *d* = 1.03** | Standardized effect size comparing baseline vs. improved classifiers across the same 44 models. Conventional thresholds: 0.2 = small, 0.5 = medium, 0.8 = large. **1.03 is a large effect**; the improvements are substantial, not marginal. |
| **Human-authored items (418)** | Real questionnaire items written by psychologists, drawn from 22 published instruments (e.g., IPIP-50, TIPI, BFI-44, BDI, HEXACO-PI-R). Tests whether classifiers generalize to real-world content they have never seen during training. |
| **Generalization** | The ability of a classifier to perform well on new, unseen data, not just the data it was trained on. The human items test this: they come from published instruments the classifiers never encountered. |
| **100% model-level convergence** | Every testable model had its human items classified above chance. No model completely failed. |
| **Triple-judge panel (95.7%)** | Three independent LLM judges were each shown every factor chain and asked which factor it belongs to. They agreed with ground truth 95.7% of the time (Cohen's kappa = 0.99), establishing a quality ceiling: the encoding itself is sound, and the remaining gap is classifier capacity. |
| **Cohen's kappa** | A statistic measuring inter-rater agreement beyond chance. 0 = chance agreement, 1 = perfect agreement. Kappa = 0.99 means near-perfect agreement among the three judges. |

## The Discovery

| Term | What it means |
|------|---------------|
| **Semantic signal** | Meaningful pattern in the embedding space. "No semantic signal" means the grouping carries no information about what the traits actually mean; the labels are administrative, not substantive. |
| **Silhouette score (~ 0)** | Measures how well data points match their assigned cluster labels. Ranges from -1 (wrong clusters) to +1 (perfect clusters). Near 0 means the 7 disciplinary categories have essentially no semantic coherence; a Clinical trait is no more similar to other Clinical traits than to Motivational or Trait-Based ones. |
| **Semantic Personality Index (SPI)** | Instead of using the 7 human-assigned categories, k-means clustering (k=15) was applied to all embedding vectors to find natural groupings. These 15 data-driven clusters are the SPI. |
| **k-means clustering** | An algorithm that partitions data into *k* groups by minimizing the distance between each point and its cluster center. Here, k=15 means the algorithm found 15 natural groupings in the embedding space. |
| **Diagnostic boundaries** | Clinically established distinctions between conditions. The SPI recovers these automatically: Clinical fragments into Psychopathology, Depression, Reactive Aggression, and Anxiety. Narcissism fragments into Shame, Dark Manipulation, and Grandiose. These map onto recognized diagnostic categories without any clinical labels as input. |
| **Interpersonal Circumplex** | Theory (Leary 1957, Wiggins 1979) that all interpersonal behavior organizes around two orthogonal axes: **Warmth** (communion/affiliation) and **Dominance** (agency/control). The SPI is consistent with this: four clusters (C1, C4, C6, C7) span all 7 traditions, while Warmth (C0) spans six of seven. A theory proposed from within one tradition, now supported across seven. |
| **Jangle fallacy** | Different names masking the same construct (Kelley, 1927). Example: IPN Exploitativeness and PNI Exploitativeness come from different traditions but have cosine similarity 0.959, nearly identical *lexical content* under different names. The SPI provides the first large-scale evidence consistent with jangle across 44 models. Note: embedding proximity demonstrates shared vocabulary, not proven construct equivalence; convergent validity at the score level would be needed to fully confirm jangle. |
| **Jingle fallacy** | Same name masking different constructs (Block, 1995). Does "Extraversion" in OCEAN, HEXACO, and EPM mean the same thing? If they land in the same SPI cluster, that is evidence against jingle for that construct. The SPI makes this testable. |
| **PCA (Principal Component Analysis)** | A statistical method that identifies the directions of maximum variance in high-dimensional data. Used here to measure how much unique information each model contributes to the overall embedding space. |
| **OCEAN ranks third** | PCA shows that Trait-Based models (OCEAN, HEXACO) contribute less marginal information per model than Interpersonal or Cognitive models. Adding another Big Five variant to your AI system gives you less new information than adding one model from a different tradition. |
| **Cosine similarity** | Measures the angle between two vectors. Ranges from -1 (opposite) to +1 (identical direction). Used throughout the paper to quantify how semantically similar two traits or clusters are. |
| **t-SNE / UMAP** | Dimensionality reduction methods that project high-dimensional embeddings (1,536-dim) into 2D for visualization. The SPI cluster plots use these to show how traits group in the embedding space. |
| **HiTOP** | The Hierarchical Taxonomy of Psychopathology (Kotov et al., 2017). A dimensional reorganization of clinical constructs into spectra, explicitly addressing overlap among DSM categories. The SPI provides methodological triangulation: HiTOP uses symptom co-occurrence; the SPI uses semantic content. Different methods, compatible structure. |
