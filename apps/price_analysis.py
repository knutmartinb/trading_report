import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.calculations import compute_imbalance

def app():
    st.title("Price Analysis")

    df = st.session_state.get("df")
    if df is None:
        st.error("No data loaded.")
        return

    # Ensure volume columns exist
    df_calc = compute_imbalance(df)

    # Daily vs. Monthly toggle
    view = st.radio("View granularity", ["Daily", "Monthly"], horizontal=True)

    if view == "Monthly":
        df_plot = df_calc.resample("M").agg({
            "Spot price NO2":      "mean",
            "Imbalance price NO2": "mean",
        })
    else:
        df_plot = df_calc[["Spot price NO2", "Imbalance price NO2"]]

    # Time series chart
    fig = px.line(
        df_plot,
        labels={"value": "€/MWh", "index": "Date"},
        title=f"{view} Spot vs Imbalance Price"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Top/Bottom 5 price days (daily only)
    if view == "Daily":
        daily_price = df_calc.resample("D")["Spot price NO2"].mean().dropna()
        best5  = daily_price.nlargest(5).reset_index().rename(columns={"Spot price NO2":"Avg Spot Price"})
        worst5 = daily_price.nsmallest(5).reset_index().rename(columns={"Spot price NO2":"Avg Spot Price"})

        st.subheader("Top 5 Highest-Price Days")
        st.table(best5)
        st.subheader("Top 5 Lowest-Price Days")
        st.table(worst5)

    # Spot Price Distribution with fixed bin width
    st.subheader("Spot Price Distribution")
    bin_width = st.slider("Bin width (€/MWh)", min_value=1, max_value=50, value=5, step=1)
    fig2 = go.Figure(
        data=[
            go.Histogram(
                x=df_calc["Spot price NO2"],
                xbins=dict(size=bin_width)
            )
        ]
    )
    fig2.update_layout(
        title="Spot Price Histogram",
        xaxis_title="Spot price (€/MWh)",
        yaxis_title="Count"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Scatter: daily traded volume vs avg spot price (no trendline)
    if view == "Daily":
        st.subheader("Daily Traded Volume vs. Spot Price")
        daily_vol = (
            df_calc
            .resample("D")
            .agg({"Total_Traded":"sum", "Spot price NO2":"mean"})
            .dropna()
            .reset_index()
        )
        fig3 = px.scatter(
            daily_vol,
            x="Total_Traded",
            y="Spot price NO2",
            labels={"Total_Traded":"Total Traded (MWh)", "Spot price NO2":"Avg Spot Price (€/MWh)"},
            title="Volume vs. Spot Price"
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Download daily price summary (always available)
    st.subheader("Download Daily Price Summary")
    dl = df_calc.resample("D")["Spot price NO2"].mean().dropna().reset_index().rename(columns={"Spot price NO2":"Avg Spot Price"})
    csv = dl.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "daily_price_summary.csv", "text/csv")
