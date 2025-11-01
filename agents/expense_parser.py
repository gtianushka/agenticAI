import pandas as pd
import io

def parse_and_store_expenses(file):
    try:
        df = pd.read_csv(file)
    except:
        df = pd.read_csv(io.StringIO(file.getvalue().decode("utf-8")))
    
    df.columns = [c.strip().capitalize() for c in df.columns]
    if "Amount" not in df.columns:
        raise ValueError("CSV must have an 'Amount' column.")
    
    df = df.dropna(subset=["Amount"])
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna(subset=["Amount"])
    return df
