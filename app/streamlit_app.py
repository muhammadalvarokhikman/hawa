import streamlit as st
import pandas as pd
import psycopg2
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.getcwd())
from src.predict import get_next_hour_forecast

load_dotenv()

st.set_page_config(
    page_title="Hawa - Semarang Weather Dashboard",
    page_icon="☁️",
    layout="wide"
)

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
        st.error(f"Database Connection Error: {e}")
        return None

st.title("Proyek Hawa: Semarang Real-time Weather")
st.markdown("Automated Weather Monitoring System via GitHub Actions, Supabase, and XGBoost.")

data = get_data()

if data is not None and not data.empty:
    latest = data.iloc[0]
    current_temp = latest['temperature']
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Suhu Saat Ini", f"{current_temp} °C")
    col2.metric("Kelembapan", f"{latest['humidity']}%")
    col3.metric("Tekanan", f"{latest['pressure']} hPa")
    col4.metric("Kecepatan Angin", f"{latest['wind_speed']} m/s")

    st.divider()

    st.subheader("Prediksi 1 Jam Ke Depan")
    try:
        pred_temp, pred_time, current_rmse, last_train_time = get_next_hour_forecast()
        diff = round(pred_temp - current_temp, 2)
        
        p_col1, p_col2 = st.columns([1, 3])
        with p_col1:
            st.metric(
                label=f"Estimasi ({pred_time.strftime('%H:%M')} WIB)", 
                value=f"{pred_temp} °C",
                delta=f"{diff} °C"
            )
        with p_col2:
            st.info(f"Model: XGBoost v1.0 | Akurasi: RMSE {current_rmse}°C. Model ini mempelajari pola cuaca lokal Semarang untuk memberikan estimasi suhu jam berikutnya.")
            
        # Model Health di Sidebar
        st.sidebar.markdown("---")
        st.sidebar.subheader("🛠️ Model Health")
        st.sidebar.write(f"**Current RMSE:** {current_rmse} °C")
        st.sidebar.write(f"**Last Retrained:** {last_train_time}")
            
    except Exception as e:
        st.warning(f"Inference error: {e}")

    st.divider()

    st.subheader("Tren Suhu Semarang (WIB)")
    chart_data = data.set_index('created_at')[['temperature']].sort_index()
    st.line_chart(chart_data)

    with st.expander("Historical Logs"):
        st.dataframe(data, use_container_width=True)
else:
    st.warning("No data available in the database.")

st.sidebar.info(f"Location: {os.getenv('CITY_NAME', 'Semarang')}")
st.sidebar.caption("Project by: Muhammad Alvaro Khikman")