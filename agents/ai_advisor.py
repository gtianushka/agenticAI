from transformers import pipeline

generator = pipeline("text2text-generation", model="google/flan-t5-base")

def generate_financial_advice(df):
    total_spent = df["Amount"].sum()
    summary = df.groupby("Category")["Amount"].sum().to_dict()

    prompt = f"""
    You are BudgetBuddy AI, a personal finance coach.
    Analyze this data and give a short financial advice and next-month saving plan.

    Spending Summary: {summary}
    Total spent this month: ₹{total_spent}

    Respond in 4-6 lines, be practical and encouraging.
    """

    result = generator(prompt, max_new_tokens=120)[0]["generated_text"]
    return result
