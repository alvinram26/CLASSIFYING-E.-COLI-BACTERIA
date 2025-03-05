# Klasifikasi Lokasi Protein E. coli Menggunakan Ensemble Learning

## Abstrak
Penelitian ini mengembangkan sistem klasifikasi lokasi protein E. coli menggunakan pendekatan ensemble learning yang menggabungkan Decision Tree dan XGBoost. Model ini mampu mengklasifikasikan protein ke dalam 8 lokasi subseluler berdasarkan karakteristik fisikokimia protein. Hasil menunjukkan akurasi keseluruhan 96.13%, dengan performa sempurna untuk beberapa kelas lokasi protein.

## Latar Belakang
Prediksi lokasi protein dalam sel E. coli merupakan langkah penting dalam memahami fungsi protein dan interaksinya dalam sistem seluler. Penelitian ini menggunakan pendekatan machine learning untuk mengotomatisasi proses klasifikasi berdasarkan karakteristik protein yang dapat diukur.

## Metodologi

### Dataset
Dataset terdiri dari 336 protein E. coli dengan 7 fitur:
- MCG: McGeoch Signal Sequence (0.0 - 1.0)
- GVH: von Heijne Signal Sequence (0.0 - 1.0)
- LIP: von Heijne Signal Peptidase II (0.0 - 1.0)
- CHG: Presence of Charge (0.0 - 1.0)
- AAC: Score of discriminant analysis (0.0 - 1.0)
- ALM1: Score of ALOM program (0.0 - 1.0)
- ALM2: Score of ALOM after excluding putative cleavable signal regions (0.0 - 1.0)

### Kelas Output
Model memprediksi lokasi protein dalam kategori berikut:
- **cp**: Sitoplasma
- **im**: Membran dalam tanpa urutan sinyal
- **imS**: Membran dalam dengan urutan sinyal
- **imU**: Membran dalam, urutan sinyal tidak dapat dipotong
- **om**: Membran luar
- **omL**: Lipoprotein membran luar
- **pp**: Periplasma

### Model dan Teknologi
#### 1. Model Ensemble
Menggabungkan dua algoritma:
1. Decision Tree
   - max_depth: 10
   - min_samples_split: 5
   - min_samples_leaf: 2

2. XGBoost
   - n_estimators: 100
   - max_depth: 10
   - learning_rate: 0.1
   - subsample: 0.8
   - colsample_bytree: 0.8

#### 2. Teknologi yang Digunakan
- Python 3.11+
- Streamlit 1.26.0: Framework web interface
- scikit-learn 1.3.0: Implementasi Decision Tree dan metrics
- XGBoost 2.0.0: Implementasi gradient boosting
- pandas 2.1.0: Manipulasi data
- numpy 1.24.3: Komputasi numerik
- joblib 1.3.2: Serialisasi model

### Struktur Proyek
```
ecoli/
├── README.md           # Dokumentasi penelitian
├── requirements.txt    # Daftar dependensi
├── train.py           # Script pelatihan model
├── app.py             # Aplikasi web Streamlit
├── evaluate_model.py   # Script evaluasi detail
├── ecoli.csv          # Dataset
├── ecoli.model        # Model terlatih
├── scaler.pkl         # Scaler preprocessing
├── pr.csv             # Hasil evaluasi detail
├── pr_summary.csv     # Ringkasan metrik
└── prd.md             # Dokumen kebutuhan
```

### Implementasi dan Penggunaan

#### 1. Prasyarat
- Python 3.11 atau lebih tinggi
- pip (Python package manager)

#### 2. Instalasi
1. Clone atau download repository:
   ```bash
   git clone [URL_REPOSITORY]
   cd ecoli
   ```

2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

#### 3. Komponen Utama

##### A. Training Model (`train.py`)
1. Melatih model ensemble:
   ```bash
   python train.py
   ```
   - Membaca dataset dari `ecoli.csv`
   - Preprocessing menggunakan StandardScaler
   - Melatih model ensemble (Decision Tree + XGBoost)
   - Menyimpan model ke `ecoli.model` dan scaler ke `scaler.pkl`

##### B. Web Interface (`app.py`)
1. Menjalankan aplikasi web:
   ```bash
   streamlit run app.py
   ```
   - Akses melalui `http://localhost:8501`
   - Input 7 karakteristik protein (nilai 0.0 - 1.0)
   - Tampilan hasil:
     * Prediksi lokasi protein
     * Probabilitas untuk setiap kelas
     * Highlight probabilitas tertinggi
     * Deskripsi lokasi

##### C. Evaluasi Model (`evaluate_model.py`)
1. Menjalankan evaluasi detail:
   ```bash
   python evaluate_model.py
   ```
   - Menghasilkan `pr.csv`: Detail per sampel
   - Menghasilkan `pr_summary.csv`: Metrik per kelas
   - Menampilkan analisis kesalahan prediksi

## Hasil dan Diskusi

### Performa Model
1. Akurasi Keseluruhan: 96.13%
2. Performa per Kelas:
   - Cytoplasm (cp): 97.24% presisi, 98.60% recall
   - Inner membrane (im): 93.75% presisi, 97.40% recall
   - Inner membrane with signal sequence (imS): 0% (keterbatasan data)
   - Inner membrane, uncleavable signal sequence (imU): 100% presisi, 94.29% recall
   - Outer membrane (om): 100% presisi dan recall
   - Outer membrane lipoprotein (omL): 100% presisi dan recall
   - Periplasm (pp): 92.45% presisi, 94.23% recall

### Analisis Kesalahan
1. Kesulitan dalam memprediksi kelas dengan sampel terbatas (imS, imL)
2. Beberapa kesalahan klasifikasi antara:
   - cp dan pp
   - im dan cp

## Kesimpulan
Model ensemble berhasil mengklasifikasikan lokasi protein E. coli dengan akurasi tinggi, terutama untuk kelas-kelas dengan jumlah sampel yang memadai. Pendekatan ini menunjukkan potensi untuk implementasi dalam analisis protein secara otomatis.

## Referensi
1. Dataset: UCI Machine Learning Repository - Ecoli Dataset
2. Horton, P., & Nakai, K. (1996). A probabilistic classification system for predicting the cellular localization sites of proteins. Intelligent Systems in Molecular Biology, 4, 109-115.
