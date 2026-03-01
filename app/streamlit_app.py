import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from src.predict import get_next_hour_forecast # Import fungsi prediksi kamu
import sys
sys.path.append(os.getcwd())

# Load environment variables
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
        query = "SELECT * FROM weather_forecast_data ORDER BY created_at DESC LIMIT 100"
        df = pd.read_sql(query, conn)
        conn.close()
        
        df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_convert('Asia/Jakarta')
        return df
    except Exception as e:
        st.error(f"Gagal terhubung ke database: {e}")
        return None

# --- TAMPILAN DASHBOARD ---
st.title("☁️ Proyek Hawa: Semarang Real-time Weather")
st.markdown("Dashboard ini memantau cuaca Semarang secara otomatis menggunakan **GitHub Actions**, **Supabase**, dan model **XGBoost**.")

data = get_data()

if data is not None and not data.empty:
    # 1. Baris Pertama: Metrik Saat Ini (Aktual)
    latest = data.iloc[0]
    current_temp = latest['temperature']
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Suhu saat ini", f"{current_temp} °C")
    col2.metric("Kelembapan", f"{latest['humidity']}%")
    col3.metric("Tekanan", f"{latest['pressure']} hPa")
    col4.metric("Kecepatan Angin", f"{latest['wind_speed']} m/s")

    st.divider()

    # 2. BARIS BARU: Prediksi Masa Depan (Forecasting)
    st.subheader("🔮 Ramalan Hawa (1 Jam ke Depan)")
    try:
        pred_temp, pred_time = get_next_hour_forecast()
        
        # Hitung selisih untuk indikator delta
        diff = round(pred_temp - current_temp, 2)
        
        p_col1, p_col2 = st.columns([1, 3])
        with p_col1:
            st.metric(
                label=f"Estimasi Suhu ({pred_time.strftime('%H:%M')} WIB)", 
                value=f"{pred_temp} °C",
                delta=f"{diff} °C",
                delta_color="normal" # Merah jika naik, biru jika turun
            )
        with p_col2:
            st.info(f"💡 **Info Model**: Prediksi ini dihasilkan oleh model **XGBoost v1** dengan tingkat galat (RMSE) sebesar **0.59°C**. Model belajar dari 18.000+ data historis Semarang.")
    except Exception as e:
        st.warning(f"Sistem prediksi sedang disiapkan atau terjadi error: {e}")

    st.divider()

    # 3. Baris Ketiga: Visualisasi Tren Masa Lalu
    st.subheader("📈 Tren Suhu di Semarang (WIB)")
    chart_data = data.set_index('created_at')[['temperature']].sort_index()
    st.line_chart(chart_data)

    # 4. Baris Keempat: Tabel Data Mentah
    with st.expander("Lihat Data Mentah (Historical Logs)"):
        st.dataframe(data, use_container_width=True)
else:
    st.warning("Belum ada data di database.")

st.sidebar.info(f"📍 Lokasi: {os.getenv('CITY_NAME', 'Semarang')}")
st.sidebar.caption("Project by: Muhammad Alvaro Khikman")