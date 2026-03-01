# HAWA: Semarang Real-Time Weather Forecasting (MLOps)

HAWA (Hawa Semarang) adalah sistem pemantauan dan prediksi suhu udara real-time untuk wilayah Semarang. Proyek ini mengintegrasikan prinsip Statistika dengan siklus hidup Machine Learning (MLOps) yang sepenuhnya otomatis.

## Fitur Utama

- **Automated Ingestion**: Pengambilan data cuaca setiap jam via OpenWeather/Meteostat menggunakan GitHub Actions.
- **Relational Data Store**: Penyimpanan data terstruktur menggunakan Supabase (PostgreSQL).
- **Automated Retraining**: Model melakukan self-learning setiap minggu untuk mengatasi *data drift* dan menjaga akurasi.
- **Dynamic Dashboard**: Visualisasi real-time dan prediksi 1 jam ke depan menggunakan Streamlit Cloud.

## Tech Stack

- **Language**: Python 3.12
- **Model**: XGBoost Regressor
- **Database**: Supabase (PostgreSQL)
- **CI/CD & Automation**: GitHub Actions
- **Deployment**: Streamlit Cloud

## Analisis Statistik

Model dievaluasi menggunakan metrik **Root Mean Squared Error (RMSE)** untuk mengukur deviasi antara suhu prediksi dan aktual:

$$
RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}
$$

Saat ini, model beroperasi dengan **RMSE ~0.58°C**, yang menunjukkan presisi tinggi untuk data deret waktu lokal.

## Struktur Proyek

- `app/`: Frontend dashboard Streamlit.
- `src/`: Logika utama untuk feature engineering, pelatihan, dan prediksi.
- `models/`: Artifact model tersimpan (.pkl).
- `.github/workflows/`: Konfigurasi otomatisasi GitHub Actions.
- `tests/`: Skrip pengujian integrasi sistem.

---

**Developed by Muhammad Alvaro Khikman**
*Statistics Student at Universitas Muhammadiyah Semarang*
