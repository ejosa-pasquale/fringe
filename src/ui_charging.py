from __future__ import annotations

import pandas as pd
import streamlit as st

from .charging_logic import RequirementOption, evaluate_charging_requirements, summarize_equivalences
from .constants import TIPOLOGY_A_DESC, TIPOLOGY_B_DESC


PRIVATE_BANDS = [
    ("0-10 posti", 0, 10),
    ("11-20 posti", 11, 20),
    ("21-100 posti", 21, 100),
    ("101-500 posti", 101, 500),
    ("501-1000 posti", 501, 1000),
    ("Oltre 1000 posti", 1001, None),
]

PUBLIC_BANDS = [
    ("0-10 posti", 0, 10),
    ("11-20 posti", 11, 20),
    ("21-100 posti", 21, 100),
    ("101-250 posti", 101, 250),
    ("251-500 posti", 251, 500),
    ("501-1000 posti", 501, 1000),
    ("Oltre 1000 posti", 1001, None),
]


def _options_to_rows(options: list[RequirementOption]) -> pd.DataFrame:
    rows = []
    for option in options:
        rows.append(
            {
                "Configurazione": option.label,
                "Colonnine AC minime": option.min_a,
                "Colonnine DC minime": option.min_b,
                "Predisposizioni minime": option.canalization_spaces if option.canalization_required else 0,
            }
        )
    return pd.DataFrame(rows)


def _band_options(access_type: str) -> list[tuple[str, int, int | None]]:
    return PRIVATE_BANDS if access_type == "private" else PUBLIC_BANDS


def _resolve_parking_spaces(access_type: str) -> tuple[str, int]:
    bands = _band_options(access_type)
    labels = [band[0] for band in bands]
    selected_label = st.selectbox("Fascia posti auto", options=labels)
    selected = next(band for band in bands if band[0] == selected_label)
    min_spaces, max_spaces = selected[1], selected[2]

    if max_spaces is None:
        exact_spaces = st.number_input("Numero posti auto effettivi nella fascia selezionata", min_value=min_spaces, value=min_spaces, step=1)
    elif min_spaces == max_spaces:
        exact_spaces = min_spaces
    else:
        default_value = min_spaces
        exact_spaces = st.slider("Numero posti auto effettivi nella fascia selezionata", min_value=min_spaces, max_value=max_spaces, value=default_value)

    return selected_label, int(exact_spaces)


def _render_quick_result(title: str, option: RequirementOption) -> None:
    st.markdown(f"#### {title} - {option.label}")
    a_col, b_col, c_col = st.columns(3)
    a_col.metric("Colonnine AC", option.min_a)
    b_col.metric("Colonnine DC", option.min_b)
    c_col.metric("Predisposizioni", option.canalization_spaces if option.canalization_required else 0)

    parts: list[str] = []
    if option.min_a > 0:
        parts.append(f"{option.min_a} colonnine AC")
    if option.min_b > 0:
        parts.append(f"{option.min_b} colonnine DC")
    if option.canalization_required:
        parts.append(f"{option.canalization_spaces} predisposizioni")
    if not parts:
        parts.append("nessun obbligo tabellare")

    st.success(" / ".join(parts))


def _render_target(title: str, options: list[RequirementOption]) -> None:
    st.markdown(f"### {title}")
    for option in options:
        _render_quick_result(title, option)
    st.dataframe(_options_to_rows(options), use_container_width=True, hide_index=True)


def render_charging_page() -> None:
    st.title("Pre-check colonnine per aziende")
    st.caption("Risposta veloce e chiara: quante colonnine AC, quante colonnine DC e quante predisposizioni minime servono")

    with st.expander("Legenda rapida", expanded=True):
        st.markdown(
            f"""
            - **Colonnine AC** = {TIPOLOGY_A_DESC}
            - **Colonnine DC** = {TIPOLOGY_B_DESC}
            - **Predisposizioni** = canalizzazioni / passaggi impiantistici minimi da predisporre nei posti auto quando richiesti
            """
        )

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
        selected_band, parking_spaces = _resolve_parking_spaces(access_type)
        renovation_scope_hits = st.checkbox(
            "Se e ristrutturazione importante, i lavori riguardano anche parcheggio o infrastrutture elettriche",
            value=False,
        )
        excluded_case = st.checkbox(
            "Caso escluso ex art. 4, comma 1-bis, lett. f), d.lgs. 192/2005",
            value=False,
        )

    st.info(f"Fascia decreto selezionata: **{selected_band}** | Posti auto usati nel calcolo: **{parking_spaces}**")

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
        st.warning("Usa questo modulo come pre-check interno. I casi fuori ambito o dubbi vanno verificati dal tecnico.")
        return

    summary_cols = st.columns(3)
    summary_cols[0].metric("Posti auto analizzati", assessment.parking_spaces)
    summary_cols[1].metric("Configurazioni immediate", len(assessment.target_now))
    summary_cols[2].metric("Configurazioni 2030", len(assessment.target_2030) if assessment.target_2030 else 0)

    if assessment.target_now:
        _render_target("Obbligo minimo da verificare adesso", assessment.target_now)

    if assessment.target_2030:
        _render_target("Target pieno al 01/01/2030", assessment.target_2030)

    with st.expander("Equivalenze e configurazioni alternative", expanded=False):
        for line in summarize_equivalences(assessment.target_2030 or assessment.target_now, assessment.access_type):
            st.write(f"- {line}")

    with st.expander("Assunzioni del modulo", expanded=False):
        for item in assessment.assumptions:
            st.write(f"- {item}")

    st.warning(
        "Il risultato distingue chiaramente colonnine AC, colonnine DC e predisposizioni minime. Resta comunque un pre-check: la verifica finale va fatta con progettista impianti, antincendio e consulente tecnico-legale."
    )
