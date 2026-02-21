#!/usr/bin/env python3
"""Personality Atlas — interactive demo.

Search all 6,694 traits across 44 personality models using semantic similarity.

Setup:

    git clone https://github.com/Wildertrek/survey.git
    cd survey
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

No API key needed — run with a pre-baked example:

    python demo.py                                          # list examples
    python demo.py "tends to worry about the future"        # pre-baked
    python demo.py "manipulates others for personal gain"   # pre-baked
    python demo.py "enjoys leading group discussions"        # pre-baked

To run your own queries, you need an OpenAI API key (costs < $0.001 per query):

    export OPENAI_API_KEY=sk-...
    python demo.py "your own personality description here"
    python demo.py "avoids conflict at all costs" --model ocean --top 10

You can also create a .env file in this directory with your key:
    echo 'OPENAI_API_KEY=sk-...' > .env

Get an API key at: https://platform.openai.com/api-keys
"""

import argparse
import ast
import json
import os
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

import joblib
import numpy as np
import pandas as pd

REPO_DIR = Path(__file__).parent
EXAMPLES_PATH = REPO_DIR / "examples.json"

# Slug -> (full name, category)
MODEL_INFO = {
    "ocean": ("Big Five (OCEAN)", "Trait-Based"),
    "hex": ("HEXACO", "Trait-Based"),
    "mbti": ("Myers-Briggs (MBTI)", "Trait-Based"),
    "ftm": ("Four Temperaments", "Trait-Based"),
    "epm": ("Eysenck (EPM)", "Trait-Based"),
    "sixteenpf": ("16PF", "Trait-Based"),
    "npi": ("Narcissistic Personality Inventory", "Narcissism"),
    "dtm": ("Dark Triad", "Narcissism"),
    "dt4": ("Dark Tetrad", "Narcissism"),
    "ffni": ("Five-Factor Narcissism (FFNI)", "Narcissism"),
    "ffni_sf": ("FFNI Short Form", "Narcissism"),
    "hsns": ("Hypersensitive Narcissism (HSNS)", "Narcissism"),
    "ipn": ("IPN Narcissism", "Narcissism"),
    "mcmin": ("MCMI Narcissism", "Narcissism"),
    "narq": ("NARQ", "Narcissism"),
    "pni": ("Pathological Narcissism (PNI)", "Narcissism"),
    "aam": ("Achievement Motivation (AAM)", "Motivational"),
    "sdt": ("Self-Determination (SDT)", "Motivational"),
    "rft": ("Regulatory Focus (RFT)", "Motivational"),
    "stbv": ("Schwartz Values (STBV)", "Motivational"),
    "mst": ("Mindset Theory (MST)", "Motivational"),
    "cs": ("CliftonStrengths", "Motivational"),
    "cest": ("CEST", "Cognitive"),
    "scm": ("Social Cognitive (SCM)", "Cognitive"),
    "fsls": ("Felder-Silverman (FSLS)", "Cognitive"),
    "pct": ("Personal Construct (PCT)", "Cognitive"),
    "mmpi": ("MMPI", "Clinical"),
    "scid": ("SCID (DSM-5)", "Clinical"),
    "bdi": ("Beck Depression (BDI)", "Clinical"),
    "gad7": ("GAD-7", "Clinical"),
    "tci": ("Temperament & Character (TCI)", "Clinical"),
    "mcmi": ("Millon Clinical (MCMI)", "Clinical"),
    "wais": ("Wechsler (WAIS)", "Clinical"),
    "tmp": ("TMP", "Clinical"),
    "rit": ("Rorschach (RIT)", "Clinical"),
    "tat": ("Thematic Apperception (TAT)", "Clinical"),
    "tki": ("Thomas-Kilmann (TKI)", "Interpersonal"),
    "disc": ("DISC", "Interpersonal"),
    "tei": ("Trait Emotional Intelligence", "Applied"),
    "em": ("Enneagram", "Applied"),
    "riasec": ("Holland RIASEC", "Applied"),
    "cmoa": ("Change Model of Attitudes", "Applied"),
    "bt": ("Bartle Types", "Applied"),
    "papc": ("PAPC", "Applied"),
}

ALL_SLUGS = sorted(MODEL_INFO.keys())


def load_examples():
    """Load pre-baked example embeddings from examples.json."""
    if not EXAMPLES_PATH.exists():
        return {}
    with open(EXAMPLES_PATH) as f:
        data = json.load(f)
    return {k: np.array(v) for k, v in data.items()}


def has_api_key():
    """Check if an OpenAI API key is available."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    return bool(os.environ.get("OPENAI_API_KEY"))


def embed_query(text: str, dim: int = 1536) -> np.ndarray:
    """Embed a single text query via OpenAI."""
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
    model = "text-embedding-3-small" if dim == 1536 else "text-embedding-3-large"
    resp = client.embeddings.create(input=[text], model=model)
    return np.array(resp.data[0].embedding)


def load_atlas_index():
    """Load all 44 models' embeddings into a single search index."""
    rows = []
    vectors = []

    for slug in ALL_SLUGS:
        emb_path = REPO_DIR / "Embeddings" / f"{slug}_embeddings.csv"
        if not emb_path.exists():
            continue

        df = pd.read_csv(emb_path)
        name, category = MODEL_INFO[slug]

        for _, row in df.iterrows():
            vec = np.array(ast.literal_eval(row["Embedding"]), dtype=np.float32)
            vectors.append(vec)
            rows.append({
                "slug": slug,
                "model": name,
                "category": category,
                "factor": row["Factor"],
                "adjective": row["Adjective"],
            })

    X = np.vstack(vectors)
    # L2-normalize for cosine similarity via dot product
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    X = X / norms
    return rows, X


def search(query_vec: np.ndarray, rows: list, X: np.ndarray, top_k: int = 20):
    """Find top-k nearest traits by cosine similarity."""
    q = query_vec / np.linalg.norm(query_vec)
    scores = X @ q
    top_idx = np.argsort(scores)[::-1][:top_k]
    results = []
    for i in top_idx:
        r = rows[i].copy()
        r["similarity"] = float(scores[i])
        results.append(r)
    return results


def classify(query_vec: np.ndarray, slug: str):
    """Classify the query through a specific model's RF classifier."""
    model_path = REPO_DIR / "models" / f"{slug}_rf_model.pkl"
    encoder_path = REPO_DIR / "models" / f"{slug}_label_encoder.pkl"

    if not model_path.exists():
        return None, None

    rf = joblib.load(model_path)
    encoder = joblib.load(encoder_path)

    pred = rf.predict(query_vec.reshape(1, -1))
    label = encoder.inverse_transform(pred)[0]

    probs = rf.predict_proba(query_vec.reshape(1, -1))[0]
    factor_probs = sorted(
        zip(encoder.classes_, probs), key=lambda x: x[1], reverse=True
    )

    return label, factor_probs


def display_results(query: str, results: list, top_k: int, model_slug=None,
                    query_vec=None):
    """Print search results and optional RF classification."""
    print(f'\nQuery: "{query}"\n')
    print(f"Top {top_k} nearest traits:")
    print(f"{'':>3}  {'Sim':>5}  {'Category':<14} {'Model':<30} {'Factor':<25} {'Trait'}")
    print("-" * 110)
    for i, r in enumerate(results, 1):
        print(f"{i:>3}. {r['similarity']:.3f}  {r['category']:<14} "
              f"{r['model']:<30} {r['factor']:<25} {r['adjective']}")

    # Category and model summary
    categories = {}
    models = {}
    for r in results:
        categories[r["category"]] = categories.get(r["category"], 0) + 1
        models[r["model"]] = models.get(r["model"], 0) + 1

    print(f"\nCategories in top {top_k}:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    print(f"\nModels in top {top_k}: {len(models)} unique")
    for m, count in sorted(models.items(), key=lambda x: -x[1])[:10]:
        print(f"  {m}: {count}")

    # Optional RF classification
    if model_slug and query_vec is not None:
        slug = model_slug.lower()
        if slug not in MODEL_INFO:
            print(f"\nUnknown model slug: {slug}")
            print(f"Available: {', '.join(ALL_SLUGS)}")
        else:
            label, factor_probs = classify(query_vec, slug)
            name, category = MODEL_INFO[slug]
            if label:
                print(f"\n{'='*60}")
                print(f"RF Classification — {name} ({category})")
                print(f"  Predicted factor: {label}")
                print(f"  All factor probabilities:")
                for factor, prob in factor_probs:
                    bar = "#" * int(prob * 40)
                    print(f"    {factor:<25} {prob:.1%}  {bar}")


def main():
    parser = argparse.ArgumentParser(
        description="Personality Atlas — cross-model trait search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Pre-baked examples (no API key needed):\n'
               '  python demo.py "tends to worry about the future"\n'
               '  python demo.py "manipulates others for personal gain"\n'
               '  python demo.py "enjoys leading group discussions"\n\n'
               'Custom queries (requires OPENAI_API_KEY):\n'
               '  export OPENAI_API_KEY=sk-...\n'
               '  python demo.py "avoids conflict at all costs"\n'
               '  python demo.py "driven by curiosity" --model ocean --top 10',
    )
    parser.add_argument("query", nargs="?", default=None,
                        help="Free-text personality description to search")
    parser.add_argument("--model", default=None,
                        help="Also classify through this model's RF (e.g. ocean, mmpi)")
    parser.add_argument("--top", type=int, default=20,
                        help="Number of nearest traits to return (default: 20)")
    args = parser.parse_args()

    examples = load_examples()

    # No query: list available examples
    if args.query is None:
        print("\nPersonality Atlas — cross-model trait search")
        print("=" * 50)
        print(f"\n{len(examples)} pre-baked examples (no API key needed):\n")
        for i, q in enumerate(examples, 1):
            print(f'  {i}. python demo.py "{q}"')
        print(f"\nTo search your own queries, set OPENAI_API_KEY:")
        print(f"  export OPENAI_API_KEY=sk-...")
        print(f'  python demo.py "your description here"')
        print(f"\nGet an API key at: https://platform.openai.com/api-keys")
        return

    # Check if query matches a pre-baked example
    query_vec = examples.get(args.query)

    if query_vec is not None:
        print(f"\n(Using pre-baked embedding — no API key needed)")
    elif has_api_key():
        print(f"\nEmbedding query...", end=" ", flush=True)
        query_vec = embed_query(args.query)
        print("done.")
    else:
        print(f'\nNo pre-baked embedding for: "{args.query}"')
        print(f"\nTo run custom queries, set your OpenAI API key:")
        print(f"  export OPENAI_API_KEY=sk-...")
        print(f"  python demo.py \"{args.query}\"")
        print(f"\nOr try one of the pre-baked examples:")
        for q in examples:
            print(f'  python demo.py "{q}"')
        print(f"\nGet an API key at: https://platform.openai.com/api-keys")
        return

    # Load atlas and search
    print("Loading atlas (6,694 traits across 44 models)...", end=" ", flush=True)
    rows, X = load_atlas_index()
    print(f"done ({len(rows)} vectors).")

    results = search(query_vec, rows, X, top_k=args.top)
    display_results(args.query, results, args.top, args.model, query_vec)


if __name__ == "__main__":
    main()
