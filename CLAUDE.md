# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Data mining project that clusters Indonesian provinces by natural disaster risk using K-Means on BNPB records (2018–2024). The dataset (`data_bencana.xlsx`) must be downloaded from Kaggle before running.

**Dataset source:** [Indonesia Natural Disaster Dataset (BNPB Records)](https://www.kaggle.com/datasets/maudiana/indonesia-natural-disaster-dataset-bnpb-records)

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full clustering pipeline (generates all outputs)
python clustering_bencana.py

# Open interactive notebook
jupyter notebook clustering_bencana.ipynb
```

## Architecture

The project is a single linear pipeline with no modular separation — `clustering_bencana.py` runs top-to-bottom through 11 steps:

1. **Load** — reads `data_bencana.xlsx`
2. **Preprocessing** — drops rows with null `death`, fills other nulls with 0, extracts year/month
3. **Feature Engineering** — aggregates per province: total disasters, casualties, damage counts, plus per-disaster-type pivot counts → merged into `province_features` DataFrame
4. **Standardization** — `StandardScaler` on all non-province columns
5. **Elbow + Silhouette** — tests K=2–10, picks optimal K by max silhouette score → saves `elbow_method.png`
6. **K-Means** — fits with optimal K (currently resolves to K=3)
7. **Relabeling** — re-maps raw cluster IDs to semantic labels (0=Low, 1=Extreme, 2=High) via composite severity score (mean of normalized: total_disasters, total_death, total_injured, total_damaged_house)
8. **Analysis** — prints per-cluster metrics
9. **PCA Visualization** — 2D scatter with province labels → `clustering_visualization.png`
10. **Cluster Comparison** — 2×2 bar chart grid → `cluster_comparison.png`
11. **Heatmap** — top 15 provinces by disaster count, normalized → `province_heatmap.png`

CSV outputs: `clustering_province_features.csv` (feature matrix), `clustering_results.csv` (with cluster assignments + PCA coords).

The notebook (`clustering_bencana.ipynb`) mirrors the same logic interactively.

## Key Design Notes

- Cluster relabeling uses a **composite severity score** (MinMaxScaler → row mean across 4 metrics), not manual mapping — the label assignments can shift if data changes.
- `optimal_k` is determined automatically; if the dataset changes and silhouette peaks at a different K, color/label arrays hardcoded to length 3 (`colors`, `cluster_names`, `markers`) will break.
- `plt.show()` is never called — all figures save to PNG and the script is designed for non-interactive/headless execution.
