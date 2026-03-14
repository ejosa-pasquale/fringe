from __future__ import annotations

from io import BytesIO

import pandas as pd

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
    rows = [
        {
            "brand": "Tesla",
            "model": "Model 3",
            "version": "RWD",
            "fuel_type": "electric",
            "aci_cost_per_km": 0.62,
            "registration_date": "2026-01-15",
            "contract_date": "2026-01-20",
            "delivery_date": "2026-02-01",
            "employee_contribution_annual": 0.0,
            "months_of_use": 12,
            "irpef_marginal_rate": 0.35,
            "manual_percentage": None,
        },
        {
            "brand": "BMW",
            "model": "X1",
            "version": "xDrive25e",
            "fuel_type": "plug_in",
            "aci_cost_per_km": 0.71,
            "registration_date": "2026-01-12",
            "contract_date": "2026-01-18",
            "delivery_date": "2026-02-05",
            "employee_contribution_annual": 0.0,
            "months_of_use": 12,
            "irpef_marginal_rate": 0.35,
            "manual_percentage": None,
        },
        {
            "brand": "Volkswagen",
            "model": "Golf",
            "version": "1.5 TSI",
            "fuel_type": "benzina",
            "aci_cost_per_km": 0.59,
            "registration_date": "2026-01-10",
            "contract_date": "2026-01-16",
            "delivery_date": "2026-02-03",
            "employee_contribution_annual": 0.0,
            "months_of_use": 12,
            "irpef_marginal_rate": 0.35,
            "manual_percentage": None,
        },
        {
            "brand": "Peugeot",
            "model": "308",
            "version": "BlueHDi",
            "fuel_type": "diesel",
            "aci_cost_per_km": 0.61,
            "registration_date": "2026-01-11",
            "contract_date": "2026-01-17",
            "delivery_date": "2026-02-04",
            "employee_contribution_annual": 0.0,
            "months_of_use": 12,
            "irpef_marginal_rate": 0.35,
            "manual_percentage": None,
        },
    ]
    df = pd.DataFrame(rows)
    for column in COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA
    return df[COLUMNS]


def empty_template_df() -> pd.DataFrame:
    return pd.DataFrame(columns=COLUMNS)


def csv_bytes_from_df(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def xlsx_bytes_from_df(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="catalogo")
    return output.getvalue()
