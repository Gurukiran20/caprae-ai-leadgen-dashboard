import pandas as pd
import numpy as np

def score_leads(df: pd.DataFrame):
    """
    Simple AI-powered scoring logic for leads.
    Score is based on revenue, marketing spend, and conversion rate.
    """

    # Normalize numeric columns safely
    df["Revenue_Score"] = df["Annual_Revenue (M₺)"] / df["Annual_Revenue (M₺)"].max()
    df["Spend_Score"] = df["Marketing_Spend (K₺)"] / df["Marketing_Spend (K₺)"].max()
    df["Conversion_Score"] = df["Conversion_Rate (%)"] / 100

    # Weighted scoring system
    df["Lead_Score"] = (
        0.4 * df["Revenue_Score"] +
        0.3 * df["Spend_Score"] +
        0.3 * df["Conversion_Score"]
    ) * 100  # make it 0–100 scale

    df["Lead_Category"] = pd.cut(
        df["Lead_Score"],
        bins=[0, 40, 70, 100],
        labels=["Low", "Medium", "High"]
    )

    return df[["Company_ID", "Industry", "Annual_Revenue (M₺)", "Conversion_Rate (%)", "Lead_Score", "Lead_Category"]]
