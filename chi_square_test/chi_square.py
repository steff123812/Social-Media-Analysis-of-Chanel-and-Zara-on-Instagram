# Exploratory robustness check for MSc Marketing & Business Analytics project (University of Exeter)
# Purpose: Supplementary chi-square tests of association (Brand × Content Type; Brand × Influencer Type)
# Note: This is a supporting check, not a production-level statistical pipeline.

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# ===== LOAD RQ1 DATA =====
# Single Excel file with two sheets:
# Sheet 0 = Zara posts
# Sheet 1 = Chanel posts
file_name = "zara_posts_raw(AutoRecovered)-2.xlsx"   # 

zara_df = pd.read_excel(file_name, sheet_name=0)
chanel_df = pd.read_excel(file_name, sheet_name=1)

# ===== ADD BRAND LABELS =====
zara_df["Brand"] = "Zara"
chanel_df["Brand"] = "Chanel"

# ===== CLEAN CONTENT TYPE =====
zara_df["content_type"] = zara_df["content_type"].astype(str).str.lower().str.strip()
chanel_df["content_type"] = chanel_df["content_type"].astype(str).str.lower().str.strip()

# ===== COMBINE DATA =====
df = pd.concat([zara_df, chanel_df], ignore_index=True)

# ===== CREATE INFLUENCER LABEL =====
# Expected coding: 0=None, 1=Influencer, 2=Celebrity
df["Influencer_Label"] = df["Influencer Type"].map({
    0: "None",
    1: "Influencer",
    2: "Celebrity"
})

# =====================================================
# CHI-SQUARE TEST 1: BRAND × CONTENT TYPE
# =====================================================
content_table = pd.crosstab(df["Brand"], df["content_type"])
chi2, p, dof, _ = chi2_contingency(content_table)

n = content_table.values.sum()
cramers_v = np.sqrt(chi2 / (n * (min(content_table.shape) - 1)))

print("\nRESULT 1: Brand × Content Type")
print("p-value:", p)
print("Cramér’s V:", cramers_v)
print(content_table)

# =====================================================
# CHI-SQUARE TEST 2: BRAND × INFLUENCER TYPE
# =====================================================
influencer_table = pd.crosstab(df["Brand"], df["Influencer_Label"])
chi2_i, p_i, dof_i, _ = chi2_contingency(influencer_table)

n_i = influencer_table.values.sum()
cramers_v_i = np.sqrt(chi2_i / (n_i * (min(influencer_table.shape) - 1)))

print("\nRESULT 2: Brand × Influencer Type")
print("p-value:", p_i)
print("Cramér’s V:", cramers_v_i)
print(influencer_table)
