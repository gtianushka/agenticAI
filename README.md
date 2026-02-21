PPT link : https://docs.google.com/presentation/d/1XjiFQYI1GXnNBsl9Zwp-liq1R167tBPCYHGZ5yESN2s/edit?usp=sharing
# 🤖 BudgetBuddy AI - Multi-Agent Financial Planner

BudgetBuddy AI is an intelligent financial planning application that uses a multi-agent system to help users track expenses, analyze spending patterns, and receive AI-powered financial advice. Built with Python, LangChain, Hugging Face Transformers, and Matplotlib.

### Using BudgetBuddy AI

#### 1. **Home Page** 🏠
- View summary statistics (total spent, transactions, average)
- Quick overview of spending by category
- Recent expenses list

#### 2. **Add Expenses** 📊
- **CSV Upload**: Upload one or more CSV files with columns: `date`, `description`, `amount`, `category`
- **Manual Entry**: Add individual expenses with date, description, amount, and category

#### 3. **View Analysis** 📈
- Analyze spending for a specific date range
- View metrics: total spent, average daily, transaction count, top category
- Category breakdown with percentages
- Overspending alerts for categories exceeding 30% of budget

#### 4. **Financial Advice** 🎯
- Generate AI-powered financial insights
- Select a specific month to analyze
- Receive actionable saving tips
- View history of previous advice

#### 5. **Visualizations** 📉
- **Dashboard View**: Comprehensive overview with multiple charts
- **Pie Chart**: Category spending distribution
- **Bar Chart**: Horizontal category comparison
- **Time Series**: Spending trends over time
- **Daily Spending**: Daily amounts with average line
- **Trend Analysis**: Category-specific or overall trends

## 📊 CSV Format

Your CSV files should have the following columns (case-insensitive):

| Column | Description | Example |
|--------|-------------|---------|
| date | Date of expense | 2025-01-15 or 2025-01-15 |
| description | Description of expense | Groceries |
| amount | Amount spent | 45.99 |
| category | Expense category | Food |



## 📁 Project Structure

```
BudgetBuddy-AI/
├── agents/
│   ├── __init__.py
│   ├── database.py           # Database management
│   ├── tracker_agent.py      # Tracker agent
│   ├── advisor_agent.py      # Advisor agent with AI
│   ├── visualizer_agent.py   # Visualization agent
│   ├── ai_advisor.py         # Legacy AI advisor
│   ├── expense_parser.py     # Expense parsing utilities
│   ├── category_agent.py     # Category classification
│   ├── forecast_agent.py     # Forecasting utilities
│   ├── memory_agent.py       # Memory management
│   ├── memory_manager.py     # Memory utilities
│   └── notifications.py      # Notification functions
├── data/
│   ├── sample_expenses.csv   # Sample data
│   └── combined_expenses.csv # Combined sample data
├── database/
│   └── budgetbuddy.db        # SQLite database (auto-generated)
├── app.py                    # Streamlit application
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```





