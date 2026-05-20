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

- **Jumlah Data:** 28.772 kejadian bencana (setelah cleaning)
- **Periode:** 1 Januari 2018 – 21 Mei 2024
- **Cakupan:** **38 provinsi** (setelah normalisasi nama duplikat)
- **Level Data:** Per kabupaten/kota per kejadian

---

## 🔧 PREPROCESSING & PENANGANAN ANOMALI 2018

Tahun 2018 memuat beberapa bencana katastropik (Gempa-Tsunami Palu di Sulawesi Tengah, Gempa Lombok di NTB, Tsunami Selat Sunda di Banten) yang membuat **satu kejadian mendominasi total provinsi** dan mengganggu clustering. Beberapa langkah diambil untuk menanganinya:

### 1. Handling Missing Values
- `death`: 1 missing → di-drop
- `missing_person`, `flooded_house`, `damaged_house`, `damaged_facility`: di-fill 0

### 2. Normalisasi Nama Provinsi Duplikat
- `P A P U A` → `PAPUA`
- `DAERAH ISTIMEWA YOGYAKARTA` → `DI YOGYAKARTA`
- Hasil: **40 → 38 provinsi** (provinsi pemekaran Papua 2022 tetap terpisah)

### 3. Feature Engineering
Agregasi per provinsi (19 fitur): total bencana, korban (meninggal/luka/hilang), kerusakan (rumah rusak/terendam/fasilitas), dan frekuensi per jenis bencana.

### 4. Transformasi & Scaling (anti-outlier)
- **`log1p`** pada seluruh fitur → meredam ekor kanan ekstrem agar satu bencana 2018 tidak mendominasi.
- **`RobustScaler`** (median & IQR) menggantikan StandardScaler → tahan terhadap sisa outlier.

---

## 📊 CLUSTERING

### Penentuan Jumlah Cluster

| K | Silhouette Score |
|---|------------------|
| 2 | **0.4871** (tertinggi) |
| 3 | 0.3315 |
| 4 | 0.2963 |

- Secara statistik silhouette memuncak di **K=2**, karena 5 provinsi pemekaran Papua (data hanya ~1,5 tahun) menjadi outlier "miskin data" yang memisah kuat.
- **Keputusan: K=3 (override manual)** demi tingkatan risiko Low / High / Extreme yang lebih bermakna dan actionable.
- **PCA explained variance:** PCA1 70,1% + PCA2 8,4% = **78,5%**.

### Ringkasan Karakteristik (rata-rata per provinsi)

| Metrik | 🟢 Cluster 0 (Low) | 🟠 Cluster 1 (High) | 🔴 Cluster 2 (Extreme) |
|--------|---:|---:|---:|
| Jumlah provinsi | 4 | 21 | 13 |
| Total bencana | 4,5 | 338,7 | 1.664,8 |
| Korban meninggal | 4,5 | 80,7 | 806,1 |
| Korban luka | 10,5 | 1.118,4 | 4.032,3 |
| Rumah rusak | 509,5 | 5.648,3 | 56.010,9 |
| Rumah terendam | 1.955 | 90.844 | 339.755 |

> Gradasi metrik naik konsisten (Low < High < Extreme) di semua dimensi — pelabelan sudah valid.

---

## 🗂️ DAFTAR PROVINSI PER CLUSTER

### 🟢 CLUSTER 0 — LOW RISK (4 provinsi)
Provinsi pemekaran Papua 2022 dengan periode data sangat pendek (kejadian sangat sedikit).

1. PAPUA BARAT DAYA
2. PAPUA PEGUNUNGAN
3. PAPUA SELATAN
4. PAPUA TENGAH

**Bencana dominan:** Banjir (13), Tanah Longsor (3)
**Catatan:** Risiko rendah di sini lebih mencerminkan **keterbatasan periode data** (~1,5 thn), bukan tentu bebas risiko. Perlu pemantauan lanjutan saat datanya lengkap.

---

### 🟠 CLUSTER 1 — HIGH RISK (21 provinsi)
Provinsi dengan risiko menengah — frekuensi & dampak signifikan namun di bawah zona ekstrem.

1. BENGKULU
2. DI YOGYAKARTA
3. DKI JAKARTA
4. GORONTALO
5. JAMBI
6. KALIMANTAN BARAT
7. KALIMANTAN TENGAH
8. KALIMANTAN TIMUR
9. KALIMANTAN UTARA
10. KEPULAUAN BANGKA BELITUNG
11. KEPULAUAN RIAU
12. LAMPUNG
13. MALUKU
14. MALUKU UTARA
15. PAPUA
16. PAPUA BARAT
17. RIAU
18. SULAWESI BARAT
19. SULAWESI TENGGARA
20. SULAWESI UTARA
21. SUMATERA SELATAN

**Bencana dominan:** Banjir (2.734), Kebakaran Hutan & Lahan (2.297), Cuaca Ekstrem (997), Tanah Longsor (634)

---

### 🔴 CLUSTER 2 — EXTREME RISK (13 provinsi)
Provinsi paling rawan — frekuensi tinggi dan/atau dampak korban & kerusakan terbesar.

1. ACEH
2. BALI
3. BANTEN
4. JAWA BARAT
5. JAWA TENGAH
6. JAWA TIMUR
7. KALIMANTAN SELATAN
8. NUSA TENGGARA BARAT
9. NUSA TENGGARA TIMUR
10. SULAWESI SELATAN
11. SULAWESI TENGAH
12. SUMATERA BARAT
13. SUMATERA UTARA

**Bencana dominan:** Cuaca Ekstrem (6.271), Banjir (5.858), Tanah Longsor (4.948), Kebakaran Hutan & Lahan (2.670)

**Sorotan provinsi (efek 2018 kini terdistribusi wajar):**
- **Jawa Barat** — frekuensi tertinggi nasional (6.159 kejadian, 130.493 rumah rusak).
- **Sulawesi Tengah** — korban meninggal tertinggi (4.261) & rumah rusak 113.903 akibat Gempa-Tsunami Palu 2018. Kini **berkelompok wajar** bersama provinsi ekstrem lain, bukan lagi cluster tunggal.
- **Nusa Tenggara Barat** — rumah rusak tertinggi nasional (234.980) akibat Gempa Lombok 2018.
- **Banten** — korban luka tinggi (10.966) akibat Tsunami Selat Sunda 2018.

---

## 📈 KEY INSIGHTS

### Top 10 Provinsi Berdasarkan Frekuensi Bencana
1. Jawa Barat — 6.159
2. Jawa Tengah — 4.500
3. Jawa Timur — 2.387
4. Aceh — 1.548
5. Kalimantan Selatan — 1.403
6. Sulawesi Selatan — 1.182
7. Sumatera Barat — 921
8. Sumatera Utara — 848
9. Riau — 721
10. Kalimantan Tengah — 653

### Jenis Bencana Paling Sering (Nasional)
1. Banjir — 8.605 (29,9%)
2. Cuaca Ekstrem — 7.268 (25,3%)
3. Tanah Longsor — 5.585 (19,4%)
4. Kebakaran Hutan & Lahan — 4.967 (17,3%)
5. Puting Beliung — 1.113 (3,9%)

---

## 🎯 KESIMPULAN & REKOMENDASI

1. **Tiga zona risiko Indonesia (K=3):**
   - 🟢 **Low (4 prov, Papua pemekaran):** lengkapi/pantau data; bangun kapasitas BPBD baru.
   - 🟠 **High (21 prov):** prioritas mitigasi banjir & karhutla; perkuat early warning.
   - 🔴 **Extreme (13 prov):** prioritas tertinggi — infrastruktur tahan bencana, sistem peringatan dini gempa/tsunami (khususnya Sulteng, NTB, Banten), normalisasi sungai & mitigasi longsor (Pulau Jawa).

2. **Pulau Jawa = hotspot frekuensi** (Jabar, Jateng, Jatim) → fokus banjir, longsor, cuaca ekstrem.

3. **Catatan metodologis:** silhouette optimal sebenarnya K=2; K=3 dipilih untuk narasi 3 tingkatan. Alternatif: gabungkan/keluarkan provinsi Papua pemekaran agar tingkatan lebih murni berbasis risiko (bukan ketersediaan data).

---

## 📁 OUTPUT FILES

| File | Deskripsi |
|------|-----------|
| `clustering_province_features.csv` | Feature matrix (19 fitur × 38 provinsi) |
| `clustering_results.csv` | Hasil clustering + label cluster per provinsi |
| `elbow_method.png` | Elbow & Silhouette score |
| `clustering_visualization.png` | PCA scatter plot (78,5% variance) |
| `cluster_comparison.png` | Bar chart perbandingan karakteristik |
| `province_heatmap.png` | Heatmap top 15 provinsi |

---

**Prepared by:** Guava 🍈
**Date:** 20 Mei 2026
**Tools:** Python 3.13, Pandas, Scikit-learn, Matplotlib, Seaborn
