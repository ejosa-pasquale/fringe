from __future__ import annotations

import pandas as pd
import streamlit as st

from .charging_logic import ChargingAssessment, RequirementOption, evaluate_charging_requirements, summarize_equivalences


def _options_to_rows(options: list[RequirementOption]) -> pd.DataFrame:
    rows = []
    for option in options:
        rows.append(
            {
                "Opzione": option.label,
                "Minimo Tipologia A": option.min_a,
                "Minimo Tipologia B": option.min_b,
                "Canalizzazione": "Si" if option.canalization_required else "No",
                "Posti da predisporre": option.canalization_spaces if option.canalization_required else 0,
            }
        )
    return pd.DataFrame(rows)


def _render_target(title: str, options: list[RequirementOption]) -> None:
    st.markdown(f"#### {title}")
    st.dataframe(_options_to_rows(options), use_container_width=True, hide_index=True)


def render_charging_page() -> None:
    st.title("Pre-check colonnine per aziende")
    st.caption("Modulo dedicato ai parcheggi aziendali con risultato minimo, opzioni alternative ed evidenza della canalizzazione")

    left, right = st.columns(2)
    with left:
        building_type = st.selectbox(
            "Tipologia edificio",
            options=["non_residential", "residential"],
            format_func=lambda x: "Non residenziale" if x == "non_residential" else "Residenziale",
        )
        access_type = st.selectbox(
            "Accesso al parcheggio",
            options=["private", "public"],
            format_func=lambda x: "Privato" if x == "private" else "Pubblico",
        )
        intervention_type = st.selectbox(
            "Tipo intervento",
            options=["new", "major_renovation", "existing"],
            format_func=lambda x: {
                "new": "Nuova costruzione",
                "major_renovation": "Ristrutturazione importante",
                "existing": "Edificio esistente",
            }[x],
        )
    with right:
        parking_spaces = st.number_input("Numero posti auto", min_value=0, value=30, step=1)
        renovation_scope_hits = st.checkbox(
            "Nel caso di ristrutturazione, i lavori riguardano anche parcheggio o infrastrutture elettriche",
            value=False,
        )
        excluded_case = st.checkbox(
            "Caso escluso ex art. 4, comma 1-bis, lett. f), d.lgs. 192/2005",
            value=False,
        )

    assessment = evaluate_charging_requirements(
        building_type=building_type,
        access_type=access_type,
        intervention_type=intervention_type,
        parking_spaces=int(parking_spaces),
        renovation_scope_hits_parking_or_electric=renovation_scope_hits,
        excluded_case=excluded_case,
    )

    status_col, note_col = st.columns([1, 3])
    status_col.metric("Esito", assessment.status)
    note_col.info(assessment.note)

    if not assessment.applicable:
        st.warning("Usa questo modulo solo come filtro preliminare interno. I casi fuori ambito o dubbi vanno rimandati al tecnico.")
        return

    summary_cols = st.columns(3)
    summary_cols[0].metric("Posti auto analizzati", assessment.parking_spaces)
    summary_cols[1].metric("Opzioni target immediate", len(assessment.target_now))
    summary_cols[2].metric("Opzioni target 2030", len(assessment.target_2030) if assessment.target_2030 else 0)

    if assessment.target_now:
        _render_target("Target minimo da verificare ora", assessment.target_now)

    if assessment.target_2030:
        _render_target("Target pieno al 01/01/2030", assessment.target_2030)

    st.markdown("### Equivalenze e configurazioni alternative")
    for line in summarize_equivalences(assessment.target_2030 or assessment.target_now, assessment.access_type):
        st.write(f"- {line}")

    st.markdown("### Assunzioni mostrate dal modulo")
    for item in assessment.assumptions:
        st.write(f"- {item}")

    st.warning(
        "Usa questo risultato come pre-check interno. Verifica finale con progettista impianti, antincendio e consulente legale/tecnico."
    )
