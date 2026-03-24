"""
R3-m1 Response: Classifier comparison on novel test items and human items.

The existing E2 comparison (e2_classifier_comparison.json) evaluated
RF/LR/SVC/kNN via 5-fold CV on training embeddings, where all methods
score 97-99%. This script evaluates the same classifiers on:
1. 5,038 novel LLM-generated test items (Experiment 1)
2. 368 human-authored items from 21 published instruments (Experiment 3)

This is the comparison that matters: performance on unseen data.
"""

import os, json, csv, ast, sys
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from scipy.stats import friedmanchisquare
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SURVEY = "/Users/jsr/Documents/GitHub/survey"
RESULTS = f"{SURVEY}/results/reviewer_experiments"
DATASETS = f"{SURVEY}/datasets"
EMBEDDINGS = f"{SURVEY}/Embeddings"
TEST_ITEMS = f"{SURVEY}/test_items"
HUMAN_ITEMS = f"{SURVEY}/human_items"
CACHE = f"{SURVEY}/.validation_cache"

client = OpenAI()


def get_embedding_batch(texts, model="text-embedding-3-small"):
    all_embeddings = []
    for i in range(0, len(texts), 2048):
        batch = texts[i:i + 2048]
        response = client.embeddings.create(input=batch, model=model)
        all_embeddings.extend([item.embedding for item in response.data])
    return all_embeddings


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


def load_test_items(model_key):
    test_file = f"{TEST_ITEMS}/{model_key}_tests.json"
    if not os.path.exists(test_file):
        return [], []
    with open(test_file) as f:
        data = json.load(f)
    return ([item["text"] for item in data["items"]],
            [item["expected_factor"] for item in data["items"]])


def load_human_items_for_model(model_key):
    texts, labels = [], []
    for fname in os.listdir(HUMAN_ITEMS):
        if not fname.endswith(".json"):
            continue
        with open(f"{HUMAN_ITEMS}/{fname}") as f:
            data = json.load(f)
        if data.get("atlas_model") == model_key:
            for item in data["items"]:
                texts.append(item["text"])
                labels.append(item["factor"])
    return texts, labels


def embed_with_cache(texts, labels, model_key, item_type):
    cache_emb = f"{CACHE}/{model_key}_{item_type}_1536.npy"
    cache_lbl = f"{CACHE}/{model_key}_{item_type}_labels.json"

    if os.path.exists(cache_emb) and os.path.exists(cache_lbl):
        X = np.load(cache_emb)
        with open(cache_lbl) as f:
            cached = json.load(f)
        if cached == labels and X.shape[0] == len(labels):
            return X
    # Embed fresh
    embs = get_embedding_batch(texts)
    X = np.array(embs)
    np.save(cache_emb, X)
    with open(cache_lbl, "w") as f:
        json.dump(labels, f)
    return X


def main():
    os.makedirs(RESULTS, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)

    model_keys = sorted(
        f.replace(".csv", "") for f in os.listdir(DATASETS) if f.endswith(".csv")
    )

    clf_factories = {
        "RF": lambda: RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        "LR": lambda: LogisticRegression(max_iter=1000, random_state=42),
        "SVC": lambda: LinearSVC(max_iter=2000, random_state=42, dual="auto"),
        "kNN": lambda: KNeighborsClassifier(n_neighbors=5),
    }
    clf_names = list(clf_factories.keys())

    results = {"description": "Classifier comparison on novel items (R3-m1)", "models": {}}
    total_test, total_human = 0, 0

    for model_key in model_keys:
        X_train, y_train = load_training_data(model_key)
        if X_train is None:
            continue

        le = LabelEncoder()
        y_enc = le.fit_transform(y_train)
        if len(le.classes_) < 2:
            continue

        # --- Test items ---
        test_texts, test_labels = load_test_items(model_key)
        valid = [(t, l) for t, l in zip(test_texts, test_labels) if l in le.classes_]
        if not valid:
            continue

        t_texts = [t for t, _ in valid]
        t_labels = [l for _, l in valid]
        print(f"{model_key}: embedding {len(t_texts)} test items...", end="", flush=True)
        X_test = embed_with_cache(t_texts, t_labels, model_key, "test")
        y_test = le.transform(t_labels)
        total_test += len(t_labels)

        # --- Human items (if available) ---
        h_texts, h_labels = load_human_items_for_model(model_key)
        h_valid = [(t, l) for t, l in zip(h_texts, h_labels) if l in le.classes_]
        X_human, y_human = None, None
        if h_valid:
            hh_texts = [t for t, _ in h_valid]
            hh_labels = [l for _, l in h_valid]
            X_human = embed_with_cache(hh_texts, hh_labels, model_key, "human")
            y_human = le.transform(hh_labels)
            total_human += len(hh_labels)

        # --- Train & evaluate ---
        mr = {"k": len(le.classes_), "n_test": len(y_test)}
        if y_human is not None:
            mr["n_human"] = len(y_human)

        for cn in clf_names:
            clf = clf_factories[cn]()
            if cn == "kNN" and len(X_train) < 6:
                clf = KNeighborsClassifier(n_neighbors=max(1, len(X_train) - 1))
            clf.fit(X_train, y_enc)
            mr[f"{cn}_test"] = round(float(clf.score(X_test, y_test)), 4)
            if X_human is not None:
                mr[f"{cn}_human"] = round(float(clf.score(X_human, y_human)), 4)

        results["models"][model_key] = mr
        best_test = max(clf_names, key=lambda c: mr[f"{c}_test"])
        print(f" best={best_test} ({mr[f'{best_test}_test']:.3f})")

    # --- Summary ---
    for item_type in ["test", "human"]:
        accs = {c: [] for c in clf_names}
        for mr in results["models"].values():
            for c in clf_names:
                k = f"{c}_{item_type}"
                if k in mr:
                    accs[c].append(mr[k])
        if not accs["RF"]:
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

        wins = {c: 0 for c in clf_names}
        for mr in results["models"].values():
            scores = {c: mr.get(f"{c}_{item_type}", -1) for c in clf_names}
            best = max(scores, key=scores.get)
            if scores[best] >= 0:
                wins[best] += 1
        summary["wins"] = wins

        arrays = [accs[c] for c in clf_names if len(accs[c]) == len(accs["RF"])]
        if len(arrays) == 4 and len(arrays[0]) >= 3:
            stat, p = friedmanchisquare(*arrays)
            summary["friedman"] = {"chi2": round(float(stat), 3), "p": round(float(p), 6)}

        results.setdefault("summary", {})[item_type] = summary

    results["total_test_items"] = total_test
    results["total_human_items"] = total_human

    out = f"{RESULTS}/r3m1_classifier_novel_items.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*60}")
    print("CLASSIFIER COMPARISON ON NOVEL ITEMS")
    print(f"{'='*60}")
    for it in ["test", "human"]:
        if it not in results.get("summary", {}):
            continue
        s = results["summary"][it]
        print(f"\n{it.upper()} ITEMS:")
        for c in clf_names:
            if c in s:
                print(f"  {c:4s}: {s[c]['mean']:.3f} ± {s[c]['std']:.3f}  (n={s[c]['n']})")
        print(f"  Wins: {s.get('wins', {})}")
        if "friedman" in s:
            print(f"  Friedman: χ²={s['friedman']['chi2']}, p={s['friedman']['p']}")
    print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
