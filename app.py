
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Used-Car Price Explorer")

st.write(
    "Explore how horsepower is associated with used-car prices. "
    "Select manufacturers to compare their cars."
)

url = (
    "https://archive.ics.uci.edu/ml/"
    "machine-learning-databases/autos/imports-85.data"
)

columns = [
    "symboling", "normalized_losses", "make", "fuel_type",
    "aspiration", "num_of_doors", "body_style", "drive_wheels",
    "engine_location", "wheel_base", "length", "width", "height",
    "curb_weight", "engine_type", "num_of_cylinders", "engine_size",
    "fuel_system", "bore", "stroke", "compression_ratio",
    "horsepower", "peak_rpm", "city_mpg", "highway_mpg", "price"
]

@st.cache_data
def load_data():
    df = pd.read_csv(url, names=columns, na_values="?")
    for col in ["price", "horsepower"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load the dataset: {e}")
    st.stop()

manufacturers = sorted(df["make"].dropna().unique())

selected = st.multiselect(
    "Select manufacturers",
    manufacturers,
    default=manufacturers[:3]
)

filtered = df[
    df["make"].isin(selected)
].dropna(subset=["price", "horsepower"])

st.write("Number of cars:", len(filtered))

if not filtered.empty:
    fig, ax = plt.subplots()
    ax.scatter(filtered["horsepower"], filtered["price"])
    ax.set_xlabel("Horsepower")
    ax.set_ylabel("Price")
    ax.set_title("Horsepower vs. Used-Car Price")
    fig.tight_layout()
    st.pyplot(fig)

    st.subheader("Price summary by manufacturer")
    summary = filtered.groupby("make")["price"].agg(
        ["count", "median", "mean"]
    )
    st.dataframe(summary.round(2))
else:
    st.warning("Select a manufacturer with available data.")
