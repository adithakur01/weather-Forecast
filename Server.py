from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd, joblib, os, yaml, numpy as np
from datetime import datetime, timedelta

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/forecast_data")
async def get_forecast():
    try:
        cfg = yaml.safe_load(open("config.yaml"))
        city = cfg['data_settings']['target_city']
    
        feat_path = os.path.join(cfg['paths']['processed_data_dir'], f"{city}_final_features.csv")
        state_df = pd.read_csv(feat_path)
        state = state_df.tail(1).iloc[-1].to_dict()

        models = {m: joblib.load(os.path.join(cfg['paths']['model_dir'], f"{m}_full.pkl")) 
                  for m in ['temp', 'humidity', 'windspeed', 'pressure']}
        
        forecast = []
        for i in range(7):
            t = datetime.now() + timedelta(days=i)
            
            vec = pd.DataFrame([{
                'temp_lag_1': float(state['temp']),
                'temp_lag_24': float(state['temp'] + np.random.normal(0, 0.4)),
                'temp_std_6h': float(state.get('temp_std_6h', 0.5)), # Syncing with Math Logic
                'temp_diff_1h': float(state.get('temp_diff_1h', 0.1)), # Syncing with Math Logic
                'pressure_temp_ratio': float(state.get('pressure', 1010) / (state['temp'] + 273.15)),
                'sin_hour': np.sin(2 * np.pi * t.hour/23),
                'cos_hour': np.cos(2 * np.pi * t.hour/23),
                'humidity_lag_1': float(state.get('humidity', 50)),
                'windspeed_lag_1': float(state.get('windspeed', 10)),
                'is_daylight': 1 if (6 <= t.hour <= 18) else 0
            }])

            cols_order = ['temp_lag_1', 'temp_lag_24', 'temp_std_6h', 'temp_diff_1h', 'pressure_temp_ratio', 'sin_hour', 'cos_hour', 'humidity_lag_1', 'windspeed_lag_1', 'is_daylight']
            X_scaled = models['temp']['scaler'].transform(vec[cols_order]) # Using any scaler for order
            
            preds = {}
            for m in ['temp', 'humidity', 'windspeed', 'pressure']:
                X_input = models[m]['scaler'].transform(vec[cols_order])
                preds[m] = float(models[m]['model'].predict(X_input)[0])
            
            forecast.append({
                "day_name": t.strftime('%A'),
                "date": t.strftime('%d %b'),
                "temp": round(preds['temp'], 1),
                "humidity": int(np.clip(preds['humidity'], 0, 100)),
                "wind": round(abs(preds['windspeed']), 1),
                "pressure": round(preds['pressure'], 1),
                "condition": "Clear" if preds['humidity'] < 65 else "Cloudy",
                "sunrise": "06:40", "sunset": "18:45",
                "hourly": [{"time": f"{h}:00", "t": round(preds['temp'] + np.sin(h/4)*4, 1)} for h in range(0, 24, 3)]
            })
            
            state.update(preds)
            
        return {"forecast": forecast}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def home(): return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)