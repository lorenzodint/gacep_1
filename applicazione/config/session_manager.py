from typing import Any

import streamlit as st
from pydantic import BaseModel

from applicazione.config import Pagine


class SessionKeys(BaseModel):

    @staticmethod
    def key_loading() -> str:
        return 'loading'

    @staticmethod
    def key_current_page() -> str:
        return 'current_page'

    @staticmethod
    def key_logged_in() -> str:
        return 'logged_in'

    @staticmethod
    def key_utente_loggato() -> str:
        return 'utente_loggato'

    @staticmethod
    def key_file_c1() -> str:
        return 'file_c1'

    @staticmethod
    def key_file_c2() -> str:
        return 'file_c2'

    @staticmethod
    def key_file_c3() -> str:
        return 'file_c3'

    @staticmethod
    def key_pagina_file_corrente() -> str:
        return 'pagina_file_corrente'


class SessionManager:

    def __init__(self):
        self.initialize_state()

    @staticmethod
    def initialize_state():
        if SessionKeys.key_loading() not in st.session_state:
            st.session_state[SessionKeys.key_loading()] = False

        if SessionKeys.key_logged_in() not in st.session_state:
            st.session_state[SessionKeys.key_logged_in()] = False

        if SessionKeys.key_utente_loggato() not in st.session_state:
            st.session_state[SessionKeys.key_utente_loggato()] = None

        if SessionKeys.key_current_page() not in st.session_state:
            st.session_state[SessionKeys.key_current_page()] = Pagine.HOME

        # ________________________________________________________________________________________________
        if SessionKeys.key_file_c1() not in st.session_state:
            st.session_state[SessionKeys.key_file_c1()] = None
        if SessionKeys.key_file_c2() not in st.session_state:
            st.session_state[SessionKeys.key_file_c2()] = None
        if SessionKeys.key_file_c3() not in st.session_state:
            st.session_state[SessionKeys.key_file_c3()] = None
        if SessionKeys.key_pagina_file_corrente() not in st.session_state:
            st.session_state[SessionKeys.key_pagina_file_corrente()] = 1

    @staticmethod
    def get(key: str, default: Any = None):
        return st.session_state.get(key, default)

    @staticmethod
    def set(key: str, value: Any):
        st.session_state[key] = value

    @staticmethod
    def delete(key: str):
        if key in st.session_state:
            del st.session_state[key]

    @staticmethod
    def check(key: str):
        if key in st.session_state:
            if st.session_state[key] is not None:
                return True
        return False

    @property
    def session(self):
        return st.session_state

    # @property
    def logout(self):
        for k in st.session_state:
            self.delete(k)
        self.initialize_state()



    # @property
    def start_loading(self):
        SessionManager.set(SessionKeys.key_loading(), True)
        # return

    # @property
    def stop_loading(self):
        SessionManager.set(SessionKeys.key_loading(), False)
        # return

