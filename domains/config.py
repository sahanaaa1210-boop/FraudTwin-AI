from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

DB_PATH = DATA_DIR / "fraudtwin.db"
MODEL_PATH = MODELS_DIR / "fraud_model.pkl"
SCALER_PATH = MODELS_DIR / "scaler.pkl"
HISTORY_FILE = DATA_DIR / "history.csv"
INVESTIGATION_FILE = DATA_DIR / "investigations.json"

# Model schema (30 features matching Credit Card Fraud dataset)
FEATURE_NAMES = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

# Scoring weights & bounds
MAX_CONTEXT_POINTS = 30
ML_WEIGHT = 0.7
CONTEXT_WEIGHT = 0.3

# Navigation
NAV_PAGES = ["Home", "Analyze", "Investigate", "Reports", "Settings"]

# Transaction dropdown options
DEVICE_OPTIONS = [
    "Desktop - Trusted Chrome",
    "Mobile App - iOS",
    "Mobile App - Android",
    "Mobile Browser",
    "New Device",
]

LOCATION_OPTIONS = [
    "Mumbai, IN",
    "Delhi, IN",
    "Bengaluru, IN",
    "Hyderabad, IN",
    "Chennai, IN",
    "Kolkata, IN",
    "Unusual Location",
]

TYPE_OPTIONS = [
    "POS Swipe",
    "Online Purchase",
    "ATM Withdrawal",
    "UPI Transfer",
    "Large Transfer",
]

# Risk color palette (semantic colors)
RISK_COLORS = {
    "HIGH RISK": "#E05260",
    "MEDIUM RISK": "#F3C86B",
    "LOW RISK": "#45A56A",
    "HIGH": "#E05260",
    "MEDIUM": "#F3C86B",
    "LOW": "#45A56A",
    "CRITICAL": "#E05260",
    "SEVERE": "#E05260",
    "MODERATE": "#F3C86B",
    "SEVERE ATTACK": "#E05260",
    "HIGH ATTACK RISK": "#E05260",
    "MODERATE ATTACK RISK": "#F3C86B",
    "LOW ATTACK IMPACT": "#45A56A",
}
