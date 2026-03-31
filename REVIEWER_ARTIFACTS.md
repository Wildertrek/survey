# Artifact Verification Map

**Manuscript:** TIST-2025-12-1243 — *A Survey and Computational Atlas of Personality Models*

For reviewers who want to verify specific claims, this table maps paper sections to repository files.

| Paper Claim | Verify In |
|------------|-----------|
| 44 datasets, 6,694 traits | `datasets/*.csv` (44 files) |
| 5-column lexical schema | Any `datasets/<model>.csv` |
| PCA scree plot (no elbow) | `results/pca_scree_plot.png`, `results/pca_variance_explained.csv` |
| PCA 2D projection | `results/pca_2d_all_models.png`, `results/pca_model_centroids_2d.png` |
| Model overlap matrix | `results/pca_model_overlap_matrix.csv` |
| RQ1: 58.6% mean accuracy | `results/validation/individual_model_results.csv` |
| RQ2: r = -0.67 complexity | `results/validation/factor_complexity.csv` |
| RQ3-4: Judge agreement | `results/validation/individual_model_results.csv` (Inter-Judge columns) |
| RQ5: Cross-model retrieval | Run FAISS section in [Quick Start Colab](https://colab.research.google.com/github/Wildertrek/survey/blob/main/notebooks/atlas_quick_start.ipynb) |
| RQ6: Category breakdown | `results/validation/category_results.csv` |
| RQ7: 3072-dim upgrade | `results/validation/experiment2_comparison.csv`, [HF Hub](https://huggingface.co/datasets/Wildertrek/personality-atlas-3072) |
| RQ8: Augmentation results | `results/validation/experiment2_comparison.csv` |
| RQ9: Hierarchical results | `results/validation/experiment2_comparison.csv` |
| RQ10: Multi-generator | `test_items/` (GPT-4o) vs `test_items_opus/` (Claude Opus) |
| RQ11: Human items | `human_items/` (22 JSON files, 418 items) |
| RQ12: Convergent validity | Run evaluation bank section in [Quick Start Colab](https://colab.research.google.com/github/Wildertrek/survey/blob/main/notebooks/atlas_quick_start.ipynb) |
| RQ13: Embedding space topology | `figures/spi_15_clusters_tsne.png`, run SPI section in [Embedding Projector Colab](https://colab.research.google.com/github/Wildertrek/survey/blob/main/notebooks/atlas_embedding_projector.ipynb) |
| RQ14: Semantic reorganization (SPI) | 15 cluster table + Interpersonal Circumplex confirmation in [Embedding Projector Colab](https://colab.research.google.com/github/Wildertrek/survey/blob/main/notebooks/atlas_embedding_projector.ipynb) |
| DSM-5 alignment | `data/dsm5_disorders.json`, `data/dsm5_embeddings.csv` |
| KG validation | `results/validation/` + `graphs/` (44 JSON graph files) |
| 44 model cards | `atlas/*/MODEL_CARD.md` |
| Computational benchmarks | `results/validation/latency.json` |

## Quick Verification Paths

**Zero setup (Colab):** Click the Quick Start badge in [README.md](README.md) to reproduce all 14 RQs interactively (RQ1-12 in Quick Start, RQ13-14 in Embedding Projector).

**30 seconds (demo.py):**
```bash
git clone https://github.com/Wildertrek/survey.git && cd survey
pip install -r requirements.txt
python demo.py "tends to worry about the future"
```

**5 minutes (full validation):**
```bash
python validate.py --all --no-embed    # No API key needed
python validate.py --all               # Re-embed + validate (~$0.05, requires OpenAI key)
python validate.py --all --dim 3072    # 3072-dim validation
```
