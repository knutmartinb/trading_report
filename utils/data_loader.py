import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, engine="openpyxl", parse_dates=["date/time"])
    df = df.set_index("date/time").sort_index()
    # ensure numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df
