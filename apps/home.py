import streamlit as st
from utils.calculations import compute_imbalance, compute_financials
import pandas as pd
import plotly.express as px

def app():
    st.title("Home: Last 7 Days Highlights")

    df = st.session_state.get("df")
    if df is None:
        st.error("Data not loaded.")
        return

    # Compute imbalance & get last 7 unique days
    df_calc = compute_imbalance(df)
    unique_dates = pd.Index(df_calc.index.normalize().unique()).sort_values()
    if len(unique_dates) < 7:
        st.warning(f"Not enough days of data (found {len(unique_dates)}).")
        return
    last7 = unique_dates[-7:]
    last_week = df_calc[df_calc.index.normalize().isin(last7)]

    # Financial summary
    fin7 = compute_financials(last_week)

    # Display period
    st.markdown(f":calendar: **Period:** {last7[0].date()} → {last7[-1].date()}")

    # 1) Price Time Series
    st.subheader("Spot vs Imbalance Price (Last 7 Days)")
    price_df = last_week.resample('H').mean()[['Spot price NO2', 'Imbalance price NO2']]
    fig_price = px.line(
        price_df,
        labels={'value': '€/MWh', 'index': 'Date'},
        title='Hourly Spot and Imbalance Price'
    )
    # Build custom grid lines via shapes
    ymin, ymax = price_df.min().min() * 0.9, price_df.max().max() * 1.1
    shapes = []
    for day in pd.date_range(last7[0], last7[-1] + pd.Timedelta(days=1), freq='D'):
        shapes.append(dict(
            type='line', x0=day, x1=day, y0=ymin, y1=ymax,
            xref='x', yref='y', line=dict(color='LightGray', width=1)
        ))
    for hr in pd.date_range(price_df.index.min().floor('H'),
                             price_df.index.max().ceil('H'), freq='H'):
        if hr.normalize() in last7:
            shapes.append(dict(
                type='line', x0=hr, x1=hr, y0=ymin, y1=ymax,
                xref='x', yref='y',
                line=dict(color='LightGray', width=0.5, dash='dot')
            ))
    fig_price.update_layout(shapes=shapes)
    st.plotly_chart(fig_price, use_container_width=True)

    # 2) Volumes Section
    st.subheader("Volumes (MWh)")
    vols = [
        ("Total Imbalance (MWh)",    fin7["Total Imbalance (MWh)"],   "Sum of abs(Actual – Traded)."),
        ("Positive Imbalance (MWh)", fin7["Positive Imbalance (MWh)"], "Consumption > Traded."),
        ("Negative Imbalance (MWh)", fin7["Negative Imbalance (MWh)"], "Traded > Consumption."),
    ]
    cols1 = st.columns(3)
    for col, (label, val, desc) in zip(cols1, vols):
        color = "red" if val < 0 else "green"
        col.markdown(f"**{label}**")
        col.markdown(f"<h3 style='color:{color}; margin:0;'>{val:,.2f}</h3>",
                     unsafe_allow_html=True)
        col.caption(desc)

    # 3) Profit/Loss on Imbalance Section
    st.subheader("Profit/Loss on Imbalance (€)")
    items = [
        ("Profit/Loss on Imbalance Buy (€)",  fin7["Profit/Loss on Imbalance Buy (€)"],
         "= Σ((Spot price – Imbalance price) × (–Imbalance)), Imbalance>0."),
        ("Profit/Loss on Imbalance Sell (€)", fin7["Profit/Loss on Imbalance Sell (€)"],
         "= Σ((Spot price – Imbalance price) × (–Imbalance)), Imbalance<0."),
    ]
    cols2 = st.columns(2)
    for col, (label, val, desc) in zip(cols2, items):
        color = "red" if val < 0 else "green"
        col.markdown(f"**{label}**")
        col.markdown(f"<h3 style='color:{color}; margin:0;'>{val:,.2f}</h3>",
                     unsafe_allow_html=True)
        col.caption(desc)

    # 4) Turnover & Total Cost Section
    turnover = fin7["Total Income on Traded (€)"]
    total_cost = fin7["Total Cost (€)"]
    cols_tc = st.columns(2)

    cols_tc[0].subheader("Turnover (€)")
    color_t = "red" if turnover < 0 else "green"
    cols_tc[0].markdown(f"<h3 style='color:{color_t}; margin:0;'>€{turnover:,.2f}</h3>",
                        unsafe_allow_html=True)
    cols_tc[0].caption("Total income from sold volume at spot price.")

    cols_tc[1].subheader("Total Cost (€)")
    color_c = "red" if total_cost < 0 else "green"
    cols_tc[1].markdown(f"<h3 style='color:{color_c}; margin:0;'>€{total_cost:,.2f}</h3>",
                        unsafe_allow_html=True)
    cols_tc[1].caption("= -(Spot×Traded) + P/L Sell + P/L Buy.")

    # 5) Total Result Section (fixed)
    st.subheader("Total Result (€)")
    total_result = turnover + total_cost
    res_color = "red" if total_result < 0 else "green"
    st.markdown(f"<h3 style='color:{res_color};'>€{total_result:,.2f}</h3>",
                unsafe_allow_html=True)
    st.caption("Turnover + Total Cost = Total Result")

    st.markdown("---")
    st.info(":information: Use the sidebar to explore detailed Price and Volume analyses.")
