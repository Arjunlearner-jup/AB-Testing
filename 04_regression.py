import streamlit as st
import pandas as pd
import statsmodels.api as sm

st.set_page_config(page_title="Logit Regression", layout="centered")
st.title("Logit Regression Results")

# Load data
df = pd.read_csv("digital_marketing_campaign_dataset_cleaned.csv")
df.columns = df.columns.str.strip()

numeric_cols = [
    "Age", "Income", "AdSpend", "ClickThroughRate", "ConversionRate",
    "WebsiteVisits", "PagesPerVisit", "TimeOnSite", "SocialShares",
    "EmailOpens", "EmailClicks", "PreviousPurchases", "LoyaltyPoints",
    "Conversion"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

ab = df[df["CampaignChannel"].isin(["Email", "Social Media"])].copy()
ab = ab.dropna(subset=["CampaignChannel", "Conversion", "Age", "Income", "AdSpend"])
ab["treatment"] = (ab["CampaignChannel"] == "Email").astype(int)

model_df = ab[["Conversion", "treatment", "Age", "Income", "AdSpend"]].dropna()
X = sm.add_constant(model_df[["treatment", "Age", "Income", "AdSpend"]], has_constant="add")
y = model_df["Conversion"]

try:
    model = sm.Logit(y, X).fit()
    summary_text = model.summary().as_text()
    st.code(summary_text, language=None)
except Exception as e:
    st.error(f"Model fitting failed: {e}")