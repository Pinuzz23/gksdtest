import streamlit as st
 
st.title("Ciao, sono Luca, e sto programmando per GKSD")
st.subheader("Questo è un test per creare un'app per la manipolazione dei dati")
st.text("il mio scopo è quello di creare una piattaforma che sia in grado di ricevere in ingestion file excel e eseguire analisi forecast"
        )

import streamlit as st
import pandas as pd
from openpyxl import load_workbook

# Percorso al file Excel
file_path = "anagrafica_fornitori.xlsx"

# Funzione per caricare il file Excel
def load_data():
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        # Se il file non esiste, creiamo una base vuota
        df = pd.DataFrame(columns=[
            "Codice Fornitore", "Ragione Sociale", "Partita IVA", "Indirizzo",
            "Città", "Telefono", "Email", "Persona di Contatto"
        ])
        df.to_excel(file_path, index=False)
    return df

# Funzione per aggiungere una riga al file Excel
def save_data(data):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_excel(file_path, index=False)
    st.success("Dati salvati correttamente!")

# Layout Streamlit
st.title("Anagrafica Fornitori")

# Creazione del form
with st.form(key='fornitori_form'):
    codice_fornitore = st.text_input("Codice Fornitore")
    ragione_sociale = st.text_input("Ragione Sociale")
    partita_iva = st.text_input("Partita IVA")
    indirizzo = st.text_input("Indirizzo")
    citta = st.text_input("Città")
    telefono = st.text_input("Telefono")
    email = st.text_input("Email")
    persona_contatto = st.text_input("Persona di Contatto")

    # Pulsante di salvataggio
    submit_button = st.form_submit_button(label="Salva Dati")

if submit_button:
    # Validazione dati
    if not codice_fornitore or not ragione_sociale:
        st.error("I campi Codice Fornitore e Ragione Sociale sono obbligatori.")
    else:
        nuovo_fornitore = {
            "Codice Fornitore": codice_fornitore,
            "Ragione Sociale": ragione_sociale,
            "Partita IVA": partita_iva,
            "Indirizzo": indirizzo,
            "Città": citta,
            "Telefono": telefono,
            "Email": email,
            "Persona di Contatto": persona_contatto
        }
        save_data(nuovo_fornitore)

# Mostra i dati aggiornati
st.header("Anagrafica Attuale")
st.dataframe(load_data())
