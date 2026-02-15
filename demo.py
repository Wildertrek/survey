#!/usr/bin/env python3
"""Quick demo: load a personality model, predict factors from pre-computed embeddings.

Usage:
    python demo.py              # default: OCEAN
    python demo.py --model mbti # any of 44 model slugs
"""

import argparse
import ast

import joblib
import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Personality Atlas Demo")
    parser.add_argument("--model", default="ocean", help="Model slug (e.g. ocean, mbti, hexaco)")
    args = parser.parse_args()

    slug = args.model.lower()

    # Load dataset, embeddings, and trained classifier
    df = pd.read_csv(f"datasets/{slug}.csv")
    embeddings = pd.read_csv(f"Embeddings/{slug}_embeddings.csv")
    model = joblib.load(f"models/{slug}_rf_model.pkl")
    encoder = joblib.load(f"models/{slug}_label_encoder.pkl")

    # Parse embedding vectors and predict
    X = np.array([ast.literal_eval(e) for e in embeddings["Embedding"]])
    predictions = model.predict(X)
    labels = encoder.inverse_transform(predictions)
    accuracy = (labels == df["Factor"].values).mean()

    print(f"{slug.upper()}: {len(df)} traits, {len(set(labels))} factors, accuracy={accuracy:.1%}")
    print(f"Factors: {sorted(set(labels))}")


if __name__ == "__main__":
    main()
