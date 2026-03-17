import pandas as pd, numpy as np, yaml, os, joblib
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import r2_score, accuracy_score, f1_score

cfg = yaml.safe_load(open("config.yaml"))
city = cfg['data_settings']['target_city']
df = pd.read_csv(os.path.join(cfg['paths']['processed_data_dir'], f"{city}_final_features.csv"))

features = [
    'temp_lag_1', 'temp_lag_24', 'temp_std_6h', 'temp_diff_1h',
    'pressure_temp_ratio', 'sin_hour', 'cos_hour', 
    'humidity_lag_1', 'windspeed_lag_1', 'is_daylight'
]

os.makedirs(cfg['paths']['model_dir'], exist_ok=True)

for target in ['temp', 'humidity', 'windspeed', 'pressure']:
    print(f"\n--- Optimizing {target.upper()} Intelligence ---")
    
    X = df[features].astype(np.float32)
    y = df[target].astype(np.float32)
    split = int(len(df) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    scaler = RobustScaler()
    X_tr_sc = scaler.fit_transform(X_train)
    X_ts_sc = scaler.transform(X_test)
    model = ExtraTreesRegressor(
        n_estimators=200,
        max_depth=16, 
        min_samples_leaf=2,
        n_jobs=-1, 
        random_state=42
    )
    model.fit(X_tr_sc, y_train)
    preds = model.predict(X_ts_sc)
    y_bins = pd.cut(y_test, bins=10, labels=False) 
    p_bins = pd.cut(preds, bins=10, labels=False)
    
    print(f"R2_Score: {r2_score(y_test, preds):.4f}")
    print(f"ccuracy: {accuracy_score(y_bins, p_bins)*100:.2f}%")
    
    joblib.dump({"scaler": scaler, "model": model}, 
                os.path.join(cfg['paths']['model_dir'], f"{target}_full.pkl"), compress=3)

print("\nModels traine Successfully")