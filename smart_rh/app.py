from views.show_job_form import show_job_form
from views.show_jobs_page import show_jobs_page
from views.show_job_upload_file import show_job_upload_file
from views.config_page import show_config_page
from views.analysis_ia_page import show_analysis_page
import streamlit as st


st.set_page_config(
    page_title="Smart RH",
    page_icon="\U0001f4bc",
    layout="wide"
)

if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

def change_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

with st.sidebar:
    st.title("\U0001f4bc Smart RH")
    st.markdown("---")
    
    if st.button("\U0001f3e0 Home"):
        change_page("home")

    if st.button("\U0001f50e Análise com IA"):
        change_page("analysis_job")

    if st.button("\U00002795 Cadastrar Vaga"):
        change_page("add_job")
    
    if st.button("\U0001f4cb Visualizar Vagas"):
        change_page("view_jobs")
    
    if st.button("\U0001f4e4 Upload de Currículos"):
        change_page("upload_resumes")
    
    if st.button("\u2699 Configurações"):
        change_page("config_page")
    
    st.markdown("---")

    st.caption("v1.0 | © 2025 Smart RH")

if st.session_state.current_page == "home":
    st.title("Bem-vindo ao Smart RH")
    st.markdown("""
    **\U0001f4bb Descrição:**  
    Sistema inteligente de recrutamento que conecta candidatos às melhores oportunidades.  
    
    \U0001f680 **Funcionalidades:**  
    - \U0001f4bc Cadastrar vagas detalhadas  
    - \U0001f50d Visualizar oportunidades disponíveis  
    - \U0001f4e5 Upload de Currículos (em breve)  
    - \U0001f4ca Análise por IA (em desenvolvimento)  
    """)
    st.divider()

elif st.session_state.current_page == "view_jobs":
    show_jobs_page()

elif st.session_state.current_page == "add_job":
    show_job_form()

elif st.session_state.current_page == "upload_resumes":
    show_job_upload_file()

elif st.session_state.current_page == "config_page":
    show_config_page()

elif st.session_state.current_page == "analysis_job":
    show_analysis_page()