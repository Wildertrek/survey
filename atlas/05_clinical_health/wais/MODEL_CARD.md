# (38) Wechsler Adult Intelligence Scale

**Abbreviation:** WAIS
**Category:** Clinical and Psychological Health Models
**Model Number:** 38 of 44

[![WAIS Model Diagram](wais_small.png)](../../../graphs/wais_large.png)

---

### Description.
The **Wechsler Adult Intelligence Scale (WAIS)**, first introduced by David Wechsler in 1955 [Wechsler1955WAIS] and revised through WAIS-R (1981) [Wechsler1981WAISR], WAIS-III (1997) [Wechsler1997WAISIII], and WAIS-IV (2008) [Wechsler2008WAISIV], is the most widely used standardized test of adult intelligence.
It yields four index scores, *Verbal Comprehension, Perceptual Reasoning, Working Memory,* and *Processing Speed*, that together generate a Full-Scale IQ, reflecting both crystallized and fluid cognitive abilities.

### Dimensions, Examples, and Brain-Function Mapping.
> AI maturity mappings (L1–L3) follow the foundation-agent cognitive hierarchy of Liu et al. (2025).

  - **Verbal Comprehension Index (VCI).**
  Assesses verbal reasoning and concept formation.

    - **Similarities:** "How are a train and a bicycle alike?" → *Semantic comparison & abstraction* (L2).
    - **Vocabulary:** "Define 'benevolent.'" → *Lexical knowledge & concept representation* (L3).
    - **Information:** "What is the capital of France?" → *Knowledge recall & integration* (L2-L3).
    - **Comprehension:** "Why do people obey laws?" → *Pragmatic reasoning & social cognition* (L3).


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
    - **Letter-Number Sequencing:** Reorder mixed symbols → *Dual-task coordination & cognitive flexibility* (L3).


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

  - **1939:** Wechsler-Bellevue Intelligence Scale introduced [Wechsler1939WB].
  - **1955:** WAIS established standardized adult IQ testing [Wechsler1955WAIS].
  - **1981:** WAIS-R revision improves norms and item structure [Wechsler1981WAISR].
  - **1997:** WAIS-III introduces Working Memory and Processing Speed [Wechsler1997WAISIII].
  - **2008:** WAIS-IV refines index scales and psychometrics [Wechsler2008WAISIV].
  - **2020s:** Digital WAIS-V under development, adaptive testing, global norms, AI scoring integration.

### Psychometrics.

  - **Reliability:** Subtests show high internal consistency ( > 0.90) and test-retest stability (r > 0.85) [Wechsler2008WAISIV].
  - **Validity:** Strong evidence for four-factor model (VCI, PRI, WMI, PSI); excellent construct and criterion validity [Pearson2012WAISValidity].
  - **Norming:** WAIS-IV normed on 2,200 U.S. adults (ages 16-90) stratified by education, gender, and ethnicity [Wechsler2008WAISIV].
  - **Clinical Utility:** Central to diagnostics in neuropsychology, forensic assessment, and cognitive rehabilitation.

### Data Structure.
Dataset `wais.csv` defines:

  - `Factor` ,  Primary ability index (VCI, PRI, WMI, PSI).
  - `Adjective` ,  Specific cognitive subtest.
  - `Description` ,  Subtest definition.
  - `Synonym, Verb, Noun` ,  Lexical fields for embeddings.

### Resources.

  - **Primary Sources:** [Wechsler1955WAIS, Wechsler1981WAISR, Wechsler1997WAISIII, Wechsler2008WAISIV].
  - **Connected Papers:** [WAIS Graph](https://www.connectedpapers.com/main/a520a3464986d22e56025474b92be3aad7b71cf5/Wechsler-Adult-Intelligence-Scale%E2%80%93Fourth-Edition/graph).
  - **Dataset:** [`WAIS_Dataset.csv`](https://github.com/Wildertrek/survey/blob/main/datasets/wais.csv).
  - **Embeddings:** [`wais_embeddings.csv`](https://github.com/Wildertrek/survey/blob/main/Embeddings/wais_embeddings.csv).

---

## Atlas Resources

| Resource | Location |
|----------|----------|
| Dataset | [`datasets/wais.csv`](../../../datasets/wais.csv) |
| Embeddings | [`Embeddings/wais_embeddings.csv`](../../../Embeddings/wais_embeddings.csv) |
| RF Model | [`models/wais_rf_model.pkl`](../../../models/wais_rf_model.pkl) |
| Label Encoder | [`models/wais_label_encoder.pkl`](../../../models/wais_label_encoder.pkl) |
| Graph (large) | [`graphs/wais_large.png`](../../../graphs/wais_large.png) |


---

## Validation Results

> From: Raetano, Gregor, & Tamang (2026). "A Survey and Computational Atlas of Personality Models." Under review, ACM TIST.

**Status:** Validated. WAIS measures cognitive ability rather than personality traits, so its factors are semantically more distant from the personality-oriented embedding space. Despite this, the RF classifier achieves above-chance accuracy.

| Metric | Value |
|--------|-------|
| Factors | 4 |
| Test Items Generated | 57 |
| RF Accuracy | 45.6% |
| F1 (macro) | 0.422 |
| Random Baseline | 25.0% |
| Lift over Random | +20.6% |
| Performance Tier | Moderate |
| Best Factor | VCI (F1 = 0.692) |
| Worst Factor | WMI (F1 = 0.190) |

**Note:** WAIS is included in the atlas as a clinical instrument. Its moderate accuracy (45.6%) is well above the 25% random baseline for 4 factors, demonstrating that even cognitive ability constructs produce partially discriminable embeddings in the atlas's lexical schema.

### Experiment 2: Model Improvement

| Intervention | Accuracy | Delta |
|-------------|----------|-------|
| Exp1 baseline (1536-dim) | 45.6% | — |
| RQ9: 3072-dim embeddings | 45.6% | +0.0% |
| RQ7: Data augmentation | 87.7% | +42.1% |
| **Best result** | **87.7%** | **+42.1%** |

Best intervention: Data augmentation (55 LLM-generated items).

## References

The following references are cited in this model card:

- `Pearson2012WAISValidity`
- `Wechsler1939WB`
- `Wechsler1955WAIS`
- `Wechsler1981WAISR`
- `Wechsler1997WAISIII`
- `Wechsler2008WAISIV`

See `references.bib` in the atlas root for full bibliographic entries.
