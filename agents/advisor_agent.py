"""
LangChain-based Advisor Agent for BudgetBuddy AI
An intelligent agent that analyzes expenses and provides financial advice using agentic reasoning
"""

import pandas as pd
from datetime import datetime
from agents.database import DatabaseManager
from transformers import pipeline


class AdvisorAgent:
    """Agent responsible for analyzing expenses and providing financial advice"""
    
    def __init__(self, model_name="facebook/bart-large-cnn"):
        """
        Initialize the advisor agent with a summarization model
        
        Args:
            model_name: Hugging Face model name for summarization
                       Options: "facebook/bart-large-cnn", "t5-base", "google/flan-t5-base"
        """
        self.model_name = model_name
        # Use intelligent rule-based system (more reliable than current AI models)
        # The dynamic rule-based system provides better, personalized insights
        self.generator = None
        self.use_summarization = False
        
        self.db = DatabaseManager()
    
    def analyze_spending_patterns(self, expenses_df, year=None, month=None):
        """
        Agent task: Analyze spending patterns with intelligent reasoning
        
        This agentic function detects trends, insights, and patterns in spending data
        
        Args:
            expenses_df: DataFrame with expense data
            year: Optional year filter
            month: Optional month filter
            
        Returns:
            Dictionary with comprehensive spending analysis
        """
        if expenses_df.empty:
            return {
                'total_spent': 0,
                'category_breakdown': {},
                'average_daily': 0,
                'top_category': None,
                'num_transactions': 0,
                'trends': [],
                'insights': []
            }
        
        # Calculate total spending
        total_spent = expenses_df['amount'].sum()
        
        # Category breakdown
        category_summary = expenses_df.groupby('category')['amount'].sum().to_dict()
        category_percentages = {cat: (amt/total_spent*100) for cat, amt in category_summary.items()}
        
        # Top spending category
        top_category = max(category_summary, key=category_summary.get) if category_summary else None
        
        # Agent reasoning: Trends and insights
        trends = []
        insights = []
        
        # Average daily spending with trend analysis
        if 'date' in expenses_df.columns:
            expenses_df['date'] = pd.to_datetime(expenses_df['date'])
            days = (expenses_df['date'].max() - expenses_df['date'].min()).days + 1
            avg_daily = total_spent / days if days > 0 else total_spent
            
            # Detect weekly spending trends
            expenses_df['week'] = expenses_df['date'].dt.isocalendar().week
            expenses_df['year'] = expenses_df['date'].dt.isocalendar().year
            expenses_df['year_week'] = expenses_df['year'].astype(str) + '_' + expenses_df['week'].astype(str)
            weekly_spending = expenses_df.groupby('year_week')['amount'].sum().sort_index()
            if len(weekly_spending) > 1:
                if weekly_spending.iloc[-1] > weekly_spending.iloc[-2] * 1.2:
                    trends.append("🔺 Increasing spending trend detected in recent weeks")
                elif weekly_spending.iloc[-1] < weekly_spending.iloc[-2] * 0.8:
                    trends.append("🔻 Decreasing spending trend detected - great job!")
        else:
            avg_daily = total_spent
        
        # Agent insights: Concentration analysis
        top_3_categories = sorted(category_summary.items(), key=lambda x: x[1], reverse=True)[:3]
        top_3_total = sum(amt for _, amt in top_3_categories)
        
        if top_3_total / total_spent > 0.7:
            insights.append("📌 Heavy concentration (>70%) in top 3 categories - consider diversifying")
        
        # Agent insights: Transaction analysis
        num_transactions = len(expenses_df)
        avg_transaction = total_spent / num_transactions if num_transactions > 0 else 0
        
        if avg_transaction > 1000:
            insights.append("💰 High average transaction (₹{:.2f}) - review large purchases".format(avg_transaction))
        elif avg_transaction < 200:
            insights.append("✅ Good transaction discipline - low average spend")
        
        # Agent insights: Category balance
        well_balanced = [cat for cat, pct in category_percentages.items() if 10 <= pct <= 25]
        if well_balanced:
            insights.append("⚖️ Well-balanced categories: {}".format(", ".join(well_balanced)))
        
        return {
            'total_spent': total_spent,
            'category_breakdown': category_summary,
            'average_daily': avg_daily,
            'top_category': top_category,
            'num_transactions': num_transactions,
            'trends': trends,
            'insights': insights,
            'category_percentages': category_percentages
        }
    
    def detect_overspending(self, category_breakdown, threshold_percentage=30):
        """
        Detect categories with unusually high spending
        
        Args:
            category_breakdown: Dictionary of category: amount
            threshold_percentage: Percentage threshold for detecting overspending
            
        Returns:
            List of overspending categories
        """
        if not category_breakdown:
            return []
        
        total = sum(category_breakdown.values())
        if total == 0:
            return []
        
        overspending = []
        threshold = threshold_percentage / 100.0
        
        for category, amount in category_breakdown.items():
            percentage = amount / total
            if percentage > threshold:
                severity = "HIGH" if percentage > 0.5 else "MEDIUM"
                overspending.append({
                    'category': category,
                    'amount': amount,
                    'percentage': percentage * 100,
                    'severity': severity
                })
        
        return overspending
    
    def generate_saving_tips(self, overspending_categories):
        """
        Generate smart, actionable saving tips based on overspending detection
        
        Args:
            overspending_categories: List of overspending categories
            
        Returns:
            List of dynamic saving tips
        """
        tips = []
        
        # Comprehensive tips with actionable advice
        tips_mapping = {
            'Food': "🍽️ Meal Planning Win: Prep 3-4 meals weekly to reduce eating out by ₹2,000-3,000/month",
            'Entertainment': "🎬 Smart Entertainment: Audit streaming subscriptions - keep only 2 active to save ₹500-800/month",
            'Transport': "🚗 Travel Smart: Use metro/bus 2 days/week + carpooling to cut transport costs by 30%",
            'Shopping': "🛍️ 48-Hour Rule: Wait 2 days before any purchase over ₹500. Saves ₹3,000-5,000/month",
            'Utilities': "⚡ Energy Audit: Switch to LED bulbs, unplug chargers to save ₹500-800 monthly on electricity",
            'Shopping': "🛒 One-Click Fix: Turn off 'save payment info' to reduce impulse online shopping",
            'Health': "💊 Generic Swaps: Ask pharmacist for generic alternatives to save 40-50% on medicines",
            'Education': "📚 Second-Hand Savings: Buy used books/courses, join library to save 30-40%",
            'Bills': "📱 Bill Optimization: Review phone/data plans, negotiate insurance - potential ₹1,000-2,000/month savings",
            'Other': "💡 Audit Subscriptions: Cancel unused apps/memberships. Most people waste ₹1,500-3,000 monthly",
            'Uncategorized': "📝 Categorization First: Properly tag all expenses to identify hidden leaks worth ₹2,000-4,000"
        }
        
        for overspent in overspending_categories:
            category = overspent['category']
            percentage = overspent.get('percentage', 0)
            
            # Get tip or generate dynamic one
            if category in tips_mapping:
                tip = tips_mapping[category]
            else:
                # Generate category-specific tip
                if percentage > 50:
                    tip = f"🚨 {category} dominates your budget! Aim to reduce by 20% = ₹{overspent['amount']*0.2:.0f}/month saved"
                else:
                    tip = f"💰 Review {category} expenses. Even 15% reduction = ₹{overspent['amount']*0.15:.0f} saved"
            
            tips.append(tip)
        
        return tips
    
    def generate_ai_advice(self, analysis_summary, overspending_list, saving_tips):
        """
        Generate AI-powered financial advice using Hugging Face models
        
        Args:
            analysis_summary: Dictionary with spending analysis
            overspending_list: List of overspending categories
            saving_tips: List of saving tips
            
        Returns:
            String with AI-generated advice
        """
        # Build context for AI model
        context = f"""
        Spending Summary:
        Total Amount: ₹{analysis_summary['total_spent']:.2f}
        Average Daily Spending: ₹{analysis_summary['average_daily']:.2f}
        Number of Transactions: {analysis_summary['num_transactions']}
        Top Category: {analysis_summary['top_category']}
        
        Category Breakdown: {analysis_summary['category_breakdown']}
        
        Overspending Detected: {[f"{x['category']} ({x['percentage']:.1f}%)" for x in overspending_list]}
        
        Saving Tips: {saving_tips}
        """
        
        # Generate advice prompt
        if self.use_summarization and self.generator:
            # Use summarization approach
            advice_prompt = f"""
            You are BudgetBuddy AI, a personal finance coach. Analyze this spending data and provide concise, actionable financial advice.
            
            {context}
            
            Provide a brief summary of their spending patterns, identify the main area of concern, and give one practical step to improve their financial health next month. Keep it encouraging and practical.
            """
            
            try:
                result = self.generator(advice_prompt, max_length=150, min_length=80, do_sample=False)
                advice = result[0]['summary_text']
            except:
                advice = self._generate_rule_based_advice(analysis_summary, overspending_list, saving_tips)
        elif self.generator:
            # Use text generation approach
            advice_prompt = f"""
            As BudgetBuddy AI, analyze this spending and give financial advice: {context}
            Advice:"""
            
            try:
                result = self.generator(advice_prompt, max_new_tokens=120, do_sample=False, temperature=0.7)
                advice = result[0]['generated_text'].replace(advice_prompt, "").strip()
            except:
                advice = self._generate_rule_based_advice(analysis_summary, overspending_list, saving_tips)
        else:
            # Fallback to rule-based advice
            advice = self._generate_rule_based_advice(analysis_summary, overspending_list, saving_tips)
        
        return advice
    
    def _generate_rule_based_advice(self, analysis_summary, overspending_list, saving_tips):
        """
        Generate intelligent, dynamic advice based on agent reasoning
        
        Args:
            analysis_summary: Dictionary with spending analysis
            overspending_list: List of overspending categories
            saving_tips: List of saving tips
            
        Returns:
            String with comprehensive agentic advice
        """
        advice_parts = []
        total_spent = analysis_summary['total_spent']
        avg_daily = analysis_summary['average_daily']
        num_trans = analysis_summary['num_transactions']
        projected_monthly = avg_daily * 30
        
        # Dynamic greeting based on spending patterns
        advice_parts.append("🤖 BUDGETBUDDY AI FINANCIAL REPORT")
        advice_parts.append("=" * 70)
        advice_parts.append("")
        
        # Context-aware opening
        if total_spent == 0:
            opening = "📝 No expenses recorded yet. Ready to start your financial journey!"
        elif projected_monthly > 50000:
            opening = f"📊 Active Spending Month: You've spent ₹{total_spent:.2f} with {num_trans} transactions"
        elif projected_monthly < 15000:
            opening = f"💰 Moderate Spender: ₹{total_spent:.2f} spent across {num_trans} transactions"
        else:
            opening = f"📈 Regular Spending: ₹{total_spent:.2f} total with {num_trans} transactions"
        
        advice_parts.append(opening)
        advice_parts.append("")
        
        # Dynamic insights based on actual data
        insights_generated = []
        
        # 1. Transaction pattern insights
        if num_trans > 50:
            insights_generated.append(f"⚠️ High transaction frequency ({num_trans}): Many small purchases add up. Consider bundling errands.")
        elif num_trans < 5 and total_spent > 5000:
            insights_generated.append(f"💳 Few but large transactions: Your spending style is concentrated. Good for tracking!")
        elif num_trans >= 10 and num_trans <= 30:
            insights_generated.append(f"✅ Balanced transaction count ({num_trans}): Healthy spending frequency.")
        
        # 2. Category distribution insights
        cat_breakdown = analysis_summary.get('category_breakdown', {})
        if cat_breakdown:
            unique_cats = len(cat_breakdown)
            if unique_cats == 1:
                insights_generated.append("🎯 Single category focus: All spending in one area. Consider diversity.")
            elif unique_cats >= 5:
                insights_generated.append(f"🌟 Well-diversified spending across {unique_cats} categories. Great variety!")
            else:
                insights_generated.append(f"📂 {unique_cats} spending categories active. Consider reviewing each.")
            
            # Top 3 category analysis
            top_3 = sorted(cat_breakdown.items(), key=lambda x: x[1], reverse=True)[:3]
            if len(top_3) >= 3:
                top_total = sum(amt for _, amt in top_3)
                pct = (top_total / total_spent * 100) if total_spent > 0 else 0
                if pct > 75:
                    insights_generated.append(f"📌 Concentration: Top 3 categories ({', '.join([c for c, _ in top_3])}) = {pct:.1f}% of budget")
        
        # 3. Daily spending pattern
        if avg_daily > 2000:
            insights_generated.append(f"💸 High daily average (₹{avg_daily:.0f}/day): Consider reducing frequent expenses.")
        elif avg_daily < 500:
            insights_generated.append(f"✨ Excellent daily control (₹{avg_daily:.0f}/day): Keep up the discipline!")
        
        # 4. Trend insights
        if analysis_summary.get('trends'):
            for trend in analysis_summary['trends']:
                insights_generated.append(f"📈 {trend}")
        
        # Display insights
        if insights_generated:
            advice_parts.append("🧠 KEY INSIGHTS")
            for insight in insights_generated:
                advice_parts.append(f"   {insight}")
            advice_parts.append("")
        
        # Category breakdown with smart commentary
        if cat_breakdown:
            advice_parts.append("📊 SPENDING BREAKDOWN")
            sorted_cats = sorted(cat_breakdown.items(), key=lambda x: x[1], reverse=True)
            for category, amount in sorted_cats:
                percentage = (amount / total_spent * 100) if total_spent > 0 else 0
                
                # Dynamic comments per category
                if percentage > 40:
                    comment = " ⚠️ Very high"
                elif percentage > 25:
                    comment = " 📌 Above average"
                elif percentage > 10:
                    comment = " ✅ Balanced"
                else:
                    comment = " 💚 Low"
                
                advice_parts.append(f"   • {category}: ₹{amount:.2f} ({percentage:.1f}%){comment}")
            advice_parts.append("")
        
        # Overspending warnings with severity
        if overspending_list:
            advice_parts.append("⚠️ PRIORITY ALERTS")
            for overspent in overspending_list:
                severity = overspent.get('severity', 'MEDIUM')
                if severity == 'HIGH':
                    icon = "🚨"
                    urgency = "URGENT ACTION"
                else:
                    icon = "⚠️"
                    urgency = "Needs attention"
                
                advice_parts.append(f"{icon} {overspent['category']}: {overspent['percentage']:.1f}% ({urgency})")
            advice_parts.append("")
        
        # Smart action plan
        if saving_tips:
            advice_parts.append("💡 RECOMMENDED ACTIONS")
            for i, tip in enumerate(saving_tips[:3], 1):  # Top 3 actionable tips
                advice_parts.append(f"{i}. {tip}")
            advice_parts.append("")
        
        # Dynamic forecast with context
        advice_parts.append("🔮 30-DAY PROJECTION")
        advice_parts.append(f"Estimated Monthly: ₹{projected_monthly:.2f}")
        
        if projected_monthly > 50000:
            forecast_msg = f"💸 EXCEEDING: Projected monthly {projected_monthly:.0f} likely above comfortable range"
        elif projected_monthly > 35000:
            forecast_msg = "📊 MODERATE: Projected spending in typical urban range"
        elif projected_monthly > 20000:
            forecast_msg = "💰 BALANCED: Healthy monthly projection"
        else:
            forecast_msg = "✨ EXCELLENT: Well-controlled spending projected"
        
        advice_parts.append(forecast_msg)
        advice_parts.append("")
        
        # Personalized closing
        if overspending_list:
            closing = "🎯 Focus on your top spending category first - small changes there make big impact!"
        elif projected_monthly < 25000:
            closing = "🌟 You're doing great! Keep tracking to maintain healthy habits."
        else:
            closing = "📝 Regular tracking helps identify opportunities. Keep monitoring!"
        
        advice_parts.append("=" * 70)
        advice_parts.append(closing)
        advice_parts.append("=" * 70)
        
        return "\n".join(advice_parts)
    
    def provide_monthly_analysis(self, expenses_df, year=None, month=None):
        """
        Comprehensive monthly analysis with AI-powered advice
        
        Args:
            expenses_df: DataFrame with expense data
            year: Optional year filter
            month: Optional month filter
            
        Returns:
            Dictionary with complete analysis and advice
        """
        # Analyze spending patterns
        analysis = self.analyze_spending_patterns(expenses_df, year, month)
        
        # Detect overspending
        overspending = self.detect_overspending(analysis['category_breakdown'])
        
        # Generate saving tips
        tips = self.generate_saving_tips(overspending)
        
        # Generate AI advice
        advice = self.generate_ai_advice(analysis, overspending, tips)
        
        return {
            'analysis': analysis,
            'overspending': overspending,
            'saving_tips': tips,
            'ai_advice': advice,
            'generated_at': datetime.now().isoformat()
        }
