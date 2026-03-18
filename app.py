# from views.show_jobs_page import show_jobs_page
# from views.show_job_form import show_job_form
# from views.show_job_upload_file import show_job_upload_file
# from views.analysis_ia_page import show_analysis_page
# from services.firebase_service import FirebaseService
# import streamlit as st


# st.set_page_config(
#     page_title="Smart RH",
#     page_icon="\U0001f4bc",
#     layout="wide"
# )

# if 'current_page' not in st.session_state:
#     st.session_state.current_page = "home"

# def change_page(page_name):
#     st.session_state.current_page = page_name
#     st.rerun()

# # Verifica a página atual antes de qualquer outra coisa
# if st.session_state.current_page == "view_jobs":
#     show_jobs_page()

# elif st.session_state.current_page == "add_job":
#     show_job_form()

# elif st.session_state.current_page == "upload_resumes":
#     show_job_upload_file()

# elif st.session_state.current_page == "analysis_job":
#     show_analysis_page()

# else:  # Página inicial (home)
        
#     st.markdown("""
    
#     ## Bem-vindo ao Smart RH!
                
#     **Smart RH** é um sistema inteligente de recrutamento que conecta candidatos às melhores oportunidades usando IA.
    
#     **Principais Funcionalidades:**
#     - 📋 Cadastro de vagas detalhadas
#     - 🧠 Análise de compatibilidade curricular com IA
#     - 📊 Visualização das vagas
#     - 📩 Upload e gerenciamento de currículos (em breve)
#     """)
    
#     try:
#         firebase = FirebaseService()
#         vagas = firebase.get_jobs()
#         total_vagas = len(vagas) if vagas else 0
        
#         # Estatísticas principais
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.metric(
#                 label="\U0001F4CA Vagas Ativas",
#                 value=total_vagas,
#                 delta=None
#             )
            
#         with col2:
#             # Mostra o número de vagas com alta demanda (exemplo)
#             st.metric(
#                 label="\U0001F525 Vagas Prioritárias",
#                 value=f"{total_vagas//3 if total_vagas > 0 else 0}",
#                 delta=None
#             )
        
#         # Ações rápidas
#         st.markdown("#### \u26A1 Ações Rápidas")
#         col1, col2 = st.columns(2)

#         with col1:
#             if st.button("\u2795 Nova Vaga", use_container_width=True):
#                 st.session_state.current_page = "add_job"
#                 st.rerun()
                
#             if st.button("\U0001F50D Análise com IA", use_container_width=True, type="primary"):
#                 st.session_state.current_page = "analysis_job"
#                 st.rerun()
        
#         with col2:
#             if st.button("\U0001F50D Ver Vagas", use_container_width=True):
#                 st.session_state.current_page = "view_jobs"
#                 st.rerun()
                
#             if st.button("\U0001F4E9 Upload de CV", use_container_width=True):
#                 st.session_state.current_page = "upload_resumes"
#                 st.rerun()

#         # Vagas Recentes
#         if vagas:
#             st.markdown("#### \U0001F552 Vagas Recentes")
#             # Mostrar as 3 primeiras vagas (assumindo que as mais recentes estão primeiro)
#             for vaga in vagas[:3]:
#                 with st.container():
#                     col1, col2 = st.columns([3, 1])
#                     with col1:
#                         # Tentar obter o título de diferentes maneiras
#                         title = "Vaga"  # valor padrão
#                         try:
#                             if hasattr(vaga, 'title'):
#                                 title = vaga.title
#                             elif isinstance(vaga, dict) and 'title' in vaga:
#                                 title = vaga['title']
#                             elif isinstance(vaga, tuple) and len(vaga) > 1:
#                                 # Assumindo que o segundo elemento é o título (ajuste conforme necessário)
#                                 title = vaga[1]
#                         except:
#                             pass
                        
#                         st.markdown(f"**{title}**")
                    
#                     with col2:
#                         # Tentar obter o ID de diferentes maneiras
#                         vaga_id = "job_id"  # valor padrão
#                         try:
#                             if hasattr(vaga, 'id'):
#                                 vaga_id = vaga.id
#                             elif isinstance(vaga, dict) and 'id' in vaga:
#                                 vaga_id = vaga['id']
#                             elif isinstance(vaga, tuple) and len(vaga) > 0:
#                                 # Assumindo que o primeiro elemento é o ID (ajuste conforme necessário)
#                                 vaga_id = vaga[0]
#                         except:
#                             pass
                            
#                         if st.button("Ver Detalhes", key=f"recent_{vaga_id}"):
#                             st.session_state.job_to_view = vaga_id
#                             st.session_state.current_page = "view_jobs"
#                             st.rerun()
#                     st.markdown("---")
#         else:
#             st.info("Nenhuma vaga cadastrada ainda. Crie sua primeira vaga!")
            
#     except Exception as e:
#         st.error(f"Erro ao carregar dashboard: {str(e)}")
#         if st.button("Recarregar"):
#             st.rerun()

#     st.markdown("""
#     *Versão 1.0 © 2025 Smart RH*
#     """)