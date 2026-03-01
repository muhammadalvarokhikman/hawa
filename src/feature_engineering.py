import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def prepare_features():
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)
    
    # 1. Load Data
    df = pd.read_sql("SELECT * FROM weather_forecast_data ORDER BY created_at ASC", engine)
    df['created_at'] = pd.to_datetime(df['created_at'])

    # 2. Extract Time Features
    df['hour'] = df['created_at'].dt.hour
    df['day_of_week'] = df['created_at'].dt.dayofweek
    df['month'] = df['created_at'].dt.month

    # 3. Create Lag Features (Suhu jam-jam sebelumnya)
    # Penting: Model akan belajar dari apa yang terjadi di masa lalu
    df['temp_lag_1'] = df['temperature'].shift(1)
    df['temp_lag_2'] = df['temperature'].shift(2)
    df['hum_lag_1'] = df['humidity'].shift(1)

    # 4. Drop baris pertama yang menjadi NaN karena proses shifting/lag
    df = df.dropna(subset=['temp_lag_1', 'temp_lag_2'])

    print(f"✅ Feature Engineering Selesai. Dataset siap dengan {df.shape[1]} kolom.")
    return df

if __name__ == "__main__":
    data_final = prepare_features()
    print(data_final[['created_at', 'temperature', 'temp_lag_1', 'hour']].head())