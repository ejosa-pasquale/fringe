from __future__ import annotations

from io import BytesIO

import pandas as pd

DEMO_CARS = [
    {
        "brand": "Demo",
        "model": "City EV",
        "version": "60 kWh",
        "fuel_type": "electric",
        "aci_cost_per_km": 0.68,
        "registration_date": "2026-01-10",
        "contract_date": "2026-01-15",
        "delivery_date": "2026-02-01",
        "employee_contribution_annual": 0,
        "months_of_use": 12,
        "irpef_marginal_rate": 0.35,
        "manual_percentage": None,
    },
    {
        "brand": "Demo",
        "model": "Family PHEV",
        "version": "1.6 Plug-in",
        "fuel_type": "plug_in",
        "aci_cost_per_km": 0.73,
        "registration_date": "2026-01-10",
        "contract_date": "2026-01-15",
        "delivery_date": "2026-02-01",
        "employee_contribution_annual": 480,
        "months_of_use": 12,
        "irpef_marginal_rate": 0.35,
        "manual_percentage": None,
    },
    {
        "brand": "Demo",
        "model": "Business Hybrid",
        "version": "2.0 Full Hybrid",
        "fuel_type": "full_hybrid",
        "aci_cost_per_km": 0.79,
        "registration_date": "2026-01-10",
        "contract_date": "2026-01-15",
        "delivery_date": "2026-02-01",
        "employee_contribution_annual": 720,
        "months_of_use": 12,
        "irpef_marginal_rate": 0.35,
        "manual_percentage": None,
    },
]

COLUMNS = [
    "brand",
    "model",
    "version",
    "fuel_type",
    "aci_cost_per_km",
    "registration_date",
    "contract_date",
    "delivery_date",
    "employee_contribution_annual",
    "months_of_use",
    "irpef_marginal_rate",
    "manual_percentage",
]


def demo_catalog_df() -> pd.DataFrame:
    return pd.DataFrame(DEMO_CARS, columns=COLUMNS)


def empty_template_df() -> pd.DataFrame:
    return pd.DataFrame(columns=COLUMNS)


def csv_bytes_from_df(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def xlsx_bytes_from_df(df: pd.DataFrame) -> bytes:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="catalogo")
    return buffer.getvalue()
