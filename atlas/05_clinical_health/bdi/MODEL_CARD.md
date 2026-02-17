# (30) Beck Depression Inventory

**Abbreviation:** BDI
**Category:** Clinical and Psychological Health Models
**Model Number:** 30 of 44

[![BDI Model Diagram](bdi_small.png)](../../../graphs/bdi_large.png)

---

### Description.
The **Beck Depression Inventory (BDI)** is a 21-item self-report instrument developed by Aaron T. Beck to measure the intensity of depressive symptoms [Beck1961AnInventory].
Each item describes a specific symptom, rated on a four-point scale (0–3), producing total scores from 0–63 that indicate severity categories (minimal, mild, moderate, or severe).
The *BDI-II* [BeckSteerBrown1996BDIIManual], published in 1996, updates the original to align with DSM–IV diagnostic criteria and is validated for ages 13 and above.
The BDI assesses affective, cognitive, somatic, and motivational aspects of depression and remains one of the most frequently used clinical measures worldwide.

### Dimensions, Examples, and AI Mapping.
> AI maturity mappings (L1–L3) follow the foundation-agent cognitive hierarchy of Liu et al. (2025).

Representative BDI-II items and their functional mappings include:

  - **Sadness (Affective):** Feeling persistently down or tearful.
  Example: “I feel sad most of the time.”
  Maps to *Negative Affect Regulation & Mood Simulation* (L3).
  - **Pessimism (Cognitive):** Hopeless outlook toward the future.
  Example: “I believe things will only get worse.”
  Maps to *Negative Predictive Bias / Future Expectancy Modeling* (L3).
  - **Loss of Pleasure (Anhedonia):** Diminished ability to experience enjoyment.
  Example: “I no longer enjoy activities I used to like.”
  Maps to *Reward Circuit Attenuation / Goal Deactivation* (L3).
  - **Self-Criticalness (Cognitive):** Excessive self-blame or guilt.
  Example: “I blame myself for everything bad that happens.”
  Maps to *Self-Referential Negative Attribution Modeling* (L3).
  - **Loss of Energy (Somatic):** Persistent fatigue and decreased drive.
  Example: “I feel too tired to do most things.”
  Maps to *Arousal Regulation & Motivation Deficit Simulation* (L3).
  - **Difficulty Concentrating (Cognitive):** Impaired attention or working memory.
  Example: “I find it hard to focus or think clearly.”
  Maps to *Cognitive Load Dysregulation / Sustained Attention Impairment* (L2–L3).

*Additional BDI-II items include:* past failure, guilt, punishment feelings, self-dislike, suicidal thoughts, crying, agitation, loss of interest, indecisiveness, worthlessness, sleep and appetite changes, irritability, fatigue, and loss of interest in sex.

### Applications.

  - **Clinical Assessment:** Screening and severity measurement for depressive symptoms [BeckSteerBrown1996BDIIManual].
  - **Treatment Monitoring:** Evaluating response to psychotherapy or pharmacological interventions [Schneibel2012Sensitivity].
  - **Psychological Research:** Studying depression correlates, risk factors, and outcomes across populations.
  - **AI for Mental Health:** Training models for early detection of depression via text, voice, or behavioral data.
  - **Personalized AI Companions:** Modulating conversational tone or empathy level based on detected mood indicators (within ethical constraints).
  - **Computational Psychiatry:** Simulating depressive cognition and affect for mechanistic modeling of mood disorders.

### Timeline.

  - **1961:** Original BDI introduced [Beck1961AnInventory].
  - **1978:** BDI-IA revision with updated items.
  - **1988:** Major psychometric review published [BeckSteerCarbin1988Psychometric].
  - **1996:** BDI-II aligns with DSM–IV criteria [BeckSteerBrown1996BDIIManual].
  - **Ongoing:** Cross-cultural validations and clinical refinements continue.

### Psychometrics.

  - **Format:** 21 items, each scored 0–3; total 0–63.
  - **Reliability:** Cronbach’s  = 0.80–0.93; stable test–retest reliability [BeckSteerCarbin1988Psychometric].
  - **Validity:** Strong correlations with clinician ratings and convergent depression scales (e.g., HRSD) [Brown1995Assessing].
  - **Method:** Standardized self-report; widely normed across populations.

### Data Structure.
The `bdi.csv` dataset encodes lexical descriptors for each BDI symptom item:

  - `Factor` – BDI symptom item (e.g., `Sadness`, `Pessimism`).
  - `Adjective` – Key descriptor (e.g., `Despondent`).
  - `Synonym` – Equivalent adjective (e.g., `Down`).
  - `Verb` – Action/state form (e.g., `Suffer`).
  - `Noun` – Nominal form (e.g., `Despondency`).

### Resources.

  - **Connected Papers:** [Beck et al. (1961)](https://www.connectedpapers.com/main/33b2110fa59d8e52a848a5ebead9a088fb255f4e/Beck-Depression-Inventory%E2%80%93II/graph).
  - **Dataset:** [`BDI_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/bdi.csv).
  - **Embeddings:** [`bdi_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/bdi_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/bdi.csv`](../../../datasets/bdi.csv) |
| Embeddings | [`Embeddings/bdi_embeddings.csv`](../../../Embeddings/bdi_embeddings.csv) |
| RF Model | [`models/bdi_rf_model.pkl`](../../../models/bdi_rf_model.pkl) |
| Label Encoder | [`models/bdi_label_encoder.pkl`](../../../models/bdi_label_encoder.pkl) |
| Graph (large) | [`graphs/bdi_large.png`](../../../graphs/bdi_large.png) |


---

## Validation Results

> From: Raetano, Gregor, & Tamang (2026). "A Survey and Computational Atlas of Personality Models." Under review, ACM TIST.

**Performance Tier:** Moderate (50-70%)

### Classification Performance

| Metric | Value |
|--------|-------|
| Factors | 21 |
| Test Items | 297 |
| RF Accuracy | 59.9% |
| F1 Score (macro) | 0.5903 |
| Precision | 0.6722 |
| Recall | 0.5998 |

### Baseline Comparisons

| Baseline | Accuracy | Lift |
|----------|----------|------|
| Random | 4.8% | +55.2% |
| Frequency | 4.8% | +55.2% |

### LLM Judge Evaluation

Triple-judge panel: GPT-5.2, Gemini 3 Pro, Claude Opus 4.6.

| Metric | Value |
|--------|-------|
| RF-Judge Agreement | 20.0% |
| Expected-Factor Agreement | 100.0% |
| Item Validity Rate | 20.0% |
| Mean Confidence | 5.00 / 5.0 |
| Inter-Judge Agreement | 100.0% |

### Category Context

| Metric | Value |
|--------|-------|
| Category | Clinical |
| Category Mean Accuracy | 46.1% |
| Category Best | gad7 (67.7%) |
| Models in Category | 10 |

## References

The following references are cited in this model card:

- [Beck, A. T. et al. (1961). *An inventory for measuring depression*](https://doi.org/10.1001/archpsyc.1961.01710120031004)
- [Beck, A. T. et al. (1996). *Beck Depression Inventory–II (BDI-II) Manual*](https://www.pearsonassessments.com/store/usassessments/en/Store/Professional-Assessments/Behavior/Depression-Suicide/Beck-Depression-Inventory-%7C-Second-Edition/p/100000159.html)
- [Beck, A. T. et al. (1988). *Psychometric properties of the Beck Depression Inventory: Twenty-five years of evaluation*](https://doi.org/10.1016/0272-7358(88)90050-5)
- [Brown, C. et al. (1995). *Assessing Depression in Primary Care Practice with the Beck Depression Inventory and the Hamilton Rating Scale for Depression*](https://doi.org/10.1037/1040-3590.7.1.59)
- [Schneibel, R. et al. (2012). *Sensitivity to detect change and the correlation of clinical factors with the Hamilton Depression Rating Scale and the Beck Depression Inventory in depressed inpatients*](https://doi.org/10.1016/j.psychres.2011.11.014)

See `references.bib` in the atlas root for full bibliographic entries.
