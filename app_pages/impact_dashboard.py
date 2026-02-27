"""Impact deep dive: cross-portfolio impact analysis."""

import streamlit as st
from components.charts import radar_chart, grouped_bar
from config import COMPANY_COLORS


SDG_MAP = {
    "Complete Farmer": {"SDG 1": True, "SDG 2": True, "SDG 5": True, "SDG 8": True, "SDG 9": True, "SDG 12": False, "SDG 13": False},
    "AgroEknor": {"SDG 1": True, "SDG 2": True, "SDG 5": True, "SDG 8": True, "SDG 9": True, "SDG 12": True, "SDG 13": False},
    "Koolboks": {"SDG 1": True, "SDG 2": True, "SDG 5": True, "SDG 8": True, "SDG 9": True, "SDG 12": True, "SDG 13": True},
    "Yikodeen": {"SDG 1": False, "SDG 2": False, "SDG 5": True, "SDG 8": True, "SDG 9": True, "SDG 12": True, "SDG 13": False},
    "Toasties": {"SDG 1": False, "SDG 2": False, "SDG 5": True, "SDG 8": True, "SDG 9": False, "SDG 12": True, "SDG 13": False},
}

SDG_LABELS = {
    "SDG 1": "No Poverty",
    "SDG 2": "Zero Hunger",
    "SDG 5": "Gender Equality",
    "SDG 8": "Decent Work",
    "SDG 9": "Industry & Innovation",
    "SDG 12": "Responsible Consumption",
    "SDG 13": "Climate Action",
}


def format_number(n: float | int | None) -> str:
    if n is None:
        return "N/A"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return f"{n:,.0f}"


companies = st.session_state.companies

st.title("Impact deep dive")
st.caption("Gender, youth, and employment across the portfolio")

# Compute totals
total_women_reached = 0
total_youth_reached = 0
total_lives = 0

for co in companies:
    latest = co.latest
    if not latest:
        continue
    imp = latest.impact
    beneficiaries = imp.total_beneficiaries or 0
    total_lives += beneficiaries
    if imp.female_participation_pct is not None:
        total_women_reached += int(beneficiaries * imp.female_participation_pct / 100)
    if imp.youth_participation_pct is not None:
        total_youth_reached += int(beneficiaries * imp.youth_participation_pct / 100)

# Big numbers
with st.container(horizontal=True):
    st.metric("Women reached", format_number(total_women_reached), border=True)
    st.metric("Youth engaged", format_number(total_youth_reached), border=True)
    st.metric("Total lives touched", format_number(total_lives), border=True)

# Radar chart
st.subheader("Impact profile comparison")
with st.container(border=True):
    categories = ["Female %", "Youth %", "Income uplift", "Jobs created", "Geographic reach"]
    company_data = {}
    radar_colors = {}

    for co in companies:
        latest = co.latest
        if not latest:
            continue
        imp = latest.impact
        ops = latest.operational

        female = imp.female_participation_pct or 0
        youth = imp.youth_participation_pct or 0
        income = min((imp.income_improvement_pct or 0) * 1.0, 100)
        jobs = min(((imp.direct_jobs or 0) + (imp.indirect_jobs or 0)) / 50, 100)
        geo = min((ops.countries_operating or (ops.markets_served or 1)) / 28 * 100, 100)

        company_data[co.name] = [female, youth, income, jobs, geo]
        radar_colors[co.name] = COMPANY_COLORS.get(co.id, "#00905D")

    fig = radar_chart(categories, company_data, radar_colors)
    st.plotly_chart(fig, use_container_width=True)

# Comparative bars
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        names = []
        groups = {"Female %": []}
        for co in companies:
            latest = co.latest
            if latest and latest.impact.female_participation_pct is not None:
                names.append(co.name)
                groups["Female %"].append(latest.impact.female_participation_pct)
        if names:
            fig = grouped_bar(names, groups, {"Female %": "#E879F9"}, title="Female participation", y_suffix="%")
            fig.update_layout(yaxis=dict(range=[0, 100]), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

with col2:
    with st.container(border=True):
        names = []
        groups = {"Income uplift %": []}
        for co in companies:
            latest = co.latest
            if latest and latest.impact.income_improvement_pct is not None:
                names.append(co.name)
                groups["Income uplift %"].append(latest.impact.income_improvement_pct)
        if names:
            fig = grouped_bar(names, groups, {"Income uplift %": "#FBB500"}, title="Income improvement", y_suffix="%")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

# SDG alignment
st.subheader("SDG alignment")
sdg_keys = list(SDG_LABELS.keys())

with st.container(border=True):
    header_cols = st.columns([2] + [1] * len(sdg_keys))
    with header_cols[0]:
        st.caption("**Company**")
    for i, sdg in enumerate(sdg_keys):
        with header_cols[i + 1]:
            st.caption(f"{sdg}")

    for co in companies:
        row_cols = st.columns([2] + [1] * len(sdg_keys))
        sdg_data = SDG_MAP.get(co.name, {})
        with row_cols[0]:
            st.markdown(co.name)
        for i, sdg in enumerate(sdg_keys):
            with row_cols[i + 1]:
                if sdg_data.get(sdg, False):
                    st.badge("Y", color="green")
                else:
                    st.badge("-", color="gray")
