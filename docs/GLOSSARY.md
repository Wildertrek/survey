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
| **Psychometric instrument** | A scientifically validated questionnaire published in peer-reviewed literature (e.g., BFI-44, IPIP-50, GAD-7, HEXACO-60, TIPI). The atlas validated classifiers on 418 items from 22 such instruments. |
| **Facet / subscale** | A lower-order dimension within a larger instrument. For example, the FFNI has 15 facets organized under 3 higher-order dimensions. A facet captures a narrower slice of the broader construct. |
| **Unidimensional** | An instrument whose items all measure a single underlying construct. GAD-7 is unidimensional (one anxiety factor); FFNI is multidimensional (three higher-order factors, 15 facets). |

## The Encoding

| Term | What it means |
|------|---------------|
| **Factor chain** | The paper's core encoding. Each trait (factor) is expanded into a structured 5-word tuple: *(Factor, Adjective, Synonym, Verb, Noun)*. Example: `(Openness, Artistic, Creative, Create, Creativity)`. |
| **Lexical tuple** | An ordered set of words following a fixed schema. "Lexical" = word-based; "tuple" = a fixed-length ordered sequence (from mathematics/computer science). |
| **6,694 chains / 358 factors** | 44 models contain 358 total factors (traits, scales, subscales). Each factor has multiple chains capturing different word combinations for the same trait. Total: 6,694 chains across all models. |
| **Neural embedding** | Each chain is converted to a 1,536-dimensional numerical vector (via OpenAI text-embedding-3-small). Similar concepts produce similar vectors, putting all 44 models into one shared mathematical space. |
| **Embedding space** | The shared 1,536-dimensional mathematical space where all factor chains live as vectors. Distance between vectors reflects semantic similarity; traits that mean similar things are close together regardless of which model they come from. |
| **L2 normalization** | Scaling each vector to unit length (‖v‖ = 1). This converts dot-product distance to cosine similarity, so all comparisons measure directional alignment rather than magnitude. |

## The Classifiers

| Term | What it means |
|------|---------------|
| **Trained classifiers** | Four classifiers per model (RF, SVC, LR, kNN), 176 total. Given a new sentence describing a personality trait, they predict which factor of that model the sentence belongs to. SVC and kNN are recommended for deployment; RF is retained as a conservative baseline. |
| **Random Forest (RF)** | An ensemble machine learning method that aggregates predictions from many decision trees. Each tree votes on the answer; the majority wins. Robust and interpretable, but the weakest of the four classifiers on novel items. |
| **Support Vector Classifier (SVC)** | A machine learning classifier that finds the optimal hyperplane separating classes with the maximum margin. LinearSVC is used here. Consistently outperforms RF on novel human-authored items and is recommended for deployment alongside kNN. |
| **Logistic Regression (LR)** | A linear probabilistic classifier that models the probability of class membership using a logistic (sigmoid) function. One of four classifiers trained per model; provides calibrated probability estimates. |
| **k-Nearest Neighbors (kNN)** | An instance-based classifier that assigns labels based on the *k* closest training examples (here k=5). Unlike RF and SVC, kNN stores all training data and compares at prediction time ("lazy learning"). Achieves 83.5% mean accuracy on human-authored items; recommended for deployment. |
| **Instance-based learning** | A family of classifiers (like kNN) that do not learn an explicit model during training. Instead, they store the training examples and compare against them at prediction time. Also called "lazy learning" because computation is deferred to prediction. |
| **Oracle ceiling** | The accuracy attainable when each model is retrospectively assigned its single best-performing classifier. Represents the practical upper bound of the current classifier suite (86.8% on human items). |
| **Hyperparameters** | Settings chosen before training that control how a classifier learns (e.g., number of trees in RF, value of *k* in kNN, regularization strength in SVC/LR). Tuned via cross-validation, not learned from the data. |

## The Validation

| Term | What it means |
|------|---------------|
| **Classification accuracy (71.5%)** | When classifiers are tested on held-out items, they correctly identify the right factor 71.5% of the time on average across all 44 models. Chance would be ~6-12% depending on model size. |
| **Cohen's *d* = 1.03** | Standardized effect size comparing baseline vs. improved classifiers across the same 44 models. Conventional thresholds: 0.2 = small, 0.5 = medium, 0.8 = large. **1.03 is a large effect**; the improvements are substantial, not marginal. |
| **Human-authored items (418)** | Real questionnaire items written by psychologists, drawn from 22 published instruments (e.g., IPIP-50, TIPI, BFI-44, BDI, HEXACO-PI-R). Tests whether classifiers generalize to real-world content they have never seen during training. |
| **Training data** | The set of examples (factor chain embeddings) used to fit a classifier. The classifier learns patterns from this data. |
| **Held-out items / test set** | Examples deliberately withheld during training to evaluate how well a classifier performs on data it has never seen. |
| **Generalization** | The ability of a classifier to perform well on new, unseen data, not just the data it was trained on. The human items test this: they come from published instruments the classifiers never encountered. |
| **Cross-validation** | A validation technique that divides data into *k* equal parts, training on *k*-1 parts and testing on 1 part, repeated *k* times. Five-fold CV is used in the atlas so every trait appears in the test set exactly once. |
| **Stratified split** | A train-test division that preserves the proportion of each class in both sets, preventing skewed results when some factors have more chains than others. |
| **Confusion matrix** | A table comparing predicted vs. actual class labels. Rows represent actual factors, columns represent predicted factors. The diagonal shows correct predictions; off-diagonal cells show which factors are confused with each other. |
| **Precision** | Of all items the classifier predicted as factor X, what fraction actually belong to factor X? Precision = TP / (TP + FP). High precision means few false positives. |
| **Recall** | Of all items that actually belong to factor X, what fraction did the classifier find? Recall = TP / (TP + FN). High recall means few missed items. |
| **F1 score** | The harmonic mean of precision and recall, balancing both into a single number. Ranges from 0 to 1; useful when classes are imbalanced. |
| **Reverse-scored items** | Questionnaire items phrased in the opposite direction of the trait they measure (e.g., "I rarely feel anxious" for Neuroticism). These test whether classifiers understand semantic content rather than just surface wording. |
| **100% model-level convergence** | Every testable model had its human items classified above chance. No model completely failed. |
| **Triple-judge panel (95.7%)** | Three independent LLM judges were each shown every factor chain and asked which factor it belongs to. They agreed with ground truth 95.7% of the time (Cohen's kappa = 0.99), establishing a quality ceiling: the encoding itself is sound, and the remaining gap is classifier capacity. |
| **Cohen's kappa** | A statistic measuring inter-rater agreement beyond chance. 0 = chance agreement, 1 = perfect agreement. Kappa = 0.99 means near-perfect agreement among the three judges. |
| **Baselines (random / frequency)** | Random baseline = accuracy if a classifier guesses randomly among all factors; frequency baseline = accuracy if it always predicts the most common factor. All 44 models beat random (+35.7% lift); 41 of 44 beat frequency. |
| **Friedman test** | A non-parametric statistical test for comparing multiple classifiers across multiple datasets. Used here to determine whether the four classifier types (RF, SVC, LR, kNN) differ significantly in accuracy across all 44 models. |

## The Psychometric Properties

| Term | What it means |
|------|---------------|
| **Cronbach's alpha (α)** | A measure of internal consistency (0 to 1): whether items in a scale measure the same underlying construct. α > 0.70 is acceptable, > 0.80 is good. Example: GAD-7 α = 0.92. |
| **Test-retest reliability** | The correlation between scores from the same instrument given to the same people at two time points. High values (r > 0.70) indicate stable measurement over time. |
| **Likert scale** | A rating scale for survey items, typically 5-point (Strongly Disagree to Strongly Agree) or 7-point. GAD-7 uses a 4-point scale (0-3). Named after psychologist Rensis Likert. |
| **Construct validity** | Does the instrument actually measure the theoretical construct it claims to measure? Established through convergent validity, discriminant validity, and factor analysis. |
| **Convergent validity** | The extent to which measures of the same or similar constructs correlate highly with each other. High correlation is expected and confirms that the instruments are measuring the same thing. |
| **Discriminant validity** | The extent to which measures of different constructs show low correlation. Confirms that the instrument is measuring something distinct, not just overlapping with unrelated constructs. |
| **CFA (Confirmatory Factor Analysis)** | A statistical method that tests whether observed data match a hypothesized factor structure. Confirms (or rejects) the theoretical organization of an instrument's subscales. Example: CFA supports FFNI's 15-facet structure. |

## The Discovery

| Term | What it means |
|------|---------------|
| **Semantic signal** | Meaningful pattern in the embedding space. "No semantic signal" means the grouping carries no information about what the traits actually mean; the labels are administrative, not substantive. |
| **Silhouette score (~ 0)** | Measures how well data points match their assigned cluster labels. Ranges from -1 (wrong clusters) to +1 (perfect clusters). Near 0 means the 7 disciplinary categories have essentially no semantic coherence; a Clinical trait is no more similar to other Clinical traits than to Motivational or Trait-Based ones. |
| **Semantic Personality Index (SPI)** | Instead of using the 7 human-assigned categories, k-means clustering (k=15) was applied to all embedding vectors to find natural groupings. These 15 data-driven clusters are the SPI. |
| **k-means clustering** | An algorithm that partitions data into *k* groups by minimizing the distance between each point and its cluster center. Here, k=15 means the algorithm found 15 natural groupings in the embedding space. |
| **Permutation null model** | A statistical baseline created by randomly shuffling category assignments. SPI's 4 clusters spanning all 7 categories falls far below the null expectation of 14.4 single-tradition clusters, proving the cross-tradition structure is genuine, not an artifact. |
| **Diagnostic boundaries** | Clinically established distinctions between conditions. The SPI recovers these automatically: Clinical fragments into Psychopathology, Depression, Reactive Aggression, and Anxiety. Narcissism fragments into Shame, Dark Manipulation, and Grandiose. These map onto recognized diagnostic categories without any clinical labels as input. |
| **Interpersonal Circumplex** | Theory (Leary 1957, Wiggins 1979) that all interpersonal behavior organizes around two orthogonal axes: **Warmth** (communion/affiliation) and **Dominance** (agency/control). The SPI is consistent with this: four clusters (C1, C4, C6, C7) span all 7 traditions, while Warmth (C0) spans six of seven. A theory proposed from within one tradition, now supported across seven. |
| **Jangle fallacy** | Different names masking the same construct (Kelley, 1927). Example: IPN Exploitativeness and PNI Exploitativeness come from different traditions but have cosine similarity 0.959, nearly identical *lexical content* under different names. The SPI provides the first large-scale evidence consistent with jangle across 44 models. Note: embedding proximity demonstrates shared vocabulary, not proven construct equivalence; convergent validity at the score level would be needed to fully confirm jangle. |
| **Jingle fallacy** | Same name masking different constructs (Block, 1995). Does "Extraversion" in OCEAN, HEXACO, and EPM mean the same thing? If they land in the same SPI cluster, that is evidence against jingle for that construct. The SPI makes this testable. |
| **PCA (Principal Component Analysis)** | A statistical method that identifies the directions of maximum variance in high-dimensional data. Used here to measure how much unique information each model contributes to the overall embedding space. |
| **OCEAN ranks third** | PCA shows that Trait-Based models (OCEAN, HEXACO) contribute less marginal information per model than Interpersonal or Cognitive models. Adding another Big Five variant to your AI system gives you less new information than adding one model from a different tradition. |
| **Cosine similarity** | Measures the angle between two vectors. Ranges from -1 (opposite) to +1 (identical direction). Used throughout the paper to quantify how semantically similar two traits or clusters are. |
| **t-SNE / UMAP** | Dimensionality reduction methods that project high-dimensional embeddings (1,536-dim) into 2D for visualization. The SPI cluster plots use these to show how traits group in the embedding space. |
| **HiTOP** | The Hierarchical Taxonomy of Psychopathology (Kotov et al., 2017). A dimensional reorganization of clinical constructs into spectra, explicitly addressing overlap among DSM categories. The SPI provides methodological triangulation: HiTOP uses symptom co-occurrence; the SPI uses semantic content. Different methods, compatible structure. |
| **Mantel test** | A statistical test for correlation between two distance (or similarity) matrices. Used here to test whether embedding-space distances correlate with theoretically expected trait relationships across models. |

## The Infrastructure

| Term | What it means |
|------|---------------|
| **FAISS (Facebook AI Similarity Search)** | An open-source library from Meta AI Research for fast similarity search over dense vectors ([Douze et al., 2024](https://arxiv.org/abs/2401.08281); [Johnson et al., 2021](https://doi.org/10.1109/TBDATA.2019.2921572)). In the atlas, a FAISS flat inner-product index over 6,694 L2-normalized embeddings enables cross-model personality trait search in under 1 millisecond. The full index is 40 MB and runs on commodity hardware with no GPU required. |
| **Inner-product index (IndexFlatIP)** | The specific FAISS index type used in the atlas. It computes similarity as the dot product of unit-normalized vectors, which is equivalent to cosine similarity after L2 normalization. "Flat" means exact (brute-force) search with no approximation. |
| **AGPL-3.0** | GNU Affero General Public License, version 3. The license for this repository's source code. Requires any modifications and networked deployments to share source code. Non-code assets (datasets, embeddings, model cards) use CC BY-NC-SA 4.0. |
| **CC BY-NC-SA 4.0** | Creative Commons Attribution-NonCommercial-ShareAlike 4.0. The license for datasets, embeddings, and model cards. Allows sharing and adaptation for non-commercial purposes with attribution, under the same license terms. |
