#!/usr/bin/env python3
"""
Generate the SPA (Semantic Personality Atlas) cluster table for Paper 1.

CANONICAL script for Table 7. All SPA claims must match this output.

Pipeline:
  1. Load 44 model embeddings from Embeddings/*.csv (pandas, json.loads)
  2. PCA to 50 components (NO StandardScaler)
  3. k-means k=15 (random_state=42, n_init=10, algorithm='lloyd')
  4. Hungarian optimal assignment: match k-means IDs to semantic labels
  5. Profile + output JSON

Usage:
  python scripts/generate_spa_table.py
  python scripts/generate_spa_table.py --output results/spa_table.json
"""

import argparse
import json
import os
import sys
from collections import Counter

import numpy as np
import pandas as pd
import sklearn
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

SURVEY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMBEDDINGS_DIR = os.path.join(SURVEY_ROOT, "Embeddings")

MODEL_LIST = sorted([
    "aam", "bdi", "bt", "cest", "cmoa", "cs", "disc", "dt4", "dtm", "em",
    "epm", "ffni", "ffni_sf", "fsls", "ftm", "gad7", "hex", "hsns", "ipn",
    "mbti", "mcmi", "mcmin", "mmpi", "mst", "narq", "npi", "ocean", "papc",
    "pct", "pni", "rft", "riasec", "rit", "scid", "scm", "sdt", "sixteenpf",
    "stbv", "tat", "tci", "tei", "tki", "tmp", "wais",
])

MODEL_CATEGORIES = {
    "ocean": "Trait-Based", "hex": "Trait-Based", "epm": "Trait-Based",
    "sixteenpf": "Trait-Based", "mbti": "Trait-Based", "ftm": "Trait-Based",
    "npi": "Narcissism-Based", "narq": "Narcissism-Based", "ffni": "Narcissism-Based",
    "hsns": "Narcissism-Based", "pni": "Narcissism-Based", "mcmin": "Narcissism-Based",
    "ffni_sf": "Narcissism-Based", "ipn": "Narcissism-Based",
    "dtm": "Narcissism-Based", "dt4": "Narcissism-Based",
    "aam": "Motivational", "mst": "Motivational", "rft": "Motivational",
    "sdt": "Motivational", "stbv": "Motivational", "cs": "Motivational",
    "pct": "Cognitive", "scm": "Cognitive", "cest": "Cognitive", "fsls": "Cognitive",
    "mmpi": "Clinical", "tci": "Clinical", "tmp": "Clinical", "bdi": "Clinical",
    "gad7": "Clinical", "scid": "Clinical", "mcmi": "Clinical",
    "rit": "Clinical", "tat": "Clinical", "wais": "Clinical",
    "tki": "Interpersonal", "disc": "Interpersonal",
    "riasec": "App/Holistic", "bt": "App/Holistic", "tei": "App/Holistic",
    "em": "App/Holistic", "papc": "App/Holistic", "cmoa": "App/Holistic",
}

# Semantic labels + keyword signatures for content-based matching.
# Hungarian optimal assignment matches each label to a k-means cluster
# by maximizing keyword overlap, making results robust to sklearn version.
LABEL_SIGNATURES = [
    ("Warmth & Prosociality", {
        "empathetic", "cooperative", "agreeableness", "cooperativeness",
        "empathy", "relationship building", "warmth", "reward dependence"}),
    ("Dominance & Persistence", {
        "assertive", "dominant", "assertiveness", "authority",
        "persistence", "dominance", "competitive"}),
    ("Clinical Psychopathology", {
        "delusional", "erratic", "neurodevelopmental",
        "psychoticism", "schizophrenia", "somatic symptom disorder"}),
    ("Depression & Anhedonia", {
        "hopeless", "indifferent", "sadness", "loss of pleasure",
        "crying", "depressed mood", "anhedonia", "negative"}),
    ("Activation & Approach", {
        "adventurous", "active", "extraversion", "promotion focus",
        "novelty seeking", "approach", "activation", "innovativeness"}),
    ("Imagination & Openness", {
        "creative", "curious", "intuition", "intuitive",
        "openness", "imagination", "fantasy", "openness to change"}),
    ("Withdrawal & Avoidance", {
        "avoidant", "reserved", "introversion", "hiding the self",
        "withdrawal", "social_introversion", "quiet", "paranoia"}),
    ("Self-Direction & Autonomy", {
        "independent", "self-sufficiency", "self-directedness",
        "autonomy", "resourceful", "self-transcendence", "self-assured"}),
    ("Reactive Aggression", {
        "impulsive", "irritable", "aggressive", "disinhibition",
        "aggression", "entitlement rage", "anger"}),
    ("Shame & Self-Punishment", {
        "insecure", "self-blaming", "devaluing", "guilty",
        "shame", "regretful", "self-dislike", "punishment feelings"}),
    ("Dark Manipulation", {
        "manipulative", "exploitative", "machiavellianism",
        "meanness", "callousness", "exploitativeness", "deceptive"}),
    ("Grandiose Narcissism", {
        "grandiose", "entitled", "exhibitionism", "narcissism",
        "entitlement", "grandiosity", "attention-seeking", "grandiose fantasy"}),
    ("Anxiety & Fear", {
        "anxious", "fearful", "worrying", "nervous",
        "harm avoidance", "restless", "trouble relaxing"}),
    ("Analytical Cognition", {
        "analytical", "logical", "sensing", "rational",
        "sequential", "thinking", "structured"}),
    ("Applied Life Domains", {
        "resilience", "career", "mental health",
        "stress management", "environmental", "lifelong learning",
        "conflict resolution", "career and professional development"}),
]


def load_embeddings():
    """Load all 44 model embeddings using pandas (matching Colab notebook)."""
    all_embeddings = []
    all_metadata = []

    for model_key in MODEL_LIST:
        fname = os.path.join(EMBEDDINGS_DIR, f"{model_key}_embeddings.csv")
        if not os.path.exists(fname):
            print(f"  WARNING: {fname} not found, skipping")
            continue

        emb_df = pd.read_csv(fname)
        embeddings = [json.loads(e) for e in emb_df["Embedding"]]
        all_embeddings.append(np.array(embeddings, dtype=np.float32))

        model_name = model_key.upper()
        for _, row in emb_df.iterrows():
            all_metadata.append({
                "model": model_key,
                "category": MODEL_CATEGORIES[model_key],
                "factor": str(row.get("Factor", "")),
                "adjective": str(row.get("Adjective", "")),
            })

    X = np.vstack(all_embeddings)
    df = pd.DataFrame(all_metadata)
    return X, df


def cluster_and_assign(X, df):
    """PCA-50 + k-means + Hungarian label assignment."""
    # PCA (no scaler). random_state pinned for reproducibility.
    # PCA uses randomized SVD when n_components < 0.8 * min(n_samples, n_features).
    pca = PCA(n_components=50, random_state=42)
    X_pca = pca.fit_transform(X).astype(np.float32)

    # k-means
    km = KMeans(n_clusters=15, random_state=42, n_init=10,
                algorithm="lloyd", max_iter=300, tol=1e-4)
    raw_labels = km.fit_predict(X_pca)
    sil = silhouette_score(X_pca, raw_labels)

    # Build vocabulary per raw cluster (top 15 adjectives + factors, lowercased)
    cluster_vocabs = {}
    for c_id in range(15):
        mask = raw_labels == c_id
        cdf = df[mask]
        top_adjs = set(
            a.lower().strip()
            for a in cdf["adjective"].value_counts().head(15).index if a
        )
        top_facts = set(
            f.lower().strip()
            for f in cdf["factor"].value_counts().head(15).index if f
        )
        cluster_vocabs[c_id] = top_adjs | top_facts

    # Hungarian optimal assignment: maximize keyword overlap
    n_labels = len(LABEL_SIGNATURES)
    cost_matrix = np.zeros((n_labels, 15))
    for i, (_, keywords) in enumerate(LABEL_SIGNATURES):
        for c_id in range(15):
            cost_matrix[i, c_id] = -len(keywords & cluster_vocabs[c_id])

    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    label_to_raw = {}
    for li, ci in zip(row_ind, col_ind):
        label_to_raw[li] = ci

    # Remap: create new label array where label_index i -> semantic label i
    remapped_labels = np.empty_like(raw_labels)
    for li, raw_id in label_to_raw.items():
        remapped_labels[raw_labels == raw_id] = li

    return remapped_labels, X_pca, sil, pca, label_to_raw, cluster_vocabs


def profile_clusters(labels, df):
    """Compute per-cluster statistics."""
    clusters = []
    for c_id in range(15):
        mask = labels == c_id
        cdf = df[mask]
        n = int(mask.sum())
        if n == 0:
            continue

        cat_counts = cdf["category"].value_counts()
        factor_counts = cdf["factor"].value_counts()
        adj_counts = cdf["adjective"].value_counts()
        n_models = cdf["model"].nunique()

        dominant_cat = cat_counts.index[0]
        dominant_pct = round(100 * cat_counts.iloc[0] / n)
        top_adjs = [a for a in adj_counts.head(5).index if a and a != "nan"][:2]

        clusters.append({
            "id": c_id,
            "label": LABEL_SIGNATURES[c_id][0],
            "n": n,
            "n_categories": len(cat_counts),
            "n_models": n_models,
            "dominant_category": dominant_cat,
            "dominant_pct": dominant_pct,
            "top_adjectives": top_adjs,
            "category_breakdown": dict(cat_counts.items()),
            "top_factors": list(factor_counts.head(5).index),
            "categories_list": sorted(cat_counts.index),
        })

    return clusters


def main():
    parser = argparse.ArgumentParser(
        description="Generate SPA cluster table for Paper 1")
    parser.add_argument(
        "--output", "-o",
        default=os.path.join(SURVEY_ROOT, "results", "spa_table.json"),
        help="Output JSON path",
    )
    args = parser.parse_args()

    print(f"sklearn {sklearn.__version__}, numpy {np.__version__}")
    print("Pipeline: PCA-50 (no scaler) -> k-means k=15 "
          "(random_state=42, n_init=10, lloyd)")
    print("Label assignment: Hungarian optimal (content-based)\n")

    X, df = load_embeddings()
    print(f"Loaded {X.shape[0]} embeddings from {df['model'].nunique()} models")

    labels, X_pca, sil, pca, label_to_raw, vocabs = cluster_and_assign(X, df)
    print(f"Silhouette (k=15): {sil:.4f}")
    print(f"PCA variance explained: {100 * pca.explained_variance_ratio_.sum():.1f}%\n")

    # Show assignment
    print("Label assignment (Hungarian):")
    for li, raw_id in sorted(label_to_raw.items()):
        label = LABEL_SIGNATURES[li][0]
        keywords = LABEL_SIGNATURES[li][1]
        overlap = len(keywords & vocabs[raw_id])
        print(f"  C{li:2d} {label:<30} <- raw cluster {raw_id:2d} "
              f"(overlap: {overlap} keywords)")

    clusters = profile_clusters(labels, df)

    # Print table
    print(f"\n{'C':>3}  {'Label':<30} {'n':>5}  {'Cats':>4}  "
          f"{'Top Adjectives':<30}  {'Dominant'}")
    print("-" * 95)
    for c in clusters:
        adjs = ", ".join(c["top_adjectives"]) if c["top_adjectives"] else "N/A"
        dom = f"{c['dominant_category']} ({c['dominant_pct']}%)"
        print(f"C{c['id']:2d}  {c['label']:<30} {c['n']:5d}  "
              f"{c['n_categories']:4d}  {adjs:<30}  {dom}")

    # Summary
    cats_7 = [c for c in clusters if c["n_categories"] == 7]
    cats_6 = [c for c in clusters if c["n_categories"] == 6]
    print()
    for span, group in [(7, cats_7), (6, cats_6)]:
        if group:
            names = ", ".join(f"C{c['id']} ({c['label']})" for c in group)
            print(f"Span {span}/7: {names}")

    # Save
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    result = {
        "pipeline": {
            "sklearn_version": sklearn.__version__,
            "numpy_version": np.__version__,
            "n_embeddings": int(X.shape[0]),
            "embedding_dim": int(X.shape[1]),
            "n_models": df["model"].nunique(),
            "pca_components": 50,
            "pca_variance_explained": round(
                float(pca.explained_variance_ratio_.sum()), 4),
            "scaler": "none",
            "kmeans_k": 15,
            "kmeans_random_state": 42,
            "kmeans_n_init": 10,
            "kmeans_algorithm": "lloyd",
            "silhouette_k15": round(float(sil), 4),
        },
        "label_assignment": {
            LABEL_SIGNATURES[li][0]: int(raw_id)
            for li, raw_id in label_to_raw.items()
        },
        "clusters": clusters,
    }

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
