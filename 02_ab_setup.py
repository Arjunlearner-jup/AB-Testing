import pandas as pd

# Load cleaned data
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

# 8. Keep only the two treatment groups you want
ab = df[df["CampaignChannel"].isin(["Email", "Social Media"])].copy()

# 9. Drop rows missing key columns
ab = ab.dropna(subset=["CampaignChannel", "Conversion", "ConversionRate"])

# 10. Create treatment flag
ab["treatment"] = (ab["CampaignChannel"] == "Email").astype(int)

# 11. Group sizes and summaries
print(ab["CampaignChannel"].value_counts())
print(ab.groupby("CampaignChannel")[["Conversion", "ConversionRate"]].agg(["count", "mean", "std"]))
