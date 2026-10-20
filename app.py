"""
Used-Car Price Explorer
CMSE 830 Midterm Project

Run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Used-Car Price Explorer",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_URL = (
    "https://archive.ics.uci.edu/ml/"
    "machine-learning-databases/autos/imports-85.data"
)
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
    "symboling", "normalized_losses", "wheel_base", "length", "width",
    "height", "curb_weight", "engine_size", "bore", "stroke",
    "compression_ratio", "horsepower", "peak_rpm", "city_mpg",
    "highway_mpg", "price",
]
CATEGORICAL_COLUMNS = [
    "make", "fuel_type", "aspiration", "num_of_doors", "body_style",
    "drive_wheels", "engine_location", "engine_type", "num_of_cylinders",
    "fuel_system",
]


@st.cache_data(show_spinner="Loading automobile data…")
def load_data():
    """Read a local data copy if available; otherwise download from UCI."""
    local_path = next((p for p in LOCAL_DATA_CANDIDATES if p.exists()), None)
    if local_path:
        data = pd.read_csv(
            local_path, names=COLUMNS, header=None, na_values="?"
        )
        source = f"Local file: {local_path}"
    else:
        data = pd.read_csv(
            DATA_URL, names=COLUMNS, header=None, na_values="?"
        )
        source = "UCI Machine Learning Repository (downloaded at runtime)"

    for col in NUMERIC_COLUMNS:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    for col in CATEGORICAL_COLUMNS:
        data[col] = data[col].astype("string").str.strip()

    # Records without a price cannot be used in price comparisons.
    data = data.dropna(subset=["price"]).copy()
    data["make"] = data["make"].str.title()
    return data, source


def money(value):
    return f"${value:,.0f}" if pd.notna(value) else "—"


def correlation(x, y):
    paired = pd.concat([x, y], axis=1).dropna()
    if len(paired) < 2 or paired.iloc[:, 0].nunique() < 2:
        return float("nan"), len(paired)
    return paired.iloc[:, 0].corr(paired.iloc[:, 1]), len(paired)


st.title("🚗 Used-Car Price Explorer")
st.caption(
    "An interactive exploration of vehicle characteristics and prices "
    "in the UCI Automobile dataset."
)
st.markdown(
    """
**Guiding question:** Which recorded vehicle characteristics tend to be
associated with automobile price?

Use the filters to compare a subset of cars. These are historical automobile
records, not current-market listings, so the results should not be used as
today's price estimates.
"""
)

try:
    df, data_source = load_data()
except Exception as exc:
    st.error(
        "The dataset could not be loaded. Check your internet connection, "
        "or place a copy of the dataset at `data/automobile.csv`."
    )
    with st.expander("Technical details"):
        st.code(str(exc))
    st.stop()

with st.sidebar:
    st.header("Explore the data")
    st.caption("Filters update the charts and summaries below.")

    makes = sorted(df["make"].dropna().unique().tolist())
    selected_makes = st.multiselect(
        "Manufacturer",
        options=makes,
        default=makes,
        help="Clear the selection to compare no manufacturers.",
    )

    body_styles = sorted(df["body_style"].dropna().unique().tolist())
    selected_bodies = st.multiselect(
        "Body style", options=body_styles, default=body_styles
    )

    fuel_types = sorted(df["fuel_type"].dropna().unique().tolist())
    selected_fuels = st.multiselect(
        "Fuel type", options=fuel_types, default=fuel_types
    )

    min_price = int(df["price"].min())
    max_price = int(df["price"].max())
    price_range = st.slider(
        "Price range ($)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=100,
    )

filtered = df[
    df["make"].isin(selected_makes)
    & df["body_style"].isin(selected_bodies)
    & df["fuel_type"].isin(selected_fuels)
    & df["price"].between(price_range[0], price_range[1])
].copy()

st.caption(f"Data source: {data_source}")
metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric("Cars in selection", f"{len(filtered):,}")
metric2.metric("Median price", money(filtered["price"].median()))
metric3.metric("Mean price", money(filtered["price"].mean()))
metric4.metric("Manufacturers", f"{filtered['make'].nunique():,}")

if filtered.empty:
    st.warning("No cars match these filters. Adjust the filters in the sidebar.")
    st.stop()

tab_overview, tab_makes, tab_quality = st.tabs(
    ["Price relationships", "Manufacturer comparison", "Data quality & limits"]
)

with tab_overview:
    st.subheader("How do vehicle characteristics relate to price?")
    feature_options = {
        "Horsepower": "horsepower",
        "Engine size": "engine_size",
        "Curb weight": "curb_weight",
        "City fuel economy (MPG)": "city_mpg",
        "Highway fuel economy (MPG)": "highway_mpg",
    }
    feature_label = st.selectbox(
        "Choose a characteristic for the x-axis",
        list(feature_options.keys()),
        index=0,
    )
    feature = feature_options[feature_label]
    plot_data = filtered[[feature, "price"]].dropna()
    corr, n_pairs = correlation(plot_data[feature], plot_data["price"])

    left, right = st.columns([2, 1])
    with left:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(
            plot_data[feature], plot_data["price"],
            alpha=0.72, edgecolors="none"
        )
        ax.set_xlabel(feature_label)
        ax.set_ylabel("Price ($)")
        ax.set_title(f"{feature_label} vs. automobile price")
        ax.grid(True, alpha=0.25)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with right:
        st.metric("Pearson correlation (r)", "N/A" if pd.isna(corr) else f"{corr:.2f}")
        st.metric("Cars in this plot", f"{n_pairs:,}")
        st.markdown("**How to read this**")
        if pd.isna(corr):
            st.write("There are not enough paired observations to calculate a correlation.")
        elif corr >= 0.5:
            st.write(
                f"In this filtered subset, higher {feature_label.lower()} tends "
                "to be associated with higher prices."
            )
        elif corr <= -0.5:
            st.write(
                f"In this filtered subset, higher {feature_label.lower()} tends "
                "to be associated with lower prices."
            )
        else:
            st.write(
                f"The linear association between {feature_label.lower()} and "
                "price is weak in this filtered subset."
            )
        st.caption(
            "Correlation describes association, not causation. Other vehicle "
            "characteristics may also help explain price."
        )

    st.subheader("Price distribution")
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.hist(filtered["price"].dropna(), bins=20, edgecolor="white")
    ax.set_xlabel("Price ($)")
    ax.set_ylabel("Number of cars")
    ax.set_title("Distribution of prices in the current selection")
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with tab_makes:
    st.subheader("How do prices vary by manufacturer?")
    min_group_size = st.slider(
        "Minimum number of cars per manufacturer",
        min_value=1,
        max_value=max(1, min(20, int(filtered["make"].value_counts().max()))),
        value=2 if filtered["make"].value_counts().max() >= 2 else 1,
    )
    make_summary = (
        filtered.groupby("make", observed=True)["price"]
        .agg(count="count", median="median", mean="mean")
        .query("count >= @min_group_size")
        .sort_values("median", ascending=False)
    )

    if make_summary.empty:
        st.info("No manufacturer meets that minimum group size.")
    else:
        fig, ax = plt.subplots(figsize=(9, max(4, 0.35 * len(make_summary))))
        ordered = make_summary.sort_values("median", ascending=True)
        ax.barh(ordered.index.astype(str), ordered["median"])
        ax.set_xlabel("Median price ($)")
        ax.set_ylabel("Manufacturer")
        ax.set_title("Median price by manufacturer")
        ax.grid(axis="x", alpha=0.25)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        display_summary = make_summary.copy()
        display_summary["median"] = display_summary["median"].map(money)
        display_summary["mean"] = display_summary["mean"].map(money)
        st.dataframe(display_summary, use_container_width=True)

        st.caption(
            "Group sizes differ. A median based on a small number of cars "
            "may be unstable and should be interpreted cautiously."
        )

with tab_quality:
    st.subheader("Data quality checks")
    total_rows = len(df)
    missing_price = int(pd.to_numeric(df["price"], errors="coerce").isna().sum())
    duplicate_rows = int(df.duplicated().sum())
    missing_table = (
        df.isna().sum()
        .rename("Missing values")
        .to_frame()
    )
    missing_table["Percent missing"] = (
        100 * missing_table["Missing values"] / len(df)
    ).round(1)
    missing_table = missing_table[missing_table["Missing values"] > 0].sort_values(
        "Missing values", ascending=False
    )

    q1, q2, q3 = st.columns(3)
    q1.metric("Rows retained after missing-price removal", f"{total_rows:,}")
    q2.metric("Exact duplicate rows", f"{duplicate_rows:,}")
    q3.metric("Missing price values after cleaning", f"{missing_price:,}")

    st.markdown("**Missing values by column (before filtering)**")
    if missing_table.empty:
        st.write("No missing values were detected.")
    else:
        st.dataframe(missing_table, use_container_width=True)

    st.markdown("**Important limitations**")
    st.markdown(
        """
- **Historical data:** these automobiles are from an older era and do not represent today's used-car market.
- **Missing values:** some variables, including normalized losses and engine specifications, have missing observations.
- **Unequal group sizes:** some manufacturers and body styles have many more records than others.
- **Potential confounding:** mileage, condition, accident history, maintenance, location, and current market demand are not represented.
- **Association is not causation:** correlations do not show that a characteristic alone causes a higher or lower price.
- **Price is not a modern valuation:** do not use these results to set a current listing price.
"""
    )

st.divider()
st.caption(
    "CMSE 830 Midterm Project · Used-Car Price Explorer · "
    "Source: UCI Automobile dataset (imports-85)"
)

# Offer a download of the currently filtered records.
csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered records (CSV)",
    data=csv_bytes,
    file_name="used_car_filtered_data.csv",
    mime="text/csv",
)
