import pandas as pd
import xgboost as xgb
from sklearn.metrics import root_mean_squared_error
import joblib
from feature_engineering import prepare_features # Import fungsi yang sudah kamu buat

def train_hawa_model():
    # 1. Ambil data yang sudah diproses fiturnya
    df = prepare_features()
    
    # 2. Tentukan fitur (X) dan target (y)
    features = ['hour', 'day_of_week', 'month', 'temp_lag_1', 'temp_lag_2', 'hum_lag_1', 'humidity', 'pressure', 'wind_speed']
    target = 'temperature'
    
    X = df[features]
    y = df[target]

    # 3. Split Data secara kronologis (80% Train, 20% Test)
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    print(f"📊 Training dengan {len(X_train)} baris data...")

    # 4. Inisialisasi Model XGBoost
    # Sebagai orang statistik, kamu bisa tuning hyperparameter ini nanti
    model = xgb.XGBRegressor(
        n_estimators=1000,
        learning_rate=0.05,
        max_depth=5,
        early_stopping_rounds=50,
        eval_metric="rmse"
    )

    # 5. Training
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=100
    )

    # 6. Evaluasi dengan RMSE
    predictions = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, predictions)
    print(f"\n✅ Model Selesai Dilatih!")
    print(f"📉 Nilai RMSE: {rmse:.4f} derajat Celcius")

    # 7. Simpan Model untuk Deployment
    joblib.dump(model, 'models/hawa_v1.pkl')
    print("💾 Model disimpan di 'models/hawa_v1.pkl'")

if __name__ == "__main__":
    train_hawa_model()