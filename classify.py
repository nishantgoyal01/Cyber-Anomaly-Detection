import pandas as pd

# Load model predictions
df = pd.read_csv("data/predictions.csv")


def classify_attack(row):
    if row["failed_attempts"] > 5:
        return "Brute Force"

    elif row["command_count"] > 20:
        return "Lateral Movement"

    elif row["risk_score"] > 85:
        return "Device Spoofing"

    elif row["risk_score"] > 70:
        return "Impossible Travel"

    return "Unknown Anomaly"


def explain(row):
    reasons = []

    if row["failed_attempts"] > 5:
        reasons.append("Multiple failed login attempts detected.")

    if row["command_count"] > 20:
        reasons.append("Unusually high command execution.")

    if row["login_hour"] < 6 or row["login_hour"] > 22:
        reasons.append("Access outside normal working hours.")

    if row["risk_score"] > 85:
        reasons.append("Very high anomaly score.")

    if not reasons:
        reasons.append("Behavior deviates from learned baseline.")

    return " | ".join(reasons)


def risk_level(score):
    if score >= 80:
        return "Critical"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    return "Low"


attack_types = []
explanations = []

for _, row in df.iterrows():
    if row["prediction"] == 1:
        attack_types.append(classify_attack(row))
        explanations.append(explain(row))
    else:
        attack_types.append("Normal")
        explanations.append("Normal behavior.")

df["attack_type"] = attack_types
df["explanation"] = explanations
df["risk_level"] = df["risk_score"].apply(risk_level)

df.to_csv("data/classified_predictions.csv", index=False)

print("Classification complete!")
print(df[["risk_score", "risk_level", "attack_type", "explanation"]].head(10))