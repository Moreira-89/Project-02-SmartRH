from utils.FuncCadastroJob import FuncCadastroJob
from utils.FuncVisualizarVagas import FuncVisualizarVagas
from utils.FunUploadFile import FunUploadFile
import streamlit as st

st.sidebar.title("Ferramentas:")

st.sidebar.button("\U0001F4BC Cadastrar Vaga", on_click=FuncCadastroJob)

st.sidebar.button("\U0001f4dd Visualizar Vagas", on_click=FuncVisualizarVagas)

st.sidebar.button("\U0001F4BC Upload de Arquivos", on_click=FunUploadFile)

st.sidebar.markdown("---")

st.title("Smart RH")

st.write("Bem-vindo ao Smart RH")
