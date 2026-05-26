import pandas as pd
import numpy as np
from scipy import stats
import streamlit as st

st.set_page_config(page_title="A/B Test: Email vs Social Media", layout="wide")
st.title("A/B Test Analysis: Email vs Social Media")


# Hardcoded file path
file_path = "digital_marketing_campaign_dataset_cleaned.csv"

try:
    # Load cleaned CSV
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    # Convert numeric columns
    numeric_cols = [
        "Age", "Income", "AdSpend", "ClickThroughRate", "ConversionRate",
        "WebsiteVisits", "PagesPerVisit", "TimeOnSite", "SocialShares",
        "EmailOpens", "EmailClicks", "PreviousPurchases", "LoyaltyPoints",
        "Conversion"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Filter Email vs Social Media
    ab = df[df["CampaignChannel"].isin(["Email", "Social Media"])].copy()
    ab = ab.dropna(subset=["CampaignChannel", "Conversion", "ConversionRate"])
    summary = ab.groupby("CampaignChannel")[["Conversion", "ConversionRate"]].agg(["count", "mean", "std"])
    st.dataframe(summary)

    # A/B test on binary conversion
    email_conv = ab.loc[ab["CampaignChannel"] == "Email", "Conversion"]
    social_conv = ab.loc[ab["CampaignChannel"] == "Social Media", "Conversion"]
    t_stat, p_val = stats.ttest_ind(email_conv, social_conv, equal_var=False)

    # A/B test on conversion rate
    email_rate = ab.loc[ab["CampaignChannel"] == "Email", "ConversionRate"]
    social_rate = ab.loc[ab["CampaignChannel"] == "Social Media", "ConversionRate"]
    t_stat_rate, p_val_rate = stats.ttest_ind(email_rate, social_rate, equal_var=False)

    # Confidence interval
    diff = email_rate.mean() - social_rate.mean()
    se = np.sqrt(email_rate.var(ddof=1) / len(email_rate) + social_rate.var(ddof=1) / len(social_rate))
    ci_low = diff - 1.96 * se
    ci_high = diff + 1.96 * se

    st.subheader("A/B Test Results")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Binary Conversion t-stat", f"{t_stat:.4f}")
        st.metric("Binary Conversion p-value", f"{p_val:.6f}")

    with col2:
        st.metric("Conversion Rate t-stat", f"{t_stat_rate:.4f}")
        st.metric("Conversion Rate p-value", f"{p_val_rate:.6f}")

    st.subheader("Difference in Conversion Rate")
    st.write(f"Mean Difference (Email - Social Media): **{diff:.6f}**")
    st.write(f"95% Confidence Interval: **({ci_low:.6f}, {ci_high:.6f})**")

    st.subheader("Interpretation")
    if p_val_rate < 0.05:
        st.success("The difference in ConversionRate is statistically significant at the 5% level.")
    else:
        st.warning("The difference in ConversionRate is not statistically significant at the 5% level.")

except FileNotFoundError:
    st.error(f"File not found: {file_path}")
    st.info("Make sure digital_marketing_campaign_dataset_cleaned.csv is in the same folder as this Streamlit app.")