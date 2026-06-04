# Lightweight Explainable AI for Network Threat Detection

> Real-time intrusion detection with risk scoring, MITRE ATT&CK mapping, SHAP explanations, and a SOC-style operations dashboard — running on CPU, no GPU required.

**[Live Dashboard](https://your-app.streamlit.app)** · [API Docs](https://your-backend.onrender.com/docs) · [Report a Bug](https://github.com/rahul4018/lightweight-ai-network-threat-detection/issues)

---

![SOC Dashboard](https://github.com/user-attachments/assets/22b925a7-c8b7-4c8a-ab3c-53bf2d5b5858)

---

## The problem

Enterprise networks generate traffic volumes no human team can monitor manually. Most ML-based IDS tools are black boxes — they fire an alert, give no reason, and analysts either ignore them or spend hours investigating. This project fixes both problems: lightweight enough to run on modest hardware, explainable enough for a SOC analyst to act on.

---

## What it does

- Classifies network traffic as normal or attack using a supervised ML model trained on NSL-KDD
- Assigns a **risk score (0–100)** and severity level — LOW / MEDIUM / HIGH / CRITICAL
- Maps threats to **MITRE ATT&CK tactics**
- Flags behavioral anomalies via **Isolation Forest** (unsupervised, label-independent)
- Explains every prediction with **SHAP feature importance**
- Surfaces everything in a **SOC-style Streamlit dashboard** with risk gauge, threat timeline, session explorer, and AI-generated incident reports

---

## Architecture

```
┌──────────────────────────────┐
│     Streamlit SOC Dashboard  │
│                              │
│  Risk Gauge · Timeline       │
│  Severity Analytics          │
│  Session Explorer · Reports  │
└──────────────┬───────────────┘
               │  REST API
               ▼
┌──────────────────────────────┐
│     FastAPI Prediction Engine │
└──────────────┬───────────────┘
               │
   ┌───────────┼────────────────┐
   ▼           ▼                ▼
ML Classifier  Isolation Forest  SHAP Explainer
(supervised)   (anomaly)         (interpretability)
   │
   ▼
Risk Scoring Engine → MITRE ATT&CK Mapper
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| Dashboard | Streamlit + Plotly |
| ML | scikit-learn (classifier + Isolation Forest) |
| Explainability | SHAP |
| Data | Pandas · NumPy |
| Dataset | NSL-KDD |
| Deployment | Render (API) + Streamlit Cloud (dashboard) |

---

## Quickstart

```bash
git clone https://github.com/rahul4018/lightweight-ai-network-threat-detection.git
cd lightweight-ai-network-threat-detection

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Start the API:**

```bash
cd app/backend
uvicorn api:app --reload
```

API docs → `http://localhost:8000/docs`

**Start the dashboard:**

```bash
cd app
streamlit run dashboard.py
```

Dashboard → `http://localhost:8501`

---

## ML Pipeline

```
Raw NSL-KDD traffic logs
        │
        ▼
Preprocessing + feature encoding
        │
        ▼
Feature selection (top N by importance)
        │
        ├──────────────────────────────┐
        ▼                              ▼
Supervised classifier            Isolation Forest
(attack type + severity)         (behavioral anomaly)
        │
        ▼
Risk scoring engine (0–100)
        │
        ▼
SHAP explainability layer
        │
        ▼
MITRE ATT&CK tactic mapping
        │
        ▼
REST API response → Dashboard
```

---

## API Reference

**Batch predict**

```
POST /batch_predict
```

Input: array of network session feature vectors

Response per session:

```json
{
  "prediction": "neptune",
  "risk_score": 87,
  "severity": "HIGH",
  "mitre_tactic": "Initial Access",
  "anomaly_flag": true,
  "top_features": [
    { "feature": "dst_bytes", "shap_value": 0.41 },
    { "feature": "duration",  "shap_value": 0.19 }
  ],
  "incident_summary": "High-confidence DoS pattern detected..."
}
```

---

## Project Structure

```
lightweight-ai-network-threat-detection/
├── app/
│   ├── backend/
│   │   └── api.py              # FastAPI entrypoint
│   ├── components/             # Dashboard UI components
│   ├── pages/                  # Streamlit multipage views
│   ├── dashboard.py            # Main dashboard
│   ├── risk_engine.py          # Risk scoring logic
│   └── stream_engine.py        # Simulated streaming mode
├── models/
│   ├── model.pkl               # Trained classifier
│   ├── encoders.pkl            # Label encoders
│   ├── top_features.pkl        # Selected feature list
│   └── shap_summary.png        # SHAP summary plot
├── data/
│   ├── KDDTrain+.txt
│   └── KDDTest+.txt
├── notebooks/
│   ├── train.py                # Model training script
│   └── explain.py              # SHAP analysis
├── utils/
│   ├── forecast.py
│   └── report_generator.py     # AI incident report generation
└── requirements.txt
```

---

## Deployment

**Backend on Render:**

```bash
uvicorn app.backend.api:app --host 0.0.0.0 --port $PORT
```

**Dashboard on Streamlit Cloud:**

Set main file to `app/dashboard.py`, then update the backend URL:

```python
BACKEND_URL = "https://your-backend.onrender.com/batch_predict"
```

---

## Dataset

**NSL-KDD** — an improved version of the KDD Cup '99 intrusion detection dataset, with duplicate records removed and a more balanced test set. Contains labeled network session records across four attack categories: DoS, Probe, R2L, U2R.

[Download NSL-KDD](https://www.unb.ca/cic/datasets/nsl.html)

---

## Roadmap

- [ ] Live packet capture via `scapy`
- [ ] Kafka-based streaming pipeline
- [ ] User authentication + RBAC
- [ ] Docker Compose for one-command deployment
- [ ] CI/CD pipeline
- [ ] Deep learning model comparison (LSTM for sequence-based detection)

---

## License

MIT — intended for research and educational use.
