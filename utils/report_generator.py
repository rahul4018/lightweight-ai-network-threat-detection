from datetime import datetime

def generate_report(stats):

    risk = stats["risk"]
    attacks = stats["attacks"]

    if risk > 70:
        severity = "CRITICAL"
        action = "Immediate containment recommended."
    elif risk > 40:
        severity = "HIGH"
        action = "Investigate suspicious activity."
    else:
        severity = "LOW"
        action = "Monitor traffic."

    report = f"""
AI NETWORK INCIDENT REPORT
==========================

Generated: {datetime.now()}

Threat Severity: {severity}
Total Attacks Detected: {attacks}
Average Risk Score: {risk}

Recommended Action:
{action}

System Assessment:
AI detected abnormal behavioral patterns consistent with cyber intrusion attempts.
"""

    return report