import streamlit as st
import tempfile
import logging
from services.firebase_service import FirebaseService
from models.job import Job
from models.analysis import Analysis
from services.analysis_extractor import (
    read_uploaded_file,
    read_docx,
    extract_data_analysis
)
from services.langchain_service import LangChainService
from config.langchain_config import LangChainConfig
import os
import uuid

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def show_analysis_page():
    st.markdown("### \U0001f50e Análise de Compatibilidade IA")
    st.markdown("""
    **\U0001f4a1 Passo a Passo:**
    1. Selecione uma vaga
    2. Envie seu currículo (PDF/DOCX)
    3. Clique em analisar
                
    Caso você não tenha a vaga para o seu currículo, você pode criar uma vaga acessando a opção ao lado **"Cadastrar Nova Vaga"**.
    """)

    st.markdown("---")

    try:
        # Inicializa serviços
        firebase = FirebaseService()
        langchain = LangChainService(LangChainConfig())

        # Carrega vagas
        vagas = firebase.get_jobs()
        if not vagas:
            st.warning("Nenhuma vaga cadastrada!", icon="⚠️")
            return

        # Seleção de vaga
        selected_job = st.selectbox(
            "\U0001f4cb Selecione a vaga:",
            options=vagas,
            format_func=lambda vaga: f"{vaga.title}",
            index=None
        )

        if selected_job:
            st.session_state.selected_job = selected_job
            
            # Exibe detalhes da vaga
            with st.expander("\U0001f4ca Detalhes da Vaga", expanded=True):
                st.markdown(f"**Requisitos:** {selected_job.prerequisites}")
                st.markdown(f"**Atividades:** {selected_job.main_activity}")

            # Upload de currículo
            st.subheader("\U0001f4c2 Envie seu currículo")
            uploaded_file = st.file_uploader(
                "Seu currículo (PDF ou DOCX)",
                type=["pdf", "docx"],
                key="resume_uploader"
            )

            if uploaded_file and st.button("\U0001f50e Executar Análise com IA", type="primary"):
                with st.spinner("Processando análise - Isso pode levar alguns minutos..."):
                    try:
                        # Salva temporariamente o arquivo
                        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name

                        # Extrai texto do arquivo
                        if uploaded_file.type == "application/pdf":
                            cv_text = read_uploaded_file(tmp_path)
                            
                        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                            cv_text = read_docx(tmp_path)
                            
                        else:
                            raise ValueError("Formato de arquivo não suportado")

                        markdown_summary = langchain.resume_cv(cv_text)
                        score = langchain.generate_score(cv_text, selected_job.prerequisites)
                        
                        analysis = extract_data_analysis(
                            resum_cv=markdown_summary,
                            job_id=selected_job.id,
                            resum_id=str(uuid.uuid4()),
                            score=score
                        )

                        firebase.create_analysis(analysis)

                        st.success("Análise concluída com sucesso!")
                        _display_analysis_results(analysis)

                    except Exception as e:
                        st.error(f"Erro durante a análise: {str(e)}")
                        logger.error(f"Erro na análise: {str(e)}", exc_info=True)
                    finally:
                        if 'tmp_path' in locals():
                            os.unlink(tmp_path)

    except Exception as e:
        st.error(f"Erro geral: {str(e)}")
        logger.error(f"Erro crítico: {str(e)}", exc_info=True)

def _display_analysis_results(analysis: Analysis):
    """Exibe os resultados formatados corretamente"""
    st.divider()
    
    # Cabeçalho
    st.markdown(f"## {analysis.name}")
    
    # Pontuação com cor condicional
    score_color = "#2ecc71" if analysis.score >= 7 else "#f39c12" if analysis.score >= 4 else "#e74c3c"
    st.markdown(
        f"### <span style='color:{score_color}'>\U0001f3c6 Pontuação: {analysis.score}/10</span>",
        unsafe_allow_html=True
    )
    
    # Seções organizadas
    sections = [
        ("\U0001f528 Habilidades Técnicas", analysis.skills),
        ("\U0001f393 Formação Acadêmica", analysis.education),
        ("\U0001f310 Idiomas", analysis.languages)
    ]
    
    for emoji_title, items in sections:
        with st.container():
            st.markdown(f"### {emoji_title}")
            if items:
                for item in items:
                    st.markdown(f"- {item}")
            else:
                st.markdown("*Não especificado no currículo*")
            st.markdown("---")
    
    # Botão de ação
    st.button("\U0001f504 Fazer Nova Análise", on_click=lambda: st.session_state.clear())