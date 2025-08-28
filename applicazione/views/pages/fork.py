import streamlit as st

link_progetto = "https://github.com/lorenzodint/gacep_1.git"
nome_ambiente_virtuale = 'mioAmbienteVirtuale'
nome_file_principale = 'main.py'


def show():
    st.header('FORK')


    st.header("Clonare il Progetto sul computer")

    st.markdown(f"Link del progetto: `{link_progetto}`")
    st.write("Per clonare il progetto sul computer basta eseguire il comando: `git clone`")
    st.info("""
        **Consiglio:** Per evitare di creare una cartella extra, puoi clonare il repository direttamente nella
        cartella in cui ti trovi. Apri il terminale, naviga fino alla tua cartella di lavoro
        (es. `cd C:\\Progetti\\nuovo-progetto`) e usa il comando `git clone` seguito da un punto (`.`).
        """)
    st.code('git clone <URL_DEL_REPOSITORY> .', language='bash', width=600)
    st.write("In questo caso, una volta dentro la nostra cartella del progetto eseguire da terminale:")
    st.code(f'git clone {link_progetto} .', language='bash', width=600)
    st.caption("IMPORTANTE: non dimenticare il punto finale per evitare una cartella extra.")

    st.divider()

    st.header("Creare un Ambiente Virtuale Python")
    st.markdown("""
    Un ambiente virtuale è una cartella isolata che contiene una specifica installazione di Python
    e tutti i pacchetti necessari per il tuo progetto. Questo evita conflitti tra le dipendenze
    di progetti diversi. È una pratica **fondamentale**.
    """)
    st.markdown("Una volta dentro la cartella del progetto, eseguire:")
    st.code('python -m venv <NOME_AMBIENTE_VIRTUALE>', language='bash', width=600)
    st.markdown(f"""
    Sostituire `<NOME_AMBIENTE_VIRTUALE>` con il nome che si vuole assegnare al nuovo ambiente, in genere si utilizza `venv`.
    
    Esempio ambiente virtuale con nome `{nome_ambiente_virtuale}`:
    """)
    st.code(f'python -m venv {nome_ambiente_virtuale}', language='bash', width=600)

    st.markdown(f"""
    Questo comando crea una nuova cartella chiamata `{nome_ambiente_virtuale}` che contiene il nuovo ambiente pulito.
    """)

    st.divider()

    st.header("Attivare l'Ambiente Virtuale")
    st.markdown("""
    Una volta che l'ambiente è stato creato bisogna **attivarlo** per poterlo usare. L'attivazione dice al terminale
    di usare la versione di Python e i pacchetti contenuti in quella cartella, invece di quelli globali.
    """)
    st.write("Eseguire nel terminale:")
    st.code('<NOME_AMBIENTE_VIRTUALE>\\Scripts\\activate', language='bash', width=600)
    st.write("In questo esempio:")
    st.code(f'{nome_ambiente_virtuale}\\Scripts\\activate', language='bash', width=600)


    st.markdown(f"""
    **Come si capisce se ha funzionato?** Il nome del tuo ambiente (`{nome_ambiente_virtuale}`) apparirà tra parentesi
    all'inizio della riga di comando, così:
    
    `({nome_ambiente_virtuale}) C:\\Progetti\\nuovo-progetto>`
    """)

    st.divider()

    st.header("Impostare l'Interprete Python nel tuo Editor")
    st.markdown("""
    Anche se il terminale sta usando l'ambiente virtuale, l' editor di codice (come VS Code o PyCharm) deve essere istruito a fare lo stesso. Altrimenti, quando verrà eseguito del codice, l'editor, userà l'interprete Python globale e non troverà i pacchetti installati.
    """)

    st.caption("Spesso gli editor di codice riconoscono un nuovo ambiente virtuale e al momento della creazione chiedono se questo vuole essere impostato come interprete")

    with st.expander("👨‍💻 Istruzioni per Visual Studio Code"):
        st.markdown(f"""
        1. Premi `Ctrl+Shift+P` per aprire la Command Palette.
        2. Digita e seleziona `Python: Select Interpreter`.
        3. Scegli l'interprete che ha `({nome_ambiente_virtuale})` nel nome o che punta al percorso `.\\{nome_ambiente_virtuale}\\Scripts\\python.exe`.
        """)


    with st.expander("🎓 Istruzioni per PyCharm"):
        st.markdown(f"""
        PyCharm è molto attento alla gestione degli interpreti a livello di progetto.
        1. Vai su **File > Settings...** (o `Ctrl+Alt+S`).
        2. Naviga a **Project: [nome-progetto] > Python Interpreter**.
        3. Seleziona **Add interpreter**.
        4. Nella nuova finestra, seleziona **Virtualenv Environment** a sinistra e la scheda **Existing** a destra.
        5. Clicca sui `...` e naviga fino a selezionare il file `python.exe` dentro la cartella `{nome_ambiente_virtuale}\\Scripts`.
        6. Conferma con **OK**.
        """)
        st.info(
            "**Scorciatoia:** Puoi anche cliccare sull'interprete mostrato nell'angolo in basso a destra della finestra di PyCharm per accedere rapidamente allo stesso menu.")

    st.divider()

    st.header("Installare le Dipendenze ed Eseguire il Progetto")
    st.markdown("""
    Il file `requirements.txt` elenca tutti i pacchetti necessari per funzionare.
    """)

    st.markdown(f"Assicurati che il tuo ambiente virtuale sia attivo (vedi il `({nome_ambiente_virtuale})` nel terminale) ed esegui:")
    st.code('pip install -r requirements.txt', language='bash', width=600)
    st.markdown(f"Questo comando leggerà il file e installerà tutte le librerie necessarie nel tuo ambiente `{nome_ambiente_virtuale}`.")

    st.markdown("""
    Individua il file principale del progetto (spesso chiamato `main.py`, `app.py` o simile) ed eseguilo dal terminale:
    """)
    st.code(f'python {nome_file_principale}', language='bash', width=600)
    st.write('In caso di applicazione Streamlit il comando è il seguente:')
    st.code(f"streamlit run {nome_file_principale}", language='bash', width=600)
