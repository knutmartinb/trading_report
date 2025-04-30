# apps/volume_analysis.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.calculations import compute_imbalance

def app():
    st.title("Volume Analysis")

    df = st.session_state.get("df")
    if df is None:
        st.error("No data loaded.")
        return

    df = compute_imbalance(df)

    # Daily vs Monthly
    view = st.radio("View granularity", ["Daily", "Monthly"], horizontal=True)

    if view == "Monthly":
        df_plot = df.resample("M").agg({
            "Total_Actual": "sum",
            "Total_Traded": "sum",
            "Imbalance": "sum"
        })
    else:
        df_plot = df[["Total_Actual", "Total_Traded", "Imbalance"]]

    # Time series
    st.subheader(f"{view} Consumption & Traded Volumes")
    fig = px.line(
        df_plot,
        labels={"value": "MWh", "index": "Date"},
    )
    st.plotly_chart(fig, use_container_width=True)

    # Top & Bottom 5 imbalance days by absolute volume
    daily_imb = df.resample("D")["Imbalance"].sum().dropna().abs()
    top5_imb = daily_imb.nlargest(5).reset_index().rename(columns={"Imbalance": "Abs Imbalance"})
    worst5_imb = daily_imb.nsmallest(5).reset_index().rename(columns={"Imbalance": "Abs Imbalance"})

    st.subheader("Top 5 Days with Largest Imbalance")
    st.table(top5_imb)
    st.subheader("Top 5 Days with Smallest Imbalance")
    st.table(worst5_imb)

    # Histogram of imbalance
    st.subheader("Imbalance Volume Distribution")
    bins = st.slider("Bins", min_value=10, max_value=100, value=30, key="imb_bins")
    fig2 = px.histogram(
        df,
        x="Imbalance",
        nbins=bins,
        title="Imbalance Histogram"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Correlation heatmap
    st.subheader("Correlation: Volume & Prices")
    corr = df[[
        "Total_Actual", "Total_Traded", "Imbalance",
        "Spot price NO2", "Imbalance price NO2"
    ]].resample("D").mean().dropna().corr()
    fig3 = px.imshow(
        corr,
        text_auto=True,
        title="Daily Correlation Matrix"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Download monthly summary CSV
    summary = df.resample("M").agg({
        "Total_Actual": "sum",
        "Total_Traded": "sum",
        "Imbalance": "sum"
    }).reset_index().rename(columns={"index": "Date"})
    csv = summary.to_csv(index=False).encode("utf-8")
    st.subheader("Download Monthly Volume Summary")
    st.download_button(
        "📥 Download CSV",
        data=csv,
        file_name="monthly_volume_summary.csv",
        mime="text/csv"
    )
