#!/usr/bin/env python3
"""Cross-Model PCA Analysis — Unified dimensional analysis of all 44 personality models.

Loads all 44 model embedding files, runs PCA across the unified embedding space,
and identifies which personality dimensions drive the most variance. This directly
addresses ACM TIST Reviewer 2's demand for an ablation/PCA study showing the top-5
dimensions by marginal utility.

Usage:
    python notebooks/01_cross_model_pca_analysis.py
    python notebooks/01_cross_model_pca_analysis.py --output-dir results/

Outputs:
    - results/pca_variance_explained.csv        — Variance explained by top-N components
    - results/pca_top_factors_by_variance.csv    — Top personality factors ranked by contribution
    - results/pca_model_overlap_matrix.csv       — Cosine similarity between model centroids
    - results/pca_scree_plot.png                 — Scree plot of explained variance
    - results/pca_2d_all_models.png              — 2D PCA projection of all 6,800+ trait rows
    - results/pca_model_centroids_2d.png         — Model centroid positions in PCA space
    - results/pca_factor_loadings_heatmap.png    — Top-20 factor loadings on PC1-PC5
    - results/pca_summary_report.json            — Machine-readable summary
"""

import argparse
import ast
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


# ── Model registry ────────────────────────────────────────────────────────────

MODEL_DISPLAY = {
    "aam": "AAM (Approach-Avoidance)",
    "bdi": "BDI (Beck Depression)",
    "bt": "BT (Bartle Types)",
    "cest": "CEST (Cognitive-Experiential)",
    "cmoa": "CMOA (Circumplex of Affect)",
    "cs": "CS (Clifton Strengths)",
    "disc": "DISC",
    "dt4": "DT4 (Dark Tetrad)",
    "dtm": "DTM (Dark Triad)",
    "em": "EM (Enneagram)",
    "epm": "EPM (Eysenck PEN)",
    "ocean": "OCEAN (Big Five)",
    "ffni": "FFNI (Five-Factor Narcissism)",
    "ffni_sf": "FFNI-SF (Short Form)",
    "fsls": "FSLS (Felder-Silverman Learning)",
    "ftm": "FTM (Four Temperaments)",
    "gad7": "GAD-7 (Anxiety)",
    "hex": "HEXACO",
    "hsns": "HSNS (Hypersensitive Narcissism)",
    "ipn": "IPN (Interpersonal)",
    "mbti": "MBTI",
    "mcmi": "MCMI (Millon Clinical)",
    "mcmin": "MCMI-N (Narcissism)",
    "mmpi": "MMPI",
    "mst": "MST (Motivational Systems)",
    "narq": "NARQ (Narcissistic Admiration/Rivalry)",
    "npi": "NPI (Narcissistic Personality)",
    "papc": "PAPC",
    "pct": "PCT (Personal Construct)",
    "pni": "PNI (Pathological Narcissism)",
    "rft": "RFT (Regulatory Focus)",
    "riasec": "RIASEC (Holland Vocational)",
    "rit": "RIT (Rorschach Inkblot)",
    "scid": "SCID (DSM Structured Interview)",
    "scm": "SCM (Social-Cognitive)",
    "sdt": "SDT (Self-Determination)",
    "sixteenpf": "16PF (Cattell)",
    "stbv": "STBV (Schwartz Values)",
    "tat": "TAT (Thematic Apperception)",
    "tci": "TCI (Temperament & Character)",
    "tei": "TEI (Emotional Intelligence)",
    "tki": "TKI (Thomas-Kilmann Conflict)",
    "tmp": "TMP (Triarchic Psychopathy)",
    "wais": "WAIS (Intelligence)",
}

MODEL_CATEGORY = {
    "ocean": "Trait-Based", "hex": "Trait-Based",
    "epm": "Trait-Based", "sixteenpf": "Trait-Based", "mbti": "Trait-Based",
    "ftm": "Trait-Based",
    "aam": "Motivational", "mst": "Motivational", "rft": "Motivational",
    "sdt": "Motivational", "stbv": "Motivational", "cs": "Motivational",
    "pct": "Cognitive", "scm": "Cognitive", "cest": "Cognitive", "fsls": "Cognitive",
    "mmpi": "Clinical", "tci": "Clinical", "tmp": "Clinical", "bdi": "Clinical",
    "gad7": "Clinical", "scid": "Clinical", "mcmi": "Clinical",
    "rit": "Clinical", "tat": "Clinical", "wais": "Clinical",
    "npi": "Narcissism", "narq": "Narcissism", "ffni": "Narcissism",
    "hsns": "Narcissism", "pni": "Narcissism", "mcmin": "Narcissism",
    "ffni_sf": "Narcissism", "ipn": "Narcissism",
    "dtm": "Dark Personality", "dt4": "Dark Personality",
    "tki": "Interpersonal", "disc": "Interpersonal",
    "riasec": "Application", "bt": "Application", "tei": "Application",
    "em": "Holistic", "papc": "Holistic", "cmoa": "Holistic",
}

CATEGORY_COLORS = {
    "Trait-Based": "#1f77b4",
    "Motivational": "#2ca02c",
    "Cognitive": "#ff7f0e",
    "Clinical": "#d62728",
    "Narcissism": "#9467bd",
    "Dark Personality": "#8c564b",
    "Interpersonal": "#e377c2",
    "Application": "#7f7f7f",
    "Holistic": "#bcbd22",
}


# ── Data loading ──────────────────────────────────────────────────────────────

def load_all_embeddings(embedding_dir: Path) -> pd.DataFrame:
    """Load all model embedding CSVs into a single DataFrame."""
    rows = []
    embedding_dir = Path(embedding_dir)

    for csv_path in sorted(embedding_dir.glob("*_embeddings.csv")):
        name = csv_path.stem.replace("_embeddings", "")
        # Skip clustered/confusion/character files and duplicates
        if "clustered" in name or "confusion" in name or name == "character_model":
            continue
        # Skip non-personality-model files
        if name in ("cpm", "character_model"):
            continue

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            print(f"  WARN: Could not read {csv_path.name}: {e}")
            continue

        if "Embedding" not in df.columns:
            print(f"  WARN: No 'Embedding' column in {csv_path.name}")
            continue

        for _, row in df.iterrows():
            try:
                emb = ast.literal_eval(row["Embedding"]) if isinstance(row["Embedding"], str) else row["Embedding"]
                if len(emb) != 1536:
                    continue
                rows.append({
                    "model": name,
                    "model_display": MODEL_DISPLAY.get(name, name.upper()),
                    "category": MODEL_CATEGORY.get(name, "Other"),
                    "factor": row.get("Factor", "Unknown"),
                    "adjective": row.get("Adjective", ""),
                    "embedding": emb,
                })
            except (ValueError, SyntaxError):
                continue

    if not rows:
        print("ERROR: No embeddings loaded.")
        sys.exit(1)

    result = pd.DataFrame(rows)
    print(f"Loaded {len(result)} trait rows from {result['model'].nunique()} models")
    return result


# ── Analysis functions ────────────────────────────────────────────────────────

def run_pca(df: pd.DataFrame, n_components: int = 50):
    """Run PCA on the full embedding matrix."""
    X = np.array(df["embedding"].tolist())
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=min(n_components, X_scaled.shape[0], X_scaled.shape[1]))
    X_pca = pca.fit_transform(X_scaled)

    return pca, X_pca, X_scaled


def factor_loadings(pca, df: pd.DataFrame, n_top: int = 20):
    """Identify which personality factors load most heavily on each PC."""
    # Group by factor, compute mean embedding, then project
    factors = df.groupby(["model", "factor"]).first().reset_index()
    X_factors = np.array(factors["embedding"].tolist())
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_factors)
    X_proj = pca.transform(X_scaled)

    loadings = []
    for i, (_, row) in enumerate(factors.iterrows()):
        for pc in range(min(5, X_proj.shape[1])):
            loadings.append({
                "model": row["model"],
                "model_display": row["model_display"],
                "category": row["category"],
                "factor": row["factor"],
                f"PC{pc+1}": X_proj[i, pc],
            })

    # Pivot to get factor × PC matrix
    load_df = pd.DataFrame(loadings)
    pc_cols = [c for c in load_df.columns if c.startswith("PC")]
    pivot = load_df.groupby(["model_display", "factor"])[pc_cols].mean().reset_index()
    pivot["label"] = pivot["model_display"] + " — " + pivot["factor"]

    # Rank by absolute loading on PC1
    pivot["abs_PC1"] = pivot["PC1"].abs()
    pivot = pivot.sort_values("abs_PC1", ascending=False).head(n_top)

    return pivot


def model_centroid_similarity(df: pd.DataFrame):
    """Compute cosine similarity between model centroid embeddings."""
    centroids = {}
    for model, group in df.groupby("model"):
        embs = np.array(group["embedding"].tolist())
        centroids[model] = embs.mean(axis=0)

    models = sorted(centroids.keys())
    C = np.array([centroids[m] for m in models])
    sim = cosine_similarity(C)

    sim_df = pd.DataFrame(sim, index=[MODEL_DISPLAY.get(m, m) for m in models],
                          columns=[MODEL_DISPLAY.get(m, m) for m in models])
    return sim_df


def top_factors_by_variance(pca, X_pca, df: pd.DataFrame, n_pcs: int = 10):
    """Rank personality factors by their contribution to top PCs."""
    results = []
    for model_name, group in df.groupby("model"):
        for factor_name, fgroup in group.groupby("factor"):
            idx = fgroup.index.tolist()
            # Variance of this factor's projections on top PCs
            factor_proj = X_pca[idx, :n_pcs]
            total_var = np.var(factor_proj, axis=0).sum()
            results.append({
                "model": model_name,
                "model_display": MODEL_DISPLAY.get(model_name, model_name),
                "category": MODEL_CATEGORY.get(model_name, "Other"),
                "factor": factor_name,
                "n_rows": len(idx),
                "variance_contribution": round(total_var, 6),
            })

    result_df = pd.DataFrame(results).sort_values("variance_contribution", ascending=False)
    return result_df


# ── Visualization ─────────────────────────────────────────────────────────────

def plot_scree(pca, output_path: Path):
    """Scree plot showing cumulative variance explained."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    n = min(30, len(pca.explained_variance_ratio_))
    x = range(1, n + 1)
    var = pca.explained_variance_ratio_[:n]
    cum_var = np.cumsum(var)

    ax1.bar(x, var * 100, color="#1f77b4", alpha=0.7)
    ax1.set_xlabel("Principal Component")
    ax1.set_ylabel("Variance Explained (%)")
    ax1.set_title("Individual Variance per Component")

    ax2.plot(x, cum_var * 100, "o-", color="#d62728", linewidth=2)
    ax2.axhline(y=90, color="gray", linestyle="--", alpha=0.5, label="90% threshold")
    ax2.axhline(y=95, color="gray", linestyle=":", alpha=0.5, label="95% threshold")
    ax2.set_xlabel("Number of Components")
    ax2.set_ylabel("Cumulative Variance Explained (%)")
    ax2.set_title("Cumulative Variance Explained")
    ax2.legend()

    # Annotate cumulative at 50 components
    final_cum = cum_var[-1] * 100
    ax2.annotate(f"{n} PCs = {final_cum:.0f}%", xy=(n, final_cum), fontsize=9,
                 arrowprops=dict(arrowstyle="->"), xytext=(n - 8, final_cum + 10))

    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_path}")
    return None, None


def plot_2d_all_models(X_pca, df: pd.DataFrame, pca, output_path: Path):
    """2D scatter of all trait rows colored by model category."""
    fig, ax = plt.subplots(figsize=(14, 10))

    for cat, color in CATEGORY_COLORS.items():
        mask = df["category"] == cat
        if mask.sum() == 0:
            continue
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1],
                   c=color, alpha=0.4, s=15, label=cat)

    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)")
    ax.set_title(f"Unified PCA of 44 Personality Models ({len(df)} Trait Descriptors)")
    ax.legend(loc="upper right", fontsize=9, markerscale=3)

    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_path}")


def plot_model_centroids(X_pca, df: pd.DataFrame, pca, output_path: Path):
    """Plot model centroid positions in 2D PCA space."""
    fig, ax = plt.subplots(figsize=(16, 12))

    for model_name, group in df.groupby("model"):
        idx = group.index.tolist()
        cx = X_pca[idx, 0].mean()
        cy = X_pca[idx, 1].mean()
        cat = MODEL_CATEGORY.get(model_name, "Other")
        color = CATEGORY_COLORS.get(cat, "#333333")
        display = MODEL_DISPLAY.get(model_name, model_name).split("(")[0].strip()

        ax.scatter(cx, cy, c=color, s=group.shape[0] * 2, alpha=0.7, edgecolors="white", linewidth=0.5)
        ax.annotate(display, (cx, cy), fontsize=7, ha="center", va="bottom",
                    xytext=(0, 5), textcoords="offset points")

    # Legend for categories
    for cat, color in CATEGORY_COLORS.items():
        ax.scatter([], [], c=color, s=80, label=cat)
    ax.legend(loc="upper right", fontsize=8, title="Category")

    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)")
    ax.set_title("Model Centroids in Unified PCA Space (bubble size = row count)")

    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_path}")


def plot_factor_loadings_heatmap(pivot_df: pd.DataFrame, output_path: Path):
    """Heatmap of top-20 factor loadings on PC1-PC5."""
    pc_cols = [c for c in pivot_df.columns if c.startswith("PC")]
    data = pivot_df.set_index("label")[pc_cols].astype(float)

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(data.values, cmap="RdBu_r", aspect="auto", vmin=-3, vmax=3)

    ax.set_xticks(range(len(pc_cols)))
    ax.set_xticklabels(pc_cols)
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(data.index, fontsize=7)
    ax.set_title("Top-20 Factor Loadings on Principal Components")

    plt.colorbar(im, ax=ax, label="Loading Strength")
    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Cross-Model PCA Analysis")
    parser.add_argument("--embedding-dir", type=str, default=None,
                        help="Directory containing *_embeddings.csv files")
    parser.add_argument("--output-dir", type=str, default="results",
                        help="Output directory for results")
    args = parser.parse_args()

    # Find embedding directory
    if args.embedding_dir:
        emb_dir = Path(args.embedding_dir)
    else:
        # Try survey repo first, then Personality-Trait-Models
        candidates = [
            Path(__file__).parent.parent / "Embeddings",
            Path(__file__).parent.parent.parent / "survey" / "Embeddings",
            Path(__file__).parent.parent.parent / "Personality-Trait-Models" / "Embeddings",
        ]
        emb_dir = None
        for c in candidates:
            if c.exists() and list(c.glob("*_embeddings.csv")):
                emb_dir = c
                break
        if emb_dir is None:
            print("ERROR: Cannot find embeddings directory. Use --embedding-dir.")
            sys.exit(1)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Embedding directory: {emb_dir}")
    print(f"Output directory: {out_dir}")
    print()

    # ── Step 1: Load ──
    print("=" * 60)
    print("STEP 1: Loading all model embeddings")
    print("=" * 60)
    df = load_all_embeddings(emb_dir)
    df = df.reset_index(drop=True)

    print(f"\nModels loaded: {df['model'].nunique()}")
    print(f"Total trait rows: {len(df)}")
    print(f"Categories: {df['category'].nunique()}")
    print(f"Unique factors: {df['factor'].nunique()}")
    print()

    # ── Step 2: PCA ──
    print("=" * 60)
    print("STEP 2: Running PCA (50 components)")
    print("=" * 60)
    pca, X_pca, X_scaled = run_pca(df, n_components=50)

    cum_var = np.cumsum(pca.explained_variance_ratio_)
    n_90 = int(np.argmax(cum_var >= 0.90)) + 1 if cum_var[-1] >= 0.90 else None
    n_95 = int(np.argmax(cum_var >= 0.95)) + 1 if cum_var[-1] >= 0.95 else None

    print(f"\nPC1 explains: {pca.explained_variance_ratio_[0]*100:.1f}%")
    print(f"PC2 explains: {pca.explained_variance_ratio_[1]*100:.1f}%")
    print(f"PC1-5 explain: {cum_var[4]*100:.1f}%")
    print(f"PC1-10 explain: {cum_var[9]*100:.1f}%")
    print(f"PC1-50 explain: {cum_var[-1]*100:.1f}%")
    if n_90:
        print(f"Components for 90% variance: {n_90}")
    else:
        print(f"Components for 90% variance: >{len(pca.explained_variance_ratio_)} (only {cum_var[-1]*100:.1f}% with {len(pca.explained_variance_ratio_)} PCs)")
    print()

    # ── Step 3: Factor rankings ──
    print("=" * 60)
    print("STEP 3: Ranking factors by variance contribution")
    print("=" * 60)
    top_factors = top_factors_by_variance(pca, X_pca, df, n_pcs=10)
    print("\nTop 15 factors by variance contribution:")
    for _, row in top_factors.head(15).iterrows():
        print(f"  {row['model_display']:>35} — {row['factor']:<25} var={row['variance_contribution']:.4f}  (n={row['n_rows']})")
    top_factors.to_csv(out_dir / "pca_top_factors_by_variance.csv", index=False)
    print(f"\n  Saved: {out_dir / 'pca_top_factors_by_variance.csv'}")
    print()

    # ── Step 4: Factor loadings ──
    print("=" * 60)
    print("STEP 4: Computing factor loadings on PC1-PC5")
    print("=" * 60)
    loadings = factor_loadings(pca, df, n_top=20)
    print("\nTop-10 loadings on PC1:")
    pc1_sorted = loadings.sort_values("PC1", key=abs, ascending=False)
    for _, row in pc1_sorted.head(10).iterrows():
        print(f"  {row['label']:<50} PC1={row['PC1']:+.3f}")
    print()

    # ── Step 5: Model overlap ──
    print("=" * 60)
    print("STEP 5: Computing model centroid similarities")
    print("=" * 60)
    sim_df = model_centroid_similarity(df)
    sim_df.to_csv(out_dir / "pca_model_overlap_matrix.csv")
    print(f"  Saved: {out_dir / 'pca_model_overlap_matrix.csv'}")

    # Find most/least similar pairs
    sim_vals = []
    models_list = sim_df.index.tolist()
    for i in range(len(models_list)):
        for j in range(i + 1, len(models_list)):
            sim_vals.append((models_list[i], models_list[j], sim_df.iloc[i, j]))
    sim_vals.sort(key=lambda x: x[2], reverse=True)

    print("\nMost similar model pairs:")
    for a, b, s in sim_vals[:5]:
        print(f"  {a} ↔ {b}: {s:.4f}")
    print("\nLeast similar model pairs:")
    for a, b, s in sim_vals[-5:]:
        print(f"  {a} ↔ {b}: {s:.4f}")
    print()

    # ── Step 6: Variance explained CSV ──
    var_df = pd.DataFrame({
        "component": [f"PC{i+1}" for i in range(len(pca.explained_variance_ratio_))],
        "variance_explained": pca.explained_variance_ratio_,
        "cumulative_variance": cum_var,
    })
    var_df.to_csv(out_dir / "pca_variance_explained.csv", index=False)
    print(f"  Saved: {out_dir / 'pca_variance_explained.csv'}")

    # ── Step 7: Visualizations ──
    print()
    print("=" * 60)
    print("STEP 7: Generating visualizations")
    print("=" * 60)

    plot_scree(pca, out_dir / "pca_scree_plot.png")
    plot_2d_all_models(X_pca, df, pca, out_dir / "pca_2d_all_models.png")
    plot_model_centroids(X_pca, df, pca, out_dir / "pca_model_centroids_2d.png")
    plot_factor_loadings_heatmap(loadings, out_dir / "pca_factor_loadings_heatmap.png")

    # ── Step 8: Summary report ──
    print()
    print("=" * 60)
    print("STEP 8: Generating summary report")
    print("=" * 60)

    # Category-level variance analysis
    cat_variance = {}
    for cat, group in df.groupby("category"):
        idx = group.index.tolist()
        cat_var = np.var(X_pca[idx, :10], axis=0).sum()
        cat_variance[cat] = round(float(cat_var), 4)

    report = {
        "title": "Cross-Model PCA Analysis of 44 Personality Models",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "n_models": int(df["model"].nunique()),
        "n_trait_rows": len(df),
        "n_categories": int(df["category"].nunique()),
        "n_unique_factors": int(df["factor"].nunique()),
        "embedding_dim": 1536,
        "pca_components_computed": len(pca.explained_variance_ratio_),
        "variance_explained": {
            "PC1": round(float(pca.explained_variance_ratio_[0]), 4),
            "PC2": round(float(pca.explained_variance_ratio_[1]), 4),
            "PC1_5": round(float(cum_var[4]), 4),
            "PC1_10": round(float(cum_var[9]), 4),
            "n_for_90pct": n_90,
            "n_for_95pct": n_95,
        },
        "top_5_factors_by_variance": [
            {
                "model": row["model_display"],
                "factor": row["factor"],
                "category": row["category"],
                "variance": round(float(row["variance_contribution"]), 4),
                "n_rows": int(row["n_rows"]),
            }
            for _, row in top_factors.head(5).iterrows()
        ],
        "category_variance_contribution": dict(sorted(cat_variance.items(),
                                                       key=lambda x: x[1], reverse=True)),
        "most_similar_models": [
            {"model_a": a, "model_b": b, "cosine_similarity": round(float(s), 4)}
            for a, b, s in sim_vals[:5]
        ],
        "least_similar_models": [
            {"model_a": a, "model_b": b, "cosine_similarity": round(float(s), 4)}
            for a, b, s in sim_vals[-5:]
        ],
        "model_row_counts": {
            MODEL_DISPLAY.get(m, m): int(c)
            for m, c in df.groupby("model").size().sort_values(ascending=False).items()
        },
        "outputs": [
            "pca_variance_explained.csv",
            "pca_top_factors_by_variance.csv",
            "pca_model_overlap_matrix.csv",
            "pca_scree_plot.png",
            "pca_2d_all_models.png",
            "pca_model_centroids_2d.png",
            "pca_factor_loadings_heatmap.png",
            "pca_summary_report.json",
        ],
    }

    with open(out_dir / "pca_summary_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"  Saved: {out_dir / 'pca_summary_report.json'}")

    # ── Final summary ──
    print()
    print("=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"\n  Models analyzed: {report['n_models']}")
    print(f"  Trait rows: {report['n_trait_rows']}")
    print(f"  PC1 variance: {report['variance_explained']['PC1']*100:.1f}%")
    print(f"  PC1-5 variance: {report['variance_explained']['PC1_5']*100:.1f}%")
    print(f"  Components for 90%: {report['variance_explained']['n_for_90pct']}")
    print(f"\n  Top-5 personality dimensions by variance:")
    for i, f in enumerate(report["top_5_factors_by_variance"], 1):
        print(f"    {i}. {f['model']} — {f['factor']} ({f['category']}, var={f['variance']})")
    print(f"\n  All outputs in: {out_dir.resolve()}")


if __name__ == "__main__":
    main()
