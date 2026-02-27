"""Geographic footprint: interactive map of portfolio company locations."""

import streamlit as st
from components.kpi_card import render_kpi_card
from components.charts import africa_map
from config import COMPANY_COLORS

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

st.title("Geographic footprint")
st.caption(f"{aggregates['company_count']} portfolio companies across West Africa")

# Build map data
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
fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True)

# Country summary below the map
countries = {}
for co in companies:
    countries.setdefault(co.country, []).append(co)

cols = st.columns(len(countries))
for i, (country, cos) in enumerate(countries.items()):
    with cols[i]:
        with st.container(border=True):
            st.subheader(f":material/location_on: {country}")
            for co in cos:
                latest = co.latest
                beneficiaries = format_number(latest.impact.total_beneficiaries) if latest and latest.impact.total_beneficiaries else "N/A"
                st.markdown(f"**{co.name}** · {co.sector.value}  \n{beneficiaries} beneficiaries")
