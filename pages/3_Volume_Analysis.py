import streamlit as st
import plotly.express as px
from utils.calculations import compute_imbalance

df = st.session_state.get("df")
if df is None:
    st.error("Data not found.")
    st.stop()

st.title("Volume Analysis")
df_calc = compute_imbalance(df)

# 1) all four series
fig1 = px.line(
    df_calc,
    y=[
        "Actual consumption residual NO2",
        "Actual consumption commercial NO2",
        "Traded volume residual NO2",
        "Traded volume commercial NO2",
    ],
    labels={"value": "MWh"},
    title="Consumption & Traded Volumes"
)
st.plotly_chart(fig1, use_container_width=True)

# 2) aggregated totals
fig2 = px.line(
    df_calc,
    y=["Total_Actual", "Total_Traded"],
    labels={"value": "MWh"},
    title="Total Consumption vs. Total Traded"
)
st.plotly_chart(fig2, use_container_width=True)
