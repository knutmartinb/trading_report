import streamlit as st
import pandas as pd

st.title("Home")
st.markdown(
    """
Welcome to your NO₂ 2024 analytics app.  
Use the sidebar filter in **app.py** to select the date range.
"""
)

df = st.session_state.get("df") or st.experimental_memo(lambda: None)  # loaded in app.py
if df is None:
    st.warning("Data not loaded. Please run the app from `app.py`.")
else:
    st.subheader("Raw Data Preview")
    st.dataframe(df.head(100), use_container_width=True)
