import math
import time
import pandas as pd
import streamlit as st
from struttura.strutturaC1 import FileC1, RecordC1, FileC1Repository, ControlloFileC1
from struttura.strutturaC2 import FileC2, RecordC2, FileC2Repository, ControlloFileC2
from applicazione.config import percorsi, SessionManager, SessionKeys, Pagine
from struttura.strutturaResult import Result, display_errore
from typing import Union

session_manager = SessionManager()
session_manager.initialize_state()


key = SessionKeys()





FILE_C1 = percorsi.get_storage() + 'file_c1.txt'
FILE_C2 = percorsi.get_storage() + 'file_c2.txt'
FILE_C3 = percorsi.get_storage() + 'file_c3.txt'

# @st.cache_data
def carica_file(percorso_file):
    with open(percorso_file, 'r', encoding='utf-8') as f:
        return f.readlines()



# @st.cache_data
def control_file(file_path, _repository: Union[FileC1Repository, FileC2Repository]):

    repo = _repository

    controllo_result = repo.controlla_file(file_path)
    if controllo_result.is_failure():

        # session_manager.set(key.key_current_page(), Pagine.HOME)
        # display_errore(controllo_result)
        # st.rerun()
        return controllo_result



    oggetto_result = repo.carica_da_file(file_path)
    if oggetto_result.is_failure():

        session_manager.set(key.key_current_page(), Pagine.HOME)
        display_errore(oggetto_result)
        st.rerun()

    file: Union[FileC1, FileC2] = oggetto_result.risultato
    return Result.success(file)



def set_pagina_corrente(key_sessione_pagina, valore):
    """Callback per impostare un valore specifico nella sessione."""
    st.session_state[key_sessione_pagina] = valore

def incrementa_pagina(key_sessione_pagina):
    """Callback per il bottone 'Successivo'."""
    st.session_state[key_sessione_pagina] += 1

def decrementa_pagina(key_sessione_pagina):
    """Callback per il bottone 'Precedente'."""
    st.session_state[key_sessione_pagina] -= 1


def tab_file_c1():
    key_file_data = key.key_file_c1()
    key_pagina_corrente = "pagina_corrente_c1"

    if not session_manager.check(key_file_data):
        session_manager.set(key_pagina_corrente, 1)

        repo = FileC1Repository()
        result_file = control_file(FILE_C1, repo)

        if result_file.is_failure():
            st.error(result_file.errore)
            for errore in result_file.info:
                with st.expander(f"{errore['messaggio']}"):
                    st.warning(f"Valore ricevuto: **{errore['dettagli']}**")
        else:
            file_c1: FileC1 = result_file.risultato
            validatore = ControlloFileC1(file_c1)
            result_validatore = validatore.controllo()
            if result_validatore.is_failure():
                st.error(f"Errore durante il controllo del File C1")
                if result_validatore.info == 'LISTA_DI_ERRORI':
                    lista_errori = result_validatore.errore

                    for errore in lista_errori:
                        with st.expander(f"Errore riga: **{errore['riga']}**"):
                            st.error(errore['messaggio'])
                            st.warning(f"Valore ricevuto: *'{errore['valore']}'*")
                else:
                    with st.expander(result_validatore.errore):
                        st.warning(result_validatore.info)
            else:
                st.success('Nessun errore riscontrato durante il controllo del File C1')
                session_manager.set(key_file_data, file_c1.records)
                st.rerun()
    else:
        # mostra_file(key_file_data, key_pagina_corrente, 'FILE_C1')
        mostra_file(
            key_session_file=key_file_data,
            key_session_pagina=key_pagina_corrente,
            tipo_file="FILE_C1",
            campi_da_escludere=['uuid', 'campo_vuoto']
        )



def tab_file_c2():
    key_file_data = key.key_file_c2()
    key_pagina_corrente = "pagina_corrente_c2"

    if not session_manager.check(key_file_data):
        session_manager.set(key_pagina_corrente, 1)

        repo = FileC2Repository()
        result_file = control_file(FILE_C2, repo)

        if result_file.is_failure():
            st.error(result_file.errore)
            for errore in result_file.info:
                with st.expander(f"{errore['messaggio']}"):
                    st.warning(f"Valore ricevuto: **{errore['dettagli']}**")
        else:
            file_c2: FileC2 = result_file.risultato
            validatore = ControlloFileC2(file_c2)
            result_validatore = validatore.controllo()
            if result_validatore.is_failure():
                st.error(f"Errore durante il controllo del File C2")
                if result_validatore.info == 'LISTA_DI_ERRORI':
                    lista_errori = result_validatore.errore

                    for errore in result_validatore.errore:
                        with st.expander(f"Errore riga: **{errore['riga']}**"):
                            st.error(errore['messaggio'])
                            st.warning(f"Valore ricevuto: *'{errore['valore']}'*")
                else:
                    with st.expander(result_validatore.errore):
                        st.warning(result_validatore.info[0])
                    st.divider()
                    st.caption('Lista errori')
                    for errore in result_validatore.info[1]:
                        with st.expander(f"Errore riga: **{errore['riga']}**"):
                            st.error(errore['messaggio'])
                            st.warning(f"Valore ricevuto: *'{errore['valore']}'*")
            else:
                st.success('Nessun errore riscontrato durante il controllo del File C1')
                session_manager.set(key_file_data, file_c2.records)
                st.rerun()
    else:
        # mostra_file(key_file_data, key_pagina_corrente, 'FILE_C1')
        mostra_file(
            key_session_file=key_file_data,
            key_session_pagina=key_pagina_corrente,
            tipo_file="FILE_C2",
            campi_da_escludere=['uuid', 'campo_vuoto']
        )



def tab_file_c3():
    st.write('file c3')




def mostra_file(key_session_file, key_session_pagina, tipo_file, campi_da_escludere):
    if not session_manager.check(key_session_file):
        st.warning("Dati non trovati in sessione")
        return

    tutte_le_righe = session_manager.get(key_session_file)
    totale_righe = len(tutte_le_righe)

    col1, col2 = st.columns([1,1])
    with col1:

        righe_per_pagina = st.selectbox(
            "Righe per pagina",
            options=[50, 100, 200, 500, 1000, 10000],
            index=1,
            key=f"selectbox_{tipo_file}"
        )
    totale_pagine = math.ceil(totale_righe / righe_per_pagina) if righe_per_pagina > 0 else 1

    with col2:
        st.number_input(
            f"Vai alla pagina (1-{totale_pagine})",
            min_value=1,
            max_value=totale_pagine,
            key=key_session_pagina
        )



    col1, col2,col3 = st.columns([1,2,1])
    pagina_corrente = session_manager.get(key_session_pagina)

    with col1:
        st.button('⬅️ Precedente',
                  use_container_width=True,
                  disabled=(pagina_corrente <= 1),
                  key=f"prec_{tipo_file}",
                  on_click=decrementa_pagina,
                  args=(key_session_pagina,))
    with col2:
        st.markdown(
            f"<h4 style='text-align: center;'>Pagina {pagina_corrente} di {totale_pagine}</h4>",
            unsafe_allow_html=True)

    with col3:
        st.button('Successivo ➡️',
                  use_container_width=True,
                  disabled=(pagina_corrente >= totale_pagine),
                  key=f"succ_{tipo_file}",
                  on_click=incrementa_pagina,
                  args=(key_session_pagina,))

    st.divider()

    start_index = (pagina_corrente -1) * righe_per_pagina
    end_index = start_index + righe_per_pagina
    righe_da_mostrare = tutte_le_righe[start_index:end_index]

    st.header(f"Visualizzando righe da {start_index + 1} a {min(end_index, totale_righe)}")


    righe_formattate = [riga.dati for riga in righe_da_mostrare]
    lista_record = [vars(record) for record in righe_formattate]

    mostra_tabella_record(lista_record, campi_da_escludere=campi_da_escludere)



def mostra_tabella_record(dati, campi_da_escludere=None):
    if campi_da_escludere is None:
        campi_da_escludere = []
    df_originale = pd.DataFrame(dati)

    df_visualizzato = df_originale.drop(columns=campi_da_escludere)

    st.dataframe(df_visualizzato)


def show():

    st.title('Controllo')

    with st.spinner('Caricamento file...'):

        tab_1, tab_2, tab_3 = st.tabs(["File C1", "File C2", "File C3"])

        with tab_1:
            tab_file_c1()

        with tab_2:
            tab_file_c2()

        # with tab_3:
        #     tab_file_c3()
