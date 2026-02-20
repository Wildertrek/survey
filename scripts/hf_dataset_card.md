---
license: mit
task_categories:
  - text-classification
  - feature-extraction
language:
  - en
tags:
  - personality
  - psychology
  - embeddings
  - trait-classification
pretty_name: "Personality Atlas — 3072-dim Assets"
size_categories:
  - 1K<n<10K
---

# Personality Atlas — 3072-dim Embeddings and Classifiers

Upgraded embeddings and retrained Random Forest classifiers for the 44-model personality atlas described in:

> Raetano, J., Gregor, J., & Tamang, S. (2026). *A Survey and Computational Atlas of Personality Models.* ACM Transactions on Intelligent Systems and Technology (TIST). Under review.

## Contents

| Directory | Files | Description | Size |
|-----------|-------|-------------|------|
| `Embeddings_3072/` | 44 CSVs | OpenAI `text-embedding-3-large` (3072-dim) embeddings for all 6,694 trait rows | ~440 MB |
| `models_3072/` | 88 pkl files | Retrained scikit-learn RF classifiers + label encoders for all 44 models | ~107 MB |

## Usage

```python
from huggingface_hub import hf_hub_download
import pandas as pd
import joblib
import ast
import numpy as np

# Download a single model's assets
slug = "ocean"
emb_path = hf_hub_download("Wildertrek/personality-atlas-3072", f"Embeddings_3072/{slug}_embeddings.csv", repo_type="dataset")
model_path = hf_hub_download("Wildertrek/personality-atlas-3072", f"models_3072/{slug}_rf_model.pkl", repo_type="dataset")
enc_path = hf_hub_download("Wildertrek/personality-atlas-3072", f"models_3072/{slug}_label_encoder.pkl", repo_type="dataset")

emb_df = pd.read_csv(emb_path)
X = np.array([ast.literal_eval(e) for e in emb_df["Embedding"]])
model = joblib.load(model_path)
encoder = joblib.load(enc_path)

predictions = encoder.inverse_transform(model.predict(X))
print(f"{slug.upper()}: {len(X)} traits, accuracy = {(predictions == pd.read_csv(f'atlas/datasets/{slug}.csv')['Factor'].values).mean():.1%}")
```

## Relationship to Main Repository

The **1536-dim** assets (default) are in the main GitHub repository: [github.com/Wildertrek/survey](https://github.com/Wildertrek/survey)

The **3072-dim** assets here are the upgraded versions from Experiment 2 (RQ7: embedding dimensionality upgrade). They improve mean accuracy from 58.7% to 63.8% (+5.1pp) across all 44 models.

## Validation

```bash
# Clone the main repo and validate 3072-dim assets
git clone https://github.com/Wildertrek/survey.git
cd survey
python scripts/validate.py --all --dim 3072
```

## License

MIT — same as the main repository.
