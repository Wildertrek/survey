# How the Atlas Was Built

This document covers the origin and construction of the Personality Atlas.

---

## The question that started it

This project started in April 2023 with a simpler question than you might expect: how many personality models are there?

I knew about the Big Five. I knew about the MMPI. I started digging and found 6, then 12, then 22, and eventually capped it at 44. I am sure there are more out there, and one of the things I hope this paper does is surface them — and help refine these models further with feedback from other researchers who know traditions I have not reached yet.

## Seven categories emerged

As the collection grew, patterns started to emerge. The models were not all doing the same thing — some measured normal-range traits, some mapped clinical disorders, some focused specifically on narcissism or motivation or how people interact. That is where the seven categories came from:

| # | Category | Models | Example |
|---|----------|--------|---------|
| 1 | Trait-Based | 6 | OCEAN, HEXACO, MBTI |
| 2 | Narcissism | 10 | Dark Triad, FFNI, NPI |
| 3 | Motivational | 6 | SDT, Schwartz Values, CliftonStrengths |
| 4 | Cognitive | 4 | CEST, Felder-Silverman |
| 5 | Clinical | 10 | MMPI, SCID, BDI, GAD-7 |
| 6 | Interpersonal | 2 | TKI, DISC |
| 7 | Applied | 6 | Enneagram, RIASEC, Bartle Types |

The taxonomy was not imposed from the top down. It emerged from the models themselves as I kept finding more of them. You can see it reflected in the folder structure under [`atlas/`](atlas/).

## The factor chain

The trait-based models came first — the Big Five, HEXACO, MBTI. Through those I started analyzing how traits were used across models: what words defined each factor, how different instruments carved up the same personality space.

That analysis led to a normalization. Every model, no matter how different its theoretical origins, ultimately describes **factors**, and every factor is defined by **trait vocabulary**. I started calling this the factor chain — the repeating pattern that connects a theoretical construct to the words that measure it. Once every model follows the same pattern, you can compare them and normalize them into a single index.

## The five-column schema

The early datasets had just two columns: Factor and Adjective. But a single adjective was not enough. "Warm" could be a personality trait or a temperature. So we expanded — first adding Synonyms to disambiguate, then Verbs and Nouns to get full lexical coverage of what each factor actually describes.

| Factor | Adjective | Synonym | Verb | Noun |
|--------|-----------|---------|------|------|
| Extraversion | Active | Energetic | Activate | Activator |
| Neuroticism | Anxious | Worried | Fret | Anxiety |
| Agreeableness | Warm | Caring | Nurture | Nurturer |

"Warm, caring, nurtures, nurturer" gives the embedding model enough context to land in the right region of semantic space. We standardized on that five-column pattern and carried it through every model from that point on. That consistency is what makes cross-model comparison possible — every trait, from every tradition, encoded the same way.

The idea draws from the psycholexical tradition — the hypothesis that personality differences get encoded in natural language. If a distinction matters to people, there will be words for it. The schema extends that insight to computation: we use lexical markers to encode known factors in a format that embedding models can consume.

## Scale

This encoding had to be done for every factor of every model:

- OCEAN has 5 factors
- HEXACO has 6
- The MMPI has 10 clinical scales
- The SCID has 21 DSM-based categories
- The FFNI has 15 narcissism facets

44 models. 358 factors. 6,694 individual trait entries. That work took about 13 months of primary construction — April 2023 through May 2024 — with over a hundred Jupyter notebooks in a [separate repository](https://github.com/Wildertrek/Personality-Trait-Models).

## From datasets to embeddings to classifiers

Once the 44 datasets existed, the pipeline had three stages:

**1. Embedding.** Every trait entry was passed through OpenAI's text-embedding-3-small model, which maps text to a 1,536-dimensional vector. Semantically similar text lands near similar vectors. "Anxious" and "worried" end up close together; "anxious" and "organized" end up far apart. After embedding, each of the 6,694 traits became a point in 1,536-dimensional space.

**2. Classification.** For each model, we trained a Random Forest classifier to predict which factor a trait belongs to, given its embedding vector. Most score above 95% on their own training data. That is the expected baseline — the sanity check that the embeddings captured real semantic distinctions.

**3. Cross-model search.** We built a FAISS index over all 6,694 embeddings. FAISS lets you query any trait and find its nearest neighbors across all 44 models in milliseconds. That is the atlas's core capability: cross-tradition retrieval.

All of this — the datasets, the embeddings, the trained classifiers, the FAISS-ready vectors — ships in this repository. You can try it yourself:

```bash
python demo.py "tends to worry about the future"
```

## What the validation experiments found

The validation experiments serve two purposes: measuring classifier generalization and auditing data quality. Three of the final fixes in the atlas were discovered because a model's accuracy was unexpectedly low, which sent us back to the source data. The experiments caught what manual review missed.

### Experiment 1: Baseline discriminant validity

We generated 5,052 novel test items (none seen during training) and classified each through its corresponding model's Random Forest.

- **Mean accuracy: 58.6%** across all 44 models (median 61.1%)
- Every model beats its random baseline (100%). A 5-factor model's random baseline is 20%, a 21-factor model's is 4.8%. The atlas averages 3.5x above chance.
- Strong negative correlation between factor count and accuracy (r = -0.67, p < .001) — models with more factors are harder to classify, as expected.
- Inter-judge agreement (Cohen's kappa) of 0.99 across a triple-judge LLM panel, confirming the test items are unambiguous.
- Category breakdown: Motivational (74.5%) > Narcissism (68.3%) > Trait-Based (64.0%) > Cognitive (51.8%) > Clinical (50.6%) > Interpersonal (23.7%). The low-factor motivational models are easiest; the high-factor clinical models are hardest.

### Experiment 2: Improvement cycle

Three targeted interventions, evaluated on the same test items:

- **Embedding upgrade** (1,536 → 3,072 dimensions): +5.1pp across all 44 models. The higher-dimensional space separates similar factors more cleanly.
- **Data augmentation** (synonym expansion for underperforming models): +25.9pp on 14 targeted models. The models that struggled most had sparse training data — more lexical variety fixed that.
- **Hierarchical classification** (category-level pre-filter before factor-level prediction): +4.8pp on 8 targeted models with nested factor structures.
- **Combined best-per-model: 71.5%** (+12.9pp over baseline). 22 of 44 models now above 70%, up from 13. Zero models below 30%, down from 3.

### Experiment 3: External validation

The first two experiments used LLM-generated test items. Experiment 3 asks: do the classifiers work on items written by psychologists?

- **368 items from 21 published instruments** (BFI-44, HEXACO-60, GAD-7, Short Dark Triad, NARQ, etc.) classified through the atlas.
- **Accuracy: 69.6%** — 11 percentage points higher than on LLM-generated items. Published psychometric items are designed to load cleanly on single factors, and the classifiers pick up on that.
- **Multi-generator consistency**: A second set of 5,369 items generated by Claude Opus produced 55.5% accuracy vs GPT-4o's 58.7% (Cohen's d = 0.17). The results are not an artifact of one generator.
- **Convergent validity**: 100% category hit rate in the evaluation bank. Every human item retrieves neighbors from its correct atlas category, with a mean of 8.2 independent models per query.

The full results, per-model breakdowns, and reproduction instructions are in the [Empirical Validation](README.md#empirical-validation) section of the README.

## Timeline

| Period | Milestone |
|--------|-----------|
| Apr 2023 | Project started — "how many personality models are there?" |
| Apr–May 2023 | First 6 trait-based models (OCEAN, HEXACO, MBTI, EPM, 16PF, FTM) |
| Jun–Aug 2023 | Narcissism and clinical models added (10 + 10) |
| Sep–Nov 2023 | Motivational, cognitive, interpersonal, applied models (18 more) |
| Dec 2023 | 44 models, 358 factors, 6,694 trait rows complete |
| Jan–May 2024 | Embeddings, classifiers, FAISS index, PCA analysis |
| Jun–Nov 2024 | Validation experiments 1 and 2 |
| Dec 2024 | Paper submitted to ACM TIST |
| Jan–Feb 2025 | Model cards, starter notebooks, public repository |
| Feb 2026 | Experiment 3 (human items, multi-generator, DSM-5 alignment) |

---

*Next: open the [Quick Start notebook](https://colab.research.google.com/github/Wildertrek/survey/blob/main/notebooks/atlas_quick_start.ipynb) and explore all 44 models in one embedding space.*
