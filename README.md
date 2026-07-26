# 🛡️ AI-Powered User Behavior Anomaly Detection for Cybersecurity

An end-to-end User and Entity Behavior Analytics (UEBA) system that detects anomalous user activities using unsupervised machine learning. The project generates synthetic cybersecurity logs, learns normal user behavior using Isolation Forest, assigns risk scores, classifies detected anomalies, and visualizes security alerts through an interactive Streamlit dashboard.

---

## 📌 Problem Statement

Traditional rule-based security systems often fail to detect previously unseen insider threats and behavioral anomalies. This project addresses that challenge by building a lightweight AI-powered anomaly detection pipeline capable of identifying suspicious user activities without requiring labeled attack data.

---

## 🚀 Features

* 📊 **Synthetic Cybersecurity Log Generation**
* 🤖 **Unsupervised Anomaly Detection** using Isolation Forest
* ⚠️ **Risk Score Calculation** (0–100)
* 🔍 **Rule-Based Anomaly Classification**
* 📝 **Explainable AI** with human-readable alert descriptions
* 📈 **Interactive SOC-Style Dashboard** using Streamlit
* 📂 **End-to-End Machine Learning Pipeline**

---

## 🏗️ Project Architecture

```text
                Synthetic Log Generator
                          │
                          ▼
               synthetic_logs.csv
                          │
                          ▼
                 Data Preprocessing
                          │
                          ▼
               Feature Engineering
                          │
                          ▼
                Isolation Forest Model
                          │
                          ▼
                Risk Score Generation
                          │
                          ▼
          Rule-Based Attack Classification
                          │
                          ▼
            Streamlit Security Dashboard

---

# 📁 Project Structure

```text
AI-Behavioral-Anomaly-Detection/
│
├── data/
│   ├── synthetic_logs.csv
│   ├── processed_logs.csv
│   ├── predictions.csv
│   └── classified_predictions.csv
│
├── models/
│   ├── isolation_forest.pkl
│   ├── encoders.pkl
│   └── scaler.pkl
│
├── generator.py
├── preprocess.py
├── train.py
├── classifier.py
├── dashboard.py
│
├── requirements.txt
└── README.md
```

---

⚙️ Tech Stack

### Programming Language
* Python 3.10+

### Libraries
* Pandas
* NumPy
* Scikit-learn
* Faker
* Streamlit
* Matplotlib
* Joblib

📂 Dataset

The project creates a synthetic dataset containing approximately 5,000 user activity logs.

Each log contains:

| Feature | Description |
| :--- | :--- |
| `user_id` | User identifier |
| `timestamp` | Login timestamp |
| `login_hour` | Hour of login |
| `country` | Login country |
| `ip_address` | User IP |
| `device` | Device used |
| `resource` | Resource accessed |
| `auth_method` | Authentication method |
| `session_duration` | Session duration (minutes) |
| `command_count` | Commands executed |
| `failed_attempts` | Failed login attempts |
| `label` | Ground truth (Normal / Attack) |

Approximately 97% of the logs represent normal behavior, while 3% are injected anomalies.

---

🚨 Simulated Attack Types

The synthetic dataset contains four common cybersecurity attack scenarios:

### Brute Force Attack
* **Characteristics:**
  * Multiple failed login attempts
  * High authentication failures

### Impossible Travel
* **Characteristics:**
  * Same user logging in from geographically distant locations within a short period

### Device Spoofing
* **Characteristics:**
  * User accesses resources using an unfamiliar device

### Lateral Movement
* **Characteristics:**
  * Sudden access to privileged resources
  * High command execution count

---

🧠 Machine Learning Pipeline

### 1. Data Generation
Generates synthetic user behavior using Faker.

* **Output:** `synthetic_logs.csv`

---

### 2. Data Preprocessing
Operations performed:
* Timestamp parsing
* Feature extraction
* Label encoding
* Feature scaling
* Processed dataset creation

* **Output:** `processed_logs.csv`

---

### 3. Anomaly Detection
* **Model Used:** Isolation Forest
* **Configuration:**
  ```python
  IsolationForest(
      contamination=0.03,
      n_estimators=100,
      random_state=42
  )

The model learns normal user behavior and flags deviations as anomalies.

### 4. Risk Score Generation
Isolation Forest decision scores are normalized into a 0–100 risk score.

| Risk Score | Interpretation |
| :--- | :--- |
| **0–40** | Low Risk |
| **40–60** | Medium Risk |
| **60–80** | High Risk |
| **80–100** | Critical |

---

### 5. Rule-Based Classification
Detected anomalies are categorized into:
* Brute Force
* Impossible Travel
* Device Spoofing
* Lateral Movement

---

### 6. Explainability
Each detected anomaly includes an explanation such as:

> **Risk Score:** 94  
> **Attack Type:** Brute Force  
> **Reason:**  
> • Multiple failed login attempts  
> • Access outside normal working hours  
> • High anomaly score

---

## 📊 Dashboard

The Streamlit dashboard includes:

### Security Metrics
* Total Events
* Total Alerts
* Average Risk Score
* Critical Alerts

### Visualizations
* Risk Score Distribution
* Attack Type Distribution

### Panels & Tables
* Alert Table
* Event Logs
* Incident Investigation Panel


---

# ▶️ Running the Project

Follow the steps below to set up and run the complete AI Behavioral Anomaly Detection pipeline.

## Step 1: Clone the Repository

```bash
git clone https://github.com/nishantgoyal01/AI-Behavioral-Anomaly-Detection.git
cd AI-Behavioral-Anomaly-Detection
```

---

## Step 2: Create and Activate a Virtual Environment (Recommended)

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Generate Synthetic User Activity Logs

```bash
python generator.py
```

This generates the synthetic dataset and saves it as:

```text
data/synthetic_logs.csv
```

---

## Step 5: Preprocess the Dataset

```bash
python preprocess.py
```

This performs feature encoding and scaling, then saves:

```text
data/processed_logs.csv
models/encoders.pkl
models/scaler.pkl
```

---

## Step 6: Train the Anomaly Detection Model

```bash
python train.py
```

This trains the Isolation Forest model and saves:

```text
models/isolation_forest.pkl
data/predictions.csv
```

---

## Step 7: Classify Detected Anomalies

```bash
python classifier.py
```

This enriches detected anomalies with attack types, explanations, and risk levels, generating:

```text
data/classified_predictions.csv
```

---

## Step 8: Launch the Dashboard

```bash
streamlit run dashboard.py
```

Open the URL displayed in the terminal (typically **http://localhost:8501**) to explore the interactive cybersecurity dashboard.

---
## DASHBOARD SNAPSHOT

<img width="2940" height="6850" alt="image" src="https://github.com/user-attachments/assets/0abe3861-de9d-4c3e-b867-2548d927e519" />


---

# 📈 Project Workflow

```text
Generate Synthetic Logs
        │
        ▼
Preprocess Data
        │
        ▼
Train Isolation Forest
        │
        ▼
Detect Anomalies
        │
        ▼
Generate Risk Scores
        │
        ▼
Classify Attack Types
        │
        ▼
Visualize Security Insights
```

---

# 📊 Expected Results

The trained anomaly detection pipeline is capable of:

- ✅ Learning baseline user behavior from enterprise activity logs
- 🚨 Detecting unknown and suspicious user activities
- 📈 Assigning anomaly risk scores to detected events
- 🔍 Classifying anomalies into attack categories
- 🛡️ Providing explainable security alerts for investigation

---

# 📌 Future Improvements

The project can be extended with several advanced cybersecurity capabilities:

- Train the anomaly detection model using only normal behavioral data
- Support real-time log ingestion and streaming analytics
- Incorporate sequence-based anomaly detection using LSTMs or Transformers
- Integrate with SIEM platforms such as Splunk, ELK Stack, and Microsoft Sentinel
- Enrich alerts using MITRE ATT&CK mapping and threat intelligence feeds
- Containerize the application using Docker and deploy with Kubernetes
- Replace rule-based attack classification with supervised multi-class models
- Integrate Large Language Models (LLMs) for automated incident summarization and SOC assistance

---

# 🎯 Learning Outcomes

This project demonstrates practical implementation of:

- User and Entity Behavior Analytics (UEBA)
- Unsupervised Machine Learning
- Cybersecurity Anomaly Detection
- Feature Engineering
- Explainable AI (XAI)
- Risk Scoring and Threat Classification
- Interactive Data Visualization
- End-to-End Machine Learning Pipeline Development

---

# 👨‍💻 Author

**Nishant Goyal**

B.Tech, Computer Science and Engineering  
Vellore Institute of Technology, Bhopal
