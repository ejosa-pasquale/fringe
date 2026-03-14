# Fleet & Charging Suite

App Streamlit multipagina per due casi d'uso aziendali:

1. **calcolo e confronto del fringe benefit auto** per dipendenti
2. **pre-check degli obblighi minimi sulle infrastrutture di ricarica** nei parcheggi aziendali

## Novita della versione aggiornata

- interfaccia auto piu chiara con ranking automatico
- export risultati in CSV e XLSX
- alert per righe incomplete o casi in manual review
- modulo colonnine corretto per gestire le formule scalari e le opzioni alternative A/B
- evidenza del numero minimo di posti da predisporre per la canalizzazione quando prevista

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

- se immatricolazione, contratto e consegna sono tutte dal 01/01/2025 in poi, il modulo applica automaticamente la nuova disciplina
- categorie gestite:
  - `electric` -> elettrica pura
  - `plug_in` -> ibrida plug-in
  - tutte le altre -> altri veicoli
- se il caso non rientra automaticamente nella nuova disciplina, il modulo segnala `manual review`
- il campo `manual_percentage` consente di inserire un'aliquota manuale solo per simulazioni interne

## Logica del modulo colonnine

Il modulo e pensato per **aziende / edifici non residenziali**.
Output:

- stato di applicabilita del pre-check
- target minimo immediato
- target pieno al 2030 per gli edifici esistenti
- opzioni alternative A/B quando rilevanti
- evidenza della canalizzazione minima quando prevista

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
