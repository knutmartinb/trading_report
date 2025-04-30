import streamlit as st
from utils.calculations import compute_imbalance, aggregate_kpis

df = st.session_state.get("df")
if df is None:
    st.error("Data not found.")
    st.stop()

st.title("Key Performance Indicators (KPIs)")
df_calc = compute_imbalance(df)
kpis = aggregate_kpis(df_calc)

cols = st.columns(3)
for idx, (name, val) in enumerate(kpis.items()):
    with cols[idx % 3]:
        st.metric(label=name, value=f"{val:,.2f}")
        
st.markdown(
    """
- **Total Imbalance** is the absolute difference between consumption and traded volumes.
- **Cost to Buy** is when consumption exceeded traded; **Revenue from Sell** is when traded exceeded consumption.
"""
)
