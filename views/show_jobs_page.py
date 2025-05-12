from services.firebase_service import FirebaseService
import streamlit as st

def show_jobs_page():
    try:
        service = FirebaseService()
        vagas = service.get_jobs()

        if st.button("← Voltar para Home"):
            st.session_state.current_page = "home"
            st.rerun()

        st.markdown("### \U0001f4cb Vagas Disponíveis")
        st.markdown("""
        **\U0001f50d Descrição:**  
        Aqui você visualiza todas as vagas cadastradas no sistema.  
                    
        \U0001f4ca *Cada vaga mostra os requisitos e diferenciais para ajudar na análise dos candidatos.*
        """)

        if not vagas:
            st.warning("Nenhuma vaga cadastrada", icon="⚠️")
            return

        # Mostra uma vaga por vez em seções expansíveis
        for vaga in vagas:
            with st.expander(f"\U0001f539 {vaga.title}", expanded=False):
                st.markdown("**Atividades:**")
                st.write(vaga.main_activity)
                
                st.markdown("**Requisitos:**")
                st.write(vaga.prerequisites)
                
                if vaga.differentials:
                    st.markdown("**Diferenciais:**")
                    st.write(vaga.differentials)
                
                st.divider()

    except Exception as e:
        st.error(f"Erro ao carregar: {str(e)}")
        st.button("Recarregar", on_click=st.rerun)