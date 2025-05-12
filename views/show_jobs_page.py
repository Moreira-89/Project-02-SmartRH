from services.firebase_service import FirebaseService
import streamlit as st
import re

def show_jobs_page():
    try:
        service = FirebaseService()
        vagas = service.get_jobs()

        # Cabeçalho da página
        st.title("\U0001f4cb Vagas Disponíveis")
        
        # Botão voltar para home
        if st.button("\u2190 Voltar para Home"):
            st.session_state.current_page = "home"
            st.rerun()
            
        st.markdown("""
        **\U0001f50d Descrição:**  
        Aqui você visualiza todas as vagas cadastradas no sistema.  
                    
        \U0001f4ca *Cada vaga mostra os requisitos e diferenciais para ajudar na análise dos candidatos.*
        """)
        
        # Verifica se existem vagas cadastradas
        if not vagas:
            st.warning("Nenhuma vaga cadastrada", icon="\u26A0\ufe0f")
            
            if st.button("\u2795 Cadastrar Nova Vaga", type="primary"):
                st.session_state.current_page = "add_job"
                st.rerun()
            
            return

        # Adicionando filtros e opções de exibição
        with st.expander("\U0001f50d Filtros e Opções", expanded=True):
            col1, col2= st.columns([2, 2])
            
            with col1:
                # Campo de busca por palavra-chave
                search_term = st.text_input(
                    "Buscar por palavra-chave:",
                    placeholder="Ex: python, aws, react...",
                    help="Busca nos títulos e requisitos das vagas"
                )
            
            with col2:
                # Ordenação
                sort_option = st.selectbox(
                    "Ordenar por:",
                    options=["Recentes", "Título (A-Z)", "Título (Z-A)"],
                    index=0
                )

        # Ordenar vagas conforme selecionado
        if sort_option == "Título (A-Z)":
            vagas = sorted(vagas, key=lambda x: x.title)
        elif sort_option == "Título (Z-A)":
            vagas = sorted(vagas, key=lambda x: x.title, reverse=True)

        total_vagas = len(vagas)
        vagas_filtradas = 0
        
        # Filtrar vagas conforme o termo de busca
        filtered_vagas = []
        for vaga in vagas:
            if search_term and search_term.strip():
                search_term = search_term.lower()
                title_match = search_term in vaga.title.lower() if vaga.title else False
                req_match = search_term in vaga.prerequisites.lower() if vaga.prerequisites else False
                act_match = search_term in vaga.main_activity.lower() if vaga.main_activity else False
                
                if not (title_match or req_match or act_match):
                    continue
            
            filtered_vagas.append(vaga)
            vagas_filtradas += 1
        
        # Exibir estatísticas de filtragem
        if search_term and search_term.strip():
            st.caption(f"Exibindo {vagas_filtradas} de {total_vagas} vagas")
            
        # Criar grid de cards (2 colunas)
        cols = st.columns(2)
        
        # Distribuir vagas em 2 colunas
        for i, vaga in enumerate(filtered_vagas):
            col_index = i % 2  # Alternar entre coluna 0 e 1
            
            with cols[col_index]:
                # Criar card da vaga com estilo melhorado
                with st.container():
                    # Usar cor de fundo para destacar o card
                    st.markdown("---")
                    
                    # Título da vaga com ícone
                    st.subheader(f"\U0001f4dd {vaga.title}")
                    
                    # Botão para analisar CV
                    if st.button("\U0001f4dd Analisar CV", key=f"analyze_{vaga.id}"):
                        st.session_state.selected_job = vaga
                        st.session_state.current_page = "analysis_job"
                        st.rerun()
                    
                    # Mostrar detalhes diretamente, sem precisar expandir
                    # Exibir detalhes da vaga usando tabs
                    tab1, tab2, tab3 = st.tabs(["\U0001f4cb Descrição", "\U0001f3af Requisitos", "\u2728 Diferenciais"])
                    
                    with tab1:
                        st.markdown("#### Atividades Principais")
                        st.write(vaga.main_activity)
                    
                    with tab2:
                        st.markdown("#### Requisitos")
                        st.write(vaga.prerequisites)
                    
                    with tab3:
                        st.markdown("#### Diferenciais")
                        if vaga.differentials:
                            st.write(vaga.differentials)
                        else:
                            st.info("Nenhum diferencial especificado")
        
        # Botão para cadastrar nova vaga no final da página
        st.markdown("---")
        col1, col2= st.columns([1,2])
        with col1:
            st.button("\u2795 Cadastrar Nova Vaga", type="primary", on_click=lambda: setattr(st.session_state, 'current_page', 'add_job'))

    except Exception as e:
        st.error(f"Erro ao carregar: {str(e)}")
        st.button("Recarregar", on_click=st.rerun)