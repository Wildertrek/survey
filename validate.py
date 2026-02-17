#!/usr/bin/env python3
"""Standalone validation script — reproduce atlas classifier accuracy on held-out test items.

Loads a model's dataset, pre-trained RF classifier, and test items, then embeds
the test items via OpenAI and runs RF predictions to compute accuracy metrics.

Requirements:
    pip install -r requirements.txt python-dotenv
    export OPENAI_API_KEY=sk-...   (or add to .env file)

Usage:
    python validate.py --model ocean              # single model
    python validate.py --all                      # all 44 models
    python validate.py --all --dim 3072           # 3072-dim embeddings
    python validate.py --model ocean --no-embed   # skip embedding (use cached)
"""

import argparse
import ast
import json
import os
import sys
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

# All 44 model slugs
ALL_SLUGS = [
    "aam", "bdi", "bt", "cest", "cmoa", "cs", "disc", "dt4", "dtm", "em",
    "epm", "ffni", "ffni_sf", "fsls", "ftm", "gad7", "hex", "hsns", "ipn",
    "mbti", "mcmi", "mcmin", "mmpi", "mst", "narq", "npi", "ocean", "papc",
    "pct", "pni", "rft", "riasec", "rit", "scid", "scm", "sdt", "sixteenpf",
    "stbv", "tat", "tci", "tei", "tki", "tmp", "wais",
]

REPO_DIR = Path(__file__).parent


def load_test_items(slug: str) -> list[dict]:
    """Load test items from test_items/{slug}_tests.json."""
    path = REPO_DIR / "test_items" / f"{slug}_tests.json"
    if not path.exists():
        raise FileNotFoundError(f"No test items found: {path}")
    data = json.loads(path.read_text())
    return data["items"]


def embed_texts(texts: list[str], model: str = "text-embedding-3-small",
                dim: int = 1536) -> np.ndarray:
    """Embed a list of texts using OpenAI API."""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: pip install openai")
        sys.exit(1)

    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    client = OpenAI()
    model_name = "text-embedding-3-small" if dim == 1536 else "text-embedding-3-large"

    # Batch in groups of 100
    all_embeddings = []
    for i in range(0, len(texts), 100):
        batch = texts[i:i+100]
        resp = client.embeddings.create(input=batch, model=model_name)
        for item in resp.data:
            all_embeddings.append(item.embedding)
        if i + 100 < len(texts):
            time.sleep(0.1)

    return np.array(all_embeddings)


def validate_model(slug: str, dim: int = 1536, cache_dir: Path | None = None,
                   no_embed: bool = False) -> dict:
    """Validate a single model and return metrics."""
    # Load RF model and label encoder
    if dim == 3072:
        model_path = REPO_DIR / "models_3072" / f"{slug}_rf_model.pkl"
        encoder_path = REPO_DIR / "models_3072" / f"{slug}_label_encoder.pkl"
        if not model_path.exists():
            model_path = REPO_DIR / "models" / f"{slug}_rf_model.pkl"
            encoder_path = REPO_DIR / "models" / f"{slug}_label_encoder.pkl"
    else:
        model_path = REPO_DIR / "models" / f"{slug}_rf_model.pkl"
        encoder_path = REPO_DIR / "models" / f"{slug}_label_encoder.pkl"

    if not model_path.exists():
        return {"slug": slug, "error": f"No RF model: {model_path}"}
    if not encoder_path.exists():
        return {"slug": slug, "error": f"No label encoder: {encoder_path}"}

    rf_model = joblib.load(model_path)
    encoder = joblib.load(encoder_path)

    # Load test items
    try:
        items = load_test_items(slug)
    except FileNotFoundError as e:
        return {"slug": slug, "error": str(e)}

    if not items:
        return {"slug": slug, "error": "No test items"}

    texts = [item["text"] for item in items]
    expected = [item["expected_factor"] for item in items]

    # Filter items whose expected_factor is in the encoder's classes
    valid_classes = set(encoder.classes_)
    valid_mask = [e in valid_classes for e in expected]
    if sum(valid_mask) < len(items):
        n_dropped = len(items) - sum(valid_mask)
        texts = [t for t, v in zip(texts, valid_mask) if v]
        expected = [e for e, v in zip(expected, valid_mask) if v]

    if not texts:
        return {"slug": slug, "error": "No valid test items after filtering"}

    # Embed test items (or load from cache)
    cache_path = None
    if cache_dir:
        cache_path = cache_dir / f"{slug}_{dim}_embeddings.npy"

    if no_embed and cache_path and cache_path.exists():
        X_test = np.load(cache_path)
    else:
        X_test = embed_texts(texts, dim=dim)
        if cache_path:
            cache_dir.mkdir(parents=True, exist_ok=True)
            np.save(cache_path, X_test)

    # Predict
    y_true = encoder.transform(expected)
    y_pred = rf_model.predict(X_test)

    n_factors = len(valid_classes)
    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    precision = precision_score(y_true, y_pred, average="macro", zero_division=0)
    recall = recall_score(y_true, y_pred, average="macro", zero_division=0)

    # Baselines
    random_acc = 1.0 / n_factors if n_factors > 0 else 0
    from collections import Counter
    freq_counts = Counter(y_true)
    most_common = freq_counts.most_common(1)[0][1]
    freq_acc = most_common / len(y_true)

    return {
        "slug": slug,
        "n_factors": n_factors,
        "n_test_items": len(texts),
        "accuracy": round(accuracy, 4),
        "f1_macro": round(f1, 4),
        "precision_macro": round(precision, 4),
        "recall_macro": round(recall, 4),
        "random_baseline": round(random_acc, 4),
        "frequency_baseline": round(freq_acc, 4),
        "lift_over_random": round(accuracy - random_acc, 4),
        "embedding_dim": dim,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate atlas RF classifiers on held-out test items"
    )
    parser.add_argument("--model", type=str, help="Model slug (e.g., ocean, mbti)")
    parser.add_argument("--all", action="store_true", help="Validate all 44 models")
    parser.add_argument("--dim", type=int, default=1536, choices=[1536, 3072],
                        help="Embedding dimension (default: 1536)")
    parser.add_argument("--no-embed", action="store_true",
                        help="Skip embedding; use cached embeddings only")
    parser.add_argument("--cache-dir", type=str, default=".validation_cache",
                        help="Directory for cached embeddings")
    parser.add_argument("--output", type=str, default=None,
                        help="Output CSV path for results")
    args = parser.parse_args()

    if not args.model and not args.all:
        parser.error("Specify --model SLUG or --all")

    cache_dir = Path(args.cache_dir) if args.cache_dir else None
    slugs = ALL_SLUGS if args.all else [args.model]

    results = []
    errors = []

    print(f"Validating {len(slugs)} model(s) with {args.dim}-dim embeddings")
    print(f"{'='*70}")

    for i, slug in enumerate(slugs, 1):
        print(f"\n[{i}/{len(slugs)}] {slug}...", end=" ", flush=True)
        result = validate_model(slug, dim=args.dim, cache_dir=cache_dir,
                                no_embed=args.no_embed)
        if "error" in result:
            print(f"ERROR: {result['error']}")
            errors.append(result)
        else:
            print(f"accuracy={result['accuracy']:.1%}  "
                  f"F1={result['f1_macro']:.3f}  "
                  f"factors={result['n_factors']}  "
                  f"items={result['n_test_items']}")
            results.append(result)

    # Summary
    print(f"\n{'='*70}")
    print(f"RESULTS: {len(results)} models validated, {len(errors)} errors")

    if results:
        accs = [r["accuracy"] for r in results]
        print(f"\n  Mean accuracy: {np.mean(accs):.1%}")
        print(f"  Median accuracy: {np.median(accs):.1%}")
        print(f"  Min: {min(accs):.1%}  Max: {max(accs):.1%}")
        print(f"  Models > 70%: {sum(1 for a in accs if a >= 0.7)}/{len(accs)}")
        print(f"  Total test items: {sum(r['n_test_items'] for r in results)}")

    if errors:
        print(f"\n  Errors:")
        for e in errors:
            print(f"    {e['slug']}: {e['error']}")

    # Save results
    if results:
        out_path = Path(args.output) if args.output else Path(f"validation_results_{args.dim}.csv")
        df = pd.DataFrame(results)
        df.to_csv(out_path, index=False)
        print(f"\n  Results saved to: {out_path}")


if __name__ == "__main__":
    main()
