"""Brand colors, traffic light thresholds, and layout constants."""

# Brand palette
BRAND = {
    "green": "#00905D",
    "gold": "#FBB500",
    "orange": "#FF6C05",
}

# Dark theme
THEME = {
    "bg": "#0E1117",
    "card_bg": "#1B1F2B",
    "card_border": "#2A2F3F",
    "text_primary": "#FAFAFA",
    "text_secondary": "#9CA3AF",
    "text_muted": "#6B7280",
}

# Traffic light colors
TRAFFIC = {
    "green": "#10B981",
    "yellow": "#F59E0B",
    "red": "#EF4444",
    "grey": "#6B7280",
}

# Company accent colors (for charts)
COMPANY_COLORS = {
    "complete-farmer": "#00905D",
    "agroeknor": "#FBB500",
    "koolboks": "#3B82F6",
    "yikodeen": "#FF6C05",
    "toasties": "#8B5CF6",
}

# Traffic light targets: (target_value, higher_is_better)
KPI_TARGETS = {
    "female_participation_pct": (35.0, True),   # 35% is strong in African PE context
    "youth_participation_pct": (40.0, True),
    "income_improvement_pct": (10.0, True),
    "default_rate_pct": (5.0, False),
    "yield_increase_pct": (20.0, True),         # 20% yield increase is significant
    "protocol_adherence_pct": (80.0, True),
    "gross_margin_pct": (35.0, True),
    "spoilage_reduction_pct": (40.0, True),
}

# Variance thresholds
GREEN_THRESHOLD = 0.05   # within 5% of target
YELLOW_THRESHOLD = 0.15  # within 15% of target


def evaluate_status(metric_key: str, value: float | None) -> str:
    """Evaluate a KPI value against its target and return a traffic light status."""
    if value is None:
        return "grey"
    if metric_key not in KPI_TARGETS:
        return "grey"

    target, higher_is_better = KPI_TARGETS[metric_key]

    if higher_is_better:
        ratio = value / target if target else 1.0
        if ratio >= (1.0 - GREEN_THRESHOLD):
            return "green"
        elif ratio >= (1.0 - YELLOW_THRESHOLD):
            return "yellow"
        else:
            return "red"
    else:
        # Lower is better (e.g., default rate)
        ratio = value / target if target else 1.0
        if ratio <= (1.0 + GREEN_THRESHOLD):
            return "green"
        elif ratio <= (1.0 + YELLOW_THRESHOLD):
            return "yellow"
        else:
            return "red"
