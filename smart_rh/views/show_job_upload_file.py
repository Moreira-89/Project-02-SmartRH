import streamlit as st

def show_job_upload_file():
    st.markdown("### \U0001f4e4 Upload de Currículos")
    st.divider()
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem; border: 2px dashed #666; border-radius: 1rem;'>
        <h3>\U0001F6A7 Funcionalidade em Construção \U0001F6A7 </h3>
        <p>Estamos trabalhando para trazer a opção de salvamento de currilos no banco de dados em breve!</p>
        <p>Enquanto isso, você pode:</p>
        <ul style='text-align: left; display: inline-block;'>
            <li>Cadastrar novas vagas</li>
            <li>Visualizar oportunidades disponíveis</li>
            <li>Utilizar a IA para analisar um curriulo seu</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("📅 Previsão de lançamento: Versão 2.0")