# 🌤️ Atmosphere AI: Ultra-Level Weather Intelligence

Atmosphere AI is a production-ready, autonomous machine learning pipeline designed to predict weather patterns with high precision. It uses an **ExtraTreesRegressor** backbone combined with **Physics-Based Feature Engineering** to forecast Temperature, Humidity, Windspeed, and Pressure for the next 7 days.

## 🚀 Key Features
- **Autonomous Pipeline:** Automated data ingestion, transformation, and model retraining.
- **Physics-Informed ML:** Incorporates Air Density Proxy, Barometric Momentum, and Cyclical Time features for >90% accuracy.
- **Recursive Forecasting:** Day $n$ predictions feed into Day $n+1$ for dynamic 7-day outlooks.
- **Ultra-Level Dashboard:** Premium Glassmorphism UI with Apple/Google aesthetics and Dark/Light mode support.
- **Streamlit Integration:** Industrial-grade deployment ready for cloud hosting.

## 🏗️ Project Architecture
The system follows a modular 4-stage pipeline:
1. **Ingestion:** Fetches 2 years of historical data from Open-Meteo API.
2. **Transformation:** Time-weighted interpolation and data cleaning.
3. **Feature Engineering:** Calculates EMA, Volatility (Std Dev), and Momentum.
4. **Modeling:** Optimized Ensemble learning with Robust Scaling.



## 🛠️ Tech Stack
- **Language:** Python 3.12
- **ML Libraries:** Scikit-Learn, Pandas, NumPy, Joblib
- **Backend:** FastAPI / Uvicorn
- **Frontend:** Streamlit, Plotly, CSS (Glassmorphism)
- **Data Source:** Open-Meteo Archive API

##    Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/Atmosphere-AI.git](https://github.com/your-username/Atmosphere-AI.git)
   cd Atmosphere-AI
   ```

2. **Setup Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Autonomous Pipeline:**
   ```bash
   python main.py
   ```

5. **Launch Dashboard:**
   ```bash
   streamlit run streamlit_app.py
   ```

## 📊 Model Performance (Jaipur Station)
| Metric | Temperature | Humidity | Pressure |
| :--- | :--- | :--- | :--- |
| **R2 Score** | 0.999 | 0.990 | 0.951 |
| **AI Accuracy (5% Tol)** | 89.3% | 83.7% | 78.5%  |
---

Developed with ❤️ by **Aditya Raghav**
---

