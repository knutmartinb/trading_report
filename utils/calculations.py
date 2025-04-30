import pandas as pd

def compute_imbalance(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Total_Actual"] = (
        df["Actual consumption residual NO2"]
        + df["Actual consumption commercial NO2"]
    )
    df["Total_Traded"] = (
        df["Traded volume residual NO2"]
        + df["Traded volume commercial NO2"]
    )
    df["Imbalance"] = df["Total_Actual"] - df["Total_Traded"]
    return df

def compute_financials(df: pd.DataFrame) -> dict:
    """
    Returns:
      - Total Consumption (MWh)
      - Total Traded in Day Ahead (MWh)
      - Total Imbalance (MWh)
      - Positive Imbalance (MWh)
      - Negative Imbalance (MWh)
      - Profit/Loss on Imbalance Buy (€)
      - Profit/Loss on Imbalance Sell (€)
      - Total Income on Traded (€)
      - Total Cost (€) = -(Spot price × Total_Traded) + P/L Sell + P/L Buy
    """
    df_calc = compute_imbalance(df)

    # Volumes
    total_consumption = df_calc["Total_Actual"].sum()
    total_traded      = df_calc["Total_Traded"].sum()
    total_imbalance   = df_calc["Imbalance"].abs().sum()
    pos_imbalance     = df_calc.loc[df_calc["Imbalance"] > 0, "Imbalance"].sum()
    neg_imbalance     = df_calc.loc[df_calc["Imbalance"] < 0, "Imbalance"].sum()

    # Profit/Loss on Imbalance Buy: for Imbalance > 0
    buy_df = df_calc[df_calc["Imbalance"] > 0]
    pl_buy = (
        (buy_df["Spot price NO2"] - buy_df["Imbalance price NO2"])
        * (-buy_df["Imbalance"])
    ).sum()

    # Profit/Loss on Imbalance Sell: for Imbalance < 0
    sell_df = df_calc[df_calc["Imbalance"] < 0]
    pl_sell = (
        (sell_df["Spot price NO2"] - sell_df["Imbalance price NO2"])
        * (-sell_df["Imbalance"])
    ).sum()

    # Income at spot price for all traded volume
    total_income = (df_calc["Total_Traded"] * df_calc["Spot price NO2"]).sum()

    # New Total Cost = -(traded*spot) + P/L Sell + P/L Buy
    total_cost = -total_income + pl_sell + pl_buy

    return {
        "Total Consumption (MWh)":         total_consumption,
        "Total Traded in Day Ahead (MWh)": total_traded,
        "Total Imbalance (MWh)":          total_imbalance,
        "Positive Imbalance (MWh)":       pos_imbalance,
        "Negative Imbalance (MWh)":       neg_imbalance,
        "Profit/Loss on Imbalance Buy (€)":  pl_buy,
        "Profit/Loss on Imbalance Sell (€)": pl_sell,
        "Total Income on Traded (€)":     total_income,
        "Total Cost (€)":                 total_cost,
    }
