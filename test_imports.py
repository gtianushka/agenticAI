"""
Test script to verify all imports and basic functionality
Run this script before starting the main application
"""

import sys

def test_imports():
    """Test all required imports"""
    print("🧪 Testing BudgetBuddy AI imports...")
    print()
    
    try:
        import streamlit
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import matplotlib
        print("✅ matplotlib imported successfully")
    except ImportError as e:
        print(f"❌ matplotlib import failed: {e}")
        return False
    
    try:
        import transformers
        print("✅ transformers imported successfully")
    except ImportError as e:
        print(f"❌ transformers import failed: {e}")
        return False
    
    try:
        import torch
        print("✅ torch imported successfully")
    except ImportError as e:
        print(f"❌ torch import failed: {e}")
        return False
    
    print()
    print("🔬 Testing agent imports...")
    print()
    
    try:
        from agents.tracker_agent import TrackerAgent
        print("✅ TrackerAgent imported successfully")
    except ImportError as e:
        print(f"❌ TrackerAgent import failed: {e}")
        return False
    
    try:
        from agents.database import DatabaseManager
        print("✅ DatabaseManager imported successfully")
    except ImportError as e:
        print(f"❌ DatabaseManager import failed: {e}")
        return False
    
    try:
        from agents.advisor_agent import AdvisorAgent
        print("✅ AdvisorAgent imported successfully")
    except ImportError as e:
        print(f"❌ AdvisorAgent import failed: {e}")
        return False
    
    try:
        from agents.visualizer_agent import VisualizerAgent
        print("✅ VisualizerAgent imported successfully")
    except ImportError as e:
        print(f"❌ VisualizerAgent import failed: {e}")
        return False
    
    print()
    print("🎉 All imports successful!")
    print()
    return True


def test_basic_functionality():
    """Test basic agent functionality"""
    print("🔧 Testing basic functionality...")
    print()
    
    try:
        from agents.database import DatabaseManager
        
        # Test database creation
        db = DatabaseManager("database/test_budgetbuddy.db")
        print("✅ Database created successfully")
        
        # Test inserting expense
        db.insert_expense("2025-01-15", "Test expense", 10.00, "Test")
        print("✅ Expense inserted successfully")
        
        # Test retrieving expenses
        expenses = db.get_all_expenses()
        print(f"✅ Retrieved {len(expenses)} expense(s)")
        
        print()
        print("✅ Basic functionality tests passed!")
        print()
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("BudgetBuddy AI - Import and Functionality Test")
    print("=" * 50)
    print()
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test basic functionality
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("=" * 50)
            print("🎉 All tests passed! Ready to launch BudgetBuddy AI")
            print("=" * 50)
            print()
            print("To start the application, run:")
            print("  streamlit run app.py")
            print()
            sys.exit(0)
        else:
            print("=" * 50)
            print("⚠️  Functionality tests failed")
            print("=" * 50)
            sys.exit(1)
    else:
        print("=" * 50)
        print("❌ Import tests failed")
        print("=" * 50)
        print()
        print("Please ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        print()
        sys.exit(1)

