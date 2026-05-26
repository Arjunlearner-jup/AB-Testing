# Digital Marketing Campaign Analysis

This project analyzes a digital marketing campaign dataset with a simple end-to-end workflow: clean the raw CSV, prepare an A/B test between **Email** and **Social Media**, run statistical tests, and fit a logistic regression model for conversion.[file:32][file:33][file:34][file:35][file:36]

## Project files

| File | Purpose |
|---|---|
| `01_clean_data.py` | Loads the raw dataset, strips column names, converts numeric and text fields, removes duplicates, handles missing values, and saves `digital_marketing_campaign_dataset_cleaned.csv`.[file:32] |
| `02_ab_setup.py` | Filters the cleaned data to the two campaign groups, creates a treatment flag, and prints grouped summaries for conversion and conversion rate.[file:36] |
| `03_ab_test_streamlit.py` | Streamlit app for the A/B test comparing Email and Social Media using t-tests and a confidence interval for conversion rate differences.[file:33] |
| `04_regression.py` | Streamlit script that fits a logistic regression model and shows the statsmodels summary output in a console-style block.[file:34] |
| `04_logit_streamlit.py` | Streamlit app that fits logistic regression, displays coefficient-level results, odds ratios, and a treatment interpretation panel.[file:35] |

## Workflow

1. Run `01_clean_data.py` to create the cleaned dataset file `digitalmarketingcampaigndatasetcleaned.csv` or `digital_marketing_campaign_dataset_cleaned.csv`, depending on the script version being used.[file:32][file:34][file:35]
2. Use `02_ab_setup.py` to confirm the Email and Social Media subsets, treatment coding, and grouped summary statistics before testing.[file:36]
3. Launch `03_ab_test_streamlit.py` to review the A/B test metrics for binary conversion and conversion rate.[file:33]
4. Launch either `04_regression.py` or `04_logit_streamlit.py` to estimate a logit model with `Conversion` as the dependent variable and `treatment`, `Age`, `Income`, and `AdSpend` as predictors.[file:34][file:35]

## Requirements

Install these Python packages before running the scripts:[file:33][file:34][file:35]

```bash
pip install pandas numpy scipy statsmodels streamlit
```

## How to run

### 1. Clean the raw data

```bash
python 01_clean_data.py
```

This script reads the raw marketing dataset, standardizes columns, fills missing values, and writes a cleaned CSV for the later steps.[file:32]

### 2. Check the A/B setup

```bash
python 02_ab_setup.py
```

This step keeps only `Email` and `Social Media`, drops missing values in key testing fields, creates a binary `treatment` indicator, and prints summary statistics.[file:36]

### 3. Run the A/B test dashboard

```bash
streamlit run 03_ab_test_streamlit.py
```

The dashboard computes t-tests for `Conversion` and `ConversionRate`, reports p-values, and shows a 95% confidence interval for the difference in conversion rate between channels.[file:33]

### 4. Run the logistic regression app

Choose one of the following:

```bash
streamlit run 04_regression.py
```

or

```bash
streamlit run 04_logit_streamlit.py
```

Both scripts fit a logistic regression model on the filtered Email vs Social Media sample, while the second app adds coefficient tables, odds ratios, and a treatment interpretation section.[file:34][file:35]

## Model specification

The logistic regression is fit on the filtered subset where `CampaignChannel` is either `Email` or `Social Media`, with a treatment variable defined as 1 for Email and 0 for Social Media.[file:34][file:35][file:36]

The model uses:

- Dependent variable: `Conversion`.[file:34][file:35]
- Predictors: `treatment`, `Age`, `Income`, `AdSpend`.[file:34][file:35]

