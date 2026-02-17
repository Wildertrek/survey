# (37) DiSC Workplace Profile

**Abbreviation:** DiSC
**Category:** Interpersonal and Conflict Resolution Models
**Model Number:** 37 of 44

[![DiSC Model Diagram](disc_small.png)](../../../graphs/disc_large.png)

---

### Description.
The **Everything DiSC Workplace Profile (DiSC)** is a behavioral assessment developed by Wiley, based on William Moulton Marston's foundational *DISC theory of emotions and behavior* [Marston1928Emotions].
It classifies individuals into four primary styles *Dominance (D)*, *Influence (i)*, *Steadiness (S)*, and *Conscientiousness (C)*, to enhance self-awareness, interpersonal communication, and team collaboration [McKennaSheltonDarling2002, BrueningMadsenEvanovichFuller2010].
Unlike traditional personality inventories, DiSC focuses on observable behavioral tendencies within workplace contexts rather than underlying traits.

### Dimensions, Examples, and Brain-Function Mapping.
> AI maturity mappings (L1–L3) follow the foundation-agent cognitive hierarchy of Liu et al. (2025).

  - **Dominance (D):**
  Direct, assertive, results-oriented.
  *Maps to* Strategic Planning & Goal-Oriented Decision-Making (L2).

    - **Example (L2):** AlphaZero-like agents using Monte Carlo Tree Search to maximize strategic advantage.


  - **Influence (i):**
  Sociable, persuasive, expressive.
  *Maps to* Social Cognition & Persuasion Modeling (L2-L3).

    - **Example (L2):** LLMs generating context-aware persuasive messages.
    - **Example (L3):** Generative agents modeling shared emotional states and cooperative intent.


  - **Steadiness (S):**
  Cooperative, patient, relationship-focused.
  *Maps to* Adaptive Feedback Loops & Stability Maintenance (L2).

    - **Example (L2):** Transformer-based dialogue systems maintaining long-context coherence to foster rapport.


  - **Conscientiousness (C):**
  Analytical, systematic, quality-driven.
  *Maps to* Logical Reasoning & Error Monitoring (L2).

    - **Example (L2):** Neuro-symbolic reasoning engines applying rule-based consistency checks in decision pipelines.


### Applications.

  - **Team Development:** Diagnose communication mismatches and align complementary work styles.
  - **Leadership Coaching:** Guide adaptive leadership behaviors across diverse interpersonal contexts.
  - **Organizational Training:** Improve workplace culture by embedding DiSC-informed communication frameworks.
  - **Sales and Client Relations:** Personalize engagement tactics based on behavioral style prediction [Scarbecz2007].
  - **AI Interaction Design:** Parameterize conversational agents with human-aligned communication archetypes (e.g., assertive vs.\ affiliative dialogue policies).

### Data Structure.
Dataset `disc.csv` defines each DiSC style and its behavioral attributes:

  - `Domain`: DiSC
  - `Subcategory`: Primary style (D, i, S, C).
  - `Factor`: Behavioral facet (e.g., decisiveness, empathy, precision).
  - `Adjective`: Descriptive phrase of trait expression.
  - `Synonym, Verb, Noun`: Lexical and semantic fields.

Flattened schema: `Domain, Subcategory, Factor, Adjective, Synonym, Verb, Noun, Embedding`.

### Resources.

  - **Primary Theory:** Marston, W. M. (1928). *Emotions of Normal People* [Marston1928Emotions].
  - **Assessment Publisher:** Everything DiSC (Wiley) [Wiley2012DISCManual].
  - **Supporting Research:**

    - Bruening et al.\ (2010) on emotional intelligence and DiSC in teams [BrueningMadsenEvanovichFuller2010].
    - McKenna et al.\ (2002) on management and leadership applications [McKennaSheltonDarling2002].

  - **Interactive Literature Map:** [Connected Papers graph for DiSC](https://www.connectedpapers.com/main/700b81973fa8dbae12a2c683d020965954af8fc0/Research-Review-on-the-Significance-of-Implication-of-Psychometric-Tests-build-on-DISC-Theory-of-William-MarstonAssessing-its-Outcome-on-Employees-in-IT-SectorLinked-to-Behavioural-Engagement-and-Organizational-Productivity/graph).
  - **Dataset:** [`DiSC_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/disc.csv).
  - **Embeddings:** [`disc_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/disc_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/disc.csv`](../../../datasets/disc.csv) |
| Embeddings | [`Embeddings/disc_embeddings.csv`](../../../Embeddings/disc_embeddings.csv) |
| RF Model | [`models/disc_rf_model.pkl`](../../../models/disc_rf_model.pkl) |
| Label Encoder | [`models/disc_label_encoder.pkl`](../../../models/disc_label_encoder.pkl) |
| Graph (large) | [`graphs/disc_large.png`](../../../graphs/disc_large.png) |


---

## Validation Results

> From: Raetano, Gregor, & Tamang (2026). "A Survey and Computational Atlas of Personality Models." Under review, ACM TIST.

**Performance Tier:** Low (<50%)

### Classification Performance

| Metric | Value |
|--------|-------|
| Factors | 29 |
| Test Items | 409 |
| RF Accuracy | 9.5% |
| F1 Score (macro) | 0.0664 |
| Precision | 0.0680 |
| Recall | 0.0954 |

### Baseline Comparisons

| Baseline | Accuracy | Lift |
|----------|----------|------|
| Random | 3.5% | +6.1% |
| Frequency | 51.6% | -42.1% |

### LLM Judge Evaluation

Triple-judge panel: GPT-5.2, Gemini 3 Pro, Claude Opus 4.6.

| Metric | Value |
|--------|-------|
| RF-Judge Agreement | 20.0% |
| Expected-Factor Agreement | 100.0% |
| Item Validity Rate | 23.3% |
| Mean Confidence | 5.00 / 5.0 |
| Inter-Judge Agreement | 100.0% |

### Category Context

| Metric | Value |
|--------|-------|
| Category | Interpersonal |
| Category Mean Accuracy | 23.7% |
| Category Best | tki (37.8%) |
| Models in Category | 2 |

## References

The following references are cited in this model card:

- [Bruening, J. et al. (2010). *Discovery, Integration, Application and Teaching: Service Learning through Sport and Physical Activity*](https://doi.org/10.1123/SMEJ.4.1.31)
- [Marston, W. M. (1928). *Emotions of Normal People*](https://archive.org/details/emotionsofnormal032195mbp)
- [McKenna, M. et al. (2002). *The Impact of Behavioral Style Assessment on Organizational Effectiveness: A Call for Action*](https://doi.org/10.1108/01437730210441274)
- [Scarbecz, M. (2007). *Using the DISC System to Motivate Dental Patients*](https://doi.org/10.14219/JADA.ARCHIVE.2007.0171)
- `Wiley2012DISCManual`

See `references.bib` in the atlas root for full bibliographic entries.
