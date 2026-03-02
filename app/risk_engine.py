import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


# -----------------------------
# Risk Score Calculation
# -----------------------------
def calculate_risk(predictions, probabilities):

    risk_score = probabilities * 100

    severity = []
    for r in risk_score:
        if r < 30:
            severity.append("LOW")
        elif r < 60:
            severity.append("MEDIUM")
        elif r < 85:
            severity.append("HIGH")
        else:
            severity.append("CRITICAL")

    return pd.DataFrame({
        "Prediction": predictions,
        "RiskScore": risk_score,
        "Severity": severity
    })


# -----------------------------
# Behavioral Anomaly Detection
# -----------------------------
def behavioral_anomaly(df_features):

    iso = IsolationForest(
        contamination=0.08,
        random_state=42
    )

    anomaly = iso.fit_predict(df_features)

    # -1 anomaly → 1
    anomaly = np.where(anomaly == -1, 1, 0)

    return anomaly


# -----------------------------
# MITRE ATT&CK Mapping
# -----------------------------
def mitre_mapping(severity):

    if severity == "CRITICAL":
        return "TA0001 - Initial Access"
    elif severity == "HIGH":
        return "TA0005 - Defense Evasion"
    elif severity == "MEDIUM":
        return "TA0007 - Discovery"
    else:
        return "Normal Activity"