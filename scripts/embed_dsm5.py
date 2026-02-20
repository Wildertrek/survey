"""
Pre-compute DSM-5 disorder embeddings for Colab reproducibility.

Generates 1536-dim embeddings for 222 DSM-5-TR disorders using
text-embedding-3-small, saves as CSV alongside the source JSON.

Usage: python scripts/embed_dsm5.py
"""

import json
import ast
import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from collections import Counter

# Paths
DSM5_SRC = Path("/Users/jsr/Downloads/GitHub/Personality-Trait-Models/Data/DSM5_Disorders_Dataset.json")
SURVEY_DIR = Path(__file__).parent.parent
DSM5_DEST = SURVEY_DIR / "data" / "dsm5_disorders.json"
EMB_DEST = SURVEY_DIR / "data" / "dsm5_embeddings.csv"


def load_dsm5(path):
    """Load DSM-5 disorders and extract embeddable text."""
    with open(path) as f:
        data = json.load(f)

    records = []
    for cat in data["DSM-5-TR"]["Categories"]:
        cat_name = cat["CategoryName"]
        for disorder in cat["Disorders"]:
            name = disorder["DisorderName"]
            criteria = disorder.get("CoreDiagnosticCriteria", "")
            keywords = disorder.get("Keywords", [])

            text = f"{name}: {criteria}"
            if keywords:
                text += " Keywords: " + ", ".join(keywords)

            records.append({
                "dsm5_category": cat_name,
                "disorder_name": name,
                "text": text,
                "n_keywords": len(keywords),
            })
    return records


def embed_texts(texts, model="text-embedding-3-small"):
    """Embed texts using OpenAI API."""
    from openai import OpenAI
    from dotenv import load_dotenv
    # Load .env from mindbench (where API keys live)
    load_dotenv(Path(__file__).parent.parent.parent / "mindbench" / ".env")
    load_dotenv()  # also try CWD

    client = OpenAI()
    embeddings = []
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        response = client.embeddings.create(model=model, input=batch)
        for item in response.data:
            embeddings.append(item.embedding)
        print(f"  Embedded {min(i+batch_size, len(texts))}/{len(texts)}")
    return embeddings


def run_alignment_test(records, dsm5_embeddings):
    """Test alignment against base atlas (6,694 vectors)."""
    import faiss

    # Load all atlas embeddings
    datasets_dir = SURVEY_DIR / "datasets"
    embeddings_dir = SURVEY_DIR / "Embeddings"

    CATEGORIES = {
        "Trait-Based": ["ocean", "hex", "mbti", "epm", "sixteenpf", "ftm"],
        "Narcissism-Based": ["npi", "pni", "hsns", "dtm", "dt4", "ffni", "ffni_sf", "narq", "mcmin", "ipn"],
        "Motivational/Value": ["stbv", "sdt", "rft", "aam", "mst", "cs"],
        "Cognitive/Learning": ["pct", "cest", "scm", "fsls"],
        "Clinical/Health": ["mmpi", "scid", "bdi", "gad7", "wais", "tci", "mcmi", "tmp", "rit", "tat"],
        "Interpersonal/Conflict": ["disc", "tki"],
        "Application-Specific": ["riasec", "cmoa", "tei", "bt", "em", "papc"]
    }
    slug_to_cat = {s: c for c, slugs in CATEGORIES.items() for s in slugs}

    slugs = sorted([f.replace(".csv", "") for f in os.listdir(datasets_dir) if f.endswith(".csv")])

    all_vecs, all_labels, all_cats, all_factors = [], [], [], []
    for slug in slugs:
        df = pd.read_csv(datasets_dir / f"{slug}.csv")
        emb = pd.read_csv(embeddings_dir / f"{slug}_embeddings.csv")
        X = np.array([ast.literal_eval(e) for e in emb["Embedding"]])
        all_vecs.append(X)
        all_labels.extend([slug.upper()] * len(df))
        all_cats.extend([slug_to_cat.get(slug, "Unknown")] * len(df))
        all_factors.extend(df["Factor"].values)

    X_all = np.vstack(all_vecs)
    X_norm = (X_all / np.linalg.norm(X_all, axis=1, keepdims=True)).astype(np.float32)
    index = faiss.IndexFlatIP(X_norm.shape[1])
    index.add(X_norm)
    print(f"  Atlas FAISS index: {index.ntotal} vectors from {len(slugs)} models")

    # Query DSM-5 embeddings against atlas
    dsm5_vecs = np.array(dsm5_embeddings, dtype=np.float32)
    dsm5_norms = np.linalg.norm(dsm5_vecs, axis=1, keepdims=True)
    dsm5_norms[dsm5_norms == 0] = 1
    dsm5_vecs = dsm5_vecs / dsm5_norms

    k = 20
    D, I = index.search(dsm5_vecs, k)

    # Analyze: what category does each disorder route to?
    clinical_count = 0
    for idx, record in enumerate(records):
        cats_found = Counter()
        for ni in I[idx]:
            if ni >= 0:
                cats_found[all_cats[ni]] += 1
        top_cat = cats_found.most_common(1)[0][0] if cats_found else "none"
        if top_cat == "Clinical/Health":
            clinical_count += 1

    rate = clinical_count / len(records)
    print(f"\n  DSM-5 → Clinical alignment: {clinical_count}/{len(records)} = {rate:.1%}")
    return rate


def main():
    print("=" * 60)
    print("DSM-5 Embedding Generation for Survey Repo")
    print("=" * 60)

    # 1. Copy DSM-5 JSON
    print(f"\n1. Copying DSM-5 dataset to {DSM5_DEST}...")
    DSM5_DEST.parent.mkdir(parents=True, exist_ok=True)
    records = load_dsm5(DSM5_SRC)
    print(f"   {len(records)} disorders across {len(set(r['dsm5_category'] for r in records))} categories")

    # Save a clean version with just what we need
    dsm5_clean = []
    for r in records:
        dsm5_clean.append({
            "dsm5_category": r["dsm5_category"],
            "disorder_name": r["disorder_name"],
            "text": r["text"],
        })
    with open(DSM5_DEST, "w") as f:
        json.dump(dsm5_clean, f, indent=2)
    print(f"   Saved {DSM5_DEST} ({DSM5_DEST.stat().st_size / 1024:.0f} KB)")

    # 2. Embed
    print(f"\n2. Embedding {len(records)} disorder criteria...")
    texts = [r["text"] for r in records]
    embeddings = embed_texts(texts)
    print(f"   Generated {len(embeddings)} x {len(embeddings[0])}-dim embeddings")

    # 3. Save embeddings CSV
    print(f"\n3. Saving embeddings to {EMB_DEST}...")
    emb_df = pd.DataFrame({
        "dsm5_category": [r["dsm5_category"] for r in records],
        "disorder_name": [r["disorder_name"] for r in records],
        "Embedding": [str(e) for e in embeddings],
    })
    emb_df.to_csv(EMB_DEST, index=False)
    print(f"   Saved {EMB_DEST} ({EMB_DEST.stat().st_size / 1024:.0f} KB)")

    # 4. Test alignment
    print(f"\n4. Testing alignment against base atlas...")
    rate = run_alignment_test(records, embeddings)

    print(f"\n{'=' * 60}")
    print(f"DONE. Files saved to {DSM5_DEST.parent}/")
    print(f"  dsm5_disorders.json  — 222 disorders (clean extract)")
    print(f"  dsm5_embeddings.csv  — 222 x 1536 pre-computed embeddings")
    print(f"  Clinical alignment rate: {rate:.1%}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
