import time
import asyncio
import streamlit as st
from applicazione.config import SessionKeys, SessionManager, Pagine, percorsi
from struttura.strutturaResult import Result, display_errore
from pathlib import Path
import os

session_manager = SessionManager()
session_manager.initialize_state()

mostra_avviso = False


def reset_session():
    session_manager.set(SessionKeys.key_file_c1(), None)
    session_manager.set(SessionKeys.key_file_c2(), None)
    session_manager.set(SessionKeys.key_file_c3(), None)
    # session_manager.set(SessionKeys.key(), None)

def reset_storage():
    storage = percorsi.get_storage()
    if os.path.exists(storage):
        try:
            os.remove(storage)
            print(f"✔️ File '{storage}' esistente eliminato con successo.")
        except OSError as e:
            print(f"❌ Errore durante l'eliminazione del file: {e}")
            return

    os.mkdir(storage)
    with open(f"{storage}demo.txt", "w") as f:
        f.write("")


# def check_file(file_c1, file_c2, file_c3):
def check_file(file_c1, file_c2):

    if file_c1 is None:
        risultato = Result.failure('File C1 mancante o non caricato correttamente')
        display_errore(risultato)
        return False
    if file_c2 is None:
        risultato = Result.failure('File C2 mancante o non caricato correttamente')
        display_errore(risultato)
        return False
    # if file_c3 is None:
    #     risultato = Result.failure('File C3 mancante o non caricato correttamente')
    #     display_errore(risultato)
    #     return False
    return True


@st.fragment
def caricamento_file():
    with st.container(
            border=True,
            horizontal=True,
            horizontal_alignment="distribute"
    ):
        file_c1 = st.file_uploader("File C1", type=['txt'])
        file_c2 = st.file_uploader("File C2", type=['txt'])
        # file_c3 = st.file_uploader("File C3", type=['txt'])

    return file_c1, file_c2, # file_c3


def show():
    reset_session()
    reset_storage()
    st.header('Carica i file di testo')



    # file_c1, file_c2, file_c3 = caricamento_file()
    file_c1, file_c2 = caricamento_file()

    with st.container(
            horizontal=True,
            horizontal_alignment='center'
    ):
        procedi_button = st.button('Procedi con questi file', width=300, type="primary")
        # controllo = st.button('controllo')

    if procedi_button:
        # if check_file(file_c1, file_c2, file_c3):
        if check_file(file_c1, file_c2):
            with st.spinner('Salvataggio dei file...'):
                try:
                    storage_path = Path('applicazione/storage')
                    storage_path.mkdir(parents=True, exist_ok=True)

                    (storage_path / 'file_c1.txt').write_bytes(file_c1.getvalue())
                    (storage_path / 'file_c2.txt').write_bytes(file_c2.getvalue())
                    # (storage_path / 'file_c3.txt').write_bytes(file_c3.getvalue())

                    st.toast('File caricati e salvati correttamente', icon=":material/check_box:")

                    session_manager.set(SessionKeys.key_current_page(), Pagine.CONTROLLO)
                    st.rerun()







                except Exception as e:
                    risultato = Result.failure(f"Errore durante il salvataggio dei file", info=f"{e}")
                    display_errore(risultato)
                    raise
        else:
            st.header('no')

    # if controllo:
    #     session_manager.set(SessionKeys.key_current_page(), Pagine.CONTROLLO)
    #     st.rerun()

