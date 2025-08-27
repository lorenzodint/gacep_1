from typing import Optional, Any
from datetime import datetime
from pydantic import Field
import streamlit as st
from dataclasses import dataclass


@dataclass
class Result:
    stato: bool = Field(default=True)
    risultato: Optional[Any] = Field(default=None)
    errore: Optional[str] = Field(default=None)
    info: Optional[str] = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.now)

    @classmethod
    def success(cls, risultato, info=None):
        return cls(stato=True, risultato=risultato, info=info)

    @classmethod
    def failure(cls, errore, info=None):
        return cls(stato=False, errore=errore, info=info)

    def is_success(self) -> bool:
        return self.stato

    def is_failure(self) -> bool:
        return not self.stato


def display_errore(risultato: Result):
    @st.dialog("Errore", width="large", on_dismiss="rerun")
    def show_error(risultato: Result):
        st.error(risultato.errore)
        if risultato.info is not None:
            with st.expander("Info"):
                st.warning(risultato.info)

    show_error(risultato)
    st.stop()
