"""
Visualizer Agent for BudgetBuddy AI
Creates charts and visualizations for expense analysis using Matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import io


class VisualizerAgent:
    """Agent responsible for creating visual representations of expense data"""
    
    def __init__(self, figsize=(10, 6), style='seaborn-v0_8'):
        """
        Initialize the visualizer agent
        
        Args:
            figsize: Default figure size (width, height)
            style: Matplotlib style
        """
        self.figsize = figsize
        plt.style.use(style)
    
    def create_category_pie_chart(self, expenses_df):
        """
        Create a pie chart showing spending by category
        
        Args:
            expenses_df: DataFrame with expense data
            
        Returns:
            Matplotlib figure
        """
        if expenses_df.empty or 'category' not in expenses_df.columns:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            ax.set_title('Category-wise Spending')
            return fig
        
        # Group by category and sum amounts
        category_totals = expenses_df.groupby('category')['amount'].sum().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create pie chart
        colors = plt.cm.Set3(range(len(category_totals)))
        wedges, texts, autotexts = ax.pie(
            category_totals,
            labels=category_totals.index,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        
        # Style adjustments
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('Spending by Category', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        return fig
    
    def create_category_bar_chart(self, expenses_df):
        """
        Create a bar chart showing spending by category
        
        Args:
            expenses_df: DataFrame with expense data
            
        Returns:
            Matplotlib figure
        """
        if expenses_df.empty or 'category' not in expenses_df.columns:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            ax.set_title('Category-wise Spending')
            return fig
        
        # Group by category and sum amounts
        category_totals = expenses_df.groupby('category')['amount'].sum().sort_values(ascending=True)
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create bar chart
        colors = plt.cm.viridis(range(len(category_totals)) / len(category_totals))
        bars = ax.barh(category_totals.index, category_totals.values, color=colors)
        
        # Add value labels on bars
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2,
                   f'₹{width:.2f}',
                   ha='left', va='center', fontweight='bold')
        
        ax.set_xlabel('Amount (₹)', fontsize=12)
        ax.set_ylabel('Category', fontsize=12)
        ax.set_title('Spending by Category', fontsize=16, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        return fig
    
    def create_time_series_chart(self, expenses_df):
        """
        Create a time series chart showing spending over time
        
        Args:
            expenses_df: DataFrame with expense data
            
        Returns:
            Matplotlib figure
        """
        if expenses_df.empty or 'date' not in expenses_df.columns:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            ax.set_title('Spending Over Time')
            return fig
        
        # Convert date column to datetime
        expenses_df = expenses_df.copy()
        expenses_df['date'] = pd.to_datetime(expenses_df['date'])
        
        # Group by date and sum amounts
        daily_totals = expenses_df.groupby('date')['amount'].sum().sort_index()
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create line chart
        ax.plot(daily_totals.index, daily_totals.values, marker='o', linewidth=2, markersize=8)
        ax.fill_between(daily_totals.index, daily_totals.values, alpha=0.3)
        
        # Formatting
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Amount (₹)', fontsize=12)
        ax.set_title('Spending Over Time', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return fig
    
    def create_daily_spending_chart(self, expenses_df):
        """
        Create a bar chart showing daily spending amounts
        
        Args:
            expenses_df: DataFrame with expense data
            
        Returns:
            Matplotlib figure
        """
        if expenses_df.empty or 'date' not in expenses_df.columns:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            ax.set_title('Daily Spending')
            return fig
        
        # Convert date column to datetime
        expenses_df = expenses_df.copy()
        expenses_df['date'] = pd.to_datetime(expenses_df['date'])
        
        # Group by date and sum amounts
        daily_totals = expenses_df.groupby('date')['amount'].sum().sort_index()
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create bar chart
        ax.bar(daily_totals.index, daily_totals.values, color='steelblue', alpha=0.7)
        
        # Add average line
        avg_spending = daily_totals.mean()
        ax.axhline(y=avg_spending, color='red', linestyle='--', linewidth=2, 
                  label=f'Average: ₹{avg_spending:.2f}')
        
        # Formatting
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Amount (₹)', fontsize=12)
        ax.set_title('Daily Spending', fontsize=16, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.legend()
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return fig
    
    def create_trend_analysis(self, expenses_df, category=None):
        """
        Create a trend analysis chart for a specific category or overall
        
        Args:
            expenses_df: DataFrame with expense data
            category: Optional category to filter by
            
        Returns:
            Matplotlib figure
        """
        if expenses_df.empty or 'date' not in expenses_df.columns:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            ax.set_title('Trend Analysis')
            return fig
        
        # Convert date column to datetime
        expenses_df = expenses_df.copy()
        expenses_df['date'] = pd.to_datetime(expenses_df['date'])
        
        # Filter by category if specified
        if category:
            expenses_df = expenses_df[expenses_df['category'] == category]
        
        # Group by date and category, calculate totals
        if 'category' in expenses_df.columns and not category:
            trend_data = expenses_df.groupby(['date', 'category'])['amount'].sum().unstack(fill_value=0)
        else:
            trend_data = expenses_df.groupby('date')['amount'].sum()
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Plot trend data
        if isinstance(trend_data, pd.DataFrame):
            trend_data.plot(kind='line', ax=ax, marker='o', linewidth=2, markersize=6)
        else:
            ax.plot(trend_data.index, trend_data.values, marker='o', linewidth=2, markersize=6)
        
        # Formatting
        title = f'Trend Analysis' + (f' - {category}' if category else '')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Amount (₹)', fontsize=12)
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend()
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return fig
    
    def create_summary_dashboard(self, expenses_df):
        """
        Create a comprehensive dashboard with multiple visualizations
        
        Args:
            expenses_df: DataFrame with expense data
            
        Returns:
            List of matplotlib figures
        """
        figures = []
        
        # Pie chart
        figures.append(self.create_category_pie_chart(expenses_df))
        
        # Bar chart
        figures.append(self.create_category_bar_chart(expenses_df))
        
        # Time series (if date data is available)
        if 'date' in expenses_df.columns:
            figures.append(self.create_time_series_chart(expenses_df))
            figures.append(self.create_daily_spending_chart(expenses_df))
        
        return figures
    
    def save_chart_to_bytes(self, fig):
        """
        Convert a matplotlib figure to bytes for display
        
        Args:
            fig: Matplotlib figure
            
        Returns:
            Bytes object
        """
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        return buf


