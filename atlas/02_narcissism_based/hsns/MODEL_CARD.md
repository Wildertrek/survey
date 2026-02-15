# (12) Hypersensitive Narcissism Scale

**Abbreviation:** HSNS
**Category:** Narcissism-Based Models
**Model Number:** 12 of 44

[![HSNS Model Diagram](hsns_small.png)](../../../graphs/hsns_large.png)

---

### Description.
The **Hypersensitive Narcissism Scale (HSNS)** [Hendin1997] is a 10-item self-report instrument designed to assess *vulnerable* or *covert* narcissism.
Unlike grandiose measures (e.g., NPI or FFNI), the HSNS focuses on internalized self-absorption marked by emotional fragility, rumination, and hypersensitivity to evaluation.
It captures a single latent dimension reflecting defensive introversion, social withdrawal, and unstable self-worth.

### Dimensions, Examples, and Functional Mapping.
**Hypersensitive Narcissism.**
Represents the core of vulnerable narcissism: overreactivity to criticism, chronic self-consciousness, and inwardly directed shame.
*Example:* Ruminating for days over a mildly critical comment, interpreting it as personal rejection.
Maps to:

  - *Emotion Processing and Threat Sensitivity* (L2), AI detecting subtle evaluative cues indicating potential negative feedback.
  - *Self-Referential Reflection and Negative Appraisal* (L2), AI modeling internal “self-assessment” loops after performance critiques.
  - *Affective Forecasting and Rumination Simulation* (L3), AI generating prolonged self-focused thought patterns following perceived loss or criticism.
  - *Metacognitive Calibration (Fragile Confidence)* (L3), AI dynamically lowering internal confidence estimates based on feedback history.

### Timeline.

  - **1997:** Hendin and Cheek develop and validate the HSNS as a measure of covert narcissism [Hendin1997].
  - **2018:** Cruz *et al.* conduct cross-cultural validation across five languages, confirming factorial stability [Cruz2018].
  - **2020:** Alabak *et al.* link hypersensitive narcissism with maladaptive “deep acting” strategies affecting well-being and performance [Alabak2020DeepActing].

### Applications.

  - **Clinical and Counseling Research:**
    Identifies individuals prone to social withdrawal, rumination, and distress from evaluative feedback [Hendin1997].
  - **Organizational Psychology:**
    Examines how hypersensitivity to criticism predicts burnout, job strain, and interpersonal conflict [Hosie2019].
  - **Cross-Cultural Studies:**
    Validates the vulnerable narcissism construct across diverse linguistic and cultural contexts [Cruz2018].
  - **AI and Mental Health Modeling:**
    Supports adaptive AI systems tuned to user sensitivity and self-esteem fluctuations, or modeling emotion regulation in affective computing.

### Psychometrics.

  - **Format:** 10 items, 5-point Likert scale (1 = *not at all like me*, 5 = *very much like me*).
  - **Reliability:** Cronbach’s α typically 0.75–0.85 [Hendin1997].
  - **Validity:** Converges with measures of shame, neuroticism, and social anxiety; diverges from grandiose narcissism and psychopathy.
  - **Method:** Self-report inventory; unidimensional scale.

### Data Structure.
Dataset (`hsns.csv`) captures lexical representations of hypersensitive narcissism:

  - `Factor` – Subscale: `Oversensitivity` or `Egocentrism`.
  - `Adjective` – Descriptive term (e.g., `Hypersensitive`, `Self-absorbed`).
  - `Synonym` – Equivalent adjective (e.g., `Fragile`, `Touchy`).
  - `Verb` – Behavioral form (e.g., `Ruminate`, `Withdraw`).
  - `Noun` – Nominal form (e.g., `Vulnerability`, `Oversensitivity`).

### Resources.

  - **Mapped Brain Functions Table:** Table tab:hsns-mapping.
  - **L1–L3 AI Maturity Definitions:** Section sec:ai-maturity-levels.
  - **Interactive Literature Map:**
    [Connected Papers: Hendin & Cheek (1997)](https://www.connectedpapers.com/main/fbfe7b261373cdd7d93fe2c558a3cd7c9076ac24/Evaluating-the-psychometric-properties-of-the-hypersensitive-narcissism-scale%3A-Implications-for-the-distinction-of-covert-and-overt-narcissism/graph).
  - **Dataset:** [`HSNS_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/hsns.csv).
  - **Embeddings File:** [`hsns_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/hsns_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/hsns.csv`](../../../datasets/hsns.csv) |
| Embeddings | [`Embeddings/hsns_embeddings.csv`](../../../Embeddings/hsns_embeddings.csv) |
| RF Model | [`models/hsns_rf_model.pkl`](../../../models/hsns_rf_model.pkl) |
| Label Encoder | [`models/hsns_label_encoder.pkl`](../../../models/hsns_label_encoder.pkl) |
| Graph (large) | [`graphs/hsns_large.png`](../../../graphs/hsns_large.png) |


## References

The following references are cited in this model card:

- `Alabak2020DeepActing`
- `Cruz2018`
- `Hendin1997`
- `Hosie2019`

See `references.bib` in the atlas root for full bibliographic entries.
