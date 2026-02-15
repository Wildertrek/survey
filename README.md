# A Survey and Computational Atlas of Personality Models

**44 personality models** — standardized datasets, 1536-dim embeddings, trained RF classifiers, and verified model cards — ready to use in five minutes.

> Raetano, J., Gregor, J., & Tamang, S. (2026). *A Survey and Computational Atlas of Personality Models.* ACM Transactions on Intelligent Systems and Technology (TIST). Under review.

---

## Quick Start

Each of the 44 models has a Jupyter notebook you can open and run immediately.

```
atlas/01_trait_based/ocean/          ← open OCEAN-Updated.ipynb
atlas/02_narcissism_based/dtm/       ← open DTM.ipynb
atlas/05_clinical_health/mmpi/       ← open MMPI.ipynb
...any of 44 folders
```

**In 10 lines:**

```python
import pandas as pd
import joblib

# 1. Load any model's dataset and trained classifier
df = pd.read_csv("datasets/ocean.csv")
model = joblib.load("models/ocean_rf_model.pkl")
encoder = joblib.load("models/ocean_label_encoder.pkl")

# 2. Load pre-computed embeddings (1536-dim, text-embedding-3-small)
embeddings = pd.read_csv("Embeddings/ocean_embeddings.csv")
X = embeddings.iloc[:, 1:].values  # drop index column

# 3. Predict personality factors
predictions = model.predict(X)
labels = encoder.inverse_transform(predictions)
print(f"Predicted factors: {set(labels)}")
```

**Or run the standalone demo:**

```bash
pip install -r requirements.txt
python demo.py              # OCEAN by default
python demo.py --model rft  # any of 44 model slugs
```

**Dependencies:** `pandas`, `scikit-learn`, `joblib` (included with scikit-learn). For notebooks: add `matplotlib`, `openai`.

---

## What's in the Atlas

| Asset | Count | Format | Size |
|-------|-------|--------|------|
| [Lexical datasets](datasets/) | 44 | CSV (Factor, Adjective, Synonym, Verb, Noun) | 532 KB |
| [Embeddings](Embeddings/) | 44 | CSV (1536-dim, OpenAI text-embedding-3-small) | 246 MB |
| [RF classifiers](models/) | 44 | scikit-learn pickle | 31 MB (avg 717 KB) |
| [Label encoders](models/) | 44 | scikit-learn pickle | 29 KB (avg 671 bytes) |
| [Model graphs](graphs/) | 44 | PNG (high-res factor diagrams) | 164 MB |
| [Model cards](atlas/) | 44 | Markdown (verified from peer-reviewed appendix) | — |
| [Starter notebooks](atlas/) | 44 | Jupyter (.ipynb) | — |
| **Total trait rows** | **6,694** | across all 44 models | |

---

## Repository Structure

```
survey/
├── README.md
├── LICENSE                         (MIT)
├── CITATION.cff                    (CFF citation metadata)
├── requirements.txt                (pip dependencies)
├── demo.py                         (10-line standalone demo)
│
├── atlas/                          ★ Start here — 44 model cards + notebooks
│   ├── README.md                   (master index, all 44 models)
│   ├── references.bib              (328 citations across all cards)
│   │
│   ├── 01_trait_based/             (6 models)
│   │   ├── ocean/                  OCEAN (Big Five)
│   │   ├── mbti/                   Myers-Briggs Type Indicator
│   │   ├── hexaco/                 HEXACO Personality Model
│   │   ├── epm/                    Eysenck Personality Model
│   │   ├── 16pf/                   Sixteen Personality Factors
│   │   └── ftm/                    Four Temperaments
│   │
│   ├── 02_narcissism_based/        (10 models)
│   │   ├── npi/                    Narcissistic Personality Inventory
│   │   ├── pni/                    Pathological Narcissism Inventory
│   │   ├── ffni/                   Five-Factor Narcissism Inventory
│   │   ├── ffni_sf/                FFNI Short Form
│   │   ├── narq/                   Narcissistic Admiration & Rivalry
│   │   ├── hsns/                   Hypersensitive Narcissism Scale
│   │   ├── dtm/                    Dark Triad
│   │   ├── dt4/                    Dark Tetrad
│   │   ├── mcmin/                  MCMI-IV Narcissistic Scales
│   │   └── ipn/                    Inventory of Pathological Narcissism
│   │
│   ├── 03_motivational_value/      (6 models)
│   │   ├── stbv/                   Schwartz Theory of Basic Values
│   │   ├── mst/                    Motivational Systems Theory
│   │   ├── rft/                    Regulatory Focus Theory
│   │   ├── sdt/                    Self-Determination Theory
│   │   ├── aam/                    Approach/Avoidance Motivation
│   │   └── clifton/                Clifton Strengths
│   │
│   ├── 04_cognitive_learning/      (4 models)
│   │   ├── pct/                    Personal Construct Theory
│   │   ├── scm/                    Social-Cognitive Model
│   │   ├── cest/                   Cognitive-Experiential Self-Theory
│   │   └── fsls/                   Felder-Silverman Learning Styles
│   │
│   ├── 05_clinical_health/         (9 models)
│   │   ├── mmpi/                   Minnesota Multiphasic Personality Inventory
│   │   ├── tci/                    Temperament and Character Inventory
│   │   ├── tmp/                    Triarchic Model of Psychopathy
│   │   ├── bdi/                    Beck Depression Inventory
│   │   ├── gad7/                   Generalized Anxiety Disorder 7
│   │   ├── scid/                   Structured Clinical Interview for DSM
│   │   ├── mcmi/                   Millon Clinical Multiaxial Inventory
│   │   ├── rit/                    Rorschach Inkblot Test
│   │   └── tat/                    Thematic Apperception Test
│   │
│   ├── 06_interpersonal_conflict/  (2 models)
│   │   ├── tki/                    Thomas-Kilmann Conflict Mode Instrument
│   │   └── disc/                   DiSC Workplace Profile
│   │
│   └── 07_application_holistic/    (7 models)
│       ├── wais/                   Wechsler Adult Intelligence Scale
│       ├── riasec/                 Holland's Theory of Career Choice
│       ├── bt/                     Bartle Types
│       ├── tei/                    Theories of Emotional Intelligence
│       ├── em/                     Enneagram Model
│       ├── papc/                   Parametric Analysis of Person Characteristics
│       └── cmoa/                   Circumplex Model of Affect
│
│   Each model folder contains:
│   ├── MODEL_CARD.md               (verified model card)
│   ├── <MODEL>.ipynb               (starter notebook)
│   └── <model>_small.png           (factor diagram thumbnail)
│
├── datasets/                       44 CSV files (lexical schemas)
├── Embeddings/                     44 embedding CSVs (1536-dim)
├── models/                         44 RF classifiers + 44 label encoders
├── graphs/                         44 high-res model diagrams
│
├── notebooks/                      Cross-model analysis scripts
│   └── 01_cross_model_pca_analysis.py
│
├── results/                        PCA analysis outputs
│   ├── README.md                   (methodology + full results)
│   ├── pca_summary_report.json
│   ├── pca_scree_plot.png
│   ├── pca_2d_all_models.png
│   ├── pca_model_centroids_2d.png
│   ├── pca_factor_loadings_heatmap.png
│   ├── pca_variance_explained.csv
│   ├── pca_top_factors_by_variance.csv
│   └── pca_model_overlap_matrix.csv
│
└── Supplementary_Appendices_for_A_Survey_and_Computational_Atlas_of_Personality_Models.pdf
```

---

## The 44 Models

### I. Trait-Based Models (6)

| # | Model | Full Name | Traits | Rows |
|---|-------|-----------|--------|------|
| 1 | [OCEAN](atlas/01_trait_based/ocean/MODEL_CARD.md) | Big Five Factor Model | O, C, E, A, N | 120 |
| 2 | [MBTI](atlas/01_trait_based/mbti/MODEL_CARD.md) | Myers-Briggs Type Indicator | EI, SN, TF, JP | 144 |
| 3 | [HEXACO](atlas/01_trait_based/hexaco/MODEL_CARD.md) | HEXACO Personality Model | H, E, X, A, C, O | 66 |
| 4 | [EPM](atlas/01_trait_based/epm/MODEL_CARD.md) | Eysenck Personality Model | P, E, N | 90 |
| 5 | [16PF](atlas/01_trait_based/16pf/MODEL_CARD.md) | Sixteen Personality Factors | 16 primary factors | 192 |
| 6 | [FT](atlas/01_trait_based/ftm/MODEL_CARD.md) | Four Temperaments | Sanguine, Choleric, Melancholic, Phlegmatic | 80 |

### II. Narcissism-Based Models (10)

| # | Model | Full Name | Rows |
|---|-------|-----------|------|
| 7 | [NPI](atlas/02_narcissism_based/npi/MODEL_CARD.md) | Narcissistic Personality Inventory | 168 |
| 8 | [PNI](atlas/02_narcissism_based/pni/MODEL_CARD.md) | Pathological Narcissism Inventory | 168 |
| 9 | [FFNI](atlas/02_narcissism_based/ffni/MODEL_CARD.md) | Five-Factor Narcissism Inventory | 360 |
| 10 | [FFNI-SF](atlas/02_narcissism_based/ffni_sf/MODEL_CARD.md) | FFNI Short Form | 60 |
| 11 | [NARQ](atlas/02_narcissism_based/narq/MODEL_CARD.md) | Narcissistic Admiration & Rivalry | 48 |
| 12 | [HSNS](atlas/02_narcissism_based/hsns/MODEL_CARD.md) | Hypersensitive Narcissism Scale | 48 |
| 13 | [DT3](atlas/02_narcissism_based/dtm/MODEL_CARD.md) | Dark Triad | 54 |
| 14 | [DT4](atlas/02_narcissism_based/dt4/MODEL_CARD.md) | Dark Tetrad | 96 |
| 15 | [MCMI-Narc](atlas/02_narcissism_based/mcmin/MODEL_CARD.md) | MCMI-IV Narcissistic Scales | 72 |
| 16 | [IPN](atlas/02_narcissism_based/ipn/MODEL_CARD.md) | Inventory of Pathological Narcissism | 80 |

### III. Motivational and Value Models (6)

| # | Model | Full Name | Rows |
|---|-------|-----------|------|
| 17 | [STBV](atlas/03_motivational_value/stbv/MODEL_CARD.md) | Schwartz Theory of Basic Values | 128 |
| 18 | [MST](atlas/03_motivational_value/mst/MODEL_CARD.md) | Motivational Systems Theory | 64 |
| 19 | [RFT](atlas/03_motivational_value/rft/MODEL_CARD.md) | Regulatory Focus Theory | 56 |
| 20 | [SDT](atlas/03_motivational_value/sdt/MODEL_CARD.md) | Self-Determination Theory | 84 |
| 21 | [AAM](atlas/03_motivational_value/aam/MODEL_CARD.md) | Approach/Avoidance Motivation | 40 |
| 22 | [CS](atlas/03_motivational_value/clifton/MODEL_CARD.md) | Clifton Strengths | 136 |

### IV. Cognitive and Learning Models (4)

| # | Model | Full Name | Rows |
|---|-------|-----------|------|
| 23 | [PCT](atlas/04_cognitive_learning/pct/MODEL_CARD.md) | Personal Construct Theory | 899 |
| 24 | [SCM](atlas/04_cognitive_learning/scm/MODEL_CARD.md) | Social-Cognitive Model | 180 |
| 25 | [CEST](atlas/04_cognitive_learning/cest/MODEL_CARD.md) | Cognitive-Experiential Self-Theory | 72 |
| 26 | [FSLS](atlas/04_cognitive_learning/fsls/MODEL_CARD.md) | Felder-Silverman Learning Styles | 360 |

### V. Clinical and Psychological Health Models (9)

| # | Model | Full Name | Rows |
|---|-------|-----------|------|
| 27 | [MMPI](atlas/05_clinical_health/mmpi/MODEL_CARD.md) | Minnesota Multiphasic Personality Inventory | 360 |
| 28 | [TCI](atlas/05_clinical_health/tci/MODEL_CARD.md) | Temperament and Character Inventory | 252 |
| 29 | [TMP](atlas/05_clinical_health/tmp/MODEL_CARD.md) | Triarchic Model of Psychopathy | 108 |
| 30 | [BDI](atlas/05_clinical_health/bdi/MODEL_CARD.md) | Beck Depression Inventory | 756 |
| 31 | [GAD-7](atlas/05_clinical_health/gad7/MODEL_CARD.md) | Generalized Anxiety Disorder 7 | 252 |
| 32 | [SCID](atlas/05_clinical_health/scid/MODEL_CARD.md) | Structured Clinical Interview for DSM | 401 |
| 33 | [MCMI](atlas/05_clinical_health/mcmi/MODEL_CARD.md) | Millon Clinical Multiaxial Inventory | 84 |
| 34 | [RIT](atlas/05_clinical_health/rit/MODEL_CARD.md) | Rorschach Inkblot Test | 45 |
| 35 | [TAT](atlas/05_clinical_health/tat/MODEL_CARD.md) | Thematic Apperception Test | 39 |

### VI. Interpersonal and Conflict Resolution Models (2)

| # | Model | Full Name | Rows |
|---|-------|-----------|------|
| 36 | [TKI](atlas/06_interpersonal_conflict/tki/MODEL_CARD.md) | Thomas-Kilmann Conflict Mode Instrument | 20 |
| 37 | [DiSC](atlas/06_interpersonal_conflict/disc/MODEL_CARD.md) | DiSC Workplace Profile | 31 |

### VII. Application-Specific and Holistic Models (7)

| # | Model | Full Name | Rows |
|---|-------|-----------|------|
| 38 | [WAIS](atlas/07_application_holistic/wais/MODEL_CARD.md) | Wechsler Adult Intelligence Scale | 60 |
| 39 | [RIASEC](atlas/07_application_holistic/riasec/MODEL_CARD.md) | Holland's Theory of Career Choice | 120 |
| 40 | [BT](atlas/07_application_holistic/bt/MODEL_CARD.md) | Bartle Types | 64 |
| 41 | [TEI](atlas/07_application_holistic/tei/MODEL_CARD.md) | Theories of Emotional Intelligence | 48 |
| 42 | [EM](atlas/07_application_holistic/em/MODEL_CARD.md) | Enneagram Model | 81 |
| 43 | [PAPC](atlas/07_application_holistic/papc/MODEL_CARD.md) | Parametric Analysis of Person Characteristics | 72 |
| 44 | [CMOA](atlas/07_application_holistic/cmoa/MODEL_CARD.md) | Circumplex Model of Affect | 36 |

---

## Cross-Model PCA Analysis

Principal Component Analysis across all 44 models (6,694 trait rows, 1536-dim embeddings):

| Metric | Value |
|--------|-------|
| PC1 variance explained | 4.5% |
| Top-5 components | 15.5% cumulative |
| Top-10 components | 25.2% cumulative |
| Most similar pair | IPN / PNI (cosine = 0.959) |
| Least similar pair | TKI / WAIS (cosine = 0.268) |
| Highest-variance category | Narcissism (352.5) |

See [`results/README.md`](results/README.md) for full PCA outputs: scree plot, 2D projections, factor loadings heatmap, model overlap matrix, similarity rankings, and summary report.

**Reproduce:**
```bash
python notebooks/01_cross_model_pca_analysis.py
```

---

## Computational Benchmarks

All 44 classifiers are Random Forest models trained on 1536-dim OpenAI `text-embedding-3-small` embeddings.

| Measurement | Value |
|-------------|-------|
| Total atlas size (44 RF models) | 31 MB |
| Average model size | 717 KB |
| Smallest model (OCEAN) | 195 KB |
| Total label encoders | 29 KB |
| Batch inference (50 chars × 1 model) | 5.3 ms |
| Full atlas inference (50 chars × 44 models) | 233 ms |
| Embedding generation (all 44 models) | $0.27 |
| ONNX export | Supported |
| Platform | Apple M1 CPU (no GPU required) |

The entire atlas runs on commodity hardware. Individual models are small enough for browser deployment via [ONNX.js](https://onnxruntime.ai/docs/tutorials/web/) or mobile via Core ML / TFLite.

---

## Lexical Schema

Every dataset follows a standardized five-column lexical schema:

| Column | Description | Example (OCEAN) |
|--------|-------------|-----------------|
| `Factor` | Personality dimension | Extraversion |
| `Adjective` | Trait descriptor | Active |
| `Synonym` | Near-equivalent | Energetic |
| `Verb` | Behavioral form | Activate |
| `Noun` | Nominal quality | Activeness |

This schema enables consistent embedding generation, cross-model comparison, and integration into LLM-based personality inference pipelines.

### Schema Variations

38 of 44 models use the standard five-column schema above. Six models extend the schema with additional hierarchy or domain columns:

| Model | Columns | Notes |
|-------|---------|-------|
| WAIS | `Factor, Adjective, Description, Synonym, Verb, Noun, Embedding` | Extra `Description` column |
| DISC | `Domain, Subcategory, Factor, Adjective, Synonym, Verb, Noun` | Two hierarchy columns prepended |
| EM | `Type, Name, Factor, Adjective, Synonym, Verb, Noun, Adjacencies` | Enneagram type/name + adjacency list |
| TAT | `Category, Factor, Adjective, Synonym, Verb, Noun` | One hierarchy column prepended |
| TEI | `Domain, Factor, Adjective, Synonym, Verb, Noun` | One hierarchy column prepended |
| TKI | `Category, Factor, Adjective, Synonym, Verb, Noun` | One hierarchy column prepended |

All models share the core `Synonym, Verb, Noun` columns used for embedding generation. The five-column schema is the minimum; extensions provide additional categorical or relational structure.

---

## Model Cards

Each model has a verified [MODEL_CARD.md](atlas/) containing:

- **Description** — theoretical basis and origin
- **Dimensions** — factors, facets, and AI maturity mappings (L1–L3)
- **Applications** — use cases in psychology, AI, and human–AI interaction
- **Timeline** — historical milestones
- **Psychometrics** — reliability, validity, instruments
- **Data Structure** — schema fields and example entries
- **Resources** — links to dataset, embeddings, classifier, and graph in this repo

All cards were converted from the peer-reviewed supplementary appendix and verified by the authors.

---

## Starter Notebooks

Each model folder in [`atlas/`](atlas/) includes a Jupyter notebook that demonstrates:

1. Loading the model's lexical dataset
2. Generating or loading embeddings
3. Training a Random Forest classifier
4. Evaluating classification accuracy
5. Visualizing embedding clusters (PCA)

These notebooks were developed in the [Personality-Trait-Models](https://github.com/Wildertrek/Personality-Trait-Models) research repository and represent the exact workflow used to produce the atlas artifacts.

---

## Supplementary Material

The full supplementary appendix (44 model card catalog, mapping tables, notation standards, psychometric definitions, PRISM protocol specification) is available as:

- **PDF:** [`Supplementary_Appendices_for_A_Survey_and_Computational_Atlas_of_Personality_Models.pdf`](Supplementary_Appendices_for_A_Survey_and_Computational_Atlas_of_Personality_Models.pdf)
- **Navigable model cards:** [`atlas/`](atlas/) (recommended — each card links directly to its data)

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).

---

## Citation

```bibtex
@article{Raetano2026Atlas,
  title   = {A Survey and Computational Atlas of Personality Models},
  author  = {Raetano, Joseph and Gregor, Jens and Tamang, Suzanne},
  journal = {ACM Transactions on Intelligent Systems and Technology},
  year    = {2026},
  note    = {Under review (TIST-2025-12-1243)}
}
```

See also [`CITATION.cff`](CITATION.cff).
