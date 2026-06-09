# Spacez Operations AI Dashboard

AI-Powered Review Analysis Prototype for Spacez AI Product Associate assignment.

## Overview
This is an interactive Streamlit dashboard that analyzes synthetic guest reviews for Spacez luxury villas. It demonstrates:
- Cross-platform rating normalization (/5 → /10 scale)
- Automated issue categorization and recurrence detection
- Actionable insights for Operations team
- Caretaker performance with responsibility attribution

## Features
- **Overview Tab**: Property performance metrics
- **Issue Analysis Tab**: Recurring issues (Pool, Cleanliness, Check-in, etc.) + Priority Action Queue
- **Caretaker Insights Tab**: Performance tracking with notes on multi-property patterns (e.g., Lokesh Gowda)

## Setup for Streamlit Deployment

1. Clone or download this repository
2. Place `spacez_reviews_dataset.xlsx` in the root folder
3. Run locally: `streamlit run operations_dashboard.py`
4. Or deploy directly on [Streamlit Cloud](https://share.streamlit.io/)

## Files
- `operations_dashboard.py` — Main Streamlit app
- `spacez_reviews_dataset.xlsx` — Review data

## Key Design Decisions
- Ratings are normalized before aggregation
- Issues are categorized using simple keyword matching (can be upgraded to LLM)
- Separates caretaker-controllable issues from listing/property issues
- Highlights recurring problems for quick Operations action

Built as part of the Spacez AI Product Associate take-home assignment.

---
**Submission Note**: This prototype focuses on the **Operations** stakeholder for fastest impact and clearest actionability.
