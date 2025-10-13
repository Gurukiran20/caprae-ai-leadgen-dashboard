import streamlit as st
import pandas as pd
import plotly.express as px
from insights import generate_insights
from scoring import score_leads
from preprocessing import load_and_clean_data


@st.cache_data
def load_default_data():
    return load_and_clean_data(r"C:\LeadDash\leadscoreapp\data\leads_dataset.csv")


def main():
    st.set_page_config(page_title="Smart Lead & Insights Dashboard", layout="wide")
    st.title("📊 Smart Lead & Insights Dashboard")

    # --- File Upload ---
    uploaded_file = st.sidebar.file_uploader("📤 Upload your lead CSV file", type=["csv"])

    if uploaded_file:
        try:
            uploaded_file.seek(0)
            original_df = pd.read_csv(uploaded_file)
            uploaded_file.seek(0)
            cleaned_data, removed_duplicates = load_and_clean_data(uploaded_file)
            st.success("✅ Uploaded file loaded and cleaned successfully!")
        except ValueError as ve:
            st.error(f"⚠️ File error: {ve}")
            return
        except Exception as e:
            st.error(f"🚫 Unexpected error: {e}")
            return
    else:
        st.info("ℹ️ No file uploaded — using default sample dataset.")
        original_df = pd.read_csv(r"C:\LeadDash\leadscoreapp\data\leads_dataset.csv")
        cleaned_data, removed_duplicates = load_default_data()

    # --- Duplicate Summary ---
    removed_count = len(original_df) - len(cleaned_data)
    st.caption(f"🧹 Removed **{removed_count}** duplicate rows (fuzzy matched on `Company_Name`)")

    # --- View Removed Duplicates ---
    if not removed_duplicates.empty:
        with st.expander("🔍 View Removed Duplicates"):
            st.dataframe(removed_duplicates[["Company_Name", "Industry", "Region", "District"]].head(25))

    # --- Sidebar Filters ---
    st.sidebar.header("Filters")
    industry_filter = st.sidebar.multiselect("Select Industry", options=cleaned_data["Industry"].unique())
    region_filter = st.sidebar.multiselect("Select Region", options=cleaned_data["Region"].unique())
    district_filter = st.sidebar.multiselect("Select District", options=cleaned_data["District"].unique())

    # --- Apply Filters ---
    filtered_data = cleaned_data.copy()
    if industry_filter:
        filtered_data = filtered_data[filtered_data["Industry"].isin(industry_filter)]
    if region_filter:
        filtered_data = filtered_data[filtered_data["Region"].isin(region_filter)]
    if district_filter:
        filtered_data = filtered_data[filtered_data["District"].isin(district_filter)]

    # --- Lead Scoring ---
    lead_scores = score_leads(filtered_data)
    filtered_data = filtered_data.merge(
        lead_scores,
        on=["Company_ID", "Industry", "Annual_Revenue (M₺)", "Conversion_Rate (%)"],
        how="left"
    )


    #  1. Lead Distribution Chart
    st.subheader("📌 Lead Distribution by Industry")
    industry_counts = filtered_data["Industry"].value_counts().reset_index()
    industry_counts.columns = ["Industry", "Count"]

    fig = px.bar(
        industry_counts,
        x="Industry",
        y="Count",
        color="Industry",
        title="Industry Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)


    #   2. Lead Prioritization Chart
 
    if "Lead_Category" in filtered_data.columns:
        st.subheader("🏆 Lead Priority Breakdown")
        priority_fig = px.pie(
            filtered_data,
            names="Lead_Category",
            title="Lead Prioritization (High / Medium / Low)",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(priority_fig, use_container_width=True)

    
    #   3. Top Insights
    st.subheader("💡 Top Insights")
    insights = generate_insights(filtered_data)
    st.write(insights)

    #   4. Data Table
    
    st.subheader("📋 Sample Data (Top 10 Rows After Cleaning & Scoring)")

    # Reset index so it starts from 1 instead of 0
    filtered_data = filtered_data.reset_index(drop=True)
    filtered_data.index = filtered_data.index + 1

    st.dataframe(filtered_data.head(10))


if __name__ == "__main__":
    main()
