import pandas as pd

def compute_imbalance(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # total consumption & traded
    df["Total_Actual"] = df["Actual consumption residual NO2"] + df["Actual consumption commercial NO2"]
    df["Total_Traded"] = df["Traded volume residual NO2"] + df["Traded volume commercial NO2"]
    # imbalance = actual - traded
    df["Imbalance"] = df["Total_Actual"] - df["Total_Traded"]
    # cost: positive = buy at imbalance price, negative = sell
    df["Cost"] = df["Imbalance"] * df["Imbalance price NO2"]
    return df

def aggregate_kpis(df: pd.DataFrame) -> dict:
    total_consumption = df["Total_Actual"].sum()
    total_traded = df["Total_Traded"].sum()
    total_imbalance = (df["Imbalance"].abs()).sum()
    positive_imb = df.loc[df["Imbalance"] > 0, "Imbalance"].sum()
    negative_imb = df.loc[df["Imbalance"] < 0, "Imbalance"].sum()
    cost_positive = (df.loc[df["Imbalance"] > 0, "Cost"]).sum()
    revenue_negative = (df.loc[df["Imbalance"] < 0, "Cost"]).sum()
    return {
        "Total Consumption (MWh)": total_consumption,
        "Total Traded (MWh)": total_traded,
        "Total Imbalance (MWh)": total_imbalance,
        "Positive Imbalance (MWh)": positive_imb,
        "Negative Imbalance (MWh)": negative_imb,
        "Cost to Buy (€)": cost_positive,
        "Revenue from Sell (€)": revenue_negative,
    }
