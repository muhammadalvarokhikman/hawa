import joblib
import xgboost as xgb
from sklearn.metrics import root_mean_squared_error
from feature_engineering import prepare_features
import os

def retrain_process():
    print("Memulai proses retraining harian...")
    df = prepare_features()
    
    features = ['hour', 'day_of_week', 'month', 'temp_lag_1', 'temp_lag_2', 'hum_lag_1', 'humidity', 'pressure', 'wind_speed']
    target = 'temperature'
    
    X = df[features]
    y = df[target]

    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    model = xgb.XGBRegressor(n_estimators=1000, learning_rate=0.05, max_depth=5)
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    preds = model.predict(X_test)
    new_rmse = root_mean_squared_error(y_test, preds)
    
    model_artifacts = {
        'model': model,
        'rmse': round(float(new_rmse), 4)
    }

    joblib.dump(model_artifacts, 'models/hawa_v1.pkl')
    print(f"Retrain selesai. RMSE Baru: {new_rmse:.4f}")

if __name__ == "__main__":
    retrain_process()