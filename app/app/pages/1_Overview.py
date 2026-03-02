import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

from risk_engine import (
    calculate_risk,
    behavioral_anomaly,
    mitre_mapping
)

st.title("🔴 SOC Live Threat Intelligence")

model = joblib.load("../models/model.pkl")
top_features = joblib.load("../models/top_features.pkl")
encoders = joblib.load("../models/encoders.pkl")

uploaded = st.sidebar.file_uploader("Upload NSL-KDD Dataset")

if uploaded:

    df = pd.read_csv(uploaded, header=None)

    # ---------- timestamps ----------
    df["timestamp"] = pd.date_range(
        start="2026-01-01",
        periods=len(df),
        freq="S"
    )

    df_model = df[top_features]

    preds = model.predict(df_model)
    probs = model.predict_proba(df_model)[:,1]

    risk_df = calculate_risk(preds, probs)
    df = pd.concat([df, risk_df], axis=1)

    # ---------- behavioral anomaly ----------
    df["BehaviorAnomaly"] = behavioral_anomaly(df_model)

    # ---------- MITRE mapping ----------
    df["MITRE_Tactic"] = df["Severity"].apply(mitre_mapping)

    # ================= KPI =================
    st.markdown("## 🚨 SOC Overview")

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Packets", len(df))
    col2.metric("Attacks", int((df.Prediction==1).sum()))
    col3.metric("Anomalies", int(df.BehaviorAnomaly.sum()))
    col4.metric("Avg Risk", round(df.RiskScore.mean(),2))

    # ================= TIMELINE =================
    st.markdown("## ⏱ Attack Timeline")

    timeline = df.groupby("timestamp")["RiskScore"].mean().reset_index()

    fig = px.line(
        timeline,
        x="timestamp",
        y="RiskScore",
        title="Threat Evolution Over Time"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ================= MITRE VIEW =================
    st.markdown("## 🎯 MITRE ATT&CK Mapping")

    mitre_counts = df["MITRE_Tactic"].value_counts()

    st.bar_chart(mitre_counts)

    # ================= SESSION EXPLORER =================
    st.markdown("## 🔎 Threat Session Explorer")

    selected = st.selectbox(
        "Select Packet Session",
        df.index
    )

    st.json(df.loc[selected].to_dict())

    # ================= CAMPAIGN CLUSTERS =================
    st.markdown("## 🧠 Threat Campaign Discovery")

    cluster_fig = px.scatter(
        df.sample(1500),
        x="RiskScore",
        y="BehaviorAnomaly",
        color="Severity",
        title="Behavioral Threat Clusters"
    )

    st.plotly_chart(cluster_fig, use_container_width=True)

else:
    st.info("Upload dataset to activate SOC intelligence.")