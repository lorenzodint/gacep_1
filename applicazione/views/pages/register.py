import streamlit as st
from struttura.strutturaResult import Result, display_errore
from struttura.strutturaUtente import UtenteRepository, UtenteBuilder, Utente
from applicazione.config import SessionKeys, SessionManager, Pagine, PaginePerRuolo

session_manager = SessionManager()
session_manager.initialize_state()


def check_input(username, email, password):
    if username is None or username == '':
        risultato = Result.failure('Il campo Username non può essere vuoto')
        display_errore(risultato, show_avviso=False)
        return
    if email is None or email == '':
        risultato  =Result.failure('Il campo Email non può essere vuoto')
        display_errore(risultato, show_avviso=False)
        return
    if password is None or password == '':
        risultato = Result.failure('Il campo Password non può essere vuoto')
        display_errore(risultato, show_avviso=False)
        return
    return


def show():


    with st.container(
        horizontal_alignment="center"
    ):
        with st.container(
            border=True,
            width=500,
            horizontal=False
        ):
            st.header('Registrazione')
            username = st.text_input('Username')
            email = st.text_input("Email")
            password = st.text_input('Password', type="password")

            if st.button('Registra'):
                check_input(username, email, password)

                utente_dati = UtenteBuilder()

                utente_dati.set_username(username)
                utente_dati.set_email(email)
                utente_dati.set_password(password)







                repo = UtenteRepository()

                regist_result = repo.registra_utente(utente_dati)


                st.write(regist_result)