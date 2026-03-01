import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables untuk local testing
load_dotenv()

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Hawa - Semarang Weather Dashboard",
    page_icon="☁️",
    layout="wide"
)

# --- FUNGSI AMBIL DATA ---
def get_data():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT")
        )
        # Mengambil 100 data terbaru
        query = "SELECT * FROM weather_forecast_data ORDER BY created_at DESC LIMIT 100"
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Konversi waktu ke Asia/Jakarta (WIB)
        df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_convert('Asia/Jakarta')
        return df
    except Exception as e:
        st.error(f"Gagal terhubung ke database: {e}")
        return None

# --- TAMPILAN DASHBOARD ---
st.title("☁️ Proyek Hawa: Semarang Real-time Weather")
st.markdown("Dashboard ini memantau cuaca Semarang secara otomatis menggunakan **GitHub Actions** dan **Supabase**.")

data = get_data()

if data is not None and not data.empty:
    # Baris pertama: Ringkasan (Metrics)
    latest = data.iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Suhu saat ini", f"{latest['temperature']} °C")
    col2.metric("Kelembapan", f"{latest['humidity']}%")
    col3.metric("Tekanan", f"{latest['pressure']} hPa")
    col4.metric("Kecepatan Angin", f"{latest['wind_speed']} m/s")

    st.divider()

    # Baris kedua: Visualisasi Tren
    st.subheader("📈 Tren Suhu di Semarang (WIB)")
    # Menyiapkan data untuk chart
    chart_data = data.set_index('created_at')[['temperature']].sort_index()
    st.line_chart(chart_data)

    # Baris ketiga: Tabel Data Mentah
    with st.expander("Lihat Data Mentah (Historical Logs)"):
        st.dataframe(data, use_container_width=True)
else:
    st.warning("Belum ada data di database. Tunggu siklus otomatis jam berikutnya atau jalankan manual di GitHub Actions.")

st.sidebar.info(f"📍 Lokasi: {os.getenv('CITY_NAME', 'Semarang')}")
st.sidebar.caption("Project by: Muhammad Alvaro Khikman")