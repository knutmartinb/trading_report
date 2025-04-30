import streamlit as st
from utils.data_loader import load_data
from apps.home           import app as home_app
from apps.price_analysis import app as price_app
from apps.volume_analysis import app as volume_app
from apps.kpis          import app as kpis_app

# 1) Page config
st.set_page_config(page_title="NO2 Analytics Platform", layout="wide")

# 2) Load & cache data once\@@
@st.cache_data
def get_data():
    return load_data("data/data_dashboard_poc.xlsx")

df_full = get_data()

# 3) Sidebar navigation (persisted)
st.sidebar.title("Navigation")
selection = st.sidebar.radio(
    "Go to",
    ["Home", "Price Analysis", "Volume Analysis", "KPIs"],
    index=st.session_state.get("page_index", 0),
    key="page_selection"
)
st.session_state.page_index = ["Home", "Price Analysis", "Volume Analysis", "KPIs"].index(selection)

# 4) Date-range filter for non-Home pages
df = df_full
if selection != "Home":
    st.sidebar.header("Filters")
    date_range = st.sidebar.date_input(
        "Select date range",
        [df_full.index.min().date(), df_full.index.max().date()],
        key="date_filter"
    )
    # Apply filter
    df = df_full.loc[date_range[0]: date_range[1]]
st.session_state.df = df

# 5) Render selected page
if selection == "Home":
    home_app()
elif selection == "Price Analysis":
    price_app()
elif selection == "Volume Analysis":
    volume_app()
else:
    kpis_app()