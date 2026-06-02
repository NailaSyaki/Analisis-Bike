![Dashboard VeloStats](/assets/Dashboard.png)

# 🚲 VeloStats: Bike Sharing Data Analysis Dashboard

<br>

## 📌 Deskripsi Proyek

<br>Proyek ini merupakan bagian dari tugas analisis data yang berfokus pada eksplorasi pola penyewaan sepeda pada sistem Capital Bikeshare di Washington D.C. Dashboard ini menganalisis bagaimana faktor lingkungan (cuaca, suhu, musim) dan variabel waktu memengaruhi perilaku pengguna, baik pengguna Casual maupun Registered.

## 📊 Pertanyaan Bisnis

1. Dampak Kondisi Lingkungan: Bagaimana pengaruh cuaca ekstrem dan perubahan musim terhadap total jumlah penyewaan sepeda?
2. Perilaku Pengguna: Apakah terdapat perbedaan pola penyewaan antara pengguna Casual dan Registered pada hari kerja (working day) dibandingkan dengan hari libur?

## ⚙️ Fitur Utama

<br>Exploratory Data Analysis (EDA): Pembersihan data, pengolahan tipe data, dan pemetaan kategori.

- Visualisasi Interaktif: Menggunakan Plotly Express untuk melihat hubungan suhu vs penyewaan serta perbandingan musim.
- Analisis Lanjutan: Implementasi Manual Clustering (Binning) untuk mengelompokkan kategori permintaan (Low, Medium, High Demand).
- Dashboard Streamlit: Antarmuka modern dengan tema gelap untuk navigasi data yang mudah.

## 📂 Struktur Dataset

<br>Dataset terdiri dari dua file utama:

- day.csv: Agregasi data penyewaan berdasarkan harian.
- hour.csv: Agregasi data penyewaan berdasarkan jam.

### Variabel Kunci:

- cnt: Total penyewaan (target).
- temp & atemp: Suhu dan suhu yang dirasakan.
- weathersit: Kondisi cuaca (Cerah, Mendung, Hujan/Salju).
- workingday: Indikator hari kerja atau hari libur.

## 🚀 Cara Menjalankan

1. Pastikan Python sudah terinstal.
2. Instal library yang dibutuhkan:
   <br>pip install pandas matplotlib seaborn plotly streamlit statsmodels
3. Jalankan aplikasi:
   <br>streamlit run dashboard.py

## 📈 Conclusion & Insights

Berdasarkan analisis yang telah dilakukan melalui dashboard VeloStats, berikut adalah beberapa temuan kunci:
<br>1. Pengaruh Faktor Cuaca & Musim

- Suhu adalah Driver Utama: Terdapat korelasi positif yang kuat antara suhu dan jumlah penyewaan. Semakin hangat suhu (hingga titik tertentu), semakin tinggi minat masyarakat untuk bersepeda.
- Musim Gugur (Fall) & Panas (Summer): Kedua musim ini merupakan periode puncak (peak season) dengan rata-rata penyewaan tertinggi. Sebaliknya, musim dingin (Winter) mengalami penurunan drastis karena faktor cuaca ekstrem.
- Kondisi Cuaca: Pengguna sangat sensitif terhadap cuaca. Penyewaan turun lebih dari 50% saat kondisi cuaca berubah dari "Cerah/Berawan" ke "Hujan/Salju Ringan".

<br><br>2. Strategi Berdasarkan Perilaku Pengguna

- Komuter vs Wisatawan: Pengguna Registered menunjukkan pola stabil di hari kerja (diduga untuk transportasi kerja), sedangkan pengguna Casual mengalami lonjakan signifikan (hingga 2-3x lipat) pada akhir pekan dan hari libur.
- Peluang Konversi: Hari libur di musim panas adalah waktu terbaik untuk melakukan kampanye pemasaran keanggotaan, karena pada saat itulah volume pengguna casual berada pada titik tertinggi.

<br><br>3. Rekomendasi Bisnis

- Manajemen Armada: Melakukan pemeliharaan besar-besaran pada musim dingin agar seluruh armada siap tempur di musim semi dan panas.
- Stok Dinamis: Menambah jumlah ketersediaan sepeda di stasiun-stasiun area rekreasi pada akhir pekan untuk mengakomodasi lonjakan pengguna casual.
  ![Informasi](/assets/Insight.png)

## 📚 Sumber Dataset

Dataset ini diperoleh dari UCI Machine Learning Repository. Penggunaan data ini dalam publikasi wajib mencantumkan sitasi berikut:
<br>Fanaee-T, Hadi, and Gama, Joao, "Event labeling combining ensemble detectors and background knowledge", Progress in Artificial Intelligence (2013): pp. 1-15, Springer Berlin Heidelberg, doi:10.1007/s13748-013-0040-3.
