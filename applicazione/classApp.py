import streamlit as st

from applicazione.config import SessionKeys, SessionManager, Pagine
from applicazione.utils import Router
from applicazione.views import pages as page


class App:


    def __init__(self):
        self.session_manager = SessionManager()

        self.session_manager.initialize_state()

        self.is_loading = self.session_manager.get(SessionKeys.key_loading())

        self.primary_color = st.get_option("theme.primaryColor")
        self.overlay_color = "rgba(255,255,255,0.5)" if st.get_option("theme.base") == "light" else "rgba(0,0,0,0.5)"

        st.set_page_config(
            layout="wide"
        )

        self.overlay_css = f"""
                <style>
                .overlay {{
                    position:fixed;
                    top:0;
                    left:0;
                    width:100vw;
                    height:100vh;
                    background-color:{self.overlay_color};
                    z-index:9999;
                    cursor:wait;
                    display: flex;
                    justify-content:center;
                    align-items:center;
                }}
                
                
                .loader {{
                  width: 48px;
                  height: 48px;
                  border-radius: 50%;
                  display: inline-block;
                  border-top: 3px solid {self.primary_color};
                  border-right: 3px solid transparent;
                  box-sizing: border-box;
                  animation: rotation 1s linear infinite;
                }}
                
                @keyframes rotation {{
                  0% {{
                    transform: rotate(0deg);
                  }}
                  100% {{
                    transform: rotate(360deg);
                  }}
                }} 
                </style>
                """

        self.overlay_html = """
        <div class="overlay">
            <span class="loader"></span>
        </div>
        """


    def run(self):
        if self.is_loading:
            st.markdown(self.overlay_css, unsafe_allow_html=True)
            st.markdown(self.overlay_html, unsafe_allow_html=True)

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
                self.session_manager.logout()
                st.rerun()
            # st.sidebar.write(self.session_manager.get(SessionKeys.key_loading()))

            self.router.render_current_page()
            # try:
            #     self.router.render_current_page()
            # finally:
            #     if self.session_manager.get(SessionKeys.key_loading()):
            #         self.session_manager.stop_loading
            #         st.rerun()


            if self.is_loading:
                self.session_manager.stop_loading()
                st.rerun()

        # st.write(self.session_manager.session)

