# (44) Circumplex Model of Affect

**Abbreviation:** CMOA
**Category:** Application-Specific and Holistic Models
**Model Number:** 44 of 44

[![CMOA Model Diagram](cmoa_small.png)](../../../graphs/cmoa_large.png)

---

### Description.
The **Circumplex Model of Affect (CMOA)** [Russell1980, Russell2003] organizes emotional states within a two-dimensional space defined by *valence* (pleasant–unpleasant) and *arousal* (activation–deactivation).
This framework models affect as a continuous field rather than discrete categories, enabling both psychological and computational representations of emotion.
The CMOA underpins affective neuroscience, psychometrics, and affective computing, serving as a bridge between subjective emotional experience and measurable physiological or linguistic indicators.

### Dimensions and Brain–Function Mapping.

  - **Valence:** Reflects emotional polarity (positive vs.\ negative).
    *Example:* Classifying user sentiment in text or speech as positive or negative.
    *Maps to* Semantic Understanding & Sentiment Analysis (L2) ,  transformer models performing affective polarity classification.

  - **Arousal:** Represents physiological or subjective activation (high vs.\ low).
    *Example:* Detecting elevated heart rate as an indicator of excitement or stress.
    *Maps to* Sensory Perception & State Monitoring (L1) ,  multimodal pipelines integrating biosignals for affect inference.

### Applications.

  - **Affective Computing:** Enables real-time emotion recognition for dialogue systems and empathetic agents.
  - **Mental-Health Monitoring:** Tracks affective states via wearable or mobile data to detect stress or depression indicators.
  - **Adaptive Interfaces:** Dynamically adjust interface tone, content, or notifications based on user mood.
  - **Multimedia Tagging:** Annotates audio–visual data using valence–arousal coordinates for recommendation engines.
  - **Human–Robot Interaction:** Guides affect-responsive behavior modulation in socially assistive robots.

### Timeline.

  - **1980:** Russell introduces the circumplex structure of affect [Russell1980].
  - **1991:** Roseman develops appraisal determinants linking cognitive appraisal to discrete emotions [Roseman1991].
  - **1999:** Watson et al.\ identify dual activation systems underlying affective states [Watson1999].
  - **2002:** Ekkekakis & Petruzzello extend the model to exercise and health psychology [Ekkekakis2002].
  - **2003:** Russell refines “core affect” as a neuropsychological construct [Russell2003].

### Psychometrics.

  - **Self-Report Instruments:**
    The *Affect Grid* and the *PANAS-X* (Positive and Negative Affect Schedule ,  Expanded Form) [Watson1999] provide reliable two-axis assessment of valence–arousal states.
  - **Physiological Measures:**
    Heart-rate variability (HRV), galvanic skin response (GSR), and EEG alpha asymmetry are standard indicators of arousal and valence.
  - **Neuroimaging Evidence:**
    FMRI and PET studies associate valence with the orbitofrontal cortex and amygdala, and arousal with insular and subcortical activations [Russell2003].
  - **Cross-Cultural Validation:**
    The valence–arousal space has shown strong invariance across cultures, supporting its universality [Ekkekakis2002].

### Data Structure.
Dataset `cmoa.csv` encodes lexical affective descriptors positioned along the valence–arousal continuum:
`Factor, Adjective, Synonym, Verb, Noun.`
Each row represents an affective unit suitable for vectorization and clustering in embedding space, enabling cross-model mapping between affective lexicons and personality trait embeddings.

### Resources.

  - **Foundational Works:** Russell (1980, 2003) on the circumplex and core affect.
  - **Appraisal Theory:** Roseman (1991) linking cognitive evaluation to emotion generation.
  - **Measurement Tools:** PANAS-X [Watson1999] and Affect Grid for empirical affect mapping.
  - **Applied Psychology:** Ekkekakis & Petruzzello (2002) on affect in exercise and health.
  - **Interactive Literature Map:**
    [Connected Papers graph for CMOA.](https://www.connectedpapers.com/main/0f27792ee0e7eed4c02a52ca3a81f54c1589cc9c/Circumplex-Model-of-Affect%3A-A-Measure-of-Pleasure-and-Arousal-During-Virtual-Reality-Distraction-Analgesia./graph)
  - **Dataset:** [`cmoa_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/cmoa.csv).
  - **Embeddings:** [`cmoa_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/cmoa_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/cmoa.csv`](../../../datasets/cmoa.csv) |
| Embeddings | [`Embeddings/cmoa_embeddings.csv`](../../../Embeddings/cmoa_embeddings.csv) |
| RF Model | [`models/cmoa_rf_model.pkl`](../../../models/cmoa_rf_model.pkl) |
| Label Encoder | [`models/cmoa_label_encoder.pkl`](../../../models/cmoa_label_encoder.pkl) |
| Graph (large) | [`graphs/cmoa_large.png`](../../../graphs/cmoa_large.png) |


## References

The following references are cited in this model card:

- `Ekkekakis2002`
- `Roseman1991`
- `Russell1980`
- `Russell2003`
- `Watson1999`

See `references.bib` in the atlas root for full bibliographic entries.
