import pandas as pd

def forecast_next_month(df):
    if df.empty:
        return "Not enough data for forecasting."
    cat_sum = df.groupby("Category")["Amount"].sum()
    avg_expense = cat_sum.mean()
    highest = cat_sum.idxmax()
    return (
        f"Based on your spending trends, your average category expense is ₹{avg_expense:.2f}. "
        f"You tend to spend the most on **{highest}**. "
        "Consider reducing that category by 10% next month to save more!"
    )
