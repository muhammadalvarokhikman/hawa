import joblib
import pandas as pd
import xgboost as xgb
from sqlalchemy import create_engine
from sklearn.metrics import root_mean_squared_error
from feature_engineering import prepare_features
import os
from dotenv import load_dotenv

load_dotenv()

def retrain_process():
    print("🔄 Memulai proses Retraining Model...")
    
    # 1. Ambil data terbaru (termasuk 18rb data historis + data baru GA)
    df = prepare_features()
    
    features = ['hour', 'day_of_week', 'month', 'temp_lag_1', 'temp_lag_2', 'hum_lag_1', 'humidity', 'pressure', 'wind_speed']
    target = 'temperature'
    
    X = df[features]
    y = df[target]

    # 2. Split Data (Tetap gunakan kronologis 80/20)
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    # 3. Latih Ulang Model
    model = xgb.XGBRegressor(n_estimators=1000, learning_rate=0.05, max_depth=5)
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    # 4. Validasi Performa
    preds = model.predict(X_test)
    new_rmse = root_mean_squared_error(y_test, preds)
    print(f"📉 New RMSE: {new_rmse:.4f}")

    # 5. Simpan Model Baru (Menimpa versi lama)
    joblib.dump(model, 'models/hawa_v1.pkl')
    print("✅ Model hawa_v1.pkl berhasil diperbarui dengan data terbaru!")

if __name__ == "__main__":
    retrain_process()