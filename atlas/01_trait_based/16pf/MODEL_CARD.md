# (5) Sixteen Personality Factors

**Abbreviation:** 16PF
**Category:** Trait-Based Models
**Model Number:** 5 of 44

[![16PF Model Diagram](16PF_small.png)](../../../graphs/16PF_large.png)

---

### Description.
Developed by Raymond B. Cattell, the Sixteen Personality Factor Questionnaire (**16PF**) provides a multidimensional measure of normal-range personality.
Cattell used factor analysis of large lexical datasets and behavioral observations to identify sixteen primary *source traits*, which can be grouped into higher-order global dimensions [Cattell1949, Cattell1956, Cattell1963].
The 16PF remains one of the most empirically grounded models in differential psychology, bridging lexical, behavioral, and psychometric traditions.

### Dimensions, Examples, and Functional Mapping.
> AI maturity mappings (L1–L3) follow the foundation-agent cognitive hierarchy of Liu et al. (2025).

Each of the sixteen factors represents a continuum of personality attributes with potential analogs in AI cognition and system behavior:

  - **Warmth (A):** Outgoing, participative, attentive.
    *Example:* Welcoming new colleagues with enthusiasm.
    Maps to *Social Cognition and Interaction*, AI inferring affective states and generating empathic dialogue (L2–L3).
  - **Reasoning (B):** Abstract, quick learner.
    *Example:* Rapidly understanding complex logical relationships.
    Maps to *Abstract Reasoning and Problem Solving*, symbolic or relational inference (L2–L3).
  - **Emotional Stability (C):** Calm, adaptive, resilient.
    *Example:* Maintaining composure under stress.
    Maps to *Affect Regulation and Resilience*, AI stabilizing outputs or confidence under uncertainty (L2–L3).
  - **Dominance (E):** Assertive, decisive, forceful.
    *Example:* Volunteering to lead a project.
    Maps to *Goal-Directed Planning and Assertiveness*, AI prioritizing among competing subgoals (L2–L3).
  - **Liveliness (F):** Enthusiastic, expressive, spontaneous.
    *Example:* Injecting humor into group interactions.
    Maps to *Behavioral Activation and Exploration*, AI managing novelty vs. exploitation (L1–L2).
  - **Rule-Consciousness (G):** Conforming, disciplined, ethical.
    *Example:* Adhering to governance and compliance rules.
    Maps to *Norm Adherence and Policy Enforcement*, AI executing rule-based constraints (L2–L3).
  - **Social Boldness (H):** Daring, uninhibited, adventurous.
    *Example:* Initiating conversation with unfamiliar peers.
    Maps to *Risk Tolerance and Social Engagement*, AI sustaining exploration despite feedback uncertainty (L2–L3).
  - **Sensitivity (I):** Intuitive, tender-minded, empathic.
    *Example:* Being emotionally moved by others’ stories.
    Maps to *Affective Sensitivity and Empathy*, AI interpreting subtle emotional cues (L2–L3).
  - **Vigilance (L):** Skeptical, critical, questioning.
    *Example:* Double-checking details before acceptance.
    Maps to *Anomaly Detection and Verification*, AI identifying inconsistencies or adversarial inputs (L2–L3).
  - **Abstractedness (M):** Imaginative, idealistic, unconventional.
    *Example:* Daydreaming about innovative solutions.
    Maps to *Conceptual Creativity and Ideation*, AI producing novel conceptual combinations (L3).
  - **Privateness (N):** Reserved, discreet, self-contained.
    *Example:* Preferring privacy before disclosure.
    Maps to *Self-Disclosure Management and Simulation*, AI deciding what internal state to externalize (L2–L3).
  - **Apprehension (O):** Insecure, self-critical, guilt-prone.
    *Example:* Overanalyzing potential mistakes.
    Maps to *Uncertainty Monitoring and Self-Correction*, AI adjusting output confidence dynamically (L2–L3).
  - **Openness to Change (Q1):** Analytical, experimental, non-traditional.
    *Example:* Adopting new technologies rapidly.
    Maps to *Adaptive Learning and Flexibility*, AI updating world models in response to new inputs (L2–L3).
  - **Self-Reliance (Q2):** Independent, self-sufficient.
    *Example:* Preferring autonomous problem solving.
    Maps to *Autonomous Goal Pursuit*, AI sustaining motivation via intrinsic reward systems (L2–L3).
  - **Perfectionism (Q3):** Organized, precise, disciplined.
    *Example:* Iteratively refining work until flawless.
    Maps to *Quality Control and Iterative Improvement*, AI refining internal models via error feedback (L2–L3).
  - **Tension (Q4):** Driven, impatient, restless.
    *Example:* Feeling uneasy when idle.
    Maps to *Arousal and Drive Regulation*, AI modulating activation levels or prediction-error energy (L1–L3).

### Timeline.

  - **1949:** Cattell identifies primary source traits via large-scale factor analysis [Cattell1949].
  - **1956–1957:** First 16PF Questionnaire released by the Institute for Personality and Ability Testing (IPAT) [Cattell1956].
  - **1963:** Third-edition *Handbook for the 16PF* published [Cattell1963].
  - **1993:** Fifth Edition introduces updated norms and psychometrics [Cattell1993].
  - **Present:** Continuous cross-cultural validation and digital adaptation in applied contexts.

### Applications.

  - **Personnel Selection and Leadership Development:** Core predictors of job performance, leadership, and teamwork [Salgado1997FFMJobPerformance, Judge2002PersonalityJobSatisfaction].
  - **Career Counseling and Guidance:** Aligns occupational paths with reasoning (B) and warmth (A) profiles [Carson1998, Conn1994].
  - **Educational Psychology:** Tailors instruction to learning styles using Abstractedness (M) and Rule-Consciousness (G) [CattellKrug1986, CattellEber1995].
  - **Clinical Assessment:** Extends to normal-range personality diagnostics; factors C and O correlate with adjustment [BahnerClark2020_16PF].
  - **AI-Driven Talent Analytics:** Modern HR systems leverage 16PF-analogous embeddings to match candidates with organizational culture [Winsor2025, Testlify2024].

### Psychometrics.

  - **Format:** Forced-choice self-report; results standardized to *sten* (1–10) scores.
  - **Reliability:** Internal consistency  = 0.70–0.85 across primary factors; strong test-retest stability.
  - **Validity:** Robust construct and criterion validity across occupational and cross-cultural samples.
  - **Method:** Derived via multi-method data integration (questionnaires, life records, observer ratings).

### Data Structure.
Each dataset row (e.g., `sixteenpf.csv`) encodes lexical representations of primary traits:

  - `Factor` – Primary factor (e.g., `Warmth`, `Reasoning`)
  - `Adjective` – Descriptive term (e.g., `Affectionate`)
  - `Synonym` – Near equivalent (e.g., `Kindly`)
  - `Verb` – Behavioral form (e.g., `Empathize`)
  - `Noun` – Abstract representation (e.g., `Empathy`)

### Resources.

  - **Interactive Literature Map:** [Connected Papers: Cattell & Krug (1986)](https://www.connectedpapers.com/main/1d34d0a7db285927d8e612e926655a9b236f57f1/The-Number-of-Factors-in-the-16PF%3A-A-Review-of-the-Evidence-with-Special-Emphasis-on-Methodological-Problems/graph).
  - **Dataset:** [`16PF_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/sixteenpf.csv).
  - **Embeddings File:** [`16PF_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/sixteenpf_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/sixteenpf.csv`](../../../datasets/sixteenpf.csv) |
| Embeddings | [`Embeddings/sixteenpf_embeddings.csv`](../../../Embeddings/sixteenpf_embeddings.csv) |
| RF Model | [`models/sixteenpf_rf_model.pkl`](../../../models/sixteenpf_rf_model.pkl) |
| Label Encoder | [`models/sixteenpf_label_encoder.pkl`](../../../models/sixteenpf_label_encoder.pkl) |
| Graph (large) | [`graphs/16PF_large.png`](../../../graphs/16PF_large.png) |


---

## Validation Results

> From: Raetano, Gregor, & Tamang (2026). "A Survey and Computational Atlas of Personality Models." Under review, ACM TIST.

**Performance Tier:** Moderate (50-70%)

### Classification Performance

| Metric | Value |
|--------|-------|
| Factors | 16 |
| Test Items | 225 |
| RF Accuracy | 50.7% |
| F1 Score (macro) | 0.4944 |
| Precision | 0.5498 |
| Recall | 0.5068 |

### Baseline Comparisons

| Baseline | Accuracy | Lift |
|----------|----------|------|
| Random | 6.2% | +44.4% |
| Frequency | 6.2% | +44.4% |

### LLM Judge Evaluation

Triple-judge panel: GPT-5.2, Gemini 3 Pro, Claude Opus 4.6.

| Metric | Value |
|--------|-------|
| RF-Judge Agreement | 50.0% |
| Expected-Factor Agreement | 100.0% |
| Item Validity Rate | 55.0% |
| Mean Confidence | 4.75 / 5.0 |
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

- [Bahner, C. A. & Clark, C. B. (2020). *Sixteen Personality Factor Questionnaire (16PF)*](https://doi.org/10.1007/978-3-319-28099-8_86-1)
- `Carson1998`
- [Cattell, R. B. (1949). *The description of personality: Basic traits resolved into clusters*](https://doi.org/10.1037/h0060010)
- `Cattell1956`
- `Cattell1963`
- `Cattell1993`
- `CattellEber1995`
- [Cattell, R. B. & Krug, S. E. (1986). *The number of factors in the 16PF: A review of the evidence with special emphasis on methodological problems*](https://doi.org/10.1177/0013164486463006)
- `Conn1994`
- [Judge, T. A. et al. (2002). *Personality and Job Satisfaction: The Role of the Five-Factor Model*](https://doi.org/10.1037/0021-9010.87.3.530)
- [Salgado, J. F. (1997). *The Five Factor Model of Personality and Job Performance in the European Community*](https://doi.org/10.1037/0021-9010.82.1.30)
- [Testlify (2024). *AI-Powered skills and personality assessment*](https://testlify.com/)
- [Winsor, J. (2025). *AI-Driven Talent Acquisition: Transforming How We Find and Screen Talent*](https://www.forbes.com/sites/johnwinsor/2025/02/24/ai-driven-talent-acquisition-transforming-how-we-find-and-screen-talent/)

See `references.bib` in the atlas root for full bibliographic entries.
