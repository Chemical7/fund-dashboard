"""Data models for the PE Portfolio Monitoring Dashboard."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Sector(str, Enum):
    AGRITECH = "Agritech"
    AGRIBUSINESS = "Agribusiness"
    CLEANTECH = "Cleantech"
    MANUFACTURING = "Manufacturing"
    QSR = "QSR / Food"


class KPIStatus(str, Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
    GREY = "grey"


@dataclass
class ImpactMetrics:
    female_participation_pct: Optional[float] = None
    youth_participation_pct: Optional[float] = None
    total_beneficiaries: Optional[int] = None
    direct_jobs: Optional[int] = None
    indirect_jobs: Optional[int] = None
    income_improvement_pct: Optional[float] = None
    female_leadership_pct: Optional[float] = None


@dataclass
class FinancialMetrics:
    total_funding_usd: Optional[float] = None
    revenue_estimate_usd: Optional[float] = None
    gross_margin_pct: Optional[float] = None
    revenue_growth_multiple: Optional[float] = None
    default_rate_pct: Optional[float] = None


@dataclass
class OperationalMetrics:
    registered_users: Optional[int] = None
    active_users: Optional[int] = None
    acreage_managed: Optional[int] = None
    yield_increase_pct: Optional[float] = None
    protocol_adherence_pct: Optional[float] = None
    tonnes_exported: Optional[float] = None
    markets_served: Optional[int] = None
    processing_capacity_tonnes: Optional[float] = None
    daily_production_capacity: Optional[int] = None
    daily_production_target: Optional[int] = None
    locations: Optional[int] = None
    spoilage_reduction_pct: Optional[float] = None
    extra_selling_hours: Optional[float] = None
    countries_operating: Optional[int] = None


@dataclass
class QuarterlySnapshot:
    quarter: str  # e.g. "Q4 2025"
    is_synthetic: bool = False
    impact: ImpactMetrics = field(default_factory=ImpactMetrics)
    financial: FinancialMetrics = field(default_factory=FinancialMetrics)
    operational: OperationalMetrics = field(default_factory=OperationalMetrics)


@dataclass
class PortfolioCompany:
    id: str
    name: str
    country: str
    sector: Sector
    iv_name: str
    founded_year: int
    description: str
    snapshots: list[QuarterlySnapshot] = field(default_factory=list)

    @property
    def latest(self) -> Optional[QuarterlySnapshot]:
        return self.snapshots[-1] if self.snapshots else None
