from __future__ import annotations

import pandas as pd
import streamlit as st

from .car_logic import compute_car_dataframe
from .sample_data import COLUMNS, csv_bytes_from_df, demo_catalog_df, empty_template_df, xlsx_bytes_from_df


DISPLAY_COLUMNS = {
    "vehicle_label": "Veicolo",
    "fuel_label": "Alimentazione",
    "regime": "Regime",
    "regime_note": "Nota regime",
    "fiscal_category": "Categoria fiscale",
    "percentage": "% applicata",
    "annual_gross_full_year": "Fringe annuo teorico",
    "gross_for_assignment_period": "Fringe per periodo di assegnazione",
    "employee_contribution_annual": "Contributo dipendente annuo",
    "annual_net_of_contribution": "Imponibile annuo netto contributo",
    "monthly_net_of_contribution": "Imponibile mensile",
    "months_of_use": "Mesi utilizzo",
    "combined_benefits": "Fringe complessivi",
    "threshold_headroom_after_car": "Residuo soglia",
    "threshold_excess_after_car": "Eccedenza soglia",
    "yearly_tax_estimate": "Stima costo fiscale annuo",
    "monthly_tax_estimate": "Stima costo fiscale mensile",
    "warning": "Alert",
}

DATE_COLUMNS = ["registration_date", "contract_date", "delivery_date"]
NUMERIC_COLUMNS = [
    "aci_cost_per_km",
    "employee_contribution_annual",
    "months_of_use",
    "irpef_marginal_rate",
    "manual_percentage",
]
TEXT_COLUMNS = ["brand", "model", "version", "fuel_type"]
FUEL_OPTIONS = ["electric", "plug_in", "full_hybrid", "mild_hybrid", "benzina", "diesel", "other"]
FUEL_CAPTIONS = {
    "electric": "elettrica pura",
    "plug_in": "ibrida plug-in",
    "full_hybrid": "full hybrid",
    "mild_hybrid": "mild hybrid",
    "benzina": "benzina",
    "diesel": "diesel",
    "other": "altro",
}


def _typed_empty_catalog_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "brand": pd.Series(dtype="string"),
            "model": pd.Series(dtype="string"),
            "version": pd.Series(dtype="string"),
            "fuel_type": pd.Series(dtype="string"),
            "aci_cost_per_km": pd.Series(dtype="float64"),
            "registration_date": pd.Series(dtype="datetime64[ns]"),
            "contract_date": pd.Series(dtype="datetime64[ns]"),
            "delivery_date": pd.Series(dtype="datetime64[ns]"),
            "employee_contribution_annual": pd.Series(dtype="float64"),
            "months_of_use": pd.Series(dtype="float64"),
            "irpef_marginal_rate": pd.Series(dtype="float64"),
            "manual_percentage": pd.Series(dtype="float64"),
        }
    )[COLUMNS]


def _prepare_catalog_for_editor(raw_df: pd.DataFrame | None) -> pd.DataFrame:
    base_df = _typed_empty_catalog_df()
    if raw_df is None:
        return base_df

    df = raw_df.copy()
    for column in COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA
    df = df[COLUMNS]

    for column in TEXT_COLUMNS:
        df[column] = df[column].astype("string")
        df[column] = df[column].replace({"nan": pd.NA, "None": pd.NA, "": pd.NA})

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    for column in DATE_COLUMNS:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    if "fuel_type" in df.columns:
        normalized = df["fuel_type"].astype("string").str.strip().str.lower()
        df["fuel_type"] = normalized.where(normalized.isin(FUEL_OPTIONS), other="other")
        df.loc[normalized.isna(), "fuel_type"] = pd.NA

    return df


def _load_catalog() -> pd.DataFrame:
    if "catalog_df" not in st.session_state:
        st.session_state.catalog_df = _prepare_catalog_for_editor(demo_catalog_df())
    return _prepare_catalog_for_editor(st.session_state.catalog_df)


def _format_results_for_display(df: pd.DataFrame) -> pd.DataFrame:
    view_df = df.copy()
    currency_cols = [
        "annual_gross_full_year",
        "gross_for_assignment_period",
        "employee_contribution_annual",
        "annual_net_of_contribution",
        "monthly_net_of_contribution",
        "combined_benefits",
        "threshold_headroom_after_car",
        "threshold_excess_after_car",
        "yearly_tax_estimate",
        "monthly_tax_estimate",
    ]
    for col in currency_cols:
        if col in view_df.columns:
            view_df[col] = view_df[col].map(lambda x: None if pd.isna(x) else round(float(x), 2))
    if "percentage" in view_df.columns:
        view_df["percentage"] = view_df["percentage"].map(lambda x: None if pd.isna(x) else round(float(x) * 100, 2))
    if "regime" in view_df.columns:
        view_df["regime"] = view_df["regime"].replace({"new_2025": "Nuova disciplina 2025+", "manual_review": "Manual review"})
    return view_df.rename(columns=DISPLAY_COLUMNS)


def render_car_page() -> None:
    st.title("Calcolo fringe benefit auto")
    st.caption("Confronto veicoli per il dipendente con catalogo caricabile, ranking automatico ed export risultati")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Carica dati demo", use_container_width=True):
            st.session_state.catalog_df = _prepare_catalog_for_editor(demo_catalog_df())
    with col2:
        if st.button("Azzera catalogo", use_container_width=True):
            st.session_state.catalog_df = _typed_empty_catalog_df()
    with col3:
        st.download_button(
            "Scarica template CSV",
            data=csv_bytes_from_df(empty_template_df()),
            file_name="car_catalog_template.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col4:
        st.download_button(
            "Scarica template XLSX",
            data=xlsx_bytes_from_df(empty_template_df()),
            file_name="car_catalog_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    uploaded = st.file_uploader("Carica il tuo catalogo CSV", type=["csv"])
    if uploaded is not None:
        st.session_state.catalog_df = _prepare_catalog_for_editor(pd.read_csv(uploaded))

    with st.expander("Come funziona il calcolo del fringe benefit", expanded=True):
        st.markdown(
            """
            1. **Verifica regime**: il tool controlla se immatricolazione, contratto e consegna sono tutte dal 01/01/2025.
            2. **Individua la percentuale fiscale**:
               - 10% elettrica pura
               - 20% ibrida plug-in
               - 50% benzina, diesel, mild hybrid, full hybrid e altri veicoli
            3. **Calcola la base annua teorica**: costo ACI x 15.000 km x percentuale.
            4. **Riproporziona il periodo**: se l'auto e assegnata per meno di 12 mesi, il valore viene ridotto pro-quota.
            5. **Sottrae il contributo del dipendente**: ottieni l'imponibile annuo netto.
            6. **Stima il costo fiscale**: solo se inserisci l'aliquota IRPEF marginale.
            7. **Confronta la soglia fringe generale**: il tool verifica se, sommando l'auto agli altri fringe benefit, resti entro la soglia annua configurata.
            """
        )
        st.info(
            "Nota soglia fringe benefit 2025-2027: 1.000 euro per la generalita dei dipendenti, 2.000 euro per dipendenti con figli fiscalmente a carico. Questa soglia non e il massimo del fringe benefit auto: serve solo per capire se il totale annuo dei fringe benefit resta entro il limite di non imponibilita."
        )

    st.markdown("### Parametri generali")
    p0, p1, p2, p3 = st.columns([1.2, 1, 1, 1])
    with p0:
        threshold_preset = st.selectbox(
            "Soglia annua di esenzione fringe",
            options=[1000.0, 2000.0, -1.0],
            format_func=lambda x: "1.000 euro - standard" if x == 1000.0 else ("2.000 euro - figli a carico" if x == 2000.0 else "Altro valore manuale"),
        )
    with p1:
        threshold_amount = st.number_input(
            "Valore soglia usato nel confronto",
            min_value=0.0,
            value=1000.0 if threshold_preset == -1.0 else float(threshold_preset),
            step=100.0,
            disabled=threshold_preset != -1.0,
            help="Usa 1.000 euro come valore standard e 2.000 euro solo per dipendenti con figli fiscalmente a carico.",
        )
    with p2:
        other_benefits_amount = st.number_input(
            "Altri fringe benefit gia assegnati al dipendente",
            min_value=0.0,
            value=0.0,
            step=100.0,
        )
    with p3:
        show_only_complete = st.checkbox("Mostra solo righe complete nei risultati", value=False)

    st.caption("Nel catalogo puoi confrontare anche benzina e diesel: se le date rientrano nella nuova disciplina 2025+, il tool le tratta nella categoria 'altri veicoli' con percentuale 50%.")

    st.markdown("### Catalogo veicoli")
    catalog_df = _load_catalog()

    edited = st.data_editor(
        catalog_df,
        num_rows="dynamic",
        use_container_width=True,
        key="catalog_editor",
        column_config={
            "brand": st.column_config.TextColumn("Marca"),
            "model": st.column_config.TextColumn("Modello"),
            "version": st.column_config.TextColumn("Versione"),
            "fuel_type": st.column_config.SelectboxColumn(
                "Alimentazione",
                options=FUEL_OPTIONS,
                required=False,
                help="Valori gestiti: elettrica pura, ibrida plug-in, full hybrid, mild hybrid, benzina, diesel, altro.",
            ),
            "aci_cost_per_km": st.column_config.NumberColumn("Costo ACI per km", format="%.4f"),
            "registration_date": st.column_config.DateColumn("Data immatricolazione", format="YYYY-MM-DD"),
            "contract_date": st.column_config.DateColumn("Data contratto", format="YYYY-MM-DD"),
            "delivery_date": st.column_config.DateColumn("Data consegna", format="YYYY-MM-DD"),
            "employee_contribution_annual": st.column_config.NumberColumn("Contributo dipendente annuo", format="%.2f"),
            "months_of_use": st.column_config.NumberColumn("Mesi utilizzo", min_value=1, max_value=12, format="%.0f"),
            "irpef_marginal_rate": st.column_config.NumberColumn("Aliquota marginale IRPEF", min_value=0.0, max_value=1.0, format="%.2f"),
            "manual_percentage": st.column_config.NumberColumn(
                "Percentuale manuale",
                min_value=0.0,
                max_value=1.0,
                format="%.2f",
                help="Usa questo campo solo se il caso non rientra automaticamente nella nuova disciplina 2025+.",
            ),
        },
    )
    st.session_state.catalog_df = _prepare_catalog_for_editor(edited)

    if edited.empty:
        st.warning("Il catalogo e vuoto. Inserisci almeno un veicolo per eseguire il confronto.")
        return

    comparison_df = compute_car_dataframe(st.session_state.catalog_df, threshold_amount, other_benefits_amount)
    if show_only_complete:
        comparison_df = comparison_df[comparison_df["annual_net_of_contribution"].notna()].copy()

    if comparison_df.empty:
        st.warning("Non ci sono righe complete da mostrare con il filtro attuale.")
        return

    valid_rank = comparison_df.dropna(subset=["annual_net_of_contribution"]).sort_values("annual_net_of_contribution")
    invalid_rows = comparison_df[comparison_df["annual_net_of_contribution"].isna()]

    st.markdown("### Sintesi decisionale")
    m1, m2, m3 = st.columns(3)
    if not valid_rank.empty:
        best = valid_rank.iloc[0]
        m1.metric("Opzione migliore", best["vehicle_label"])
        m2.metric("Imponibile annuo migliore", f"EUR {best['annual_net_of_contribution']:.2f}")
        if len(valid_rank) > 1:
            second = valid_rank.iloc[1]
            delta = second["annual_net_of_contribution"] - best["annual_net_of_contribution"]
            m3.metric("Vantaggio vs seconda opzione", f"EUR {delta:.2f}")
        else:
            m3.metric("Vantaggio vs seconda opzione", "n.d.")

        st.success(
            f"Tra le opzioni complete, il veicolo fiscalmente piu conveniente e {best['vehicle_label']} con imponibile annuo netto contributo di EUR {best['annual_net_of_contribution']:.2f}."
        )

    if not invalid_rows.empty:
        st.warning(f"Ci sono {len(invalid_rows)} righe incomplete o in manual review senza percentuale manuale.")

    st.markdown("### Risultati confronto")
    display_df = _format_results_for_display(comparison_df)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            "Esporta risultati CSV",
            data=display_df.to_csv(index=False).encode("utf-8"),
            file_name="fringe_benefit_results.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with d2:
        st.download_button(
            "Esporta risultati XLSX",
            data=xlsx_bytes_from_df(display_df),
            file_name="fringe_benefit_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
