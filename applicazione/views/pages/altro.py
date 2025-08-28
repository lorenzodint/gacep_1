import streamlit as st
from struttura.strutturaResult import Result, display_errore
from pydantic import ValidationError
from applicazione.config import SessionManager, SessionKeys


session_manager = SessionManager()

def show():
    st.title('Altro')





