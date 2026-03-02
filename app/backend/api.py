from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
import os
from sklearn.ensemble import IsolationForest

app = FastAPI(
    title="AI Network Threat Detection API",
    version="2.0"
)

# ==========================================
# SAFE MODEL LOADING (RENDER COMPATIBLE)
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../models"))

model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
top_features = joblib.load(os.path.join(MODEL_DIR, "top_features.pkl"))
encoders = joblib.load(os.path.join(MODEL_DIR, "encoders.pkl"))

# ==========================================
# FULL DATASET SCHEMA
# ==========================================
columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
    "wrong_fragment","urgent","hot","num_failed_logins","logged_in",
    "num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count",
    "dst_host_srv_count","dst_host_same_srv_rate",
    "dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate",
    "dst_host_srv_rerror_rate","label","difficulty"
]

# ==========================================
# REQUEST MODEL
# ==========================================
class BatchPackets(BaseModel):
    data: list


# ==========================================
# HEALTH CHECK
# ==========================================
@app.get("/")
def health():
    return {"status": "API running successfully"}


# ==========================================
# HELPER FUNCTIONS
# ==========================================
def map_severity(score):
    if score < 30:
        return "LOW"
    elif score < 60:
        return "MEDIUM"
    elif score < 85:
        return "HIGH"
    else:
        return "CRITICAL"


def map_mitre(severity):
    if severity == "CRITICAL":
        return "TA0001 - Initial Access"
    elif severity == "HIGH":
        return "TA0005 - Defense Evasion"
    elif severity == "MEDIUM":
        return "TA0007 - Discovery"
    else:
        return "Normal Activity"


# ==========================================
# BATCH PREDICT
# ==========================================
@app.post("/batch_predict")
def batch_predict(packets: BatchPackets):

    try:
        # Rebuild dataframe
        df = pd.DataFrame(packets.data, columns=columns)

        # Convert label to binary
        df["label"] = df["label"].apply(
            lambda x: 0 if x == "normal" else 1
        )

        # Encode categorical columns
        for col in df.select_dtypes(include="object").columns:
            if col in encoders:
                df[col] = encoders[col].transform(df[col])

        # Select model features
        df_model = df[top_features]

        # ML Predictions
        preds = model.predict(df_model)
        probs = model.predict_proba(df_model)[:, 1]

        # Behavioral anomaly detection
        iso = IsolationForest(contamination=0.08, random_state=42)
        anomaly_flags = iso.fit_predict(df_model)
        anomaly_flags = np.where(anomaly_flags == -1, 1, 0)

        results = []

        for p, pr, an in zip(preds, probs, anomaly_flags):

            risk_score = float(pr * 100)
            severity = map_severity(risk_score)
            mitre = map_mitre(severity)

            results.append({
                "prediction": int(p),
                "risk_score": risk_score,
                "severity": severity,
                "behavior_anomaly": int(an),
                "mitre_tactic": mitre
            })

        return {"results": results}

    except Exception as e:
        return {"error": str(e)}