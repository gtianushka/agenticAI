"""
Tracker Agent for BudgetBuddy AI
Handles expense input from manual entry or CSV files and stores in database
"""

import pandas as pd
import io
from datetime import datetime
from agents.database import DatabaseManager


def categorize_auto(df):
    """Auto-categorize expenses based on description keywords"""
    keywords = {
        "Food": ["restaurant", "groceries", "meal", "snack", "food", "cafe", "coffee", "starbucks", "dining", "lunch", "dinner"],
        "Transport": ["uber", "bus", "train", "fuel", "taxi", "metro", "flight", "transport", "travel", "ride"],
        "Entertainment": ["movie", "game", "netflix", "cinema", "theater", "entertainment", "spotify", "music"],
        "Utilities": ["electricity", "water", "gas", "wifi", "internet", "mobile", "phone", "utility", "bill"],
        "Shopping": ["amazon", "flipkart", "shopping", "mall", "store", "purchase", "buy", "order"],
        "Health": ["medical", "pharmacy", "hospital", "doctor", "medicine", "health", "clinic"],
        "Education": ["school", "tuition", "course", "education", "university", "book", "study"],
        "Bills": ["electricity", "water", "rent", "insurance", "loan", "emi", "bill"],
        "Savings": ["bank", "deposit", "investment", "sip", "mutual"]
    }
    
    for key, words in keywords.items():
        df.loc[df['description'].str.lower().str.contains('|'.join(words), na=False), 'category'] = key


class TrackerAgent:
    """Agent responsible for tracking and storing user expenses"""
    
    def __init__(self):
        """Initialize the tracker agent with database connection"""
        self.db = DatabaseManager()
    
    def parse_csv_expenses(self, file_input):
        """
        Parse expenses from a CSV file with smart detection
        
        Args:
            file_input: File object or file path
            
        Returns:
            DataFrame with standardized expense data
        """
        try:
            # Handle different input types
            if isinstance(file_input, bytes):
                df = pd.read_csv(io.BytesIO(file_input))
            elif hasattr(file_input, 'read'):
                df = pd.read_csv(file_input)
            else:
                df = pd.read_csv(file_input)
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")
        
        # Normalize column names (case-insensitive)
        df.columns = [c.strip().lower() for c in df.columns]
        
        # Map common column name variations (comprehensive)
        column_mapping = {
            # Amount variations
            'amount': 'amount', 'amt': 'amount', 'cost': 'amount', 'price': 'amount',
            'value': 'amount', 'money': 'amount', 'spending': 'amount', 'expense': 'amount',
            'charge': 'amount', 'fee': 'amount', 'total': 'amount',
            # Description variations
            'desc': 'description', 'detail': 'description', 'item': 'description',
            'name': 'description', 'merchant': 'description', 'vendor': 'description',
            'shop': 'description', 'store': 'description', 'note': 'description',
            # Category variations
            'cat': 'category', 'type': 'category', 'group': 'category',
            'classification': 'category',
            # Date variations
            'date': 'date', 'timestamp': 'date', 'time': 'date', 'dt': 'date',
            'transaction_date': 'date', 'transaction_dt': 'date'
        }
        
        # Rename columns
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns and new_col not in df.columns:
                df = df.rename(columns={old_col: new_col})
        
        # Validate required columns - be flexible
        if 'amount' not in df.columns:
            # Try to find any numeric column as amount
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) > 0:
                # Use first numeric column as amount
                df = df.rename(columns={numeric_cols[0]: 'amount'})
            else:
                raise ValueError(
                    "CSV must contain at least one numeric column for amount. "
                    "Supported columns: amount, amt, cost, price, value, money, spending, expense"
                )
        
        # Clean and convert data
        df = df.dropna(subset=['amount'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df = df.dropna(subset=['amount'])
        
        # Ensure amount is positive (spending)
        df['amount'] = df['amount'].abs()
        
        # Add default values for missing columns
        if 'description' not in df.columns:
            # Use first text column as description
            text_cols = df.select_dtypes(include=['object']).columns
            if len(text_cols) > 0 and text_cols[0] != 'date':
                df = df.rename(columns={text_cols[0]: 'description'})
            else:
                df['description'] = 'No description'
        
        if 'category' not in df.columns:
            # Auto-categorize based on description keywords
            df['category'] = 'Uncategorized'
            categorize_auto(df)
        
        if 'date' not in df.columns:
            df['date'] = datetime.now().strftime('%Y-%m-%d')
        else:
            # Try to parse dates
            try:
                df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            except:
                df['date'] = datetime.now().strftime('%Y-%m-%d')
        
        return df
    
    def store_expenses(self, expenses_df):
        """
        Store expenses in the database
        
        Args:
            expenses_df: DataFrame with expense data
            
        Returns:
            Number of records stored
        """
        if expenses_df.empty:
            return 0
        
        self.db.insert_expenses_batch(expenses_df)
        return len(expenses_df)
    
    def add_manual_expense(self, date, description, amount, category):
        """
        Add a single expense manually
        
        Args:
            date: Date of expense (YYYY-MM-DD)
            description: Description of expense
            amount: Amount spent
            category: Category of expense
            
        Returns:
            True if successful
        """
        self.db.insert_expense(date, description, amount, category)
        return True
    
    def get_all_expenses(self):
        """Retrieve all stored expenses"""
        return self.db.get_all_expenses()
    
    def get_monthly_expenses(self, year=None, month=None):
        """
        Get expenses for a specific month
        
        Args:
            year: Year (defaults to current year)
            month: Month (1-12, defaults to current month)
            
        Returns:
            DataFrame with monthly expenses
        """
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        return self.db.get_expenses_by_month(year, month)
    
    def process_and_store_csv(self, file_input):
        """
        Process CSV file and store expenses in one step
        
        Args:
            file_input: File object or file path
            
        Returns:
            Tuple of (DataFrame, number_of_records_stored)
        """
        df = self.parse_csv_expenses(file_input)
        count = self.store_expenses(df)
        return df, count
