#!/usr/bin/env python3
"""E4: Circumplex Orthogonality — Quantitative test of C0 (Warmth) and C1
(Dominance) near-orthogonality in the SPI embedding space.

Loads embeddings, runs PCA-50, k-means k=15, computes centroid vectors for
C0 and C1, reports cosine similarity and angle.
"""

import os, json, csv, ast
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

SURVEY = "/Users/jsr/Documents/GitHub/survey"
RESULTS = f"{SURVEY}/results/reviewer_experiments"


def load_all_embeddings():
    """Load all embeddings into a single matrix with metadata."""
    emb_dir = f"{SURVEY}/Embeddings"
    all_emb, all_factors, all_models = [], [], []

    for fname in sorted(os.listdir(emb_dir)):
        if not fname.endswith("_embeddings.csv") or "clustered" in fname:
            continue
        model_key = fname.replace("_embeddings.csv", "")
        with open(f"{emb_dir}/{fname}") as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_factors.append(row["Factor"])
                all_models.append(model_key)
                emb = ast.literal_eval(row["Embedding"])
                all_emb.append(emb)

    return np.array(all_emb), all_factors, all_models


def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def main():
    print("=== E4: Circumplex Orthogonality ===\n")

    all_emb, all_factors, all_models = load_all_embeddings()
    print(f"Loaded {len(all_emb)} embeddings from {len(set(all_models))} models")

    # PCA to 50 dims
    print("Running PCA-50...")
    pca = PCA(n_components=50, random_state=42)
    reduced = pca.fit_transform(all_emb)
    print(f"Variance explained by 50 components: {pca.explained_variance_ratio_.sum():.3f}")

    # k-means k=15
    print("Running k-means (k=15)...")
    km = KMeans(n_clusters=15, random_state=42, n_init=10)
    labels = km.fit_predict(reduced)
    centroids = km.cluster_centers_

    # Identify C0 (Warmth) and C1 (Dominance) by examining cluster contents
    # We'll label clusters by their dominant adjective vocabulary
    # First, get top factors per cluster
    cluster_factors = {i: [] for i in range(15)}
    for i, factor in enumerate(all_factors):
        cluster_factors[labels[i]].append(factor)

    # Score clusters for Warmth and Dominance keywords
    warmth_keywords = {"empathetic", "cooperative", "kind", "sympathetic", "warm",
                       "caring", "generous", "compassionate", "agreeable", "friendly",
                       "agreeableness", "warmth", "prosocial"}
    dominance_keywords = {"assertive", "dominant", "persistent", "ambitious", "competitive",
                          "forceful", "commanding", "leadership", "authority", "power",
                          "dominance", "extraversion", "agency"}

    warmth_scores = {}
    dominance_scores = {}

    for c_id in range(15):
        factors_lower = [f.lower() for f in cluster_factors[c_id]]
        w_count = sum(1 for f in factors_lower if any(kw in f for kw in warmth_keywords))
        d_count = sum(1 for f in factors_lower if any(kw in f for kw in dominance_keywords))
        warmth_scores[c_id] = w_count / max(len(factors_lower), 1)
        dominance_scores[c_id] = d_count / max(len(factors_lower), 1)

    c0_id = max(warmth_scores, key=warmth_scores.get)
    c1_id = max(dominance_scores, key=dominance_scores.get)

    # If they're the same cluster, pick second-best for dominance
    if c0_id == c1_id:
        sorted_dom = sorted(dominance_scores, key=dominance_scores.get, reverse=True)
        c1_id = sorted_dom[1]

    print(f"\nCluster identification:")
    print(f"  C0 (Warmth): cluster {c0_id} (score={warmth_scores[c0_id]:.3f}, n={len(cluster_factors[c0_id])})")
    print(f"  C1 (Dominance): cluster {c1_id} (score={dominance_scores[c1_id]:.3f}, n={len(cluster_factors[c1_id])})")

    # Top factors in each
    from collections import Counter
    c0_top = Counter(cluster_factors[c0_id]).most_common(5)
    c1_top = Counter(cluster_factors[c1_id]).most_common(5)
    print(f"  C0 top factors: {c0_top}")
    print(f"  C1 top factors: {c1_top}")

    # Compute cosine similarity between centroids
    c0_centroid = centroids[c0_id]
    c1_centroid = centroids[c1_id]
    cos_sim = cosine_similarity(c0_centroid, c1_centroid)
    angle_rad = np.arccos(np.clip(cos_sim, -1, 1))
    angle_deg = float(np.degrees(angle_rad))

    print(f"\n=== Circumplex Orthogonality ===")
    print(f"C0-C1 cosine similarity: {cos_sim:.4f}")
    print(f"C0-C1 angle: {angle_deg:.1f} degrees")
    print(f"Perfect orthogonality would be 0.0 cosine / 90.0 degrees")

    # Context: median pairwise cosine similarity across all 15 centroids
    pairwise_cos = []
    for i in range(15):
        for j in range(i + 1, 15):
            pairwise_cos.append(cosine_similarity(centroids[i], centroids[j]))

    median_cos = float(np.median(pairwise_cos))
    mean_cos = float(np.mean(pairwise_cos))

    print(f"\nContext (all 15 centroid pairs):")
    print(f"  Median pairwise cosine: {median_cos:.4f}")
    print(f"  Mean pairwise cosine: {mean_cos:.4f}")
    print(f"  Min: {min(pairwise_cos):.4f}, Max: {max(pairwise_cos):.4f}")
    print(f"  C0-C1 is {'below' if cos_sim < median_cos else 'above'} median")

    # Count categories spanned by C0 and C1
    from experiment_variance_bootstrap import MODEL_CATEGORIES
    c0_cats = set()
    c1_cats = set()
    for i in range(len(all_models)):
        if labels[i] == c0_id and all_models[i] in MODEL_CATEGORIES:
            c0_cats.add(MODEL_CATEGORIES[all_models[i]])
        elif labels[i] == c1_id and all_models[i] in MODEL_CATEGORIES:
            c1_cats.add(MODEL_CATEGORIES[all_models[i]])

    print(f"\n  C0 spans {len(c0_cats)} categories: {sorted(c0_cats)}")
    print(f"  C1 spans {len(c1_cats)} categories: {sorted(c1_cats)}")

    results = {
        "c0_cluster_id": int(c0_id),
        "c1_cluster_id": int(c1_id),
        "c0_n": len(cluster_factors[c0_id]),
        "c1_n": len(cluster_factors[c1_id]),
        "c0_top_factors": c0_top,
        "c1_top_factors": c1_top,
        "c0_categories_spanned": sorted(list(c0_cats)),
        "c1_categories_spanned": sorted(list(c1_cats)),
        "cosine_similarity": cos_sim,
        "angle_degrees": angle_deg,
        "median_pairwise_cosine": median_cos,
        "mean_pairwise_cosine": mean_cos,
        "min_pairwise_cosine": float(min(pairwise_cos)),
        "max_pairwise_cosine": float(max(pairwise_cos)),
        "pca_variance_explained_50": float(pca.explained_variance_ratio_.sum()),
        "interpretation": f"C0 and C1 are {'near-orthogonal' if abs(cos_sim) < 0.3 else 'not orthogonal'} (cosine={cos_sim:.4f}, angle={angle_deg:.1f} deg)"
    }

    out_path = f"{RESULTS}/e4_circumplex_orthogonality.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
