PPT link : https://docs.google.com/presentation/d/1XjiFQYI1GXnNBsl9Zwp-liq1R167tBPCYHGZ5yESN2s/edit?usp=sharing
# 🤖 BudgetBuddy AI - Multi-Agent Financial Planner

BudgetBuddy AI is an intelligent financial planning application that uses a multi-agent system to help users track expenses, analyze spending patterns, and receive AI-powered financial advice. Built with Python, LangChain, Hugging Face Transformers, and Matplotlib.

## ✨ Features

- **📊 Tracker Agent**: Easily upload expense CSVs or manually enter expenses
- **🧠 Advisor Agent**: AI-powered financial insights using Hugging Face models
- **📈 Visualizer Agent**: Beautiful charts and visualizations of your spending
- **💾 SQLite Database**: Secure local storage of all financial data
- **🎯 Streamlit Dashboard**: Intuitive web interface for managing your finances

## 🏗️ System Architecture

BudgetBuddy AI consists of three specialized agents working together:

### 1. Tracker Agent (`agents/tracker_agent.py`)
- **Responsibilities**: Expense input and data management
- **Features**:
  - Parse and validate CSV expense files
  - Manual expense entry
  - Store expenses in SQLite database
  - Retrieve expenses by date range
  - Category summary generation

### 2. Advisor Agent (`agents/advisor_agent.py`)
- **Responsibilities**: Financial analysis and AI-powered advice
- **Features**:
  - Spending pattern analysis
  - Overspending detection (configurable thresholds)
  - AI-powered advice generation using Hugging Face models
  - Saving tips generation
  - Support for multiple AI models:
    - `facebook/bart-large-cnn` (default, summarization)
    - `t5-base` (text-to-text generation)
    - `google/flan-t5-base` (alternative option)
  - Rule-based fallback when AI models are unavailable

### 3. Visualizer Agent (`agents/visualizer_agent.py`)
- **Responsibilities**: Data visualization and insights
- **Features**:
  - Pie charts (category spending breakdown)
  - Bar charts (horizontal category comparison)
  - Time series charts (spending trends over time)
  - Daily spending charts (with average line)
  - Trend analysis (category-specific or overall)
  - Comprehensive dashboard view

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for downloading AI models on first run)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd BudgetBuddy-AI
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   The database will be automatically created when you first run the application.

## 🎮 Usage

### Starting the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

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

**Supported column name variations:**
- Amount: `amount`, `amt`, `cost`, `price`
- Description: `description`, `desc`, `detail`, `item`, `name`
- Category: `category`, `cat`, `type`
- Date: `date`, `timestamp`

## 🤖 AI Models

BudgetBuddy AI uses Hugging Face Transformers for generating financial advice:

### Recommended Models

1. **facebook/bart-large-cnn** (Default)
   - Fine-tuned for summarization tasks
   - Best for concise financial advice
   - ~550MB download

2. **google/flan-t5-base**
   - General-purpose text generation
   - Good balance of performance and size
   - ~850MB download

3. **t5-base**
   - Text-to-text transfer transformer
   - Versatile for various tasks
   - ~850MB download

**Note**: Models are downloaded automatically on first use. Ensure you have sufficient disk space and internet bandwidth.

## 🗂️ Database Schema

The application uses SQLite with three main tables:

### `expenses` table
- `id`: Primary key (auto-increment)
- `date`: Date of expense
- `description`: Expense description
- `amount`: Amount spent
- `category`: Expense category
- `created_at`: Timestamp

### `advice` table
- `id`: Primary key (auto-increment)
- `text`: AI-generated advice text
- `generated_at`: Timestamp

### `monthly_summaries` table
- `id`: Primary key (auto-increment)
- `month`: Month identifier
- `total_amount`: Total spending for the month
- `category_breakdown`: JSON string of category totals
- `created_at`: Timestamp

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

## 🔧 Configuration

### Customizing AI Models

Edit `agents/advisor_agent.py` to change the default model:

```python
# In the AdvisorAgent.__init__ method
def __init__(self, model_name="facebook/bart-large-cnn"):
    # Change model_name to your preferred model
```

Available options: `"facebook/bart-large-cnn"`, `"google/flan-t5-base"`, `"t5-base"`

### Adjusting Overspending Threshold

Edit `agents/advisor_agent.py`:

```python
# In the detect_overspending method
def detect_overspending(self, category_breakdown, threshold_percentage=30):
    # Change 30 to your desired threshold (e.g., 25, 35, 40)
```

### Changing Chart Styles

Edit `agents/visualizer_agent.py`:

```python
# In the VisualizerAgent.__init__ method
def __init__(self, figsize=(10, 6), style='seaborn-v0_8'):
    # Change figsize or style to customize charts
```

## 🐛 Troubleshooting

### Issue: AI model download fails

**Solution**: Models download on first use. Ensure you have:
- Stable internet connection
- Sufficient disk space (~2GB recommended)
- Permission to write to the Hugging Face cache directory

### Issue: Database errors

**Solution**: Delete the database folder and restart:
```bash
rm -rf database/
streamlit run app.py
```

### Issue: Import errors

**Solution**: Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Streamlit not starting

**Solution**: Check if port 8501 is available:
```bash
# On macOS/Linux
lsof -ti:8501 | xargs kill

# On Windows
netstat -ano | findstr :8501
```

## 🧪 Testing with Sample Data

Use the provided sample CSV files to test the application:

```bash
# The application includes sample data in data/sample_expenses.csv
# Upload this file from the "Add Expenses" page
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [LangChain](https://github.com/hwchase17/langchain) for agent framework concepts
- [Hugging Face](https://huggingface.co/) for transformer models
- [Streamlit](https://streamlit.io/) for the web interface
- [Matplotlib](https://matplotlib.org/) for visualizations

## 📞 Support

For questions, issues, or suggestions, please open an issue on the repository.

---

**Made with ❤️ using Python, LangChain, and Hugging Face Transformers**

