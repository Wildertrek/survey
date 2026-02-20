"""
Pre-compute embeddings for Experiment 3 data (human items + Opus items).
Saves consolidated JSON + npz files to data/ for use in Colab notebooks.

Usage:
    python scripts/precompute_experiment3_embeddings.py

Requires: OPENAI_API_KEY in environment or .env file.
Cost: ~$0.01 total (6,000 texts at $0.02/1M tokens).
"""

import json
import glob
import os
import sys
import numpy as np
from pathlib import Path

# Add parent to path for local imports if needed
REPO_ROOT = Path(__file__).resolve().parent.parent

def embed_texts(texts: list[str], model: str = "text-embedding-3-small", batch_size: int = 100) -> np.ndarray:
    """Embed texts using OpenAI API in batches."""
    from openai import OpenAI
    client = OpenAI()

    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(input=batch, model=model)
        for item in response.data:
            all_embeddings.append(item.embedding)
        print(f"  Embedded {min(i + batch_size, len(texts))}/{len(texts)}")

    return np.array(all_embeddings, dtype=np.float32)


def consolidate_human_items():
    """Consolidate 21 human item JSON files into one list."""
    items_dir = REPO_ROOT / "human_items"
    all_items = []

    for f in sorted(items_dir.glob("*.json")):
        data = json.load(open(f))
        instrument = data["instrument"]
        slug = data["atlas_model"]
        citation = data.get("citation", "")

        for item in data["items"]:
            all_items.append({
                "slug": slug,
                "instrument": instrument,
                "text": item["text"],
                "expected_factor": item.get("expected_factor") or item.get("factor"),
                "source_type": "human",
            })

    return all_items


def consolidate_opus_items():
    """Consolidate 45 Opus test item JSON files into one list."""
    items_dir = REPO_ROOT / "test_items_opus"
    all_items = []

    for f in sorted(items_dir.glob("*_tests.json")):
        if f.name == "generation_summary.json":
            continue
        data = json.load(open(f))
        slug = data["model"]

        for item in data["items"]:
            all_items.append({
                "slug": slug,
                "text": item["text"],
                "expected_factor": item["expected_factor"],
                "confidence": item.get("confidence", ""),
                "source_type": "opus",
            })

    return all_items


def main():
    from dotenv import load_dotenv
    # Try loading .env from multiple locations
    for env_path in [REPO_ROOT / ".env", REPO_ROOT.parent / "mindbench" / ".env"]:
        if env_path.exists():
            load_dotenv(env_path)
            break

    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found. Set it in environment or .env file.")
        sys.exit(1)

    data_dir = REPO_ROOT / "data"
    data_dir.mkdir(exist_ok=True)

    # --- Human Items ---
    print("=== Human Items ===")
    human_items = consolidate_human_items()
    print(f"Consolidated {len(human_items)} human items from 21 instruments")

    human_json_path = data_dir / "human_items.json"
    json.dump(human_items, open(human_json_path, "w"), indent=2)
    print(f"Saved: {human_json_path}")

    human_texts = [item["text"] for item in human_items]
    print("Embedding human items...")
    human_embeddings = embed_texts(human_texts)
    human_npz_path = data_dir / "human_items_embeddings.npz"
    np.savez_compressed(human_npz_path, embeddings=human_embeddings)
    print(f"Saved: {human_npz_path} ({human_embeddings.shape})")

    # --- Opus Items ---
    print("\n=== Opus Items ===")
    opus_items = consolidate_opus_items()
    print(f"Consolidated {len(opus_items)} Opus items from {len(set(i['slug'] for i in opus_items))} models")

    opus_json_path = data_dir / "opus_items.json"
    json.dump(opus_items, open(opus_json_path, "w"), indent=2)
    print(f"Saved: {opus_json_path}")

    opus_texts = [item["text"] for item in opus_items]
    print("Embedding Opus items...")
    opus_embeddings = embed_texts(opus_texts)
    opus_npz_path = data_dir / "opus_items_embeddings.npz"
    np.savez_compressed(opus_npz_path, embeddings=opus_embeddings)
    print(f"Saved: {opus_npz_path} ({opus_embeddings.shape})")

    print("\n=== Summary ===")
    print(f"Human: {len(human_items)} items, {human_embeddings.shape[1]}-dim embeddings")
    print(f"Opus:  {len(opus_items)} items, {opus_embeddings.shape[1]}-dim embeddings")
    print("Done. Files saved to data/")


if __name__ == "__main__":
    main()
