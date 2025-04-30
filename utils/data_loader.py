import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    # read Excel with comma-as-decimal, parse the Date/time column
    df = pd.read_excel(
        path,
        engine="openpyxl",
        decimal=',',
        parse_dates=["Date/time"],
    )
    # strip any leading/trailing spaces in column names
    df.columns = df.columns.str.strip()

    # move the Date/time column into the index
    df = df.set_index("Date/time").sort_index()

    # force everything else to numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
