# agents/memory_agent.py
import os
import json

MEMORY_FILE = "data/memory.json"

def load_memory():
    """Load past expense summaries."""
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_to_memory(summary):
    """Store the latest expense summary."""
    memory = load_memory()
    memory.append(summary)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def get_trends():
    """Return insights from memory."""
    memory = load_memory()
    if not memory:
        return "No past expense history found."

    # Example trend analysis
    total_spend = [sum(cat["amount"] for cat in m["categories"]) for m in memory if "categories" in m]
    if len(total_spend) > 1:
        diff = total_spend[-1] - total_spend[-2]
        trend = "increased" if diff > 0 else "decreased"
        return f"Your total expenses have {trend} by ₹{abs(diff)} compared to the previous month."
    return "Insufficient data for trend analysis."
