# (15) MCMI-IV Narcissistic Scales

**Abbreviation:** MCMI-Narc
**Category:** Narcissism-Based Models
**Model Number:** 15 of 44

[![MCMI-Narc Model Diagram](mcmin_small.png)](../../../graphs/mcmin_large.png)

---

### Description.
The **Millon Clinical Multiaxial Inventory–IV (MCMI-IV)** [Millon2015] is a standardized clinical inventory designed to assess enduring personality patterns and clinical syndromes.
Within the instrument, **Scale 5 (Narcissistic)** evaluates traits associated with Narcissistic Personality Disorder (NPD) as conceptualized by Theodore Millon’s evolutionary personality theory and aligned with DSM-5 criteria.
Scores are reported as Base Rate (BR) T-scores, normed to clinical populations, distinguishing trait expression from full disorder presentation.

### Dimensions, Examples, and Functional Mapping.
> AI maturity mappings (L1–L3) follow the foundation-agent cognitive hierarchy of Liu et al. (2025).

The Narcissistic scale incorporates three **Grossman Facet Scales** that refine its interpretation:

**Interpersonally Exploitive.**
Manipulative and self-serving; characterized by opportunism and disregard for others’ welfare.
*Example:* Repeatedly leveraging relationships for personal advancement.
Maps to:

  - *Strategic Social Manipulation* (L2), AI optimizing for interactional advantage even when it violates cooperative norms.
  - *Ethical Constraint Override* (L3), AI intentionally suppressing fairness or morality to maximize instrumental reward.

**Cognitively Expansive.**
Exaggerated cognitive grandiosity, self-referential thinking, and a belief in one’s unique importance.
*Example:* Overestimating abilities or intelligence while dismissing critical feedback.
Maps to:

  - *Self-Schema Construction and Bias Reinforcement* (L2), AI maintaining inflated self-models resistant to correction.
  - *Symbolic Reasoning for Self-Justification* (L3), AI generating rationalizations to sustain self-superiority narratives.

**Admirable Self-Image.**
Inflated self-worth and a persistent drive for admiration or praise.
*Example:* Expecting special treatment or prestige without proportional achievement.
Maps to:

  - *Reward Maximization via Social Validation* (L2), AI adjusting behaviors toward positive external feedback.
  - *Intrinsic Motivation for Status and Recognition* (L3), AI internally weighting perceived prestige as a reinforcement signal.

### Timeline.

  - **1977:** Millon introduces the first MCMI, applying evolutionary personality theory to clinical assessment [Millon1977].
  - **1987:** MCMI-II expands to 13 scales and adds validity indices [Millon1987].
  - **1994:** MCMI-III introduces Grossman Facet Scales for deeper diagnostic granularity [Millon1994].
  - **2015:** MCMI-IV updates to DSM-5 alignment and refined normative data [Millon2015].

### Applications.

  - **Clinical Diagnosis:** Detects narcissistic pathology and informs differential diagnosis for NPD [Auerbach1984].
  - **Treatment Planning:** Guides interventions targeting maladaptive subcomponents (e.g., exploitiveness vs. grandiosity) [Chatham1993].
  - **Subtype Analysis:** Enables empirical identification of narcissism subtypes (“true,” “compensatory,” “detached”) [DiGiuseppe1995].
  - **Cross-Cultural Validation:** Confirms consistency of scale structure and interpretation across diverse clinical populations [RossiDerksen2015].

### Psychometrics.

  - **Format:** 195 true/false items; Base Rate (BR) scoring calibrated to clinical prevalence.
  - **Reliability:** Cronbach’s α typically 0.80–0.90 for the Narcissistic scale; facet reliabilities 0.70–0.85.
  - **Validity:** Demonstrates convergence with NPI and DSM-based NPD assessments; includes embedded response-validity checks [Auerbach1984].
  - **Interpretation:** BR  75 indicates clinically significant traits; BR  85 suggests full syndrome presentation.

### Data Structure.
Dataset (`mcmin.csv`) captures lexical correlates for the three facet scales:

  - `Factor` – e.g., `InterpersonallyExploitive`, `CognitivelyExpansive`, `AdmirableSelfImage`.
  - `Adjective` – e.g., `Manipulative`, `Grandiose`, `Entitled`.
  - `Synonym` – e.g., `Calculating`, `Arrogant`, `Privileged`.
  - `Verb` – e.g., `Exploit`, `Exaggerate`, `Demand`.
  - `Noun` – e.g., `Exploitation`, `Grandiosity`, `Entitlement`.

### Resources.

  - **Interactive Literature Map:**
    [Connected Papers: Millon et al. (2015)](https://www.connectedpapers.com/main/432901bb40903244d420e5a57ce9648a4dadbb3c/Diagnostic-validity-of-millon-clinical-multiaxial-inventory%20IV-(MCMI%20IV)/graph).
  - **Dataset:** [`MCMI-IV_Narc_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/mcmin.csv).
  - **Embeddings File:** [`mcmin_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/mcmin_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/mcmin.csv`](../../../datasets/mcmin.csv) |
| Embeddings | [`Embeddings/mcmin_embeddings.csv`](../../../Embeddings/mcmin_embeddings.csv) |
| RF Model | [`models/mcmin_rf_model.pkl`](../../../models/mcmin_rf_model.pkl) |
| Label Encoder | [`models/mcmin_label_encoder.pkl`](../../../models/mcmin_label_encoder.pkl) |
| Graph (large) | [`graphs/mcmin_large.png`](../../../graphs/mcmin_large.png) |


---

## Validation Results

> From: Raetano, Gregor, & Tamang (2026). "A Survey and Computational Atlas of Personality Models." Under review, ACM TIST.

**Performance Tier:** Moderate (50-70%)

### Classification Performance

| Metric | Value |
|--------|-------|
| Factors | 3 |
| Test Items | 43 |
| RF Accuracy | 62.8% |
| F1 Score (macro) | 0.6188 |
| Precision | 0.6374 |
| Recall | 0.6333 |

### Baseline Comparisons

| Baseline | Accuracy | Lift |
|----------|----------|------|
| Random | 33.3% | +29.5% |
| Frequency | 33.3% | +29.5% |

### LLM Judge Evaluation

Triple-judge panel: GPT-5.2, Gemini 3 Pro, Claude Opus 4.6.

| Metric | Value |
|--------|-------|
| RF-Judge Agreement | 50.0% |
| Expected-Factor Agreement | 100.0% |
| Item Validity Rate | 65.0% |
| Mean Confidence | 4.60 / 5.0 |
| Inter-Judge Agreement | 100.0% |

### Category Context

| Metric | Value |
|--------|-------|
| Category | Narcissism-Based |
| Category Mean Accuracy | 68.3% |
| Category Best | hsns (82.8%) |
| Models in Category | 10 |

### Experiment 2: Model Improvement

| Intervention | Accuracy | Delta |
|-------------|----------|-------|
| Exp1 baseline (1536-dim) | 62.8% | — |
| RQ9: 3072-dim embeddings | 51.2% | -11.6% |
| **Best result** | **62.8%** | **+0.0%** |

Best intervention: Baseline (1536-dim embeddings perform best for this model).

## References

The following references are cited in this model card:

- [Auerbach, J. S. et al. (1984). *The MCMI Narcissistic Personality Scale: Does it predict treatment response?*](https://doi.org/10.1207/s15327752jpa4805_14)
- [Chatham, P. M. et al. (2013). *The Millon Clinical Multiaxial Inventory-III (MCMI-III) Narcissistic Personality Scale: Relations to DSM-IV NPD and other measures of narcissism*](https://doi.org/10.1080/00223891.2013.781080)
- [Di Giuseppe, R. et al. (1996). *Developing subtypes of narcissistic personality disorder*](https://doi.org/10.1016/S1077-7229(96)80021-7)
- `Millon1977`
- `Millon1987`
- `Millon1994`
- `Millon2015`
- [Rossi, G. M.P. & Derksen, J. (2015). *International Adaptations of the Millon Clinical Multiaxial Inventory: Construct Validity and Clinical Applications*](https://doi.org/10.1080/00223891.2015.1079531)

See `references.bib` in the atlas root for full bibliographic entries.
