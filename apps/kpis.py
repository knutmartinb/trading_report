import streamlit as st
from utils.calculations import compute_financials

def app():
    st.title("Key Performance Indicators")

    df = st.session_state.get("df")
    if df is None:
        st.error("Data not loaded.")
        return

    kpis = compute_financials(df)

    # 1) Total Result (fixed)
    total_result = kpis["Total Income on Traded (€)"] + kpis["Total Cost (€)"]
    st.header("Total Result")
    res_color = "green" if total_result >= 0 else "red"
    st.markdown(
        f"<h2 style='color:{res_color};'>€{total_result:,.2f}</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # 2) Volumes Section
    st.header("Volumes (MWh)")
    volume_labels = [
        "Total Consumption (MWh)",
        "Total Traded in Day Ahead (MWh)",
        "Total Imbalance (MWh)",
        "Positive Imbalance (MWh)",
        "Negative Imbalance (MWh)",
    ]
    cols_vol = st.columns(len(volume_labels))
    for idx, label in enumerate(volume_labels):
        val = kpis.get(label, 0)
        cols_vol[idx].metric(label=label, value=f"{val:,.2f}")
    st.markdown("---")

    # 3) Turnover Section
    st.header("Turnover (€)")
    turnover_items = [
        ("Trade Income (€)",              kpis["Total Income on Traded (€)"],        "Total income from sold volume at spot price."),
        ("Profit/Loss on Imbalance Buy (€)",  kpis["Profit/Loss on Imbalance Buy (€)"],    "= Σ((Spot price – Imbalance price) × (–Imbalance)), Imbalance>0 (buy)."),
        ("Profit/Loss on Imbalance Sell (€)", kpis["Profit/Loss on Imbalance Sell (€)"],   "= Σ((Spot price – Imbalance price) × (–Imbalance)), Imbalance<0 (sell)."),
        ("Total Cost (€)",                 kpis["Total Cost (€)"],                    "= -(Spot×Traded) + P/L Sell + P/L Buy."),
    ]
    cols_turn = st.columns(len(turnover_items))
    for idx, (label, val, caption) in enumerate(turnover_items):
        color = "green" if val >= 0 else "red"
        col = cols_turn[idx]
        col.markdown(f"**{label}**")
        col.markdown(
            f"<h3 style='color:{color}; margin:0;'>€{val:,.2f}</h3>",
            unsafe_allow_html=True,
        )
        col.caption(caption)

    # Calculation Notes
    st.markdown(
        """
        **Calculation Notes**  
        - **Trade Income** = Σ(Spot price NO2 × Total Traded in Day Ahead)  
        - **Profit/Loss on Imbalance Buy** = Σ((Spot price – Imbalance price) × (–Imbalance)), for Imbalance > 0  
        - **Profit/Loss on Imbalance Sell** = Σ((Spot price – Imbalance price) × (–Imbalance)), for Imbalance < 0  
        - **Total Cost** = -(Spot price × Total Traded) + Profit/Loss on Imbalance Sell + Profit/Loss on Imbalance Buy
        """
    )
