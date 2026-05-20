# 🍈 Clustering Wilayah Rawan Bencana Indonesia

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Project Data Mining:** Clustering provinsi di Indonesia berdasarkan pola bencana alam menggunakan K-Means Clustering.

---

## 📋 Deskripsi Project

Project ini menganalisis dataset bencana alam Indonesia (2018-2024) dari BNPB untuk:
- ✅ Mengelompokkan provinsi berdasarkan risiko bencana
- ✅ Mengidentifikasi zona risiko tinggi, menengah, dan rendah
- ✅ Memberikan rekomendasi alokasi resources dan mitigasi bencana

**Dataset:** [Indonesia Natural Disaster Dataset (BNPB Records)](https://www.kaggle.com/datasets/maudiana/indonesia-natural-disaster-dataset-bnpb-records)

---

## 🎯 Hasil Clustering

> Clustering menggunakan **38 provinsi** (setelah normalisasi nama duplikat), dengan **log1p + RobustScaler** untuk meredam outlier bencana besar 2018 (Palu, Lombok, Selat Sunda). K=3 dipilih demi tingkatan risiko Low/High/Extreme.

### 🟢 **Cluster 0: LOW RISK**
- **4 provinsi:** Papua Barat Daya, Papua Pegunungan, Papua Selatan, Papua Tengah
- Rata-rata: 4 kejadian, 5 korban meninggal, 510 rumah rusak
- **Catatan:** risiko rendah lebih mencerminkan periode data sangat pendek (provinsi pemekaran 2022, ~1,5 thn), bukan tentu bebas risiko
- **Rekomendasi:** Lengkapi/pantau data & bangun kapasitas BPBD baru

### 🟠 **Cluster 1: HIGH RISK**
- **21 provinsi** (risiko menengah, mayoritas Indonesia)
- Rata-rata: 339 kejadian, 81 korban meninggal, 5.648 rumah rusak
- **Rekomendasi:** Prioritas mitigasi banjir & karhutla, perkuat early warning

### 🔴 **Cluster 2: EXTREME RISK**
- **13 provinsi:** Aceh, Bali, Banten, Jawa Barat, Jawa Tengah, Jawa Timur, Kalimantan Selatan, NTB, NTT, Sulawesi Selatan, Sulawesi Tengah, Sumatera Barat, Sumatera Utara
- Rata-rata: **1.665 kejadian**, **806 korban meninggal**, **56.011 rumah rusak** (tertinggi di semua metrik)
- **Rekomendasi:** Prioritas tertinggi — infrastruktur tahan bencana, early warning gempa/tsunami (Sulteng, NTB, Banten), mitigasi banjir & longsor (Pulau Jawa)

---

## 📊 Visualisasi

### 1. Elbow Method & Silhouette Score
![Elbow Method](elbow_method.png)

### 2. PCA Visualization
![Clustering Visualization](clustering_visualization.png)

### 3. Cluster Comparison
![Cluster Comparison](cluster_comparison.png)

### 4. Heatmap Top 15 Provinsi
![Province Heatmap](province_heatmap.png)

---

## 🚀 Cara Menjalankan

### **1. Clone Repository**
```bash
git clone https://github.com/GuavaPopper/Clustering_Datmin.git
cd Clustering_Datmin
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Jalankan Python Script**
```bash
python clustering_bencana.py
```

### **4. Atau Buka Jupyter Notebook**
```bash
jupyter notebook clustering_bencana.ipynb
```

---

## 📁 Struktur File

```
Clustering_Datmin/
│
├── data_bencana.xlsx                      # Dataset (download dari Kaggle)
├── clustering_bencana.py                  # Python script utama
├── clustering_bencana.ipynb               # Jupyter Notebook
├── requirements.txt                        # Dependencies
├── README.md                               # Dokumentasi
│
├── clustering_province_features.csv       # Feature matrix (output)
├── clustering_results.csv                 # Hasil clustering (output)
├── cluster_interpretation.txt             # Interpretasi cluster (output)
│
├── elbow_method.png                       # Visualisasi 1
├── clustering_visualization.png           # Visualisasi 2
├── cluster_comparison.png                 # Visualisasi 3
├── province_heatmap.png                   # Visualisasi 4
│
└── LAPORAN_CLUSTERING_BENCANA.md          # Laporan lengkap
```

---

## 🔧 Dependencies

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- openpyxl

Install semua dependencies:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl
```

---

## 📖 Metodologi

### 1️⃣ **Data Preprocessing**
- Handle missing values
- Normalisasi nama provinsi duplikat (40 → 38 provinsi)
- Feature engineering (agregasi per provinsi)
- **log1p transform + RobustScaler** (anti-outlier 2018, menggantikan StandardScaler)

### 2️⃣ **Feature Engineering**
- Total kejadian bencana per provinsi
- Total korban jiwa (meninggal, luka, hilang)
- Total kerusakan (rumah rusak, rumah terendam, fasilitas)
- Frekuensi per jenis bencana (banjir, longsor, cuaca ekstrem, dll.)

### 3️⃣ **Clustering**
- **Algoritma:** K-Means Clustering
- **Penentuan K:** Elbow Method + Silhouette Score (silhouette tertinggi di K=2 = 0.487)
- **Hasil:** **K=3** dipilih manual demi tingkatan risiko Low/High/Extreme yang lebih bermakna

### 4️⃣ **Relabeling Cluster**
- Cluster di-relabel berdasarkan composite severity score
- **0 = Low Risk, 1 = High Risk, 2 = Extreme Risk**

### 5️⃣ **Visualisasi**
- PCA 2D scatter plot (78.5% explained variance)
- Bar chart comparison
- Heatmap top 15 provinsi

---

## 📊 Key Insights

1. **Pulau Jawa = hotspot bencana** dengan 13,046 kejadian (45.3% total nasional)
2. **Banjir = ancaman #1** (8,605 kejadian atau 29.9%)
3. **Sulawesi Tengah** memiliki korban jiwa tertinggi akibat Gempa Palu 2018
4. **Jawa Barat, Jawa Tengah, Jawa Timur** memiliki frekuensi bencana paling tinggi

---

## 💡 Rekomendasi Kebijakan

### 🔴 **Untuk Cluster 2 (Extreme Risk - 13 provinsi)**
- **Prioritas #1** untuk early warning system gempa & tsunami (khususnya Sulteng, NTB, Banten)
- Penguatan infrastruktur tahan gempa & rumah tahan bencana
- Mitigasi **banjir** & **tanah longsor** untuk Pulau Jawa (drainase, normalisasi sungai, reboisasi)
- Evakuasi drills rutin untuk penduduk pesisir

### 🟠 **Untuk Cluster 1 (High Risk - 21 provinsi)**
- Fokus mitigasi **banjir** dan **kebakaran hutan & lahan**
- Perkuat sistem peringatan dini berbasis teknologi
- Maintain readiness (stock logistik, pelatihan SAR)

### 🟢 **Untuk Cluster 0 (Low Risk - 4 provinsi Papua pemekaran)**
- Lengkapi & pantau pengumpulan data (periode masih pendek)
- Bangun kapasitas BPBD provinsi baru
- Strengthen local capacity (relawan, infrastruktur dasar kebencanaan)

---

## 📈 Pengembangan Lebih Lanjut

- [ ] Clustering per kabupaten/kota (lebih granular)
- [ ] Time series forecasting untuk prediksi bencana
- [ ] Dashboard interaktif dengan Streamlit/Plotly Dash
- [ ] Geospatial analysis dengan peta Indonesia interaktif
- [ ] Integration dengan data cuaca & topografi real-time

---

## 👨‍💻 Author

**Guava** 🍈  
Mahasiswa Teknik Informatika, Universitas Tanjungpura (UNTAN)

---

## 📄 License

MIT License - feel free to use this project for learning purposes!

---

## 🙏 Acknowledgments

- Dataset: [BNPB (Badan Nasional Penanggulangan Bencana)](https://bnpb.go.id/)
- Kaggle Dataset by [maudiana](https://www.kaggle.com/datasets/maudiana/indonesia-natural-disaster-dataset-bnpb-records)

---

**⭐ Jangan lupa kasih star kalau project ini bermanfaat!**
