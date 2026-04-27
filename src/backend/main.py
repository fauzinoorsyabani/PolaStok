from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="PolaStok API",
    description="Backend untuk proyek Capstone PolaStok (Market Insight & Inventory Prediction)",
    version="0.2.0"
)

# CORS agar Streamlit frontend bisa mengakses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---

class StatusResponse(BaseModel):
    status: str
    message: str

class TambahBarangRequest(BaseModel):
    """Schema untuk request body POST /inventory dari Frontend Agni."""
    nama_baru: str
    kategori_baru: str
    harga_baru: int
    stok_baru: int

# --- Mock Database (Data Sementara di Memori) ---
# Ini akan diganti dengan koneksi database SQL sungguhan nanti.

BATAS_STOK_KRITIS = 10

inventory_db: list[dict] = [
    {"nama": "Beras Petruk 5kg",        "kategori": "Sembako", "harga": 75000,  "stok": 45},
    {"nama": "Minyak Goreng Bimoli 2L",  "kategori": "Sembako", "harga": 35000,  "stok": 8},
    {"nama": "Gula Pasir 1kg",           "kategori": "Sembako", "harga": 16000,  "stok": 30},
    {"nama": "Indomie Goreng (Dus)",     "kategori": "Makanan", "harga": 115000, "stok": 15},
    {"nama": "Telur Ayam 1kg",           "kategori": "Sembako", "harga": 28000,  "stok": 5},
]


def _format_for_frontend(item: dict) -> dict:
    """Mengubah format internal ke format JSON yang diminta Frontend (Agni).
    Keys harus PERSIS sama huruf besar/kecilnya agar pandas tidak error.
    """
    status = "Kritis" if item["stok"] <= BATAS_STOK_KRITIS else "Aman"
    return {
        "Nama Barang": item["nama"],
        "Kategori": item["kategori"],
        "Harga Satuan (Rp)": item["harga"],
        "Sisa Stok": item["stok"],
        "Status": status,
    }


# --- Endpoints ---

@app.get("/", response_model=StatusResponse)
async def root():
    return {
        "status": "success",
        "message": "Backend FastAPI PolaStok berhasil berjalan! AI Module siap diintegrasikan."
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/inventory")
async def get_inventory():
    """Endpoint GET /inventory — Mengembalikan seluruh data inventaris.
    Format JSON keys disesuaikan dengan kebutuhan Frontend (pandas DataFrame).
    Status 'Kritis' otomatis diberikan jika stok <= BATAS_STOK_KRITIS (default: 10).
    """
    return [_format_for_frontend(item) for item in inventory_db]


@app.post("/inventory")
async def add_inventory(data: TambahBarangRequest):
    """Endpoint POST /inventory — Menambahkan barang baru ke inventaris.
    Menerima data dari form 'Tambah Barang Baru' di Streamlit.
    """
    if not data.nama_baru.strip():
        raise HTTPException(status_code=400, detail="Nama barang tidak boleh kosong.")

    new_item = {
        "nama": data.nama_baru.strip(),
        "kategori": data.kategori_baru,
        "harga": data.harga_baru,
        "stok": data.stok_baru,
    }
    inventory_db.append(new_item)

    return {
        "status": "success",
        "message": f"Barang '{data.nama_baru}' berhasil ditambahkan ke inventaris.",
        "data": _format_for_frontend(new_item),
    }
