from __future__ import annotations

import streamlit as st


def render_home() -> None:
    st.title("Fleet & Charging Suite")
    st.caption("Simulatore Streamlit per fringe benefit auto aziendali e pre-check colonnine di ricarica")

    st.markdown(
        """
        Questa app e pensata come base pronta per GitHub e Streamlit Community Cloud.

        **Modulo 1 - Dipendente**
        - confronto tra elettrica, plug-in, benzina, diesel e altre auto
        - spiegazione diretta del processo di calcolo
        - base ACI 15.000 km, quota periodo e imponibile netto evidenziati nei risultati
        - nota chiara sulla soglia fringe generale da **1.000 / 2.000 euro**
        - ranking automatico delle opzioni e export CSV/XLSX

        **Modulo 2 - Azienda**
        - verifica preliminare degli obblighi minimi per i parcheggi aziendali
        - distinzione immediata tra **colonnine AC**, **colonnine DC** e **predisposizioni**
        - selezione guidata delle fasce posti auto richiamate dal decreto
        - differenza tra nuova costruzione, ristrutturazione importante ed edificio esistente
        - gestione di opzioni alternative A/B quando previste dal pre-check
        """
    )

    st.info(
        "Sostituisci i dati demo con il tuo catalogo aziendale e con i costi ACI ufficiali dell'anno fiscale di riferimento prima dell'uso operativo."
    )

    left, right = st.columns(2)
    with left:
        st.subheader("Come partire")
        st.markdown(
            """
            1. Carica o modifica il catalogo veicoli nel modulo auto.
            2. Inserisci il costo ACI ufficiale per ogni modello.
            3. Seleziona la soglia fringe standard da 1.000 euro oppure quella da 2.000 euro per figli a carico.
            4. Compila il modulo colonnine scegliendo la fascia posti auto del sito aziendale.
            5. Esporta i risultati per condividerli con HR, fleet o facility.
            """
        )
    with right:
        st.subheader("Attenzioni")
        st.markdown(
            """
            - I casi 2025 transitori vanno sempre validati dal payroll.
            - La soglia da 1.000 / 2.000 euro non e il massimo del fringe auto: e solo il limite generale di esenzione dei fringe benefit.
            - La sezione colonnine e un pre-check, non una verifica progettuale definitiva.
            - I dati demo inclusi non sono pronti per uso operativo.
            """
        )
