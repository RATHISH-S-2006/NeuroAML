🧠 NeuroAML
Real-Time Anti–Money Laundering Intelligence & Operations Platform

NeuroAML is an end-to-end, real-time Anti–Money Laundering (AML) system that combines behavioral analytics, transaction network intelligence, temporal risk analysis, and operational case management into a single, unified platform.
Unlike traditional rule-based AML systems, NeuroAML provides dynamic risk evolution, fraud typology reasoning, early risk forecasting, and regulator-ready SAR report generation, making it suitable for financial institutions, regulators, and compliance teams.

🚀 Key Highlights

🔍 Real-time risk monitoring with continuous risk evolution

🧠 Fraud typology reasoning (Smurfing, Layering, Mule Networks)

🔮 Risk forecasting engine (early warning before escalation)

🧾 Case management system with full audit trail

📊 Global case dashboard for operational oversight

📤 SAR (Suspicious Activity Report) export

🎬 Demo Mode for accelerated live demonstrations

🧩 Modular architecture (clean, scalable, maintainable)

🏗️ System Architecture (High Level)
Data Ingestion
      ↓
Behavioral Analysis
      ↓
Transaction Network Intelligence
      ↓
Temporal Risk Evolution
      ↓
Hybrid Risk Engine
      ↓
Fraud Typology Classification
      ↓
Risk Forecasting (Early Warning)
      ↓
Case Management & Audit Trail
      ↓
SAR Report Generation


Each layer is independent, modular, and explainable, mirroring real-world AML platforms used in banks and financial regulators.

🧩 Project Structure
NeuroAML/
│
├── dashboard.py                # Main Streamlit UI & orchestration
├── phase4.py                   # Compliance, impact metrics & demo mode
│
├── intelligence/               # Intelligence & reasoning engines
│   ├── typology_engine.py      # Fraud typology classification
│   └── risk_forecast.py        # Risk forecasting engine
│
├── governance/                 # AML operations layer
│   ├── case_management.py      # Case lifecycle & audit trail
│   └── sar_export.py           # SAR report generation
│
├── render.yaml                 # Cloud deployment config
├── requirements.txt
└── README.md

🧠 Core Features Explained
🔍 Dynamic Risk Monitoring

Each account has a continuously evolving risk score

Risk levels automatically transition: LOW → MEDIUM → HIGH

Behavior accumulates over time (not static scoring)

🧠 Fraud Typology Reasoning

NeuroAML doesn’t just flag risk — it explains what kind of financial crime is likely occurring:

💸 Smurfing

🕸️ Layering

🧍‍♂️ Mule Networks

🚨 High-risk anomalous behavior

Each typology includes a human-readable justification.

🔮 Risk Forecasting (Early Warning)

Predicts future risk 3–5 cycles ahead

Flags accounts likely to escalate soon

Enables proactive compliance action

🧾 Case Management & Audit Trail

Automatically creates AML cases for suspicious accounts

Tracks case status:

🟡 Open

🕵️ Under Review

🚨 Escalated

✅ Closed

Maintains a full audit trail of analyst actions

📊 Global Case Dashboard

Centralized view of all AML cases

Real-time case statistics

Drill-down into individual cases and audit logs

📤 SAR Report Export

One-click generation of Suspicious Activity Reports

Structured, regulator-style JSON output

Includes:

Evidence

Typologies

Risk forecast

Compliance mapping

Recommended actions

🎬 Demo Mode

Accelerates time-based risk evolution

Allows full fraud escalation during live demos

Logic remains unchanged — only time is compressed

This is critical for hackathons and live evaluations.

🛠️ Tech Stack

Frontend: Streamlit

Backend API: FastAPI (separate service)

Data Processing: Python, Pandas

Graph Intelligence: NetworkX

Visualization: Matplotlib

Deployment: Render / Streamlit Cloud

Version Control: Git & GitHub

▶️ How to Run Locally
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Start backend API (if applicable)
uvicorn main:app --reload

3️⃣ Run the dashboard
streamlit run dashboard.py

🎤 Demo Flow (Recommended for Judges)

Open Monitoring Mode → observe live risk evolution

Enable Demo Mode → watch rapid escalation

Switch to Investigation Mode → inspect:

Evidence

Fraud typology

Risk forecast

Open a case → escalate → view audit trail

Generate and download SAR report

Open Global Case Dashboard → show scalability

🏆 Why NeuroAML Stands Out

Not a static dashboard — a living AML system

Combines intelligence + operations

Mirrors real-world regulatory workflows

Designed with scalability and explainability in mind

Built using industry-style modular architecture

📌 Future Enhancements

PDF SAR export (regulator format)

Role-based analyst access

Cross-border transaction intelligence

Advanced fraud simulations

ML-based risk calibration

👤 Author

Rathish
Computer Science Engineering
NeuroAML — SIH Project
