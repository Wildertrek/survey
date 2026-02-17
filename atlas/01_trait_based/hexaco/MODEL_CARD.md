# (3) HEXACO Personality Model

**Abbreviation:** HEXACO
**Category:** Trait-Based Models
**Model Number:** 3 of 44

[![HEXACO Model Diagram](hex_small.png)](../../../graphs/hex_large.png)

---

### Description.
Developed by Kibeom Lee and Michael C. Ashton, the HEXACO model extends the traditional Big Five framework by introducing a sixth major dimension, **Honesty–Humility**.
It posits that personality is best described across six broad domains validated across multiple cultures and languages [AshtonLee2004, LeeAshton2012].

### Dimensions, Examples, and Brain–Function Mapping.
> AI maturity mappings (L1–L3) follow the foundation-agent cognitive hierarchy of Liu et al. (2025).

  - **H – Honesty–Humility:** Sincerity, fairness, greed avoidance, and modesty.

      - Example: Refusing to exploit an unfair advantage even if undetected.
      - Maps to *Moral Reasoning and Fairness Computation* (L2 AI Maturity), AI applying fairness or ethical constraints in decision processes.

  - **E – Emotionality:** Anxiety, fearfulness, dependence, and sentimentality.

      - Example: Feeling anxious about potential harm or easily moved by a sad story.
      - Maps to *Emotional Processing and Threat Assessment* (L3), AI modeling nuanced emotion and risk detection.

  - **X – Extraversion:** Social boldness, liveliness, and confidence.

      - Example: Engaging energetically in social gatherings.
      - Maps to *Reward Sensitivity and Social Engagement* (L2), AI behaviors guided by feedback or reward mechanisms.

  - **A – Agreeableness (vs. Anger):** Forgiveness, gentleness, flexibility, and patience.

      - Example: Mediating conflicts calmly and empathetically.
      - Maps to *Social Cognition and Conflict Resolution* (L3), AI modeling intentions and resolving social tension collaboratively.

  - **C – Conscientiousness:** Organization, diligence, perfectionism, and prudence.

      - Example: Meticulously managing a multi-step project timeline.
      - Maps to *Working Memory, Planning, and Goal Pursuit* (L2), AI maintaining task-state and sequence control.

  - **O – Openness to Experience:** Aesthetic appreciation, inquisitiveness, and creativity.

      - Example: Exploring novel ideas or unconventional problem-solving approaches.
      - Maps to *Cognitive Flexibility and Creative Exploration* (L3), AI generating innovative solutions in dynamic contexts.


### Applications.

  - **Personnel Selection and Organizational Behavior:** Predicts performance, integrity, and leadership via Honesty–Humility and Conscientiousness [LeeBerry2019, Pletzer2019].
  - **Moral Reasoning and Ethics:** Connects Honesty–Humility to prosocial and moral decision-making [Bell2021MoralMosaic, Moran2020].
  - **Cross-Cultural Validation:** Confirms six-factor stability across diverse societies [DeVries2015, Castro2014].
  - **AI Personality Modeling and HCI:** Guides the development of trustworthy and believable virtual agents [HannaRichards2015, JiTang2024].
  - **Conflict Resolution and Interpersonal Dynamics:** Informs mediation and collaboration strategies based on Agreeableness and Emotionality [Balliet2013, PletzerThielmann2018].

### Timeline.

  - **Early 2000s:** Cross-linguistic psycholexical studies indicate a six-factor model.
  - **2004:** Ashton and Lee formally introduce the HEXACO model and HEXACO Personality Inventory (HEXACO–PI) [AshtonLee2004].
  - **2007:** Empirical validation highlights the predictive power of Honesty–Humility [AshtonLee2007].
  - **2009–2012:** Revised HEXACO–PI–R published and standardized [LeeAshton2012].

### Psychometrics.

  - **Format:** 60–200 items rated on 5-point Likert scales.
  - **Reliability:** Cronbach’s α = 0.80–0.90; high test–retest reliability [LeeAshton2012].
  - **Factor Validity:** Supported across numerous cultures and languages.
  - **Cross-Cultural Stability:** Replicated in over 30 nations, confirming robustness.

### Data Structure.
The dataset (`hex.csv`) encodes lexical information for each HEXACO factor:

  - `Factor` – Domain (e.g., `Honesty-Humility`, `Emotionality`)
  - `Adjective` – Descriptive trait (e.g., `Sincere`, `Anxious`)
  - `Synonym` – Near-equivalent term (e.g., `Fair`)
  - `Verb` – Behavioral form (e.g., `Empathize`)
  - `Noun` – Nominal form (e.g., `Sincerity`, `Empathizer`)

### Resources.

  - **Official Website:** [hexaco.org](http://hexaco.org).
  - **Interactive Literature Map:** [Connected Papers graph for Ashton & Lee (2004)](https://www.connectedpapers.com/main/b44b39beaf8a9bdeddd6f7e558c45dde7056f20a/Psychometric-Properties-of-the-HEXACO-Personality-Inventory/graph).
  - **Dataset:** [`HEXACO_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/hex.csv).
  - **Embeddings File:** [`hex_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/hex_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/hex.csv`](../../../datasets/hex.csv) |
| Embeddings | [`Embeddings/hex_embeddings.csv`](../../../Embeddings/hex_embeddings.csv) |
| RF Model | [`models/hex_rf_model.pkl`](../../../models/hex_rf_model.pkl) |
| Label Encoder | [`models/hex_label_encoder.pkl`](../../../models/hex_label_encoder.pkl) |
| Graph (large) | [`graphs/hex_large.png`](../../../graphs/hex_large.png) |


---

## Validation Results

> From: Raetano, Gregor, & Tamang (2026). "A Survey and Computational Atlas of Personality Models." Under review, ACM TIST.

**Performance Tier:** Moderate (50-70%)

### Classification Performance

| Metric | Value |
|--------|-------|
| Factors | 6 |
| Test Items | 85 |
| RF Accuracy | 62.4% |
| F1 Score (macro) | 0.6098 |
| Precision | 0.6406 |
| Recall | 0.6270 |

### Baseline Comparisons

| Baseline | Accuracy | Lift |
|----------|----------|------|
| Random | 16.7% | +45.7% |
| Frequency | 22.7% | +39.6% |

### LLM Judge Evaluation

Triple-judge panel: GPT-5.2, Gemini 3 Pro, Claude Opus 4.6.

| Metric | Value |
|--------|-------|
| RF-Judge Agreement | 32.5% |
| Expected-Factor Agreement | 100.0% |
| Item Validity Rate | 35.8% |
| Mean Confidence | 4.93 / 5.0 |
| Inter-Judge Agreement | 100.0% |

### Category Context

| Metric | Value |
|--------|-------|
| Category | Trait-Based |
| Category Mean Accuracy | 64.0% |
| Category Best | ocean (76.1%) |
| Models in Category | 6 |

## References

The following references are cited in this model card:

- [Ashton, M. C. et al. (2004). *A six-factor structure of personality-descriptive adjectives: Solutions from psycholexical studies in seven languages*](https://doi.org/10.1037/0022-3514.86.2.356)
- [Ashton, M. C. & Lee, K. (2007). *Empirical, theoretical, and practical advantages of the HEXACO model of personality structure*](https://doi.org/10.1177/1088868306294907)
- [Balliet, D. & Van Lange, P. A. M. (2013). *Trust, conflict, and cooperation across 18 societies: A meta-analysis*](https://doi.org/10.1037/a0030939)
- [Bell, K. R. & Showers, C. J. (2021). *The Moral Mosaic: A Factor Structure for Predictors of Moral Behavior*](https://doi.org/10.1016/j.paid.2020.110340)
- [Castro, Y. et al. (2014). *Validation of the HEXACO-100 in a Spanish sample*](https://doi.org/10.1016/j.paid.2014.01.031)
- [de Vries, R. E. et al. (2015). *A cross-cultural analysis of personality structure through the lens of the HEXACO model*](https://osf.io/btsk7)
- [Hanna, N. & Richards, D. (2015). *The influence of users' personality on the perception of intelligent virtual agents and trust in collaboration*](https://doi.org/10.1007/978-3-319-24804-2_3)
- [Ji, Y. et al. (2024). *Is persona enough for personality? Using ChatGPT to reconstruct an agent's latent personality*](https://arxiv.org/abs/2406.12216)
- `LeeAshton2012`
- [Lee, Y. et al. (2019). *The importance of being humble: A meta-analysis of Honesty-Humility and job performance*](https://doi.org/10.1037/apl0000421)
- [Moran, J. M. et al. (2020). *Moral judgements of fairness-related actions are flexibly updated in light of new evidence*](https://doi.org/10.1038/s41598-020-74975-0)
- [Pletzer, J. L. et al. (2019). *A Meta‑Analysis of the Relations between Personality and Workplace Deviance: Big Five versus HEXACO*](https://doi.org/10.1016/j.jvb.2019.04.004)
- [Pletzer, J. L. et al. (2021). *HEXACO Personality and Organizational Citizenship Behavior: A Domain‑ and Facet‑Level Meta‑Analysis*](https://doi.org/10.1080/08959285.2021.1891072)

See `references.bib` in the atlas root for full bibliographic entries.
