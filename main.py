import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio

# st.set_page_config(layout = 'wide')
st.sidebar.title('ESMFold')
st.sidebar.write(
    '[*ESMFold*](https://esmatlas.com/about) представляет собой сквозной предсказатель структуры белка с одной последовательностью, основанный на языковой модели ESM-2.')

st.sidebar.divider()


# stmol
def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb, 'pdb')
    pdbview.setStyle({'cartoon': {'color': 'spectrum'}})
    pdbview.setBackgroundColor('white')  # ('0xeeeeee')
    pdbview.zoomTo()
    showmol(pdbview, height=500, width=800)


# Protein sequence input
DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
txt = st.sidebar.text_area('Ввод последовательности', DEFAULT_SEQ, height=176)


# st.write(back_translate_to_dna(txt))

# ESMfold


def update(sequence=txt):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence,
                             verify=False)

    name = sequence[:3] + sequence[-3:]
    pdb_string = response.content.decode('utf-8')

    with open('predicted.pdb', 'w') as f:
        f.write(pdb_string)

    struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"])
    b_value = round(struct.b_factor.mean(), 4)

    # Display protein structure
    st.subheader('Bизуализация предсказанной структуры белка')
    render_mol(pdb_string)

    # plDDT value is stored in the B-factor field
    st.subheader('plDDT')
    st.write('plDDT представляет собой оценку достоверности прогноза в расчете на остаток по шкале от 0 до 100.')
    st.info(f'plDDT: {b_value}')

    st.download_button(
        label="Скачать PDB",
        data=pdb_string,
        file_name='predicted.pdb',
        mime='text/plain',
    )


predict = st.sidebar.button('Предсказать', on_click=update)
