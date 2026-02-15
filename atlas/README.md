# Computational Atlas of Personality Models

**44 models** across **7 categories**, each with:
- **MODEL_CARD.md** — Verified model card (converted from peer-reviewed supplementary appendix)
- **Jupyter Notebook** — Starter notebook for dataset exploration, embedding generation, and RF classification
- **Model diagram** — Visual overview of the model's factor structure

## Quick Start

```python
# Pick any model folder, open the notebook, and run it.
# Each notebook loads the model's dataset from the survey repo,
# generates embeddings, trains an RF classifier, and evaluates.
```

## Survey Repository

All datasets, embeddings, trained models, and label encoders are hosted at:
**[github.com/Wildertrek/survey](https://github.com/Wildertrek/survey)**

| Asset | Count | Format |
|-------|-------|--------|
| Datasets | 44 | CSV |
| Embeddings | 44 | CSV (1536-dim) |
| RF Models | 44 | pickle (avg 717 KB) |
| Label Encoders | 44 | pickle (avg 671 bytes) |
| Total Size | — | 31 MB |

## Models by Category


### Trait-Based Models

| # | Model | Full Name | Notebook |
|---|-------|-----------|----------|
| 1 | [OCEAN](01_trait_based/ocean/MODEL_CARD.md) | OCEAN (Big Five Factor Model) | Yes |
| 2 | [MBTI](01_trait_based/mbti/MODEL_CARD.md) | Myers-Briggs Type Indicator | Yes |
| 3 | [HEXACO](01_trait_based/hexaco/MODEL_CARD.md) | HEXACO Personality Model | Yes |
| 4 | [EPM](01_trait_based/epm/MODEL_CARD.md) | Eysenck Personality Model (PEN) | Yes |
| 5 | [16PF](01_trait_based/16pf/MODEL_CARD.md) | Sixteen Personality Factors | Yes |
| 6 | [FT](01_trait_based/ftm/MODEL_CARD.md) | Four Temperaments | Yes |


### Narcissism-Based Models

| # | Model | Full Name | Notebook |
|---|-------|-----------|----------|
| 7 | [NPI](02_narcissism_based/npi/MODEL_CARD.md) | Narcissistic Personality Inventory | Yes |
| 8 | [PNI](02_narcissism_based/pni/MODEL_CARD.md) | Pathological Narcissism Inventory | Yes |
| 9 | [FFNI](02_narcissism_based/ffni/MODEL_CARD.md) | Five-Factor Narcissism Inventory | Yes |
| 10 | [FFNI-SF](02_narcissism_based/ffni_sf/MODEL_CARD.md) | Five-Factor Narcissism Inventory (Short) | Yes |
| 11 | [NARQ](02_narcissism_based/narq/MODEL_CARD.md) | Narcissistic Admiration and Rivalry Questionnaire | Yes |
| 12 | [HSNS](02_narcissism_based/hsns/MODEL_CARD.md) | Hypersensitive Narcissism Scale | Yes |
| 13 | [DT3](02_narcissism_based/dtm/MODEL_CARD.md) | Dark Triad Scales | Yes |
| 14 | [DT4](02_narcissism_based/dt4/MODEL_CARD.md) | Dark Tetrad Scales | Yes |
| 15 | [MCMI-Narc](02_narcissism_based/mcmin/MODEL_CARD.md) | MCMI-IV Narcissistic Scales | Yes |
| 16 | [IPN](02_narcissism_based/ipn/MODEL_CARD.md) | Inventory of Pathological Narcissism | Yes |


### Motivational and Value Models

| # | Model | Full Name | Notebook |
|---|-------|-----------|----------|
| 17 | [STBV](03_motivational_value/stbv/MODEL_CARD.md) | Schwartz Theory of Basic Values | Yes |
| 18 | [MST](03_motivational_value/mst/MODEL_CARD.md) | Motivational Systems Theory | Yes |
| 19 | [RFT](03_motivational_value/rft/MODEL_CARD.md) | Regulatory Focus Theory | Yes |
| 20 | [SDT](03_motivational_value/sdt/MODEL_CARD.md) | Self-Determination Theory | Yes |
| 21 | [AAM](03_motivational_value/aam/MODEL_CARD.md) | Approach/Avoidance Motivation | Yes |
| 22 | [CS](03_motivational_value/clifton/MODEL_CARD.md) | Clifton Strengths | Yes |


### Cognitive and Learning Models

| # | Model | Full Name | Notebook |
|---|-------|-----------|----------|
| 23 | [PCT](04_cognitive_learning/pct/MODEL_CARD.md) | Personal Construct Theory | Yes |
| 24 | [SCM](04_cognitive_learning/scm/MODEL_CARD.md) | Social-Cognitive Model | Yes |
| 25 | [CEST](04_cognitive_learning/cest/MODEL_CARD.md) | Cognitive-Experiential Self-Theory | Yes |
| 26 | [FSLS](04_cognitive_learning/fsls/MODEL_CARD.md) | Felder-Silverman Learning Styles | Yes |


### Clinical and Psychological Health Models

| # | Model | Full Name | Notebook |
|---|-------|-----------|----------|
| 27 | [MMPI](05_clinical_health/mmpi/MODEL_CARD.md) | Minnesota Multiphasic Personality Inventory | Yes |
| 28 | [TCI](05_clinical_health/tci/MODEL_CARD.md) | Temperament and Character Inventory | Yes |
| 29 | [TMP](05_clinical_health/tmp/MODEL_CARD.md) | Triarchic Model of Psychopathy | Yes |
| 30 | [BDI](05_clinical_health/bdi/MODEL_CARD.md) | Beck Depression Inventory | Yes |
| 31 | [GAD7](05_clinical_health/gad7/MODEL_CARD.md) | Generalized Anxiety Disorder 7 | Yes |
| 32 | [SCID](05_clinical_health/scid/MODEL_CARD.md) | Structured Clinical Interview for DSM | Yes |
| 33 | [MCMI](05_clinical_health/mcmi/MODEL_CARD.md) | Millon Clinical Multiaxial Inventory | Yes |
| 34 | [RIT](05_clinical_health/rit/MODEL_CARD.md) | Rorschach Inkblot Test | Yes |
| 35 | [TAT](05_clinical_health/tat/MODEL_CARD.md) | Thematic Apperception Test | Yes |


### Interpersonal and Conflict Resolution Models

| # | Model | Full Name | Notebook |
|---|-------|-----------|----------|
| 36 | [TKI](06_interpersonal_conflict/tki/MODEL_CARD.md) | Thomas-Kilmann Conflict Mode Instrument | Yes |
| 37 | [DiSC](06_interpersonal_conflict/disc/MODEL_CARD.md) | DiSC Workplace Profile | Yes |


### Application-Specific and Holistic Models

| # | Model | Full Name | Notebook |
|---|-------|-----------|----------|
| 38 | [WAIS](07_application_holistic/wais/MODEL_CARD.md) | Wechsler Adult Intelligence Scale | Yes |
| 39 | [RIASEC](07_application_holistic/riasec/MODEL_CARD.md) | Holland's Theory of Career Choice | Yes |
| 40 | [BT](07_application_holistic/bt/MODEL_CARD.md) | Bartle Types | Yes |
| 41 | [TEI](07_application_holistic/tei/MODEL_CARD.md) | Theories of Emotional Intelligence | Yes |
| 42 | [EM](07_application_holistic/em/MODEL_CARD.md) | Enneagram Model | Yes |
| 43 | [PAPC](07_application_holistic/papc/MODEL_CARD.md) | Parametric Analysis of Person Characteristics | Yes |
| 44 | [CMOA](07_application_holistic/cmoa/MODEL_CARD.md) | Circumplex Model of Affect | Yes |


## References

All references cited across the 44 model cards are collected in [`references.bib`](references.bib).

---

*Generated from supplementary appendix model_catalog.tex (verified by authors)*
*Source: TIST-2025-12-1243 "A Survey and Computational Atlas of Personality Models"*
