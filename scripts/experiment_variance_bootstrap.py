#!/usr/bin/env python3
"""E3: Trait-3rd Bootstrap — Prove Trait-Based ranking 3rd in per-model PCA
variance is not an artifact of unbalanced category sizes.

Uses the SAME metric as the original PCA analysis:
  total_cat_variance = sum of variances across PCA-10 for all rows in category
  per_model_variance = total_cat_variance / n_models_in_category

Then:
1. Bootstrap 10,000 resamples for category-level rank CIs
2. Permutation test: randomly reassign models to categories, check Trait-Based rank
"""

import os, json, csv, ast
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

SURVEY = "/Users/jsr/Documents/GitHub/survey"
RESULTS = f"{SURVEY}/results/reviewer_experiments"

# Exact category mapping from original PCA script (01_cross_model_pca_analysis.py)
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
    """Load all model embeddings with model labels per row."""
    emb_dir = f"{SURVEY}/Embeddings"
    all_emb = []
    all_model_keys = []

    for fname in sorted(os.listdir(emb_dir)):
        if not fname.endswith("_embeddings.csv") or "clustered" in fname:
            continue
        model_key = fname.replace("_embeddings.csv", "")
        if model_key not in MODEL_CATEGORIES:
            print(f"  Warning: {model_key} not in category map, skipping")
            continue
        with open(f"{emb_dir}/{fname}") as f:
            reader = csv.DictReader(f)
            for row in reader:
                emb = ast.literal_eval(row["Embedding"])
                all_emb.append(emb)
                all_model_keys.append(model_key)

    return np.array(all_emb), all_model_keys


def compute_category_per_model_variance(X_pca, model_keys, n_pca_dims=10):
    """Compute per-model variance = total_category_pca_variance / n_models.

    This matches the original PCA script metric exactly.
    """
    categories = sorted(set(MODEL_CATEGORIES.values()))

    # Models present in data
    models_present = sorted(set(model_keys))

    cat_total_var = {}
    cat_n_models = {}
    cat_per_model_var = {}

    for cat in categories:
        cat_models = [m for m in models_present if MODEL_CATEGORIES.get(m) == cat]
        cat_n_models[cat] = len(cat_models)

        # Get all rows belonging to this category
        cat_mask = np.array([MODEL_CATEGORIES.get(m) == cat for m in model_keys])
        if cat_mask.sum() == 0:
            cat_total_var[cat] = 0.0
            cat_per_model_var[cat] = 0.0
            continue

        cat_rows = X_pca[cat_mask, :n_pca_dims]
        total_var = float(np.var(cat_rows, axis=0).sum())
        cat_total_var[cat] = total_var
        cat_per_model_var[cat] = total_var / max(len(cat_models), 1)

    return cat_total_var, cat_n_models, cat_per_model_var


def bootstrap_ranks(X_pca, model_keys, n_bootstrap=10000, n_pca_dims=10):
    """Bootstrap per-model variance ranks by resampling rows within each model."""
    categories = sorted(set(MODEL_CATEGORIES.values()))
    models_present = sorted(set(model_keys))
    model_keys_arr = np.array(model_keys)

    # Pre-compute model row indices
    model_row_indices = {}
    for m in models_present:
        model_row_indices[m] = np.where(model_keys_arr == m)[0]

    # Observed
    _, cat_n_models, obs_per_model = compute_category_per_model_variance(X_pca, model_keys, n_pca_dims)
    sorted_cats = sorted(categories, key=lambda c: obs_per_model[c], reverse=True)
    observed_ranks = {c: sorted_cats.index(c) + 1 for c in categories}

    print(f"\nObserved per-model variance (descending):")
    for i, c in enumerate(sorted_cats):
        print(f"  {i+1}. {c}: {obs_per_model[c]:.1f} (n={cat_n_models[c]} models)")

    # Bootstrap: resample rows within each model, recompute category per-model variance
    rng = np.random.RandomState(42)
    rank_samples = {c: [] for c in categories}

    for b in range(n_bootstrap):
        # Resample rows within each model
        boot_X = np.empty_like(X_pca)
        for m in models_present:
            idx = model_row_indices[m]
            boot_idx = rng.choice(idx, size=len(idx), replace=True)
            boot_X[idx] = X_pca[boot_idx]

        # Compute per-model variance on bootstrapped data
        boot_per_model = {}
        for cat in categories:
            cat_mask = np.array([MODEL_CATEGORIES.get(m) == cat for m in model_keys])
            if cat_mask.sum() == 0:
                boot_per_model[cat] = 0.0
                continue
            cat_models = [m for m in models_present if MODEL_CATEGORIES.get(m) == cat]
            cat_rows = boot_X[cat_mask, :n_pca_dims]
            total_var = float(np.var(cat_rows, axis=0).sum())
            boot_per_model[cat] = total_var / max(len(cat_models), 1)

        sorted_boot = sorted(categories, key=lambda c: boot_per_model[c], reverse=True)
        for c in categories:
            rank_samples[c].append(sorted_boot.index(c) + 1)

    rank_cis = {}
    for c in categories:
        ranks = np.array(rank_samples[c])
        rank_cis[c] = {
            "observed_rank": observed_ranks[c],
            "observed_per_model_variance": round(obs_per_model[c], 1),
            "n_models": cat_n_models[c],
            "mean_rank": round(float(np.mean(ranks)), 2),
            "median_rank": float(np.median(ranks)),
            "ci_lower": float(np.percentile(ranks, 2.5)),
            "ci_upper": float(np.percentile(ranks, 97.5)),
            "rank_3_or_worse_pct": round(float(np.mean(ranks >= 3)) * 100, 1),
        }

    return rank_cis, obs_per_model


def permutation_test(X_pca, model_keys, n_permutations=10000, n_pca_dims=10):
    """Permutation test: randomly reassign models to categories (preserving sizes),
    check how often Trait-Based ranks 3rd or worse."""
    categories = sorted(set(MODEL_CATEGORIES.values()))
    models_present = sorted(set(model_keys))
    model_keys_arr = np.array(model_keys)

    # Observed per-model variance
    _, cat_n_models, obs_per_model = compute_category_per_model_variance(X_pca, model_keys, n_pca_dims)
    sorted_cats = sorted(categories, key=lambda c: obs_per_model[c], reverse=True)
    observed_tb_rank = sorted_cats.index("Trait-Based") + 1

    # Build model-level variance (total var of each model's rows in PCA space)
    model_total_var = {}
    for m in models_present:
        idx = np.where(model_keys_arr == m)[0]
        model_rows = X_pca[idx, :n_pca_dims]
        model_total_var[m] = float(np.var(model_rows, axis=0).sum())

    # Category assignment: list of (model, category) pairs
    model_cat_pairs = [(m, MODEL_CATEGORIES[m]) for m in models_present]
    cat_sizes = {c: sum(1 for _, cat in model_cat_pairs if cat == c) for c in categories}

    rng = np.random.RandomState(42)
    count_rank_ge = 0

    for _ in range(n_permutations):
        # Shuffle model-to-category assignment (preserving category sizes)
        perm_models = list(rng.permutation(models_present))
        perm_cat_map = {}
        idx = 0
        for c in categories:
            n = cat_sizes[c]
            for m in perm_models[idx:idx + n]:
                perm_cat_map[m] = c
            idx += n

        # Compute per-model variance under permuted assignment
        perm_per_model = {}
        for cat in categories:
            cat_models_perm = [m for m in models_present if perm_cat_map.get(m) == cat]
            if not cat_models_perm:
                perm_per_model[cat] = 0.0
                continue
            # Sum row-level variance for all models assigned to this category
            cat_mask = np.array([perm_cat_map.get(m) == cat for m in model_keys])
            cat_rows = X_pca[cat_mask, :n_pca_dims]
            total_var = float(np.var(cat_rows, axis=0).sum())
            perm_per_model[cat] = total_var / len(cat_models_perm)

        sorted_perm = sorted(categories, key=lambda c: perm_per_model[c], reverse=True)
        tb_rank = sorted_perm.index("Trait-Based") + 1
        if tb_rank >= observed_tb_rank:
            count_rank_ge += 1

    p_value = count_rank_ge / n_permutations

    return {
        "observed_trait_based_rank": observed_tb_rank,
        "observed_trait_based_per_model_variance": round(obs_per_model["Trait-Based"], 1),
        "permutation_p_value": round(float(p_value), 4),
        "n_permutations": n_permutations,
        "interpretation": f"Trait-Based ranking {observed_tb_rank}th: p={p_value:.4f} ({'significant' if p_value < 0.05 else 'not significant at 0.05'})"
    }


def main():
    print("=== E3: Trait-3rd Variance Bootstrap ===\n")

    all_emb, model_keys = load_all_embeddings()
    print(f"Loaded {len(all_emb)} embeddings from {len(set(model_keys))} models")

    # StandardScaler + PCA (matching original 01_cross_model_pca_analysis.py)
    print("Scaling embeddings (StandardScaler)...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(all_emb)
    print("Running PCA-50...")
    pca = PCA(n_components=50, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    print(f"PCA-50 variance explained: {pca.explained_variance_ratio_.sum():.3f}")

    print("\nBootstrapping category ranks (10,000 resamples)...")
    rank_cis, obs_per_model = bootstrap_ranks(X_pca, model_keys)

    print("\nRunning permutation test (10,000 permutations)...")
    perm_result = permutation_test(X_pca, model_keys)

    print(f"\n=== E3 RESULTS ===")
    tb_ci = rank_cis.get("Trait-Based", {})
    print(f"Trait-Based observed rank: {tb_ci.get('observed_rank')}")
    print(f"Trait-Based bootstrap: mean rank {tb_ci.get('mean_rank')} [CI: {tb_ci.get('ci_lower')}-{tb_ci.get('ci_upper')}]")
    print(f"Trait-Based ranks 3rd+ in {tb_ci.get('rank_3_or_worse_pct')}% of bootstrap samples")
    print(f"Permutation test: {perm_result['interpretation']}")

    print("\nAll categories:")
    for c in sorted(rank_cis.keys(), key=lambda c: rank_cis[c]["observed_rank"]):
        ci = rank_cis[c]
        print(f"  {ci['observed_rank']}. {c}: per-model var={ci['observed_per_model_variance']}, "
              f"mean_rank={ci['mean_rank']} [{ci['ci_lower']}-{ci['ci_upper']}], n={ci['n_models']}")

    results = {
        "method": "PCA-50, variance computed on first 10 components (matching original analysis)",
        "category_rank_bootstrap": rank_cis,
        "permutation_test": perm_result,
        "observed_per_model_variance": {c: round(v, 1) for c, v in obs_per_model.items()},
    }

    out_path = f"{RESULTS}/e3_variance_bootstrap.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
