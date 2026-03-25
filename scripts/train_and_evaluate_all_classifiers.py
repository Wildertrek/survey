"""
Train SVC, LR, kNN classifiers for all 44 models alongside existing RF.
Evaluate all 4 classifiers on test items and human items.
Save new classifiers to models/ directory.

Phase 1+2 of the classifier improvement plan.
"""

import os, json, csv, ast, sys
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from scipy.stats import friedmanchisquare
from collections import defaultdict

SURVEY = "/Users/jsr/Documents/GitHub/survey"
MODELS = f"{SURVEY}/models"
EMBEDDINGS = f"{SURVEY}/Embeddings"
DATASETS = f"{SURVEY}/datasets"
TEST_ITEMS = f"{SURVEY}/test_items"
HUMAN_ITEMS = f"{SURVEY}/human_items"
CACHE = f"{SURVEY}/.validation_cache"
RESULTS = f"{SURVEY}/results/reviewer_experiments"


def load_training_data(model_key):
    emb_file = f"{EMBEDDINGS}/{model_key}_embeddings.csv"
    if not os.path.exists(emb_file):
        return None, None
    labels, embeddings = [], []
    with open(emb_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            labels.append(row["Factor"])
            embeddings.append(ast.literal_eval(row["Embedding"]))
    return np.array(embeddings), np.array(labels)


def load_cached_embeddings(model_key, item_type):
    """Load pre-cached embeddings and labels."""
    cache_emb = f"{CACHE}/{model_key}_{item_type}_1536.npy"
    cache_lbl = f"{CACHE}/{model_key}_{item_type}_labels.json"
    if os.path.exists(cache_emb) and os.path.exists(cache_lbl):
        X = np.load(cache_emb)
        with open(cache_lbl) as f:
            labels = json.load(f)
        return X, labels
    return None, None


def load_human_items_for_model(model_key):
    """Load human items and their labels for a specific model."""
    texts, labels, reverses = [], [], []
    for fname in os.listdir(HUMAN_ITEMS):
        if not fname.endswith(".json"):
            continue
        with open(f"{HUMAN_ITEMS}/{fname}") as f:
            data = json.load(f)
        if data.get("atlas_model") == model_key:
            for item in data["items"]:
                texts.append(item["text"])
                labels.append(item["factor"])
                reverses.append(item.get("reverse", False))
    return texts, labels, reverses


def main():
    os.makedirs(RESULTS, exist_ok=True)

    model_keys = sorted(
        f.replace(".csv", "") for f in os.listdir(DATASETS) if f.endswith(".csv")
    )

    clf_factories = {
        "rf": lambda: RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        "lr": lambda: LogisticRegression(max_iter=1000, random_state=42),
        "svc": lambda: LinearSVC(max_iter=2000, random_state=42, dual="auto"),
        "knn": lambda: KNeighborsClassifier(n_neighbors=5),
    }
    clf_names = list(clf_factories.keys())

    results = {
        "description": "Multi-classifier training and evaluation",
        "models": {},
        "summary": {},
    }

    total_trained = 0
    total_skipped = 0

    for model_key in model_keys:
        X_train, y_train = load_training_data(model_key)
        if X_train is None:
            total_skipped += 1
            continue

        le = LabelEncoder()
        y_enc = le.fit_transform(y_train)
        if len(le.classes_) < 2:
            total_skipped += 1
            continue

        k = len(le.classes_)
        print(f"{model_key} (k={k}, n={len(y_train)}):", end=" ", flush=True)

        mr = {"k": k, "n_train": len(y_train)}

        # --- Train and save all classifiers ---
        trained_clfs = {}
        for cn in clf_names:
            clf = clf_factories[cn]()
            if cn == "knn" and len(X_train) < 6:
                clf = KNeighborsClassifier(n_neighbors=max(1, len(X_train) - 1))
            clf.fit(X_train, y_enc)
            trained_clfs[cn] = clf

            # Save new classifiers (skip RF — already exists)
            if cn != "rf":
                model_path = f"{MODELS}/{model_key}_{cn}_model.pkl"
                joblib.dump(clf, model_path)

        print("trained", end="", flush=True)

        # --- Evaluate on test items ---
        X_test, test_labels = load_cached_embeddings(model_key, "test")
        if X_test is not None and test_labels:
            valid_mask = [l in le.classes_ for l in test_labels]
            if any(valid_mask):
                X_t = X_test[valid_mask]
                y_t = le.transform([l for l, v in zip(test_labels, valid_mask) if v])
                mr["n_test"] = len(y_t)
                for cn in clf_names:
                    mr[f"{cn}_test"] = round(float(trained_clfs[cn].score(X_t, y_t)), 4)
                # Best on test
                best_test = max(clf_names, key=lambda c: mr.get(f"{c}_test", -1))
                mr["best_test"] = best_test
                mr["best_test_acc"] = mr[f"{best_test}_test"]
                print(f" | test: best={best_test} {mr['best_test_acc']:.3f}", end="", flush=True)

        # --- Evaluate on human items ---
        X_human, human_labels = load_cached_embeddings(model_key, "human")
        if X_human is not None and human_labels:
            valid_mask = [l in le.classes_ for l in human_labels]
            if any(valid_mask):
                X_h = X_human[valid_mask]
                y_h = le.transform([l for l, v in zip(human_labels, valid_mask) if v])
                mr["n_human"] = len(y_h)
                for cn in clf_names:
                    mr[f"{cn}_human"] = round(float(trained_clfs[cn].score(X_h, y_h)), 4)
                best_human = max(clf_names, key=lambda c: mr.get(f"{c}_human", -1))
                mr["best_human"] = best_human
                mr["best_human_acc"] = mr[f"{best_human}_human"]
                print(f" | human: best={best_human} {mr['best_human_acc']:.3f}", end="", flush=True)

                # --- Reverse-scored breakdown (if human items available) ---
                _, h_labels_raw, h_reverses = load_human_items_for_model(model_key)
                if h_labels_raw and len(h_labels_raw) == len(human_labels):
                    for cn in clf_names:
                        y_pred = trained_clfs[cn].predict(X_human[valid_mask])
                        y_pred_labels = le.inverse_transform(y_pred)
                        valid_labels = [l for l, v in zip(human_labels, valid_mask) if v]
                        valid_reverses = [r for r, v in zip(h_reverses, valid_mask) if v]

                        rev_correct = sum(1 for t, p, r in zip(valid_labels, y_pred_labels, valid_reverses) if r and t == p)
                        rev_total = sum(1 for r in valid_reverses if r)
                        fwd_correct = sum(1 for t, p, r in zip(valid_labels, y_pred_labels, valid_reverses) if not r and t == p)
                        fwd_total = sum(1 for r in valid_reverses if not r)

                        if rev_total > 0:
                            mr[f"{cn}_rev_err"] = round(1 - rev_correct / rev_total, 4)
                        if fwd_total > 0:
                            mr[f"{cn}_fwd_err"] = round(1 - fwd_correct / fwd_total, 4)

        results["models"][model_key] = mr
        total_trained += 1
        print()

    # --- Summary statistics ---
    for item_type in ["test", "human"]:
        accs = {c: [] for c in clf_names}
        for mr in results["models"].values():
            for c in clf_names:
                k = f"{c}_{item_type}"
                if k in mr:
                    accs[c].append(mr[k])
        if not accs["rf"]:
            continue

        summary = {}
        for c in clf_names:
            if accs[c]:
                summary[c] = {
                    "mean": round(float(np.mean(accs[c])), 4),
                    "median": round(float(np.median(accs[c])), 4),
                    "std": round(float(np.std(accs[c])), 4),
                    "n": len(accs[c]),
                }

        # Best-per-model oracle
        best_accs = []
        for mr in results["models"].values():
            scores = {c: mr.get(f"{c}_{item_type}", -1) for c in clf_names}
            best = max(scores.values())
            if best >= 0:
                best_accs.append(best)
        if best_accs:
            summary["best_per_model"] = {
                "mean": round(float(np.mean(best_accs)), 4),
                "median": round(float(np.median(best_accs)), 4),
                "n": len(best_accs),
            }

        # Wins count
        wins = {c: 0 for c in clf_names}
        for mr in results["models"].values():
            scores = {c: mr.get(f"{c}_{item_type}", -1) for c in clf_names}
            best = max(scores, key=scores.get)
            if scores[best] >= 0:
                wins[best] += 1
        summary["wins"] = wins

        # Friedman test
        arrays = [accs[c] for c in clf_names if len(accs[c]) == len(accs["rf"])]
        if len(arrays) == 4 and len(arrays[0]) >= 3:
            stat, p = friedmanchisquare(*arrays)
            summary["friedman"] = {"chi2": round(float(stat), 3), "p": round(float(p), 6)}

        results["summary"][item_type] = summary

    # --- Reliability tiers under best classifier ---
    tiers = {"reliable": [], "usable": [], "research_only": []}
    for mk, mr in results["models"].items():
        best_acc = mr.get("best_test_acc", mr.get("rf_test", 0))
        if best_acc >= 0.70:
            tiers["reliable"].append(mk)
        elif best_acc >= 0.50:
            tiers["usable"].append(mk)
        else:
            tiers["research_only"].append(mk)

    results["reliability_tiers"] = {
        "reliable": {"count": len(tiers["reliable"]), "models": sorted(tiers["reliable"])},
        "usable": {"count": len(tiers["usable"]), "models": sorted(tiers["usable"])},
        "research_only": {"count": len(tiers["research_only"]), "models": sorted(tiers["research_only"])},
    }

    # --- Reverse-scored summary ---
    for cn in clf_names:
        rev_errs = [mr[f"{cn}_rev_err"] for mr in results["models"].values() if f"{cn}_rev_err" in mr]
        fwd_errs = [mr[f"{cn}_fwd_err"] for mr in results["models"].values() if f"{cn}_fwd_err" in mr]
        if rev_errs:
            results["summary"].setdefault("reverse_scored", {})[cn] = {
                "mean_rev_err": round(float(np.mean(rev_errs)), 4),
                "mean_fwd_err": round(float(np.mean(fwd_errs)), 4),
                "n_models": len(rev_errs),
            }

    results["total_trained"] = total_trained
    results["total_skipped"] = total_skipped

    out = f"{RESULTS}/multi_classifier_evaluation.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)

    # --- Print summary ---
    print(f"\n{'='*70}")
    print("MULTI-CLASSIFIER EVALUATION SUMMARY")
    print(f"{'='*70}")
    print(f"Trained: {total_trained} models, Skipped: {total_skipped}")
    print(f"New classifiers saved: {total_trained * 3} files (LR, SVC, kNN per model)")

    for it in ["test", "human"]:
        if it not in results["summary"]:
            continue
        s = results["summary"][it]
        print(f"\n{it.upper()} ITEMS:")
        for c in clf_names:
            if c in s:
                print(f"  {c:4s}: {s[c]['mean']:.3f} +/- {s[c]['std']:.3f}  (n={s[c]['n']})")
        if "best_per_model" in s:
            print(f"  BEST: {s['best_per_model']['mean']:.3f}  (best classifier per model)")
        print(f"  Wins: {s.get('wins', {})}")
        if "friedman" in s:
            print(f"  Friedman: chi2={s['friedman']['chi2']}, p={s['friedman']['p']}")

    print(f"\nReliability tiers (best classifier per model):")
    for tier in ["reliable", "usable", "research_only"]:
        t = results["reliability_tiers"][tier]
        print(f"  {tier:15s}: {t['count']} models")

    if "reverse_scored" in results.get("summary", {}):
        print(f"\nReverse-scored error rates:")
        for cn in clf_names:
            if cn in results["summary"]["reverse_scored"]:
                rs = results["summary"]["reverse_scored"][cn]
                print(f"  {cn:4s}: rev={rs['mean_rev_err']:.1%}, fwd={rs['mean_fwd_err']:.1%}")

    print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
