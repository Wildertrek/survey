# (36) Thomas-Kilmann Conflict Mode Instrument

**Abbreviation:** TKI
**Category:** Interpersonal and Conflict Resolution Models
**Model Number:** 36 of 44

[![TKI Model Diagram](tki_small.png)](../../../graphs/tki_large.png)

---

### Description.
The **Wechsler Adult Intelligence Scale (WAIS)**, first introduced by David Wechsler in 1955 [Wechsler1955WAIS] and revised through WAIS-R (1981) [Wechsler1981WAISR], WAIS-III (1997) [Wechsler1997WAISIII], and WAIS-IV (2008) [Wechsler2008WAISIV], is the most widely used standardized test of adult intelligence.
It yields four index scores, *Verbal Comprehension, Perceptual Reasoning, Working Memory,* and *Processing Speed*, that together generate a Full-Scale IQ, reflecting both crystallized and fluid cognitive abilities.

### Dimensions, Examples, and Brain-Function Mapping.

  - **Verbal Comprehension Index (VCI).**
  Assesses verbal reasoning and concept formation.

    - **Similarities:** “How are a train and a bicycle alike?” → *Semantic comparison & abstraction* (L2).
    - **Vocabulary:** “Define ‘benevolent.’” → *Lexical knowledge & concept representation* (L3).
    - **Information:** “What is the capital of France?” → *Knowledge recall & integration* (L2–L3).
    - **Comprehension:** “Why do people obey laws?” → *Pragmatic reasoning & social cognition* (L3).


  - **Perceptual Reasoning Index (PRI).**
  Evaluates nonverbal problem solving and spatial reasoning.

    - **Block Design:** Reproduce a pattern with blocks → *Spatial assembly & visual-motor coordination* (L2).
    - **Matrix Reasoning:** Identify the missing piece in a matrix → *Pattern inference & analogical reasoning* (L3).
    - **Visual Puzzles:** Solve jigsaw-type problems → *Mental rotation & spatial manipulation* (L2).
    - **Figure Weights:** Balance scales using weight inference → *Quantitative reasoning & analogy* (L3).


  - **Working Memory Index (WMI).**
  Measures short-term storage and cognitive manipulation.

    - **Digit Span:** Repeat sequences forward/backward → *Sequential encoding & attention control* (L2).
    - **Arithmetic:** Mental problem solving → *Numerical reasoning & sustained concentration* (L3).
    - **Letter–Number Sequencing:** Reorder mixed symbols → *Dual-task coordination & cognitive flexibility* (L3).


  - **Processing Speed Index (PSI).**
  Tests rapid scanning, matching, and psychomotor efficiency.

    - **Symbol Search:** Find target symbols → *Perceptual speed & pattern recognition* (L2).
    - **Coding:** Match numbers to symbols → *Processing fluency & graphomotor speed* (L2).
    - **Cancellation:** Mark specified targets → *Selective attention & visual search* (L3).


### Applications.

  - **Clinical Assessment:** Gold-standard tool for diagnosing intellectual disability, cognitive decline, and neuropsychological disorders.
  - **Cognitive Modeling:** Informs architectures simulating working memory, reasoning, and executive functions.
  - **Adaptive Testing:** Foundation for AI-driven item selection in computerized intelligence tests.
  - **Educational AI:** Enables personalized learning paths based on cognitive index profiles.
  - **Neuroscience Research:** Links index scores with functional neuroimaging of cognitive domains.

### Timeline.

  - **1939:** Wechsler–Bellevue Intelligence Scale introduced [Wechsler1939WB].
  - **1955:** WAIS established standardized adult IQ testing [Wechsler1955WAIS].
  - **1981:** WAIS-R revision improves norms and item structure [Wechsler1981WAISR].
  - **1997:** WAIS-III introduces Working Memory and Processing Speed [Wechsler1997WAISIII].
  - **2008:** WAIS-IV refines index scales and psychometrics [Wechsler2008WAISIV].
  - **2020s:** Digital WAIS-V under development, adaptive testing, global norms, AI scoring integration.

### Psychometrics.

  - **Reliability:** Subtests show high internal consistency ( > 0.90) and test–retest stability (r > 0.85) [Wechsler2008WAISIV].
  - **Validity:** Strong evidence for four-factor model (VCI, PRI, WMI, PSI); excellent construct and criterion validity [Pearson2012WAISValidity].
  - **Norming:** WAIS-IV normed on 2,200 U.S. adults (ages 16–90) stratified by education, gender, and ethnicity [Wechsler2008WAISIV].
  - **Clinical Utility:** Central to diagnostics in neuropsychology, forensic assessment, and cognitive rehabilitation.

### Data Structure.
Dataset `wais.csv` defines:

  - `Index` ,  Primary ability (VCI, PRI, WMI, PSI).
  - `Subtest` ,  Specific cognitive task.
  - `Description` ,  Subtest definition.
  - `Synonym, Verb, Noun` ,  Lexical fields for embeddings.

### Resources.

  - **Primary Sources:** [Wechsler1955WAIS, Wechsler1981WAISR, Wechsler1997WAISIII, Wechsler2008WAISIV].
  - **Mapped Brain Functions Table:** Table tab:wais-mapping.
  - **AI Maturity Levels:** Appendix sec:ai-maturity-levels.
  - **Connected Papers:** [WAIS Graph](https://www.connectedpapers.com/main/a520a3464986d22e56025474b92be3aad7b71cf5/Wechsler-Adult-Intelligence-Scale%E2%80%93Fourth-Edition/graph).
  - **Dataset:** [`WAIS_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/wais.csv).
  - **Embeddings:** [`wais_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/wais_embeddings.csv).

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

- `Pearson2012WAISValidity`
- `Wechsler1939WB`
- `Wechsler1955WAIS`
- `Wechsler1981WAISR`
- `Wechsler1997WAISIII`
- `Wechsler2008WAISIV`

See `references.bib` in the atlas root for full bibliographic entries.
