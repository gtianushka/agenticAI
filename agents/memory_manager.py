import sqlite3
import pandas as pd
import os

DB_PATH = "database/budgetbuddy.db"
os.makedirs("database", exist_ok=True)

def store_analysis(df, advice):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("expenses", conn, if_exists="append", index=False)
    conn.execute("CREATE TABLE IF NOT EXISTS advice (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")
    conn.execute("INSERT INTO advice (text) VALUES (?)", (advice,))
    conn.commit()
    conn.close()

def load_past_data():
    conn = sqlite3.connect(DB_PATH)
    try:
        advices = pd.read_sql("SELECT * FROM advice", conn)
        return advices.tail(5)
    except:
        return "No previous data found."
