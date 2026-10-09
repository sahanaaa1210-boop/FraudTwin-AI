import os
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

try:
    from imblearn.over_sampling import SMOTE
    HAS_SMOTE = True
except ImportError:
    HAS_SMOTE = False

from xgboost import XGBClassifier

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "creditcard.csv"
MODEL_PATH = BASE_DIR / "models" / "fraud_model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

def train():
    if not DATA_PATH.exists():
        print(f"Error: Dataset not found at {DATA_PATH}")
        print("Please place the creditcard.csv dataset into the data/ directory.")
        return

    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    print("Dataset loaded! Shape:", df.shape)

    X = df.drop("Class", axis=1)
    y = df["Class"]

    print("\nFraud distribution:")
    print(y.value_counts())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train = X_train.copy()
    X_test = X_test.copy()

    X_train[["Time", "Amount"]] = scaler.fit_transform(X_train[["Time", "Amount"]])
    X_test[["Time", "Amount"]] = scaler.transform(X_test[["Time", "Amount"]])

    if HAS_SMOTE:
        print("\nApplying SMOTE...")
        smote = SMOTE(random_state=42)
        X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    else:
        print("\nimbalanced-learn not installed; training without SMOTE...")
        X_train_resampled, y_train_resampled = X_train, y_train

    print("\nTraining FraudTwin AI model...")
    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train_resampled, y_train_resampled)
    print("Model training completed!")

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("\n==============================")
    print("MODEL PERFORMANCE")
    print("==============================")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    auc = roc_auc_score(y_test, y_prob)
    print("ROC-AUC Score:", round(auc, 4))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print(f"\nModel and scaler successfully saved to {MODEL_PATH} and {SCALER_PATH}")

if __name__ == "__main__":
    train()
