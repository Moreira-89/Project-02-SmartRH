from utils.FuncCadastroJob import FuncCadastroJob
from utils.FuncVisualizarVagas import FuncVisualizarVagas
import streamlit as st

st.title("Smart RH")

st.write("Bem-vindo ao Smart RH")


st.sidebar.button("\U0001F4BC Cadastrar Vaga", on_click=FuncCadastroJob)

st.sidebar.button("\U0001f4dd Visualizar Vagas", on_click=FuncVisualizarVagas)
