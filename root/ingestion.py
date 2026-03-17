import yaml, requests, os, pandas as pd
from datetime import datetime, timedelta

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg1 = yaml.safe_load(open(os.path.join(base_dir, "config1.yaml")))
cfg = yaml.safe_load(open(os.path.join(base_dir, "config.yaml")))

end_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=2190)).strftime('%Y-%m-%d') 

raw_dir = os.path.join(base_dir, cfg['paths']['raw_data_dir'])
os.makedirs(raw_dir, exist_ok=True)

params = {
    "latitude": 26.9124, "longitude": 75.7873,
    "start_date": start_date,
    "end_date": end_date,
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure",
    "daily": "sunrise,sunset", "timezone": "auto"
}

print(f"Fetching Fresh Data: {start_date} to {end_date}")
res = requests.get("https://archive-api.open-meteo.com/v1/archive", params=params)

if res.status_code == 200:
    data = res.json()
    h_df = pd.DataFrame(data['hourly']).rename(columns={
        "time": "datetime", "temperature_2m": "temp", "relative_humidity_2m": "humidity",
        "wind_speed_10m": "windspeed", "surface_pressure": "pressure"
    })
    d_df = pd.DataFrame(data['daily']).rename(columns={"time": "date"})
    h_df['date'] = pd.to_datetime(h_df['datetime']).dt.date.astype(str)
    
    master = pd.merge(h_df, d_df, on='date', how='left').drop(columns=['date'])
    master.to_csv(os.path.join(raw_dir, f"{cfg1['data_settings']['target_city']}_master_raw.csv"), index=False)
    print(f"✅ Downloaded {len(master)} fresh rows.")