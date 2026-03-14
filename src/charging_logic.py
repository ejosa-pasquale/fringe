from __future__ import annotations

from dataclasses import dataclass, field
from math import floor


@dataclass
class RequirementOption:
    label: str
    min_a: int = 0
    min_b: int = 0
    canalization_required: bool = False
    canalization_spaces: int = 0


@dataclass
class ChargingAssessment:
    applicable: bool
    status: str
    note: str
    access_type: str
    intervention_type: str
    parking_spaces: int
    target_now: list[RequirementOption] = field(default_factory=list)
    target_2030: list[RequirementOption] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)


def _canalization_spaces(parking_spaces: int) -> int:
    return floor(parking_spaces / 5)


def _private_new(parking_spaces: int) -> list[RequirementOption]:
    canal = _canalization_spaces(parking_spaces) if parking_spaces > 10 else 0
    if 11 <= parking_spaces <= 20:
        return [RequirementOption("Configurazione minima", min_a=3, canalization_required=True, canalization_spaces=canal)]
    if 21 <= parking_spaces <= 100:
        return [RequirementOption("Configurazione minima", min_a=3 * floor(parking_spaces / 20), canalization_required=True, canalization_spaces=canal)]
    if 101 <= parking_spaces <= 500:
        return [
            RequirementOption("Opzione A", min_a=3 * floor(parking_spaces / 50), canalization_required=True, canalization_spaces=canal),
            RequirementOption("Opzione B", min_b=1, canalization_required=True, canalization_spaces=canal),
        ]
    if 501 <= parking_spaces <= 1000:
        return [RequirementOption("Configurazione minima", min_b=2, canalization_required=True, canalization_spaces=canal)]
    if parking_spaces > 1000:
        return [RequirementOption("Configurazione minima", min_b=3, canalization_required=True, canalization_spaces=canal)]
    return []


def _private_major(parking_spaces: int) -> list[RequirementOption]:
    canal = _canalization_spaces(parking_spaces) if parking_spaces > 10 else 0
    if 11 <= parking_spaces <= 20:
        return [RequirementOption("Configurazione minima", min_a=2, canalization_required=True, canalization_spaces=canal)]
    if 21 <= parking_spaces <= 100:
        return [RequirementOption("Configurazione minima", min_a=2 * floor(parking_spaces / 20), canalization_required=True, canalization_spaces=canal)]
    if 101 <= parking_spaces <= 500:
        return [RequirementOption("Configurazione minima", min_a=2 * floor(parking_spaces / 50), canalization_required=True, canalization_spaces=canal)]
    if 501 <= parking_spaces <= 1000:
        return [RequirementOption("Configurazione minima", min_b=1, canalization_required=True, canalization_spaces=canal)]
    if parking_spaces > 1000:
        return [RequirementOption("Configurazione minima", min_b=2, canalization_required=True, canalization_spaces=canal)]
    return []


def _private_existing(parking_spaces: int) -> list[RequirementOption]:
    if 21 <= parking_spaces <= 100:
        return [RequirementOption("Configurazione minima", min_a=3 * floor(parking_spaces / 20))]
    if 101 <= parking_spaces <= 500:
        return [
            RequirementOption("Opzione A", min_a=3 * floor(parking_spaces / 50)),
            RequirementOption("Opzione B", min_b=1),
        ]
    if 501 <= parking_spaces <= 1000:
        return [RequirementOption("Configurazione minima", min_b=2)]
    if parking_spaces > 1000:
        return [RequirementOption("Configurazione minima", min_b=3)]
    return []


def _public_new(parking_spaces: int) -> list[RequirementOption]:
    canal = _canalization_spaces(parking_spaces) if parking_spaces > 10 else 0
    if 11 <= parking_spaces <= 20:
        return [RequirementOption("Configurazione minima", min_a=2, canalization_required=True, canalization_spaces=canal)]
    if 21 <= parking_spaces <= 100:
        return [RequirementOption("Configurazione minima", min_a=2 * floor(parking_spaces / 20), canalization_required=True, canalization_spaces=canal)]
    if 101 <= parking_spaces <= 250:
        return [
            RequirementOption("Opzione A", min_a=2 * floor(parking_spaces / 50), canalization_required=True, canalization_spaces=canal),
            RequirementOption("Opzione B", min_b=1, canalization_required=True, canalization_spaces=canal),
        ]
    if 251 <= parking_spaces <= 500:
        return [RequirementOption("Configurazione minima", min_b=2, canalization_required=True, canalization_spaces=canal)]
    if 501 <= parking_spaces <= 1000:
        return [RequirementOption("Configurazione minima", min_b=3, canalization_required=True, canalization_spaces=canal)]
    if parking_spaces > 1000:
        return [RequirementOption("Configurazione minima", min_b=4, canalization_required=True, canalization_spaces=canal)]
    return []


def _public_major(parking_spaces: int) -> list[RequirementOption]:
    canal = _canalization_spaces(parking_spaces) if parking_spaces > 10 else 0
    if 11 <= parking_spaces <= 20:
        return [RequirementOption("Configurazione minima", min_a=1, canalization_required=True, canalization_spaces=canal)]
    if 21 <= parking_spaces <= 100:
        return [RequirementOption("Configurazione minima", min_a=floor(parking_spaces / 20), canalization_required=True, canalization_spaces=canal)]
    if 101 <= parking_spaces <= 250:
        return [RequirementOption("Configurazione minima", min_a=floor(parking_spaces / 50), canalization_required=True, canalization_spaces=canal)]
    if 251 <= parking_spaces <= 500:
        return [RequirementOption("Configurazione minima", min_b=1, canalization_required=True, canalization_spaces=canal)]
    if 501 <= parking_spaces <= 1000:
        return [RequirementOption("Configurazione minima", min_b=2, canalization_required=True, canalization_spaces=canal)]
    if parking_spaces > 1000:
        return [RequirementOption("Configurazione minima", min_b=3, canalization_required=True, canalization_spaces=canal)]
    return []


def _public_existing(parking_spaces: int) -> list[RequirementOption]:
    if 21 <= parking_spaces <= 100:
        return [RequirementOption("Configurazione minima", min_a=2 * floor(parking_spaces / 20))]
    if 101 <= parking_spaces <= 250:
        return [
            RequirementOption("Opzione A", min_a=2 * floor(parking_spaces / 50)),
            RequirementOption("Opzione B", min_b=1),
        ]
    if 251 <= parking_spaces <= 500:
        return [RequirementOption("Configurazione minima", min_b=2)]
    if 501 <= parking_spaces <= 1000:
        return [RequirementOption("Configurazione minima", min_b=3)]
    if parking_spaces > 1000:
        return [RequirementOption("Configurazione minima", min_b=4)]
    return []


RULE_MAP = {
    ("private", "new"): _private_new,
    ("private", "major_renovation"): _private_major,
    ("private", "existing"): _private_existing,
    ("public", "new"): _public_new,
    ("public", "major_renovation"): _public_major,
    ("public", "existing"): _public_existing,
}


def _lookup_options(access_type: str, intervention_type: str, parking_spaces: int) -> list[RequirementOption]:
    fn = RULE_MAP[(access_type, intervention_type)]
    return fn(parking_spaces)


def _half_floor_options(options: list[RequirementOption]) -> list[RequirementOption]:
    return [
        RequirementOption(
            label=option.label,
            min_a=floor(option.min_a / 2),
            min_b=floor(option.min_b / 2),
            canalization_required=False,
            canalization_spaces=0,
        )
        for option in options
    ]


def summarize_equivalences(options: list[RequirementOption], access_type: str) -> list[str]:
    lines: list[str] = []
    for option in options:
        if option.min_a > 0:
            lines.append(f"{option.label}: {option.min_a} punti A possono essere sostituiti da {option.min_a / 10:.1f} sistemi B equivalenti teorici.")
        if option.min_b > 0:
            lines.append(f"{option.label}: {option.min_b} sistemi B equivalgono teoricamente a {option.min_b * 10} punti A.")
    lines.append("2 sistemi B possono essere sostituiti da 1 sistema ultraveloce >= 150 kW.")
    lines.append("4 sistemi B possono essere sostituiti da 1 sistema ultraveloce >= 350 kW.")
    if access_type == "private":
        lines.append("Per accesso privato, l'equivalenza B -> A e particolarmente utile per studiare configurazioni miste.")
    return lines


def evaluate_charging_requirements(
    building_type: str,
    access_type: str,
    intervention_type: str,
    parking_spaces: int,
    renovation_scope_hits_parking_or_electric: bool,
    excluded_case: bool,
) -> ChargingAssessment:
    assumptions: list[str] = []

    if building_type != "non_residential":
        return ChargingAssessment(
            applicable=False,
            status="Fuori ambito del modulo azienda",
            note="Il modulo incluso nel progetto e pensato per edifici aziendali non residenziali.",
            access_type=access_type,
            intervention_type=intervention_type,
            parking_spaces=parking_spaces,
            target_now=[],
            target_2030=[],
            assumptions=assumptions,
        )

    if excluded_case:
        return ChargingAssessment(
            applicable=False,
            status="Esclusione dichiarata",
            note="L'utente ha indicato un caso escluso ex art. 4, comma 1-bis, lett. f), d.lgs. 192/2005.",
            access_type=access_type,
            intervention_type=intervention_type,
            parking_spaces=parking_spaces,
            target_now=[],
            target_2030=[],
            assumptions=assumptions,
        )

    if parking_spaces <= 0:
        return ChargingAssessment(
            applicable=False,
            status="Dati insufficienti",
            note="Inserire un numero di posti auto maggiore di zero.",
            access_type=access_type,
            intervention_type=intervention_type,
            parking_spaces=parking_spaces,
            target_now=[],
            target_2030=[],
            assumptions=assumptions,
        )

    if intervention_type == "major_renovation" and not renovation_scope_hits_parking_or_electric:
        return ChargingAssessment(
            applicable=False,
            status="Trigger non attivato",
            note="Per la ristrutturazione importante, il modulo considera applicabile l'obbligo solo se i lavori riguardano parcheggio o infrastrutture elettriche.",
            access_type=access_type,
            intervention_type=intervention_type,
            parking_spaces=parking_spaces,
            target_now=[],
            target_2030=[],
            assumptions=assumptions,
        )

    full_options = _lookup_options(access_type, intervention_type if intervention_type != "existing" else "existing", parking_spaces)
    if not full_options:
        return ChargingAssessment(
            applicable=False,
            status="Nessun obbligo tabellare",
            note="Con il numero di posti auto indicato non emerge un obbligo minimo tabellare nel modulo implementato.",
            access_type=access_type,
            intervention_type=intervention_type,
            parking_spaces=parking_spaces,
            target_now=[],
            target_2030=[],
            assumptions=assumptions,
        )

    target_now: list[RequirementOption] = []
    target_2030: list[RequirementOption] = []

    if intervention_type == "existing":
        target_2030 = full_options
        target_now = _half_floor_options(full_options)
        assumptions.append("Per gli edifici esistenti il modulo mostra la soglia maturata al 01/01/2025 e il target pieno al 01/01/2030.")
        assumptions.append("Nel target 2025 gli arrotondamenti sono mostrati per difetto; alcune opzioni alternative possono quindi ridursi a zero.")
    else:
        target_now = full_options

    assumptions.append("Le opzioni A/B mostrate rappresentano configurazioni alternative quando compare la dicitura 'Opzione A' oppure 'Opzione B'.")
    if any(option.canalization_required for option in target_now):
        assumptions.append("Quando prevista, la canalizzazione minima e espressa come numero di posti auto da predisporre.")

    return ChargingAssessment(
        applicable=True,
        status="Applicabile",
        note="Pre-check positivo: il modulo ha individuato uno o piu set minimi di obblighi da verificare in progetto.",
        access_type=access_type,
        intervention_type=intervention_type,
        parking_spaces=parking_spaces,
        target_now=target_now,
        target_2030=target_2030,
        assumptions=assumptions,
    )
