# Fleet & Charging Suite

App Streamlit multipagina per due casi d'uso aziendali:

1. **calcolo e confronto del fringe benefit auto** per dipendenti
2. **pre-check degli obblighi minimi sulle infrastrutture di ricarica** nei parcheggi aziendali

## Novita della versione aggiornata

- spiegazione passo-passo del processo di calcolo del fringe benefit direttamente nell'app
- colonne risultato piu leggibili: base ACI 15.000 km, quota periodo, fringe teorico, fringe per periodo e imponibile netto
- export risultati in CSV e XLSX
- alert per righe incomplete o casi in manual review
- modulo colonnine piu chiaro con distinzione netta tra:
  - **colonnine AC**
  - **colonnine DC**
  - **predisposizioni**
- selezione della **fascia posti auto** richiamata dal decreto, con numero effettivo di posti all'interno della fascia per mantenere il calcolo puntuale
- evidenza delle configurazioni alternative A/B quando ammesse

## Cosa include

- `app.py`: entrypoint Streamlit
- `src/ui_home.py`: home con guida rapida
- `src/ui_car.py`: simulatore fringe benefit
- `src/ui_charging.py`: modulo colonnine azienda
- `src/car_logic.py`: regole di calcolo auto
- `src/charging_logic.py`: regole per il pre-check ricarica
- `data/car_catalog_template.csv`: template per il catalogo auto
- `.streamlit/config.toml`: tema e config base
- `requirements.txt`: dipendenze

## Come avviare il progetto in locale

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Come pubblicarlo su GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <TUO_REPO_GITHUB>
git push -u origin main
```

## Come pubblicarlo su Streamlit Community Cloud

1. carica il repository su GitHub
2. crea una nuova app da Streamlit Community Cloud
3. seleziona il repository e come file principale `app.py`
4. verifica che `requirements.txt` sia nella root del repository

## Dati auto da sostituire prima dell'uso operativo

I dati inclusi nel progetto sono **demo** e servono solo per mostrare il funzionamento dell'app.
Prima dell'uso reale sostituisci sempre:

- costo ACI per km
- date di immatricolazione / contratto / consegna
- eventuale contributo dipendente
- eventuale aliquota IRPEF marginale usata per simulazione

## Logica del modulo auto

Il simulatore mostra direttamente il processo di calcolo:

1. verifica del regime applicabile
2. scelta della percentuale fiscale
3. calcolo della base ACI convenzionale su **15.000 km**
4. calcolo del fringe annuo teorico
5. riproporzionamento per i mesi di utilizzo
6. sottrazione dell'eventuale contributo del dipendente
7. confronto con la soglia fringe impostata nel simulatore

Se il caso non rientra automaticamente nella nuova disciplina, il modulo segnala `manual review`.
Il campo `manual_percentage` consente di inserire un'aliquota manuale solo per simulazioni interne.

## Logica del modulo colonnine

Il modulo e pensato per **aziende / edifici non residenziali**.
Output:

- stato di applicabilita del pre-check
- obbligo minimo immediato espresso in:
  - numero minimo di **colonnine AC**
  - numero minimo di **colonnine DC**
  - numero minimo di **predisposizioni**
- target pieno al 2030 per gli edifici esistenti
- opzioni alternative A/B quando rilevanti
- selezione guidata della fascia posti auto prevista dal decreto

## Limiti voluti del progetto

- non sostituisce una verifica fiscale o tecnico-legale
- non scarica automaticamente le tabelle ACI
- non sostituisce il progetto impiantistico e la verifica antincendio
- non gestisce workflow autorizzativi o integrazioni con fleet provider

## Template catalogo CSV

Colonne attese:

- `brand`
- `model`
- `version`
- `fuel_type`
- `aci_cost_per_km`
- `registration_date`
- `contract_date`
- `delivery_date`
- `employee_contribution_annual`
- `months_of_use`
- `irpef_marginal_rate`
- `manual_percentage`
