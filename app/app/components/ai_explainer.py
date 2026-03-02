import numpy as np

def generate_ai_explanation(df):

    attack_ratio = (df["Prediction"]==1).mean()*100
    avg_risk = df["RiskScore"].mean()

    if avg_risk < 30:
        level = "LOW"
        message = "Network traffic appears stable with minimal anomaly patterns."
    elif avg_risk < 60:
        level = "ELEVATED"
        message = "Suspicious traffic patterns detected requiring monitoring."
    elif avg_risk < 85:
        level = "HIGH"
        message = "Multiple attack signatures detected across sessions."
    else:
        level = "CRITICAL"
        message = "Active attack behavior detected. Immediate mitigation required."

    explanation = f"""
    ### 🤖 AI Security Assessment

    • Attack Traffic Ratio: **{attack_ratio:.2f}%**
    • Average Risk Score: **{avg_risk:.2f}**
    • Threat Level: **{level}**

    **AI Insight:**
    {message}

    Recommended SOC Action:
    - Inspect abnormal sessions
    - Apply firewall filtering
    - Monitor affected hosts
    """

    return explanation