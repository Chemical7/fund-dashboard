"""Portfolio overview: all companies at a glance."""

import streamlit as st
from components.kpi_card import render_kpi_card, render_company_scorecard
from components.charts import horizontal_bar, africa_map
from config import COMPANY_COLORS, evaluate_status

COUNTRY_COORDS = {
    "Ghana": (7.95, -1.02),
    "Nigeria": (9.08, 7.49),
}


def format_number(n: float | int | None, currency: bool = False) -> str:
    if n is None:
        return "N/A"
    prefix = "$" if currency else ""
    if n >= 1_000_000:
        return f"{prefix}{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{prefix}{n / 1_000:.1f}K"
    return f"{prefix}{n:,.0f}"


companies = st.session_state.companies
aggregates = st.session_state.aggregates

# Header
st.title("Portfolio overview")
st.caption(f"Last updated Q4 2025 · {aggregates['company_count']} portfolio companies")

# Aggregate KPIs
with st.container(horizontal=True):
    st.metric(
        "Total beneficiaries",
        format_number(aggregates["total_beneficiaries"]),
        help="Across all portfolio companies",
        border=True,
    )
    st.metric(
        "Jobs created",
        format_number(aggregates["total_jobs"]),
        help="Direct + indirect",
        border=True,
    )
    avg_f = aggregates.get("avg_female_pct")
    st.metric(
        "Avg female participation",
        f"{avg_f:.0f}%" if avg_f else "N/A",
        border=True,
    )
    st.metric(
        "Funding deployed",
        format_number(aggregates["total_funding_usd"], currency=True),
        help="Equity + debt + grants",
        border=True,
    )

# Company scorecards
st.subheader("Portfolio companies")
card_cols = st.columns(len(companies))

for i, co in enumerate(companies):
    latest = co.latest
    if not latest:
        continue

    imp = latest.impact
    fin = latest.financial
    ops = latest.operational

    kpis = []
    if imp.female_participation_pct is not None:
        kpis.append((
            "Female %",
            f"{imp.female_participation_pct:.0f}%",
            evaluate_status("female_participation_pct", imp.female_participation_pct),
        ))
    if imp.total_beneficiaries is not None:
        kpis.append(("Beneficiaries", format_number(imp.total_beneficiaries), "grey"))
    if imp.income_improvement_pct is not None:
        kpis.append((
            "Income uplift",
            f"{imp.income_improvement_pct:.0f}%",
            evaluate_status("income_improvement_pct", imp.income_improvement_pct),
        ))
    if ops.yield_increase_pct is not None:
        kpis.append((
            "Yield increase",
            f"{ops.yield_increase_pct:.0f}%",
            evaluate_status("yield_increase_pct", ops.yield_increase_pct),
        ))
    if fin.gross_margin_pct is not None:
        kpis.append((
            "Gross margin",
            f"{fin.gross_margin_pct:.0f}%",
            evaluate_status("gross_margin_pct", fin.gross_margin_pct),
        ))
    if fin.default_rate_pct is not None:
        kpis.append((
            "Default rate",
            f"{fin.default_rate_pct:.1f}%",
            evaluate_status("default_rate_pct", fin.default_rate_pct),
        ))
    if ops.spoilage_reduction_pct is not None:
        kpis.append((
            "Spoilage reduction",
            f"{ops.spoilage_reduction_pct:.0f}%",
            evaluate_status("spoilage_reduction_pct", ops.spoilage_reduction_pct),
        ))
    if ops.daily_production_capacity is not None and ops.daily_production_target:
        utilization = ops.daily_production_capacity / ops.daily_production_target * 100
        kpis.append((
            "Capacity utilization",
            f"{utilization:.0f}%",
            "yellow" if utilization < 50 else "green",
        ))
    if imp.youth_participation_pct is not None:
        kpis.append((
            "Youth %",
            f"{imp.youth_participation_pct:.0f}%",
            evaluate_status("youth_participation_pct", imp.youth_participation_pct),
        ))

    kpis = kpis[:4]

    with card_cols[i]:
        render_company_scorecard(
            name=co.name,
            country=co.country,
            sector=co.sector.value,
            kpis=kpis,
        )

# Charts
col_left, col_right = st.columns(2)

with col_left:
    with st.container(border=True):
        names, vals, colors = [], [], []
        for co in companies:
            latest = co.latest
            if latest and latest.impact.total_beneficiaries:
                names.append(co.name)
                vals.append(latest.impact.total_beneficiaries)
                colors.append(COMPANY_COLORS.get(co.id, "#00905D"))
        if names:
            fig = horizontal_bar(names, vals, colors, title="Total beneficiaries by company")
            st.plotly_chart(fig, use_container_width=True)

with col_right:
    with st.container(border=True):
        names, female_vals, colors_list = [], [], []
        for co in companies:
            latest = co.latest
            if latest and latest.impact.female_participation_pct is not None:
                names.append(co.name)
                female_vals.append(latest.impact.female_participation_pct)
                colors_list.append(COMPANY_COLORS.get(co.id, "#00905D"))
        if names:
            fig = horizontal_bar(
                names, female_vals, colors_list,
                title="Female participation by company",
                value_suffix="%",
            )
            fig.update_layout(xaxis=dict(range=[0, 100]))
            st.plotly_chart(fig, use_container_width=True)

# Map
st.subheader("Geographic footprint")
with st.container(border=True):
    map_names, map_lats, map_lons, map_sizes, map_colors, map_hovers = [], [], [], [], [], []
    for co in companies:
        lat, lon = COUNTRY_COORDS.get(co.country, (0, 0))
        if co.country == "Nigeria":
            offset = {"agroeknor": (-1.5, -2), "koolboks": (1.5, -1), "yikodeen": (-0.5, 2), "toasties": (1.0, 1.5)}
            dx, dy = offset.get(co.id, (0, 0))
            lat += dx
            lon += dy

        latest = co.latest
        size = latest.impact.total_beneficiaries if latest and latest.impact.total_beneficiaries else 1000
        map_names.append(co.name)
        map_lats.append(lat)
        map_lons.append(lon)
        map_sizes.append(size)
        map_colors.append(COMPANY_COLORS.get(co.id, "#00905D"))
        map_hovers.append(f"<b>{co.name}</b><br>{co.country} | {co.sector.value}<br>Beneficiaries: {format_number(size)}")

    fig = africa_map(map_names, map_lats, map_lons, map_sizes, map_colors, map_hovers)
    st.plotly_chart(fig, use_container_width=True)
