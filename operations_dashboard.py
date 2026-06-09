import streamlit as st
import pandas as pd

st.set_page_config(page_title="Spacez Operations Dashboard", layout="wide")
st.title("🛠️ Spacez Operations AI Dashboard")
st.markdown("**AI-Powered Review Analysis for Operations**")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("spacez_reviews_dataset.xlsx", sheet_name="Reviews")
    return df

df = load_data()

# Normalize ratings
def normalize_rating(row):
    if row['rating_scale'] == 5:
        return round(row['rating_raw'] * 2, 1)
    else:
        return round(row['rating_raw'], 1)

df['normalized_rating'] = df.apply(normalize_rating, axis=1)

# Issue categorization
def categorize_issue(text):
    text_lower = str(text).lower()
    if any(word in text_lower for word in ['pool', 'swimming', 'murky', 'dirty', 'cleaned']):
        return "Pool Maintenance"
    elif any(word in text_lower for word in ['check-in', 'late', 'arrival', 'receive']):
        return "Check-in Delay"
    elif any(word in text_lower for word in ['clean', 'dirty', 'housekeeping', 'bedsheet']):
        return "Cleanliness"
    elif any(word in text_lower for word in ['wifi', 'heating', 'ac', 'heater']):
        return "Amenities/Facilities"
    elif any(word in text_lower for word in ['photo', 'listing', 'view', 'misleading']):
        return "Listing Issue"
    elif any(word in text_lower for word in ['road', 'access', 'location']):
        return "Location/Access"
    else:
        return "Other"

df['issue_category'] = df['review_text'].apply(categorize_issue)

# Filters
st.sidebar.header("Filters")
selected_property = st.sidebar.selectbox("Property", ["All"] + list(df['property_name'].unique()))
selected_caretaker = st.sidebar.selectbox("Caretaker", ["All"] + list(df['caretaker_name'].unique()))

filtered_df = df.copy()
if selected_property != "All":
    filtered_df = filtered_df[filtered_df['property_name'] == selected_property]
if selected_caretaker != "All":
    filtered_df = filtered_df[filtered_df['caretaker_name'] == selected_caret
