# Model Card Template

Use this template when adding a new personality model to the atlas.

---

# (N) Model Name

**Abbreviation:** ABBR
**Category:** One of: Trait-Based, Narcissism-Based, Motivational, Cognitive, Clinical/Health, Interpersonal, Applied/Holistic
**Model Number:** N of 44

[![Model Diagram](model_small.png)](../../../graphs/model_large.png)

---

### Description.
One paragraph describing the model's theoretical foundation, primary constructs, and historical context. Include seminal citations in [Author Year] format.

### Dimensions, Examples, and Brain-Function Mapping.
> AI maturity mappings (L1-L3) follow the foundation-agent cognitive hierarchy of Liu et al. (2025).

For each factor/dimension:
  - **Factor Name:** Brief definition.
  Example: Behavioral illustration.
  Maps to *cognitive function* (LN AI Maturity), AI application description.

### Applications.
Bulleted list of 3-5 application domains with brief descriptions and citations.

### Timeline.
Chronological milestones (year, event, citation) from the model's origin to present.

### Psychometrics.

| Property | Value |
|----------|-------|
| Number of factors | N |
| Items per standard instrument | N |
| Internal consistency (Cronbach's alpha) | Range |
| Test-retest reliability | Range (interval) |
| Normative sample size | N |
| Available instruments | List |

### Atlas Encoding.

| Property | Value |
|----------|-------|
| Dataset file | `datasets/model_name.csv` |
| Embedding file | `Embeddings/model_name_embeddings.csv` |
| Classifier files | `models/model_name_{rf,svc,lr,knn}_model.pkl` |
| Label encoder | `models/model_name_label_encoder.pkl` |
| Factor chains | N rows |
| Embedding dimensions | 1,536 (text-embedding-3-small) |

### Classifier Performance.

| Classifier | Cross-Val | Novel Items | Psychometric Items |
|------------|-----------|-------------|-------------|
| RF         | --% | --% | --% |
| SVC        | --% | --% | --% |
| LR         | --% | --% | --% |
| kNN        | --% | --% | --% |

### Reliability Tier.
One of: Reliable (>70%), Usable (50-70%), Research-Only (<50%). Based on best-per-model novel item accuracy.

### References.
Numbered list of key references in standard academic format.
