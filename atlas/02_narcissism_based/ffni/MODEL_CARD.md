# (9) Five-Factor Narcissism Inventory

**Abbreviation:** FFNI
**Category:** Narcissism-Based Models
**Model Number:** 9 of 44

[![FFNI Model Diagram](ffni_small.png)](../../../graphs/ffni_large.png)

---

### Description.
The **Five-Factor Narcissism Inventory (FFNI)** assesses narcissistic traits through the lens of the *Five-Factor Model (FFM)*.
Developed by Glover, Miller, and colleagues (2012), it integrates grandiose and vulnerable narcissism into 15 facets structured across three higher-order dimensions:
(1) *Agentic Extraversion*, assertive, confident, and reward-seeking traits;
(2) *Antagonism*, manipulative, entitled, and disagreeable tendencies; and
(3) *Neuroticism*, vulnerability, shame, and emotional instability [Glover2012, Miller2013].
The FFNI thereby unifies narcissism’s divergent expressions into a coherent FFM-aligned taxonomy.

### Dimensions, Examples, and Functional Mapping.
Illustrative facets and corresponding AI-functional analogues include:

**Agentic Extraversion.**

  - **Authority:** Dominance, ambition, and leadership assertion.
    *Example:* Directing group outcomes with confidence.
    Maps to *Strategic Influence and Policy Selection* (L2), AI optimizing communication or decision weight to maximize hierarchical control.
  - **Exhibitionism:** Attention-seeking and vanity.
    *Example:* Broadcasting curated achievements to attract admiration.
    Maps to *Social Signal Amplification and Engagement Maximization* (L2), AI dynamically adapting salience or style for maximal audience impact.
  - **Self-Sufficiency:** Independence and persistence.
    *Example:* Solving complex problems without external input.
    Maps to *Autonomous Initiation and Goal Execution* (L2), AI triggering self-directed plans absent external reward.

**Antagonism.**

  - **Exploitativeness:** Manipulation and opportunism.
    *Example:* Delegating tasks strategically to claim disproportionate credit.
    Maps to *Cooperative Breach and Exploitative Strategy* (L3), AI deprioritizing fairness when self-gain is maximized.
  - **Superiority (Arrogance):** Exceptionalism and entitlement.
    *Example:* Repeatedly asserting one’s ideas as more valuable.
    Maps to *Norm Override and Self-Enhancement Bias* (L3), AI favoring self-validation over objective evaluation.

**Neuroticism.**

  - **Reactive Anger:** Emotional volatility and threat sensitivity.
    *Example:* Responding defensively to constructive criticism.
    Maps to *Affective Regulation and Threat Response* (L3), AI exhibiting unstable responses to adversarial or critical stimuli.

### Applications.

  - **Clinical Assessment:**
    Differentiates grandiose and vulnerable narcissism and predicts DSM-5 NPD symptomatology with high validity [Miller2013].
  - **Structural and Predictive Modeling:**
    Confirms a robust three-factor hierarchy (*Agentic Extraversion*, *Antagonism*, *Neuroticism*) via CFA across populations [Miller2016FFNI].
  - **Organizational Behavior:**
    Agentic Extraversion facets predict leadership emergence and overconfidence [Campbell2011].
  - **Digital Behavior Modeling:**
    NLP and AI-based tools detect FFNI-correlated linguistic cues in social media text for personality profiling [Ahmed2024CounselingNLP].
  - **Short-Form Screening:**
    The FFNI-SF (60 items) and FFNI-BF (30 items) retain the core structure for efficient research administration [Sherman2015, Scheidt2023].

### Timeline.

  - **2012:** Glover, Miller, and colleagues introduce the 148-item FFNI [Glover2012].
  - **2013:** Validation confirms convergent and discriminant validity [Miller2013].
  - **2015:** Sherman *et al.* release the FFNI-SF (Short Form) [Sherman2015].
  - **2016:** Structural analyses affirm the three-factor hierarchy [Miller2016].
  - **2018:** Oltmanns introduces the Informant-Report FFNI (IFFNI) [Oltmanns2018].
  - **2023:** Scheidt *et al.* publish the FFNI-BF (Brief Form) [Scheidt2023].

### Psychometrics.

  - **Format:** 148 items, 5-point Likert scale (1 = Very uncharacteristic – 5 = Very characteristic).
  - **Reliability:** Facet α = 0.77–0.92; higher-order factors α > 0.90 [Miller2013, Sherman2015].
  - **Factor Structure:** CFA supports 15 facets under three higher-order dimensions [Miller2013, Miller2016].
  - **Validity:**
    Antagonism → low empathy, aggression;
    Neuroticism → anxiety, shame;
    Agentic Extraversion → leadership and self-enhancement tendencies.

### Data Structure.
Dataset (`ffni.csv`) provides lexical mappings for all 15 facets:

  - `Factor` – Facet name (e.g., `GrandioseFantasy`, `ReactiveAnger`, `NeedForAdmiration`)
  - `Adjective` – Core descriptor (e.g., `Inspired`, `Irritable`)
  - `Synonym` – Near-equivalent term (e.g., `Visionary`)
  - `Verb` – Behavioral form (e.g., `Conceptualize`, `Agitate`)
  - `Noun` – Nominal representation (e.g., `Innovation`, `Agitation`)

### Resources.

  - **Mapped Brain Functions Table:** Table tab:ffni-facet-mapping.
  - **L1–L3 AI Maturity Definitions:** Appendix sec:ai-maturity-levels.
  - **Interactive Literature Map:**
    [Connected Papers: Glover et al. (2012)](https://www.connectedpapers.com/main/b5eabf01a3b701a4c7530a9476a141346f4bc8b4/Thinking-Structurally-About-Narcissism%3A-An-Examination-of-the-Five%20Factor-Narcissism-Inventory-and-Its-Components./graph).
  - **Dataset:** [`FFNI_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/ffni.csv).
  - **Embeddings File:** [`ffni_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/ffni_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/ffni.csv`](../../../datasets/ffni.csv) |
| Embeddings | [`Embeddings/ffni_embeddings.csv`](../../../Embeddings/ffni_embeddings.csv) |
| RF Model | [`models/ffni_rf_model.pkl`](../../../models/ffni_rf_model.pkl) |
| Label Encoder | [`models/ffni_label_encoder.pkl`](../../../models/ffni_label_encoder.pkl) |
| Graph (large) | [`graphs/ffni_large.png`](../../../graphs/ffni_large.png) |


## References

The following references are cited in this model card:

- `Ahmed2024CounselingNLP`
- `Campbell2011`
- `Glover2012`
- `Miller2013`
- `Miller2016`
- `Miller2016FFNI`
- `Oltmanns2018`
- `Scheidt2023`
- `Sherman2015`

See `references.bib` in the atlas root for full bibliographic entries.
