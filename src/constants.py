from __future__ import annotations

from datetime import date

NEW_REGIME_START = date(2025, 1, 1)
DM_MATURED_DEADLINE = date(2025, 1, 1)
DM_FINAL_DEADLINE = date(2030, 1, 1)

FUEL_LABELS = {
    "electric": "Elettrica pura",
    "plug_in": "Ibrida plug-in",
    "full_hybrid": "Full hybrid",
    "mild_hybrid": "Mild hybrid",
    "benzina": "Benzina",
    "diesel": "Diesel",
    "other": "Altro",
}

NEW_REGIME_PERCENTAGES = {
    "electric": 0.10,
    "plug_in": 0.20,
    "full_hybrid": 0.50,
    "mild_hybrid": 0.50,
    "benzina": 0.50,
    "diesel": 0.50,
    "other": 0.50,
}

FISCAL_CATEGORY_LABELS = {
    "electric": "Veicolo elettrico puro",
    "plug_in": "Veicolo ibrido plug-in",
    "other": "Altro veicolo",
}

CHARGING_ACCESS_LABELS = {
    "private": "Accesso privato",
    "public": "Accesso pubblico",
}

INTERVENTION_LABELS = {
    "new": "Nuova costruzione",
    "major_renovation": "Ristrutturazione importante",
    "existing": "Edificio esistente",
}

TIPOLOGY_A_DESC = "Punto di ricarica Tipologia A (>= 7,4 kW, >= 32 A per fase)"
TIPOLOGY_B_DESC = "Punto di ricarica Tipologia B (DC >= 50 kW)"
