import os
import joblib
import sys

# Memastikan root project masuk ke path agar bisa import src
sys.path.append(os.getcwd())
from src.retrain import retrain_process

def run_integration_test():
    print("=== HAWA SYSTEM INTEGRATION TEST ===")
    
    # 1. Uji Proses Pelatihan
    try:
        retrain_process()
        print("Status: retrain_process executed successfully.")
    except Exception as e:
        print(f"Failure: retrain_process failed with error: {e}")
        return

    # 2. Verifikasi Eksistensi Artifact
    model_path = 'models/hawa_v1.pkl'
    if not os.path.exists(model_path):
        print("Failure: models/hawa_v1.pkl was not created.")
        return
    print("Status: model file exists.")

    # 3. Verifikasi Struktur Artifact
    try:
        artifacts = joblib.load(model_path)
        if isinstance(artifacts, dict) and 'model' in artifacts and 'rmse' in artifacts:
            print("Status: Dictionary structure verified.")
            print(f"Metadata: RMSE {artifacts['rmse']}")
            print("TEST RESULT: PASSED")
        else:
            print("Failure: Artifact structure is invalid (expected dict with model and rmse).")
    except Exception as e:
        print(f"Failure: Could not load artifact: {e}")

if __name__ == "__main__":
    run_integration_test()