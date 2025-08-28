import streamlit as st

import applicazione.views.pages.login
from applicazione.config import Pagine, PaginePerRuolo, SessionKeys, SessionManager
from typing import Callable, List, Union, Any
from pathlib import Path
from struttura.strutturaUtente import Ruolo
import applicazione.views.pages as page
from enum import Enum


class Router:

    def __init__(self):
        self.session_manager = SessionManager()

        user = self.session_manager.get(SessionKeys.key_utente_loggato())
        if user:
            self.pages = PaginePerRuolo.get_pagine(user.ruolo)
        else:
            self.pages = [Pagine.LOGIN]

        if SessionKeys.key_current_page() not in st.session_state:
            self.session_manager.set(SessionKeys.key_current_page(), Pagine.HOME)





    def get_current_page(self) -> Pagine:
        return self.session_manager.get(SessionKeys.key_current_page())

    def set_current_page(self, page: Pagine):
        self.session_manager.set(SessionKeys.key_current_page(), page)

    def render_navigation(self):

        iterable_pages = None

        if isinstance(self.pages, dict):
            iterable_pages = self.pages.keys()
        elif isinstance(self.pages, list):
            iterable_pages = self.pages

        else:
            st.error(
                f"Errore di configurazione: 'pages' deve essere una lista o un dizionario, non {type(self.pages).__name__}.")
            return

        page_options = [page for page in iterable_pages if page != Pagine.LOGIN]

        for page in page_options:

            if st.sidebar.button(
                    page.value.capitalize(), key=f"nav_button_{page.value}", disabled=self.session_manager.get(SessionKeys.key_loading())
            ):
                if self.get_current_page() != page:
                    self.session_manager.start_loading()
                    self.set_current_page(page)
                    st.rerun()



    def render_current_page(self):

        with st.spinner('caricamento...'):
            current_page = self.get_current_page()

            if current_page == Pagine.LOGIN:
                page.login.show()
            elif current_page == Pagine.REGISTER:
                page.register.show()
            elif current_page == Pagine.HOME:
                page.home.show()
            elif current_page == Pagine.ALTRO:
                page.altro.show()
            elif current_page == Pagine.PROVA:
                page.prova.show()
            elif current_page == Pagine.TEST_1:
                page.test_1.show()
            elif current_page == Pagine.CONTROLLO:
                page.controllo.show()
            elif current_page == Pagine.FORK:
                page.fork.show()



            else:
                st.error(f"Pagina non trovata: {current_page}")
                self.set_current_page(Pagine.HOME)
                st.rerun()






