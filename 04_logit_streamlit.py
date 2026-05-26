import pandas as pd
import statsmodels.api as sm
import streamlit as st

st.set_page_config(page_title="Logistic Regression: Email vs Social Media", layout="wide")
st.title("Logistic Regression Analysis: Email vs Social Media")
st.write("This app runs a logistic regression for Conversion using treatment, Age, Income, and AdSpend.")

file_path = "digital_marketing_campaign_dataset.csv"

try:
    df = pd.read_csv(file_path)
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

    st.subheader("Filtered Data")
    st.write("Rows used for regression:", ab.shape[0])
    st.dataframe(ab.head())

    model_df = ab[["Conversion", "treatment", "Age", "Income", "AdSpend"]].dropna()
    X = sm.add_constant(model_df[["treatment", "Age", "Income", "AdSpend"]])
    y = model_df["Conversion"]

    model = sm.Logit(y, X).fit(disp=False)

    results_df = pd.DataFrame({
        "Coefficient": model.params,
        "P-value": model.pvalues,
        "Std Error": model.bse,
        "Odds Ratio": model.params.apply(lambda x: pd.np.exp(x))
    })

    st.subheader("Regression Results")
    st.dataframe(results_df)

    st.subheader("Treatment Interpretation")
    treatment_coef = model.params["treatment"]
    treatment_p = model.pvalues["treatment"]

    st.write(f"Treatment coefficient: **{treatment_coef:.4f}**")
    st.write(f"Treatment p-value: **{treatment_p:.6f}**")

    if treatment_coef > 0:
        st.success("Email is associated with a higher conversion likelihood than Social Media.")
    else:
        st.warning("Email is associated with a lower conversion likelihood than Social Media.")

    if treatment_p < 0.05:
        st.success("The treatment effect is statistically significant at the 5% level.")
    else:
        st.info("The treatment effect is not statistically significant at the 5% level.")

    st.subheader("Model Summary")
    st.text(model.summary())

except FileNotFoundError:
    st.error(f"File not found: {file_path}")
    st.info("Make sure digital_marketing_campaign_dataset.csv is in the same folder as this Streamlit app.")
