import joblib
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def get_next_hour_forecast():
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)
    
    df = pd.read_sql("SELECT * FROM weather_forecast_data ORDER BY created_at DESC LIMIT 2", engine)
    df = df.sort_values('created_at')
    
    latest_time = pd.to_datetime(df['created_at'].iloc[-1])
    next_hour_time = latest_time + pd.Timedelta(hours=1)
    
    input_data = pd.DataFrame([{
        'hour': next_hour_time.hour,
        'day_of_week': next_hour_time.dayofweek,
        'month': next_hour_time.month,
        'temp_lag_1': df['temperature'].iloc[-1],
        'temp_lag_2': df['temperature'].iloc[0],
        'hum_lag_1': df['humidity'].iloc[-1],
        'humidity': df['humidity'].iloc[-1],
        'pressure': df['pressure'].iloc[-1],
        'wind_speed': df['wind_speed'].iloc[-1]
    }])
    
    artifacts = joblib.load('models/hawa_v1.pkl')
    
    if isinstance(artifacts, dict):
        model = artifacts['model']
        rmse = artifacts.get('rmse', 0.59)
    else:
        model = artifacts
        rmse = 0.59

    prediction = model.predict(input_data)[0]
    return round(float(prediction), 2), next_hour_time, rmse