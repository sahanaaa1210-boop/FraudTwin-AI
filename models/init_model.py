import os
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

MODELS_DIR = Path(__file__).resolve().parent
MODEL_PATH = MODELS_DIR / "fraud_model.pkl"
SCALER_PATH = MODELS_DIR / "scaler.pkl"


def bootstrap_models():
    """
    Creates a pre-calibrated XGBoost fraud detection model and StandardScaler
    if they do not already exist. This ensures FraudTwin works immediately
    without requiring the user to download a 150MB Kaggle CSV beforehand.
    """
    if MODEL_PATH.exists() and SCALER_PATH.exists():
        print(f"Models already exist at {MODELS_DIR}")
        return

    print("Bootstrapping baseline fraud model and scaler...")

    np.random.seed(42)
    n_samples = 3000

    time_seconds = np.random.uniform(0, 86400, n_samples)
    amounts = np.concatenate([
        np.random.exponential(scale=1500, size=int(n_samples * 0.9)),
        np.random.uniform(50000, 250000, size=int(n_samples * 0.1))
    ])
    np.random.shuffle(amounts)

    scaler = StandardScaler()
    scaled_ta = scaler.fit_transform(pd.DataFrame({"Time": time_seconds, "Amount": amounts}))

    v_features = np.random.normal(0, 1, size=(n_samples, 28))
    feature_names = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]
    X = pd.DataFrame(
        np.column_stack([scaled_ta[:, 0:1], v_features, scaled_ta[:, 1:2]]),
        columns=feature_names
    )

    hours = (time_seconds / 3600) % 24
    risk_metric = (
        (amounts > 75000).astype(int) * 3 +
        ((hours < 5) | (hours > 23)).astype(int) * 2 +
        (v_features[:, 13] > 1.8).astype(int) * 2 +
        np.random.normal(0, 1, n_samples)
    )
    y = (risk_metric > 2.5).astype(int)

    model = XGBClassifier(
        n_estimators=80,
        max_depth=4,
        learning_rate=0.1,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, y)

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    print(f"Bootstrap complete: saved {MODEL_PATH} and {SCALER_PATH}")


if __name__ == "__main__":
    bootstrap_models()
