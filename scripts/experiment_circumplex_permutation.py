#!/usr/bin/env python3
"""R4-m2: Circumplex Permutation Baseline — Null distribution for the C0-C1
near-orthogonality finding.

The paper reports C0 (Warmth) and C1 (Dominance) have cosine similarity = 0.091
(angle = 84.8 deg). A reviewer asks: "How often would two random centroids from
this space be this close to 90 degrees?"

This script answers by computing:
1. All 105 pairwise cosine similarities between the 15 k-means centroids
2. Where |cos| = 0.091 falls in that empirical distribution
3. A 10,000-sample analytical baseline of random unit vectors in 50-dim space
"""

import os, json, csv, ast
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy import stats

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
    print("=== R4-m2: Circumplex Permutation Baseline ===\n")

    # --- Load and reduce ---
    all_emb, all_factors, all_models = load_all_embeddings()
    print(f"Loaded {len(all_emb)} embeddings from {len(set(all_models))} models")

    print("Running PCA-50...")
    pca = PCA(n_components=50, random_state=42)
    reduced = pca.fit_transform(all_emb)
    var_explained = float(pca.explained_variance_ratio_.sum())
    print(f"Variance explained by 50 components: {var_explained:.3f}")

    # --- K-means k=15 ---
    print("Running k-means (k=15)...")
    km = KMeans(n_clusters=15, random_state=42, n_init=10)
    km.fit(reduced)
    centroids = km.cluster_centers_

    # =========================================================
    # Part 1: All 105 pairwise cosine similarities
    # =========================================================
    print("\n--- Part 1: Empirical centroid pairwise distribution (105 pairs) ---")

    pairwise_cos = []
    pairwise_labels = []
    for i in range(15):
        for j in range(i + 1, 15):
            cos = cosine_similarity(centroids[i], centroids[j])
            pairwise_cos.append(cos)
            pairwise_labels.append(f"C{i}-C{j}")

    pairwise_arr = np.array(pairwise_cos)
    pairwise_abs = np.abs(pairwise_arr)

    print(f"  N pairs: {len(pairwise_cos)}")
    print(f"  Cosine similarity:")
    print(f"    Mean:   {pairwise_arr.mean():.4f}")
    print(f"    Std:    {pairwise_arr.std():.4f}")
    print(f"    Min:    {pairwise_arr.min():.4f}")
    print(f"    Max:    {pairwise_arr.max():.4f}")
    print(f"    Median: {float(np.median(pairwise_arr)):.4f}")
    print(f"  Percentiles: 5th={np.percentile(pairwise_arr, 5):.4f}, "
          f"25th={np.percentile(pairwise_arr, 25):.4f}, "
          f"75th={np.percentile(pairwise_arr, 75):.4f}, "
          f"95th={np.percentile(pairwise_arr, 95):.4f}")

    # |cosine| distribution (distance from orthogonality)
    print(f"\n  |Cosine| (distance from orthogonality):")
    print(f"    Mean:   {pairwise_abs.mean():.4f}")
    print(f"    Std:    {pairwise_abs.std():.4f}")
    print(f"    Median: {float(np.median(pairwise_abs)):.4f}")

    # =========================================================
    # Part 2: Where does C0-C1 (cos=0.091) fall?
    # =========================================================
    c0c1_cos = 0.091  # reported value
    # Also compute from actual centroids (clusters 14 and 7 from E4 results)
    c0c1_actual = cosine_similarity(centroids[14], centroids[7])
    print(f"\n--- Part 2: C0-C1 positioning ---")
    print(f"  C0-C1 cosine (from E4): {c0c1_cos:.4f}")
    print(f"  C0-C1 cosine (recomputed): {c0c1_actual:.4f}")

    # Percentile rank of the C0-C1 |cosine| in the |cosine| distribution
    # "What fraction of pairs have |cosine| <= |c0c1|?"
    c0c1_abs = abs(c0c1_actual)
    n_closer_to_orthogonal = int(np.sum(pairwise_abs <= c0c1_abs))
    pct_rank_abs = float(stats.percentileofscore(pairwise_abs, c0c1_abs, kind='weak'))

    # Percentile rank of raw cosine in the signed distribution
    pct_rank_signed = float(stats.percentileofscore(pairwise_arr, c0c1_actual, kind='weak'))

    print(f"  |C0-C1 cosine|: {c0c1_abs:.4f}")
    print(f"  Pairs with |cosine| <= {c0c1_abs:.4f}: {n_closer_to_orthogonal} / {len(pairwise_cos)}")
    print(f"  Percentile rank of |cos|={c0c1_abs:.4f} in |cosine| distribution: {pct_rank_abs:.1f}th")
    print(f"  Percentile rank of cos={c0c1_actual:.4f} in signed distribution: {pct_rank_signed:.1f}th")

    # Angle distribution
    angles = np.degrees(np.arccos(np.clip(pairwise_arr, -1, 1)))
    c0c1_angle = float(np.degrees(np.arccos(np.clip(c0c1_actual, -1, 1))))
    pct_rank_angle = float(stats.percentileofscore(angles, c0c1_angle, kind='weak'))
    print(f"\n  Angle distribution:")
    print(f"    Mean:   {angles.mean():.1f} deg")
    print(f"    Std:    {angles.std():.1f} deg")
    print(f"    Min:    {angles.min():.1f} deg (most aligned)")
    print(f"    Max:    {angles.max():.1f} deg (most opposed)")
    print(f"    C0-C1:  {c0c1_angle:.1f} deg (percentile: {pct_rank_angle:.1f}th)")

    # How many pairs are within +/- 5 degrees of 90?
    near_orthogonal = int(np.sum(np.abs(angles - 90) <= 5))
    print(f"    Pairs within 85-95 deg: {near_orthogonal} / {len(angles)}")

    # =========================================================
    # Part 3: Analytical baseline -- random unit vectors in 50-dim
    # =========================================================
    print("\n--- Part 3: Random unit vector baseline (50-dim, N=10,000) ---")
    rng = np.random.RandomState(42)
    n_random = 10000

    # Generate pairs of random unit vectors in 50-dim space
    # Random direction: sample from N(0,1) then normalize
    v1 = rng.randn(n_random, 50)
    v2 = rng.randn(n_random, 50)
    v1 = v1 / np.linalg.norm(v1, axis=1, keepdims=True)
    v2 = v2 / np.linalg.norm(v2, axis=1, keepdims=True)
    random_cos = np.sum(v1 * v2, axis=1)

    print(f"  Cosine similarity of random unit vector pairs:")
    print(f"    Mean:   {random_cos.mean():.4f}")
    print(f"    Std:    {random_cos.std():.4f}")
    print(f"    Min:    {random_cos.min():.4f}")
    print(f"    Max:    {random_cos.max():.4f}")
    print(f"    Median: {float(np.median(random_cos)):.4f}")

    random_abs = np.abs(random_cos)
    print(f"  |Cosine|:")
    print(f"    Mean:   {random_abs.mean():.4f}")
    print(f"    Std:    {random_abs.std():.4f}")
    print(f"    Median: {float(np.median(random_abs)):.4f}")

    # Theoretical expectation: for d-dim, E[cos^2] = 1/d, so E[|cos|] ~ sqrt(1/d)
    d = 50
    expected_abs_cos = np.sqrt(2 / (np.pi * d))  # E[|cos|] for d-dim
    print(f"\n  Theoretical E[|cos|] for d={d}: {expected_abs_cos:.4f}")
    print(f"  Empirical E[|cos|]:              {random_abs.mean():.4f}")

    # What fraction of random pairs have |cosine| <= 0.091?
    n_random_closer = int(np.sum(random_abs <= c0c1_abs))
    pct_random = float(stats.percentileofscore(random_abs, c0c1_abs, kind='weak'))
    print(f"\n  Random pairs with |cos| <= {c0c1_abs:.4f}: {n_random_closer} / {n_random} ({100*n_random_closer/n_random:.1f}%)")
    print(f"  Percentile rank of |cos|={c0c1_abs:.4f} in random distribution: {pct_random:.1f}th")

    random_angles = np.degrees(np.arccos(np.clip(random_cos, -1, 1)))
    near_orth_random = int(np.sum(np.abs(random_angles - 90) <= 5))
    print(f"  Random angles within 85-95 deg: {near_orth_random} / {n_random} ({100*near_orth_random/n_random:.1f}%)")

    # =========================================================
    # Interpretation
    # =========================================================
    print("\n" + "=" * 60)
    print("INTERPRETATION")
    print("=" * 60)

    if pct_rank_abs < 50:
        rank_desc = "below median"
        remarkable = "C0-C1 is MORE orthogonal than most centroid pairs"
    else:
        rank_desc = "above median"
        remarkable = "C0-C1 is LESS orthogonal than most centroid pairs"

    print(f"\n  C0-C1 |cosine| = {c0c1_abs:.4f} is at the {pct_rank_abs:.1f}th percentile")
    print(f"  of all 105 centroid pairs ({rank_desc}).")
    print(f"  {remarkable}.")
    print(f"\n  In the empirical distribution, {n_closer_to_orthogonal}/{len(pairwise_cos)} pairs")
    print(f"  ({100*n_closer_to_orthogonal/len(pairwise_cos):.1f}%) are closer to orthogonal than C0-C1.")
    print(f"\n  In 50-dim space, random unit vectors have E[|cos|] = {random_abs.mean():.4f},")
    print(f"  so near-orthogonality is {'the default' if random_abs.mean() < 0.2 else 'not automatic'}.")
    print(f"  {100*n_random_closer/n_random:.1f}% of random pairs have |cos| <= {c0c1_abs:.4f}.")

    is_remarkable = pct_rank_abs < 25  # in the bottom quartile
    if n_closer_to_orthogonal <= 10:
        verdict = "REMARKABLE: C0-C1 orthogonality is in the bottom decile of centroid pairs"
    elif is_remarkable:
        verdict = "NOTABLE: C0-C1 is more orthogonal than ~75% of centroid pairs"
    else:
        verdict = "EXPECTED: Near-orthogonality is common in high-dimensional spaces"

    print(f"\n  VERDICT: {verdict}")

    # =========================================================
    # Save results
    # =========================================================
    os.makedirs(RESULTS, exist_ok=True)

    results = {
        "experiment": "R4-m2: Circumplex Permutation Baseline",
        "question": "Is cos=0.091 between C0 (Warmth) and C1 (Dominance) remarkable?",
        "c0c1_cosine_reported": c0c1_cos,
        "c0c1_cosine_recomputed": round(c0c1_actual, 6),
        "c0c1_abs_cosine": round(c0c1_abs, 6),
        "c0c1_angle_degrees": round(c0c1_angle, 2),
        "empirical_centroid_distribution": {
            "n_pairs": len(pairwise_cos),
            "cosine_mean": round(float(pairwise_arr.mean()), 4),
            "cosine_std": round(float(pairwise_arr.std()), 4),
            "cosine_min": round(float(pairwise_arr.min()), 4),
            "cosine_max": round(float(pairwise_arr.max()), 4),
            "cosine_median": round(float(np.median(pairwise_arr)), 4),
            "cosine_p5": round(float(np.percentile(pairwise_arr, 5)), 4),
            "cosine_p25": round(float(np.percentile(pairwise_arr, 25)), 4),
            "cosine_p75": round(float(np.percentile(pairwise_arr, 75)), 4),
            "cosine_p95": round(float(np.percentile(pairwise_arr, 95)), 4),
            "abs_cosine_mean": round(float(pairwise_abs.mean()), 4),
            "abs_cosine_std": round(float(pairwise_abs.std()), 4),
            "abs_cosine_median": round(float(np.median(pairwise_abs)), 4),
            "angle_mean_degrees": round(float(angles.mean()), 2),
            "angle_std_degrees": round(float(angles.std()), 2),
            "pairs_within_85_95_deg": near_orthogonal,
        },
        "c0c1_vs_empirical": {
            "percentile_rank_abs_cosine": round(pct_rank_abs, 2),
            "percentile_rank_signed_cosine": round(pct_rank_signed, 2),
            "percentile_rank_angle": round(pct_rank_angle, 2),
            "n_pairs_closer_to_orthogonal": n_closer_to_orthogonal,
            "frac_pairs_closer_to_orthogonal": round(n_closer_to_orthogonal / len(pairwise_cos), 4),
        },
        "random_unit_vector_baseline": {
            "n_samples": n_random,
            "dimensionality": d,
            "cosine_mean": round(float(random_cos.mean()), 4),
            "cosine_std": round(float(random_cos.std()), 4),
            "abs_cosine_mean": round(float(random_abs.mean()), 4),
            "abs_cosine_std": round(float(random_abs.std()), 4),
            "theoretical_expected_abs_cosine": round(expected_abs_cos, 4),
            "frac_with_abs_cos_leq_c0c1": round(n_random_closer / n_random, 4),
            "pct_within_85_95_deg": round(100 * near_orth_random / n_random, 2),
        },
        "verdict": verdict,
        "pca_variance_explained_50": round(var_explained, 4),
    }

    out_path = f"{RESULTS}/r4m2_circumplex_permutation.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
