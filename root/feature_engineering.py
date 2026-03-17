import pandas as pd
import numpy as np
import yaml
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = yaml.safe_load(open(os.path.join(base_dir, "config.yaml")))
city = config['data_settings']['target_city']
clean_csv = os.path.join(base_dir, config['paths']['processed_data_dir'], f"{city}_weather_clean.csv")

df = pd.read_csv(clean_csv)
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.set_index('datetime')

for col in ['temp', 'humidity', 'windspeed', 'pressure']:
    df[f'{col}_lag_1'] = df[col].shift(1)
    df[f'{col}_lag_24'] = df[col].shift(24)
    df[f'{col}_diff_1h'] = df[col].diff()
    df[f'{col}_std_6h'] = df[col].rolling(6).std()

df['pressure_temp_ratio'] = df['pressure'] / (df['temp'] + 273.15)
df['hour'] = df.index.hour
df['sin_hour'] = np.sin(2 * np.pi * df['hour']/23)
df['cos_hour'] = np.cos(2 * np.pi * df['hour']/23)

df['is_daylight'] = ((df['hour'] >= 6) & (df['hour'] <= 18)).astype(int)
final_path = os.path.join(base_dir, config['paths']['processed_data_dir'], f"{city}_final_features.csv")
df.dropna().reset_index().to_csv(final_path, index=False)

print(f"Features created Successfully..")