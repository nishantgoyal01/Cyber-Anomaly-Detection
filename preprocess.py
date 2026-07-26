import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("data/synthetic_logs.csv")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Feature engineering
df["day"] = df["timestamp"].dt.day
df["month"] = df["timestamp"].dt.month
df["weekday"] = df["timestamp"].dt.weekday
df["hour"] = df["timestamp"].dt.hour

# Drop raw timestamp
df.drop(columns=["timestamp"], inplace=True)

# Encode categorical columns
categorical_columns = [
    "user_id",
    "country",
    "device",
    "resource",
    "auth_method"
]

encoders = {}

for column in categorical_columns:
    encoder = LabelEncoder()
    df[column] = encoder.fit_transform(df[column])
    encoders[column] = encoder

# Binary label
df["is_anomaly"] = df["label"].apply(
    lambda x: 0 if x == "Normal" else 1
)

# Features for training
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

# Scale
scaler = StandardScaler()

df[feature_columns] = scaler.fit_transform(
    df[feature_columns]
)

# Save preprocessing objects
joblib.dump(encoders, "models/encoders.pkl")
joblib.dump(scaler, "models/scaler.pkl")

# Save processed data
df.to_csv(
    "data/processed_logs.csv",
    index=False
)

print("Preprocessing completed successfully!")
print(df.head())
print(f"Dataset Shape: {df.shape}")
print(df["is_anomaly"].value_counts())