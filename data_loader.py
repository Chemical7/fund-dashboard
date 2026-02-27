"""Load portfolio data from JSON and compute aggregates."""

import json
from pathlib import Path
from models import (
    PortfolioCompany, QuarterlySnapshot, ImpactMetrics,
    FinancialMetrics, OperationalMetrics, Sector,
)

DATA_DIR = Path(__file__).parent / "data"


def _build_metrics(data: dict, cls):
    """Build a dataclass instance from a dict, skipping unknown keys."""
    import dataclasses
    field_names = {f.name for f in dataclasses.fields(cls)}
    filtered = {k: v for k, v in data.items() if k in field_names}
    return cls(**filtered)


def load_companies() -> list[PortfolioCompany]:
    """Load all portfolio companies from JSON."""
    path = DATA_DIR / "portfolio_companies.json"
    raw = json.loads(path.read_text(encoding="utf-8"))

    companies = []
    for c in raw["companies"]:
        snapshots = []
        for s in c["snapshots"]:
            snap = QuarterlySnapshot(
                quarter=s["quarter"],
                is_synthetic=s.get("is_synthetic", False),
                impact=_build_metrics(s.get("impact", {}), ImpactMetrics),
                financial=_build_metrics(s.get("financial", {}), FinancialMetrics),
                operational=_build_metrics(s.get("operational", {}), OperationalMetrics),
            )
            snapshots.append(snap)

        company = PortfolioCompany(
            id=c["id"],
            name=c["name"],
            country=c["country"],
            sector=Sector(c["sector"]),
            iv_name=c["iv_name"],
            founded_year=c["founded_year"],
            description=c["description"],
            snapshots=snapshots,
        )
        companies.append(company)

    return companies


def compute_aggregates(companies: list[PortfolioCompany]) -> dict:
    """Compute portfolio-level aggregate metrics from the latest snapshot of each company."""
    total_jobs = 0
    total_beneficiaries = 0
    total_funding = 0
    female_pcts = []
    youth_pcts = []

    for co in companies:
        latest = co.latest
        if not latest:
            continue

        imp = latest.impact
        fin = latest.financial

        if imp.direct_jobs:
            total_jobs += imp.direct_jobs
        if imp.indirect_jobs:
            total_jobs += imp.indirect_jobs
        if imp.total_beneficiaries:
            total_beneficiaries += imp.total_beneficiaries
        if fin.total_funding_usd:
            total_funding += fin.total_funding_usd
        if imp.female_participation_pct is not None:
            female_pcts.append(imp.female_participation_pct)
        if imp.youth_participation_pct is not None:
            youth_pcts.append(imp.youth_participation_pct)

    avg_female = sum(female_pcts) / len(female_pcts) if female_pcts else None
    avg_youth = sum(youth_pcts) / len(youth_pcts) if youth_pcts else None

    return {
        "total_jobs": total_jobs,
        "total_beneficiaries": total_beneficiaries,
        "total_funding_usd": total_funding,
        "avg_female_pct": avg_female,
        "avg_youth_pct": avg_youth,
        "company_count": len(companies),
    }
