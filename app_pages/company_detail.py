"""Company detail: drill-down for a single portfolio company."""

import streamlit as st
from components.kpi_card import render_kpi_card
from components.charts import line_chart, donut_chart
from config import COMPANY_COLORS, evaluate_status


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

# Company selector
company_names = [co.name for co in companies]
selected_name = st.selectbox(
    "Select company",
    company_names,
    label_visibility="collapsed",
)
company = next(co for co in companies if co.name == selected_name)
accent = COMPANY_COLORS.get(company.id, "#00905D")

# Header
st.title(company.name)
st.caption(f"{company.country} · {company.sector.value} · Founded {company.founded_year} · IV: {company.iv_name}")
st.markdown(company.description)

# KPIs
latest = company.latest
if latest:
    imp = latest.impact
    fin = latest.financial
    ops = latest.operational

    kpis = []

    if imp.female_participation_pct is not None:
        kpis.append(("Female participation", f"{imp.female_participation_pct:.0f}%",
                      evaluate_status("female_participation_pct", imp.female_participation_pct)))
    if imp.youth_participation_pct is not None:
        kpis.append(("Youth participation", f"{imp.youth_participation_pct:.0f}%",
                      evaluate_status("youth_participation_pct", imp.youth_participation_pct)))
    if imp.income_improvement_pct is not None:
        kpis.append(("Income improvement", f"{imp.income_improvement_pct:.0f}%",
                      evaluate_status("income_improvement_pct", imp.income_improvement_pct)))
    if ops.registered_users is not None:
        kpis.append(("Registered users", format_number(ops.registered_users), "grey"))
    if ops.active_users is not None:
        kpis.append(("Active users", format_number(ops.active_users), "grey"))
    if ops.acreage_managed is not None:
        kpis.append(("Acreage managed", format_number(ops.acreage_managed), "grey"))
    if ops.yield_increase_pct is not None:
        kpis.append(("Yield increase", f"{ops.yield_increase_pct:.0f}%",
                      evaluate_status("yield_increase_pct", ops.yield_increase_pct)))
    if ops.protocol_adherence_pct is not None:
        kpis.append(("Protocol adherence", f"{ops.protocol_adherence_pct:.0f}%",
                      evaluate_status("protocol_adherence_pct", ops.protocol_adherence_pct)))
    if ops.tonnes_exported is not None:
        kpis.append(("Tonnes exported", format_number(ops.tonnes_exported), "grey"))
    if ops.markets_served is not None:
        kpis.append(("Markets served", str(ops.markets_served), "grey"))
    if ops.spoilage_reduction_pct is not None:
        kpis.append(("Spoilage reduction", f"{ops.spoilage_reduction_pct:.0f}%",
                      evaluate_status("spoilage_reduction_pct", ops.spoilage_reduction_pct)))
    if fin.default_rate_pct is not None:
        kpis.append(("PAYG default rate", f"{fin.default_rate_pct:.1f}%",
                      evaluate_status("default_rate_pct", fin.default_rate_pct)))
    if fin.gross_margin_pct is not None:
        kpis.append(("Gross margin", f">{fin.gross_margin_pct:.0f}%",
                      evaluate_status("gross_margin_pct", fin.gross_margin_pct)))
    if ops.daily_production_capacity is not None:
        kpis.append(("Daily capacity", f"{ops.daily_production_capacity:,} units", "grey"))
    if ops.locations is not None:
        kpis.append(("Locations", str(ops.locations), "grey"))
    if imp.direct_jobs is not None:
        kpis.append(("Direct jobs", format_number(imp.direct_jobs), "grey"))

    st.subheader("Key performance indicators")

    for row_start in range(0, min(len(kpis), 9), 3):
        row_kpis = kpis[row_start:row_start + 3]
        cols = st.columns(3)
        for j, (label, value, status) in enumerate(row_kpis):
            with cols[j]:
                render_kpi_card(label, value, status)

# Time-series
if len(company.snapshots) > 1:
    has_synthetic = any(s.is_synthetic for s in company.snapshots)
    if has_synthetic:
        st.info(
            "Synthetic time-series for illustration. Connect your reporting pipeline to replace with actuals.",
            icon=":material/science:",
        )

    st.subheader("Trends")
    quarters = [s.quarter for s in company.snapshots]
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            if company.snapshots[0].operational.registered_users is not None:
                series = {"Registered users": [s.operational.registered_users or 0 for s in company.snapshots]}
                fig = line_chart(quarters, series, {list(series.keys())[0]: accent}, title="User growth")
                st.plotly_chart(fig, use_container_width=True)
            elif company.snapshots[0].operational.spoilage_reduction_pct is not None:
                series = {"Spoilage reduction": [s.operational.spoilage_reduction_pct or 0 for s in company.snapshots]}
                fig = line_chart(quarters, series, {list(series.keys())[0]: accent}, title="Spoilage reduction (%)", y_suffix="%")
                st.plotly_chart(fig, use_container_width=True)

    with col2:
        with st.container(border=True):
            if company.snapshots[0].impact.female_participation_pct is not None:
                series = {"Female %": [s.impact.female_participation_pct or 0 for s in company.snapshots]}
                fig = line_chart(quarters, series, {list(series.keys())[0]: "#E879F9"}, title="Female participation (%)", y_suffix="%")
                fig.update_layout(yaxis=dict(range=[0, 100]))
                st.plotly_chart(fig, use_container_width=True)
else:
    with st.container(border=True):
        st.caption("Time-series data not yet available. Connect quarterly reporting pipeline to enable trend analysis.")

# Impact profile
if latest:
    imp = latest.impact
    cols_available = []
    if imp.female_participation_pct is not None:
        cols_available.append("gender")
    if imp.youth_participation_pct is not None:
        cols_available.append("youth")
    if imp.direct_jobs is not None:
        cols_available.append("jobs")

    if cols_available:
        st.subheader("Impact profile")
        d_cols = st.columns(len(cols_available))

        for idx, col_type in enumerate(cols_available):
            with d_cols[idx]:
                with st.container(border=True):
                    if col_type == "gender":
                        male = 100 - imp.female_participation_pct
                        fig = donut_chart(
                            ["Female", "Male"],
                            [imp.female_participation_pct, male],
                            [accent, "#4B5563"],
                            title="Gender split",
                            center_text=f"{imp.female_participation_pct:.0f}%",
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    elif col_type == "youth":
                        non_youth = 100 - imp.youth_participation_pct
                        fig = donut_chart(
                            ["Youth (<30)", "Other"],
                            [imp.youth_participation_pct, non_youth],
                            ["#FBB500", "#4B5563"],
                            title="Youth split",
                            center_text=f"{imp.youth_participation_pct:.0f}%",
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    elif col_type == "jobs":
                        vals = [imp.direct_jobs]
                        labels = ["Direct jobs"]
                        colors = ["#FF6C05"]
                        if imp.indirect_jobs:
                            vals.append(imp.indirect_jobs)
                            labels.append("Indirect jobs")
                            colors.append("#4B5563")
                        fig = donut_chart(
                            labels, vals, colors,
                            title="Employment",
                            center_text=format_number(sum(vals)),
                        )
                        st.plotly_chart(fig, use_container_width=True)

# Funding
if latest and latest.financial.total_funding_usd:
    st.subheader("Funding")
    st.metric(
        "Total capital raised",
        format_number(latest.financial.total_funding_usd, currency=True),
        border=True,
    )
