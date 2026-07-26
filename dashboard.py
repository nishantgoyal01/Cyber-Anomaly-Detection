import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ======================================================
# Page Configuration
# ======================================================

st.set_page_config(
    page_title="Cyber Behaviour Analytics",
    page_icon="🛡️",
    layout="wide",
)

plt.rcParams.update({
    "figure.figsize": (8, 4),
    "axes.titlesize": 15,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.grid": True,
    "grid.alpha": 0.3,
})

# ======================================================
# Title
# ======================================================

st.title("🛡️ AI Powered Behavioural Anomaly Detection")
st.markdown(
    """
Enterprise User & Entity Behaviour Analytics (UEBA) Dashboard powered by
Machine Learning for detecting anomalous user activities.
"""
)

# ======================================================
# Load Data
# ======================================================

df = pd.read_csv("data/classified_predictions.csv")

# ======================================================
# KPIs
# ======================================================

alerts = df[df["prediction"] == 1]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📄 Total Events", len(df))

with col2:
    st.metric("🚨 Detected Alerts", len(alerts))

with col3:
    st.metric("📈 Average Risk Score", f"{df['risk_score'].mean():.2f}")

with col4:
    st.metric(
        "🔥 Critical Alerts",
        len(df[df["risk_level"] == "Critical"])
    )

# ======================================================
# Sidebar Filters
# ======================================================

st.sidebar.header("🔍 Filters")

risk = st.sidebar.selectbox(
    "Risk Level",
    ["All"] + sorted(df["risk_level"].unique())
)

attack = st.sidebar.selectbox(
    "Attack Type",
    ["All"] + sorted(df["attack_type"].unique())
)

filtered = df.copy()

if risk != "All":
    filtered = filtered[
        filtered["risk_level"] == risk
    ]

if attack != "All":
    filtered = filtered[
        filtered["attack_type"] == attack
    ]

# ======================================================
# Dashboard Charts
# ======================================================

left, right = st.columns(2)

# ======================================================
# Risk Distribution
# ======================================================

with left:

    st.subheader("📊 Risk Score Distribution")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.hist(
        filtered["risk_score"],
        bins=25,
        edgecolor="black",
        linewidth=0.7
    )

    mean_score = filtered["risk_score"].mean()

    ax.axvline(
        mean_score,
        linestyle="--",
        linewidth=2,
        label=f"Average = {mean_score:.2f}"
    )

    ax.set_xlabel("Risk Score")
    ax.set_ylabel("Events")
    ax.set_title("Distribution of Risk Scores")

    ax.legend()

    st.pyplot(fig)

# ======================================================
# Attack Distribution
# ======================================================

with right:

    st.subheader("⚠️ Attack Distribution")

    attack_counts = (
        filtered["attack_type"]
        .value_counts()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 4))

    bars = ax.bar(
        attack_counts.index,
        attack_counts.values
    )

    for bar in bars:
        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            str(int(height)),
            ha="center",
            fontsize=9,
        )

    ax.set_title("Attack Categories")
    ax.set_xlabel("Attack Type")
    ax.set_ylabel("Count")

    plt.xticks(rotation=20)

    st.pyplot(fig)

# ======================================================
# Second Row
# ======================================================

left, right = st.columns(2)

# ======================================================
# Risk Level Breakdown
# ======================================================

with left:

    st.subheader("🟢 Risk Level Breakdown")

    risk_counts = filtered["risk_level"].value_counts()

    fig, ax = plt.subplots(figsize=(7, 6))

    wedges, texts, autotexts = ax.pie(
        risk_counts,
        labels=None,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.8,
        wedgeprops=dict(width=0.45)   # Creates the donut chart
    )

    # Legend
    ax.legend(
        wedges,
        risk_counts.index,
        title="Risk Levels",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    # Center text
    ax.text(
        0, 0,
        "Risk\nLevels",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_title("Risk Level Distribution", fontsize=15, weight="bold")

    plt.tight_layout()

    st.pyplot(fig)

# ======================================================
# Login Timeline
# ======================================================

with right:

    st.subheader("🕒 Login Activity by Hour")

    hour_counts = (
        filtered["login_hour"]
        .value_counts()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(
        hour_counts.index,
        hour_counts.values,
        marker="o",
        linewidth=2,
    )

    ax.set_xticks(range(6))

    ax.set_xlabel("Hour")
    ax.set_ylabel("Logins")
    ax.set_title("User Login Timeline")

    st.pyplot(fig)

# ======================================================
# Top Risk Users
# ======================================================

st.subheader("👤 Top 10 High Risk Users")

top_users = (
    filtered.groupby("user_id")["risk_score"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.barh(
    top_users.index,
    top_users.values
)

ax.invert_yaxis()

ax.set_xlabel("Average Risk Score")
ax.set_title("Users with Highest Average Risk")

for bar in bars:
    width = bar.get_width()

    ax.text(
        width + 0.02,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.2f}",
        va="center",
    )

st.pyplot(fig)

# ======================================================
# Alert Table
# ======================================================

st.subheader("🚨 Detected Alerts")

alerts = (
    filtered[
        filtered["prediction"] == 1
    ]
    .sort_values(
        by="risk_score",
        ascending=False
    )
)

st.dataframe(
    alerts[
        [
            "risk_score",
            "risk_level",
            "attack_type",
            "user_id",
            "login_hour",
            "explanation",
        ]
    ],
    use_container_width=True,
)

# ======================================================
# Investigation Panel
# ======================================================

st.subheader("🔍 Alert Investigation")

if not alerts.empty:

    selected = st.selectbox(
        "Select Alert",
        alerts.index
    )

    row = alerts.loc[selected]

    c1, c2 = st.columns(2)

    with c1:

        st.info(f"### {row['attack_type']}")

        st.write("**User ID:**", row["user_id"])
        st.write("**Risk Score:**", f"{row['risk_score']:.2f}")
        st.write("**Risk Level:**", row["risk_level"])
        st.write("**Login Hour:**", row["login_hour"])

    with c2:

        st.success("### Investigation Summary")

        st.write(row["explanation"])

# ======================================================
# Raw Logs
# ======================================================

st.subheader("📑 Raw Event Logs")

st.dataframe(
    filtered,
    use_container_width=True,
)