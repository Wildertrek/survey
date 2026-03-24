#!/usr/bin/env python3
"""R3-M3: K-Means Stability Test — Run k-means 100 times with different random
seeds on the same PCA-50 embeddings. Report ARI distribution to determine
whether the 15-cluster SPA structure is stable.
"""

import os, json, csv, ast
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

SURVEY = "/Users/jsr/Documents/GitHub/survey"
RESULTS = f"{SURVEY}/results/reviewer_experiments"


def load_all_embeddings():
    emb_dir = f"{SURVEY}/Embeddings"
    all_emb = []
    for fname in sorted(os.listdir(emb_dir)):
        if not fname.endswith("_embeddings.csv") or "clustered" in fname:
            continue
        with open(f"{emb_dir}/{fname}") as f:
            reader = csv.DictReader(f)
            for row in reader:
                emb = ast.literal_eval(row["Embedding"])
                all_emb.append(emb)
    return np.array(all_emb)


def main():
    print("=== R3-M3: K-Means Stability Test ===\n")

    all_emb = load_all_embeddings()
    print(f"Loaded {len(all_emb)} embeddings")

    print("Running PCA-50...")
    pca = PCA(n_components=50, random_state=42)
    reduced = pca.fit_transform(all_emb)

    n_runs = 100
    k = 15
    print(f"Running k-means (k={k}) {n_runs} times with different random seeds...\n")

    all_labels = []
    all_inertias = []

    for seed in range(n_runs):
        km = KMeans(n_clusters=k, random_state=seed, n_init=10)
        labels = km.fit_predict(reduced)
        all_labels.append(labels)
        all_inertias.append(km.inertia_)

    # Compute pairwise ARI between all runs
    ari_values = []
    for i in range(n_runs):
        for j in range(i + 1, n_runs):
            ari = adjusted_rand_score(all_labels[i], all_labels[j])
            ari_values.append(ari)

    ari_arr = np.array(ari_values)

    # Also compute ARI between each run and the "canonical" run (seed=42)
    # seed=42 is index 42 in our array
    canonical_idx = 42
    ari_vs_canonical = []
    for i in range(n_runs):
        if i != canonical_idx:
            ari = adjusted_rand_score(all_labels[canonical_idx], all_labels[i])
            ari_vs_canonical.append(ari)

    ari_canon_arr = np.array(ari_vs_canonical)

    # Identify which clusters are stable
    # For each run, match clusters to canonical via best ARI alignment
    from scipy.optimize import linear_sum_assignment

    canonical_labels = all_labels[canonical_idx]
    cluster_stability = {c: 0 for c in range(k)}

    for i in range(n_runs):
        if i == canonical_idx:
            continue
        # Build confusion matrix between canonical and this run
        confusion = np.zeros((k, k), dtype=int)
        for pt in range(len(canonical_labels)):
            confusion[canonical_labels[pt], all_labels[i][pt]] += 1
        # Hungarian matching to find best alignment
        row_ind, col_ind = linear_sum_assignment(-confusion)
        # For each canonical cluster, count how many points match
        for c_canon, c_run in zip(row_ind, col_ind):
            overlap = confusion[c_canon, c_run]
            total = confusion[c_canon, :].sum()
            if total > 0 and overlap / total > 0.8:
                cluster_stability[c_canon] += 1

    # Normalize to percentage of runs
    for c in cluster_stability:
        cluster_stability[c] = round(cluster_stability[c] / (n_runs - 1) * 100, 1)

    print(f"=== R3-M3 RESULTS ===")
    print(f"Pairwise ARI ({len(ari_values)} pairs):")
    print(f"  Mean: {ari_arr.mean():.4f}")
    print(f"  Median: {np.median(ari_arr):.4f}")
    print(f"  Std: {ari_arr.std():.4f}")
    print(f"  Min: {ari_arr.min():.4f}, Max: {ari_arr.max():.4f}")
    print(f"  95% CI: [{np.percentile(ari_arr, 2.5):.4f}, {np.percentile(ari_arr, 97.5):.4f}]")
    print(f"\nARI vs canonical (seed=42, {len(ari_vs_canonical)} comparisons):")
    print(f"  Mean: {ari_canon_arr.mean():.4f}")
    print(f"  Min: {ari_canon_arr.min():.4f}, Max: {ari_canon_arr.max():.4f}")

    print(f"\nPer-cluster stability (>80% point overlap in >X% of runs):")
    for c in sorted(cluster_stability, key=cluster_stability.get, reverse=True):
        status = "STABLE" if cluster_stability[c] > 80 else ("MODERATE" if cluster_stability[c] > 50 else "UNSTABLE")
        print(f"  C{c}: {cluster_stability[c]:.0f}% of runs  [{status}]")

    stable_count = sum(1 for v in cluster_stability.values() if v > 80)
    moderate_count = sum(1 for v in cluster_stability.values() if 50 < v <= 80)
    unstable_count = sum(1 for v in cluster_stability.values() if v <= 50)

    interpretation = (
        f"K-means at k=15 is {'highly stable' if ari_arr.mean() > 0.8 else 'moderately stable' if ari_arr.mean() > 0.6 else 'unstable'} "
        f"across random initializations (mean ARI={ari_arr.mean():.3f}). "
        f"{stable_count} of 15 clusters are stable (>80% point overlap), "
        f"{moderate_count} moderate, {unstable_count} unstable."
    )
    print(f"\nInterpretation: {interpretation}")

    results = {
        "n_runs": n_runs,
        "k": k,
        "n_embeddings": len(all_emb),
        "pairwise_ari": {
            "mean": round(float(ari_arr.mean()), 4),
            "median": round(float(np.median(ari_arr)), 4),
            "std": round(float(ari_arr.std()), 4),
            "min": round(float(ari_arr.min()), 4),
            "max": round(float(ari_arr.max()), 4),
            "ci_lower": round(float(np.percentile(ari_arr, 2.5)), 4),
            "ci_upper": round(float(np.percentile(ari_arr, 97.5)), 4),
        },
        "ari_vs_canonical": {
            "mean": round(float(ari_canon_arr.mean()), 4),
            "min": round(float(ari_canon_arr.min()), 4),
            "max": round(float(ari_canon_arr.max()), 4),
        },
        "per_cluster_stability_pct": {f"C{k}": v for k, v in cluster_stability.items()},
        "stable_clusters": stable_count,
        "moderate_clusters": moderate_count,
        "unstable_clusters": unstable_count,
        "inertia_mean": round(float(np.mean(all_inertias)), 1),
        "inertia_std": round(float(np.std(all_inertias)), 1),
        "interpretation": interpretation,
    }

    out_path = f"{RESULTS}/r3m3_kmeans_stability.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
