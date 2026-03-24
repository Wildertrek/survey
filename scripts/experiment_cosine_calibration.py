#!/usr/bin/env python3
"""R3-m8: Cosine Similarity Calibration — Compute baseline cosine similarity
statistics so readers can interpret similarity claims in the paper.

Reports: random pair baseline, within-model mean, between-model mean,
within-category mean, between-category mean.
"""

import os, json, csv, ast
import numpy as np

SURVEY = "/Users/jsr/Documents/GitHub/survey"
RESULTS = f"{SURVEY}/results/reviewer_experiments"

MODEL_CATEGORIES = {
    "ocean": "Trait-Based", "hex": "Trait-Based",
    "epm": "Trait-Based", "sixteenpf": "Trait-Based", "mbti": "Trait-Based",
    "ftm": "Trait-Based",
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


def load_all_embeddings():
    emb_dir = f"{SURVEY}/Embeddings"
    all_emb, all_models = [], []
    for fname in sorted(os.listdir(emb_dir)):
        if not fname.endswith("_embeddings.csv") or "clustered" in fname:
            continue
        model_key = fname.replace("_embeddings.csv", "")
        with open(f"{emb_dir}/{fname}") as f:
            reader = csv.DictReader(f)
            for row in reader:
                emb = ast.literal_eval(row["Embedding"])
                all_emb.append(emb)
                all_models.append(model_key)
    return np.array(all_emb), all_models


def main():
    print("=== R3-m8: Cosine Similarity Calibration ===\n")

    all_emb, all_models = load_all_embeddings()
    n = len(all_emb)
    print(f"Loaded {n} embeddings from {len(set(all_models))} models")

    # Normalize for cosine similarity
    norms = np.linalg.norm(all_emb, axis=1, keepdims=True)
    all_emb_norm = all_emb / norms

    # 1. Random pair baseline (sample 10K pairs)
    rng = np.random.RandomState(42)
    n_sample = 10000
    idx_a = rng.randint(0, n, n_sample)
    idx_b = rng.randint(0, n, n_sample)
    random_cos = np.array([float(np.dot(all_emb_norm[i], all_emb_norm[j]))
                           for i, j in zip(idx_a, idx_b) if i != j])

    print(f"Random pair cosine (N={len(random_cos)}):")
    print(f"  Mean: {random_cos.mean():.4f}")
    print(f"  Std: {random_cos.std():.4f}")
    print(f"  Median: {np.median(random_cos):.4f}")

    # 2. Within-model similarity
    models_arr = np.array(all_models)
    unique_models = sorted(set(all_models))

    within_model_means = []
    for m in unique_models:
        idx = np.where(models_arr == m)[0]
        if len(idx) < 2:
            continue
        # Sample up to 500 pairs per model
        if len(idx) > 50:
            pairs = min(500, len(idx) * (len(idx) - 1) // 2)
            cos_vals = []
            for _ in range(pairs):
                i, j = rng.choice(idx, 2, replace=False)
                cos_vals.append(float(np.dot(all_emb_norm[i], all_emb_norm[j])))
        else:
            cos_vals = []
            for i_pos in range(len(idx)):
                for j_pos in range(i_pos + 1, len(idx)):
                    cos_vals.append(float(np.dot(all_emb_norm[idx[i_pos]], all_emb_norm[idx[j_pos]])))
        within_model_means.append(np.mean(cos_vals))

    within_model = np.array(within_model_means)

    print(f"\nWithin-model cosine (N={len(within_model)} models):")
    print(f"  Mean: {within_model.mean():.4f}")
    print(f"  Std: {within_model.std():.4f}")
    print(f"  Min: {within_model.min():.4f} (most diverse model)")
    print(f"  Max: {within_model.max():.4f} (most homogeneous model)")

    # 3. Between-model similarity (model centroid pairs)
    centroids = {}
    for m in unique_models:
        idx = np.where(models_arr == m)[0]
        centroids[m] = all_emb_norm[idx].mean(axis=0)
        centroids[m] = centroids[m] / np.linalg.norm(centroids[m])

    between_model = []
    within_cat = []
    between_cat = []
    for i, m1 in enumerate(unique_models):
        for m2 in unique_models[i+1:]:
            cos = float(np.dot(centroids[m1], centroids[m2]))
            between_model.append(cos)
            cat1 = MODEL_CATEGORIES.get(m1, "?")
            cat2 = MODEL_CATEGORIES.get(m2, "?")
            if cat1 == cat2 and cat1 != "?":
                within_cat.append(cos)
            else:
                between_cat.append(cos)

    between_arr = np.array(between_model)
    within_cat_arr = np.array(within_cat) if within_cat else np.array([0])
    between_cat_arr = np.array(between_cat) if between_cat else np.array([0])

    print(f"\nBetween-model centroid cosine (N={len(between_model)} pairs):")
    print(f"  Mean: {between_arr.mean():.4f}")
    print(f"  Std: {between_arr.std():.4f}")

    print(f"\nWithin-category centroid cosine (N={len(within_cat)} pairs):")
    print(f"  Mean: {within_cat_arr.mean():.4f}")

    print(f"\nBetween-category centroid cosine (N={len(between_cat)} pairs):")
    print(f"  Mean: {between_cat_arr.mean():.4f}")

    print(f"\n=== Calibration Summary ===")
    print(f"Random pair baseline:    {random_cos.mean():.3f} +/- {random_cos.std():.3f}")
    print(f"Within-model mean:       {within_model.mean():.3f} +/- {within_model.std():.3f}")
    print(f"Between-model centroids: {between_arr.mean():.3f} +/- {between_arr.std():.3f}")
    print(f"Within-category:         {within_cat_arr.mean():.3f}")
    print(f"Between-category:        {between_cat_arr.mean():.3f}")

    results = {
        "random_pair": {
            "n": len(random_cos),
            "mean": round(float(random_cos.mean()), 4),
            "std": round(float(random_cos.std()), 4),
            "median": round(float(np.median(random_cos)), 4),
        },
        "within_model": {
            "n_models": len(within_model),
            "mean": round(float(within_model.mean()), 4),
            "std": round(float(within_model.std()), 4),
            "min": round(float(within_model.min()), 4),
            "max": round(float(within_model.max()), 4),
        },
        "between_model_centroids": {
            "n_pairs": len(between_model),
            "mean": round(float(between_arr.mean()), 4),
            "std": round(float(between_arr.std()), 4),
        },
        "within_category_centroids": {
            "n_pairs": len(within_cat),
            "mean": round(float(within_cat_arr.mean()), 4),
        },
        "between_category_centroids": {
            "n_pairs": len(between_cat),
            "mean": round(float(between_cat_arr.mean()), 4),
        },
    }

    out_path = f"{RESULTS}/r3m8_cosine_calibration.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
