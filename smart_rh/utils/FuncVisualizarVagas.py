from firebase.FirebaseAPI import FirebaseAPI
import streamlit as st

firebase_config = st.secrets["FIREBASE"]

@st.dialog("\U0001f4dd Visualizar Vagas")
def FuncVisualizarVagas():

    firebase = FirebaseAPI(
        database_url=firebase_config["DATABASE_URL"],
        secret_key=firebase_config["DATABASE_SECRET"],
    )

    vagas = firebase.get_document(collection="vagas") or {}

    if not vagas:
        st.error("\U0001F6A7 Nenhuma vaga cadastrada")
        return
    
    for vaga_id, vaga_data in vagas.items():
        with st.container(border=True):
                st.markdown(f"### \U0001F194 ID: `{vaga_id}`")
                st.markdown(f"#### \U0001F4CB {vaga_data.get('title', 'Sem título')}")

                cols = st.columns(2)
                with cols[0]:
                    st.markdown(f"**\U0001F3AF Atividade Principal:**  \n{vaga_data.get('main_activity', 'Não informado')}")
                with cols[1]:
                    st.markdown(f"**\U0001F4DA Pré-Requisitos:**  \n{vaga_data.get('prerequisites', 'Não informado')}")
                st.markdown(f"**\U0001F4D1 Diferenciais:**  \n{vaga_data.get('differentials', 'Não informados')}")
    
