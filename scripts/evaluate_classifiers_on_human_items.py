"""
Evaluate all 4 classifiers (RF, SVC, LR, kNN) + any augmented variants
on human-authored items using cached embeddings.

Produces per-model per-classifier accuracy and summary statistics.
Saves results to results/reviewer_experiments/augmented_human_evaluation.json
"""

import os, json, sys
import numpy as np
import joblib
from collections import defaultdict

SURVEY = "/Users/jsr/Documents/GitHub/survey"
MODELS = f"{SURVEY}/models"
CACHE = f"{SURVEY}/.validation_cache"
RESULTS = f"{SURVEY}/results/reviewer_experiments"

# The 20 models that have human item caches
HUMAN_MODELS = [
    "aam", "bdi", "cest", "dt4", "dtm", "ftm", "gad7", "hex",
    "hsns", "mbti", "mst", "narq", "npi", "ocean", "rft", "riasec",
    "sdt", "stbv", "tci", "tki",
]

CLASSIFIER_TYPES = ["rf", "svc", "lr", "knn"]


def load_cached_human(model_key):
    """Load pre-cached human item embeddings and labels."""
    emb_path = f"{CACHE}/{model_key}_human_1536.npy"
    lbl_path = f"{CACHE}/{model_key}_human_labels.json"
    if not os.path.exists(emb_path) or not os.path.exists(lbl_path):
        return None, None
    X = np.load(emb_path)
    with open(lbl_path) as f:
        labels = json.load(f)
    return X, labels


def find_classifiers(model_key):
    """Find all classifier pkl files for a model (standard + augmented)."""
    found = {}
    for clf_type in CLASSIFIER_TYPES:
        # Standard classifier
        std_path = f"{MODELS}/{model_key}_{clf_type}_model.pkl"
        if os.path.exists(std_path):
            found[clf_type] = std_path
        # Augmented classifier
        aug_path = f"{MODELS}/{model_key}_{clf_type}_augmented_model.pkl"
        if os.path.exists(aug_path):
            found[f"{clf_type}_aug"] = aug_path
    return found


def evaluate_classifier(clf_path, le, X, true_labels):
    """Load a classifier and compute accuracy on human items."""
    clf = joblib.load(clf_path)
    y_true = le.transform(true_labels)
    y_pred = clf.predict(X)
    acc = np.mean(y_pred == y_true)
    return float(acc)


def main():
    os.makedirs(RESULTS, exist_ok=True)

    results = {
        "description": "All classifiers evaluated on human-authored items (cached embeddings)",
        "models": {},
    }

    # Track per-classifier accuracy across all models
    clf_accs = defaultdict(list)
    best_per_model_accs = []
    total_items = 0
    total_correct = defaultdict(int)
    total_n = defaultdict(int)
    n_augmented_found = 0

    print(f"{'Model':>8s}  {'k':>3s}  {'n':>3s}  ", end="")
    for ct in CLASSIFIER_TYPES:
        print(f"{'RF':>7s}" if ct == "rf" else f"{ct.upper():>7s}", end="  ")
    print(f"{'Best':>7s}  {'Winner':>6s}")
    print("-" * 80)

    for mkey in HUMAN_MODELS:
        X, labels = load_cached_human(mkey)
        if X is None:
            print(f"{mkey:>8s}  -- no cached embeddings, skipping")
            continue

        le_path = f"{MODELS}/{mkey}_label_encoder.pkl"
        if not os.path.exists(le_path):
            print(f"{mkey:>8s}  -- no label encoder, skipping")
            continue
        le = joblib.load(le_path)

        n = len(labels)
        k = len(le.classes_)
        total_items += n

        classifiers = find_classifiers(mkey)
        if not classifiers:
            print(f"{mkey:>8s}  -- no classifiers found, skipping")
            continue

        model_result = {"k": k, "n_human": n}
        model_accs = {}

        for clf_name, clf_path in sorted(classifiers.items()):
            try:
                acc = evaluate_classifier(clf_path, le, X, labels)
                model_result[f"{clf_name}_human"] = round(acc, 4)
                model_accs[clf_name] = acc
                clf_accs[clf_name].append(acc)

                # Track item-level totals for micro-average
                n_correct = int(round(acc * n))
                total_correct[clf_name] += n_correct
                total_n[clf_name] += n

                if "aug" in clf_name:
                    n_augmented_found += 1
            except Exception as e:
                model_result[f"{clf_name}_human"] = f"ERROR: {e}"

        if model_accs:
            best_clf = max(model_accs, key=model_accs.get)
            best_acc = model_accs[best_clf]
            model_result["best_human"] = best_clf
            model_result["best_human_acc"] = round(best_acc, 4)
            best_per_model_accs.append(best_acc)

        results["models"][mkey] = model_result

        # Print row
        print(f"{mkey:>8s}  {k:3d}  {n:3d}  ", end="")
        for ct in CLASSIFIER_TYPES:
            val = model_accs.get(ct)
            if val is not None:
                print(f"{val:7.3f}", end="  ")
            else:
                print(f"{'--':>7s}", end="  ")
        # Also print any augmented
        aug_strs = []
        for ct in CLASSIFIER_TYPES:
            aug_key = f"{ct}_aug"
            if aug_key in model_accs:
                aug_strs.append(f"{ct.upper()}_aug={model_accs[aug_key]:.3f}")
        best_acc_val = model_accs.get(max(model_accs, key=model_accs.get), 0)
        best_name = max(model_accs, key=model_accs.get)
        print(f"{best_acc_val:7.3f}  {best_name:>6s}", end="")
        if aug_strs:
            print(f"  [{', '.join(aug_strs)}]", end="")
        print()

    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    summary = {
        "n_models": len(HUMAN_MODELS),
        "n_models_evaluated": len(results["models"]),
        "total_human_items": total_items,
        "n_augmented_classifiers_found": n_augmented_found,
    }

    print(f"\nModels evaluated: {summary['n_models_evaluated']}")
    print(f"Total human items: {total_items}")
    print(f"Augmented classifiers found: {n_augmented_found}")

    # Per-classifier macro-average (mean of per-model accuracies)
    print(f"\n{'Classifier':>12s}  {'Macro Avg':>9s}  {'Micro Avg':>9s}  {'Median':>7s}  {'Std':>7s}  {'N':>3s}")
    print("-" * 60)
    clf_summary = {}
    for ct in CLASSIFIER_TYPES:
        accs = clf_accs.get(ct, [])
        if accs:
            macro = np.mean(accs)
            micro = total_correct[ct] / total_n[ct] if total_n[ct] > 0 else 0
            med = np.median(accs)
            std = np.std(accs)
            clf_summary[ct] = {
                "macro_mean": round(float(macro), 4),
                "micro_mean": round(float(micro), 4),
                "median": round(float(med), 4),
                "std": round(float(std), 4),
                "n_models": len(accs),
            }
            print(f"{ct.upper():>12s}  {macro:9.4f}  {micro:9.4f}  {med:7.4f}  {std:7.4f}  {len(accs):3d}")
        # Also check augmented
        aug_key = f"{ct}_aug"
        aug_accs = clf_accs.get(aug_key, [])
        if aug_accs:
            macro = np.mean(aug_accs)
            micro = total_correct[aug_key] / total_n[aug_key] if total_n[aug_key] > 0 else 0
            med = np.median(aug_accs)
            std = np.std(aug_accs)
            clf_summary[aug_key] = {
                "macro_mean": round(float(macro), 4),
                "micro_mean": round(float(micro), 4),
                "median": round(float(med), 4),
                "std": round(float(std), 4),
                "n_models": len(aug_accs),
            }
            print(f"{aug_key.upper():>12s}  {macro:9.4f}  {micro:9.4f}  {med:7.4f}  {std:7.4f}  {len(aug_accs):3d}")

    # Best-per-model
    if best_per_model_accs:
        bpm_macro = np.mean(best_per_model_accs)
        bpm_micro = sum(
            results["models"][m]["best_human_acc"] * results["models"][m]["n_human"]
            for m in results["models"]
            if "best_human_acc" in results["models"][m]
        ) / total_items if total_items > 0 else 0
        bpm_med = np.median(best_per_model_accs)
        bpm_std = np.std(best_per_model_accs)
        clf_summary["best_per_model"] = {
            "macro_mean": round(float(bpm_macro), 4),
            "micro_mean": round(float(bpm_micro), 4),
            "median": round(float(bpm_med), 4),
            "std": round(float(bpm_std), 4),
            "n_models": len(best_per_model_accs),
        }
        print(f"{'BEST/MODEL':>12s}  {bpm_macro:9.4f}  {bpm_micro:9.4f}  {bpm_med:7.4f}  {bpm_std:7.4f}  {len(best_per_model_accs):3d}")

        # Winner distribution
        winners = defaultdict(int)
        for m in results["models"].values():
            if "best_human" in m:
                winners[m["best_human"]] += 1
        clf_summary["wins"] = dict(winners)
        print(f"\nWinner distribution: {dict(winners)}")

    summary["classifiers"] = clf_summary
    results["summary"] = summary

    # Compare to reference 86.8%
    ref_bpm = 0.8679
    if best_per_model_accs:
        delta = bpm_macro - ref_bpm
        print(f"\n--- Comparison to reference (multi_classifier_evaluation.json) ---")
        print(f"Reference best-per-model macro mean: {ref_bpm:.4f} (86.8%)")
        print(f"This evaluation best-per-model macro mean: {bpm_macro:.4f} ({bpm_macro*100:.1f}%)")
        print(f"Delta: {delta:+.4f} ({delta*100:+.1f}%)")

    # Save
    out_path = f"{RESULTS}/augmented_human_evaluation.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
