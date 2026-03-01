import requests
import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_weather():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = os.getenv("CITY_NAME")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"]
        }
    except Exception as e:
        print(f"Gagal mengambil data API: {e}")
        return None

def save_to_supabase(data):
    try:
        # Koneksi ke PostgreSQL Supabase
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()

        # Query SQL untuk memasukkan data
        query = """
        INSERT INTO weather_forecast_data 
        (city_name, temperature, humidity, pressure, wind_speed, weather_description)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        
        cur.execute(query, (
            data['city'], data['temp'], data['humidity'], 
            data['pressure'], data['wind_speed'], data['description']
        ))
        
        conn.commit()
        print("Data berhasil disimpan ke Supabase Cloud!")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Gagal menyimpan ke database: {e}")

if __name__ == "__main__":
    print("Collect data from OpenWeather API...")
    weather_info = get_weather()
    
    if weather_info:
        save_to_supabase(weather_info)