# Changelog - Perbaikan Clustering Bencana Indonesia

## Ringkasan Perubahan
Project telah diperbaiki untuk menghilangkan bugs dan meningkatkan robustness kode. Semua perubahan fokus pada:
1. Menghilangkan deprecated pandas syntax
2. Membuat array visualisasi dinamis (aman untuk K berapa pun)
3. Memperbaiki konsistensi label cluster semantik

---

## Detail Perubahan

### 1. Fix FutureWarning: `fillna(inplace=True)` (📝 Pandas Deprecation)

**File yang diubah:** 
- `clustering_bencana.py` (line 41-45)
- `clustering_bencana.ipynb` (cell-9)

**Sebelum:**
```python
df['missing_person'].fillna(0, inplace=True)
df['injured_person'].fillna(0, inplace=True)
df['flooded_house'].fillna(0, inplace=True)
df['damaged_house'].fillna(0, inplace=True)
df['damaged_facility'].fillna(0, inplace=True)
```

**Sesudah:**
```python
for col in ['missing_person', 'injured_person', 'flooded_house', 'damaged_house', 'damaged_facility']:
    df[col] = df[col].fillna(0)
```

**Alasan:** Pandas ≥2.1 mengeluarkan `FutureWarning` untuk `inplace=True`. Cara baru lebih clean dan future-proof.

---

### 2. Generalisasi Array Visualisasi (🛡️ Robustness)

**File yang diubah:**
- `clustering_bencana.py` (line 222-227)
- `clustering_bencana.ipynb` (cell-35)

**Sebelum:**
```python
colors = ['#44AA44', '#FFA500', '#FF4444']
cluster_names = ['Cluster 0: LOW RISK', 'Cluster 1: EXTREME RISK', 'Cluster 2: HIGH RISK']
markers = ['o', '^', 's']
```

**Sesudah:**
```python
_all_colors  = ['#44AA44', '#FFA500', '#FF4444', '#8844AA', '#4488FF']
_all_names   = ['Cluster 0: LOW RISK', 'Cluster 1: HIGH RISK', 'Cluster 2: EXTREME RISK',
                'Cluster 3: RISK-4', 'Cluster 4: RISK-5']
_all_markers = ['o', '^', 's', 'D', 'P']
colors        = _all_colors[:optimal_k]
cluster_names = _all_names[:optimal_k]
markers       = _all_markers[:optimal_k]
```

**Alasan:** 
- Array hardcoded panjang 3 akan crash dengan IndexError jika `optimal_k` ≠ 3
- Sekarang aman untuk K = 2, 3, 4, 5, atau lebih
- List `_all_*` dapat diperluas jika diperlukan K lebih besar

---

### 3. Perbaikan Label Cluster Semantik (🏷️ Consistency)

**File yang diubah:**
- `clustering_bencana.py` (8 lokasi)
- `clustering_bencana.ipynb` (4 cells)
- `README.md` (2 bagian)

**Perubahan label:**

| Sebelum | Sesudah | Alasan |
|---------|---------|--------|
| 0 = Low Risk | 0 = Low Risk | ✅ Sama (tetap) |
| 1 = Extreme Risk | 1 = High Risk | ⚠️ Jawa (frekuensi tertinggi) = High, bukan Extreme |
| 2 = High Risk | 2 = Extreme Risk | ⚠️ Sulteng (korban jiwa tertinggi) = Extreme, bukan High |

**Lokasi perubahan di script:**
- Line 183: print relabel message
- Line 241-242: PCA title
- Line 255-256: Cluster Comparison suptitle
- Line 267-268, 279-280, 292-293, 306-307: xticklabels di 4 subplot

**Lokasi perubahan di notebook:**
- Cell-27: Section header "Relabel Cluster"
- Cell-29: Print message
- Cell-35: PCA title & cluster_names
- Cell-37: Suptitle & xticklabels

**Lokasi perubahan di README:**
- Line 30-37: Cluster descriptions
- Line 145: Metodologi section
- Line 165-174: Rekomendasi Kebijakan

**Alasan:**
- Konsistensi semantik: "Extreme" harus lebih parah dari "High"
- Sebelumnya rank 2 (tertinggi) = "High", padahal harus "Extreme"
- Sulawesi Tengah (4,261 korban jiwa) > Jawa (frekuensi 4,349) → Extreme > High ✅

---

## File Output yang Dihasilkan

Ketika script dijalankan (dengan `data_bencana.xlsx` tersedia):

```
📊 Output CSV:
  ├── clustering_province_features.csv    [Feature matrix per provinsi]
  └── clustering_results.csv              [Hasil clustering + PCA coords]

📈 Output PNG:
  ├── elbow_method.png                    [Elbow + Silhouette Score]
  ├── clustering_visualization.png        [PCA scatter plot 2D]
  ├── cluster_comparison.png              [4 bar charts comparison]
  └── province_heatmap.png                [Heatmap top 15 provinsi]
```

---

## Testing Verification

✅ Semua perubahan sudah diterapkan. Untuk verifikasi:

1. **Jalankan script:**
   ```bash
   python clustering_bencana.py
   ```
   
   Cek:
   - ❌ Tidak ada FutureWarning dari fillna
   - ❌ Tidak ada IndexError dari array
   - ✅ Output menampilkan "Cluster 1 = High Risk, Cluster 2 = Extreme Risk"

2. **Jalankan notebook:**
   ```bash
   jupyter notebook clustering_bencana.ipynb
   ```
   
   Cek:
   - ✅ Semua cell eksekusi tanpa error
   - ✅ Visualization title konsisten: "0=Low, 1=High, 2=Extreme"

3. **Cek file output:**
   - `clustering_results.csv` → cluster column harus 0, 1, 2 (tidak ada error indexing)

---

## Notes untuk Developer

- **Jika K berubah:** Array `_all_colors/names/markers` sudah siap untuk K hingga 5. Jika perlu K > 5, tambah warna & marker di list.
- **Jika severity formula berubah:** Relabeling otomatis menyesuaikan berdasarkan rank composite score.
- **Backward compatibility:** CSV output structure tidak berubah, hanya makna cluster label yang diperbaiki.

---

**Last Updated:** 2026-05-20  
**Status:** ✅ All fixes applied
