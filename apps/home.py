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
    dates = df_calc.index.normalize()
    unique_dates = pd.Index(dates.unique()).sort_values()
    if len(unique_dates) < 7:
        st.warning(f"Not enough days of data (found {len(unique_dates)}).")
        return
    last7 = unique_dates[-7:]
    last_week = df_calc[df_calc.index.normalize().isin(last7)]

    # Financial summary
    fin7 = compute_financials(last_week)

    # Display period
    st.markdown(f":calendar: **Period:** {last7[0].date()} → {last7[-1].date()}" )

    # 1) Price Time Series
    st.subheader("Spot vs Imbalance Price (Last 7 Days)")
    price_df = last_week.resample('H').mean()[['Spot price NO2', 'Imbalance price NO2']]
    fig_price = px.line(
        price_df,
        labels={'value': '€/MWh', 'index': 'Date'},
        title='Hourly Spot and Imbalance Price'
    )
    # Remove default grid
    fig_price.update_xaxes(showgrid=False)
    fig_price.update_yaxes(showgrid=False)

    # Build custom grid lines via shapes
    ymin = price_df.min().min() * 0.9
    ymax = price_df.max().max() * 1.1
    shapes = []
    # Solid lines at each day boundary
    for day in pd.date_range(last7[0], last7[-1] + pd.Timedelta(days=1), freq='D'):
        shapes.append(dict(
            type='line', x0=day, x1=day, y0=ymin, y1=ymax,
            xref='x', yref='y',
            line=dict(color='LightGray', width=1)
        ))
    # Dotted lines at each hour
    start_hr = price_df.index.min().floor('H')
    end_hr = price_df.index.max().ceil('H')
    for hr in pd.date_range(start_hr, end_hr, freq='H'):
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
        ("Positive Imbalance (MWh)",  fin7["Positive Imbalance (MWh)"], "Consumption > Traded."),
        ("Negative Imbalance (MWh)",  fin7["Negative Imbalance (MWh)"], "Traded > Consumption."),
    ]
    cols1 = st.columns(3)
    for col, (label, val, desc) in zip(cols1, vols):
        color = "red" if val < 0 else "green"
        col.markdown(f"**{label}**")
        col.markdown(f"<h3 style='color:{color}; margin:0;'>{val:,.2f}</h3>", unsafe_allow_html=True)
        col.caption(desc)

    # 3) Imbalance Costs Section
    st.subheader("Imbalance Costs (€)")
    costs = [
        ("Imbalance Cost to Buy (€)",  fin7["Imbalance Cost to Buy (€)"],  "Cost when consumption > traded."),
        ("Imbalance Cost to Sell (€)", fin7["Imbalance Cost to Sell (€)"], "Revenue when traded > consumption."),
        ("Total Cost (€)",             fin7["Total Cost (€)"],             "Net = Trade Income - Buy Cost - Sell Revenue"),
    ]
    cols2 = st.columns(3)
    for col, (label, val, desc) in zip(cols2, costs):
        color = "red" if val < 0 else "green"
        col.markdown(f"**{label}**")
        col.markdown(f"<h3 style='color:{color}; margin:0;'>€{val:,.2f}</h3>", unsafe_allow_html=True)
        col.caption(desc)

    # 4) Trade Income Section
    st.subheader("Trade Income (€)")
    income = fin7["Total Income on Traded (€)"]
    inc_color = "red" if income < 0 else "green"
    st.markdown(f"<h3 style='color:{inc_color};'>€{income:,.2f}</h3>", unsafe_allow_html=True)
    st.caption("Total income from sold volume at spot price.")

    # 5) Total Result Section
    st.subheader("Total Result (€)")
    total_cost = fin7["Total Cost (€)"]
    total_result = income - total_cost
    res_color = "red" if total_result < 0 else "green"
    st.markdown(f"<h3 style='color:{res_color};'>€{total_result:,.2f}</h3>", unsafe_allow_html=True)
    st.caption("Trade Income - Total Cost = Net Result")

    st.markdown("---")
    st.info(":information: Use the sidebar to explore detailed Price and Volume analyses.")
