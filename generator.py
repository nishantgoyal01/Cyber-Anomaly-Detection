import random
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta


fake = Faker()

USERS = [
    "user_001",
    "user_002",
    "user_003",
    "user_004",
    "user_005",
    "user_006",
    "user_007",
    "user_008",
    "user_009",
    "user_010"
]

RESOURCES = [
    "CRM",
    "Email",
    "HR Portal",
    "Finance",
    "Database",
    "Admin Panel"
]

COUNTRIES = [
    "India",
    "USA",
    "Germany",
    "Singapore"
]

AUTH_METHODS = [
    "Password",
    "OAuth",
    "Certificate"
]

DEVICES = [
    "Windows",
    "Mac",
    "Linux"
]

def generate_normal_event(user):
    timestamp = fake.date_time_between(
        start_date="-30d",
        end_date="now"
    )

    return {
        "user_id": user,
        "timestamp": timestamp,
        "login_hour": timestamp.hour,
        "country": "India",
        "ip_address": fake.ipv4(),
        "device": "Windows",
        "resource": random.choice(["CRM", "Email"]),
        "auth_method": "Password",
        "session_duration": random.randint(15, 60),
        "command_count": random.randint(2, 10),
        "failed_attempts": 0,
        "label": "Normal"
    }

def brute_force(user):
    event = generate_normal_event(user)

    event["failed_attempts"] = random.randint(10,30)
    event["label"] = "Brute Force"

    return event

def impossible_travel(user):
    event = generate_normal_event(user)

    event["country"] = random.choice(
        ["Germany","USA","Singapore"]
    )

    event["label"] = "Impossible Travel"

    return event

def device_spoofing(user):
    event = generate_normal_event(user)

    event["device"] = "Linux"

    event["label"] = "Device Spoofing"

    return event

def lateral_movement(user):
    event = generate_normal_event(user)

    event["resource"] = "Admin Panel"
    event["command_count"] = random.randint(30,70)

    event["label"] = "Lateral Movement"

    return event

records = []

for _ in range(5000):

    user = random.choice(USERS)

    if random.random() < 0.97:

        records.append(generate_normal_event(user))

    else:

        attack = random.choice([
            brute_force,
            impossible_travel,
            device_spoofing,
            lateral_movement
        ])

        records.append(attack(user))

df = pd.DataFrame(records)

df.to_csv(
    "data/synthetic_logs.csv",
    index=False
)

print(df.head())

print(df["label"].value_counts())