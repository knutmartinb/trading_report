# apps/calculations.py

import streamlit as st

def app():
    st.title("Calculation Details")

    st.markdown(r"""
Below is a thorough breakdown of every metric and formula used in this dashboard.

---

## 1) Volumes

- **Total Consumption (MWh)**  
  $\displaystyle \sum\bigl(\text{Actual consumption residual NO2} + \text{Actual consumption commercial NO2}\bigr)$

- **Total Traded in Day Ahead (MWh)**  
  $\displaystyle \sum\bigl(\text{Traded volume residual NO2} + \text{Traded volume commercial NO2}\bigr)$

- **Imbalance (MWh)**  
  $\displaystyle \text{Total Actual} - \text{Total Traded}$

- **Total Imbalance (MWh)**  
  $\displaystyle \sum\bigl|\text{Imbalance}\bigr|$

- **Positive Imbalance (MWh)**  
  $\displaystyle \sum\bigl(\text{Imbalance}\mid \text{Imbalance}>0\bigr)$

- **Negative Imbalance (MWh)**  
  $\displaystyle \sum\bigl(\text{Imbalance}\mid \text{Imbalance}<0\bigr)$

---

## 2) Prices & Income

- **Trade Income (€)**  
  $\displaystyle \sum\bigl(\text{Spot price NO2}\times \text{Total Traded in Day Ahead}\bigr)$

---

## 3) Profit / Loss on Imbalance

Both use the same per-unit spread times the imbalance magnitude:

- **Profit/Loss on Imbalance Buy (€)**  
  When Imbalance > 0 (you needed extra volume):  
  $$\displaystyle \sum\bigl(\text{Spot price NO2} - \text{Imbalance price NO2}\bigr)\times\bigl(-\,\text{Imbalance}\bigr)\quad(\text{Imbalance}>0)$$

- **Profit/Loss on Imbalance Sell (€)**  
  When Imbalance < 0 (you had surplus to sell):  
  $$\displaystyle \sum\bigl(\text{Spot price NO2} - \text{Imbalance price NO2}\bigr)\times\bigl(-\,\text{Imbalance}\bigr)\quad(\text{Imbalance}<0)$$

---

## 4) Total Cost

Defined as:  
$$
\displaystyle
\text{Total Cost}
= -\bigl(\text{Spot price NO2}\times \text{Total Traded in Day Ahead}\bigr)
\;+\;\text{Profit/Loss on Imbalance Sell}
\;+\;\text{Profit/Loss on Imbalance Buy}
$$

---

## 5) Total Result

Finally:  
$$
\displaystyle
\text{Total Result}
= \text{Trade Income} + \text{Total Cost}
$$

This is the ultimate P&L over your selected period.
""", unsafe_allow_html=False)
