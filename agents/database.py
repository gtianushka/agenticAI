"""
Database module for BudgetBuddy AI
Handles SQLite database setup and operations for storing expenses
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os


class DatabaseManager:
    """Manages SQLite database operations for BudgetBuddy"""
    
    def __init__(self, db_path="database/budgetbuddy.db"):
        """Initialize database connection"""
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._create_tables()
    
    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Expenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Advice table for storing AI-generated recommendations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS advice (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Monthly summaries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS monthly_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month TEXT NOT NULL,
                total_amount REAL NOT NULL,
                category_breakdown TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def insert_expense(self, date, description, amount, category):
        """Insert a single expense record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO expenses (date, description, amount, category)
            VALUES (?, ?, ?, ?)
        """, (date, description, amount, category))
        
        conn.commit()
        conn.close()
    
    def insert_expenses_batch(self, expenses_df):
        """Insert multiple expenses from a DataFrame"""
        conn = sqlite3.connect(self.db_path)
        
        # Ensure required columns exist
        required_cols = ['date', 'description', 'amount', 'category']
        for col in required_cols:
            if col not in expenses_df.columns:
                raise ValueError(f"DataFrame must contain '{col}' column")
        
        # Clean and prepare data
        expenses_df = expenses_df.copy()
        expenses_df['date'] = pd.to_datetime(expenses_df['date']).dt.strftime('%Y-%m-%d')
        expenses_df['amount'] = pd.to_numeric(expenses_df['amount'], errors='coerce')
        expenses_df = expenses_df.dropna(subset=['amount'])
        
        # Insert into database
        expenses_df[required_cols].to_sql('expenses', conn, if_exists='append', index=False)
        
        conn.close()
    
    def get_all_expenses(self):
        """Retrieve all expenses from database"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM expenses ORDER BY date DESC", conn)
        conn.close()
        return df
    
    def get_expenses_by_month(self, year, month):
        """Get expenses for a specific month"""
        conn = sqlite3.connect(self.db_path)
        
        query = """
            SELECT * FROM expenses 
            WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
            ORDER BY date DESC
        """
        df = pd.read_sql_query(query, conn, params=(str(year), str(month).zfill(2)))
        
        conn.close()
        return df
    
    def get_category_summary(self, year=None, month=None):
        """Get spending summary by category"""
        conn = sqlite3.connect(self.db_path)
        
        if year and month:
            query = """
                SELECT category, SUM(amount) as total, COUNT(*) as count
                FROM expenses
                WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
                GROUP BY category
                ORDER BY total DESC
            """
            df = pd.read_sql_query(query, conn, params=(str(year), str(month).zfill(2)))
        else:
            query = """
                SELECT category, SUM(amount) as total, COUNT(*) as count
                FROM expenses
                GROUP BY category
                ORDER BY total DESC
            """
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        return df
    
    def insert_advice(self, advice_text):
        """Store AI-generated advice"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO advice (text) VALUES (?)", (advice_text,))
        
        conn.commit()
        conn.close()
    
    def get_recent_advice(self, limit=5):
        """Retrieve recent advice records"""
        conn = sqlite3.connect(self.db_path)
        
        try:
            query = f"SELECT * FROM advice ORDER BY generated_at DESC LIMIT {limit}"
            df = pd.read_sql_query(query, conn)
        except Exception as e:
            # Fallback for older database schemas
            try:
                query = f"SELECT * FROM advice ORDER BY id DESC LIMIT {limit}"
                df = pd.read_sql_query(query, conn)
                # Add generated_at if missing
                if 'generated_at' not in df.columns:
                    df['generated_at'] = pd.NaT
            except:
                df = pd.DataFrame()
        
        conn.close()
        return df


