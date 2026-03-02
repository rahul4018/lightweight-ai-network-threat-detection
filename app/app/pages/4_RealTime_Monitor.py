import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

from stream_engine import stream_packets, inject_noise
from risk_engine import calculate_risk

st.title("📡 Real-Time Threat Monitor")

model = joblib.load("../models/model.pkl")
top_features = joblib.load("../models/top_features.pkl")

uploaded = st.sidebar.file_uploader("Upload Dataset")

if uploaded:

    df = pd.read_csv(uploaded, header=None)

    df = inject_noise(df)

    chart = st.empty()
    metrics = st.empty()

    risk_history = []

    for batch in stream_packets(df):

        X = batch[top_features]

        preds = model.predict(X)
        probs = model.predict_proba(X)[:,1]

        risk_df = calculate_risk(preds, probs)

        avg_risk = risk_df["RiskScore"].mean()
        risk_history.append(avg_risk)

        metrics.metric("Live Risk Score", round(avg_risk,2))

        plot_df = pd.DataFrame({
            "step": range(len(risk_history)),
            "risk": risk_history
        })

        fig = px.line(plot_df, x="step", y="risk",
                      title="Live Network Risk")

        chart.plotly_chart(fig, use_container_width=True)