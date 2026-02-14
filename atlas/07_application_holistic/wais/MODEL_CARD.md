# (38) Wechsler Adult Intelligence Scale

**Abbreviation:** WAIS
**Category:** Application-Specific and Holistic Models
**Model Number:** 38 of 44

[![WAIS Model Diagram](wais_small.png)](../../../graphs/wais_large.png)

---

### Description.
The **Everything DiSC Workplace Profile (DiSC)** is a behavioral assessment developed by Wiley, based on William Moulton Marston’s foundational *DISC theory of emotions and behavior* [Marston1928Emotions].
It classifies individuals into four primary styles *Dominance (D)*, *Influence (i)*, *Steadiness (S)*, and *Conscientiousness (C)*, to enhance self-awareness, interpersonal communication, and team collaboration [McKennaSheltonDarling2002, BrueningMadsenEvanovichFuller2010].
Unlike traditional personality inventories, DiSC focuses on observable behavioral tendencies within workplace contexts rather than underlying traits.

### Dimensions, Examples, and Brain–Function Mapping.
Each DiSC style corresponds to characteristic cognitive or behavioral functions, which can be mirrored in AI systems for adaptive interaction modeling (see Appendix sec:ai-maturity-levels).

  - **Dominance (D):**
  Direct, assertive, results-oriented.
  *Maps to* Strategic Planning & Goal-Oriented Decision-Making (L2).

    - **Example (L2):** AlphaZero-like agents using Monte Carlo Tree Search to maximize strategic advantage.


  - **Influence (i):**
  Sociable, persuasive, expressive.
  *Maps to* Social Cognition & Persuasion Modeling (L2–L3).

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
| Dataset | [`datasets/wais.csv`](../../../datasets/wais.csv) |
| Embeddings | [`Embeddings/wais_embeddings.csv`](../../../Embeddings/wais_embeddings.csv) |
| RF Model | [`models/wais_rf_model.pkl`](../../../models/wais_rf_model.pkl) |
| Label Encoder | [`models/wais_label_encoder.pkl`](../../../models/wais_label_encoder.pkl) |
| Graph (large) | [`graphs/wais_large.png`](../../../graphs/wais_large.png) |


## References

The following references are cited in this model card:

- `BrueningMadsenEvanovichFuller2010`
- `Marston1928Emotions`
- `McKennaSheltonDarling2002`
- `Scarbecz2007`
- `Wiley2012DISCManual`

See `references.bib` in the atlas root for full bibliographic entries.
