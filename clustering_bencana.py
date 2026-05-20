"""
Clustering Wilayah Rawan Bencana Indonesia
Dataset: BNPB Records (2018-2024)
Author: Guava 🍈
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import RobustScaler, MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

print("="*70)
print("🍈 CLUSTERING WILAYAH RAWAN BENCANA INDONESIA")
print("="*70)

# ========================================
# 1. LOAD DATA
# ========================================
print("\n📂 STEP 1: LOAD DATA")
df = pd.read_excel('data_bencana.xlsx')
print(f"✅ Data loaded: {len(df)} rows, {len(df.columns)} columns")
print(f"\nKolom: {df.columns.tolist()}")

# ========================================
# 2. PREPROCESSING
# ========================================
print("\n🔧 STEP 2: PREPROCESSING")

# Handle missing values
df.dropna(subset=['death'], inplace=True)
for col in ['missing_person', 'injured_person', 'flooded_house', 'damaged_house', 'damaged_facility']:
    df[col] = df[col].fillna(0)

# Normalisasi nama provinsi duplikat (varian ejaan/spasi) sebelum agregasi,
# agar kejadian satu provinsi tidak terpecah jadi dua baris.
# Provinsi baru hasil pemekaran 2022 (PAPUA BARAT DAYA/PEGUNUNGAN/SELATAN/TENGAH) tetap terpisah.
province_name_fix = {
    'P A P U A': 'PAPUA',
    'DAERAH ISTIMEWA YOGYAKARTA': 'DI YOGYAKARTA',
}
df['province'] = df['province'].replace(province_name_fix)

print(f"✅ Missing values handled")
print(f"✅ Data after cleaning: {len(df)} rows")
print(f"✅ Province names normalized: {df['province'].nunique()} unique provinces")

# Extract date features
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

print("✅ Date features extracted")

# ========================================
# 3. FEATURE ENGINEERING PER PROVINSI
# ========================================
print("\n🏗️ STEP 3: FEATURE ENGINEERING")

# Agregasi metrics per provinsi
province_agg = df.groupby('province').agg({
    'city_id': 'count',
    'death': 'sum',
    'injured_person': 'sum',
    'missing_person': 'sum',
    'damaged_house': 'sum',
    'flooded_house': 'sum',
    'damaged_facility': 'sum'
}).reset_index()

province_agg.columns = ['province', 'total_disasters', 'total_death', 'total_injured', 
                        'total_missing', 'total_damaged_house', 'total_flooded_house', 
                        'total_damaged_facility']

# Pivot jenis bencana
disaster_pivot = df.pivot_table(
    index='province', 
    columns='disaster_type', 
    values='city_id', 
    aggfunc='count', 
    fill_value=0
).reset_index()

# Merge
province_features = province_agg.merge(disaster_pivot, on='province')

print(f"✅ Feature matrix: {len(province_features)} provinces, {len(province_features.columns)-1} features")

# Save preprocessed data
province_features.to_csv('clustering_province_features.csv', index=False)
print("💾 Saved: clustering_province_features.csv")

# ========================================
# 4. STANDARDIZATION
# ========================================
print("\n📐 STEP 4: LOG-TRANSFORM & ROBUST SCALING")

features_to_cluster = province_features.drop('province', axis=1)

# log1p meredam ekor kanan ekstrem -> satu kejadian katastropik 2018
# (Palu, Lombok, Selat Sunda) tidak lagi mendominasi jarak antar provinsi.
# Semua fitur adalah count non-negatif, jadi log1p aman (log1p(0)=0).
features_log = np.log1p(features_to_cluster)

# RobustScaler memakai median & IQR -> tahan terhadap sisa outlier
scaler = RobustScaler()
features_scaled = scaler.fit_transform(features_log)

print(f"✅ Features log-transformed & robust-scaled: {features_scaled.shape}")

# ========================================
# 5. ELBOW METHOD & SILHOUETTE SCORE
# ========================================
print("\n📊 STEP 5: ELBOW METHOD")

inertias = []
silhouette_scores = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(features_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(features_scaled, kmeans.labels_))

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
ax1.set_xlabel('Number of Clusters (K)', fontsize=12)
ax1.set_ylabel('Inertia', fontsize=12)
ax1.set_title('Elbow Method', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)

ax2.plot(K_range, silhouette_scores, 'ro-', linewidth=2, markersize=8)
ax2.set_xlabel('Number of Clusters (K)', fontsize=12)
ax2.set_ylabel('Silhouette Score', fontsize=12)
ax2.set_title('Silhouette Score', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('elbow_method.png', dpi=150, bbox_inches='tight')
print("✅ Plot saved: elbow_method.png")

# Silhouette terbaik (informatif)
silhouette_best_k = K_range[np.argmax(silhouette_scores)]
print(f"\n📐 Silhouette tertinggi di K={silhouette_best_k} (Score: {max(silhouette_scores):.4f})")

# Override manual: pakai K=3 demi tingkatan risiko Low/High/Extreme.
# Silhouette memuncak di K=2 karena 5 provinsi pemekaran Papua 2022 (data ~1,5 thn)
# mendominasi sebagai outlier data-miskin sehingga memecah jadi 2 grup saja.
optimal_k = 3
print(f"🎯 K yang dipakai (manual): {optimal_k}")

# ========================================
# 6. K-MEANS CLUSTERING
# ========================================
print(f"\n🎯 STEP 6: K-MEANS CLUSTERING (K={optimal_k})")

kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
province_features['cluster'] = kmeans.fit_predict(features_scaled)

print(f"✅ Clustering completed")

# ========================================
# 7. RELABEL CLUSTER (0=Low, 1=High, 2=Extreme)
# ========================================
print("\n🔄 STEP 7: RELABELING CLUSTER")

# Calculate severity score
cluster_severity = province_features.groupby('cluster').agg({
    'total_disasters': 'mean',
    'total_death': 'mean',
    'total_injured': 'mean',
    'total_damaged_house': 'mean'
})

# Normalize and compute composite score
norm_scaler = MinMaxScaler()
normalized = norm_scaler.fit_transform(cluster_severity)
cluster_severity['composite_score'] = normalized.mean(axis=1)

# Map old cluster to new (based on severity rank)
severity_rank = cluster_severity['composite_score'].rank().astype(int) - 1
old_to_new = severity_rank.to_dict()

print("Mapping:")
for old, new in old_to_new.items():
    print(f"  Cluster {old} (old) → Cluster {new} (new)")

# Apply relabeling
province_features['cluster'] = province_features['cluster'].map(old_to_new)

# Nama tier risiko (terendah -> tertinggi), beradaptasi terhadap optimal_k
if optimal_k == 2:
    cluster_labels = ['Low', 'High']
elif optimal_k == 3:
    cluster_labels = ['Low', 'High', 'Extreme']
else:
    cluster_labels = [f'Tier {i}' for i in range(optimal_k)]

print(f"\n✅ Clusters relabeled: {', '.join(f'{i}={n}' for i, n in enumerate(cluster_labels))}")

# ========================================
# 8. CLUSTER ANALYSIS
# ========================================
print("\n📊 STEP 8: CLUSTER ANALYSIS")

for cluster_id in range(optimal_k):
    cluster_data = province_features[province_features['cluster'] == cluster_id]
    print(f"\n{'='*70}")
    print(f"CLUSTER {cluster_id} - {len(cluster_data)} provinsi")
    print(f"{'='*70}")
    
    print(f"Provinsi: {', '.join(cluster_data['province'].tolist())}")
    
    print(f"\nMetrics:")
    print(f"  Total Bencana: {cluster_data['total_disasters'].mean():.2f}")
    print(f"  Korban Meninggal: {cluster_data['total_death'].mean():.2f}")
    print(f"  Korban Luka: {cluster_data['total_injured'].mean():.2f}")
    print(f"  Rumah Rusak: {cluster_data['total_damaged_house'].mean():.2f}")

# Save results
province_features.to_csv('clustering_results.csv', index=False)
print("\n💾 Saved: clustering_results.csv")

# ========================================
# 9. PCA VISUALIZATION
# ========================================
print("\n📊 STEP 9: PCA VISUALIZATION")

pca = PCA(n_components=2)
features_pca = pca.fit_transform(features_scaled)

province_features['PCA1'] = features_pca[:, 0]
province_features['PCA2'] = features_pca[:, 1]

# Plot
plt.figure(figsize=(16, 10))

_all_colors  = ['#44AA44', '#FFA500', '#FF4444', '#8844AA', '#4488FF']
_all_markers = ['o', '^', 's', 'D', 'P']
colors        = _all_colors[:optimal_k]
cluster_names = [f'Cluster {i}: {n.upper()} RISK' for i, n in enumerate(cluster_labels)]
markers       = _all_markers[:optimal_k]

for i in range(optimal_k):
    cluster_data = province_features[province_features['cluster'] == i]
    plt.scatter(cluster_data['PCA1'], cluster_data['PCA2'], 
                c=colors[i], label=cluster_names[i], s=250, alpha=0.7, 
                edgecolors='black', linewidth=2, marker=markers[i])
    
    for idx, row in cluster_data.iterrows():
        plt.annotate(row['province'], 
                    (row['PCA1'], row['PCA2']),
                    fontsize=9, alpha=0.8, ha='center', fontweight='bold')

plt.xlabel(f'PCA 1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)', 
          fontsize=14, fontweight='bold')
plt.ylabel(f'PCA 2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)', 
          fontsize=14, fontweight='bold')
plt.title('Clustering Wilayah Rawan Bencana Indonesia\n(' +
          ', '.join(f'{i}={n} Risk' for i, n in enumerate(cluster_labels)) + ')',
          fontsize=18, fontweight='bold', pad=20)
plt.legend(fontsize=13, loc='best', frameon=True, shadow=True)
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('clustering_visualization.png', dpi=150, bbox_inches='tight')
print("✅ Saved: clustering_visualization.png")

# ========================================
# 10. CLUSTER COMPARISON
# ========================================
print("\n📊 STEP 10: CLUSTER COMPARISON")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Perbandingan Karakteristik Cluster\n(' +
             ', '.join(f'{i}={n}' for i, n in enumerate(cluster_labels)) + ')',
             fontsize=18, fontweight='bold', y=0.995)

_palette = ['#44AA44', '#FFA500', '#FF4444', '#8844AA', '#4488FF']
colors_cluster = _palette[:optimal_k]
xticks = list(range(optimal_k))
xticklabels = [f'{i}\n({n})' for i, n in enumerate(cluster_labels)]

def _bar(ax, series, ylabel, title):
    series = series.reindex(range(optimal_k))
    ax.bar(series.index, series.values, color=colors_cluster, edgecolor='black', linewidth=2)
    ax.set_xlabel('Cluster', fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)
    ax.grid(axis='y', alpha=0.3)
    pad = series.max() * 0.02  # offset label proporsional terhadap tinggi bar
    for i, v in zip(series.index, series.values):
        ax.text(i, v + pad, f'{v:.0f}', ha='center', fontweight='bold', fontsize=12)

# 1. Total Bencana
_bar(axes[0, 0], province_features.groupby('cluster')['total_disasters'].mean(),
     'Rata-rata Total Bencana', 'Total Kejadian Bencana')

# 2. Korban Jiwa
_bar(axes[0, 1], province_features.groupby('cluster')['total_death'].mean(),
     'Rata-rata Korban Meninggal', 'Korban Meninggal')

# 3. Rumah Rusak
_bar(axes[1, 0], province_features.groupby('cluster')['total_damaged_house'].mean(),
     'Rata-rata Rumah Rusak', 'Kerusakan Rumah')

# 4. Jumlah Provinsi
_bar(axes[1, 1], province_features['cluster'].value_counts().sort_index().astype(float),
     'Jumlah Provinsi', 'Distribusi Provinsi')

plt.tight_layout()
plt.savefig('cluster_comparison.png', dpi=150, bbox_inches='tight')
print("✅ Saved: cluster_comparison.png")

# ========================================
# 11. HEATMAP TOP 15 PROVINCES
# ========================================
print("\n📊 STEP 11: HEATMAP TOP 15 PROVINCES")

top15 = province_features.nlargest(15, 'total_disasters')[
    ['province', 'cluster', 'total_disasters', 'total_death', 
     'total_injured', 'total_damaged_house']
].copy()

top15_normalized = top15.copy()
for col in ['total_disasters', 'total_death', 'total_injured', 'total_damaged_house']:
    top15_normalized[col] = (top15[col] - top15[col].min()) / (top15[col].max() - top15[col].min())

plt.figure(figsize=(12, 10))
sns.heatmap(top15_normalized.set_index('province')[
    ['total_disasters', 'total_death', 'total_injured', 'total_damaged_house']
], annot=False, cmap='YlOrRd', cbar_kws={'label': 'Normalized Value'}, 
linewidths=0.5, linecolor='white')

plt.title('Heatmap: Top 15 Provinsi Paling Rawan Bencana (Normalized)', 
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Metrics', fontsize=12, fontweight='bold')
plt.ylabel('Provinsi', fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('province_heatmap.png', dpi=150, bbox_inches='tight')
print("✅ Saved: province_heatmap.png")

# ========================================
# SUMMARY
# ========================================
print("\n" + "="*70)
print("✅ CLUSTERING PROJECT COMPLETED!")
print("="*70)
print("\nOutput Files:")
print("  📄 clustering_province_features.csv")
print("  📄 clustering_results.csv")
print("  📊 elbow_method.png")
print("  📊 clustering_visualization.png")
print("  📊 cluster_comparison.png")
print("  📊 province_heatmap.png")
print("\n🍈 Project by Guava - Clustering Wilayah Rawan Bencana Indonesia")
print("="*70)
