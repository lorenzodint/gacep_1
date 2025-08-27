from enum import Enum
from struttura.strutturaUtente import Ruolo


class Pagine(Enum):
    LOGIN = 'login'
    HOME = 'home'
    REGISTER = 'register'
    ALTRO = 'altro'
    PROVA = 'prova'
    TEST_1 = 'test_1'
    CONTROLLO = 'controllo'


    def get_pages(cls):
        return {page.name: page.value for page in cls}


class PaginePerRuolo:
    @staticmethod
    def get_pagine(ruolo: Ruolo):
        if ruolo == Ruolo.SUPERADMIN:
            return [Pagine.HOME, Pagine.REGISTER]
        elif ruolo == Ruolo.ADMIN:
            return [Pagine.HOME]
        elif ruolo == Ruolo.UTENTE:
            return [Pagine.HOME]
        else:
            return [Pagine.HOME, Pagine.ALTRO, Pagine.PROVA, Pagine.TEST_1]
