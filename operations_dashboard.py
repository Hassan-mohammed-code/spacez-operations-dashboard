import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Spacez Operations Dashboard", layout="wide")
st.title("🛠️ Spacez Operations AI Dashboard")
st.markdown("**AI-Powered Review Analysis for Operations**")

# Load data
@st.cache_data
def load_data():
    try:
        possible_paths = ["spacez_reviews_dataset.xlsx", "attachments/spacez_reviews_dataset.xlsx"]
        for path in possible_paths:
            if os.path.exists(path):
                df = pd.read_excel(path, sheet_name="Reviews")
                return df
        st.error("❌ Excel file not found. Please make sure spacez_reviews_dataset.xlsx is in the root folder.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

df = load_data()

# Normalize ratings
def normalize_rating(row):
    if pd.isna(row['rating_raw']) or pd.isna(row['rating_scale']):
        return 0.0
    if row['rating_scale'] == 5:
        return round(row['rating_raw'] * 2, 1)
    else:
        return round(row['rating_raw'], 1)

df['normalized_rating'] = df.apply(normalize_rating, axis=1)

# Issue categorization
def categorize_issue(text):
    if not isinstance(text, str):
        return "Other"
    text_lower = text.lower()
    if any(word in text_lower for word in ['pool', 'swimming', 'murky', 'dirty pool']):
        return "Pool Maintenance"
    elif any(word in text_lower for word in ['check-in', 'late', 'arrival', 'receive', 'unreachable']):
        return
