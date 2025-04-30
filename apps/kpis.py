import streamlit as st
from utils.calculations import compute_financials

def app():
    st.title("Key Performance Indicators")

    # Retrieve dataframe
    df = st.session_state.get("df")
    if df is None:
        st.error("Data not loaded.")
        return

    # Compute metrics
    kpis = compute_financials(df)

    # 1) Total Result
    total_income = kpis["Total Income on Traded (€)"]
    total_cost   = kpis["Total Cost (€)"]
    total_result = total_income - total_cost
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
        "Total Traded (MWh)",
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
        ("Trade Income",        kpis["Total Income on Traded (€)"], "Total income from traded volume at spot price."),
        ("Imbalance Cost to Buy",  kpis["Imbalance Cost to Buy (€)"], "Cost when consumption > traded."),
        ("Imbalance Cost to Sell", kpis["Imbalance Cost to Sell (€)"], "Revenue when traded > consumption."),
        ("Total Cost",            kpis["Total Cost (€)"], "Net = Income - Buy Cost - Sell Revenue"),
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

    # Notes
    st.markdown(
        """
        **Calculation Notes**  
        - **Trade Income** = Σ(Spot price × Total Traded)  
        - **Imbalance Cost to Buy** = Σ((Imbalance price – Spot price) × Imbalance), for Imbalance>0  
        - **Imbalance Cost to Sell** = Σ((Spot price – Imbalance price) × |Imbalance|), for Imbalance<0  
        - **Total Cost** = Trade Income − Imbalance Cost to Buy − Imbalance Cost to Sell
        """
    )
