# Dokumen Pengembangan Produk - Aplikasi Klasifikasi E. coli

## Gambaran Umum Proyek
Pengembangan aplikasi berbasis web untuk klasifikasi protein E. coli menggunakan ensemble learning yang menggabungkan Decision Tree dan XGBoost, dengan antarmuka web interaktif menggunakan Streamlit.

## Komponen

### 1. Dataset
- Berkas: `ecoli.csv`
- Jumlah sampel: 336 protein E. coli
- Spesifikasi:
  - Fitur Input (7 karakteristik):
    - MCG: McGeoch Signal Sequence (0.0 - 1.0)
    - GVH: von Heijne Signal Sequence (0.0 - 1.0)
    - LIP: von Heijne Signal Peptidase II (0.0 - 1.0)
    - CHG: Presence of Charge (0.0 - 1.0)
    - AAC: Score of discriminant analysis (0.0 - 1.0)
    - ALM1: Score of ALOM program (0.0 - 1.0)
    - ALM2: Score of ALOM after excluding putative cleavable signal regions (0.0 - 1.0)
  - Variabel Target: 'class' (lokasi protein)

### 2. Model Machine Learning
#### A. Implementasi Model (`train.py`)
- Ensemble Model dengan Voting Classifier:
  1. Decision Tree:
     - max_depth: 10
     - min_samples_split: 5
     - min_samples_leaf: 2
  2. XGBoost:
     - n_estimators: 100
     - max_depth: 10
     - learning_rate: 0.1
     - subsample: 0.8
     - colsample_bytree: 0.8
- Voting: Soft voting dengan bobot [1, 2] (lebih berat pada XGBoost)
- Preprocessing: StandardScaler untuk normalisasi fitur
- Rasio Train-Test Split: 80% training, 20% testing

#### B. Performa Model
- Akurasi Keseluruhan: 96.13%
- Performa per Kelas:
  - Cytoplasm (cp): 97.24% presisi, 98.60% recall
  - Inner membrane (im): 93.75% presisi, 97.40% recall
  - Inner membrane with signal sequence (imS): 0% (keterbatasan data)
  - Inner membrane, uncleavable signal sequence (imU): 100% presisi, 94.29% recall
  - Outer membrane (om): 100% presisi dan recall
  - Outer membrane lipoprotein (omL): 100% presisi dan recall
  - Periplasm (pp): 92.45% presisi, 94.23% recall

#### C. Output Model
- Model terlatih: `ecoli.model`
- Scaler: `scaler.pkl`
- File evaluasi:
  - `pr.csv`: Detail prediksi per sampel
  - `pr_summary.csv`: Ringkasan metrik performa

### 3. Aplikasi Web (`app.py`)
- Framework: Streamlit 1.26.0
- Fitur yang Diimplementasikan:
  - Form input dengan 7 karakteristik protein
  - Validasi input (range 0.0 - 1.0)
  - Layout 2 kolom untuk input yang rapi
  - Hasil prediksi:
    - Lokasi protein yang diprediksi
    - Probabilitas untuk setiap kelas dengan highlight
    - Deskripsi lengkap setiap lokasi
  - Caching untuk model loading
  - Penanganan error untuk input tidak valid

### 4. Evaluasi Model (`evaluate_model.py`)
- Analisis performa lengkap
- Identifikasi misklasifikasi
- Generasi laporan detail
- Visualisasi hasil prediksi

## Persyaratan Teknis
1. Bahasa Pemrograman: Python 3.11+
2. Dependensi:
   - pandas==2.1.0
   - numpy==1.24.3
   - scikit-learn==1.3.0
   - streamlit==1.26.0
   - joblib==1.3.2
   - xgboost==2.0.0

## Kriteria Keberhasilan
✅ Model mencapai akurasi tinggi (96.13%)
✅ Performa sempurna untuk beberapa kelas (om, omL)
✅ Antarmuka web responsif dan user-friendly
✅ Prediksi real-time berfungsi dengan baik
✅ Visualisasi hasil yang informatif
✅ Penanganan error yang robust
✅ Dokumentasi lengkap

## Kelas Target dan Deskripsi
- **cp**: Sitoplasma
  - Performa: 97.24% presisi, 98.60% recall
- **im**: Membran dalam tanpa urutan sinyal
  - Performa: 93.75% presisi, 97.40% recall
- **imS**: Membran dalam dengan urutan sinyal
  - Catatan: Performa rendah karena keterbatasan data
- **imU**: Membran dalam, urutan sinyal tidak dapat dipotong
  - Performa: 100% presisi, 94.29% recall
- **om**: Membran luar
  - Performa: 100% presisi dan recall
- **omL**: Lipoprotein membran luar
  - Performa: 100% presisi dan recall
- **pp**: Periplasma
  - Performa: 92.45% presisi, 94.23% recall

## Keterbatasan dan Potensi Pengembangan
1. Keterbatasan:
   - Kelas imS memiliki performa rendah karena keterbatasan data
   - Beberapa kesalahan klasifikasi antara cp-pp dan im-cp

2. Potensi Pengembangan:
   - Pengumpulan data tambahan untuk kelas imS
   - Implementasi teknik augmentasi data
   - Penambahan fitur visualisasi hasil prediksi
   - Pengembangan API untuk integrasi dengan sistem lain
