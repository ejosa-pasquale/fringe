from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

import pandas as pd

from .constants import FISCAL_CATEGORY_LABELS, FUEL_LABELS, NEW_REGIME_PERCENTAGES, NEW_REGIME_START


@dataclass
class CarComputation:
    vehicle_label: str
    fuel_label: str
    regime: str
    regime_note: str
    fiscal_category: str
    percentage: float | None
    annual_reference_km: int | None
    annual_aci_reference_value: float | None
    assignment_ratio: float | None
    annual_gross_full_year: float | None
    gross_for_assignment_period: float | None
    employee_contribution_annual: float | None
    annual_net_of_contribution: float | None
    monthly_net_of_contribution: float | None
    months_of_use: float | None
    total_other_benefits: float | None
    combined_benefits: float | None
    threshold_headroom_after_car: float | None
    threshold_excess_after_car: float | None
    yearly_tax_estimate: float | None
    monthly_tax_estimate: float | None
    warning: str | None


def normalize_fuel_type(raw: str) -> str:
    value = (raw or "").strip().lower()
    mapping = {
        "electric": "electric",
        "elettrica": "electric",
        "elettrica pura": "electric",
        "bev": "electric",
        "plug_in": "plug_in",
        "plug-in": "plug_in",
        "plug in": "plug_in",
        "ibrida plug-in": "plug_in",
        "ibrida plug in": "plug_in",
        "phev": "plug_in",
        "full_hybrid": "full_hybrid",
        "full hybrid": "full_hybrid",
        "full-hybrid": "full_hybrid",
        "hev": "full_hybrid",
        "mild_hybrid": "mild_hybrid",
        "mild hybrid": "mild_hybrid",
        "mild-hybrid": "mild_hybrid",
        "mhev": "mild_hybrid",
        "benzina": "benzina",
        "diesel": "diesel",
        "altro": "other",
        "other": "other",
    }
    return mapping.get(value, "other")


def parse_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == "":
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    if isinstance(value, pd.Timestamp):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        parsed = pd.to_datetime(value, errors="coerce")
        if pd.isna(parsed):
            return None
        if isinstance(parsed, pd.Timestamp):
            return parsed.date()
        return parsed
    except Exception:
        return None


def determine_regime(
    registration_date: date | None,
    contract_date: date | None,
    delivery_date: date | None,
) -> tuple[str, str]:
    if registration_date and contract_date and delivery_date:
        if (
            registration_date >= NEW_REGIME_START
            and contract_date >= NEW_REGIME_START
            and delivery_date >= NEW_REGIME_START
        ):
            return (
                "new_2025",
                "Nuova disciplina 2025+: immatricolazione, contratto e consegna risultano dal 01/01/2025 in poi.",
            )
    return (
        "manual_review",
        "Il caso non ricade automaticamente nella nuova disciplina 2025+. Serve verifica payroll per regime precedente o transitorio.",
    )


def fiscal_category_for_fuel(fuel_type: str) -> str:
    if fuel_type == "electric":
        return FISCAL_CATEGORY_LABELS["electric"]
    if fuel_type == "plug_in":
        return FISCAL_CATEGORY_LABELS["plug_in"]
    return FISCAL_CATEGORY_LABELS["other"]


def _safe_float(value: Any, default: float | None = None) -> float | None:
    if value is None or value == "":
        return default
    try:
        if pd.isna(value):
            return default
    except Exception:
        pass
    try:
        return float(value)
    except Exception:
        return default


def _build_warning(aci_cost: float | None, percentage: float | None, fuel_type: str, regime: str) -> str | None:
    warnings: list[str] = []
    if aci_cost is None:
        warnings.append("manca il costo ACI")
    if regime == "manual_review" and percentage is None:
        warnings.append("compilare manual_percentage o validare il caso")
    if fuel_type == "other":
        warnings.append("verificare la classificazione del veicolo")
    if not warnings:
        return None
    return "; ".join(warnings)


def compute_car_benefit(
    row: pd.Series,
    threshold_amount: float,
    other_benefits_amount: float,
) -> CarComputation:
    fuel_type = normalize_fuel_type(str(row.get("fuel_type", "")))
    registration_date = parse_date(row.get("registration_date"))
    contract_date = parse_date(row.get("contract_date"))
    delivery_date = parse_date(row.get("delivery_date"))
    regime, regime_note = determine_regime(registration_date, contract_date, delivery_date)

    manual_percentage = _safe_float(row.get("manual_percentage"))
    if regime == "new_2025":
        percentage = NEW_REGIME_PERCENTAGES[fuel_type]
    else:
        percentage = manual_percentage

    aci_cost = _safe_float(row.get("aci_cost_per_km"))
    months = _safe_float(row.get("months_of_use"), 12.0) or 12.0
    months = max(min(months, 12.0), 1.0)
    contribution = _safe_float(row.get("employee_contribution_annual"), 0.0) or 0.0
    irpef = _safe_float(row.get("irpef_marginal_rate"))

    vehicle_label = " - ".join(
        part
        for part in [str(row.get("brand", "")).strip(), str(row.get("model", "")).strip(), str(row.get("version", "")).strip()]
        if part
    )

    warning = _build_warning(aci_cost, percentage, fuel_type, regime)

    if aci_cost is None or percentage is None:
        return CarComputation(
            vehicle_label=vehicle_label or "Veicolo",
            fuel_label=FUEL_LABELS[fuel_type],
            regime=regime,
            regime_note=regime_note,
            fiscal_category=fiscal_category_for_fuel(fuel_type),
            percentage=percentage,
            annual_reference_km=15000 if aci_cost is not None else None,
            annual_aci_reference_value=(float(aci_cost) * 15000) if aci_cost is not None else None,
            assignment_ratio=months / 12,
            annual_gross_full_year=None,
            gross_for_assignment_period=None,
            employee_contribution_annual=contribution,
            annual_net_of_contribution=None,
            monthly_net_of_contribution=None,
            months_of_use=months,
            total_other_benefits=other_benefits_amount,
            combined_benefits=None,
            threshold_headroom_after_car=None,
            threshold_excess_after_car=None,
            yearly_tax_estimate=None,
            monthly_tax_estimate=None,
            warning=warning,
        )

    annual_reference_km = 15000
    annual_aci_reference_value = float(aci_cost) * annual_reference_km
    annual_gross_full_year = annual_aci_reference_value * float(percentage)
    assignment_ratio = months / 12
    gross_for_assignment_period = annual_gross_full_year * assignment_ratio
    annual_net = max(gross_for_assignment_period - float(contribution), 0.0)
    monthly_net = annual_net / months
    combined = other_benefits_amount + annual_net
    headroom = max(threshold_amount - combined, 0.0)
    excess = max(combined - threshold_amount, 0.0)

    yearly_tax = None
    monthly_tax = None
    if irpef is not None:
        yearly_tax = annual_net * irpef
        monthly_tax = yearly_tax / months

    return CarComputation(
        vehicle_label=vehicle_label or "Veicolo",
        fuel_label=FUEL_LABELS[fuel_type],
        regime=regime,
        regime_note=regime_note,
        fiscal_category=fiscal_category_for_fuel(fuel_type),
        percentage=float(percentage),
        annual_reference_km=annual_reference_km,
        annual_aci_reference_value=annual_aci_reference_value,
        assignment_ratio=assignment_ratio,
        annual_gross_full_year=annual_gross_full_year,
        gross_for_assignment_period=gross_for_assignment_period,
        employee_contribution_annual=contribution,
        annual_net_of_contribution=annual_net,
        monthly_net_of_contribution=monthly_net,
        months_of_use=months,
        total_other_benefits=other_benefits_amount,
        combined_benefits=combined,
        threshold_headroom_after_car=headroom,
        threshold_excess_after_car=excess,
        yearly_tax_estimate=yearly_tax,
        monthly_tax_estimate=monthly_tax,
        warning=warning,
    )


def compute_car_dataframe(df: pd.DataFrame, threshold_amount: float, other_benefits_amount: float) -> pd.DataFrame:
    results = [compute_car_benefit(row, threshold_amount, other_benefits_amount) for _, row in df.iterrows()]
    return pd.DataFrame([result.__dict__ for result in results])
