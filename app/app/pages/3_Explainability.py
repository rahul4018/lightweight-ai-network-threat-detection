import streamlit as st

st.title("🧠 Explainable AI Insights")

st.image("../models/shap_summary.png")

st.markdown("""
### How AI Makes Decisions

The model evaluates:
- Traffic byte behavior
- Connection patterns
- Error rates
- Service anomalies

SHAP values show global feature influence.
""")