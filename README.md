#  Lightweight Explainable AI for Real-Time Network Threat Detection

> Production-style AI-powered cybersecurity platform for real-time intrusion detection, threat scoring, anomaly detection, and explainable AI insights.

---

##  Overview

Modern enterprise networks generate massive volumes of traffic data, making manual monitoring infeasible.

This project delivers a lightweight yet powerful AI-driven intrusion detection system that:

- Detects malicious traffic in real time
- Assigns risk scores (0–100)
- Classifies severity (LOW → CRITICAL)
- Maps threats to MITRE ATT&CK tactics
- Detects behavioral anomalies
- Explains predictions using SHAP
- Visualizes everything in a SOC-style dashboard

Built using the **NSL-KDD dataset** and a modular, production-style ML architecture.

---

##  Core Capabilities

###  Intelligent Threat Detection
- Supervised ML classifier for intrusion detection
- Risk score generation engine
- Severity classification:
  - LOW
  - MEDIUM
  - HIGH
  - CRITICAL

###  Real-Time Monitoring
- Batch prediction mode
- Simulated streaming mode
- REST API prediction pipeline via FastAPI

###  Explainable AI (XAI)
- SHAP-based interpretability
- Feature importance visualization
- Transparent decision-making layer

###  Behavioral Anomaly Detection
- Isolation Forest model
- Detects abnormal traffic patterns independent of labels

###  MITRE ATT&CK Mapping
Threat predictions mapped to tactical categories aligned with the MITRE ATT&CK framework.

###  SOC Dashboard
Enterprise-style monitoring interface built with Streamlit:

- Risk Gauge
- Threat Timeline
- Severity Analytics
- Session Explorer
- AI-Generated Incident Report

---

##  System Architecture

```
Streamlit Dashboard
        │
        │ REST API
        ▼
FastAPI Backend (Prediction Engine)
        │
        ▼
ML Model + Encoders + Anomaly Detector + XAI
```

This architecture simulates a lightweight Security Operations Center (SOC) pipeline.

---

##  Project Structure

```
lightweight-ai-network-threat-detection/

app/
 ├── backend/
 │    └── api.py
 ├── components/
 ├── pages/
 ├── dashboard.py
 ├── risk_engine.py
 └── stream_engine.py

models/
 ├── model.pkl
 ├── encoders.pkl
 ├── top_features.pkl
 └── shap_summary.png

data/
 ├── KDDTrain+.txt
 └── KDDTest+.txt

notebooks/
 ├── train.py
 └── explain.py

utils/
 ├── forecast.py
 └── report_generator.py

requirements.txt
```

---

##  Dataset

**Dataset Used:** NSL-KDD  
An improved version of the KDD’99 intrusion detection dataset containing labeled network traffic sessions.

Used for:
- Supervised classification
- Risk modeling
- Feature engineering
- Explainability experiments

---

##  Machine Learning Pipeline

1. Data preprocessing  
2. Feature encoding  
3. Feature selection  
4. Model training (Scikit-learn)  
5. Risk scoring engine  
6. Isolation Forest anomaly detection  
7. SHAP explainability layer  

---

##  Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI |
| Frontend | Streamlit |
| ML | Scikit-learn |
| Visualization | Plotly |
| Explainability | SHAP |
| Data Processing | Pandas, NumPy |
| Deployment | Render + Streamlit Cloud |

---

##  Installation (Local Setup)

### 1️ Clone Repository

```bash
git clone https://github.com/rahul4018/lightweight-ai-network-threat-detection.git
cd lightweight-ai-network-threat-detection
```

### 2️ Create Virtual Environment

**Windows (PowerShell)**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️ Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  Run Backend API

```bash
cd app/backend
uvicorn api:app --reload
```

API docs available at:

```
http://127.0.0.1:8000/docs
```

---

##  Run Dashboard

```bash
cd app
streamlit run dashboard.py
```

Open:

```
http://localhost:8501
```

---

##  Deployment

### Backend (Render)

Start command:

```bash
uvicorn app.backend.api:app --host 0.0.0.0 --port $PORT
```

### Dashboard (Streamlit Cloud)

Main file:

```
app/dashboard.py
```

Update backend URL:

```python
BACKEND_URL = "https://your-backend-url.onrender.com/batch_predict"
```

---

##  System Outputs

- Threat prediction
- Risk score (0–100)
- Severity classification
- MITRE ATT&CK tactic
- Behavioral anomaly flag
- AI-generated incident report

---

##  Use Cases

- Security Operations Centers (SOC)
- Network intrusion detection research
- Explainable AI demonstrations
- Cybersecurity analytics platforms
- Academic and thesis projects

---

##  Author

**Rahul**  
AI & Cybersecurity Enthusiast  

GitHub:  
https://github.com/rahul4018

---

##  License

This project is intended for research and educational purposes.

---

##  Future Enhancements

- Live packet capture integration
- Kafka-based streaming pipeline
- Deep learning threat models
- User authentication & RBAC
- Cloud-native monitoring
- Docker + CI/CD integration

---

#  Why This Project Stands Out

This project demonstrates:

- End-to-end ML system design
- Real-time API architecture
- Explainable AI integration
- Security domain application
- Production-style modular codebase
- SOC-level visualization design

It is structured to simulate a real-world cybersecurity AI platform rather than a simple ML notebook project.

---

If you want next-level polish, say:
