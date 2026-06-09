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
                df = pd.read_excel(path, sheet_name="Reviews", engine='openpyxl')
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
        return "Check-in Delay"
    elif any(word in text_lower for word in ['clean', 'dirty', 'housekeeping', 'bedsheet', 'unclean']):
        return "Cleanliness"
    elif any(word in text_lower for word in ['wifi', 'heating', 'ac', 'heater', 'cold']):
        return "Amenities/Facilities"
    elif any(word in text_lower for word in ['photo', 'listing', 'view', 'misleading', 'oversold']):
        return "Listing Issue"
    elif any(word in text_lower for word in ['road', 'access', 'location', 'sedan']):
        return "Location/Access"
    else:
        return "Other"

df['issue_category'] = df['review_text'].apply(categorize_issue)

# Filters
st.sidebar.header("Filters")
selected_property = st.sidebar.selectbox("Property", ["All"] + sorted(df['property_name'].unique().tolist()))
selected_caretaker = st.sidebar.selectbox("Caretaker", ["All"] + sorted(df['caretaker_name'].unique().tolist()))

filtered_df = df.copy()
if selected_property != "All":
    filtered_df = filtered_df[filtered_df['property_name'] == selected_property]
if selected_caretaker != "All":
    filtered_df = filtered_df[filtered_df['caretaker_name'] == selected_caretaker]

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Reviews", len(filtered_df))
avg_rating = filtered_df['normalized_rating'].mean() if len(filtered_df) > 0 else 0
col2.metric("Avg Normalized Rating", f"{avg_rating:.1f}/10")
col3.metric("Low Rating Reviews (<6)", len(filtered_df[filtered_df['normalized_rating'] < 6]))
col4.metric("Actionable Issues", len(filtered_df[filtered_df['issue_category'] != "Other"]))

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Issue Analysis", "👷 Caretaker Insights"])

with tab1:
    st.subheader("Property Performance")
    prop_perf = filtered_df.groupby('property_name')['normalized_rating'].agg(['mean', 'count']).round(1)
    st.dataframe(prop_perf, use_container_width=True)

with tab2:
    st.subheader("Recurring Issues")
    issues = filtered_df[filtered_df['issue_category'] != "Other"].groupby(['issue_category', 'property_name']).size().reset_index(name='count')
    issues = issues.sort_values('count', ascending=False)
    st.dataframe(issues, use_container_width=True)
    
    st.subheader("Priority Action Queue")
    high_priority = filtered_df[(filtered_df['normalized_rating'] < 6) & (filtered_df['issue_category'] != "Other")]
    if len(high_priority) == 0:
        st.success("No high priority issues currently!")
    for _, row in high_priority.iterrows():
        with st.expander(f"🔴 {row['issue_category']} at {row['property_name']} ({row['normalized_rating']}/10)"):
            st.write(row['review_text'])
            st.caption(f"Guest: {row['guest_name']} | Caretaker: {row['caretaker_name']}")

with tab3:
    st.subheader("Caretaker Insights")
    caretaker_perf = filtered_df.groupby('caretaker_name').agg({
        'normalized_rating': 'mean',
        'review_id': 'count'
    }).round(1)
    st.dataframe(caretaker_perf, use_container_width=True)
    st.info("**Key Insight:** Lokesh Gowda manages multiple properties. Check-in delays follow the caretaker.")

st.caption("Spacez AI Product Associate Prototype • Ratings normalized to /10 scale")
