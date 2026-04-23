from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

BASE_DIR = Path(__file__).resolve().parent.parent

model_path = BASE_DIR / 'artifacts' / 'isolation_forest_final_final.pkl'
scaler_path = BASE_DIR / 'artifacts' / 'scaler.pkl'
# Load models once at startup
iso_model = joblib.load(model_path)
scaler    = joblib.load(scaler_path)

def predict_dcrm(df: pd.DataFrame) -> dict:
    # Encode categoricals
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = LabelEncoder().fit_transform(df[col].astype(str))

    
    # Select numeric
    df.columns = df.columns.astype(str)
    df = df.select_dtypes(include=[np.number])
    
    # Scale
    df.columns = df.columns.map(str)

    expected_cols = scaler.feature_names_in_

    missing = set(expected_cols) - set(df.columns)
    extra = set(df.columns) - set(expected_cols)

    print("Missing:", missing)
    print("Extra:", extra)

    df = df.reindex(columns=expected_cols, fill_value=0)
    df_scaled = scaler.transform(df)
    
    # Predict
    predictions = iso_model.predict(df_scaled)
    scores      = iso_model.decision_function(df_scaled)

    
    anomaly_pct = (predictions == -1).sum() / len(predictions) * 100
    avg_score   = float(scores.mean())

    # DEBUG - print these first!
    print(f"Anomaly %   : {anomaly_pct:.2f}%")
    print(f"Avg score   : {avg_score:.4f}")
    print(f"Min score   : {scores.min():.4f}")
    print(f"Max score   : {scores.max():.4f}")
    print(f"Predictions : {np.unique(predictions, return_counts=True)}")
    # 
    # Health status
    if anomaly_pct > 80:
        status   = 'FAULTY'
        severity = 'Critical'
    elif anomaly_pct > 50:
        status   = 'DEGRADING'
        severity = 'Moderate'
    else:
        status   = 'HEALTHY'
        severity = 'Low'
    
    
    return {
        'scores mean'          : scores.mean(),
        'status'          : status,
        'severity'        : severity,
        'anomaly_score'   : avg_score,
        'anomaly_percent' : anomaly_pct
    }