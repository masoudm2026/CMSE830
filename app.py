"""
Used-Car Price Explorer
CMSE 830 Midterm Project

Run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""

from pathlib import Path
from urllib.error import URLError

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Used-Car Price Explorer",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# UCI Automobile / imports-85 data. A local CSV can be placed in data/automobile.csv.
DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data"
LOCAL_DATA_CANDIDATES = [
    Path("data/automobile.csv"),
    Path("automobile.csv"),
]

COLUMNS = [
    "symboling", "normalized_losses", "make", "fuel_type", "aspiration",
    "num_of_doors", "body_style", "drive_wheels", "engine_location",
    "wheel_base", "length", "width", "height", "curb_weight", "engine_type",
    "num_of_cylinders", "engine_size", "fuel_system", "bore", "stroke",
    "compression_ratio", "horsepower", "peak_rpm", "city_mpg", "highway_mpg",
    "price",
]
NUMERIC_COLUMNS = [
    "symboling", "normalized_losses", "wheel_base", "length", "width", "height",
    "curb_weight", "engine_size", "bore", "stroke", "compression_ratio",
    "horsepower", "peak_rpm", "city_mpg", "highway_mpg", "price",
]


@st.cache_data(show_spinner="Loading the automobile dataset…")
def load_data():
    """Load from a local copy first, then try the public UCI source."""
    local_path = next((p for p in LOCAL_DATA_CANDIDATES if p.exists()), None)
    if local_path is not None:
        data = pd.read_csv(local_path, names=COLUMNS, header=None, na_values="?")
        source = f"local file ({local_path})"
    else:
        data = pd.read_csv(DATA_URL, names=COLUMNS, header=None, na_values="?")
        source = "UCI Machine Learning Repository (downloaded at runtime)"

    for col in NUMERIC_COLUMNS:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    for col in ["make", "fuel_type", "aspiration", "num_of_doors", "body_style",
                "drive_wheels", "engine_location", "engine_type", "num_of_cylinders",
                "fuel_system"]:
        data[col] = data[col].astype("string").str.strip()

    # Price is the outcome of interest; rows without price cannot support the plots.
    data = data.dropna(subset=["price"]).copy()
    data["make"] = data["make"].str.title()
    return data, source


def money(value):
    return f"${value:,.0f}" if pd.notna(value) else "—"


def correlation_text(series, feature_label):
    corr = series.corr(series.index.to_series()) if False else None
    # Placeholder intentionally avoided: correlation is computed from paired columns below.
    return corr


st.title("🚗 Used-Car Price Explorer")
st.caption("A data story for comparing automobile characteristics and prices in the UCI Automobile dataset.")

st.markdown(
    """
    **Guiding question:** Which recorded vehicle characteristics tend to be associated with price?

    Use the filters to compare a subset of cars. The dataset describes automobiles from an older era,
    so treat the results as an exploration of historical patterns—not a current-market valuation tool.
    """
)

try:
    df, data_source = load_data()
except (Exception, URLError) as exc:
    st.error("The dataset could not be loaded. Check your internet connection or place a CSV copy at `data/automobile.csv`.")
    with st.expander("Technical details"):
        
