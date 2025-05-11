import streamlit as st
import tempfile
import logging
import os
import uuid
from services.firebase_service import FirebaseService
from models.job import Job
from models.analysis import Analysis
from services.analysis_extractor import  read_file, extract_data_analysis
from services.langchain_service import LangChainService
from config.langchain_config import LangChainConfig

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
            st.warning("Nenhuma vaga cadastrada! Crie uma vaga primeiro.", icon="⚠️")
            if st.button("\U00002795 Ir para Cadastro de Vagas"):
                st.session_state.current_page = "add_job"
                st.rerun()
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
                st.markdown(f"**Título:** {selected_job.title}")
                st.markdown(f"**Requisitos:** {selected_job.prerequisites}")
                st.markdown(f"**Atividades:** {selected_job.main_activity}")
                if selected_job.differentials:
                    st.markdown(f"**Diferenciais:** {selected_job.differentials}")

            # Upload de currículo
            st.subheader("\U0001f4c2 Envie seu currículo")
            uploaded_file = st.file_uploader(
                "Seu currículo (PDF ou DOCX)",
                type=["pdf", "docx"],
                key="resume_uploader"
            )

            analysis_button = st.button(
                "\U0001f50e Executar Análise com IA", 
                type="primary", 
                disabled=not uploaded_file
            )

            if uploaded_file and analysis_button:
                with st.spinner("Processando análise - Isso pode levar alguns minutos..."):
                    try:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("Processando arquivo...")
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name
                        progress_bar.progress(10)
                        
                        status_text.text("Extraindo texto do currículo...")
                        try:
                            cv_text = read_file(tmp_path)
                        except Exception as e:
                            logger.error(f"Erro ao ler arquivo: {str(e)}")
                            st.error(f"Não foi possível ler o arquivo. Certifique-se que é um PDF ou DOCX válido.")
                            return
                        progress_bar.progress(30)
                        
                        status_text.text("Gerando resumo com IA...")
                        markdown_summary = langchain.resume_cv(cv_text)
                        progress_bar.progress(60)
                        
                        status_text.text("Calculando compatibilidade com a vaga...")
                        score = langchain.generate_score(cv_text, selected_job.prerequisites) 
                        progress_bar.progress(80)
                        
                        status_text.text("Finalizando análise...")
                        analysis = extract_data_analysis(
                            resume_cv=markdown_summary,
                            job_id=selected_job.id,
                            resume_id=str(uuid.uuid4()),
                            score=score
                        )
                        
                        firebase.create_analysis(analysis)
                        progress_bar.progress(100)
                        status_text.empty()
                        
                        st.success("Análise concluída com sucesso!")
                        _display_analysis_results(analysis, langchain, cv_text, selected_job)

                    except Exception as e:
                        st.error(f"Erro durante a análise: {str(e)}")
                        logger.error(f"Erro na análise: {str(e)}", exc_info=True)
                    finally:
                        if 'tmp_path' in locals():
                            try:
                                os.unlink(tmp_path)
                            except:
                                pass

    except Exception as e:
        st.error(f"Erro geral: {str(e)}")
        logger.error(f"Erro crítico: {str(e)}", exc_info=True)

def _display_analysis_results(analysis: Analysis, langchain, cv_text, selected_job):
    """Exibe os resultados formatados corretamente"""
    st.divider()
    
    st.markdown(f"## {analysis.name}")
    
    score = analysis.score
    if score >= 8:
        score_color = "#2ecc71"
        score_emoji = "🌟"
        score_text = "Excelente Compatibilidade"
    elif score >= 6:
        score_color = "#27ae60"
        score_emoji = "✅"
        score_text = "Boa Compatibilidade"
    elif score >= 4:
        score_color = "#f39c12"
        score_emoji = "⚠️"
        score_text = "Compatibilidade Média"
    else:
        score_color = "#e74c3c"
        score_emoji = "❗"
        score_text = "Compatibilidade Baixa"
    
    st.markdown(
        f"### <span style='color:{score_color}'>{score_emoji} Pontuação: {score}/10 - {score_text}</span>",
        unsafe_allow_html=True
    )
    
    tab1, tab2 = st.tabs(["📊 Análise Básica", "📝 Análise Detalhada"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### \U0001f528 Habilidades Técnicas")
            if analysis.skills:
                for skill in analysis.skills:
                    st.markdown(f"- {skill}")
            else:
                st.markdown("*Não especificado no currículo*")
        
        with col2:
            st.markdown("### \U0001f393 Formação Acadêmica")
            if analysis.education:
                for edu in analysis.education:
                    st.markdown(f"- {edu}")
            else:
                st.markdown("*Não especificado no currículo*")
        
        st.markdown("### \U0001f310 Idiomas")
        if analysis.languages:
            for lang in analysis.languages:
                st.markdown(f"- {lang}")
        else:
            st.markdown("*Não especificado no currículo*")
    
    with tab2:
        with st.spinner("Gerando análise detalhada..."):
            try:
                detailed_analysis = langchain.generate_opnion(cv_text, selected_job.prerequisites)
                st.markdown(detailed_analysis)
            except Exception as e:
                st.error("Não foi possível gerar a análise detalhada.")
                logger.error(f"Erro na geração de análise detalhada: {str(e)}")
    
    st.divider()

    if st.button("\U0001f504 Fazer Nova Análise"):
        st.session_state.current_page = "analysis_job"
        st.rerun()