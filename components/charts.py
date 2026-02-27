"""Plotly chart factory functions for the portfolio dashboard."""

import plotly.graph_objects as go
import plotly.express as px


def _hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    """Convert hex color to rgba string for Plotly compatibility."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


# Shared layout defaults
_LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FAFAFA", family="Inter, sans-serif"),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
    ),
)


def horizontal_bar(labels: list[str], values: list[float], colors: list[str],
                   title: str = "", value_suffix: str = "") -> go.Figure:
    """Horizontal bar chart for comparing a single metric across companies."""
    fig = go.Figure(go.Bar(
        y=labels,
        x=values,
        orientation="h",
        marker_color=colors,
        text=[f"{v:,.0f}{value_suffix}" for v in values],
        textposition="auto",
        textfont=dict(color="#FAFAFA", size=12),
    ))
    fig.update_layout(
        **_LAYOUT_DEFAULTS,
        title=dict(text=title, font=dict(size=14)),
        height=280,
        yaxis=dict(autorange="reversed", gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(showgrid=False, showticklabels=False),
    )
    return fig


def donut_chart(labels: list[str], values: list[float], colors: list[str],
                title: str = "", center_text: str = "") -> go.Figure:
    """Donut/ring chart for proportional breakdowns."""
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors),
        textinfo="label+percent",
        textfont=dict(size=11, color="#FAFAFA"),
        hovertemplate="%{label}: %{value:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        **_LAYOUT_DEFAULTS,
        title=dict(text=title, font=dict(size=14)),
        height=300,
        showlegend=False,
        annotations=[dict(
            text=center_text, x=0.5, y=0.5,
            font=dict(size=16, color="#FAFAFA", family="Inter, sans-serif"),
            showarrow=False,
        )] if center_text else [],
    )
    return fig


def line_chart(quarters: list[str], series: dict[str, list[float]],
               colors: dict[str, str], title: str = "",
               y_suffix: str = "") -> go.Figure:
    """Multi-series line chart for time-series trends."""
    fig = go.Figure()
    for name, values in series.items():
        fig.add_trace(go.Scatter(
            x=quarters,
            y=values,
            mode="lines+markers",
            name=name,
            line=dict(color=colors.get(name, "#FAFAFA"), width=2.5),
            marker=dict(size=7),
            hovertemplate=f"%{{x}}: %{{y:,.1f}}{y_suffix}<extra>{name}</extra>",
        ))
    fig.update_layout(
        **_LAYOUT_DEFAULTS,
        title=dict(text=title, font=dict(size=14)),
        height=320,
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
    )
    return fig


def radar_chart(categories: list[str], company_data: dict[str, list[float]],
                colors: dict[str, str], title: str = "") -> go.Figure:
    """Radar/spider chart for comparing impact profiles."""
    fig = go.Figure()
    for name, values in company_data.items():
        # Close the polygon
        vals = values + [values[0]]
        cats = categories + [categories[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals,
            theta=cats,
            fill="toself",
            name=name,
            line=dict(color=colors.get(name, "#FAFAFA"), width=2),
            fillcolor=_hex_to_rgba(colors.get(name, "#FAFAFA"), 0.12),
        ))
    fig.update_layout(
        **_LAYOUT_DEFAULTS,
        title=dict(text=title, font=dict(size=14)),
        height=400,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.1)",
                range=[0, 100],
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.1)",
            ),
        ),
    )
    return fig


def africa_map(names: list[str], lats: list[float], lons: list[float],
               sizes: list[float], colors: list[str],
               hover_texts: list[str]) -> go.Figure:
    """Scatter geo map of Africa showing portfolio company locations."""
    fig = go.Figure(go.Scattergeo(
        lat=lats,
        lon=lons,
        text=names,
        hovertext=hover_texts,
        hoverinfo="text",
        marker=dict(
            size=[max(s / 1500, 14) for s in sizes],
            color=colors,
            line=dict(width=2, color="#FAFAFA"),
            opacity=0.9,
        ),
        mode="markers+text",
        textposition="top center",
        textfont=dict(color="#FAFAFA", size=11),
    ))
    fig.update_layout(
        **_LAYOUT_DEFAULTS,
        height=420,
        geo=dict(
            scope="africa",
            bgcolor="rgba(0,0,0,0)",
            lakecolor="rgba(0,0,0,0)",
            landcolor="#1B1F2B",
            countrycolor="#2A2F3F",
            coastlinecolor="#2A2F3F",
            showframe=False,
            showocean=True,
            oceancolor="#0E1117",
            projection_type="natural earth",
            lonaxis=dict(range=[-20, 55]),
            lataxis=dict(range=[-5, 20]),
        ),
    )
    return fig


def grouped_bar(categories: list[str], groups: dict[str, list[float]],
                colors: dict[str, str], title: str = "",
                y_suffix: str = "") -> go.Figure:
    """Grouped bar chart for comparing metrics across companies."""
    fig = go.Figure()
    for name, values in groups.items():
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            name=name,
            marker_color=colors.get(name, "#FAFAFA"),
            text=[f"{v:.0f}{y_suffix}" if v else "" for v in values],
            textposition="auto",
            textfont=dict(color="#FAFAFA", size=11),
        ))
    fig.update_layout(
        **_LAYOUT_DEFAULTS,
        title=dict(text=title, font=dict(size=14)),
        height=320,
        barmode="group",
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
    )
    return fig


def data_completeness_heatmap(companies: list[str], categories: list[str],
                               values: list[list[float]]) -> go.Figure:
    """Heatmap showing data completeness per company per KPI category."""
    colorscale = [
        [0.0, "#EF4444"],
        [0.5, "#F59E0B"],
        [1.0, "#10B981"],
    ]
    fig = go.Figure(go.Heatmap(
        z=values,
        x=categories,
        y=companies,
        colorscale=colorscale,
        showscale=False,
        text=[[f"{int(v*100)}%" for v in row] for row in values],
        texttemplate="%{text}",
        textfont=dict(size=12, color="#FAFAFA"),
        hovertemplate="%{y} - %{x}: %{text}<extra></extra>",
    ))
    fig.update_layout(
        **_LAYOUT_DEFAULTS,
        height=250,
        xaxis=dict(side="top"),
        yaxis=dict(autorange="reversed"),
    )
    return fig
