import streamlit as st
import plotly.express as px
import pandas as pd

st.title("📊 Threat Analytics")

uploaded = st.sidebar.file_uploader("Upload Report CSV")

if uploaded:

    df = pd.read_csv(uploaded)

    fig = px.histogram(df, x="RiskScore",
                       title="Risk Score Distribution")

    st.plotly_chart(fig, use_container_width=True)

    sev = df["Severity"].value_counts()

    st.bar_chart(sev)