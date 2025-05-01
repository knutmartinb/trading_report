# app.py

import streamlit as st
from utils.data_loader import load_data
from apps.home import app as home_app
from apps.price_analysis import app as price_app
from apps.volume_analysis import app as volume_app
from apps.kpis import app as kpis_app
from apps.calculations import app as calc_app

# 1) First Streamlit call
st.set_page_config(
     page_title="Högson Commodities Analytics",
     page_icon="assets/favicon.png",
     layout="wide",
)
# — Custom styling for Högson Commodities —
st.markdown(
    """
    <style>
      /* Gradient header */
      header[data-testid="stHeader"] {
        background: linear-gradient(90deg, #003366, #D4AF37);
      }
      /* Sidebar drop-shadow */
      section[data-testid="stSidebar"] {
        box-shadow: 2px 0 5px rgba(0,0,0,0.1);
      }
      /* Hide default menu & footer */
      #MainMenu, footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# (Optional) Load brand font
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
    <style> * { font-family: 'Open Sans', sans-serif; } </style>
    """,
    unsafe_allow_html=True,
)


# 2) Load & cache data once
@st.cache_data
def get_data():
    return load_data("data/data_dashboard_poc.xlsx")

df = get_data()
st.session_state.df = df

# 3) Sidebar navigation
pages = ["Home", "Price Analysis", "Volume Analysis", "KPIs", "Calculations"]
# Branding logo at top of sidebar
st.sidebar.image("assets/logo.png", width=200)
st.sidebar.markdown("---")

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", pages, key="page_selection")

# 4) Date‐range filter (only on analysis/KPIs pages)
if selection not in ["Home", "Calculations"]:
    dr = st.sidebar.date_input(
        "Select date range",
        [df.index.min().date(), df.index.max().date()],
        key="date_filter"
    )
    filtered = df.loc[dr[0] : dr[1]]
    st.session_state.df = filtered

# 5) Render the selected page
if selection == "Home":
    home_app()
elif selection == "Price Analysis":
    price_app()
elif selection == "Volume Analysis":
    volume_app()
elif selection == "KPIs":
    kpis_app()
elif selection == "Calculations":
    calc_app()
