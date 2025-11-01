import pandas as pd

def categorize_expenses(df):
    if "Category" not in df.columns:
        df["Category"] = "Uncategorized"

    keywords = {
        "Food": ["restaurant", "groceries", "meal", "snack"],
        "Transport": ["uber", "bus", "train", "fuel"],
        "Entertainment": ["movie", "game", "netflix"],
        "Utilities": ["electricity", "water", "gas", "wifi"],
        "Savings": ["bank", "deposit", "investment"]
    }

    for key, words in keywords.items():
        df.loc[df["Description"].str.lower().str.contains('|'.join(words), na=False), "Category"] = key

    return df
