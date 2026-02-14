# (28) Temperament and Character Inventory

**Abbreviation:** TCI
**Category:** Clinical and Psychological Health Models
**Model Number:** 28 of 44

[![TCI Model Diagram](tci_small.png)](../../../graphs/tci_large.png)

---

### Model Type.
Clinical; Psychobiological.

### Description.
The **Temperament and Character Inventory (TCI)** operationalizes C. Robert Cloninger’s Psychobiological Model of Temperament and Character, a biosocial theory integrating genetic, neurochemical, and experiential influences on personality.
Temperament dimensions are heritable, reflecting automatic emotional responses tied to specific neurotransmitter systems, while character dimensions evolve through learning, socialization, and self-concept integration.
The TCI expands Cloninger’s earlier *Tridimensional Personality Questionnaire (TPQ)* from three to seven dimensions: four temperament and three character factors [Cloninger1986, Cloninger1993, Cloninger1994TCIManual].

### Dimensions, Examples, and Functional Mapping.

  - **Temperament Dimensions:**

      - **Novelty Seeking (NS):** Exploratory excitability and impulsive reward pursuit; linked to dopamine.
        Example: Signing up spontaneously for a new activity.
        Maps to *Adaptive Exploration & Novelty Processing* (L2).
      - **Harm Avoidance (HA):** Cautiousness, anticipatory worry, and behavioral inhibition; linked to serotonin.
        Example: Avoiding risk due to fear of negative evaluation.
        Maps to *Risk Assessment & Threat Mitigation* (L3).
      - **Reward Dependence (RD):** Sensitivity to social reward and attachment; linked to norepinephrine.
        Example: Seeking affirmation or approval from peers.
        Maps to *Social Reinforcement Learning* (L2).
      - **Persistence (PS):** Perseverance despite frustration or fatigue.
        Example: Continuing work through setbacks or exhaustion.
        Maps to *Goal Maintenance & Effort Regulation* (L2).

  - **Character Dimensions:**

      - **Self-Directedness (SD):** Autonomy, purposefulness, and self-acceptance.
        Example: Setting and achieving personal goals independently.
        Maps to *Self-Regulation & Autonomous Goal Management* (L3).
      - **Cooperativeness (CO):** Empathy, social tolerance, and helpfulness.
        Example: Mentoring or assisting colleagues with understanding.
        Maps to *Social Calibration & Prosocial Behavior* (L3).
      - **Self-Transcendence (ST):** Spirituality, idealism, and identification with universal values.
        Example: Meditation, altruism, or finding meaning in art or nature.
        Maps to *Abstract Self-Modeling & Value Integration* (L3).


### Timeline.

  - **1986–1987:** Introduction of the Tridimensional Personality Questionnaire (TPQ) [Cloninger1986].
  - **1993:** Expansion to seven dimensions with the TCI [Cloninger1993].
  - **1994:** Publication of the TCI manual [Cloninger1994TCIManual].
  - **1999–Present:** Cross-cultural validations and the TCI-R revisions [Kijima2000TCIJapan, Gutierrez2001TCISpanish, Sung2002TCICorey, Brandstrom2008TCISweden].

### Applications.

  - **Clinical Assessment:** Profiling temperament and character patterns related to mood, anxiety, and personality disorders [Pomerleau1992, Bayon1996, Svrakic1993, Young1995TCIUnipolarBipolar].
  - **Behavioral Genetics and Neurobiology:** Correlating dopamine (NS), serotonin (HA), and norepinephrine (RD) pathways with genetic polymorphisms [Gillespie2003TCIGenetics].
  - **Personalized Psychotherapy:** Targeting self-directedness and cooperativeness to enhance treatment outcomes [DeFruyt2000, Celikel2009TCIDepressionTreatment].
  - **Well-being and Resilience:** Using ST and CO scales to assess spirituality, purpose, and flourishing [Cloninger2004, Cloninger2006Wellbeing, Jylha2006TCIGeneralPopulation].
  - **Digital Phenotyping & AI-Driven Mental Health:** Employing TCI-derived behavioral traits to adapt empathic chatbot or digital therapy responses [Mouchabac2022, Fraser2023].

### Psychometrics.

  - **Format:** TCI-R – 240 items (5-point Likert); short forms (TCI-R-S, 140 items).
  - **Reliability:** α coefficients typically 0.65–0.85; stable test-retest reliability [Hansenne2005TCIRBelgian].
  - **Validity:** Robust seven-factor structure, with strong convergent validity vs.\ Big Five and clinical outcomes [Cloninger2006Wellbeing].
  - **Method:** Self-report; informant and youth versions available.

### Data Structure.
Each row in `tci.csv` represents a lexical feature for one of seven TCI dimensions, with fields:
`DimensionType` (Temperament/Character), `Factor`, `Adjective`, `Synonym`, `Verb`, `Noun`.

### Resources.

  - **Mapped Brain Functions Table:** Table tab:tci-mapping.
  - **AI Maturity Levels:** Section sec:ai-maturity-levels.
  - **Connected Papers:** [Cloninger et al. (1993) Graph](https://www.connectedpapers.com/main/3bcf1c4ec20101890c252d30548cd77dbe260b87/Temperament-and-Character-Inventory/graph).
  - **Dataset:** [`TCI_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/tci.csv).
  - **Embeddings:** [`tci_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/tci_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/tci.csv`](../../../datasets/tci.csv) |
| Embeddings | [`Embeddings/tci_embeddings.csv`](../../../Embeddings/tci_embeddings.csv) |
| RF Model | [`models/tci_rf_model.pkl`](../../../models/tci_rf_model.pkl) |
| Label Encoder | [`models/tci_label_encoder.pkl`](../../../models/tci_label_encoder.pkl) |
| Graph (large) | [`graphs/tci_large.png`](../../../graphs/tci_large.png) |


## References

The following references are cited in this model card:

- `Bayon1996`
- `Brandstrom2008TCISweden`
- `Celikel2009TCIDepressionTreatment`
- `Cloninger1986`
- `Cloninger1993`
- `Cloninger1994TCIManual`
- `Cloninger2004`
- `Cloninger2006Wellbeing`
- `DeFruyt2000`
- `Fraser2023`
- `Gillespie2003TCIGenetics`
- `Gutierrez2001TCISpanish`
- `Hansenne2005TCIRBelgian`
- `Jylha2006TCIGeneralPopulation`
- `Kijima2000TCIJapan`
- `Mouchabac2022`
- `Pomerleau1992`
- `Sung2002TCICorey`
- `Svrakic1993`
- `Young1995TCIUnipolarBipolar`

See `references.bib` in the atlas root for full bibliographic entries.
