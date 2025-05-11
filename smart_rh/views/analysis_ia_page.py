import streamlit as st
from services.firebase_service import FirebaseService
from models.job import Job
import pandas as pd

def show_analysis_page():
    st.markdown("### \U0001f50e Análise de Compatibilidade IA")
    st.markdown("""
    **\U0001f4a1 Passo a Passo:**
    1. Selecione uma vaga
    2. Envie seu currículo (PDF/DOCX)
    3. Clique em analisar
                
    Caso você não tenha a vaga para o seu currilo você pode criar uma vaga acessando a opção ao lado **"Cadastrar Nova Vaga"**.
    """)

    st.markdown("---")

    try:
        service = FirebaseService()
        
        vagas = service.get_jobs()
        if not vagas:
            st.warning("Nenhuma vaga cadastrada!", icon="⚠️")
            return

        selected_job = st.selectbox(
            "\U0001f4cb Selecione a vaga:",
            options=vagas,
            format_func=lambda vaga: f"{vaga.title} | {vaga.id}",
            index=None
        )

        selected_job = None

        if selected_job:
            st.session_state.selected_job = selected_job
            with st.expander("\U0001f4ca Detalhes da Vaga", expanded=True):
                st.markdown(f"**Requisitos:** {selected_job.prerequisites}")
                st.markdown(f"**Atividades:** {selected_job.main_activity}")

            st.subheader("\U0001f4c2 Envie seu currículo")
            uploaded_file = st.file_uploader(
                "Seu currículo (PDF ou DOCX)",
                type=["pdf", "docx"],
                accept_multiple_files=False,
                key="resume_uploader"
            )

            if uploaded_file:
                if st.button("\U0001f50e Executar Análise com IA", type="primary"):
                    pass
                
    except Exception as e:
        st.error(f"Erro na análise: {str(e)}")