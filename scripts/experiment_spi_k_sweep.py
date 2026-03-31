"""
SPI k-sweep: silhouette, Calinski-Harabasz, Davies-Bouldin for k=2..30.
Also runs R5.4 null model: shuffle category labels and check cluster span.

Uses same canonical pipeline as generate_spi_table.py:
  PCA-50 (no StandardScaler, random_state=42) -> k-means (n_init=10, lloyd)
"""

import os, json, csv, ast
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

SURVEY = "/Users/jsr/Documents/GitHub/survey"
EMBEDDINGS = f"{SURVEY}/Embeddings"
DATASETS = f"{SURVEY}/datasets"
RESULTS = f"{SURVEY}/results/reviewer_experiments"

MODEL_CATEGORIES = {
    "ocean": "Trait-Based", "mbti": "Trait-Based", "hexaco": "Trait-Based",
    "epm": "Trait-Based", "16pf": "Trait-Based", "ftm": "Trait-Based",
    "npi": "Narcissism-Based", "pni": "Narcissism-Based", "ffni": "Narcissism-Based",
    "ffni_sf": "Narcissism-Based", "narq": "Narcissism-Based", "hsns": "Narcissism-Based",
    "dtm": "Narcissism-Based", "dt4": "Narcissism-Based", "mcmin": "Narcissism-Based",
    "ipn": "Narcissism-Based",
    "stbv": "Motivational/Value", "mst": "Motivational/Value", "rft": "Motivational/Value",
    "sdt": "Motivational/Value", "aam": "Motivational/Value", "clifton": "Motivational/Value",
    "pct": "Cognitive/Learning", "scm": "Cognitive/Learning", "cest": "Cognitive/Learning",
    "fsls": "Cognitive/Learning",
    "mmpi": "Clinical/Health", "tci": "Clinical/Health", "tmp": "Clinical/Health",
    "bdi": "Clinical/Health", "gad7": "Clinical/Health", "scid": "Clinical/Health",
    "mcmi": "Clinical/Health", "rit": "Clinical/Health", "tat": "Clinical/Health",
    "wais": "Clinical/Health",
    "tki": "Interpersonal/Conflict", "disc": "Interpersonal/Conflict",
    "riasec": "Application-Specific/Holistic", "bt": "Application-Specific/Holistic",
    "tei": "Application-Specific/Holistic", "em": "Application-Specific/Holistic",
    "papc": "Application-Specific/Holistic", "cmoa": "Application-Specific/Holistic",
}


def load_all_embeddings():
    """Load all embeddings with model keys and categories."""
    all_emb, all_cats = [], []
    for fname in sorted(os.listdir(DATASETS)):
        if not fname.endswith(".csv"):
            continue
        model_key = fname.replace(".csv", "")
        emb_file = f"{EMBEDDINGS}/{model_key}_embeddings.csv"
        if not os.path.exists(emb_file):
            continue
        cat = MODEL_CATEGORIES.get(model_key, "Unknown")
        with open(emb_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_emb.append(ast.literal_eval(row["Embedding"]))
                all_cats.append(cat)
    return np.array(all_emb), np.array(all_cats)


def main():
    os.makedirs(RESULTS, exist_ok=True)

    print("Loading embeddings...")
    X_raw, categories = load_all_embeddings()
    print(f"Loaded {len(X_raw)} embeddings, {len(set(categories))} categories")

    # PCA-50 (canonical pipeline, no scaling)
    pca = PCA(n_components=50, random_state=42)
    X = pca.fit_transform(X_raw)
    pca_var = float(np.sum(pca.explained_variance_ratio_))
    print(f"PCA-50 variance explained: {pca_var:.4f}")

    # --- k-sweep ---
    k_range = list(range(2, 31))
    results = {
        "description": "SPI k-sweep: silhouette, CH, DB for k=2..30",
        "n_embeddings": len(X),
        "pca_components": 50,
        "pca_variance_explained": round(pca_var, 4),
        "k_sweep": [],
    }

    print("Running k-sweep...")
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10, algorithm="lloyd")
        labels = km.fit_predict(X)
        sil = silhouette_score(X, labels)
        ch = calinski_harabasz_score(X, labels)
        db = davies_bouldin_score(X, labels)

        # Count how many of the 7 categories each cluster spans
        unique_cats = sorted(set(categories))
        cats_per_cluster = []
        clusters_spanning_all = 0
        for ci in range(k):
            mask = labels == ci
            cluster_cats = set(categories[mask])
            cats_per_cluster.append(len(cluster_cats))
            if len(cluster_cats) == len(unique_cats):
                clusters_spanning_all += 1

        entry = {
            "k": k,
            "silhouette": round(float(sil), 4),
            "calinski_harabasz": round(float(ch), 2),
            "davies_bouldin": round(float(db), 4),
            "inertia": round(float(km.inertia_), 2),
            "clusters_spanning_all_7": clusters_spanning_all,
            "mean_cats_per_cluster": round(float(np.mean(cats_per_cluster)), 2),
            "max_cats_per_cluster": max(cats_per_cluster),
        }
        results["k_sweep"].append(entry)
        print(f"  k={k:2d}: sil={sil:.4f}, CH={ch:.1f}, DB={db:.4f}, "
              f"span_all={clusters_spanning_all}, mean_cats={np.mean(cats_per_cluster):.1f}")

    # --- R5.4 null model: shuffle category labels ---
    print("\nRunning null model (1000 category-label shuffles at k=15)...")
    km15 = KMeans(n_clusters=15, random_state=42, n_init=10, algorithm="lloyd")
    labels_15 = km15.fit_predict(X)

    n_trials = 1000
    null_spans = []
    rng = np.random.RandomState(42)
    for _ in range(n_trials):
        shuffled = rng.permutation(categories)
        unique_cats = sorted(set(shuffled))
        count_spanning = 0
        for ci in range(15):
            mask = labels_15 == ci
            if len(set(shuffled[mask])) == len(unique_cats):
                count_spanning += 1
        null_spans.append(count_spanning)

    # Actual count at k=15
    actual_spanning = 0
    for ci in range(15):
        mask = labels_15 == ci
        if len(set(categories[mask])) == len(set(categories)):
            actual_spanning += 1

    null_spans = np.array(null_spans)
    p_value = float(np.mean(null_spans >= actual_spanning))

    results["null_model_category_shuffle"] = {
        "description": "Shuffle category labels 1000 times, count clusters spanning all 7",
        "k": 15,
        "actual_clusters_spanning_all_7": actual_spanning,
        "null_mean": round(float(null_spans.mean()), 2),
        "null_std": round(float(null_spans.std()), 2),
        "null_median": int(np.median(null_spans)),
        "null_max": int(null_spans.max()),
        "null_min": int(null_spans.min()),
        "p_value": round(p_value, 4),
        "percentile_of_actual": round(float(np.mean(null_spans <= actual_spanning) * 100), 1),
        "interpretation": (
            f"Under random category assignment, {null_spans.mean():.1f} +/- {null_spans.std():.1f} "
            f"clusters span all 7 categories (actual: {actual_spanning}). "
            f"p = {p_value:.4f}."
        ),
    }

    print(f"\nNull model: actual={actual_spanning} spanning all 7, "
          f"null mean={null_spans.mean():.1f} +/- {null_spans.std():.1f}, "
          f"p={p_value:.4f}")

    # --- Find optimal k by silhouette ---
    best_k = max(results["k_sweep"], key=lambda x: x["silhouette"])
    results["best_k_by_silhouette"] = best_k["k"]
    results["best_silhouette"] = best_k["silhouette"]

    # Check monotonicity
    sils = [e["silhouette"] for e in results["k_sweep"]]
    is_monotonic = all(sils[i] <= sils[i+1] for i in range(len(sils)-1))
    results["silhouette_monotonically_increasing"] = is_monotonic

    # Find elbow in CH (largest drop)
    chs = [e["calinski_harabasz"] for e in results["k_sweep"]]
    ch_diffs = [chs[i] - chs[i+1] for i in range(len(chs)-1)]
    elbow_idx = np.argmax(ch_diffs) if ch_diffs else 0
    results["ch_elbow_k"] = k_range[elbow_idx]

    out = f"{RESULTS}/spi_k_sweep.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)

    # --- Summary ---
    print(f"\n{'='*60}")
    print("K-SWEEP SUMMARY")
    print(f"{'='*60}")
    print(f"Best k by silhouette: {best_k['k']} (sil={best_k['silhouette']:.4f})")
    print(f"Silhouette monotonically increasing: {is_monotonic}")
    print(f"CH elbow at k={results['ch_elbow_k']}")
    print(f"\nKey k values:")
    for k in [7, 10, 15, 20, 25, 30]:
        e = next((x for x in results["k_sweep"] if x["k"] == k), None)
        if e:
            print(f"  k={k:2d}: sil={e['silhouette']:.4f}, CH={e['calinski_harabasz']:.1f}, "
                  f"span_all={e['clusters_spanning_all_7']}")
    print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
