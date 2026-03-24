"""
R3-m6 Response: Error analysis on Experiment 3 human item misclassifications.

The paper reports 69.6% accuracy on 368 human items but does not analyze
what types of errors occur. This script classifies all human items and
produces:
1. Per-model accuracy and confusion pairs
2. Most common cross-factor confusions
3. Systematic prediction bias (over/under-predicted factors)
4. Reverse-scored vs forward-scored error rates
"""

import os, json, csv, ast
import numpy as np
from collections import Counter, defaultdict
import joblib
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SURVEY = "/Users/jsr/Documents/GitHub/survey"
RESULTS = f"{SURVEY}/results/reviewer_experiments"
HUMAN_ITEMS = f"{SURVEY}/human_items"
MODELS = f"{SURVEY}/models"
CACHE = f"{SURVEY}/.validation_cache"

client = OpenAI()


def get_embedding_batch(texts, model="text-embedding-3-small"):
    all_embeddings = []
    for i in range(0, len(texts), 2048):
        batch = texts[i:i + 2048]
        response = client.embeddings.create(input=batch, model=model)
        all_embeddings.extend([item.embedding for item in response.data])
    return all_embeddings


def embed_with_cache(texts, labels, model_key):
    cache_emb = f"{CACHE}/{model_key}_human_1536.npy"
    cache_lbl = f"{CACHE}/{model_key}_human_labels.json"
    if os.path.exists(cache_emb) and os.path.exists(cache_lbl):
        X = np.load(cache_emb)
        with open(cache_lbl) as f:
            cached = json.load(f)
        if cached == labels and X.shape[0] == len(labels):
            return X
    embs = get_embedding_batch(texts)
    X = np.array(embs)
    np.save(cache_emb, X)
    with open(cache_lbl, "w") as f:
        json.dump(labels, f)
    return X


def main():
    os.makedirs(RESULTS, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)

    # Load all human items grouped by atlas_model
    model_items = defaultdict(list)
    for fname in sorted(os.listdir(HUMAN_ITEMS)):
        if not fname.endswith(".json"):
            continue
        with open(f"{HUMAN_ITEMS}/{fname}") as f:
            data = json.load(f)
        mk = data.get("atlas_model")
        inst = data.get("instrument", fname)
        for item in data["items"]:
            model_items[mk].append({
                "text": item["text"],
                "factor": item["factor"],
                "instrument": inst,
                "item_id": item.get("id", ""),
                "reverse": item.get("reverse", False),
            })

    results = {
        "description": "Exp 3 human item error analysis (R3-m6)",
        "per_model": {},
        "errors": [],
        "summary": {},
    }

    total_correct = 0
    total_items = 0
    all_confusions = []
    factor_true = Counter()
    factor_pred = Counter()

    for mk, items in sorted(model_items.items()):
        model_file = f"{MODELS}/{mk}_rf_model.pkl"
        le_file = f"{MODELS}/{mk}_label_encoder.pkl"
        if not os.path.exists(model_file) or not os.path.exists(le_file):
            print(f"  Skip {mk}: no model")
            continue

        clf = joblib.load(model_file)
        le = joblib.load(le_file)

        valid = [it for it in items if it["factor"] in le.classes_]
        if not valid:
            continue

        texts = [it["text"] for it in valid]
        true_labels = [it["factor"] for it in valid]

        print(f"{mk}: {len(valid)} items...", end="", flush=True)
        X = embed_with_cache(texts, true_labels, mk)

        y_pred_enc = clf.predict(X)
        y_pred = le.inverse_transform(y_pred_enc)

        correct = sum(1 for t, p in zip(true_labels, y_pred) if t == p)
        acc = correct / len(true_labels)

        errors = []
        for it, true, pred in zip(valid, true_labels, y_pred):
            factor_true[true] += 1
            factor_pred[pred] += 1
            if true != pred:
                err = {
                    "model": mk,
                    "instrument": it["instrument"],
                    "text": it["text"][:120],
                    "true": true,
                    "predicted": pred,
                    "reverse": it.get("reverse", False),
                }
                errors.append(err)
                all_confusions.append((mk, true, pred))

        results["per_model"][mk] = {
            "n": len(valid),
            "correct": correct,
            "accuracy": round(acc, 4),
            "errors": len(errors),
            "instruments": list(set(it["instrument"] for it in valid)),
        }
        results["errors"].extend(errors)
        total_correct += correct
        total_items += len(valid)
        print(f" {acc:.1%} ({len(errors)} errors)")

    # --- Summary ---
    results["summary"]["total"] = total_items
    results["summary"]["correct"] = total_correct
    results["summary"]["accuracy"] = round(total_correct / total_items, 4) if total_items else 0
    results["summary"]["n_errors"] = len(results["errors"])

    # Top confusion pairs (across all models)
    pair_counts = Counter((true, pred) for _, true, pred in all_confusions)
    results["summary"]["top_confusions"] = [
        {"true": t, "predicted": p, "count": c}
        for (t, p), c in pair_counts.most_common(20)
    ]

    # Within-model vs cross-concept analysis
    within_model_errors = len(all_confusions)  # all are within-model by definition
    results["summary"]["all_errors_are_within_model"] = True

    # Factor bias (over/under prediction)
    bias = {}
    for f in set(list(factor_true.keys()) + list(factor_pred.keys())):
        tn = factor_true.get(f, 0)
        pn = factor_pred.get(f, 0)
        if tn > 0:
            bias[f] = {"true_n": tn, "pred_n": pn, "ratio": round(pn / tn, 3)}
    results["summary"]["factor_bias"] = dict(
        sorted(bias.items(), key=lambda x: -x[1]["ratio"])
    )

    # Reverse-scored analysis
    rev_errors = sum(1 for e in results["errors"] if e.get("reverse"))
    rev_total = sum(1 for items in model_items.values() for it in items if it.get("reverse"))
    fwd_errors = len(results["errors"]) - rev_errors
    fwd_total = total_items - rev_total

    results["summary"]["reverse_analysis"] = {
        "reverse_items": rev_total,
        "reverse_errors": rev_errors,
        "reverse_error_rate": round(rev_errors / rev_total, 4) if rev_total else None,
        "forward_items": fwd_total,
        "forward_errors": fwd_errors,
        "forward_error_rate": round(fwd_errors / fwd_total, 4) if fwd_total else None,
    }

    out = f"{RESULTS}/r3m6_human_item_error_analysis.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*60}")
    print("EXPERIMENT 3 ERROR ANALYSIS")
    print(f"{'='*60}")
    print(f"Overall: {total_correct}/{total_items} ({total_correct/total_items:.1%})")
    print(f"Errors: {len(results['errors'])}")
    print(f"\nTop confusion pairs:")
    for p in results["summary"]["top_confusions"][:10]:
        print(f"  {p['true']:25s} -> {p['predicted']:25s}  ({p['count']}x)")
    ra = results["summary"]["reverse_analysis"]
    if ra["reverse_error_rate"] is not None:
        print(f"\nReverse-scored error rate: {ra['reverse_error_rate']:.1%} ({ra['reverse_errors']}/{ra['reverse_items']})")
        print(f"Forward-scored error rate: {ra['forward_error_rate']:.1%} ({ra['forward_errors']}/{ra['forward_items']})")
    print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
