"""Reusable KPI card and scorecard components using native Streamlit."""

import streamlit as st


STATUS_BADGE_MAP = {
    "green": ("On track", ":material/check_circle:", "green"),
    "yellow": ("Watch", ":material/warning:", "orange"),
    "red": ("Off track", ":material/error:", "red"),
    "grey": ("No data", ":material/help:", "gray"),
}


def render_kpi_card(
    label: str,
    value: str,
    status: str = "grey",
    delta: str | None = None,
    help_text: str | None = None,
    sparkline: list[float] | None = None,
):
    """Render a KPI card using native st.metric with badge status."""
    with st.container(border=True):
        badge_label, badge_icon, badge_color = STATUS_BADGE_MAP.get(
            status, STATUS_BADGE_MAP["grey"]
        )
        st.badge(badge_label, icon=badge_icon, color=badge_color)
        st.metric(
            label=label,
            value=value,
            delta=delta,
            help=help_text,
            border=False,
            chart_data=sparkline,
            chart_type="line" if sparkline else None,
        )


def render_company_scorecard(
    name: str,
    country: str,
    sector: str,
    kpis: list[tuple[str, str, str]],
):
    """Render a company scorecard with KPI rows and status badges.

    kpis: list of (label, value, status) tuples.
    """
    with st.container(border=True):
        st.markdown(f"**{name}**")
        st.caption(f"{country} · {sector}")

        for label, value, status in kpis:
            badge_label, badge_icon, badge_color = STATUS_BADGE_MAP.get(
                status, STATUS_BADGE_MAP["grey"]
            )
            cols = st.columns([3, 2, 2])
            with cols[0]:
                st.caption(label)
            with cols[1]:
                st.markdown(f"**{value}**")
            with cols[2]:
                st.badge(badge_label, icon=badge_icon, color=badge_color)
