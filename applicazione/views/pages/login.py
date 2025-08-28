import streamlit as st
from struttura.strutturaResult import Result, display_errore
from struttura.strutturaUtente import UtenteRepository
from applicazione.config import SessionKeys, SessionManager, Pagine, PaginePerRuolo


session_manager = SessionManager()
session_manager.initialize_state()




def check_input(username, password):
    if username is None or username == '':
        risultato = Result.failure('Inserire un Username o una Email', info='')
        display_errore(risultato)
        return
    if password is None or password == '':
        risultato = Result.failure('Inserire una Password', info='')
        display_errore(risultato)
        return
    return


def effettua_login(username, password):
    check_input(username, password)


    repo = UtenteRepository()

    auth_result = repo.autentica_utente(username, password)


    utente = auth_result.risultato

    session_manager.set(SessionKeys.key_utente_loggato(), utente)
    session_manager.set(SessionKeys.key_logged_in(), True)
    session_manager.set(SessionKeys.key_current_page(), Pagine.HOME)
    st.rerun()


def show():
    with st.container(
            horizontal_alignment="center"
    ):
        with st.container(
                border=True,
                width=500
        ):
            st.header("Login")
            username = st.text_input('Username o Email')
            password = st.text_input('Password', type="password")
            st.write(" ")
            st.write(" ")
            with st.container(
                    horizontal=True,
                    horizontal_alignment="right"
            ):
                login_button = st.button("Login", type="primary", width=150)
                # register_button = st.button("Registrati", type="tertiary")

                if login_button:
                    effettua_login(username, password)
