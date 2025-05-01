import streamlit as st
from utils.data_loader import load_data
from apps.home import app as home_app
from apps.price_analysis import app as price_app
from apps.volume_analysis import app as volume_app
from apps.kpis import app as kpis_app
from apps.calculations import app as calc_app
from streamlit_option_menu import option_menu

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

# 3) Sidebar navigation with streamlit-option-menu
pages = ["Home", "Price Analysis", "Volume Analysis", "KPIs", "Calculations"]
with st.sidebar:
    st.image("assets/logo.png", width=200)
    st.markdown("---")
    selection = option_menu(
        menu_title=None,
        options=pages,
        icons=["house", "currency-dollar", "bar-chart-line", "speedometer", "calculator"],
        menu_icon="grid-fill",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#FFFFFF"},
            "icon":     {"color": "#003366", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "4px 0",
                "--hover-color": "#F5F7FA"
            },
            "nav-link-selected": {
                "background-color": "#003366",
                "color": "white"
            },
        }
    )

# 4) Date-range filter (only on analysis/KPIs pages)
if selection not in ["Home", "Calculations"]:
    dr = st.sidebar.date_input(
        "Select date range",
        [df.index.min().date(), df.index.max().date()],
        key="date_filter"
    )
    filtered = df.loc[dr[0]: dr[1]]
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
