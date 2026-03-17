import pandas as pd
import yaml, os, numpy as np

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(base_dir, "config.yaml")

config = yaml.safe_load(open(config_path))
city = config['data_settings']['target_city']
raw_csv = os.path.join(base_dir, config['paths']['raw_data_dir'], f"{city}_master_raw.csv")

if not os.path.exists(raw_csv):
    print(f"Error: Target file not found at {raw_csv}")
    exit(1)

df = pd.read_csv(raw_csv)
df['datetime'] = pd.to_datetime(df['datetime'])

df = df.drop_duplicates(subset=['datetime']).sort_values('datetime')
df = df.set_index('datetime').reindex(pd.date_range(df['datetime'].min(), df['datetime'].max(), freq='h')).rename_axis('datetime').reset_index()

df = df.set_index('datetime')
targets = ['temp', 'humidity', 'windspeed', 'pressure']
df[targets] = df[targets].interpolate(method='time', limit=6).ffill().bfill()

out_dir = os.path.join(base_dir, config['paths']['processed_data_dir'])
os.makedirs(out_dir, exist_ok=True)
df.reset_index().to_csv(os.path.join(out_dir, f"{city}_weather_clean.csv"), index=False)
print("Transformation Successfully Completed")