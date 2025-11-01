#!/bin/bash

# BudgetBuddy AI - Launch Script
# This script activates the virtual environment and starts the Streamlit application

echo "🤖 BudgetBuddy AI - Starting Application..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    echo "Then install dependencies: pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found!"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Start Streamlit application
echo "🚀 Starting Streamlit server..."
echo "📍 Application will open at http://localhost:8501"
echo ""
streamlit run app.py

