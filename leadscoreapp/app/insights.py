import pandas as pd

def generate_insights(df: pd.DataFrame):
    """
    Generate simple insights for the dashboard.
    """
    total_companies = df['Company_ID'].nunique()
    avg_revenue = df['Annual_Revenue (M₺)'].mean()
    top_industry = df['Industry'].mode()[0]

    insights = {
        "Total Companies": total_companies,
        "Average Revenue (M₺)": round(avg_revenue, 2),
        "Top Industry": top_industry
    }

    return insights
