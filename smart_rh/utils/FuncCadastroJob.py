from firebase.FirebaseAPI import FirebaseAPI
import streamlit as st

firebase_config = st.secrets["FIREBASE"]


@st.dialog("\U0001F4BC Cadastro de Vaga")
def FuncCadastroJob():

    with st.form("Cadastro de Vaga", clear_on_submit=True):

        col1, col2 = st.columns(2)
        with col1:
            id_vaga = st.text_input(
                "N° de identificação da Vaga*",
                help="Use um ID único (ex: 'dev_backend_01')",
            )
        with col2:
            title_vaga = st.text_input("Título da Vaga*")

        main_activity = st.text_area("Atividade Principal*")
    
        prerequisites = st.text_input("Pré-Requisitos*")

        differentials = st.text_input("Diferenciais")

        submit_button = st.form_submit_button("Cadastrar")

        if submit_button:
            if not all([id_vaga, title_vaga, main_activity, prerequisites]):
                st.error("Preencha os campos obrigatórios (*)")

            else:
                try:
                    firebase = FirebaseAPI(
                        database_url=firebase_config["DATABASE_URL"],
                        secret_key=firebase_config["DATABASE_SECRET"],
                    )

                    firebase.create_document(
                        "vagas",
                        id_vaga,
                        {
                            "title": title_vaga,
                            "main_activity": main_activity,
                            "prerequisites": prerequisites,
                            "differentials": differentials if differentials else None,
                        },
                    )
                    st.success("\u2705 Vaga cadastrada com sucesso!")

                except Exception as e:
                    st.error(f"Erro ao cadastrar vaga: {e}")
