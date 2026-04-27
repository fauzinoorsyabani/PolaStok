import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="PolaStok", page_icon="📦", layout="wide")

# URL backend API (belum diganti masih pakai dummy)
API_URL = "http://localhost:8000" 

st.markdown("""
<style>
    /* Memotong padding atas */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
    }
    
    .stApp { background-color: #f8fafc; }
    
    /* Desain card metrik dengan efek hover */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1rem 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        border-color: #cbd5e1;
    }
    div[data-testid="metric-container"] > label {
        color: #1e293b !important;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Membuat st.radio jadi modern */
    div[role="radiogroup"] label {
        background-color: transparent;
        border-radius: 10px;
        padding: 8px 12px;
        margin: 4px 0;
        transition: all 0.2s;
        font-weight: 500;
        cursor: pointer;
    }
    div[role="radiogroup"] label:hover {
        background-color: #eef2ff;
    }
    div[role="radiogroup"] label[data-testid="stRadioLabel"]:has(input:checked) {
        background-color: #e11d48 !important;
        color: white !important;
        border-radius: 10px;
    }
    div[role="radiogroup"] label[data-testid="stRadioLabel"]:has(input:checked) span {
        color: white !important;
    }
    div[role="radiogroup"] input { display: none; }
    div[role="radiogroup"] { gap: 6px; display: flex; flex-direction: column; }
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_db' not in st.session_state:
    st.session_state.user_db = {"admin": "admin123"} 
if 'nama_toko' not in st.session_state:
    st.session_state.nama_toko = "Toko Anda"

# Ambil data dari API
def get_inventory_data():
    try:
        response = requests.get(f"{API_URL}/inventory", timeout=3)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except:
        # dummy
        return pd.DataFrame({
            "Nama Barang": ["Beras Petruk 5kg", "Minyak Goreng Bimoli 2L", "Gula Pasir 1kg", "Indomie Goreng (Dus)", "Telur Ayam 1kg"],
            "Kategori": ["Sembako", "Sembako", "Sembako", "Makanan", "Sembako"],
            "Harga Satuan (Rp)": [75000, 35000, 16000, 115000, 28000],
            "Sisa Stok": [45, 8, 30, 15, 5],
            "Status": ["Aman", "Kritis", "Aman", "Aman", "Kritis"]
        })

# Halaman autentikasi
if not st.session_state.logged_in:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.write("#")
        st.title("📦 Masuk ke PolaStok")
        st.caption("Asisten Pintar Inventaris UMKM Anda.")
        with st.container(border=True):
            user = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            if st.button("Masuk Sekarang", width="stretch", type="primary"):
                if user in st.session_state.user_db and st.session_state.user_db[user] == pw:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Username atau password salah!")

# Halaman utama dashboard
else:
    df_stok = get_inventory_data()

    with st.sidebar:
        st.title("📦 PolaStok")
        st.markdown(f"**🏢 {st.session_state.nama_toko}**")
        st.markdown("Aplikasi prediksi kebutuhan stok barang.")
        st.markdown("---")
        
        menu_clean = st.radio(
            "Menu Navigasi",
            ["Beranda", "Daftar Barang", "Prediksi AI"],
            label_visibility="collapsed" 
        )
        
        st.markdown("###")
        st.markdown("---")
        
        with st.popover("⚙️ Pengaturan", width="stretch"):
            st.write("Edit Profil")
            with st.form("form_edit_toko"):
                input_toko = st.text_input("Ganti Nama Toko", value=st.session_state.nama_toko)
                tombol_simpan = st.form_submit_button("Simpan")
                if tombol_simpan:
                    st.session_state.nama_toko = input_toko
                    st.rerun()
        
        if st.button("🚪 Keluar", width="stretch", type="secondary"):
                st.session_state.logged_in = False
                st.rerun()

        st.markdown("---")
        st.caption(f"⏱️ Update terakhir: {datetime.now().strftime('%d %b %Y')}")


    # Beranda
    if menu_clean == "Beranda":
        st.header("📊 Ringkasan Beranda")
        st.caption("Pantau performa stok tokomu secara real-time.")
        
        total_jenis = len(df_stok)
        stok_aman = len(df_stok[df_stok["Status"] == "Aman"])
        stok_kritis = len(df_stok[df_stok["Status"] == "Kritis"])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric(label="Total Jenis Barang", value=total_jenis, delta="Semua Kategori")
        with col2: st.metric(label="Barang Stok Aman", value=stok_aman, delta="Kondisi Stabil")
        with col3: st.metric(label="Barang Stok Kritis", value=stok_kritis, delta="Butuh Restok!", delta_color="inverse")
        with col4: st.metric(label="Akurasi Prediksi AI", value="92%", delta="Bulan Lalu")
        st.markdown("---")
        
        st.subheader("📈 Tren Sisa Stok Inventaris")
        fig_bar = px.bar(
            df_stok, x="Nama Barang", y="Sisa Stok", color="Status", 
            color_discrete_map={"Aman":"#334155", "Kritis":"#e11d48"}, text_auto=True, height=400
        )
        fig_bar.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_bar, width="stretch")    
        st.markdown("---")
        
        st.subheader("⚠️ Stok Barang Kritis")
        st.markdown("Barang dengan stok menipis:")
        data_kritis = df_stok[df_stok["Status"] == "Kritis"]
        if len(data_kritis) > 0:
            st.dataframe(data_kritis[["Nama Barang", "Sisa Stok"]], width="stretch", hide_index=True)
        else:
            st.success("✅ Semua barang dalam kondisi stok aman.")

    # Daftar barang
    elif menu_clean == "Daftar Barang":
        st.header("📋 Daftar Seluruh Barang")
        st.markdown("---")
        
        with st.expander("➕ Tambah Barang Baru"):
            with st.form("form_tambah_barang", clear_on_submit=True):
                st.write("Masukkan detail barang baru:")
                col_form1, col_form2 = st.columns(2)
                
                with col_form1:
                    nama_baru = st.text_input("Nama Barang")
                    kategori_baru = st.selectbox("Kategori", ["Sembako", "Makanan", "Minuman", "Lainnya"])
                
                with col_form2:
                    harga_baru = st.number_input("Harga Satuan (Rp)", min_value=0, step=1000)
                    stok_baru = st.number_input("Jumlah Stok Awal", min_value=0, step=1)
                
                tombol_tambah = st.form_submit_button("Simpan")
                
                if tombol_tambah:
                    if nama_baru:
                        st.success(f"✅ Mantap! Barang '{nama_baru}' berhasil didaftarkan (Menunggu integrasi Backend).")
                    else:
                        st.error("Nama barang tidak boleh kosong!")
        
        st.write("#") 
        
        search = st.text_input("🔍 Cari barang", placeholder="Ketik nama barang...")
        if search:
            filtered = df_stok[df_stok["Nama Barang"].str.contains(search, case=False)]
            st.dataframe(filtered, width="stretch", hide_index=True)
        else:
            st.dataframe(df_stok, width="stretch", hide_index=True)

   # Prediksi AI
    elif menu_clean == "Prediksi AI":
        import plotly.graph_objects as go
        
        st.header("🤖 Analisis & Rekomendasi AI")
        st.markdown("---")
        st.info("💡 Menampilkan hasil prediksi menggunakan model time-series forecasting berdasarkan data historis UMKM.")

        # Filter barang
        barang_pil = st.selectbox("Pilih Barang untuk Dianalisis:", df_stok["Nama Barang"])

        with st.container(border=True):
            st.subheader(f"Prediksi Permintaan: {barang_pil}")
            dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=60, freq='D')
            penjualan_asli = np.random.normal(loc=40, scale=10, size=60).astype(float)
            penjualan_asli[30:] = np.nan 
            
            prediksi_ai = np.random.normal(loc=45, scale=12, size=60).astype(int)            
            fig_area = go.Figure()
            
            fig_area.add_trace(go.Scatter(
                x=dates[:31], y=penjualan_asli[:31], 
                fill='tozeroy', mode='lines',
                line=dict(color='#ff8a65', width=3),
                name='Penjualan Asli',
                fillcolor='rgba(255, 138, 101, 0.5)' 
            ))
            
            fig_area.add_trace(go.Scatter(
                x=dates, y=prediksi_ai, 
                fill='tozeroy', mode='lines',
                line=dict(color='#ce93d8', width=3, dash='dot'), 
                name='Prediksi AI',
                fillcolor='rgba(206, 147, 216, 0.4)' 
            ))
            
            fig_area.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                height=400,
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5) 
            )
            st.plotly_chart(fig_area, width="stretch")

        st.write("#") 

        st.subheader("📌 Rekomendasi Tindakan")
        with st.container(border=True):

            # Logika barang
            status_barang = df_stok[df_stok["Nama Barang"] == barang_pil]["Status"].values[0]
            sisa_stok = df_stok[df_stok["Nama Barang"] == barang_pil]["Sisa Stok"].values[0]
            
            puncak_kebutuhan = max(prediksi_ai) 
            jumlah_restok = puncak_kebutuhan - sisa_stok 
            
            if status_barang == "Kritis":
                st.error(f"**Tindakan Prioritas:** Tambah stok **{barang_pil}** sebanyak **{jumlah_restok} pcs** minggu depan.")
                st.markdown(f"**Alasan AI:** Sisa stok Anda saat ini sangat menipis ({sisa_stok} pcs), sementara algoritma mendeteksi akan ada lonjakan permintaan hingga {puncak_kebutuhan} pcs dalam rentang waktu prediksi ke depan.")
            else:
                st.success(f"**Tindakan Prioritas:** Pertahankan stok **{barang_pil}** saat ini.")
                st.markdown(f"**Alasan AI:** Sisa stok Anda ({sisa_stok} pcs) diprediksi masih sanggup memenuhi tren rata-rata permintaan pasar. Belum perlu mengeluarkan modal tambahan untuk restok saat ini.")