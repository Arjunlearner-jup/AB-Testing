import pandas as pd
import numpy as np

# 1. Load data
df = pd.read_csv("digital_marketing_campaign_dataset.csv")

# 2. Clean column names
df.columns = df.columns.str.strip()

# 3. Convert numeric columns
numeric_cols = [
    "Age", "Income", "AdSpend", "ClickThroughRate", "ConversionRate",
    "WebsiteVisits", "PagesPerVisit", "TimeOnSite", "SocialShares",
    "EmailOpens", "EmailClicks", "PreviousPurchases", "LoyaltyPoints",
    "Conversion"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# 4. Clean text columns
text_cols = ["Gender", "CampaignChannel", "CampaignType", "AdvertisingPlatform", "AdvertisingTool"]
for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# 5. Remove duplicates
df = df.drop_duplicates()

# 6. Handle missing values
# Drop rows missing key A/B testing columns
key_cols = ["CampaignChannel", "Conversion", "ConversionRate"]
df = df.dropna(subset=[col for col in key_cols if col in df.columns])

# Optional: fill remaining numeric missing values with median
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

# Optional: fill remaining text missing values with mode
for col in text_cols:
    if col in df.columns and df[col].isna().any():
        df[col] = df[col].fillna(df[col].mode()[0])

# 7. Save cleaned CSV
df.to_csv("digital_marketing_campaign_dataset_cleaned.csv", index=False)

print("Cleaned file saved as: digital_marketing_campaign_dataset_cleaned.csv")
print("Final shape:", df.shape)