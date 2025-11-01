"""
BudgetBuddy AI - Multi-Agent Financial Planner
Streamlit Dashboard for User Interaction
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys

# Import agents
from agents.tracker_agent import TrackerAgent
from agents.advisor_agent import AdvisorAgent
from agents.visualizer_agent import VisualizerAgent
from agents.database import DatabaseManager


# Page configuration
st.set_page_config(
    page_title="BudgetBuddy AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tracker' not in st.session_state:
    st.session_state.tracker = TrackerAgent()
if 'advisor' not in st.session_state:
    st.session_state.advisor = AdvisorAgent()
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = VisualizerAgent()
if 'db' not in st.session_state:
    st.session_state.db = DatabaseManager()


def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 BudgetBuddy AI</h1>', unsafe_allow_html=True)
    st.markdown("### Your Intelligent Multi-Agent Financial Planner")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["🏠 Home", "📊 Add Expenses", "📈 View Analysis", "🎯 Financial Advice", "📉 Visualizations"]
        )
        
        st.markdown("---")
        st.header("ℹ️ About")
        st.info("""
        BudgetBuddy AI uses three intelligent agents:
        1. **Tracker Agent**: Manages expense data
        2. **Advisor Agent**: Provides AI-powered financial advice
        3. **Visualizer Agent**: Creates insightful charts
        """)
    
    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "📊 Add Expenses":
        show_add_expenses_page()
    elif page == "📈 View Analysis":
        show_analysis_page()
    elif page == "🎯 Financial Advice":
        show_advice_page()
    elif page == "📉 Visualizations":
        show_visualizations_page()


def show_home_page():
    """Display home page with overview"""
    col1, col2, col3 = st.columns(3)
    
    # Get summary statistics
    all_expenses = st.session_state.db.get_all_expenses()
    
    with col1:
        total_spent = all_expenses['amount'].sum() if not all_expenses.empty else 0
        st.metric("💵 Total Spent", f"₹{total_spent:.2f}")
    
    with col2:
        num_transactions = len(all_expenses) if not all_expenses.empty else 0
        st.metric("📝 Transactions", num_transactions)
    
    with col3:
        avg_transaction = (all_expenses['amount'].mean() if not all_expenses.empty else 0)
        st.metric("📊 Avg Transaction", f"₹{avg_transaction:.2f}")
    
    st.markdown("---")
    
    # Quick stats
    if not all_expenses.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Spending by Category")
            category_summary = st.session_state.db.get_category_summary()
            st.dataframe(category_summary, use_container_width=True)
        
        with col2:
            st.subheader("📅 Recent Expenses")
            recent_expenses = all_expenses.head(10)
            st.dataframe(recent_expenses[['date', 'description', 'amount', 'category']], use_container_width=True)
    else:
        st.info("👋 Welcome to BudgetBuddy AI! Start by adding your expenses using the 'Add Expenses' page.")


def show_add_expenses_page():
    """Display page for adding expenses"""
    st.header("📊 Add Your Expenses")
    
    tab1, tab2 = st.tabs(["📄 Upload CSV", "✍️ Manual Entry"])
    
    with tab1:
        st.subheader("Upload CSV File")
        st.markdown("**Supported formats:** CSV files with columns: date, description, amount, category")
        
        uploaded_files = st.file_uploader(
            "Choose CSV file(s)",
            type=['csv'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            if st.button("📤 Upload & Process"):
                total_processed = 0
                for file in uploaded_files:
                    try:
                        df, count = st.session_state.tracker.process_and_store_csv(file)
                        total_processed += count
                        st.success(f"✅ Processed {count} expenses from {file.name}")
                    except Exception as e:
                        st.error(f"❌ Error processing {file.name}: {str(e)}")
                
                if total_processed > 0:
                    st.balloons()
                    st.success(f"🎉 Successfully added {total_processed} expenses to your database!")
    
    with tab2:
        st.subheader("Manual Expense Entry")
        
        with st.form("manual_expense_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                expense_date = st.date_input("📅 Date", value=datetime.now().date())
                amount = st.number_input("💵 Amount", min_value=0.01, step=0.01, format="%.2f")
            
            with col2:
                category = st.selectbox(
                    "📂 Category",
                    ["Food", "Transport", "Entertainment", "Utilities", "Shopping", "Health", "Other", "Uncategorized"]
                )
            
            description = st.text_input("📝 Description")
            
            submitted = st.form_submit_button("💾 Add Expense")
            
            if submitted:
                if not description:
                    st.warning("⚠️ Please provide a description for the expense.")
                else:
                    try:
                        st.session_state.tracker.add_manual_expense(
                            expense_date.strftime('%Y-%m-%d'),
                            description,
                            amount,
                            category
                        )
                        st.success(f"✅ Expense added successfully!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error adding expense: {str(e)}")


def show_analysis_page():
    """Display page for viewing analysis"""
    st.header("📈 Spending Analysis")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now().replace(day=1).date())
    with col2:
        end_date = st.date_input("End Date", value=datetime.now().date())
    
    if st.button("🔍 Analyze"):
        # Get expenses for the period
        all_expenses = st.session_state.db.get_all_expenses()
        
        if not all_expenses.empty:
            # Filter by date range
            all_expenses['date'] = pd.to_datetime(all_expenses['date'])
            filtered_expenses = all_expenses[
                (all_expenses['date'].dt.date >= start_date) &
                (all_expenses['date'].dt.date <= end_date)
            ]
            
            if not filtered_expenses.empty:
                # Perform analysis
                analysis_result = st.session_state.advisor.analyze_spending_patterns(filtered_expenses)
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("💵 Total Spent", f"₹{analysis_result['total_spent']:.2f}")
                
                with col2:
                    st.metric("📊 Avg Daily", f"₹{analysis_result['average_daily']:.2f}")
                
                with col3:
                    st.metric("📝 Transactions", analysis_result['num_transactions'])
                
                with col4:
                    st.metric("🏆 Top Category", analysis_result['top_category'] or "N/A")
                
                st.markdown("---")
                
                # Agent-detected trends
                if analysis_result.get('trends'):
                    st.markdown("---")
                    st.subheader("📈 Spending Trends")
                    for trend in analysis_result['trends']:
                        if "Increasing" in trend:
                            st.warning(f"🔺 {trend}")
                        else:
                            st.success(f"🔻 {trend}")
                
                # Agent insights
                if analysis_result.get('insights'):
                    st.markdown("---")
                    st.subheader("🧠 Key Insights")
                    for insight in analysis_result['insights']:
                        st.info(f"📌 {insight}")
                
                # Category breakdown
                st.markdown("---")
                st.subheader("📊 Category Breakdown")
                category_df = pd.DataFrame([
                    {'Category': cat, 'Amount': amt, 
                     'Percentage': f"{(amt/analysis_result['total_spent']*100):.1f}%"}
                    for cat, amt in sorted(analysis_result['category_breakdown'].items(),
                                         key=lambda x: x[1], reverse=True)
                ])
                st.dataframe(category_df, use_container_width=True, hide_index=True)
                
                # Overspending detection
                st.markdown("---")
                overspending = st.session_state.advisor.detect_overspending(
                    analysis_result['category_breakdown']
                )
                
                if overspending:
                    st.subheader("⚠️ Overspending Alerts")
                    for item in overspending:
                        st.warning(f"**{item['category']}**: {item['percentage']:.1f}% of total spending (₹{item['amount']:.2f})")
                else:
                    st.success("✅ No significant overspending detected!")
            else:
                st.info("No expenses found for the selected date range.")
        else:
            st.info("No expenses in database. Please add expenses first.")


def show_advice_page():
    """Display page for AI-powered financial advice"""
    st.header("🎯 AI-Powered Financial Advice")
    
    st.markdown("Get intelligent insights and recommendations from BudgetBuddy's AI advisor.")
    
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Year", range(2020, datetime.now().year + 2), index=datetime.now().year - 2020)
    with col2:
        month = st.selectbox("Month", range(1, 13), index=datetime.now().month - 1)
    
    if st.button("🤖 Generate AI Advice"):
        with st.spinner("Analyzing your spending patterns with AI..."):
            # Get expenses for the month
            expenses = st.session_state.db.get_expenses_by_month(year, month)
            
            if not expenses.empty:
                # Generate comprehensive analysis
                analysis = st.session_state.advisor.provide_monthly_analysis(expenses, year, month)
                
                # Display AI advice
                st.markdown("### 💡 AI Financial Insights")
                st.markdown(analysis['ai_advice'])
                
                st.markdown("---")
                
                # Saving tips
                if analysis['saving_tips']:
                    st.subheader("💡 Actionable Saving Tips")
                    for tip in analysis['saving_tips']:
                        st.info(tip)
                
                st.markdown("---")
                
                # Store advice
                st.session_state.db.insert_advice(analysis['ai_advice'])
                st.success("✅ Advice saved to your history!")
            else:
                st.warning(f"No expenses found for {month}/{year}. Please add expenses first.")
    
    # Show recent advice history
    st.markdown("---")
    st.subheader("📜 Recent Advice History")
    recent_advice = st.session_state.db.get_recent_advice(limit=5)
    if not recent_advice.empty:
        for idx, row in recent_advice.iterrows():
            with st.expander(f"Advice from {row['generated_at']}"):
                st.write(row['text'])
    else:
        st.info("No advice history yet. Generate your first advice to see it here.")


def show_visualizations_page():
    """Display page for visualizations"""
    st.header("📉 Spending Visualizations")
    
    # Get all expenses
    all_expenses = st.session_state.db.get_all_expenses()
    
    if all_expenses.empty:
        st.info("No expenses to visualize. Please add expenses first.")
        return
    
    # Visualization options
    viz_option = st.selectbox(
        "Choose a visualization:",
        ["Dashboard View", "Pie Chart", "Bar Chart", "Time Series", "Daily Spending", "Trend Analysis"]
    )
    
    if viz_option == "Dashboard View":
        st.subheader("📊 Comprehensive Dashboard")
        figures = st.session_state.visualizer.create_summary_dashboard(all_expenses)
        for fig in figures:
            st.pyplot(fig)
    
    elif viz_option == "Pie Chart":
        st.subheader("🥧 Spending by Category (Pie Chart)")
        fig = st.session_state.visualizer.create_category_pie_chart(all_expenses)
        st.pyplot(fig)
    
    elif viz_option == "Bar Chart":
        st.subheader("📊 Spending by Category (Bar Chart)")
        fig = st.session_state.visualizer.create_category_bar_chart(all_expenses)
        st.pyplot(fig)
    
    elif viz_option == "Time Series":
        st.subheader("📈 Spending Over Time")
        fig = st.session_state.visualizer.create_time_series_chart(all_expenses)
        st.pyplot(fig)
    
    elif viz_option == "Daily Spending":
        st.subheader("📅 Daily Spending Breakdown")
        fig = st.session_state.visualizer.create_daily_spending_chart(all_expenses)
        st.pyplot(fig)
    
    elif viz_option == "Trend Analysis":
        st.subheader("📉 Trend Analysis")
        categories = st.session_state.db.get_category_summary()['category'].tolist()
        if categories:
            selected_category = st.selectbox("Select Category", ["All"] + categories)
            category = None if selected_category == "All" else selected_category
            fig = st.session_state.visualizer.create_trend_analysis(all_expenses, category)
            st.pyplot(fig)
        else:
            st.info("No categories available for trend analysis.")


if __name__ == "__main__":
    main()
