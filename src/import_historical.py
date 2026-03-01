import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Gunakan huruf kecil sesuai saran terminal kamu sebelumnya
from meteostat import Point, hourly, stations 

load_dotenv()

def import_to_supabase():
    # 1. Koordinat Semarang - Dibungkus dalam objek Point
    lat, lon = -6.9667, 110.4167
    poi = Point(lat, lon) # Meteostat butuh objek ini agar punya atribut .latitude
    
    # 2. Cari Stasiun Terdekat
    print("📍 Mencari stasiun cuaca terdekat...")
    # PENTING: Gunakan 'poi' (objek), jangan 'lat' (angka)
    st_search = stations.nearby(poi) 
    
    # Ambil data stasiun
    if hasattr(st_search, 'fetch'):
        station_data = st_search.fetch(1)
    else:
        station_data = st_search.head(1)

    if station_data.empty:
        print("❌ Tidak ditemukan stasiun cuaca di sekitar Semarang.")
        return
    
    station_id = station_data.index[0]
    station_name = station_data['name'].values[0]
    print(f"✅ Menggunakan Stasiun: {station_name} (ID: {station_id})")

    # 3. Ambil Data Historis
    start = datetime(2024, 1, 1)
    end = datetime.now()
    
    print(f"🔄 Menarik data per jam dari {start} hingga {end}...")
    
    # Gunakan fungsi 'hourly' (huruf kecil)
    data_query = hourly(station_id, start, end)
    df = data_query.fetch()

    if df is None or df.empty:
        print("⚠️ Data tidak ditemukan. Cek rentang waktu atau koneksi.")
        return

    # 4. Transformasi Data
    df = df.reset_index()
    # Pastikan kolom sesuai: time, temp, rhum, pres, wspd
    df_clean = df[['time', 'temp', 'rhum', 'pres', 'wspd']].copy()
    df_clean.columns = ['created_at', 'temperature', 'humidity', 'pressure', 'wind_speed']
    df_clean['city_name'] = 'Semarang'
    df_clean['weather_description'] = 'historical'

    # 5. Kirim ke Supabase
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)
    
    print(f"🚀 Mengirim {len(df_clean)} baris data ke Supabase...")
    try:
        df_clean.to_sql('weather_forecast_data', engine, if_exists='append', index=False, chunksize=1000)
        print("🎉 Selesai! Data historis berhasil masuk ke database.")
    except Exception as e:
        print(f"❌ Error saat upload: {e}")

if __name__ == "__main__":
    import_to_supabase()