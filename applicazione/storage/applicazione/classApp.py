import streamlit as st
from applicazione.utils import Router
from applicazione.config import SessionKeys,SessionManager, Pagine,PaginePerRuolo
from struttura.strutturaUtente import Ruolo
from applicazione.views import pages as page










class App:

    def __init__(self):
        self.session_manager = SessionManager()

        self.session_manager.initialize_state()


        st.set_page_config(
            layout="wide"
        )

    def run(self):
        if not self.session_manager.get(SessionKeys.key_logged_in()):
            # st.info('non loggato')
            self.session_manager.set(SessionKeys.key_current_page(), Pagine.LOGIN)
            page.login.show()

        else:
            # st.info('loggato')

            self.user = self.session_manager.get(SessionKeys.key_utente_loggato())

            self.router = Router()

            if self.router.get_current_page() == Pagine.LOGIN:
                # st.info('loggato con pagina login')
                self.router.set_current_page(Pagine.HOME)


            st.sidebar.write(f"Benvenuto {self.user.username}")
            st.sidebar.caption(f"Ruolo: {self.user.ruolo}")
            st.sidebar.header('Menu')
            st.sidebar.divider()
            self.router.render_navigation()
            st.sidebar.divider()

            if st.sidebar.button('Logout'):
                # self.session_manager.set(SessionKeys.key_logged_in(), False)
                # self.session_manager.set(SessionKeys.key_utente_loggato(), None)
                self.session_manager.logout
                st.rerun()

            self.router.render_current_page()

        # st.write(self.session_manager.session)
