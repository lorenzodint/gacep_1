from applicazione.config import *
from struttura.strutturaC2 import FileC2Repository, FileC2, ControlloFileC2
from struttura.strutturaResult import display_errore

session_manager = SessionManager()

FILE_C2 = percorsi.get_storage() + 'test_c2.txt'


@st.cache_data
def control_file(file):
    repo_c2 = FileC2Repository()

    controllo_result = repo_c2.controlla_file(file)

    # st.write(controllo_result)
    if controllo_result.is_failure():
        display_errore(controllo_result)
        st.stop()

    oggetto_result = repo_c2.carica_da_file(file)
    if oggetto_result.is_failure():
        display_errore(oggetto_result)
        st.stop()

    file_c2: FileC2 = oggetto_result.risultato

    # st.write(file_c2.dati)
    # st.write(len(file_c2.records))
    # st.info('File caricato, inizio controllo e validazione')
    return file_c2


def show():
    st.title('test 1')

    btn_prova_c2 = st.button('prova c2')

    if btn_prova_c2:
        with st.spinner('Controllo file...', show_time=True):
            file = control_file(FILE_C2)

        validatore = ControlloFileC2(file)

        result_validatore = validatore.controllo()

        if result_validatore.is_failure():
            lista_errori = result_validatore.errore

            if len(lista_errori) > 0:
                for errore in lista_errori:
                    with st.expander(f"Errore riga: **{errore['riga']}**"):
                        st.error(errore['messaggio'])
                        st.warning(f"Valore ricevuto: *'{errore['valore']}'*")
            else:
                st.success('Nessun errore riscontrato durante i controllo del file')
