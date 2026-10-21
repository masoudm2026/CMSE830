
"""
Used-Car Price Explorer
CMSE 830 Midterm Project

Run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Used-Car Price Explorer",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Simple navy-and-blue color theme
NAVY = "#17365D"
BLUE = "#2878B5"
TEAL = "#21A6A1"
LIGHT_BLUE = "#EAF2F8"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #F7F9FC;
    }}
    [data-testid="stSidebar"] {{
        background-color: {LIGHT_BLUE};
    }}
    h1, h2, h3 {{
        color: {NAVY};
    }}
    div[data-testid="stMetric"] {{
        background-color: white;
        border: 1px solid #D9E2F0;
        padding: 14px;
        border-radius: 10px;
    }}
    div[data-testid="stMetricLabel"] {{
        color: {NAVY};
    }}
    </style>
    """,
    unsafe_allow_html=True,
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


@st.cache_data(show_spinner="Loading automobile data...")
def load_data():
    """Load the local dataset if available; otherwise use the UCI source."""
    local_path = next(
        (path for path in LOCAL_DATA_CANDIDATES if path.exists()),
        None,
    )

    if local_path:
        data = pd.read_csv(
            local_path, names=COLUMNS, header=None, na_values="?"
        )
        source = f"Local file: {local_path}"
    else:
        data = pd.read_csv(
            DATA_URL, names=COLUMNS, header=None, na_values="?"
        )
        source = "UCI Machine Learning Repository"

    for col in NUMERIC_COLUMNS:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    for col in CATEGORICAL_COLUMNS:
        data[col] = data[col].astype("string").str.strip()

    # Keep the original approach: exclude records without a price.
    data = data.dropna(subset=["price"]).copy()
    data["make"] = data["make"].str.title()

    return data, source


def money(value):
    """Format a number as dollars."""
    return f"${value:,.0f}" if pd.notna(value) else "—"


def correlation(x, y):
    """Calculate Pearson correlation using complete pairs."""
    paired = pd.concat([x, y], axis=1).dropna()

    if len(paired) < 2 or paired.iloc[:, 0].nunique() < 2:
        return float("nan"), len(paired)

    return paired.iloc[:, 0].corr(paired.iloc[:, 1]), len(paired)


# Main heading
st.title("🚗 Used-Car Price Explorer")
st.caption("CMSE 830 | Interactive automobile data exploration")

st.markdown(
    """
**Guiding question:** Which recorded vehicle characteristics tend to be
associated with automobile price?

Use the filters to explore different groups of cars. These are historical
automobile records, not current-market listings, so the results should not
be treated as today's used-car price estimates.
"""
)

# Load data
try:
    df, data_source = load_data()
except Exception as exc:
    st.error(
        "The dataset could not be loaded. Check your internet connection, "
        "or place a copy at `data/automobile.csv`."
    )
    with st.expander("Technical details"):
        st.code(str(exc))
    st.stop()


# Sidebar filters
with st.sidebar:
    st.header("Explore the data")
    st.caption("Change the filters to update the charts and metrics.")

    makes = sorted(df["make"].dropna().unique().tolist())
    body_styles = sorted(df["body_style"].dropna().unique().tolist())
    fuel_types = sorted(df["fuel_type"].dropna().unique().tolist())

    min_price = int(df["price"].min())
    max_price = int(df["price"].max())

    # Set initial selections only the first time the app runs.
    st.session_state.setdefault("selected_makes", makes)
    st.session_state.setdefault("selected_bodies", body_styles)
    st.session_state.setdefault("selected_fuels", fuel_types)
    st.session_state.setdefault(
        "price_range", (min_price, max_price)
    )

    def reset_filters():
        """Restore all filters to their original settings."""
        st.session_state["selected_makes"] = makes
        st.session_state["selected_bodies"] = body_styles
        st.session_state["selected_fuels"] = fuel_types
        st.session_state["price_range"] = (min_price, max_price)

    st.button(
        "↻ Reset filters",
        on_click=reset_filters,
        use_container_width=True,
    )

    st.multiselect(
        "Manufacturer",
        options=makes,
        key="selected_makes",
    )

    st.multiselect(
        "Body style",
        options=body_styles,
        key="selected_bodies",
    )

    st.multiselect(
        "Fuel type",
        options=fuel_types,
        key="selected_fuels",
    )

    st.slider(
        "Price range ($)",
        min_value=min_price,
        max_value=max_price,
        step=100,
        key="price_range",
    )


# Apply the selected filters
filtered = df[
    df["make"].isin(st.session_state["selected_makes"])
    & df["body_style"].isin(st.session_state["selected_bodies"])
    & df["fuel_type"].isin(st.session_state["selected_fuels"])
    & df["price"].between(
        st.session_state["price_range"][0],
        st.session_state["price_range"][1],
    )
].copy()

st.caption(f"Data source: {data_source}")

# Summary metrics
metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric("Cars in selection", f"{len(filtered):,}")
metric2.metric("Median price", money(filtered["price"].median()))
metric3.metric("Mean price", money(filtered["price"].mean()))
metric4.metric("Manufacturers", f"{filtered['make'].nunique():,}")

if filtered.empty:
    st.warning(
        "No cars match these filters. Adjust the filters or select "
        "'Reset filters' in the sidebar."
    )
    st.stop()


# Main sections
tab_overview, tab_makes, tab_quality = st.tabs(
    [
        "📊 Price relationships",
        "🏷️ Manufacturer comparison",
        "🔎 Data quality & limits",
    ]
)


# TAB 1: Price relationships
with tab_overview:
    st.subheader("How are vehicle characteristics associated with price?")

    feature_options = {
        "Horsepower": "horsepower",
        "Engine size": "engine_size",
        "Curb weight": "curb_weight",
        "City fuel economy (MPG)": "city_mpg",
        "Highway fuel economy (MPG)": "highway_mpg",
    }

    feature_label = st.selectbox(
        "Choose a vehicle characteristic",
        list(feature_options.keys()),
    )

    feature = feature_options[feature_label]
    plot_data = filtered[[feature, "price", "make"]].dropna()
    corr, n_pairs = correlation(
        plot_data[feature], plot_data["price"]
    )

    left, right = st.columns([2, 1])

    with left:
        if plot_data.empty:
            st.info("There are no complete observations for this chart.")
        else:
            fig = px.scatter(
                plot_data,
                x=feature,
                y="price",
                hover_data=["make"],
                labels={
                    feature: feature_label,
                    "price": "Price ($)",
                    "make": "Manufacturer",
                },
                title=f"{feature_label} vs. automobile price",
                color_discrete_sequence=[BLUE],
                opacity=0.75,
            )

            fig.update_traces(marker={"size": 9})
            fig.update_layout(
                template="plotly_white",
                title_font_color=NAVY,
                xaxis_title=feature_label,
                yaxis_title="Price ($)",
                margin=dict(l=20, r=20, t=60, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)

    with right:
        st.metric(
            "Pearson correlation (r)",
            "N/A" if pd.isna(corr) else f"{corr:.2f}",
        )
        st.metric("Cars in this plot", f"{n_pairs:,}")

        st.markdown("**How to read this**")

        if pd.isna(corr):
            st.write(
                "There are not enough paired observations, or not enough "
                "variation, to calculate the correlation."
            )
        elif corr >= 0.5:
            st.write(
                f"Higher {feature_label.lower()} tends to be associated "
                "with higher prices in this selection."
            )
        elif corr <= -0.5:
            st.write(
                f"Higher {feature_label.lower()} tends to be associated "
                "with lower prices in this selection."
            )
        else:
            st.write(
                f"The linear association between {feature_label.lower()} "
                "and price is weak in this selection."
            )

        st.caption(
            "Correlation describes association, not causation. Other "
            "vehicle characteristics may also help explain price."
        )

    st.subheader("Price distribution")

    histogram = px.histogram(
        filtered,
        x="price",
        nbins=20,
        labels={"price": "Price ($)", "count": "Number of cars"},
        title="Distribution of prices in the current selection",
        color_discrete_sequence=[TEAL],
    )

    histogram.update_layout(
        template="plotly_white",
        title_font_color=NAVY,
        yaxis_title="Number of cars",
        margin=dict(l=20, r=20, t=60, b=20),
    )

    st.plotly_chart(histogram, use_container_width=True)


# TAB 2: Manufacturer comparison
with tab_makes:
    st.subheader("How do prices vary by manufacturer?")

    largest_group = int(filtered["make"].value_counts().max())
    maximum_group_size = max(1, min(20, largest_group))

    min_group_size = st.slider(
        "Minimum number of cars per manufacturer",
        min_value=1,
        max_value=maximum_group_size,
        value=min(2, maximum_group_size),
        key="minimum_group_size",
    )

    make_summary = (
        filtered.groupby("make", observed=True)["price"]
        .agg(count="count", median="median", mean="mean")
    )

    make_summary = make_summary[
        make_summary["count"] >= min_group_size
    ].sort_values("median", ascending=False)

    if make_summary.empty:
        st.info("No manufacturer meets that minimum group size.")
    else:
        chart_data = (
            make_summary.reset_index()
            .sort_values("median", ascending=True)
        )

        fig = px.bar(
            chart_data,
            x="median",
            y="make",
            orientation="h",
            hover_data=["count", "mean"],
            labels={
                "median": "Median price ($)",
                "make": "Manufacturer",
                "count": "Number of cars",
                "mean": "Mean price ($)",
            },
            title="Median price by manufacturer",
            color_discrete_sequence=[BLUE],
        )

        fig.update_layout(
            template="plotly_white",
            title_font_color=NAVY,
            yaxis_title="Manufacturer",
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(fig, use_container_width=True)

        display_summary = make_summary.copy()
        display_summary["median"] = display_summary["median"].map(money)
        display_summary["mean"] = display_summary["mean"].map(money)

        st.markdown("**Manufacturer summary**")
        st.dataframe(display_summary, use_container_width=True)

        st.caption(
            "Group sizes differ. A median based on a small number of "
            "cars may be unstable and should be interpreted cautiously."
        )

        summary_csv = make_summary.reset_index().to_csv(index=False).encode(
            "utf-8"
        )

        st.download_button(
            "Download manufacturer summary (CSV)",
            data=summary_csv,
            file_name="manufacturer_price_summary.csv",
            mime="text/csv",
        )


# TAB 3: Data quality and limitations
with tab_quality:
    st.subheader("Data quality checks")

    total_rows = len(df)
    duplicate_rows = int(df.duplicated().sum())

    # df already excludes records with missing prices.
    missing_price_after_cleaning = int(df["price"].isna().sum())

    missing_table = df.isna().sum().rename(
        "Missing values"
    ).to_frame()

    missing_table["Percent missing"] = (
        100 * missing_table["Missing values"] / len(df)
    ).round(1)

    missing_table = missing_table[
        missing_table["Missing values"] > 0
    ].sort_values("Missing values", ascending=False)

    q1, q2, q3 = st.columns(3)

    q1.metric("Rows retained after price cleaning", f"{total_rows:,}")
    q2.metric("Exact duplicate rows", f"{duplicate_rows:,}")
    q3.metric(
        "Missing prices after cleaning",
        f"{missing_price_after_cleaning:,}",
    )

    st.markdown("**Missing values by column (before filtering)**")

    if missing_table.empty:
        st.write("No missing values were detected.")
    else:
        st.dataframe(missing_table, use_container_width=True)

        missing_chart_data = (
            missing_table.reset_index()
            .rename(columns={"index": "Column"})
        )

        missing_fig = px.bar(
            missing_chart_data,
            x="Missing values",
            y="Column",
            orientation="h",
            title="Columns with missing values",
            color_discrete_sequence=[TEAL],
        )

        missing_fig.update_layout(
            template="plotly_white",
            title_font_color=NAVY,
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(missing_fig, use_container_width=True)

    st.markdown("**Important limitations**")

    st.markdown(
        """
- **Historical data:** These automobiles are from an older era and do not
  represent today's used-car market.
- **Missing values:** Some variables, including normalized losses and
  engine specifications, have missing observations.
- **Unequal group sizes:** Some manufacturers and body styles have more
  records than others.
- **Potential confounding:** Mileage, condition, accident history,
  maintenance, location, and current market demand are not represented.
- **Association is not causation:** Correlations do not show that one
  characteristic alone causes a higher or lower price.
- **Price is not a modern valuation:** Do not use these results to set a
  current listing price.
"""
    )


# Download the currently filtered records
st.divider()

st.download_button(
    "⬇️ Download filtered records (CSV)",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="used_car_filtered_data.csv",
    mime="text/csv",
)

st.caption(
    "CMSE 830 Midterm Project · Used-Car Price Explorer · "
    "Source: UCI Automobile dataset (imports-85)"
)
