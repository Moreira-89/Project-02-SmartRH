from services.firebase_service import FirebaseService
from datetime import datetime
from models.job import Job
import streamlit as st
import uuid
import re

def show_job_form():

    if st.button("← Voltar para Home"):
        st.session_state.current_page = "home"
        st.rerun()

    st.markdown("### \U00002795 Cadastrar Nova Vaga")
    st.markdown("""
    **\U0001f4d6 Descrição:**  
    Nesta página você pode cadastrar novas oportunidades de trabalho no sistema Smart RH.
                
    **Benefícios:**
                
    - Análise automática de currículos para esta vaga
    - Cálculo de compatibilidade por IA
    - Organização centralizada das oportunidades

                     
    **Dicas para um bom cadastro:**
    - Seja específico nos requisitos técnicos
    - Detalhe as atividades diárias do cargo
    - Liste diferenciais que possam destacar candidatos
                
    \U0001f4a1 *Após cadastrar uma vaga, nossa IA vai poder analisar o curriculo que você fez upload em **Análise com IA** e verificar se a vaga que escolheu tem algum matche com seu curriculo!*
    """)

    if 'job_form_submitted' not in st.session_state:
        st.session_state.job_form_submitted = False
    if 'job_form_error' not in st.session_state:
        st.session_state.job_form_error = None
    if 'job_id' not in st.session_state:
        st.session_state.job_id = ""
    
    if st.session_state.job_form_submitted:
        st.success("\u2705 Vaga cadastrada com sucesso!")
        
        if st.button("\U0001F504 Cadastrar Nova Vaga"):
            st.session_state.job_form_submitted = False
            st.session_state.job_form_error = None
            st.session_state.job_id = ""
            st.rerun()
            
        if st.button("\U0001F441\ufe0f Ver Vagas Cadastradas"):
            st.session_state.current_page = "view_jobs"
            st.rerun()
            
        return
    
    with st.form("job_form", clear_on_submit=False):
        st.markdown("### Informações da Vaga:")

        def validate_job_id(id_text):
            if not id_text:
                return False, "ID da vaga é obrigatório"
            if not re.match(r'^[a-z0-9_]+$', id_text):
                return False, "ID deve conter apenas letras minúsculas, números e underscore"
            return True, ""

        default_id = f"job_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        job_id_help = "Identificador único da vaga (somente letras minúsculas, números e underscore)"

        col1, col2 = st.columns([3, 1])
        with col1:
            job_id = st.text_input(
                "ID da Vaga*", 
                value=st.session_state.job_id or default_id,
                help=job_id_help,
                placeholder="Ex: dev_backend_sr_2025"
            )
            
            if job_id:
                valid_id, id_message = validate_job_id(job_id)
                if not valid_id:
                    st.warning(id_message)
                st.session_state.job_id = job_id

        with col2:

            generate_id = st.form_submit_button("\U0001F3B2 Gerar ID", type="secondary")
            if generate_id:
                random_id = f"job_{uuid.uuid4().hex[:8]}"
                st.session_state.job_id = random_id
                st.rerun()
        
        title = st.text_input(
            "Título da Vaga*", 
            placeholder="Ex: Desenvolvedor Full Stack Senior",
            help="Título que aparecerá na listagem de vagas"
        )
        
        tabs = st.tabs(["\U0001F4DD Descrição", "\U0001F3AF Requisitos", "\u2b50 Diferenciais", "\U0001F4CA Detalhes"])

        with tabs[0]:
            st.markdown("### Descrição e Atividades")
            main_activity = st.text_area(
                "Atividades Principais*",
                placeholder=(
                    "Descreva as principais atividades e responsabilidades...\n\n"
                    "Exemplo:\n"
                    "- Desenvolvimento de APIs RESTful\n"
                    "- Manutenção de aplicações existentes\n"
                    "- Participação em planning e refinamentos"
                ),
                height=200
            )

        with tabs[1]:
            st.markdown("### Requisitos da Vaga")
            prerequisites = st.text_area(
                "Pré-Requisitos*",
                placeholder=(
                    "Liste os requisitos técnicos e comportamentais...\n\n"
                    "Exemplo:\n"
                    "- 5+ anos de experiência com Python\n"
                    "- Conhecimento em AWS\n"
                    "- Experiência com metodologias ágeis"
                ),
                height=200
            )
            
        with tabs[2]:
            st.markdown("### Diferenciais da Vaga")
            differentials = st.text_area(
                "Diferenciais",
                placeholder=(
                    "Liste os diferenciais que serão valorizados...\n\n"
                    "Exemplo:\n"
                    "- Experiência em projetos de grande escala\n"
                    "- Conhecimento em Docker e Kubernetes\n"
                    "- Certificações relevantes"
                ),
                height=150
            )
        
        with tabs[3]:
            st.markdown("### Detalhes Adicionais")
            
            col1, col2 = st.columns(2)
            
            with col1:
                status = st.selectbox(
                    "Status da Vaga",
                    options=["active", "draft", "closed"],
                    format_func=lambda x: {
                        "active": "\U0001F7E2 Ativa",
                        "draft": "\U0001F7E0 Rascunho",
                        "closed": "\U0001F534 Encerrada"
                    }.get(x),
                    index=0
                )
            
            with col2:
                st.selectbox(
                    "Nível de Senioridade",
                    options=["Jovem Aprendiz", "Estagiário", "Júnior", "Pleno", "Sênior", "Especialista", "Não especificado"],
                    index=4,
                    help="Será utilizado em futuras atualizações"
                )

        submit_button = st.form_submit_button(
            "\U0001F4BE Cadastrar Vaga", 
            type="primary",
            use_container_width=True
        )

        if submit_button:

            if not all([job_id, title, main_activity, prerequisites]):
                st.error("\u26a0\ufe0f Preencha todos os campos obrigatórios (*)")
                return
            
            valid_id, id_message = validate_job_id(job_id)
            if not valid_id:
                st.error(f"\u26a0\ufe0f {id_message}")
                return

            try:
                nova_vaga = Job(
                    id=job_id,
                    title=title,
                    main_activity=main_activity,
                    prerequisites=prerequisites,
                    differentials=differentials if differentials else None,
                )

                FirebaseService().create_job(job=nova_vaga)

                st.session_state.job_form_submitted = True
                st.rerun()
                
            except Exception as e:
                st.error(f"\u274c Erro ao cadastrar a vaga: {str(e)}")

    with st.expander("\U0001F4A1 Dicas para Recrutamento Eficiente", expanded=False):
        st.markdown("""
        ### Como Criar uma Descrição de Vaga Atraente
        
        1. **Seja específico**: Descreva exatamente o que a posição envolve
        2. **Linguagem inclusiva**: Use termos neutros e evite estereótipos
        3. **Foque em resultados**: Explique o impacto do trabalho
        4. **Diferencie requisitos obrigatórios de desejáveis**: Seja claro sobre o que é essencial
        5. **Destaque a cultura**: Mostre como é trabalhar na empresa
        
        Uma boa descrição de vaga **aumenta em 50%** as chances de atrair o candidato ideal!
        """)
