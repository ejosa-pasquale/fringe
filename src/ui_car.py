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


def _load_catalog() -> pd.DataFrame:
    if "catalog_df" not in st.session_state:
        st.session_state.catalog_df = demo_catalog_df()
    return st.session_state.catalog_df.copy()


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
            st.session_state.catalog_df = demo_catalog_df()
    with col2:
        if st.button("Azzera catalogo", use_container_width=True):
            st.session_state.catalog_df = empty_template_df()
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
        st.session_state.catalog_df = pd.read_csv(uploaded)

    st.markdown("### Parametri generali")
    p1, p2, p3 = st.columns(3)
    with p1:
        threshold_amount = st.number_input(
            "Soglia fringe benefit da usare nel confronto",
            min_value=0.0,
            value=1000.0,
            step=100.0,
            help="Campo configurabile: non e preimpostato a una soglia normativa fissa.",
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

    st.markdown("### Catalogo veicoli")
    catalog_df = _load_catalog()
    for column in COLUMNS:
        if column not in catalog_df.columns:
            catalog_df[column] = None
    catalog_df = catalog_df[COLUMNS]

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
                options=["electric", "plug_in", "full_hybrid", "mild_hybrid", "benzina", "diesel", "other"],
            ),
            "aci_cost_per_km": st.column_config.NumberColumn("Costo ACI per km", format="%.4f"),
            "registration_date": st.column_config.DateColumn("Data immatricolazione", format="YYYY-MM-DD"),
            "contract_date": st.column_config.DateColumn("Data contratto", format="YYYY-MM-DD"),
            "delivery_date": st.column_config.DateColumn("Data consegna", format="YYYY-MM-DD"),
            "employee_contribution_annual": st.column_config.NumberColumn("Contributo dipendente annuo", format="%.2f"),
            "months_of_use": st.column_config.NumberColumn("Mesi utilizzo", min_value=1, max_value=12),
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
    st.session_state.catalog_df = edited.copy()

    if edited.empty:
        st.warning("Il catalogo e vuoto. Inserisci almeno un veicolo per eseguire il confronto.")
        return

    comparison_df = compute_car_dataframe(edited, threshold_amount, other_benefits_amount)
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
        st.warning(f"Ci sono {len(invalid_rows)} righe incomplete o in manual review senza percentuale manuale: controlla la colonna Alert.")

    st.markdown("### Risultati")
    display_df = _format_results_for_display(comparison_df)
    st.dataframe(display_df, use_container_width=True)

    export_csv = display_df.to_csv(index=False).encode("utf-8")
    export_xlsx = xlsx_bytes_from_df(display_df)
    e1, e2 = st.columns(2)
    e1.download_button("Scarica risultati CSV", data=export_csv, file_name="fringe_results.csv", mime="text/csv", use_container_width=True)
    e2.download_button(
        "Scarica risultati XLSX",
        data=export_xlsx,
        file_name="fringe_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    if not valid_rank.empty:
        chart_df = valid_rank[["vehicle_label", "annual_net_of_contribution"]].set_index("vehicle_label")
        st.markdown("### Confronto rapido")
        st.bar_chart(chart_df)

    st.info(
        "La soglia fringe e mostrata come supporto decisionale. Valutazione fiscale definitiva e gestione busta paga restano in capo a HR/payroll."
    )
