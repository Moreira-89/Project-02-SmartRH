from views.show_job_form import show_job_form
from views.show_jobs_page import show_jobs_page
from views.FunUploadFile import FunUploadFile
from views.config_page import show_config_page
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
    
    if st.button("\U0001f3e0 Página Inicial"):
        change_page("home")
    
    if st.button("\U0001f4cb Visualizar Vagas"):
        change_page("view_jobs")
    
    if st.button("\U00002795 Cadastrar Vaga"):
        change_page("add_job")
    
    if st.button("\U0001f4e4 Upload Currículos"):
        change_page("upload_resumes")
    
    if st.button("\u2699 Configurações"):
        change_page("config_page")
    
    st.markdown("---")
    st.caption("v1.0 | © 2025 Smart RH")

if st.session_state.current_page == "home":
    st.title("Bem-vindo ao Smart RH")
    st.markdown("""
    **Sistema de gerenciamento de vagas e currículos**
    
    👈 Use o menu lateral para:
    - Visualizar vagas cadastradas
    - Cadastrar novas oportunidades
    - Enviar currículos
    """)

elif st.session_state.current_page == "view_jobs":
    show_jobs_page()

elif st.session_state.current_page == "add_job":
    show_job_form()

elif st.session_state.current_page == "upload_resumes":
    FunUploadFile()

elif st.session_state.current_page == "config_page":
    show_config_page()