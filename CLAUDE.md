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
2. **Preprocessing** — drops rows with null `death`, fills other nulls with 0, **normalizes duplicate province names** (`P A P U A`→`PAPUA`, `DAERAH ISTIMEWA YOGYAKARTA`→`DI YOGYAKARTA`; 40→38 provinces), extracts year/month
3. **Feature Engineering** — aggregates per province: total disasters, casualties, damage counts, plus per-disaster-type pivot counts → merged into `province_features` DataFrame
4. **Log-transform + Scaling** — `np.log1p` on all non-province columns (dampens 2018 catastrophic outliers), then `RobustScaler` (median/IQR)
5. **Elbow + Silhouette** — tests K=2–10, computes & plots both → saves `elbow_method.png` (silhouette currently peaks at K=2)
6. **K-Means** — `optimal_k` is **manually set to 3** (overriding the silhouette argmax) so the 3-tier Low/High/Extreme narrative holds
7. **Relabeling** — re-maps raw cluster IDs to semantic labels (0=Low, 1=High, 2=Extreme) via composite severity score (mean of normalized: total_disasters, total_death, total_injured, total_damaged_house); a `cluster_labels` list (adaptive to `optimal_k`) feeds all chart titles/axes
8. **Analysis** — prints per-cluster metrics
9. **PCA Visualization** — 2D scatter with province labels → `clustering_visualization.png`
10. **Cluster Comparison** — 2×2 bar chart grid → `cluster_comparison.png`
11. **Heatmap** — top 15 provinces by disaster count, normalized → `province_heatmap.png`

CSV outputs: `clustering_province_features.csv` (feature matrix), `clustering_results.csv` (with cluster assignments + PCA coords).

The notebook (`clustering_bencana.ipynb`) mirrors the same logic interactively.

## Key Design Notes

- Cluster relabeling uses a **composite severity score** (MinMaxScaler → row mean across 4 metrics), not manual mapping — the label assignments can shift if data changes.
- `optimal_k` is **hardcoded to 3** (a deliberate override; silhouette's true optimum is K=2, driven by the 5 data-sparse Papua pemekaran provinces). If you revert to auto-K or change the data, the visualization code now adapts to `optimal_k` via the `cluster_labels` list and palette slicing, so it won't break — but `cluster_labels` only has nice names for K=2/3 (else falls back to `Tier {i}`).
- `log1p` is applied to all features before scaling because casualty/damage counts are extremely right-skewed; a single 2018 catastrophe (Palu/Lombok/Selat Sunda) would otherwise dominate the Euclidean distance and force singleton clusters.
- The notebook (`clustering_bencana.ipynb`) and `clustering_bencana.py` are kept in sync — apply changes to both.
- `plt.show()` is only called in the notebook; the `.py` saves figures to PNG for non-interactive/headless execution.
