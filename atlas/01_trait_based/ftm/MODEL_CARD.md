# (6) Four Temperaments

**Abbreviation:** FT
**Category:** Trait-Based Models
**Model Number:** 6 of 44

[![FT Model Diagram](ftm_small.png)](../../../graphs/ftm_large.png)

---

### Description.
The **Four Temperaments** model is an ancient proto-psychological framework proposing four fundamental personality types, **Sanguine**, **Choleric**, **Melancholic**, and **Phlegmatic**.
Originating in Graeco-Arabic medicine, it attributed temperament to bodily “humors”: blood, yellow bile, black bile, and phlegm.
Although superseded by modern psychometrics, the typology remains influential in historical scholarship and popular character theory [HippocratesCorpus, GalenOnTemperaments].

### Dimensions, Examples, and Brain–Function Mapping.

  - **Sanguine (Optimistic / Sociable):** Outgoing, impulsive, pleasure-seeking, charismatic.
    *Example:* Initiating friendly conversations with strangers at a social event.
    Maps to *Reward Drive and Social Engagement* (L2), AI seeking social feedback or immediate sensory reward.
  - **Choleric (Ambitious / Leader-like):** Decisive, goal-oriented, dominant, assertive.
    *Example:* Taking charge of a stalled meeting to produce an actionable plan.
    Maps to *Executive Control and Goal Pursuit* (L2), AI forming and executing hierarchical task plans.
  - **Melancholic (Analytical / Reflective):** Thoughtful, precise, perfectionistic, reserved.
    *Example:* Crafting a detailed project schedule and anticipating contingencies.
    Maps to *Self-Reflection and Analytical Processing* (L3), AI engaging in deliberate evaluation before action.
  - **Phlegmatic (Calm / Peaceful):** Relaxed, consistent, agreeable, stabilizing.
    *Example:* Mediating workplace conflict with patience and composure.
    Maps to *Emotional Regulation and Stability Maintenance* (L3), AI sustaining steady affective or behavioral states under stress.

### Applications.

  - **Historical Medicine and Philosophy:**
    Guided humoral diagnostics and lifestyle prescriptions across Greek, Islamic, and medieval traditions [Heineman2005].
  - **Creative Writing and Character Design:**
    Serves as a framework for building archetypal characters in literature, theater, and game design [CreativeArchetypes2020, campbell2008hero].
  - **Team-Building and Self-Help:**
    Used informally to illustrate communication styles and conflict approaches in modern workshops [TeamDynamics2018].
  - **Popular Psychology and Digital Typology:**
    Persists in online personality quizzes and self-assessment tools [DigitalTypology2021].

### Timeline.

  - **c. 400 BC:** Hippocratic corpus describes the four humors and their behavioral effects [HippocratesCorpus].
  - **c. 130–210 AD:** Galen formalizes the link between humors and temperaments [GalenOnTemperaments].
  - **Medieval Era (5th–15th Century):** Avicenna and others integrate humoral theory into medical philosophy [MedievalHumorTheory].
  - **19th Century Typology:** Early psychologists reinterpret temperaments along emotional and activity dimensions [Crocq2013Milestones].
  - **20th Century and Beyond:** Though scientifically obsolete, the model influences educational and typological systems (e.g., Waldorf education, Keirsey Temperament Sorter).

### Psychometrics.

  - **Format:** Categorical assignment to one of four types; not a standardized instrument.
  - **Method:** Observation and philosophical reasoning historically; modern use via informal checklists.
  - **Reliability and Validity:** Lacks empirical factor structure or predictive validity; primarily of historical and conceptual value.
  - **Primary Use:** Scholarship, character creation, informal personality self-typing.

### Data Structure.
Dataset (`ftm.csv`) encodes lexical information for each temperament:

  - `Factor` – Temperament type (`Sanguine`, `Choleric`, `Melancholic`, `Phlegmatic`)
  - `Adjective` – Descriptive term (e.g., `Talkative`, `Sociable`)
  - `Synonym` – Near equivalent (e.g., `Communicative`)
  - `Verb` – Behavioral expression (e.g., `Chat`)
  - `Noun` – Nominal form (e.g., `Talkativeness`)

### Resources.

  - **Mapped Brain Functions Table:** Table tab:ft-mapping.
  - **L1–L3 AI Maturity Definitions:** Appendix sec:ai-maturity-levels.
  - **Interactive Literature Map:** [Connected Papers graph for Hippocratic Corpus](https://www.connectedpapers.com/main/4887b286108ce66f545b6e7274aac03fbe2c384d/Hippocratic-Corpus/graph).
  - **Dataset:** [`FT_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/ftm.csv).
  - **Embeddings File:** [`ft_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/ftm_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/ftm.csv`](../../../datasets/ftm.csv) |
| Embeddings | [`Embeddings/ftm_embeddings.csv`](../../../Embeddings/ftm_embeddings.csv) |
| RF Model | [`models/ftm_rf_model.pkl`](../../../models/ftm_rf_model.pkl) |
| Label Encoder | [`models/ftm_label_encoder.pkl`](../../../models/ftm_label_encoder.pkl) |
| Graph (large) | [`graphs/ftm_large.png`](../../../graphs/ftm_large.png) |


## References

The following references are cited in this model card:

- `CreativeArchetypes2020`
- `Crocq2013Milestones`
- `DigitalTypology2021`
- `GalenOnTemperaments`
- `Heineman2005`
- `HippocratesCorpus`
- `MedievalHumorTheory`
- `TeamDynamics2018`
- `campbell2008hero`

See `references.bib` in the atlas root for full bibliographic entries.
