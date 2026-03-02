import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# =====================================
# CONFIG
# =====================================
st.set_page_config(
    page_title="AI Network Security Platform",
    layout="wide"
)

# Backend URL (LOCAL + CLOUD SAFE)
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000/batch_predict"
)

# =====================================
# HEADER
# =====================================
st.title("🛡 Lightweight Explainable AI for Real-Time Network Threat Detection")
st.markdown("### Enterprise AI Network Security Intelligence Platform")

# Sidebar
mode = st.sidebar.radio(
    "Detection Mode",
    ["Batch Analysis", "Real-Time Monitoring"]
)

uploaded_file = st.sidebar.file_uploader(
    "Upload NSL-KDD File (.txt or .csv)"
)

# =====================================
# BACKEND HEALTH CHECK
# =====================================
def check_backend():
    try:
        r = requests.get(BACKEND_URL.replace("/batch_predict", "/"), timeout=3)
        return r.status_code == 200
    except:
        return False


# =====================================
# BACKEND CALL
# =====================================
def call_backend(df):

    payload = {
        "data": df.values.tolist()
    }

    try:
        response = requests.post(
            BACKEND_URL,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        data = response.json()

        if "results" not in data:
            st.error("Backend returned invalid response.")
            st.stop()

        return data["results"]

    except requests.exceptions.RequestException as e:
        st.error(f"Backend API Error: {e}")
        st.stop()


# =====================================
# MAIN PIPELINE
# =====================================
if uploaded_file:

    if not check_backend():
        st.error("🚨 Backend API is not running.")
        st.stop()

    df = pd.read_csv(uploaded_file, header=None)

    # synthetic timestamp for visualization
    df["timestamp"] = pd.date_range(
        start="2026-01-01",
        periods=len(df),
        freq="s"
    ).astype(str)

    with st.spinner("🧠 AI analyzing network traffic..."):

        results = call_backend(df.drop(columns=["timestamp"]))

    result_df = pd.DataFrame(results)

    df_final = pd.concat(
        [df.reset_index(drop=True), result_df],
        axis=1
    )

    # =====================================
    # SAFE COLUMN HANDLING
    # =====================================
    defaults = {
        "behavior_anomaly": 0,
        "severity": "UNKNOWN",
        "mitre_tactic": "N/A",
        "risk_score": 0,
        "prediction": 0
    }

    for col, val in defaults.items():
        if col not in df_final.columns:
            df_final[col] = val

    # =====================================
    # KPI CALCULATIONS
    # =====================================
    total = len(df_final)
    attacks = int((df_final["prediction"] == 1).sum())
    anomalies = int((df_final["behavior_anomaly"] == 1).sum())
    avg_risk = float(df_final["risk_score"].mean())

    # =====================================
    # SOC OVERVIEW
    # =====================================
    st.markdown("## 🚨 SOC Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Packets", total)
    c2.metric("Attacks", attacks)
    c3.metric("Anomalies", anomalies)
    c4.metric("Avg Risk", round(avg_risk, 2))

    # =====================================
    # RISK GAUGE
    # =====================================
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_risk,
        title={'text': "System Risk Level"},
        gauge={
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, 30], 'color': 'green'},
                {'range': [30, 60], 'color': 'yellow'},
                {'range': [60, 85], 'color': 'orange'},
                {'range': [85, 100], 'color': 'red'}
            ]
        }
    ))

    st.plotly_chart(gauge, width="stretch")

    # =====================================
    # TIMELINE
    # =====================================
    st.markdown("## ⏱ Threat Timeline")

    timeline = df_final.groupby("timestamp")["risk_score"].mean().reset_index()

    fig_time = px.line(
        timeline,
        x="timestamp",
        y="risk_score",
        title="Threat Evolution Over Time"
    )

    st.plotly_chart(fig_time, width="stretch")

    # =====================================
    # SEVERITY DISTRIBUTION
    # =====================================
    st.markdown("## ⚠ Severity Distribution")

    sev_df = df_final["severity"].value_counts().reset_index()
    sev_df.columns = ["severity", "count"]

    fig = px.bar(
        sev_df,
        x="severity",
        y="count",
        color="severity"
    )

    st.plotly_chart(fig, width="stretch")

    # =====================================
    # MITRE ATT&CK VIEW
    # =====================================
    st.markdown("## 🎯 MITRE ATT&CK Mapping")

    st.bar_chart(df_final["mitre_tactic"].value_counts())

    # =====================================
    # SESSION EXPLORER
    # =====================================
    st.markdown("## 🔎 Analyst Session Explorer")

    selected = st.selectbox("Select Packet", df_final.index)

    st.json(df_final.loc[selected].to_dict())

    # =====================================
    # INCIDENT REPORT
    # =====================================
    st.markdown("## 📄 AI Incident Report")

    report = f"""
AI NETWORK INCIDENT REPORT
Generated: {datetime.now()}

Packets Analysed: {total}
Attacks Detected: {attacks}
Behavioral Anomalies: {anomalies}
Average Risk Score: {avg_risk:.2f}
"""

    st.download_button(
        "Download Incident Report",
        report,
        "incident_report.txt"
    )

    # =====================================
    # EXPORT CSV
    # =====================================
    csv = df_final.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Detection Report",
        csv,
        "ai_threat_report.csv",
        "text/csv"
    )

else:
    st.info("Upload dataset to activate enterprise threat intelligence dashboard.")