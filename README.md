# Botswana Health Indicators Dashboard (WHO + Google Trends)

Interactive Public Health Analytics for Botswana 

Developer: Kago Mhlanga Modiakgotla

# 📝 Overview

The Botswana Health Indicators Dashboard is an interactive analytics tool built with Streamlit that brings together:
	•	Official WHO Global Health Observatory (GHO) data, and
	•	Google Search Trends (PyTrends)

to help analyze national health outcomes, long-term trends, and public awareness across a wide range of indicators (HIV, TB, maternal health, infant mortality, suicide, adolescent health, and more).

This dashboard supports public health decision-making, research, data storytelling, and health policy communication by combining:
	•	Hard epidemiological data
	•	Real-time public search interest
	•	Automatically generated health narratives

⸻

 Features

 1. # Indicator Trend Analysis (WHO GHO Data)
	•	Filter by:
	•	Indicator (e.g., Infant mortality, Maternal deaths, HIV prevalence)
	•	Breakdown (age group, sex, category)
	•	Year range
	•	Automatic handling of single-year data
	•	Dynamic aggregation of breakdowns

 2. # Real-Time Google Trends Integration
	•	Fetches search interest for related health topics in Botswana
	•	Helps compare public awareness vs. actual health burden

  3. # KPI Engine

Automatically computes:
	•	Latest value
	•	Absolute year-over-year change
	•	Percent change
	•	Trend classification:
	•	Increasing
	•	Decreasing
	•	Stable

 4. # Auto-Generated Health Narratives

Every indicator receives:
	•	A plain-English explanation
	•	A Botswana-focused narrative interpreting the trend
	•	Context for whether rising/falling values are good or bad

 5. Professional Visualizations
	•	Clean Plotly charts with:
	•	Unified hover
	•	Centered titles
	•	Responsive layout
	•	High-quality tables and expanded views

 6. Quality-of-Life Features
	•	Reset Filters button
	•	Session state to remember selections
	•	Smart defaults for short datasets

⸻

 # Tech Stack

Languages & Libraries
	•	Python
	•	Pandas
	•	Plotly
	•	Streamlit
	•	PyTrends
	•	NumPy

Tools
	•	Git / GitHub
	•	Virtual Environments (venv)
	•	WHO GHO dataset exports

botswana-health-dashboard/
│
├── app.py                   # Main Streamlit application
├── requirements.txt         # Dependencies
├── README.md                # Project documentation
├── .gitignore
│
├── data/
│   └── health_indicators_bwa.csv
│
├── utils/
│   └── processing.py        # Helper data-cleaning functions
│
└── screenshots/
    ├── dashboard_home.png
    ├── indicator_trend.png
    ├── google_trends.png


## 📸 Dashboard Preview

Below are key screenshots from the Botswana Health Indicators Tracker, showing both WHO indicator trends and live Google Search interest.

---

### 🟦 Tuberculosis – New & Relapse Cases (Botswana)

#### Overview
![Tuberculosis overview](./screenshots/tb_overview.png)

#### Trend Over Time (WHO Indicator)
![Tuberculosis trend](./screenshots/tb_trend.png)

#### Google Search Interest (Botswana)
![Tuberculosis Google Trends](./screenshots/tb_trends_google.png)

---

### 🟪 TB Patients with Known HIV Status (%)

#### Overview
![TB/HIV overview](./screenshots/tbhiv_overview.png)

#### Trend Over Time (WHO Indicator)
![TB/HIV trend](./screenshots/tbhiv_trend.png)

#### Google Search Interest (Botswana)
![TB/HIV Google Trends](./screenshots/tbhiv_trends_google.png)

---

# How to Run Locally

1. Clone the repository (terminal)
git clone https://github.com/Modiakgotla24/botswana-health-dashboard.git
cd botswana-health-dashboard

2. Create a virtual environment(terminal)
python3.11 -m venv venv
source venv/bin/activate

3. Install dependencies (terminal)
pip install -r requirements.txt

4. Run the dashboard (terminal)
python -m streamlit run app.py


# Data Sources

World Health Organization – Global Health Observatory (GHO)
	•	Official Botswana health indicators
	•	Large-scale global health dataset

Google Trends (PyTrends API)
	•	Real-time search interest
	•	Awareness analysis for health topics

⸻

 # Why This Project Matters

Botswana faces unique public health challenges including:
	•	HIV/AIDS
	•	Tuberculosis
	•	Maternal and neonatal health
	•	Non-communicable diseases
	•	Mental health and suicide

This dashboard integrates official epidemiological data with public awareness data to help:
	•	Policymakers track progress
	•	Students learn with real datasets
	•	Researchers explore signals
	•	Data scientists analyze health trends
	•	NGOs understand awareness gaps

It is a foundation for data-driven health strategy.

Author

Kago Mhlanga Modiakgotla
Public Health | Data Science | Biology
Botswana 🇧🇼 | Russia 🇷🇺

GitHub: https://github.com/Modiakgotla24
Email: (modiakgotlakago@gmail.com)
