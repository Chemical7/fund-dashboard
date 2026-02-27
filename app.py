"""PE Portfolio Monitoring Dashboard — Streamlit entry point.

Run with:
    cd .sys/tools/dashboard
    streamlit run app.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from data_loader import load_companies, compute_aggregates

st.set_page_config(
    page_title="Portfolio Monitor",
    page_icon=":material/monitoring:",
    layout="wide",
)


@st.cache_data
def get_data():
    companies = load_companies()
    aggregates = compute_aggregates(companies)
    return companies, aggregates


# Load data into session state
companies, aggregates = get_data()
st.session_state.setdefault("companies", companies)
st.session_state.setdefault("aggregates", aggregates)

# Navigation
page = st.navigation(
    [
        st.Page("app_pages/portfolio_overview.py", title="Portfolio overview", icon=":material/dashboard:"),
        st.Page("app_pages/company_detail.py", title="Company detail", icon=":material/business:"),
        st.Page("app_pages/impact_dashboard.py", title="Impact deep dive", icon=":material/diversity_3:"),
    ],
    position="sidebar",
)

# Shared sidebar content
with st.sidebar:
    st.caption("Prototype v0.1 · Q4 2025 data\nBuilt by ACG Digital Solutions")

page.run()
