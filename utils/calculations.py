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
    Calculate aggregated volumes and financial metrics for a given timeframe.

    Returns a dict with keys:
      - Total Consumption (MWh)
      - Total Traded (MWh)
      - Total Imbalance (MWh)
      - Positive Imbalance (MWh)
      - Negative Imbalance (MWh)
      - Imbalance Cost to Buy (€)
      - Imbalance Cost to Sell (€)
      - Total Income on Traded (€)
      - Total Cost (€)

    Imbalance Cost to Buy: Σ((Imbalance price NO2 - Spot price NO2) × Imbalance) for Imbalance>0
    Imbalance Cost to Sell: Σ((Spot price NO2 - Imbalance price NO2) × |Imbalance|) for Imbalance<0
    Total Income on Traded: Σ(Spot price NO2 × Total_Traded)
    Total Cost: Total Income on Traded - Imbalance Cost to Buy - Imbalance Cost to Sell
    """
    # Ensure imbalance columns exist
    df_calc = compute_imbalance(df)

    # Aggregate volumes
    total_consumption = df_calc["Total_Actual"].sum()
    total_traded     = df_calc["Total_Traded"].sum()
    total_imbalance  = df_calc["Imbalance"].abs().sum()
    pos_imbalance    = df_calc.loc[df_calc["Imbalance"] > 0, "Imbalance"].sum()
    neg_imbalance    = df_calc.loc[df_calc["Imbalance"] < 0, "Imbalance"].sum()

    # Cost to buy imbalance (when Imbalance>0)
    buy_df = df_calc[df_calc["Imbalance"] > 0]
    cost_buy = ((buy_df["Imbalance price NO2"] - buy_df["Spot price NO2"]) * buy_df["Imbalance"]).sum()

    # Revenue from sell imbalance (when Imbalance<0)
    sell_df = df_calc[df_calc["Imbalance"] < 0]
    cost_sell = ((sell_df["Spot price NO2"] - sell_df["Imbalance price NO2"]) * (-sell_df["Imbalance"]) ).sum()

    # Income from traded volume at spot price
    total_income = (df_calc["Total_Traded"] * df_calc["Spot price NO2"]).sum()

    # Net cost/income
    total_cost = total_income - cost_buy - cost_sell

    return {
        "Total Consumption (MWh)":    total_consumption,
        "Total Traded (MWh)":         total_traded,
        "Total Imbalance (MWh)":      total_imbalance,
        "Positive Imbalance (MWh)":   pos_imbalance,
        "Negative Imbalance (MWh)":   neg_imbalance,
        "Imbalance Cost to Buy (€)":   cost_buy,
        "Imbalance Cost to Sell (€)":  cost_sell,
        "Total Income on Traded (€)": total_income,
        "Total Cost (€)":             total_cost,
    }
