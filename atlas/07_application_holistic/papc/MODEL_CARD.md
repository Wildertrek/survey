# (43) Parametric Analysis of Person Characteristics

**Abbreviation:** PAPC
**Category:** Application-Specific and Holistic Models
**Model Number:** 43 of 44

[![PAPC Model Diagram](papc_small.png)](../../../graphs/papc_large.png)

---

### Description.
The **Parametric Analysis of Person Characteristics (PAPC)** [Ossorio1985, Ossorio2006] provides a multidimensional framework for organizing individual attributes across five primary domains: *Person, Health, Lifestyle, Psychological Characteristics,* and *Social Factors.*
Originally proposed by Peter Ossorio within the Descriptive Psychology paradigm, PAPC offers a structured ontology that integrates demographic, physiological, behavioral, and affective parameters into a unified representation of personhood, an approach highly compatible with modern AI systems that seek to model agents in context.

### Dimensions and Brain–Function Mapping.
> AI maturity mappings (L1–L3) follow the foundation-agent cognitive hierarchy of Liu et al. (2025).

  - **Person:** Core identifiers and demographic attributes (e.g., ID, Age, Gender).
    *Example:* A personal assistant recalling previous sessions by user ID to maintain context.
    *Maps to* Episodic Memory & Identity Retrieval (L2) ,  persistence and continuity in agent memory systems.

  - **Health:** Physiological and biometric data (e.g., BMI, Blood Pressure).
    *Example:* A wearable continuously transmitting vitals to a health dashboard.
    *Maps to* Sensory Perception & Biometric Monitoring (L1) ,  sensor fusion and data interpretation.

  - **Lifestyle:** Behavioral habits and routines (e.g., Diet, Exercise, Stress Level).
    *Example:* Generating personalized workout suggestions from activity logs.
    *Maps to* Decision-Making under Uncertainty (L2) ,  adaptive recommendation optimization.

  - **Psychological Characteristics:** Cognitive, affective, and motivational factors (e.g., Personality Traits, Emotional Intelligence) [Salovey1990, Petrides2007].
    *Example:* Adjusting coaching tone based on emotional intelligence assessment.
    *Maps to* Metacognition & Self-Awareness (L3) ,  agents reflecting on reasoning to improve strategy alignment.

  - **Social Factors:** Socioeconomic and interpersonal context (e.g., Social Support, SES).
    *Example:* Identifying a user’s support network to tailor behavioral interventions.
    *Maps to* Empathy & Social Cognition (L3) ,  agents modeling relational dynamics to enhance trust and rapport.

### Applications.

  - **Personalized Health Agents:** Integrating demographic and biometric data for adaptive wellness feedback.
  - **Intelligent Tutoring Systems:** Adapting instruction to learner profiles and cognitive states in real time.
  - **Context-Aware Conversational Agents:** Inferring social and emotional context to personalize dialogue.
  - **Behavioral Forecasting Models:** Predicting adherence or burnout using lifestyle and psychological indicators.
  - **Explainable Human Profiling:** Providing interpretable, domain-separated insights for clinical and HR applications.

### Timeline.

  - **1985–2000:** Ossorio formulates Descriptive Psychology and introduces PAPC [Ossorio1985].
  - **2000–2010:** Integration with health informatics and early wearable data streams [Ossorio2006].
  - **2010–2020:** Expansion of the Psychological domain with Emotional Intelligence constructs [Salovey1990, Petrides2007].
  - **2020–Present:** PAPC applied in AI-driven personalization across health, education, and social systems.

### Psychometrics.
While PAPC is primarily a *structural ontology* rather than a fixed assessment tool, its component domains can be operationalized using validated instruments:

  - **Psychological Characteristics:** TEIQue and MSCEIT for Emotional Intelligence [Petrides2007, Salovey1990].
  - **Health and Lifestyle:** SF-36 Health Survey; International Physical Activity Questionnaire (IPAQ).
  - **Social Factors:** Multidimensional Scale of Perceived Social Support (MSPSS) [Zimet1988MSPSS].

Cross-domain integration enables hybrid measurement systems combining subjective (survey-based) and objective (sensor-based) data streams.

### Data Structure.
Dataset `papc.csv` encodes lexical and semantic descriptors for each domain:
`Factor, Adjective, Synonym, Verb, Noun.`
Each row represents a semantic vector aligned with PAPC dimensions to enable embedding-based clustering and linkage with other personality frameworks.

### Resources.

  - **Primary Source:** Ossorio, P. G. (1985–2006). *The Behavior of Persons.*
  - **Supplementary References:**
    Salovey & Mayer (1990) on Emotional Intelligence; Petrides (2007) on Trait EI;
    Zimet et al. (1988) on Social Support (MSPSS).
  - **Interactive Literature Map:** [Connected Papers graph for PAPC.](https://www.connectedpapers.com/main/b3a4c2ea85229c00dc572171703b8c6092b81baf/What-is-Descriptive-Psychology%3F-An-Introduction/graph)
  - **Dataset:** [`papc_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/papc.csv).
  - **Embeddings:** [`papc_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/papc_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/papc.csv`](../../../datasets/papc.csv) |
| Embeddings | [`Embeddings/papc_embeddings.csv`](../../../Embeddings/papc_embeddings.csv) |
| RF Model | [`models/papc_rf_model.pkl`](../../../models/papc_rf_model.pkl) |
| Label Encoder | [`models/papc_label_encoder.pkl`](../../../models/papc_label_encoder.pkl) |
| Graph (large) | [`graphs/papc_large.png`](../../../graphs/papc_large.png) |


---

## Validation Results

> From: Raetano, Gregor, & Tamang (2026). "A Survey and Computational Atlas of Personality Models." Under review, ACM TIST.

**Performance Tier:** Low (<50%)

### Classification Performance

| Metric | Value |
|--------|-------|
| Factors | 5 |
| Test Items | 74 |
| RF Accuracy | 33.8% |
| F1 Score (macro) | 0.3101 |
| Precision | 0.3114 |
| Recall | 0.3381 |

### Baseline Comparisons

| Baseline | Accuracy | Lift |
|----------|----------|------|
| Random | 20.0% | +13.8% |
| Frequency | 25.0% | +8.8% |

### LLM Judge Evaluation

Triple-judge panel: GPT-5.2, Gemini 3 Pro, Claude Opus 4.6.

| Metric | Value |
|--------|-------|
| RF-Judge Agreement | 40.0% |
| Expected-Factor Agreement | 100.0% |
| Item Validity Rate | 80.0% |
| Mean Confidence | 4.65 / 5.0 |
| Inter-Judge Agreement | 100.0% |

### Category Context

| Metric | Value |
|--------|-------|
| Category | App/Holistic |
| Category Mean Accuracy | 50.9% |
| Category Best | bt (90.7%) |
| Models in Category | 6 |

### Experiment 2: Model Improvement

| Intervention | Accuracy | Delta |
|-------------|----------|-------|
| Exp1 baseline (1536-dim) | 32.4% | — |
| RQ9: 3072-dim embeddings | 21.6% | -10.8% |
| RQ7: Data augmentation | 59.5% | +27.0% |
| **Best result** | **59.5%** | **+27.0%** |

Best intervention: Data augmentation (65 LLM-generated items).

## References

The following references are cited in this model card:

- `Ossorio1985`
- `Ossorio2006`
- [Petrides, K. V. et al. (2007). *The location of trait emotional intelligence in personality factor space*](https://doi.org/10.1348/000712606X120618)
- [Salovey, P. & Mayer, J. D. (1990). *Emotional intelligence*](https://doi.org/10.2190/DUGG-P24E-52WK-6CDG)
- `Zimet1988MSPSS`

See `references.bib` in the atlas root for full bibliographic entries.
