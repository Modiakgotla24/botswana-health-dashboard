import streamlit as st
import pandas as pd
import plotly.express as px
from pytrends.request import TrendReq

st.set_page_config(
    page_title="Botswana Health Indicators Tracker",
    layout="wide"
)

DATA_PATH = "data/health_indicators_bwa.csv"


# --------------------------
# DATA LOADING & CLEANING
# --------------------------

def clean_who_botswana(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the WHO GHO Botswana CSV.

    - Drop metadata row(s) that start with '#'
    - Keep only rows with numeric values
    - Extract year (int) and numeric values (float)
    - Keep key columns for analysis
    """

    df = df_raw.copy()

    # Remove metadata rows
    df = df[~df["YEAR (DISPLAY)"].astype(str).str.startswith("#")]
    df = df[~df["GHO (CODE)"].astype(str).str.startswith("#")]

    # Drop rows without numeric values
    df = df.dropna(subset=["Numeric"])

    # Create numeric year + value columns
    df["year"] = df["YEAR (DISPLAY)"].astype(int)
    df["value"] = df["Numeric"].astype(float)

    # Keep relevant columns
    keep_cols = [
        "GHO (CODE)", "GHO (DISPLAY)",
        "year", "value",
        "COUNTRY (DISPLAY)",
        "DIMENSION (TYPE)", "DIMENSION (NAME)"
    ]
    df = df[keep_cols]

    # Create a breakdown label like "SEX – Both sexes" or "AGEGROUP – 0–27 days"
    dim_type = df["DIMENSION (TYPE)"].fillna("None")
    dim_name = df["DIMENSION (NAME)"].fillna("All")
    df["breakdown"] = dim_type + " – " + dim_name

    return df


@st.cache_data(show_spinner=True)
def load_data(path: str) -> pd.DataFrame:
    try:
        raw = pd.read_csv(path)
    except Exception as e:
        st.error(f"Could not read data file at '{path}': {e}")
        return pd.DataFrame()

    df = clean_who_botswana(raw)

    if df.empty:
        st.error("Data file loaded, but no valid rows after cleaning.")
    return df


@st.cache_data(show_spinner=False)
def get_google_trends(keyword: str, geo: str = "BW", timeframe: str = "2018-01-01 2025-12-31"):
    """
    Fetch Google Trends interest over time for a given keyword in Botswana.
    """
    try:
        pytrends = TrendReq(hl="en-US", tz=120)
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo)
        trends_df = pytrends.interest_over_time()

        if trends_df.empty:
            return trends_df

        if "isPartial" in trends_df.columns:
            trends_df = trends_df.drop(columns=["isPartial"])

        return trends_df

    except Exception as e:
        st.warning(f"Could not load Google Trends data for '{keyword}': {e}")
        return pd.DataFrame()


def describe_indicator(indicator_name: str) -> str:
    """
    Return a simple English description for some key indicators.
    Fallback: generic explanation.
    """
    name = indicator_name.lower()

    if "infant" in name or "neonatal" in name or "under-five" in name:
        return (
            "This indicator tracks deaths among very young children. "
            "Higher values usually mean worse outcomes for child survival; "
            "falling trends are a positive sign."
        )
    if "adolescent" in name:
        return (
            "This indicator focuses on health outcomes among adolescents. "
            "Monitoring this helps understand risk, injuries, and access to care for young people."
        )
    if "maternal" in name:
        return (
            "This indicator relates to the health and survival of mothers during pregnancy, "
            "childbirth, and the postnatal period. Lower mortality is better."
        )
    if "hiv" in name:
        return (
            "This indicator describes HIV-related burden or services. "
            "Declining mortality or incidence is usually good; increasing coverage of treatment is positive."
        )
    if "tb" in name or "tuberculosis" in name:
        return (
            "This indicator relates to tuberculosis burden or control. "
            "Higher mortality or incidence is concerning; declining trends suggest better TB control."
        )
    if "suicide" in name:
        return (
            "This indicator tracks deaths due to suicide. "
            "Rising values can signal growing mental health and social stress challenges."
        )

    return (
        "This indicator reflects a specific health outcome or service coverage in Botswana. "
        "Changes over time can signal improvements or emerging challenges in the health system."
    )


def classify_trend(df_yearly: pd.DataFrame) -> dict:
    """
    Classify the trend as increasing / decreasing / stable and compute percent change.
    Returns a small dict with narrative pieces.
    """
    first_row = df_yearly.iloc[0]
    last_row = df_yearly.iloc[-1]

    start_year = int(first_row["year"])
    end_year = int(last_row["year"])
    start_val = first_row["value"]
    end_val = last_row["value"]

    absolute_change = end_val - start_val
    if start_val == 0:
        percent_change = None
    else:
        percent_change = (absolute_change / start_val) * 100.0

    # Simple classification thresholds
    if percent_change is None:
        label = "uncertain"
    else:
        if percent_change > 10:
            label = "increasing"
        elif percent_change < -10:
            label = "decreasing"
        else:
            label = "relatively stable"

    return {
        "start_year": start_year,
        "end_year": end_year,
        "start_val": start_val,
        "end_val": end_val,
        "absolute_change": absolute_change,
        "percent_change": percent_change,
        "label": label,
    }


def make_trend_narrative(indicator_name: str, trend_info: dict) -> str:
    """
    Build a short national health narrative sentence about the trend.
    """
    label = trend_info["label"]
    start_year = trend_info["start_year"]
    end_year = trend_info["end_year"]
    start_val = trend_info["start_val"]
    end_val = trend_info["end_val"]
    pct = trend_info["percent_change"]

    # Round values for readability
    start_val_r = round(start_val, 2)
    end_val_r = round(end_val, 2)
    if pct is None:
        pct_txt = "an uncertain percentage change (starting value was zero)"
    else:
        pct_txt = f"about {pct:.1f}%"

    if label == "increasing":
        return (
            f"Between {start_year} and {end_year}, this indicator increased "
            f"from {start_val_r} to {end_val_r}, a change of {pct_txt}. "
            f"This suggests a worsening of the measured burden if higher values are harmful, "
            f"or improvement if the indicator tracks coverage or access."
        )
    if label == "decreasing":
        return (
            f"Between {start_year} and {end_year}, this indicator decreased "
            f"from {start_val_r} to {end_val_r}, a change of {pct_txt}. "
            f"For outcomes where high values are harmful (like deaths or mortality), "
            f"this pattern is generally positive."
        )
    if label == "relatively stable":
        return (
            f"From {start_year} to {end_year}, this indicator stayed relatively stable "
            f"around {end_val_r}, with {pct_txt} change overall. "
            f"This may mean that major shifts in this health area have not yet occurred."
        )

    return (
        f"From {start_year} to {end_year}, this indicator changed from {start_val_r} to {end_val_r}. "
        f"More detailed context is needed to interpret whether this is good or bad for Botswana."
    )


# --------------------------
# MAIN APP
# --------------------------

st.title("Botswana Health Indicators Tracker")
st.caption(
    "WHO Global Health Observatory (GHO) indicators for Botswana "
    "+ live Google Search interest in related topics."
)

df = load_data(DATA_PATH)
if df is None or df.empty:
    st.stop()

# Sidebar filters
with st.sidebar:
    st.header("Filters")

    # Reset button (uses session_state keys)
    if st.button("🔁 Reset filters"):
        if "indicator" in st.session_state:
            del st.session_state["indicator"]
        if "breakdown" in st.session_state:
            del st.session_state["breakdown"]
        if "year_range" in st.session_state:
            del st.session_state["year_range"]
        st.rerun()

    # Indicator selection
    indicator_names = sorted(df["GHO (DISPLAY)"].unique())
    selected_indicator = st.selectbox(
        "📊 Select indicator",
        options=indicator_names,
        index=0,
        key="indicator"
    )

    # Subset for this indicator
    df_ind_all = df[df["GHO (DISPLAY)"] == selected_indicator]

    # Breakdown selection (e.g., "SEX – Both sexes", "AGEGROUP – 0–27 days")
    breakdown_options = sorted(df_ind_all["breakdown"].unique())
    breakdown_options_display = ["All breakdowns (average)"] + breakdown_options

    # Determine default index for breakdown
    if "breakdown" in st.session_state and st.session_state["breakdown"] in breakdown_options_display:
        default_breakdown_index = breakdown_options_display.index(st.session_state["breakdown"])
    else:
        default_breakdown_index = 0

    selected_breakdown = st.selectbox(
        "👤 Breakdown (sex/age/etc.)",
        options=breakdown_options_display,
        index=default_breakdown_index,
        key="breakdown"
    )

    # Year range slider with single-year protection
    min_year = int(df_ind_all["year"].min())
    max_year = int(df_ind_all["year"].max())

    if min_year == max_year:
        st.info(f"Only data for year {min_year} is available for this indicator/breakdown.")
        year_range = (min_year, max_year)
    else:
        # Use session_state default if present
        if "year_range" in st.session_state:
            yr_default = st.session_state["year_range"]
            yr_start = max(min_year, int(yr_default[0]))
            yr_end = min(max_year, int(yr_default[1]))
        else:
            yr_start, yr_end = min_year, max_year

        year_range = st.slider(
            "📅 Year range",
            min_value=min_year,
            max_value=max_year,
            value=(yr_start, yr_end),
            key="year_range"
        )

# Apply filters to data
df_ind = df[df["GHO (DISPLAY)"] == selected_indicator]
df_ind = df_ind[(df_ind["year"] >= year_range[0]) & (df_ind["year"] <= year_range[1])]

if selected_breakdown != "All breakdowns (average)":
    df_ind = df_ind[df_ind["breakdown"] == selected_breakdown]

# Aggregate by year (average if multiple breakdowns)
df_yearly = (
    df_ind
    .groupby("year", as_index=False)["value"]
    .mean()
    .sort_values("year")
)

if df_yearly.empty:
    st.warning("No data available for this combination of indicator, breakdown, and years.")
    st.stop()

# Compute trend information and narrative
trend_info = classify_trend(df_yearly)
narrative = make_trend_narrative(selected_indicator, trend_info)
indicator_explainer = describe_indicator(selected_indicator)

# Tabs: WHO data vs Google Trends
tab1, tab2 = st.tabs(["📊 WHO Indicator Trend", "📈 Google Search Trends (Botswana)"])

with tab1:
    st.subheader(selected_indicator)

    # KPIs
    latest_row = df_yearly.iloc[-1]
    latest_year = int(latest_row["year"])
    latest_value = latest_row["value"]

    if len(df_yearly) > 1:
        prev_row = df_yearly.iloc[-2]
        change_abs = latest_value - prev_row["value"]
        if prev_row["value"] != 0:
            change_pct = (change_abs / prev_row["value"]) * 100.0
        else:
            change_pct = None
    else:
        change_abs = 0.0
        change_pct = None

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Latest year", latest_year)
    with col2:
        st.metric("Latest value", f"{latest_value:.2f}")
    with col3:
        st.metric("Change vs previous year", f"{change_abs:+.2f}")
    with col4:
        if change_pct is None:
            st.metric("Percent change vs prev.", "n/a")
        else:
            st.metric("Percent change vs prev.", f"{change_pct:+.1f}%")

    # Trend narrative & description
    st.markdown("### 🩺 How to read this indicator")
    st.write(indicator_explainer)

    st.markdown("### 🇧🇼 Botswana trend summary")
    st.write(narrative)

    # Line chart over years
    fig = px.line(
        df_yearly,
        x="year",
        y="value",
        markers=True,
        title=f"{selected_indicator} – Botswana"
    )
    fig.update_traces(line=dict(width=3))
    fig.update_layout(
        title_x=0.5,
        hovermode="x unified",
        margin=dict(l=40, r=20, t=60, b=40),
    )
    fig.update_xaxes(title="Year", showgrid=True)
    fig.update_yaxes(title="Value", showgrid=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Data table")
    st.dataframe(df_yearly, use_container_width=True)

with tab2:
    st.subheader("Google Search Interest in Related Topic (Botswana)")

    # Build a simple keyword from the indicator text
    keyword = selected_indicator.split(",")[0].split("(")[0]
    keyword = keyword[:80]  # avoid very long strings

    st.write(f"Using keyword for Google Trends: **{keyword} Botswana**")

    trends_df = get_google_trends(keyword=f"{keyword} Botswana")

    if trends_df.empty:
        st.info("No Google Trends data returned for this topic / timeframe.")
    else:
        value_col = trends_df.columns[0]

        fig_trends = px.line(
            trends_df.reset_index(),
            x="date",
            y=value_col,
            title=f"Google Search Interest over time – '{keyword} Botswana'"
        )
        fig_trends.update_traces(line=dict(width=2))
        fig_trends.update_layout(
            title_x=0.5,
            hovermode="x unified",
            margin=dict(l=40, r=20, t=60, b=40),
        )
        fig_trends.update_xaxes(title="Date", showgrid=True)
        fig_trends.update_yaxes(title="Relative search interest (0–100)", showgrid=True)
        st.plotly_chart(fig_trends, use_container_width=True)

        with st.expander("Show Google Trends data table"):
            st.dataframe(trends_df, use_container_width=True)