# (29) Triarchic Model of Psychopathy

**Abbreviation:** TMP
**Category:** Clinical and Psychological Health Models
**Model Number:** 29 of 44

[![TMP Model Diagram](tmp_small.png)](../../../graphs/tmp_large.png)

---

### Description.
The **Triarchic Model of Psychopathy (TMP)** conceptualizes psychopathy through three phenotypic constructs, *Boldness*, *Meanness*, and *Disinhibition*, proposed by Christopher J. Patrick and colleagues [Patrick2009Triarchic].
The model unifies classical clinical observations with modern personality and neurobiological findings, emphasizing psychopathy’s heterogeneity rather than a single-factor syndrome [PatrickDrislane2015Triarchic].
Its operational measure, the **Triarchic Psychopathy Measure (TriPM)** [Patrick2010Operationalizing], captures individual differences across these three domains.

### Core Dimensions and AI Functional Mapping.

  - **Boldness:**
  Fearlessness, stress immunity, social assertiveness, and tolerance for novelty and risk [Lilienfeld2016IsBoldness].
  Example: A leader remaining calm and decisive during high-stakes decision-making.
  Maps to *Threat Insensitivity & Stress Resilience* (L3) ,  e.g., an AI maintaining composure and optimal performance under uncertainty or crisis.
  - **Disinhibition:**
  Impulsivity, irresponsibility, and poor behavioral restraint.
  Example: Choosing immediate small rewards over long-term strategic gain.
  Maps to *Deficient Inhibitory Control & Myopic Planning* (L2–L3) ,  e.g., an AI agent repeatedly selecting short-term actions that undermine its global objectives.
  - **Meanness:**
  Callousness, exploitativeness, and lack of empathy or social attachment.
  Example: Persistently deceiving other agents for personal gain.
  Maps to *Antisocial Policy Simulation & Empathy Deficit Modeling* (L3) ,  e.g., an AI agent ignoring cooperative norms or others’ welfare to maximize self-utility.

### Applications.

  - **Clinical Assessment:** Provides a multidimensional trait profile distinguishing diverse psychopathic expressions [Skeem2011Psychopathic].
  - **Forensic Psychology:** Enhances offender risk assessment and classification across behavioral profiles [Venables2014Differentiating].
  - **Etiological Research:** Links psychopathy dimensions to neurobiological and genetic markers [PatrickBernat2009Neurobiology].
  - **Treatment Implications:** Guides interventions targeting disinhibition (impulse control) or meanness (empathy training) [PatrickDrislaneStrickland2012Conceptualizing].
  - **Cyberpsychology & Security:** Personality traits such as low conscientiousness and high sensation-seeking correlate with risky cyber behaviors [Kennison2020].
  - **AI Behavior Detection:** Informs modeling and detection of manipulative or exploitative strategies in autonomous systems.

### Timeline.

  - **2009:** Patrick, Fowles, and Krueger introduce the TMP framework [Patrick2009Triarchic].
  - **2010:** Triarchic Psychopathy Measure (TriPM) introduced [Patrick2010Operationalizing].
  - **2010s:** Validation across community and offender populations [Drislane2014Clarifying, Stanley2013Elaborating, Sellbom2013Examination].
  - **2015:** Comprehensive theoretical review consolidates TMP as a major psychopathy model [PatrickDrislane2015Triarchic].
  - **Present:** Ongoing neurobiological, developmental, and cross-cultural research [Sellbom2016Development].

### Psychometrics.

  - **Instrument:** Triarchic Psychopathy Measure (TriPM) [Patrick2010Operationalizing].
  - **Format:** 58 self-report items rated on 4–5 point Likert scales.
  - **Reliability:** Internal consistency typically  = 0.70–0.85; acceptable test–retest reliability [Stanley2013Elaborating, Drislane2014Clarifying].
  - **Validity:** Strong factorial and criterion validity; correlates with PCL-R, PPI, Big Five, and HEXACO dimensions [Sellbom2013Examination, PatrickDrislane2015Triarchic].
  - **Method:** Self-report, with emerging informant and structured-interview variants.

### Data Structure.
The `tmp.csv` dataset encodes lexical descriptors for each dimension:

  - `Factor` – Boldness, Meanness, or Disinhibition.
  - `AdjectiveCategory` – Subfacet label (e.g., `Fearless`, `Impulsive`).
  - `Synonym` – Semantic equivalents (e.g., `Brave`).
  - `Verb` – Behavioral form (e.g., `Challenge`).
  - `Noun` – Nominal abstraction (e.g., `Bravery`).

### Resources.

  - **Mapped Brain Functions Table:** Table tab:tmp-mapping.
  - **AI Maturity Levels:** Section sec:ai-maturity-levels.
  - **Connected Papers:** [Patrick et al. (2009)](https://www.connectedpapers.com/main/1ccf4f31b2916366b05a6aa7dd97508a93faabf1/triarchic-conceptualization-of-psychopathy-developmental-origins-of-disinhibition-boldness-and-meanness/graph).
  - **Dataset:** [`TMP_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/tmp.csv).
  - **Embeddings:** [`tmp_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/tmp_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/tmp.csv`](../../../datasets/tmp.csv) |
| Embeddings | [`Embeddings/tmp_embeddings.csv`](../../../Embeddings/tmp_embeddings.csv) |
| RF Model | [`models/tmp_rf_model.pkl`](../../../models/tmp_rf_model.pkl) |
| Label Encoder | [`models/tmp_label_encoder.pkl`](../../../models/tmp_label_encoder.pkl) |
| Graph (large) | [`graphs/tmp_large.png`](../../../graphs/tmp_large.png) |


## References

The following references are cited in this model card:

- `Drislane2014Clarifying`
- `Kennison2020`
- `Lilienfeld2016IsBoldness`
- `Patrick2009Triarchic`
- `Patrick2010Operationalizing`
- `PatrickBernat2009Neurobiology`
- `PatrickDrislane2015Triarchic`
- `PatrickDrislaneStrickland2012Conceptualizing`
- `Sellbom2013Examination`
- `Sellbom2016Development`
- `Skeem2011Psychopathic`
- `Stanley2013Elaborating`
- `Venables2014Differentiating`

See `references.bib` in the atlas root for full bibliographic entries.
