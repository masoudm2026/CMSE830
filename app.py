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
