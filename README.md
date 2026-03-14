# Fleet & Charging Suite

App Streamlit multipagina per due casi d'uso aziendali:

1. **calcolo e confronto del fringe benefit auto** per dipendenti
2. **pre-check degli obblighi minimi sulle infrastrutture di ricarica** nei parcheggi aziendali

## Novita della versione aggiornata

- spiegazione piu chiara del processo di calcolo del fringe benefit
- nota esplicita sulla soglia fringe generale da **1.000 / 2.000 euro**
- dati demo ampliati con esempi **elettrica**, **plug-in**, **benzina** e **diesel**
- export risultati in CSV e XLSX
- modulo colonnine con distinzione diretta tra AC, DC e predisposizioni
- selezione guidata delle fasce posti auto richiamate dal decreto

## Cosa include

- `app.py`: entrypoint Streamlit
- `src/ui_home.py`: home con guida rapida
- `src/ui_car.py`: simulatore fringe benefit
- `src/ui_charging.py`: modulo colonnine azienda
- `src/car_logic.py`: regole di calcolo auto
- `src/charging_logic.py`: regole per il pre-check ricarica
- `src/constants.py`: costanti condivise
- `src/sample_data.py`: template, export e dati demo
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

## Logica del modulo auto

- se immatricolazione, contratto e consegna sono tutte dal 01/01/2025 in poi, il modulo applica automaticamente la nuova disciplina
- categorie gestite:
  - `electric` -> elettrica pura
  - `plug_in` -> ibrida plug-in
  - `benzina`, `diesel`, `full_hybrid`, `mild_hybrid`, `other` -> altri veicoli
- la soglia da **1.000 / 2.000 euro** e solo una soglia generale di esenzione dei fringe benefit, non il massimo del fringe auto
- se il caso non rientra automaticamente nella nuova disciplina, il modulo segnala `manual review`
- il campo `manual_percentage` consente di inserire un'aliquota manuale solo per simulazioni interne

## Logica del modulo colonnine

Il modulo e pensato per **aziende / edifici non residenziali**.
Output:

- stato di applicabilita del pre-check
- target minimo immediato
- target pieno al 2030 per gli edifici esistenti
- distinzione chiara tra **colonnine AC**, **colonnine DC** e **predisposizioni**
- opzioni alternative A/B quando rilevanti

## Limiti voluti del progetto

- non sostituisce una verifica fiscale o tecnico-legale
- non scarica automaticamente le tabelle ACI
- non sostituisce il progetto impiantistico e la verifica antincendio
- non gestisce workflow autorizzativi o integrazioni con fleet provider
