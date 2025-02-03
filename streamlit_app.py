import streamlit as st
 
st.title("Ciao, sono Luca, e sto programmando per GKSD")
st.subheader("Questo è un test per creare un'app per la manipolazione dei dati")
st.text("il mio scopo è quello di creare una piattaforma che sia in grado di ricevere in ingestion file excel e eseguire analisi forecast"
        )

import streamlit as st
import pandas as pd
from prophet import Prophet

# Carica il file Excel
uploaded_file = st.file_uploader("Carica un file Excel", type=["xlsx"])

if uploaded_file:
    # Leggi il foglio Excel
    xls = pd.ExcelFile(uploaded_file)
    
    # Seleziona un foglio
    sheet_name = st.selectbox("Seleziona un foglio", xls.sheet_names)
    
    # Carica il foglio selezionato senza intestazioni per ispezionare la struttura
    df_preview = pd.read_excel(uploaded_file, sheet_name=sheet_name, header=None)
    
    # Mostra la preview grezza del foglio
    st.write("Anteprima grezza del foglio:")
    st.write(df_preview.head())
    
    # Permetti all'utente di selezionare la riga che rappresenta le intestazioni
    header_row = st.number_input("Seleziona la riga con le intestazioni (inizia da 0)", min_value=0, max_value=len(df_preview)-1, value=0)
    
    # Ricarica il DataFrame con le intestazioni corrette
    df = pd.read_excel(uploaded_file, sheet_name=sheet_name, header=header_row)
    
    # Mostra la tabella con intestazioni corrette
    st.write("Tabella rilevata con intestazioni:")
    st.write(df.head())
    
    # Selezione degli assi X e Y
    col_x = st.selectbox("Seleziona l'asse X", df.columns)
    col_y = st.selectbox("Seleziona l'asse Y", df.columns)
    
    # Visualizzazione grafica dei dati selezionati
    if col_x and col_y:
        st.write(f"Grafico dei dati: {col_x} vs {col_y}")
        st.line_chart(df[[col_x, col_y]].set_index(col_x))

    # Previsione con Prophet se selezionati assi compatibili
    if st.button("Esegui analisi forecast"):
        if pd.api.types.is_datetime64_any_dtype(df[col_x]):
            st.write("Eseguiamo una previsione sulla colonna selezionata.")
            df_forecast = df.rename(columns={col_x: 'ds', col_y: 'y'})

            # Creare un modello Prophet
            model = Prophet()
            model.fit(df_forecast)

            # Fai una previsione per i prossimi 60 giorni
            future = model.make_future_dataframe(periods=60)
            forecast = model.predict(future)

            # Visualizza il grafico delle previsioni
            st.write("Previsioni per i prossimi 60 giorni:")
            st.line_chart(forecast[['ds', 'yhat']].set_index('ds'))
        else:
            st.error("Per eseguire il forecast, l'asse X deve essere una colonna di tipo data.")
