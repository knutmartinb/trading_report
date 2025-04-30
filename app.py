import streamlit as st
from utils.data_loader import load_data

st.set_page_config(page_title="NO₂ Dashboard", layout="wide")
st.title("NO₂ 2024 Analytics Dashboard")

# Load data once
@st.cache_data
def get_data():
    return load_data("data/data_dashboard_poc.xlsx")

df = get_data()

st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Select date range",
    [df.index.min().date(), df.index.max().date()]
)
df = df.loc[date_range[0] : date_range[1]]

st.write("Use the sidebar to navigate pages ▶️")
