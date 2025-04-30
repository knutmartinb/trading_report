import streamlit as st
import plotly.express as px

df = st.session_state.get("df")
if df is None:
    st.error("Data not found – load via `app.py`.")
    st.stop()

st.title("Price Analysis")

fig = px.line(
    df,
    y=["Spot price NO2", "Imbalance price NO2"],
    labels={"value": "€/MWh", "date/time": "Date"},
    title="Spot vs. Imbalance Price"
)
st.plotly_chart(fig, use_container_width=True)
