from typing import Optional
from struttura.strutturaResult import Result, display_errore
from struttura.strutturaC1 import FileC1, RecordC1

valori_per_campo_sesso_dell_utente = {
    "1": {
        "messaggio": "Maschio"
    },
    "2": {
        "messaggio": "Femmina"
    }
}


class ControlloFileC1:
    def __init__(self, file: FileC1):
        self.record: Optional[RecordC1] = None
        self.fine_ricetta: bool = False
        self.lista_errori = []
        self.file: FileC1 = file
        self.riga = 0
        self.limite_massimo_errori = 100
        self.limite_raggiunto: bool = False


    def _controllo_limite_errori(self):
        if len(self.lista_errori) >= self.limite_massimo_errori:
            self.limite_raggiunto = True
        return

    def _controllo_se_fine_ricetta(self):
        if self.record.get_progressivo_riga_per_ricetta == '99':
            return True
        return False

    def _controllo_sesso_dell_utente(self):
        valore = self.record.get_sesso_dell_utente

        if not valore in valori_per_campo_sesso_dell_utente:
            self.lista_errori.append(
                {
                    "riga": self.riga,
                    "messaggio": f"Valore non atteso per campo 'sesso_dell_utente', valori attesi: {[v for v in valori_per_campo_sesso_dell_utente]}",
                    "valore": valore
                }
            )

        return


    def controllo(self):

        for record in self.file:
            self._controllo_limite_errori()
            if self.limite_raggiunto:
                break
            self.record = record
            self.riga +=1

            self.fine_ricetta = self._controllo_se_fine_ricetta()

            self._controllo_sesso_dell_utente()

        if self.limite_raggiunto:
            risultato = Result.failure(
                f"Il File non può essere accettato poichè ha raggiunto la soglia massima di {self.limite_massimo_errori} errori",
                info=f"Sono state controllate {self.riga} righe su un totale di {len(self.file.records)}"
            )
            display_errore(risultato)
            raise

        if len(self.lista_errori) > 0:
            return Result.failure(
                self.lista_errori
            )
        return Result.success(f"File valido")

