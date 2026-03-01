import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def check_health():
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)
    
    # Ambil semua data dari database
    df = pd.read_sql("SELECT * FROM weather_forecast_data", engine)
    
    print("=== Laporan Kesehatan Data Hawa ===")
    print(f"Total Baris: {len(df)}")
    
    # 1. Cek Missing Values (Data yang Kosong)
    print("\n🔍 Mengecek Data Kosong (NA):")
    print(df.isnull().sum())
    
    # 2. Statistik Deskriptif (Sangat penting untuk orang Statistika!)
    print("\n📊 Ringkasan Statistik:")
    print(df[['temperature', 'humidity', 'pressure', 'wind_speed']].describe())

if __name__ == "__main__":
    check_health()