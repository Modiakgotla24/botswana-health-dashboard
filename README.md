# Botswana Health Indicators Tracker

This project is a Streamlit dashboard that visualizes **WHO Global Health Observatory (GHO)** indicators for **Botswana**, and combines them with **Google Search Trends** to approximate public awareness.

## Features

- Browse WHO indicators for Botswana (mortality, adolescent deaths, infant mortality, etc.)
- Filter by:
  - Indicator
  - Breakdown (sex, age group, etc.)
  - Year range
- See:
  - Latest value
  - Change vs previous year
  - Trend over time (line chart)
- View Google Search interest in a related topic in Botswana

## Data

The main data source is a CSV file:

- `data/health_indicators_bwa.csv`

This file comes from WHO GHO exports for Botswana.

Columns used:

- `GHO (CODE)`
- `GHO (DISPLAY)`
- `YEAR (DISPLAY)`
- `COUNTRY (DISPLAY)`
- `DIMENSION (TYPE)`
- `DIMENSION (NAME)`
- `Numeric`

## How to run

```bash
# 1. Activate virtual environment
source venv/bin/activate   # or however you created it

# 2. Run the app
python -m streamlit run app.py
