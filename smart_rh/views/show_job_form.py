from smart_rh.services.firebase_service import FirebaseService
from smart_rh.models.job import Job
import streamlit as st

def show_job_form():

    st.markdown("### \U00002795 Cadastrar Nova Vaga")
    st.markdown("""
    **\U0001f4d6 Descrição:**  
    Nesta página você pode cadastrar novas vagas para que candidatos possam se candidatar.  
                
    \U0001f4a1 *Após cadastrar uma vaga, nossa IA vai poder analisar o curriculo que você fez upload em **Análise com IA** e verificar se a vaga que escolheu tem algum matche com seu curriculo!*
    """)

    with st.form("job_form", clear_on_submit=True):

        col1, col2 = st.columns(2)
        with col1:
            id_vaga = st.text_input("ID da Vaga*", help="Ex: dev_backend_01")

        with col2:
            title_vaga = st.text_input("Título da Vaga*")
        
        main_activity = st.text_area("Atividade Principal*")
        prerequisites = st.text_area("Pré-Requisitos*")
        differentials = st.text_area("Diferenciais")

        if st.form_submit_button("Cadastrar Vaga", type="primary"):
            if not all([id_vaga, title_vaga, main_activity, prerequisites]):
                st.error("Preencha os campos obrigatórios (*)")
            else:
                try:
                    nova_vaga = Job(
                        id=id_vaga,
                        title=title_vaga,
                        main_activity=main_activity,
                        prerequisites=prerequisites,
                        differentials=differentials or None
                    )
                    
                    FirebaseService().create_job(nova_vaga)
                    st.success("Vaga cadastrada!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Erro: {str(e)}")