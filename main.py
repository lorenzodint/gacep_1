import os.path

import streamlit as st
from struttura.strutturaResult import Result, display_errore
from struttura.strutturaDB import sincronizza_tabella
from struttura.strutturaUtente import DatiUtenteModel, UtenteBuilder, Utente
from applicazione import App
import tomllib

def genera_requirements():
    file_pyproject = "pyproject.toml"
    file_requirements = "requirements.txt"

    print("Avvio la generazione del file requirements.txt...")
    if os.path.exists(file_requirements):
        try:
            os.remove(file_requirements)
            print(f"✔️ File '{file_requirements}' esistente eliminato con successo.")
        except OSError as e:
            print(f"❌ Errore durante l'eliminazione del file: {e}")
            return
    try:
        with open(file_pyproject, 'rb') as f:
            data = tomllib.load(f)

            dipendenze = data.get("project", {}).get("dependencies", [])

            if not dipendenze:
                print("⚠️ Attenzione: Nessuna dipendenza trovata in [project.dependencies] dentro pyproject.toml.")
                return

            with open(file_requirements, "w", encoding='utf-8') as f:
                for dep in dipendenze:
                    f.write(f"{dep}\n")
            print(f"✅ File '{file_requirements}' creato con successo con {len(dipendenze)} dipendenze.")

    except FileNotFoundError:
        print(f"❌ Errore: Il file '{file_pyproject}' non è stato trovato nella directory corrente.")
    except tomllib.TOMLDecodeError as e:
        print(f"❌ Errore nella sintassi del file '{file_pyproject}': {e}")
    except Exception as e:
        print(f"❌ Si è verificato un errore inaspettato: {e}")



def db_config():
    modelli = [
        DatiUtenteModel,
    ]
    tabelle = [
        'utenti',
    ]

    campi_unici = [
        ['username', 'email', 'telefono', 'codice_fiscale'],
    ]

    for i in range(len(modelli)):
        db_result = sincronizza_tabella(
            model=modelli[i],
            table_name=tabelle[i],
            unique_fields=campi_unici[i]
        )


def test_creazione_utente():
    builder = UtenteBuilder()

    dati_utente = (builder
                   .set_username("marioRox")
                   .set_email('mario@gmail.com')
                   .set_password("1")
                   .set_citta('Milano')
                   )

    creazione = Utente.crea(dati_utente)

    if creazione.is_success():
        utente: Utente = creazione.risultato

        st.write(utente.username)
        st.write(utente.citta)
        st.divider()
        st.write(utente.dati)


def main():
    genera_requirements()
    # db_config()

    app = App()
    app.run()


if __name__ == "__main__":
    main()
