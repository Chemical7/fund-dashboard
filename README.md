# Fund Dashboard

PE portfolio monitoring dashboard for Fund IV. Streamlit web app with interactive Plotly charts and traffic-light KPI tracking.

## Pages

- **Portfolio Overview** - Multi-company view with map, sector breakdown, and aggregated metrics
- **Company Detail** - Single company drill-down with quarterly trend charts
- **Impact Deep Dive** - Cross-portfolio impact analysis and SDG mapping

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Data

Portfolio company data lives in `data/portfolio_companies.json`. KPI targets and thresholds are configured in `data/kpi_targets.json` and `config.py`.

Current data is synthetic (demo purposes, labeled in UI).
