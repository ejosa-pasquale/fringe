from __future__ import annotations

from datetime import date

NEW_REGIME_START = date(2025, 1, 1)

NEW_REGIME_PERCENTAGES = {
    "electric": 0.10,
    "plug_in": 0.20,
    "full_hybrid": 0.50,
    "mild_hybrid": 0.50,
    "benzina": 0.50,
    "diesel": 0.50,
    "other": 0.50,
}

FUEL_LABELS = {
    "electric": "Elettrica pura",
    "plug_in": "Ibrida plug-in",
    "full_hybrid": "Full hybrid",
    "mild_hybrid": "Mild hybrid",
    "benzina": "Benzina",
    "diesel": "Diesel",
    "other": "Altro veicolo",
}

FISCAL_CATEGORY_LABELS = {
    "electric": "10% - elettrica pura",
    "plug_in": "20% - ibrida plug-in",
    "other": "50% - altri veicoli",
}

TIPOLOGY_A_DESC = "ricarica in corrente alternata almeno 7,4 kW e 32 A per fase"
TIPOLOGY_B_DESC = "ricarica in corrente continua 50 kW"
