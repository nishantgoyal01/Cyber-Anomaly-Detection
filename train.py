import joblib
import pandas as pd
import numpy as np

from sklearn.ensemble import IsolationForest

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

# Load processed data
df = pd.read_csv("data/processed_logs.csv")

feature_columns = [
    "user_id",
    "login_hour",
    "country",
    "device",
    "resource",
    "auth_method",
    "session_duration",
    "command_count",
    "failed_attempts",
    "day",
    "month",
    "weekday",
    "hour"
]

X = df[feature_columns]
y_true = df["is_anomaly"]

# Train model
model = IsolationForest(
    contamination=0.03,
    random_state=42,
    n_estimators=100
)

model.fit(X)

# Predict
predictions = model.predict(X)

df["prediction"] = np.where(predictions == -1, 1, 0)

# Risk Score
scores = model.decision_function(X)

risk = (scores.max() - scores)
risk = risk / risk.max()
risk = risk * 100

df["risk_score"] = risk.round(2)

# Evaluation
print("=" * 50)
print("Model Evaluation")
print("=" * 50)

print("\nAccuracy:")
print(accuracy_score(y_true, df["prediction"]))

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, df["prediction"]))

print("\nClassification Report:")
print(classification_report(y_true, df["prediction"]))

# Save model
joblib.dump(
    model,
    "models/isolation_forest.pkl"
)

# Save predictions
df.to_csv(
    "data/predictions.csv",
    index=False
)

print("\nTop 10 Highest Risk Events")
print(
    df[
        ["risk_score", "label", "prediction"]
    ]
    .sort_values(
        by="risk_score",
        ascending=False
    )
    .head(10)
)

print("\nModel saved successfully!")