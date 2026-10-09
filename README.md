# 🛡️ FraudTwin — AI-Powered Transaction Risk Intelligence

**FraudTwin** is an enterprise-grade transaction risk intelligence and fraud investigation platform. It unites calibrated machine learning (XGBoost), contextual transaction heuristics, explainable AI (SHAP), what-if twin simulations, attack stress testing, and generative AI decision support (Gemini) into a unified risk management workspace.

---

## 🚀 Key Features

1. **🔐 Multi-Tenant Architecture & Complete User Isolation**
   - Built on a robust SQLite service layer (`data/fraudtwin.db`) with foreign-key constraints and WAL mode concurrency.
   - Cryptographic password protection using **PBKDF2-HMAC-SHA256** with per-user 16-byte random salts.
   - **Dedicated Dashboard for Every User**: Transactions, investigation cases, and analytics are strictly partitioned by `user_id`. Alice never sees Bob's cases.

2. **✨ Cinematic UI / UX & Dynamic Theming**
   - High-fidelity dark and light themes, custom SVG radar artwork, live pulsing signal nodes, and responsive Altair charts.
   - 100% styled components without relying on default unstyled widgets.

3. **🧠 Dual-Layer Risk Engine**
   - **Layer 1: ML Model**: 30-feature XGBoost classifier trained on historical credit card fraud patterns.
   - **Layer 2: Contextual Rule Engine**: Real-time evaluation of device fingerprint, geolocation anomalies, transaction velocities, and overnight timing.
   - **SHAP Explainability**: Visual impact decomposition showing exactly which features drove the fraud probability.

4. **⚡ What-If Twin & Attack Simulator**
   - **Twin Simulation**: Clone any active transaction, alter parameters (device, amount, timing), and observe the counterfactual risk delta in real time.
   - **Attack Stress Testing**: Stress-test transactions against high-value bursts, new device takeovers, location hopping, and coordinated fraud patterns.

5. **🤖 Gemini GenAI Risk Manager**
   - AI-assisted plain-language decision support that explains risk factors, recommends controls, and provides triage priorities without modifying deterministic ML scores.

6. **📋 Investigation & Audit Center**
   - Case tracking with statuses: `Open`, `Under Review`, `Escalated`, `Resolved - Fraud`, and `Resolved - Legitimate`.
   - Analyst notes, priority badges, and CSV export for compliance and auditing.

---

## 📁 Project Structure

```
fraudtwin_project/
├── app.py                      # Main entry point, page router, and sidebar navigation
├── domains/
│   ├── __init__.py
│   ├── config.py               # Feature schemas, weights, paths, and UI options
│   ├── database.py             # Multi-tenant SQLite database & cryptographic auth
│   ├── auth.py                 # User authentication, registration, and session setup
│   ├── landing.py              # Cinematic landing page with rotating 3D radar card
│   ├── home.py                 # Live risk monitor & user-scoped KPIs
│   ├── analysis.py             # Transaction scoring, SHAP drivers, Twin & Attack simulation
│   ├── investigation.py        # Case management, triage priority, status tracking
│   ├── reports.py              # User-isolated audit reports and CSV export
│   ├── setting.py              # User profile, appearance preferences, password updates
│   ├── risk_engine.py          # XGBoost scoring, scaling, contextual risk, attack stress
│   ├── ai_manager.py           # Gemini GenAI decision support with fallback cascade
│   ├── storage.py              # Database-backed storage facade preserving user scope
│   ├── state.py                # Session state lifecycle and navigation helpers
│   └── ui.py                   # Theme system, custom CSS, SVG background art, Altair charts
├── models/
│   ├── init_model.py           # Automatic bootstrap to generate model and scaler if absent
│   ├── fraud_model.pkl         # Trained XGBoost model
│   └── scaler.pkl              # Fitted StandardScaler for Time and Amount
├── scripts/
│   └── train_model.py          # Training pipeline (XGBoost + SMOTE) on full creditcard.csv
├── data/
│   └── fraudtwin.db            # SQLite database (auto-created on startup)
├── .streamlit/
│   └── config.toml             # Streamlit theme and performance configuration
├── requirements.txt            # Project dependencies
└── README.md                   # Documentation and guide
```

---

## 🛠️ Quickstart Guide

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```
*(On first launch, FraudTwin automatically initializes the SQLite database and bootstraps default model weights so it runs instantly with zero manual setup!)*

### 4. Optional: Gemini AI Integration
To enable the optional Gemini AI Risk Manager decision support:
1. Set the environment variable:
   ```bash
   # Windows PowerShell
   $env:GEMINI_API_KEY="your-api-key"
   ```
   *or create `.streamlit/secrets.toml`:*
   ```toml
   GEMINI_API_KEY = "your-api-key"
   GEMINI_MODEL = "gemini-2.5-flash"
   ```

### 5. Optional: Retrain on Full Kaggle Dataset
If you have downloaded the 150MB `creditcard.csv` dataset:
1. Place `creditcard.csv` inside the `data/` directory.
2. Run:
   ```bash
   python scripts/train_model.py
   ```
