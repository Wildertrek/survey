# (36) Thomas-Kilmann Conflict Mode Instrument

**Abbreviation:** TKI
**Category:** Interpersonal and Conflict Resolution Models
**Model Number:** 36 of 44

[![TKI Model Diagram](tki_small.png)](../../../graphs/tki_large.png)

---

### Description.
The **Thomas-Kilmann Conflict Mode Instrument (TKI)**, developed by Kenneth W. Thomas and Ralph H. Kilmann in 1974 [ThomasKilmann1974TKI], identifies five distinct approaches to managing conflict: *Competing, Collaborating, Compromising, Avoiding,* and *Accommodating*.
Each reflects a unique balance between *assertiveness* (pursuit of one's own interests) and *cooperativeness* (consideration of others' interests).
The TKI is a foundational tool for organizational psychology and leadership development, emphasizing situational adaptability and self-awareness in conflict engagement [Jones1976Review, GrossGuerrero2000, Rahim1983, KilmannThomas1977].

### Dimensions, Examples, and Brain-Function Mapping.
Each conflict mode corresponds to characteristic decision and affective control processes, here aligned with levels of AI maturity from Appendix sec:ai-maturity-levels.

  - **Competing (Assertive, Uncooperative):**
  Pursues personal goals regardless of opposition.
  **Example (L2):** Reinforcement-learning agent maximizing individual reward in adversarial settings.
  *Maps to* Decision-Making Under Uncertainty & Competitive Strategy Modeling (L2).

  - **Collaborating (Assertive, Cooperative):**
  Seeks integrated, win-win outcomes.
  **Example (L3):** Multi-agent systems simulating shared intentionality and affective understanding.
  *Maps to* Social Cognition & Theory of Mind Simulation (L3).

  - **Compromising (Moderately Assertive, Moderately Cooperative):**
  Balances competing needs through partial concessions.
  **Example (L2):** Pareto-optimal trade-off optimization in multi-objective agents.
  *Maps to* Ambivalence Arbitration & Utility Balancing (L2).

  - **Avoiding (Unassertive, Uncooperative):**
  Withdraws from engagement to minimize perceived threat or cost.
  **Example (L2):** Inhibitory control mechanisms suppressing decision output in uncertain environments.
  *Maps to* Risk-Averse Response Inhibition & Attention Gating (L2).

  - **Accommodating (Unassertive, Cooperative):**
  Subordinates personal goals to maintain relational harmony.
  **Example (L3):** Emotion-aware agents modulating tone and decision framing to preserve trust.
  *Maps to* Empathy Modeling & Affective Alignment (L3).

### Applications.

  - **Organizational Development:** Diagnose and balance team conflict profiles to improve collaboration.
  - **Leadership Training:** Develop adaptive strategies for high-stakes negotiation and crisis mediation.
  - **Team Dynamics:** Support conflict coaching and constructive communication frameworks.
  - **AI Negotiation Systems:** Parameterize agent interaction styles to reflect human-like negotiation patterns.

### Timeline.

  - **1974:** Thomas and Kilmann publish the original TKI [ThomasKilmann1974TKI].
  - **1976-1977:** Empirical studies validate five-mode structure and psychometrics [Jones1976Review, KilmannThomas1977].
  - **1980s-1990s:** Adoption expands into corporate training and organizational consulting.
  - **2000s-Present:** Remains a core tool in leadership development, coaching, and mediation practice.

### Psychometrics.

  - **Reliability:** Internal consistency (Cronbach's  > 0.70 across modes) [KilmannThomas1977].
  - **Test-Retest:** Stability correlations between 0.61-0.68 over 2-3 weeks [ThomasKilmann1974TKI].
  - **Validity:** Factor analyses support five-mode model; concurrent validity with the Rahim Organizational Conflict Inventory [Rahim1983].
  - **Norming:** Established across diverse organizational samples [Jones1976Review].

### Data Structure.
Dataset `tki.csv` organizes each conflict mode into lexical and behavioral dimensions for embedding:

  - `Category`: Conflict Mode (five styles).
  - `Factor`: Mode name (Competing-Accommodating).
  - `Adjective`: Descriptive phrase of mode behavior.
  - `Synonym, Verb, Noun`: Lexical attributes used for semantic expansion.

Flattened schema: `Category, Factor, Adjective, Synonym, Verb, Noun, Embedding`.

### Resources.

  - **Primary Reference:** [ThomasKilmann1974TKI].
  - **Key Studies:** [Jones1976Review, GrossGuerrero2000, Rahim1983, KilmannThomas1977].
  - **Mapped Brain Functions Table:** Table tab:tki-mapping.
  - **AI Maturity Definitions:** Appendix sec:ai-maturity-levels.
  - **Connected Papers:** [TKI Graph](https://www.connectedpapers.com/main/bc42dd495b7ff7437ab9440b51d695a8fb148196/Thomas%20Kilmann-Conflict-Mode-Instrument/graph).
  - **Dataset:** [`TKI_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/tki.csv).
  - **Embeddings:** [`tki_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/tki_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/tki.csv`](../../../datasets/tki.csv) |
| Embeddings | [`Embeddings/tki_embeddings.csv`](../../../Embeddings/tki_embeddings.csv) |
| RF Model | [`models/tki_rf_model.pkl`](../../../models/tki_rf_model.pkl) |
| Label Encoder | [`models/tki_label_encoder.pkl`](../../../models/tki_label_encoder.pkl) |
| Graph (large) | [`graphs/tki_large.png`](../../../graphs/tki_large.png) |


## References

The following references are cited in this model card:

- `GrossGuerrero2000`
- `Jones1976Review`
- `KilmannThomas1977`
- `Rahim1983`
- `ThomasKilmann1974TKI`

See `references.bib` in the atlas root for full bibliographic entries.
