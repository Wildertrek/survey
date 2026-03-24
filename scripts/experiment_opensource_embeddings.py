#!/usr/bin/env python3
"""E1: Open-Source Embedding Test — Prove the atlas isn't vendor-locked to OpenAI.

Embeds all 6,694 training rows with all-MiniLM-L6-v2 (384-dim, local, free),
trains new RF classifiers, evaluates on test items (also MiniLM-embedded),
compares to existing OpenAI 1536-dim results.
"""

import os, json, csv, ast, time
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from scipy.stats import spearmanr, wilcoxon
from sentence_transformers import SentenceTransformer

SURVEY = "/Users/jsr/Documents/GitHub/survey"
RESULTS = f"{SURVEY}/results/reviewer_experiments"


def load_dataset(model_key):
    """Load factor chain CSV, return texts and labels."""
    path = f"{SURVEY}/datasets/{model_key}.csv"
    texts, labels = [], []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Concatenate all fields into embedding text (same as original pipeline)
            text = f"{row['Factor']} {row['Adjective']} {row['Synonym']} {row['Verb']} {row['Noun']}"
            texts.append(text)
            labels.append(row["Factor"])
    return texts, labels


def load_openai_embeddings(model_key):
    """Load pre-computed OpenAI embeddings."""
    path = f"{SURVEY}/Embeddings/{model_key}_embeddings.csv"
    if not os.path.exists(path):
        return None, None
    embeddings, labels = [], []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            labels.append(row["Factor"])
            emb = ast.literal_eval(row["Embedding"])
            embeddings.append(emb)
    return np.array(embeddings), np.array(labels)


def load_test_items(model_key):
    """Load test items."""
    path = f"{SURVEY}/test_items/{model_key}_tests.json"
    if not os.path.exists(path):
        return None, None
    with open(path) as f:
        data = json.load(f)
    items = data.get("items", [])
    texts = [it["text"] for it in items]
    labels = [it["expected_factor"] for it in items]
    return texts, labels


def load_human_items(model_key):
    """Load human-authored items if available."""
    hi_dir = f"{SURVEY}/human_items"
    # Human items use instrument names, need to map to model keys
    # We'll collect all and filter by atlas_model
    items = []
    for fname in os.listdir(hi_dir):
        if not fname.endswith(".json"):
            continue
        with open(f"{hi_dir}/{fname}") as f:
            data = json.load(f)
        if data.get("atlas_model", "").lower() == model_key.lower():
            for item in data.get("items", []):
                items.append(item)
    if not items:
        return None, None
    texts = [it["text"] for it in items]
    labels = [it["factor"] for it in items]
    return texts, labels


def main():
    print("=== E1: Open-Source Embedding Test ===\n")

    # Load MiniLM model
    print("Loading all-MiniLM-L6-v2...")
    st_model = SentenceTransformer("all-MiniLM-L6-v2")
    print(f"Model loaded. Embedding dim: {st_model.get_sentence_embedding_dimension()}")

    dataset_dir = f"{SURVEY}/datasets"
    model_keys = sorted([f.replace(".csv", "") for f in os.listdir(dataset_dir) if f.endswith(".csv")])
    print(f"\nFound {len(model_keys)} models\n")

    results = []
    total_train = 0
    total_test = 0

    for model_key in model_keys:
        print(f"Processing {model_key}...", end=" ")

        # Load training data
        train_texts, train_labels = load_dataset(model_key)
        le = LabelEncoder()
        y_train = le.fit_transform(train_labels)
        n_classes = len(le.classes_)

        if n_classes < 2:
            print("skipped (< 2 classes)")
            continue

        # Embed training data with MiniLM
        train_emb_mini = st_model.encode(train_texts, show_progress_bar=False, batch_size=256)

        # Train RF on MiniLM embeddings
        rf_mini = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf_mini.fit(train_emb_mini, y_train)

        # Load test items
        test_texts, test_labels = load_test_items(model_key)
        row = {
            "model": model_key,
            "n_factors": n_classes,
            "n_train": len(train_texts),
        }

        if test_texts:
            # Embed test items with MiniLM
            test_emb_mini = st_model.encode(test_texts, show_progress_bar=False, batch_size=256)

            # Predict with MiniLM RF
            test_labels_valid = []
            test_emb_valid = []
            for i, lab in enumerate(test_labels):
                if lab in le.classes_:
                    test_labels_valid.append(lab)
                    test_emb_valid.append(test_emb_mini[i])

            if test_labels_valid:
                y_test = le.transform(test_labels_valid)
                test_emb_valid = np.array(test_emb_valid)
                mini_acc = accuracy_score(y_test, rf_mini.predict(test_emb_valid))
                row["minilm_accuracy"] = float(mini_acc)
                row["n_test"] = len(test_labels_valid)
                total_test += len(test_labels_valid)

                # Also evaluate OpenAI RF on same test items (need OpenAI test embeddings)
                # We can't re-embed with OpenAI, but we can use the stored RF model
                # to get the original accuracy from the validation results
            else:
                row["minilm_accuracy"] = None
                row["n_test"] = 0
        else:
            row["minilm_accuracy"] = None
            row["n_test"] = 0

        # Load human items
        human_texts, human_labels = load_human_items(model_key)
        if human_texts:
            human_emb_mini = st_model.encode(human_texts, show_progress_bar=False, batch_size=256)
            human_labels_valid = []
            human_emb_valid = []
            for i, lab in enumerate(human_labels):
                if lab in le.classes_:
                    human_labels_valid.append(lab)
                    human_emb_valid.append(human_emb_mini[i])
            if human_labels_valid:
                y_human = le.transform(human_labels_valid)
                human_emb_valid = np.array(human_emb_valid)
                human_acc = accuracy_score(y_human, rf_mini.predict(human_emb_valid))
                row["minilm_human_accuracy"] = float(human_acc)
                row["n_human"] = len(human_labels_valid)
            else:
                row["minilm_human_accuracy"] = None
                row["n_human"] = 0
        else:
            row["minilm_human_accuracy"] = None
            row["n_human"] = 0

        total_train += len(train_texts)
        results.append(row)

        mini_str = f"MiniLM={row.get('minilm_accuracy', 'N/A')}"
        if isinstance(row.get("minilm_accuracy"), float):
            mini_str = f"MiniLM={row['minilm_accuracy']:.3f}"
        human_str = ""
        if row.get("minilm_human_accuracy") is not None:
            human_str = f", human={row['minilm_human_accuracy']:.3f}"
        print(f"k={n_classes}, n={len(train_texts)}, {mini_str}{human_str}")

    # Load original OpenAI results for comparison
    # Try to load from existing validation results
    openai_results_path = f"{SURVEY}/results/validation_results.json"
    openai_accuracies = {}
    if os.path.exists(openai_results_path):
        with open(openai_results_path) as f:
            openai_data = json.load(f)
        for item in openai_data if isinstance(openai_data, list) else []:
            openai_accuracies[item.get("model", "")] = item.get("accuracy", None)

    # Summary statistics
    mini_accs = [r["minilm_accuracy"] for r in results if r.get("minilm_accuracy") is not None]
    mean_mini = np.mean(mini_accs) if mini_accs else 0

    mini_human = [r["minilm_human_accuracy"] for r in results if r.get("minilm_human_accuracy") is not None]
    mean_mini_human = np.mean(mini_human) if mini_human else 0

    # If we have OpenAI accuracies to compare
    paired_mini = []
    paired_openai = []
    for r in results:
        if r.get("minilm_accuracy") is not None and r["model"] in openai_accuracies:
            paired_mini.append(r["minilm_accuracy"])
            paired_openai.append(openai_accuracies[r["model"]])

    correlation = None
    wilcoxon_stat = None
    wilcoxon_p = None
    if len(paired_mini) >= 3:
        correlation = float(spearmanr(paired_mini, paired_openai).correlation)
        try:
            wilcoxon_stat, wilcoxon_p = wilcoxon(paired_mini, paired_openai)
            wilcoxon_stat = float(wilcoxon_stat)
            wilcoxon_p = float(wilcoxon_p)
        except:
            pass

    summary = {
        "n_models": len(results),
        "total_training_rows": total_train,
        "total_test_items": total_test,
        "minilm_mean_accuracy": float(mean_mini),
        "minilm_mean_human_accuracy": float(mean_mini_human) if mini_human else None,
        "n_models_with_human_items": len(mini_human),
        "openai_comparison": {
            "n_paired": len(paired_mini),
            "spearman_correlation": correlation,
            "wilcoxon_statistic": wilcoxon_stat,
            "wilcoxon_p_value": wilcoxon_p,
        },
        "per_model": results,
    }

    out_path = f"{RESULTS}/e1_opensource_embeddings.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n=== E1 SUMMARY ===")
    print(f"Models: {len(results)}, Training rows: {total_train}, Test items: {total_test}")
    print(f"MiniLM mean accuracy (test items): {mean_mini:.3f}")
    if mini_human:
        print(f"MiniLM mean accuracy (human items): {mean_mini_human:.3f} ({len(mini_human)} models)")
    if correlation is not None:
        print(f"Spearman rank correlation (MiniLM vs OpenAI): r_s = {correlation:.3f}")
    if wilcoxon_p is not None:
        print(f"Wilcoxon signed-rank: W={wilcoxon_stat:.1f}, p={wilcoxon_p:.4f}")
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
