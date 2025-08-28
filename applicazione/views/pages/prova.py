import math
import time

import streamlit as st
from pathlib import Path
from applicazione.config import SessionKeys, SessionManager
from struttura.strutturaC1 import FileC1Repository
from applicazione.config import percorsi

session_manager = SessionManager()

FILE_C1 = 'applicazione/storage/file_c1.txt'


@st.cache_data
def carica_file(percorso_file):
    with open(percorso_file, 'r', encoding='utf-8') as f:
        return f.readlines()


def contenitore_c1():
    with st.container(border=True, horizontal_alignment='center'):
        st.header('FILE C1')
        btn_controllo_c1 = st.button('controllo', key='controllo_c1')


        btn_test_c1 = st.button('test', key='test_c1')



    return btn_controllo_c1, btn_test_c1

def contenitore_c2():
    with st.container(border=True, horizontal_alignment='center'):
        st.header('FILE C2')
        btn_controllo_c2 = st.button('controllo', key='controllo_c2')

        btn_test_c2 = st.button('test', key='test_c2')

    return btn_controllo_c2, btn_test_c2




def show():
    # tutte_le_righe = None
    # totale_righe = None
    # totale_pagine = None
    pagina_selezionata = None
    st.write('prova')

    with st.container(
            horizontal_alignment="center",
    ):
        with st.container(border=False,
                          horizontal=True,
                          horizontal_alignment='center',
                          width='stretch'):
            btn_controllo_c1, btn_test_c1 = contenitore_c1()
            contenitore_c2()


    if btn_controllo_c1:
        with st.spinner('Caricamento file in corso...'):
            session_manager.set(SessionKeys.key_file_c1(), carica_file(FILE_C1))
            tutte_le_righe = session_manager.get(SessionKeys.key_file_c1())
            totale_righe = len(tutte_le_righe)
        st.info(f"File '_{FILE_C1}_' caricato con successo. Totale righe: **{totale_righe:,}**".replace(',', '.'))


    with st.container(border=True):
        if session_manager.check(SessionKeys.key_file_c1()):
            tutte_le_righe = session_manager.get(SessionKeys.key_file_c1())
            totale_righe = len(tutte_le_righe)
        st.header("Opzioni di visualizzazione")
        with st.container( horizontal=True):
            righe_per_pagina = st.selectbox(
                "Righe per pagina",
                options=[50, 100, 200, 500, 1000],
                index=1
            )
            with st.container(border=True):
                # if tutte_le_righe is None or totale_righe is None:
                if session_manager.get(SessionKeys.key_file_c1()) is None:
                    st.warning('Caricare prima un file')
                else:
                    totale_pagine = math.ceil(totale_righe / righe_per_pagina)
                    try:
                        pagina_selezionata = st.number_input(
                            f"Vai alla pagina (1-{totale_pagine})",
                            min_value=1,
                            max_value=totale_pagine,
                            value=session_manager.get(SessionKeys.key_pagina_file_corrente())
                        )
                    except:
                        st.warning('Pagina selezionata superiore al numero di pagine')
                        session_manager.set(SessionKeys.key_pagina_file_corrente(), 1)
                        time.sleep(2)
                        st.rerun()
    if pagina_selezionata is not None:
        if pagina_selezionata != session_manager.get(SessionKeys.key_pagina_file_corrente()):
            session_manager.set(SessionKeys.key_pagina_file_corrente(), pagina_selezionata)
            st.rerun()

    # if pagina_selezionata > totale_pagine:
    #     st.warning('Pagina selezionata superiore al numero di pagine')
    #     session_manager.set(SessionKeys.key_pagina_file_corrente(), 1)
    #     time.sleep(3)
    #     st.rerun()


    # if tutte_le_righe is None or totale_righe is None or totale_pagine is None:
    if session_manager.get(SessionKeys.key_file_c1()) is None:
        st.warning('Caricare prima un file')
    else:
        col1, col2, col3 = st.columns([2,3,2])


        with col1:
            if st.button('⬅️ Precedente', use_container_width=True, disabled=(session_manager.get(SessionKeys.key_pagina_file_corrente()) <= 1)):
                # pagina_selezionata = session_manager.get(SessionKeys.key_pagina_file_corrente())
                pagina_precedente = pagina_selezionata -1
                session_manager.set(SessionKeys.key_pagina_file_corrente(), pagina_precedente)
                st.rerun()

        with col2:
            st.markdown(f"<h4 style='text-align: center;'>Pagina {session_manager.get(SessionKeys.key_pagina_file_corrente())} di {totale_pagine}</h4>", unsafe_allow_html=True)


        with col3:
            if st.button('Successivo ➡️', use_container_width=True, disabled=(session_manager.get(SessionKeys.key_pagina_file_corrente()) >= totale_pagine)):
                pagina_successiva = pagina_selezionata +1
                session_manager.set(SessionKeys.key_pagina_file_corrente(), pagina_successiva)
                st.rerun()


        st.divider()

        start_index = (session_manager.get(SessionKeys.key_pagina_file_corrente()) - 1) * righe_per_pagina
        end_index = start_index + righe_per_pagina


        righe_da_mostrare = tutte_le_righe[start_index:end_index]


        st.header(f"Visualizzazione delle righe da {start_index + 1} a {min(end_index, totale_righe)}")

        righe_formattate = []

        for i, riga_letta in enumerate(righe_da_mostrare):
            numero_riga_originale = start_index + i +1
            riga = riga_letta.dati
            righe_formattate.append(f"Record {numero_riga_originale}: {riga}")
            st.write(riga)
            st.write(len(riga))


        # st.text_area(
        #     label="Contenuro della pagina",
        #     value="\n".join(righe_formattate),
        #     height=600,
        #     key='contenuto_file'
        # )
        # st.write(righe_formattate)



    if btn_test_c1:
        # repo_c1 = FileC1Repository()
        #
        # with st.spinner('Sto controllando il file...'):
        #     controllo_result = repo_c1.controlla_file(FILE_C1)
        #
        # if controllo_result.is_failure():
        #     st.error(f"**{controllo_result.errore}**")
        #
        #     lista_errori = controllo_result.info
        #
        #     st.write('Dettaglio degli errori trovati:')
        #
        #     # st.write(lista_errori)
        #
        #     for errore in lista_errori:
        #         with st.expander(f"Errore validazione dei dati alla riga {errore['riga']}"):
        #             # st.error(f"{errore['messaggio']}\n\n")
        #
        #             st.error(errore['dettagli'])
        #
        # else:
        #     st.success(controllo_result.risultato)
        st.write('test')




