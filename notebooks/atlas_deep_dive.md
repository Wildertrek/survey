# Personality Atlas — Deep Dive

The [Quick Start notebook](https://colab.research.google.com/github/Wildertrek/survey/blob/main/notebooks/atlas_quick_start.ipynb) covers the atlas at a high level — 44 models, cross-model PCA, FAISS search, and all 12 research questions from the paper. This notebook goes the other direction: **pick one model and take it apart.**

You will train a classifier from scratch, inspect where it fails, run cross-validation, visualize the embedding space with PCA and KMeans, identify which embedding dimensions carry the most weight, measure how similar the factors are to each other, and then step outside the model to see how its constructs relate to the other 43 models in the atlas.

Along the way, the analyses connect back to the paper's research questions — RQ1 (generalization to novel items), RQ2 (factor complexity vs accuracy), RQ5 (cross-model convergence), and RQ7 (3072-dim upgrade) — but examined one model at a time instead of across the full atlas.

Change `MODEL` in Section 2 and every cell adapts automatically. No API keys required.

> Raetano, J., Gregor, J., & Tamang, S. (2026). *A Survey and Computational Atlas of Personality Models.* ACM TIST. Under review.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wildertrek/survey/blob/main/notebooks/atlas_deep_dive.ipynb)

## 1. Setup


```python
import os
if not os.path.exists("atlas"):
    !git clone --depth 1 https://github.com/Wildertrek/survey.git atlas
else:
    print("Atlas already cloned.")
```


```python
!pip install -q faiss-cpu

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

import ast
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import faiss

sns.set_style("whitegrid")
print("All libraries loaded.")
```

## 2. Select a Model

Change `MODEL` below to any of the 44 model abbreviations. Every subsequent cell adapts automatically — factor distributions, PCA projections, confusion matrices, cross-model searches, and accuracy comparisons all update to reflect the selected model.

| Category | Models |
|----------|--------|
| **Trait-Based** | `ocean` (Big Five), `hex` (HEXACO), `mbti`, `epm` (Eysenck), `sixteenpf`, `ftm` (Four Temperaments) |
| **Narcissism-Based** | `npi`, `pni`, `ffni`, `ffni_sf`, `narq`, `hsns`, `dtm` (Dark Triad), `dt4` (Dark Tetrad), `mcmin`, `ipn` |
| **Motivational/Value** | `stbv` (Schwartz Values), `sdt` (Self-Determination), `rft`, `aam`, `mst`, `cs` (Clifton) |
| **Cognitive/Learning** | `pct`, `scm`, `cest`, `fsls` (Felder-Silverman) |
| **Clinical/Health** | `mmpi`, `scid` (DSM), `bdi` (Depression), `gad7` (Anxiety), `wais`, `tci`, `mcmi`, `tmp`, `rit` (Rorschach), `tat` |
| **Interpersonal/Conflict** | `disc`, `tki` (Thomas-Kilmann) |
| **Application-Specific** | `riasec` (Holland Careers), `cmoa`, `tei`, `bt` (Bartle Types), `em` (Enneagram), `papc` |


```python
# ============================================
# CHANGE THIS to explore a different model
MODEL = "ocean"
# ============================================

# Load dataset, embeddings, pre-trained model, and label encoder
df = pd.read_csv(f"atlas/datasets/{MODEL}.csv")
emb_df = pd.read_csv(f"atlas/Embeddings/{MODEL}_embeddings.csv")
clf = joblib.load(f"atlas/models/{MODEL}_rf_model.pkl")
le = joblib.load(f"atlas/models/{MODEL}_label_encoder.pkl")

# Parse embeddings from CSV strings to numpy array
X = np.array([ast.literal_eval(e) for e in emb_df["Embedding"]])
y = df["Factor"].values
y_encoded = le.transform(y)

print(f"Model: {MODEL.upper()}")
print(f"Traits: {len(df)}, Factors: {df['Factor'].nunique()}, Embedding dim: {X.shape[1]}")
print(f"Factors: {sorted(df['Factor'].unique())}")
```

## 3. Dataset Inspection

Before building any model, look at the data. How many traits does each factor have? Are the factors balanced or heavily skewed?

Imbalanced factors matter: a classifier that always predicts the majority class can score high accuracy while learning nothing about the minority factors. The distribution below tells you whether to expect that problem.


```python
# Factor distribution
factor_counts = df["Factor"].value_counts().sort_index()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Bar chart
factor_counts.plot(kind="barh", ax=axes[0], color=sns.color_palette("husl", len(factor_counts)))
axes[0].set_xlabel("Trait Count")
axes[0].set_title(f"{MODEL.upper()} — Factor Distribution ({len(df)} traits)")

# Pie chart
axes[1].pie(factor_counts, labels=factor_counts.index, autopct="%1.0f%%",
            colors=sns.color_palette("husl", len(factor_counts)))
axes[1].set_title(f"{MODEL.upper()} — Factor Proportions")

plt.tight_layout()
plt.show()
```


```python
# Lexical schema — sample traits per factor
print(f"{MODEL.upper()}: {len(df)} traits across {df['Factor'].nunique()} factors\n")

for factor, group in df.groupby("Factor"):
    sample = group["Adjective"].unique()[:6]
    print(f"  {factor} ({len(group)} traits): {', '.join(sample)}")
```

## 4. Train a Random Forest Classifier

Each trait is represented as a 1,536-dim embedding vector from OpenAI's `text-embedding-3-small`. The classification task: given an embedding, predict which factor it belongs to.

We train a fresh Random Forest using an 80/20 stratified split with the same hyperparameters as the pre-trained model shipped in the repository. If the freshly trained accuracy matches the pre-trained model, the result is reproducible — the numbers in the paper are not an artifact of a lucky random seed.

**Expect high accuracy.** For models with few well-separated factors (like OCEAN's five), 100% is normal — 1,536 dimensions is more than enough capacity to separate five clusters with distinct vocabularies. This is a sanity check, not the hard test. The hard test comes in Section 13b, where we evaluate on items the classifier has never seen.


```python
# 80/20 stratified split — same parameters as original notebooks
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Train fresh RF (same hyperparameters as the pre-trained models)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Test accuracy: {acc:.1%} ({sum(y_pred == y_test)}/{len(y_test)} correct)\n")

# Compare with pre-trained model from repo
y_pred_pretrained = clf.predict(X_test)
acc_pretrained = accuracy_score(y_test, y_pred_pretrained)
print(f"Pre-trained model accuracy: {acc_pretrained:.1%}")
print(f"Freshly trained accuracy:   {acc:.1%}")
if abs(acc - acc_pretrained) < 0.001:
    print("Identical — reproduced successfully.")
```


```python
# Full classification report
print(classification_report(y_test, y_pred, target_names=le.classes_))
```

## 5. Confusion Matrix

If you are running the default model (OCEAN), the matrix below is probably solid blue along the diagonal — 100% accuracy, zero confusion. That is the correct result. Five factors with distinct vocabularies ("anxious, moody, tense" vs. "organized, disciplined, methodical") are trivially separable in a 1,536-dim space. A classifier that *couldn't* separate them would signal a problem with the embeddings, not a hard task.

The confusion matrix becomes genuinely informative when you select a model with more factors and semantic overlap — try `mmpi`, `scid`, or `ffni`. Off-diagonal entries there reveal factor pairs that share enough vocabulary to confuse the classifier, which often corresponds to constructs that psychometricians themselves debate splitting or merging. This connects to **RQ2** (factor complexity predicts difficulty) and **RQ6** (category-level performance differences) in the paper.

The normalized view (right panel) shows per-factor recall regardless of class size, which matters when factors are imbalanced.

**Keep this in mind for later:** 100% on a model's own training lexicon does not mean 100% on items it has never seen. Section 13b runs that harder test.


```python
cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(cm, index=le.classes_, columns=le.classes_)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Raw counts
sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues", ax=axes[0])
axes[0].set_xlabel("Predicted")
axes[0].set_ylabel("Actual")
axes[0].set_title(f"{MODEL.upper()} — Confusion Matrix (counts)")

# Normalized (percentages per row)
cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)
cm_norm_df = pd.DataFrame(cm_norm, index=le.classes_, columns=le.classes_)
sns.heatmap(cm_norm_df, annot=True, fmt=".0%", cmap="Blues", ax=axes[1])
axes[1].set_xlabel("Predicted")
axes[1].set_ylabel("Actual")
axes[1].set_title(f"{MODEL.upper()} — Confusion Matrix (row-normalized)")

plt.tight_layout()
plt.show()
```

## 6. Cross-Validation

A single 80/20 split can be lucky or unlucky depending on which traits land in the test set. Five-fold cross-validation gives a more stable estimate: every trait appears in the test set exactly once across the five folds.

For OCEAN and other models with few, well-separated factors, expect all five folds to hit 100% with zero variance. That is not a sign of overfitting — it means the factor boundaries are consistent regardless of which examples the classifier trains on. The embedding geometry genuinely separates these constructs.

The diagnostic value of cross-validation appears with harder models. Select `mmpi` or `scid` and re-run: you will see fold-to-fold variance of several percentage points, revealing factors that sit near decision boundaries and are sensitive to which specific traits end up in each fold.

**The narrative arc so far:** Sections 4-6 confirm the atlas correctly encodes what psychometrics already knows — factor structure is preserved in the embedding space. Section 12 will show that difficulty varies across the 44 models, and Section 13b will test whether classifiers generalize beyond their own training lexicon.


```python
cv_scores = cross_val_score(
    RandomForestClassifier(n_estimators=100, random_state=42),
    X, y_encoded, cv=5, scoring="accuracy"
)

print(f"5-Fold Cross-Validation for {MODEL.upper()}:")
print(f"  Fold scores: {', '.join(f'{s:.1%}' for s in cv_scores)}")
print(f"  Mean: {cv_scores.mean():.1%} (+/- {cv_scores.std() * 2:.1%})")

# Visualize
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(range(1, 6), cv_scores, color=sns.color_palette("husl", 5), alpha=0.8)
ax.axhline(y=cv_scores.mean(), color="red", linestyle="--", label=f"Mean = {cv_scores.mean():.1%}")
ax.set_xlabel("Fold")
ax.set_ylabel("Accuracy")
ax.set_title(f"{MODEL.upper()} — 5-Fold Cross-Validation")
ax.set_ylim(0, 1.05)
ax.legend()
plt.tight_layout()
plt.show()
```

## 7. PCA — Embedding Space Visualization

PCA projects the 1,536-dim embedding space down to dimensions we can actually look at. Three views, each answering a different question:

- **Scree plot** (left): How concentrated is the variance? A steep initial drop followed by a long tail means a few directions carry most of the factor structure. A flatter curve means the structure is spread across many dimensions.
- **PC1 vs PC2** (center): Do the factors form visually distinct clusters, or do they overlap? Well-separated clusters predict high classifier accuracy; overlapping clouds predict confusion matrix off-diagonals.
- **PC1 vs PC3** (right): Factors that overlap in PC2 sometimes separate along PC3. Always check more than one projection before concluding that factors are inseparable.


```python
pca = PCA(n_components=10)
X_pca = pca.fit_transform(X)
cumvar = np.cumsum(pca.explained_variance_ratio_) * 100

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Scree plot
axes[0].bar(range(1, 11), pca.explained_variance_ratio_ * 100, alpha=0.6, label="Individual")
axes[0].plot(range(1, 11), cumvar, "r-o", markersize=4, label="Cumulative")
axes[0].set_xlabel("PC")
axes[0].set_ylabel("Variance Explained (%)")
axes[0].set_title(f"{MODEL.upper()} — Scree Plot")
axes[0].legend(fontsize=8)

# PC1 vs PC2 colored by factor
colors = sns.color_palette("husl", df["Factor"].nunique())
for i, factor in enumerate(sorted(df["Factor"].unique())):
    mask = y == factor
    axes[1].scatter(X_pca[mask, 0], X_pca[mask, 1], c=[colors[i]], s=30, alpha=0.7, label=factor)
axes[1].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
axes[1].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
axes[1].set_title(f"{MODEL.upper()} — PC1 vs PC2")
axes[1].legend(fontsize=7, loc="best", ncol=max(1, df['Factor'].nunique() // 8 + 1))

# PC1 vs PC3
for i, factor in enumerate(sorted(df["Factor"].unique())):
    mask = y == factor
    axes[2].scatter(X_pca[mask, 0], X_pca[mask, 2], c=[colors[i]], s=30, alpha=0.7, label=factor)
axes[2].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
axes[2].set_ylabel(f"PC3 ({pca.explained_variance_ratio_[2]*100:.1f}%)")
axes[2].set_title(f"{MODEL.upper()} — PC1 vs PC3")

plt.tight_layout()
plt.show()

print(f"\nFirst 10 PCs capture {cumvar[-1]:.1f}% of variance")
```

## 8. KMeans Clustering — Do Factors Emerge Without Labels?

If the embedding space truly captures factor structure, unsupervised clustering should recover the factors without seeing any labels. We run KMeans with *k* equal to the number of factors and compare the resulting clusters (left) against the ground-truth labels (right).

**Cluster purity** measures alignment: for each cluster, what fraction of its members share the same true factor? A purity of 1.0 means KMeans perfectly recovered the labeled structure from geometry alone — the factors are not just classifiable, they are the natural clusters in the space.


```python
n_factors = df["Factor"].nunique()

kmeans = KMeans(n_clusters=n_factors, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# KMeans clusters in PCA space
scatter = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap="tab10", s=30, alpha=0.7)
axes[0].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
axes[0].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
axes[0].set_title(f"{MODEL.upper()} — KMeans ({n_factors} clusters)")
plt.colorbar(scatter, ax=axes[0], ticks=range(n_factors))

# Ground-truth factors in PCA space (for comparison)
scatter2 = axes[1].scatter(X_pca[:, 0], X_pca[:, 1], c=y_encoded, cmap="tab10", s=30, alpha=0.7)
axes[1].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
axes[1].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
axes[1].set_title(f"{MODEL.upper()} — Ground-Truth Factors")
plt.colorbar(scatter2, ax=axes[1], ticks=range(n_factors))

plt.tight_layout()
plt.show()

# Cluster purity: how well do clusters align with factors?
from collections import Counter
purity_scores = []
for c in range(n_factors):
    mask = clusters == c
    if mask.sum() > 0:
        counts = Counter(y[mask])
        majority = counts.most_common(1)[0][1]
        purity_scores.append(majority / mask.sum())

mean_purity = np.mean(purity_scores)
print(f"Mean cluster purity: {mean_purity:.1%} (1.0 = perfect alignment with factors)")
```

## 9. Feature Importance — Which Embedding Dimensions Matter?

A Random Forest can report how much each of the 1,536 embedding dimensions contributed to its decision splits. The distribution is typically very skewed: most dimensions contribute almost nothing, and a small handful do most of the work.

The number of dimensions needed to reach 90% cumulative importance tells you the **effective dimensionality** of the classification problem. If 50 out of 1,536 dimensions carry 90% of the weight, the factor structure lives in a low-dimensional subspace — and those 50 dimensions are the semantic axes that differentiate this model's constructs.


```python
importances = rf.feature_importances_
top_k = 30
top_idx = np.argsort(importances)[-top_k:][::-1]

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(range(top_k), importances[top_idx], color="steelblue", alpha=0.8)
ax.set_xticks(range(top_k))
ax.set_xticklabels([f"d{i}" for i in top_idx], rotation=45, fontsize=8)
ax.set_xlabel("Embedding Dimension")
ax.set_ylabel("Feature Importance")
ax.set_title(f"{MODEL.upper()} — Top {top_k} Most Important Embedding Dimensions")
plt.tight_layout()
plt.show()

# Cumulative importance
sorted_imp = np.sort(importances)[::-1]
cum_imp = np.cumsum(sorted_imp)
n_90 = np.searchsorted(cum_imp, 0.9) + 1
print(f"Top {n_90} of {len(importances)} dimensions capture 90% of importance")
print(f"Top 30 dimensions capture {cum_imp[29]:.1%} of importance")
```

## 10. Intra-Model Similarity — How Related Are the Factors?

Compute the centroid (mean embedding vector) for each factor and measure pairwise cosine similarity. This reveals the model's internal geometry:

- **High similarity** (cosine > 0.85) between two factors means they share substantial lexical content and may be hard to distinguish empirically. These pairs often correspond to known measurement overlap in the psychometric literature — constructs that researchers have debated splitting or merging.
- **Low similarity** (cosine < 0.6) means the factors occupy genuinely different regions of the semantic space.

The most-similar and least-similar pairs printed below are a quick diagnostic: do they match your theoretical expectations for this model?


```python
# Compute centroid for each factor
factors_sorted = sorted(df["Factor"].unique())
centroids = np.array([X[y == f].mean(axis=0) for f in factors_sorted])

# Cosine similarity between factor centroids
norms = np.linalg.norm(centroids, axis=1, keepdims=True)
centroids_norm = centroids / norms
sim_matrix = centroids_norm @ centroids_norm.T

sim_df = pd.DataFrame(sim_matrix, index=factors_sorted, columns=factors_sorted)

fig, ax = plt.subplots(figsize=(max(8, len(factors_sorted) * 0.8), max(6, len(factors_sorted) * 0.6)))
sns.heatmap(sim_df, annot=True, fmt=".2f", cmap="RdYlBu_r", vmin=0.5, vmax=1.0,
            ax=ax, square=True)
ax.set_title(f"{MODEL.upper()} — Inter-Factor Cosine Similarity (centroids)")
plt.tight_layout()
plt.show()

# Most and least similar pairs (excluding self-comparisons)
mask = np.ones_like(sim_matrix, dtype=bool)
np.fill_diagonal(mask, False)
off_diag = sim_matrix.copy()
off_diag[~mask] = np.nan

max_idx = np.unravel_index(np.nanargmax(off_diag), off_diag.shape)
min_idx = np.unravel_index(np.nanargmin(off_diag), off_diag.shape)

print(f"Most similar pair:  {factors_sorted[max_idx[0]]} <-> {factors_sorted[max_idx[1]]} (cos = {sim_matrix[max_idx]:.3f})")
print(f"Least similar pair: {factors_sorted[min_idx[0]]} <-> {factors_sorted[min_idx[1]]} (cos = {sim_matrix[min_idx]:.3f})")
```

## 11. Cross-Model Search — Find Related Traits Across the Atlas (RQ5)

Everything above stayed within a single model. Now we step outside.

With all 6,694 traits from all 44 models in a single FAISS index, you can query any factor from the selected model and find its nearest neighbors across the entire atlas. OCEAN Extraversion connects to HEXACO Social Self-Esteem and MBTI Extraversion. Dark Triad Machiavellianism links to MMPI Psychopathic Deviate and OCEAN low Agreeableness. These cross-tradition bridges emerge directly from the shared embedding geometry.

This is the paper's **RQ5** (cross-model convergent validity) examined at the level of a single model. The Quick Start notebook runs this analysis across the full atlas; here you can see exactly which factors from other traditions are closest to each of your model's constructs.

Change `QUERY_FACTOR` below to search for a different factor. Results marked with `*` come from other models.


```python
# Build the full atlas FAISS index
CATEGORIES = {
    "Trait-Based": ["ocean", "hex", "mbti", "epm", "sixteenpf", "ftm"],
    "Narcissism-Based": ["npi", "pni", "hsns", "dtm", "dt4", "ffni", "ffni_sf", "narq", "mcmin", "ipn"],
    "Motivational/Value": ["stbv", "sdt", "rft", "aam", "mst", "cs"],
    "Cognitive/Learning": ["pct", "cest", "scm", "fsls"],
    "Clinical/Health": ["mmpi", "scid", "bdi", "gad7", "wais", "tci", "mcmi", "tmp", "rit", "tat"],
    "Interpersonal/Conflict": ["disc", "tki"],
    "Application-Specific": ["riasec", "cmoa", "tei", "bt", "em", "papc"]
}
model_to_cat = {s: c for c, model_list in CATEGORIES.items() for s in model_list}

all_models = sorted([f.replace(".csv", "") for f in os.listdir("atlas/datasets") if f.endswith(".csv")])
all_vecs, all_labels, all_cats, all_factors, all_adjs = [], [], [], [], []

for model in all_models:
    d = pd.read_csv(f"atlas/datasets/{model}.csv")
    e = pd.read_csv(f"atlas/Embeddings/{model}_embeddings.csv")
    vecs = np.array([ast.literal_eval(v) for v in e["Embedding"]])
    all_vecs.append(vecs)
    all_labels.extend([model.upper()] * len(d))
    all_cats.extend([model_to_cat.get(model, "Unknown")] * len(d))
    all_factors.extend(d["Factor"].values)
    all_adjs.extend(d["Adjective"].values)

X_all = np.vstack(all_vecs)
X_norm = (X_all / np.linalg.norm(X_all, axis=1, keepdims=True)).astype(np.float32)
index = faiss.IndexFlatIP(X_norm.shape[1])
index.add(X_norm)

print(f"FAISS index: {index.ntotal} vectors from {len(all_models)} models")
```


```python
# Search: pick a factor from the selected model
# Change QUERY_FACTOR to search for a different factor
QUERY_FACTOR = df["Factor"].value_counts().index[0]  # default: most common factor

query_mask = df["Factor"] == QUERY_FACTOR
query_idx = df[query_mask].index[0]
q = X[query_idx].reshape(1, -1).astype(np.float32)
q = q / np.linalg.norm(q)

D, I = index.search(q, 25)

query_trait = df.iloc[query_idx]
print(f"Query: {MODEL.upper()} / {QUERY_FACTOR} — \"{query_trait['Adjective']}\"\n")
print(f"{'Rank':<5} {'Model':<12} {'Factor':<30} {'Adjective':<20} {'Category':<22} {'Score':.5}")
print("-" * 95)
for rank, (i, score) in enumerate(zip(I[0], D[0]), 1):
    marker = " *" if all_labels[i] != MODEL.upper() else ""
    print(f"{rank:<5} {all_labels[i]:<12} {all_factors[i]:<30} {all_adjs[i]:<20} {all_cats[i]:<22} {score:.4f}{marker}")

# Summary
result_cats = set(all_cats[i] for i in I[0])
result_models = set(all_labels[i] for i in I[0])
cross_model = sum(1 for i in I[0] if all_labels[i] != MODEL.upper())
print(f"\n{cross_model}/25 results from other models, spanning {len(result_cats)} categories and {len(result_models)} models")
print("(* = cross-model match)")
```

## 12. Accuracy Leaderboard — All 44 Models

Each model's pre-trained Random Forest is evaluated on the model's own training lexicon (full dataset, no split). **100% is the expected baseline** — if a classifier trained on a model's own traits cannot separate its factors, either the embeddings failed to capture the semantic distinctions or the taxonomy assigned traits to the wrong factors.

Most models hit or approach 100%. The ones that fall short are the scientifically interesting cases: they have many factors with overlapping vocabulary, and the 1,536-dim embedding space does not fully separate them. Clinical instruments (MMPI, SCID) and narcissism measures (FFNI with 15 facets) tend to cluster at the bottom because their constructs share substantial psychometric vocabulary — a known challenge in the assessment literature.

These lower-accuracy models are where the atlas's 3072-dim embedding upgrade (Section 14) and augmented lexicons add the most value. The leaderboard tells you which models benefit from richer representations and which are already solved at 1,536 dimensions.


```python
results = []
for model in all_models:
    d = pd.read_csv(f"atlas/datasets/{model}.csv")
    m = joblib.load(f"atlas/models/{model}_rf_model.pkl")
    enc = joblib.load(f"atlas/models/{model}_label_encoder.pkl")
    e = pd.read_csv(f"atlas/Embeddings/{model}_embeddings.csv")
    Xm = np.array([ast.literal_eval(v) for v in e["Embedding"]])
    preds = enc.inverse_transform(m.predict(Xm))
    acc = (preds == d["Factor"].values).mean()
    results.append({
        "Model": model.upper(), "Category": model_to_cat.get(model, "Unknown"),
        "Traits": len(d), "Factors": d["Factor"].nunique(), "Accuracy": acc
    })

results_df = pd.DataFrame(results).sort_values("Accuracy", ascending=True)

# Highlight the selected model
colors = ["#ff6b6b" if m == MODEL.upper() else "#4ecdc4" for m in results_df["Model"]]

fig, ax = plt.subplots(figsize=(10, max(8, len(results_df) * 0.25)))
ax.barh(range(len(results_df)), results_df["Accuracy"], color=colors, alpha=0.85)
ax.set_yticks(range(len(results_df)))
ax.set_yticklabels([f"{m} ({f}F)" for m, f in zip(results_df["Model"], results_df["Factors"])], fontsize=7)
ax.set_xlabel("Accuracy")
ax.set_title(f"Atlas Accuracy Leaderboard — {MODEL.upper()} highlighted in red")
ax.axvline(x=results_df["Accuracy"].mean(), color="gray", linestyle="--", alpha=0.5, label=f"Mean = {results_df['Accuracy'].mean():.1%}")
ax.legend()
plt.tight_layout()
plt.show()

# Stats
selected = results_df[results_df["Model"] == MODEL.upper()].iloc[0]
rank = len(results_df) - results_df.index.get_loc(results_df[results_df["Model"] == MODEL.upper()].index[0])
print(f"\n{MODEL.upper()}: {selected['Accuracy']:.1%} accuracy — rank {rank}/{len(results_df)}")
print(f"Atlas mean: {results_df['Accuracy'].mean():.1%}, median: {results_df['Accuracy'].median():.1%}")
```

## 13. Accuracy by Category

Different research traditions pose different classification challenges. Narcissism-based models (10 instruments measuring closely related constructs) tend to be harder to separate than trait-based models (where Extraversion and Neuroticism occupy distinct semantic regions). The table below breaks down accuracy by the atlas's 7-category taxonomy.


```python
cat_stats = pd.DataFrame(results).groupby("Category").agg(
    Models=("Model", "count"),
    Mean_Accuracy=("Accuracy", "mean"),
    Min_Accuracy=("Accuracy", "min"),
    Max_Accuracy=("Accuracy", "max"),
    Total_Traits=("Traits", "sum")
).sort_values("Mean_Accuracy", ascending=False)

cat_stats["Mean_Accuracy"] = cat_stats["Mean_Accuracy"].apply(lambda x: f"{x:.1%}")
cat_stats["Min_Accuracy"] = cat_stats["Min_Accuracy"].apply(lambda x: f"{x:.1%}")
cat_stats["Max_Accuracy"] = cat_stats["Max_Accuracy"].apply(lambda x: f"{x:.1%}")
cat_stats
```

## 13b. Novel Item Evaluation (RQ1)

Sections 4-6 confirmed that each model's classifier separates its own training lexicon — most at or near 100%. The leaderboard in Section 12 showed which models are already solved and which have room to improve. But those results all test on data the classifier was built from.

The harder question, and the paper's **RQ1**: **can classifiers discriminate between factors on genuinely novel items?**

Below we evaluate on novel items generated independently by GPT-4o from factor definitions alone, without access to the training lexicon. These are the same 5,052 items used in the paper's Experiment 1 (pre-embedded in the repository — no API key needed).

For OCEAN, expect accuracy to drop from 100% (Section 4) to roughly 70-80%. That gap is the **generalization penalty** — the cost of moving from memorized lexical entries to genuinely new phrasings of the same constructs. Across all 44 models, the mean drops from ~98% to 59%. The size of that gap is the central finding of the paper's validation experiments, and it varies systematically with factor count (**RQ2**) and atlas category (**RQ6**).


```python
import json

# Load pre-computed test items (generated by GPT-4o, embedded offline)
test_items = json.load(open("atlas/data/test_items/test_items.json"))
test_emb = np.load("atlas/data/test_items/test_items_embeddings.npz")["embeddings"]

# Filter to the selected model
model_idx = [i for i, item in enumerate(test_items) if item["model"] == MODEL]

if not model_idx:
    print(f"No test items available for {MODEL.upper()}")
else:
    X_novel = test_emb[model_idx]
    y_novel_true = [test_items[i]["expected_factor"] for i in model_idx]

    # Classify using the pre-trained RF from Section 2
    y_novel_pred = le.inverse_transform(clf.predict(X_novel))

    acc_novel = accuracy_score(y_novel_true, y_novel_pred)
    print(f"{MODEL.upper()}: {acc_novel:.1%} accuracy on {len(model_idx)} novel test items")
    print(f"(vs. {acc:.1%} on 80/20 train/test split in Section 4)\n")
    print(classification_report(y_novel_true, y_novel_pred, zero_division=0))

    # Confusion matrix on novel items
    cm_novel = confusion_matrix(y_novel_true, y_novel_pred, labels=le.classes_)
    cm_novel_df = pd.DataFrame(cm_novel, index=le.classes_, columns=le.classes_)

    fig, ax = plt.subplots(figsize=(max(8, len(le.classes_) * 0.8), max(6, len(le.classes_) * 0.6)))
    sns.heatmap(cm_novel_df, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual (GPT-4o generated)")
    ax.set_title(f"{MODEL.upper()} — Novel Item Confusion Matrix ({len(model_idx)} items, {acc_novel:.1%})")
    plt.tight_layout()
    plt.show()
```

## 14. 3072-dim Embedding Upgrade (RQ7)

OpenAI's `text-embedding-3-large` produces 3,072-dim vectors — twice the resolution. The paper's **RQ7** asks: does the extra dimensionality help separate factors that were borderline in the 1,536-dim space?

The upgraded embeddings and retrained classifiers are hosted on [Hugging Face Hub](https://huggingface.co/datasets/Wildertrek/personality-atlas-3072). The cells below download the selected model's 3072-dim assets and compare both accuracy and embedding geometry side by side.

Across the full atlas, the upgrade improves mean novel-item accuracy from 59% to ~65% — a meaningful gain, but not transformative. Where it matters most is for models in the 40-60% range, where the extra dimensions can resolve borderline factor overlaps. The Quick Start notebook covers the other two improvement strategies: data augmentation (**RQ8**) and hierarchical classification (**RQ9**).


```python
!pip install -q huggingface_hub
import os
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "0"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

import warnings
warnings.filterwarnings("ignore", message=".*HF_TOKEN.*")
warnings.filterwarnings("ignore", message=".*unauthenticated.*")

from huggingface_hub import hf_hub_download

HF_REPO = "Wildertrek/personality-atlas-3072"

# Download 3072-dim assets for the selected model (public dataset — no token needed)
emb3072_path = hf_hub_download(HF_REPO, f"Embeddings_3072/{MODEL}_embeddings.csv", repo_type="dataset")
model3072_path = hf_hub_download(HF_REPO, f"models_3072/{MODEL}_rf_model.pkl", repo_type="dataset")
enc3072_path = hf_hub_download(HF_REPO, f"models_3072/{MODEL}_label_encoder.pkl", repo_type="dataset")

emb3072_df = pd.read_csv(emb3072_path)
X3072 = np.array([ast.literal_eval(e) for e in emb3072_df["Embedding"]])
clf3072 = joblib.load(model3072_path)
le3072 = joblib.load(enc3072_path)

# Full-dataset accuracy comparison
df_full = pd.read_csv(f"atlas/datasets/{MODEL}.csv")
y_true = df_full["Factor"].values

preds_1536 = le.inverse_transform(clf.predict(X))
preds_3072 = le3072.inverse_transform(clf3072.predict(X3072))

acc_1536 = (preds_1536 == y_true).mean()
acc_3072 = (preds_3072 == y_true).mean()

print(f"{MODEL.upper()} accuracy comparison:")
print(f"  1536-dim (text-embedding-3-small): {acc_1536:.1%}")
print(f"  3072-dim (text-embedding-3-large): {acc_3072:.1%}")
print(f"  Delta: {(acc_3072 - acc_1536)*100:+.1f} percentage points")
print(f"  Embedding dimensions: {X.shape[1]} → {X3072.shape[1]}")
```


```python
# PCA comparison: 1536 vs 3072 embedding spaces
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

for ax, (Xd, dim_label) in zip(axes, [(X, "1536-dim"), (X3072, "3072-dim")]):
    pca_d = PCA(n_components=2)
    Xp = pca_d.fit_transform(Xd)
    colors_d = sns.color_palette("husl", df_full["Factor"].nunique())
    for i, factor in enumerate(sorted(df_full["Factor"].unique())):
        mask = y_true == factor
        ax.scatter(Xp[mask, 0], Xp[mask, 1], c=[colors_d[i]], s=20, alpha=0.6, label=factor)
    ax.set_xlabel(f"PC1 ({pca_d.explained_variance_ratio_[0]*100:.1f}%)")
    ax.set_ylabel(f"PC2 ({pca_d.explained_variance_ratio_[1]*100:.1f}%)")
    ax.set_title(f"{MODEL.upper()} — {dim_label}")
    if df_full["Factor"].nunique() <= 12:
        ax.legend(fontsize=6, loc="best")

plt.suptitle(f"Embedding Space Comparison: 1536-dim vs 3072-dim", fontsize=13, y=1.02)
plt.tight_layout()
plt.show()
```

### Does the upgrade help on novel items?

Training-data accuracy is often high for both embedding sizes — the real test is generalization. Below we run both classifiers on the novel GPT-4o test items from Section 13b using pre-computed 3072-dim embeddings from HuggingFace.


```python
# Novel item evaluation: 1536-dim vs 3072-dim on truly novel test items
# Downloads 3072-dim test item embeddings from HuggingFace (no API key needed)
test3072_path = hf_hub_download(HF_REPO, "test_items/test_items_embeddings_3072.npz", repo_type="dataset")
test_emb_3072 = np.load(test3072_path)["embeddings"]

model_idx = [i for i, item in enumerate(test_items) if item["model"] == MODEL]

if model_idx:
    X_novel_1536 = test_emb[model_idx]
    X_novel_3072 = test_emb_3072[model_idx]
    y_novel_true = [test_items[i]["expected_factor"] for i in model_idx]

    pred_1536 = le.inverse_transform(clf.predict(X_novel_1536))
    pred_3072 = le3072.inverse_transform(clf3072.predict(X_novel_3072))

    acc_n1536 = accuracy_score(y_novel_true, pred_1536)
    acc_n3072 = accuracy_score(y_novel_true, pred_3072)
    delta = (acc_n3072 - acc_n1536) * 100

    print(f"{MODEL.upper()} — Novel item accuracy ({len(model_idx)} items):")
    print(f"  1536-dim: {acc_n1536:.1%}")
    print(f"  3072-dim: {acc_n3072:.1%}")
    print(f"  Delta:    {delta:+.1f} percentage points")
    print(f"\n(Compare with training-data accuracy: 1536={acc_1536:.1%}, 3072={acc_3072:.1%})")
else:
    print(f"No test items for {MODEL.upper()}")
```

---

## What This Notebook Covered

Starting from a single model (`MODEL`), you trained a classifier from scratch, inspected its confusion patterns, validated with cross-validation and KMeans, visualized the embedding geometry, measured inter-factor similarity, and then stepped outside to see how this model's constructs relate to the other 43 in the atlas. The 3072-dim upgrade in Section 14 showed whether higher-resolution embeddings help for this specific model.

These analyses connect to the paper's research questions at the single-model level:

| Section | Paper RQ | What you saw |
|:--------|:---------|:-------------|
| 13b. Novel Items | RQ1 | Generalization accuracy on items the classifier never trained on |
| 5. Confusion Matrix | RQ2, RQ6 | Factor overlap predicts where the classifier struggles |
| 11. Cross-Model Search | RQ5 | How this model's constructs connect to other traditions |
| 14. 3072-dim Upgrade | RQ7 | Whether doubling embedding dimensions improves this model |

The Quick Start notebook covers the remaining RQs (RQ3-RQ4 judge agreement, RQ8-RQ9 augmentation and hierarchical strategies, RQ10-RQ12 external validation) at the atlas-wide level.

## What's Next — From Atlas to Agents

Everything in this notebook treats personality as a static classification problem: given a trait description, assign it to a factor. The companion project, **MindBench**, asks the dynamic question: *can an LLM maintain a consistent personality profile while acting in a narrative?*

MindBench takes 10 novels, extracts characters with BookNLP, infers OCEAN profiles from textual evidence, and tests whether LLMs can replicate those profiles under perturbation, across tasks, and in multi-agent coordination. The atlas classifiers from this notebook become the scoring backbone — every behavioral assessment routes through the same embedding space and Random Forest pipeline you just explored.

If the atlas is the map of personality space, MindBench is the test of whether agents can navigate it.

---

Every analysis adapts to any of the 44 models — change `MODEL` in Section 2 and re-run. For the atlas-wide view (cross-model PCA, DSM-5 clinical alignment, full-atlas FAISS search, all 12 RQs), see the [Quick Start notebook](https://colab.research.google.com/github/Wildertrek/survey/blob/main/notebooks/atlas_quick_start.ipynb).

**Repository:** [github.com/Wildertrek/survey](https://github.com/Wildertrek/survey) | **3072-dim assets:** [Hugging Face Hub](https://huggingface.co/datasets/Wildertrek/personality-atlas-3072)
**Paper:** Raetano, J., Gregor, J., & Tamang, S. (2026). *A Survey and Computational Atlas of Personality Models.* ACM TIST.
**License:** MIT
