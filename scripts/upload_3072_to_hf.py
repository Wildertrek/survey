#!/usr/bin/env python3
"""Upload 3072-dim embeddings and RF classifiers to Hugging Face Hub.

Usage:
    # First time: login to Hugging Face
    pip install huggingface_hub
    huggingface-cli login

    # Then run this script
    python scripts/upload_3072_to_hf.py
"""

import os
from pathlib import Path

REPO_ID = "Wildertrek/personality-atlas-3072"
REPO_ROOT = Path(__file__).resolve().parent.parent


def main():
    from huggingface_hub import HfApi, create_repo

    api = HfApi()

    # Create the dataset repo (no-op if already exists)
    create_repo(REPO_ID, repo_type="dataset", exist_ok=True)

    # Upload README/dataset card
    card_path = REPO_ROOT / "scripts" / "hf_dataset_card.md"
    if card_path.exists():
        api.upload_file(
            path_or_fileobj=str(card_path),
            path_in_repo="README.md",
            repo_id=REPO_ID,
            repo_type="dataset",
        )
        print("Uploaded dataset card")

    # Upload Embeddings_3072/
    emb_dir = REPO_ROOT / "Embeddings_3072"
    if emb_dir.exists():
        print(f"Uploading {len(list(emb_dir.glob('*.csv')))} embedding CSVs...")
        api.upload_folder(
            folder_path=str(emb_dir),
            path_in_repo="Embeddings_3072",
            repo_id=REPO_ID,
            repo_type="dataset",
        )
        print("Embeddings uploaded.")
    else:
        print(f"WARNING: {emb_dir} not found — skipping embeddings")

    # Upload models_3072/
    model_dir = REPO_ROOT / "models_3072"
    if model_dir.exists():
        print(f"Uploading {len(list(model_dir.glob('*.pkl')))} model files...")
        api.upload_folder(
            folder_path=str(model_dir),
            path_in_repo="models_3072",
            repo_id=REPO_ID,
            repo_type="dataset",
        )
        print("Models uploaded.")
    else:
        print(f"WARNING: {model_dir} not found — skipping models")

    print(f"\nDone. Assets available at: https://huggingface.co/datasets/{REPO_ID}")


if __name__ == "__main__":
    main()
