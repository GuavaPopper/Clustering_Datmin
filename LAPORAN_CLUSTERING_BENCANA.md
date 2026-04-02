# 📊 LAPORAN PROJECT: CLUSTERING WILAYAH RAWAN BENCANA INDONESIA

**Dataset:** Indonesia Natural Disaster Dataset (BNPB Records 2018-2024)  
**Metode:** K-Means Clustering  
**Tools:** Python (Pandas, Scikit-learn, Matplotlib, Seaborn)

---

## 🎯 TUJUAN PROJECT

Mengelompokkan provinsi di Indonesia berdasarkan pola bencana alam untuk:
1. Identifikasi zona risiko bencana
2. Rekomendasi alokasi resources BNPB
3. Prioritas mitigasi per wilayah

---

## 📂 DATA OVERVIEW

- **Jumlah Data:** 28,772 kejadian bencana
- **Periode:** 1 Januari 2018 - 21 Mei 2024
- **Cakupan:** 40 provinsi di Indonesia
- **Level Data:** Per kabupaten/kota per kejadian

### Kolom Dataset:
1. `city_id` - ID kota/kabupaten
2. `date` - Tanggal kejadian
3. `disaster_type` - Jenis bencana
4. `city` - Nama kota/kabupaten
5. `province` - Nama provinsi
6. `cause` - Penyebab bencana
7. `death` - Korban meninggal
8. `missing_person` - Orang hilang
9. `injured_person` - Korban luka
10. `damaged_house` - Rumah rusak
11. `flooded_house` - Rumah terendam
12. `damaged_facility` - Fasilitas rusak

---

## 🔧 PREPROCESSING

### 1. Handling Missing Values
- `death`: 1 missing value → di-drop
- `missing_person`, `flooded_house`, `damaged_house`, `damaged_facility`: Missing values di-fill dengan 0

### 2. Feature Engineering
Agregasi data per provinsi:
- **Total kejadian bencana**
- **Total korban jiwa** (meninggal, luka, hilang)
- **Total kerusakan** (rumah rusak, rumah terendam, fasilitas)
- **Frekuensi per jenis bencana** (banjir, longsor, cuaca ekstrem, dll)

**Total fitur:** 19 features per provinsi

### 3. Standardization
Data di-standardize menggunakan `StandardScaler` untuk menghindari bias skala.

---

## 📊 CLUSTERING

### Metode: K-Means Clustering

**Penentuan Jumlah Cluster Optimal:**
- **Elbow Method:** Menunjukkan K=3 atau K=4 sebagai kandidat
- **Silhouette Score:** K=3 memiliki score tertinggi (0.5920)
- **Keputusan:** **K=3** dipilih

### Hasil Clustering:

#### 🟢 **CLUSTER 0: LOW-MODERATE RISK ZONE**
- **Jumlah Provinsi:** 36 (mayoritas Indonesia)
- **Provinsi:** Aceh, Bali, Banten, Bengkulu, DI Yogyakarta, DKI Jakarta, dll.

**Karakteristik:**
- Total Bencana: 422 kejadian
- Korban Meninggal: 130
- Korban Luka: 1,396
- Rumah Rusak: 14,450
- Rumah Terendam: 107,726

**Bencana Dominan:**
1. Banjir (5,481 kejadian)
2. Kebakaran Hutan & Lahan (3,929 kejadian)
3. Cuaca Ekstrem (3,202 kejadian)

**Insight:** Provinsi-provinsi ini memiliki risiko bencana yang lebih moderat, namun tetap perlu kesiapsiagaan terutama untuk banjir dan kebakaran hutan.

**Rekomendasi:**
- ✅ Maintain readiness (stock logistik, pelatihan SAR)
- 🔥 Mitigasi kebakaran hutan (patroli, kampanye anti-pembakaran)
- 💪 Strengthen local capacity (BPBD, relawan)

---

#### 🟠 **CLUSTER 1: EXTREME RISK ZONE**
- **Jumlah Provinsi:** 1
- **Provinsi:** SULAWESI TENGAH

**Karakteristik:**
- Total Bencana: 525 kejadian
- **Korban Meninggal: 4,261 (TERTINGGI!)**
- Korban Luka: 5,324
- Rumah Rusak: 113,903
- Rumah Terendam: 63,156

**Bencana Dominan:**
1. Banjir (384 kejadian)
2. Cuaca Ekstrem (65 kejadian)
3. Gelombang Pasang/Abrasi (22 kejadian)

**Insight:** Sulawesi Tengah memiliki tingkat keparahan bencana tertinggi, terutama karena gempa & tsunami Palu 2018 yang menyebabkan ribuan korban jiwa.

**Rekomendasi:**
- ⚠️ **Prioritas #1** untuk early warning system
- Penguatan infrastruktur tahan gempa & tsunami
- Evakuasi drills rutin untuk penduduk pesisir

---

#### 🔴 **CLUSTER 2: HIGH RISK ZONE**
- **Jumlah Provinsi:** 3
- **Provinsi:** JAWA BARAT, JAWA TENGAH, JAWA TIMUR

**Karakteristik:**
- **Total Bencana: 4,349 kejadian (TERTINGGI!)**
- Korban Meninggal: 1,082
- Korban Luka: 6,783
- Rumah Rusak: 71,560
- **Rumah Terendam: 797,016 (TERTINGGI!)**

**Bencana Dominan:**
1. Tanah Longsor (4,094 kejadian)
2. Cuaca Ekstrem (4,001 kejadian)
3. Banjir (2,740 kejadian)

**Insight:** Pulau Jawa memiliki frekuensi bencana paling tinggi karena kepadatan penduduk, curah hujan tinggi, dan kondisi geografis (pegunungan + dataran rendah).

**Rekomendasi:**
- 🌊 Fokus pada **mitigasi banjir** (drainase, waduk, normalisasi sungai)
- ⛰️ Mitigasi longsor (reboisasi, retaining walls)
- 🏗️ Infrastruktur resilient (rumah tahan bencana)
- 📱 Sistem peringatan dini berbasis teknologi (SMS blast, app)

---

## 📈 KEY INSIGHTS

### Top 10 Provinsi Paling Rawan Bencana (Berdasarkan Frekuensi):
1. **Jawa Barat:** 6,159 kejadian
2. **Jawa Tengah:** 4,500 kejadian
3. **Jawa Timur:** 2,387 kejadian
4. **Aceh:** 1,548 kejadian
5. **Kalimantan Selatan:** 1,403 kejadian
6. **Sulawesi Selatan:** 1,182 kejadian
7. **Sumatera Barat:** 921 kejadian
8. **Sumatera Utara:** 848 kejadian
9. **Riau:** 721 kejadian
10. **Kalimantan Tengah:** 653 kejadian

### Jenis Bencana Paling Sering (Nasional):
1. **Banjir:** 8,605 kejadian (29.9%)
2. **Cuaca Ekstrem:** 7,268 kejadian (25.3%)
3. **Tanah Longsor:** 5,585 kejadian (19.4%)
4. **Kebakaran Hutan & Lahan:** 4,967 kejadian (17.3%)
5. **Puting Beliung:** 1,113 kejadian (3.9%)

---

## 📊 VISUALISASI

### Files yang Dihasilkan:

1. **`elbow_method.png`**
   - Grafik Elbow Method & Silhouette Score
   - Menunjukkan K=3 sebagai optimal

2. **`clustering_visualization.png`**
   - Scatter plot PCA (2 komponen)
   - Visualisasi 3 cluster dengan label provinsi
   - Explained variance: 63.16%

3. **`cluster_comparison.png`**
   - Bar chart perbandingan karakteristik cluster
   - 4 metrics: Total Bencana, Korban Jiwa, Rumah Rusak, Jumlah Provinsi

4. **`province_heatmap.png`**
   - Heatmap top 15 provinsi paling rawan
   - Normalized values untuk 4 metrics utama

---

## 📁 OUTPUT FILES

| File | Deskripsi |
|------|-----------|
| `clustering_province_features.csv` | Feature matrix (19 features × 40 provinsi) |
| `clustering_results.csv` | Hasil clustering dengan label cluster per provinsi |
| `cluster_interpretation.txt` | Interpretasi detail setiap cluster |
| `elbow_method.png` | Grafik penentuan K optimal |
| `clustering_visualization.png` | PCA visualization |
| `cluster_comparison.png` | Bar chart comparison |
| `province_heatmap.png` | Heatmap top 15 provinsi |

---

## 🎯 KESIMPULAN

1. **Indonesia memiliki 3 zona risiko bencana yang berbeda:**
   - **Cluster 0 - Low-Moderate Risk (36 prov):** Maintain readiness & local capacity
   - **Cluster 1 - Extreme Risk (Sulteng):** Prioritas tertinggi untuk mitigasi gempa & tsunami
   - **Cluster 2 - High Risk (Jawa):** Fokus pada banjir, longsor, cuaca ekstrem

2. **Pulau Jawa adalah hotspot bencana** dengan 13,046 kejadian (45.3% dari total nasional)

3. **Banjir adalah ancaman #1** (8,605 kejadian), disusul cuaca ekstrem dan tanah longsor

4. **Rekomendasi kebijakan:**
   - Alokasi budget BNPB proporsional dengan cluster risk
   - Early warning system berbasis teknologi untuk Cluster 0 & 1
   - Infrastruktur resilient untuk Pulau Jawa
   - Edukasi & drills rutin untuk seluruh Indonesia

---

## 🔬 METODE EVALUASI

- **Silhouette Score:** 0.5920 (K=3) → Good clustering quality
- **Inertia:** Menunjukkan separation yang jelas antar cluster
- **Explained Variance (PCA):** 63.16% → Representasi visual yang cukup baik

---

## 💡 SARAN PENGEMBANGAN

1. **Clustering per kabupaten/kota** (lebih granular)
2. **Time series forecasting** untuk prediksi bencana per wilayah
3. **Geospatial analysis** dengan peta interaktif Indonesia
4. **Dashboard interaktif** (Streamlit/Plotly Dash) untuk visualisasi real-time
5. **Integration dengan data cuaca & topografi** untuk model prediktif yang lebih akurat

---

**Prepared by:** Guava 🍈  
**Date:** 2 April 2026  
**Tools:** Python 3.12, Pandas, Scikit-learn, Matplotlib, Seaborn
