# PolaStok (Smart Enterprise Data & Inventory Analytics)

## Deskripsi Singkat
PolaStok adalah platform digital berbasis Machine Learning (time-series forecasting) yang dirancang secara efektif untuk memprediksi permintaan barang di masa depan bagi UMKM. Proyek ini bertujuan untuk menurunkan angka stockout (kekurangan barang) sekaligus memotong biaya penyimpanan inventaris berlebih pada usaha kecil secara presisi berbasis data.

## Hasil Kerja & Fitur Utama (Minimum Viable Product)
1. **Modul Prediksi AI:** Memproses data historis menggunakan model time-series forecasting untuk menghasilkan rekomendasi restock 1-3 bulan ke depan.
2. **Dashboard Inventaris (Frontend):** Antarmuka visual berbasis Streamlit yang menampilkan status stok, grafik tren, serta peringatan dini untuk barang yang mendekati batas minimum.
3. **Manajemen Data Terpusat (Backend):** Sistem RESTful API menggunakan FastAPI yang mengelola pencatatan barang dan menjembatani hasil inferensi AI ke antarmuka pengguna.

## Struktur Direktori
Pembangunan sistem PolaStok dibagi menjadi beberapa komponen utama:

```text
PolaStok/
├── data/           # Dataset (Kaggle) dan data hasil preprocessing
│   ├── raw/
│   └── processed/
├── docs/           # Dokumentasi proyek teknis (Workflow, Project Plan)
├── src/            # Kode sumber utama aplikasi
│   ├── frontend/   # Dashboard Frontend menggunakan Streamlit
│   ├── backend/    # RESTful API menggunakan FastAPI
│   └── ml/         # Script pengembangan model AI, Jupyter notebooks, model (.pkl)
└── tests/          # Unit tests dan automation tests
```

## Prasyarat Lingkungan Pengembangan
Pastikan perangkat lunak berikut telah terinstal pada komputer:
- Python 3.9 atau versi lebih baru
- Git
- pip (Python package installer)

## Cara Menjalankan Proyek secara Lokal

Proses ini membutuhkan eksekusi dua komponen: Backend Server dan Frontend UI secara bersamaan.

### 1. Menjalankan Backend API (FastAPI)
1. Buka terminal dan masuk ke direktori utama proyek (`PolaStok`).
2. Disarankan menggunakan virtual environment:
   - Buat virtual environment: `python -m venv venv`
   - Aktifkan di Windows: `.\venv\Scripts\activate`
3. Instal library yang dibutuhkan:
   `pip install fastapi uvicorn pydantic`
4. Jalankan server FastAPI:
   `uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000`
5. Pastikan muncul pesan sukses dan server berjalan di `http://localhost:8000`.

### 2. Menjalankan Frontend Dashboard (Streamlit)
1. Buka terminal baru.
2. Pastikan virtual environment dalam keadaan aktif (sama seperti langkah Backend).
3. Instal library frontend jika belum ada:
   `pip install streamlit pandas plotly requests`
4. Jalankan Streamlit:
   `streamlit run src.frontend.app`
5. Browser akan otomatis membuka dashboard aplikasi di alamat `http://localhost:8501`.

## Anggota Tim
- [APC313D6Y0155] - Fauzi Noorsyabani (Project Management)
- [APC154D6X0062] - Agni Fatya Kholila (Frontend)
- [APC313D6Y0078] - Septian Samdani (Machine Learning)
- [APC313D6Y0022] - Rizky Maulana Harahap (Machine Learning)
- [APC313D6Y0319] - Muhamad Fadli Sirojudin (Backend/Database)
