import joblib
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def get_next_hour_forecast():
    # 1. Hubungkan ke database
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)
    
    # 2. Ambil 2 baris terakhir (untuk kebutuhan lag_1 dan lag_2)
    df = pd.read_sql("SELECT * FROM weather_forecast_data ORDER BY created_at DESC LIMIT 2", engine)
    df = df.sort_values('created_at') # Urutkan agar lag benar
    
    # 3. Feature Engineering untuk data baru
    latest_time = pd.to_datetime(df['created_at'].iloc[-1])
    next_hour_time = latest_time + pd.Timedelta(hours=1)
    
    # Menyiapkan fitur input model
    input_data = pd.DataFrame([{
        'hour': next_hour_time.hour,
        'day_of_week': next_hour_time.dayofweek,
        'month': next_hour_time.month,
        'temp_lag_1': df['temperature'].iloc[-1],
        'temp_lag_2': df['temperature'].iloc[0],
        'hum_lag_1': df['humidity'].iloc[-1],
        'humidity': df['humidity'].iloc[-1], # Asumsi sementara sama dengan jam lalu
        'pressure': df['pressure'].iloc[-1],
        'wind_speed': df['wind_speed'].iloc[-1]
    }])
    
    # 4. Load Model dan Prediksi
    model = joblib.load('models/hawa_v1.pkl')
    prediction = model.predict(input_data)[0]
    
    return round(float(prediction), 2), next_hour_time