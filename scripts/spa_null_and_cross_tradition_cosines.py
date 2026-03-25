#!/usr/bin/env python3
"""Cross-tradition jangle cosine pairs + random-partition null silhouette.

Part 1: Find highest-cosine factor centroid pairs across different disciplinary
categories (true cross-tradition jangle, not within-narcissism pairs).

Part 2: Compare actual silhouette scores (7-category, k=15 k-means) against
1000-trial random-partition nulls with matched size distributions.

Output: survey/results/reviewer_experiments/spa_null_and_jangle.json
"""

import os, json, csv, time
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, pairwise_distances

SURVEY = "/Users/jsr/Documents/GitHub/survey"
EMB_DIR = f"{SURVEY}/Embeddings"
RESULTS = f"{SURVEY}/results/reviewer_experiments"

# Exact category mapping (matches experiment_variance_bootstrap.py)
MODEL_CATEGORIES = {
    # 1. Trait-Based (6)
    "ocean": "Trait-Based", "hex": "Trait-Based",
    "epm": "Trait-Based", "sixteenpf": "Trait-Based", "mbti": "Trait-Based",
    "ftm": "Trait-Based",
    # 2. Narcissism-Based (10)
    "npi": "Narcissism-Based", "narq": "Narcissism-Based", "ffni": "Narcissism-Based",
    "hsns": "Narcissism-Based", "pni": "Narcissism-Based", "mcmin": "Narcissism-Based",
    "ffni_sf": "Narcissism-Based", "ipn": "Narcissism-Based",
    "dtm": "Narcissism-Based", "dt4": "Narcissism-Based",
    # 3. Motivational & Value (6)
    "aam": "Motivational", "mst": "Motivational", "rft": "Motivational",
    "sdt": "Motivational", "stbv": "Motivational", "cs": "Motivational",
    # 4. Cognitive & Learning (4)
    "pct": "Cognitive", "scm": "Cognitive", "cest": "Cognitive", "fsls": "Cognitive",
    # 5. Clinical & Health (10)
    "mmpi": "Clinical", "tci": "Clinical", "tmp": "Clinical", "bdi": "Clinical",
    "gad7": "Clinical", "scid": "Clinical", "mcmi": "Clinical",
    "rit": "Clinical", "tat": "Clinical", "wais": "Clinical",
    # 6. Interpersonal & Conflict (2)
    "tki": "Interpersonal", "disc": "Interpersonal",
    # 7. Application & Holistic (6)
    "riasec": "App/Holistic", "bt": "App/Holistic", "tei": "App/Holistic",
    "em": "App/Holistic", "papc": "App/Holistic", "cmoa": "App/Holistic",
}


def load_all_embeddings():
    """Load all model embeddings. Uses csv.DictReader + json.loads (7x faster than ast)."""
    t0 = time.time()
    all_emb = []
    all_model_keys = []
    all_factors = []

    for fname in sorted(os.listdir(EMB_DIR)):
        if not fname.endswith("_embeddings.csv") or "clustered" in fname:
            continue
        model_key = fname.replace("_embeddings.csv", "")
        if model_key not in MODEL_CATEGORIES:
            print(f"  Warning: {model_key} not in category map, skipping")
            continue

        with open(f"{EMB_DIR}/{fname}") as f:
            reader = csv.DictReader(f)
            for row in reader:
                emb = json.loads(row["Embedding"])
                all_emb.append(emb)
                all_model_keys.append(model_key)
                all_factors.append(row["Factor"])

    X = np.array(all_emb, dtype=np.float32)
    print(f"  Loaded {X.shape[0]} embeddings in {time.time()-t0:.1f}s")
    return X, all_model_keys, all_factors


def compute_centroids_and_cosines(X, model_keys, factors):
    """Compute factor centroids, then vectorized cosine similarity matrix."""
    # Build centroids
    centroid_map = {}
    for i, (mk, f) in enumerate(zip(model_keys, factors)):
        key = (mk, f)
        if key not in centroid_map:
            centroid_map[key] = []
        centroid_map[key].append(i)

    keys = sorted(centroid_map.keys())
    n_centroids = len(keys)
    dim = X.shape[1]

    C = np.zeros((n_centroids, dim), dtype=np.float32)
    for i, key in enumerate(keys):
        indices = centroid_map[key]
        C[i] = X[indices].mean(axis=0)

    # Normalize for cosine similarity
    C_norm = normalize(C)

    # Full cosine similarity matrix (vectorized, fast)
    cos_matrix = C_norm @ C_norm.T

    return keys, C, cos_matrix


def find_cross_tradition_pairs(keys, cos_matrix, top_n=20):
    """Extract top cross-tradition pairs from precomputed cosine matrix."""
    n = len(keys)

    # Build category lookup
    key_cats = [MODEL_CATEGORIES[k[0]] for k in keys]

    # Collect cross-tradition pairs efficiently
    # Use upper triangle only
    positive_pairs = []
    negative_pairs = []

    for i in range(n):
        mk_i, f_i = keys[i]
        cat_i = key_cats[i]
        for j in range(i + 1, n):
            mk_j, f_j = keys[j]
            cat_j = key_cats[j]

            # Must be different models AND different categories
            if mk_i == mk_j or cat_i == cat_j:
                continue

            sim = float(cos_matrix[i, j])

            entry = {
                "factor_a": f"{mk_i.upper()} {f_i}",
                "factor_b": f"{mk_j.upper()} {f_j}",
                "category_a": cat_i,
                "category_b": cat_j,
                "cosine": round(sim, 4),
            }

            if sim > 0:
                positive_pairs.append((sim, entry))
            else:
                negative_pairs.append((sim, entry))

    # Sort and take top_n
    positive_pairs.sort(key=lambda x: x[0], reverse=True)
    negative_pairs.sort(key=lambda x: x[0])  # most negative first

    top_pos = [e for _, e in positive_pairs[:top_n]]
    top_neg = [e for _, e in negative_pairs[:top_n]]

    return top_pos, top_neg


def lookup_specific_pair(keys, cos_matrix, mk_a, f_a, mk_b, f_b):
    """Look up cosine for a specific pair."""
    key_a = (mk_a, f_a)
    key_b = (mk_b, f_b)
    if key_a in keys and key_b in keys:
        i = keys.index(key_a)
        j = keys.index(key_b)
        return float(cos_matrix[i, j])
    return None


def random_partition_silhouette(D, actual_labels, n_trials=1000, seed=42):
    """Silhouette for random partitions matching actual label size distribution.

    Args:
        D: Precomputed distance matrix (n x n).
        actual_labels: Integer label array.
        n_trials: Number of random partition trials.
        seed: Random seed.
    """
    rng = np.random.RandomState(seed)
    n = D.shape[0]

    # Get actual size distribution
    unique_labels, counts = np.unique(actual_labels, return_counts=True)
    k = len(unique_labels)
    sizes = sorted(counts.tolist())

    # Actual silhouette (precomputed distances)
    actual_sil = silhouette_score(D, actual_labels, metric="precomputed")

    # Random null trials
    null_sils = []
    t0 = time.time()
    for t in range(n_trials):
        if (t + 1) % 200 == 0:
            elapsed = time.time() - t0
            rate = (t + 1) / elapsed
            eta = (n_trials - t - 1) / rate
            print(f"      trial {t+1}/{n_trials}  ({rate:.1f} trials/s, ETA {eta:.0f}s)")
        perm = rng.permutation(n)
        random_labels = np.empty(n, dtype=int)
        offset = 0
        for label_idx, sz in enumerate(sizes):
            random_labels[perm[offset:offset + sz]] = label_idx
            offset += sz
        null_sils.append(silhouette_score(D, random_labels, metric="precomputed"))

    null_sils = np.array(null_sils)
    null_mean = float(np.mean(null_sils))
    null_std = float(np.std(null_sils))
    ci_lo = float(np.percentile(null_sils, 2.5))
    ci_hi = float(np.percentile(null_sils, 97.5))
    p_value = float(np.mean(null_sils >= actual_sil))

    return {
        "actual_silhouette": round(actual_sil, 4),
        "null_mean": round(null_mean, 4),
        "null_std": round(null_std, 4),
        "null_95ci": [round(ci_lo, 4), round(ci_hi, 4)],
        "p_value": round(p_value, 4),
        "n_trials": n_trials,
        "k": k,
        "size_distribution": sizes,
        "ratio_actual_to_null": round(actual_sil / null_mean if null_mean != 0 else float("inf"), 2),
    }


def main():
    t_start = time.time()
    print("Loading all embeddings...")
    X_raw, model_keys, factors = load_all_embeddings()
    print(f"  {X_raw.shape[0]} embeddings, {X_raw.shape[1]} dimensions")
    print(f"  Models: {len(set(model_keys))}, Categories: {len(set(MODEL_CATEGORIES[mk] for mk in set(model_keys)))}")

    # ================================================================
    # Part 1: Cross-tradition jangle cosine pairs
    # ================================================================
    print("\n=== PART 1: Cross-tradition jangle cosine pairs ===")
    t1 = time.time()
    keys, C, cos_matrix = compute_centroids_and_cosines(X_raw, model_keys, factors)
    print(f"  Computed {len(keys)} factor centroids, cosine matrix in {time.time()-t1:.1f}s")

    top_positive, top_negative = find_cross_tradition_pairs(keys, cos_matrix, top_n=20)

    print(f"\n  Top 20 cross-tradition POSITIVE cosine pairs (jangle candidates):")
    for i, p in enumerate(top_positive):
        print(f"    {i+1:2d}. {p['factor_a']:45s} <-> {p['factor_b']:45s}  cos={p['cosine']:.4f}  ({p['category_a']} vs {p['category_b']})")

    print(f"\n  Top 20 cross-tradition NEGATIVE cosine pairs (anti-correlated):")
    for i, p in enumerate(top_negative):
        print(f"    {i+1:2d}. {p['factor_a']:45s} <-> {p['factor_b']:45s}  cos={p['cosine']:.4f}  ({p['category_a']} vs {p['category_b']})")

    # Specific pairs of interest
    print("\n  Specific pairs of interest:")
    interesting = [
        ("ocean", "Neuroticism", "tci", "Harm Avoidance"),
        ("ocean", "Agreeableness", "sdt", "Relatedness"),
        ("ocean", "Conscientiousness", "sdt", "Competence"),
        ("hex", "Honesty-Humility", "dt4", "Machiavellianism"),
        ("ocean", "Openness", "tci", "Novelty Seeking"),
        ("ocean", "Extraversion", "riasec", "Social"),
        ("ocean", "Neuroticism", "bdi", "Sadness"),
        ("ocean", "Conscientiousness", "riasec", "Conventional"),
    ]
    specific_results = []
    keys_list = list(keys)
    for mk_a, f_a, mk_b, f_b in interesting:
        key_a = (mk_a, f_a)
        key_b = (mk_b, f_b)
        if key_a in keys_list and key_b in keys_list:
            idx_a = keys_list.index(key_a)
            idx_b = keys_list.index(key_b)
            sim = float(cos_matrix[idx_a, idx_b])
            cat_a = MODEL_CATEGORIES[mk_a]
            cat_b = MODEL_CATEGORIES[mk_b]
            print(f"    {mk_a.upper()} {f_a} <-> {mk_b.upper()} {f_b}: cos={sim:.4f} ({cat_a} vs {cat_b})")
            specific_results.append({
                "factor_a": f"{mk_a.upper()} {f_a}",
                "factor_b": f"{mk_b.upper()} {f_b}",
                "category_a": cat_a,
                "category_b": cat_b,
                "cosine": round(sim, 4),
            })
        else:
            miss = []
            if key_a not in keys_list:
                miss.append(f"{mk_a}/{f_a}")
            if key_b not in keys_list:
                miss.append(f"{mk_b}/{f_b}")
            print(f"    MISSING: {', '.join(miss)}")

    # ================================================================
    # Part 2: Random-partition null silhouette
    # ================================================================
    print("\n=== PART 2: Random-partition null silhouette ===")

    # PCA to 50 dims (matching paper methodology)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw)
    pca = PCA(n_components=50, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    var_explained = float(np.sum(pca.explained_variance_ratio_))
    print(f"  PCA 50 dims: {var_explained:.1%} variance explained")

    # Precompute distance matrix for fast repeated silhouette
    print("  Precomputing pairwise distance matrix...")
    t_dist = time.time()
    D = pairwise_distances(X_pca, metric="euclidean").astype(np.float32)
    print(f"  Distance matrix: {D.shape}, {D.nbytes/1e6:.0f}MB, {time.time()-t_dist:.1f}s")

    # 2a. Actual silhouette for 7 disciplinary categories
    print("\n  2a. 7-category disciplinary silhouette (1000 null trials):")
    cat_labels = np.array([MODEL_CATEGORIES[mk] for mk in model_keys])
    unique_cats = sorted(set(cat_labels))
    cat_label_ints = np.array([unique_cats.index(c) for c in cat_labels])

    result_7cat = random_partition_silhouette(D, cat_label_ints, n_trials=1000)
    print(f"    Actual silhouette:  {result_7cat['actual_silhouette']:.4f}")
    print(f"    Null mean (1000x):  {result_7cat['null_mean']:.4f} +/- {result_7cat['null_std']:.4f}")
    print(f"    Null 95% CI:        [{result_7cat['null_95ci'][0]:.4f}, {result_7cat['null_95ci'][1]:.4f}]")
    print(f"    Ratio actual/null:  {result_7cat['ratio_actual_to_null']:.2f}x")
    print(f"    p-value:            {result_7cat['p_value']:.4f}")

    # 2b. k-means k=15 silhouette
    print("\n  2b. k-means k=15 silhouette (1000 null trials):")
    kmeans = KMeans(n_clusters=15, random_state=42, n_init=10)
    km_labels = kmeans.fit_predict(X_pca)

    result_k15 = random_partition_silhouette(D, km_labels, n_trials=1000)
    print(f"    Actual silhouette:  {result_k15['actual_silhouette']:.4f}")
    print(f"    Null mean (1000x):  {result_k15['null_mean']:.4f} +/- {result_k15['null_std']:.4f}")
    print(f"    Null 95% CI:        [{result_k15['null_95ci'][0]:.4f}, {result_k15['null_95ci'][1]:.4f}]")
    print(f"    Ratio actual/null:  {result_k15['ratio_actual_to_null']:.2f}x")
    print(f"    p-value:            {result_k15['p_value']:.4f}")

    # ================================================================
    # Save results
    # ================================================================
    os.makedirs(RESULTS, exist_ok=True)

    output = {
        "description": "Cross-tradition jangle cosine pairs and random-partition null silhouette",
        "n_embeddings": int(X_raw.shape[0]),
        "n_dimensions_raw": int(X_raw.shape[1]),
        "n_pca_dims": 50,
        "pca_variance_explained": round(var_explained, 4),
        "part1_cross_tradition_jangle": {
            "description": "Factor centroid cosine similarities across different disciplinary categories",
            "n_factor_centroids": len(keys),
            "top_20_positive": top_positive,
            "top_20_negative": top_negative,
            "specific_pairs_of_interest": specific_results,
        },
        "part2_null_silhouette": {
            "seven_category": {
                "description": "7 disciplinary categories vs random partition null (k=7)",
                "categories": unique_cats,
                **result_7cat,
            },
            "kmeans_k15": {
                "description": "k-means k=15 vs random partition null (k=15)",
                **result_k15,
            },
        },
    }

    outpath = f"{RESULTS}/spa_null_and_jangle.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)

    elapsed = time.time() - t_start
    print(f"\n  Results saved to {outpath}")

    # Summary
    print(f"\n=== SUMMARY (elapsed: {elapsed:.0f}s) ===")
    print(f"Best cross-tradition jangle pair: {top_positive[0]['factor_a']} <-> {top_positive[0]['factor_b']} (cos={top_positive[0]['cosine']:.4f})")
    print(f"7-cat silhouette: actual={result_7cat['actual_silhouette']:.4f} vs null={result_7cat['null_mean']:.4f} ({result_7cat['ratio_actual_to_null']:.1f}x, p={result_7cat['p_value']:.4f})")
    print(f"k=15 silhouette:  actual={result_k15['actual_silhouette']:.4f} vs null={result_k15['null_mean']:.4f} ({result_k15['ratio_actual_to_null']:.1f}x, p={result_k15['p_value']:.4f})")


if __name__ == "__main__":
    main()
