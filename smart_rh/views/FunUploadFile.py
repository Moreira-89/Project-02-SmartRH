from services.firebase_service import FirebaseService
from datetime import datetime
import streamlit as st
import uuid
import re

firebase_config = st.secrets["FIREBASE"]

@st.dialog("📤 Upload de Currículos")
def FunUploadFile():
  
    MAX_SIZE_MB = 5

    # Inicializa o Firebase
    firebase = FirebaseService(
        database_url=firebase_config["DATABASE_URL"],
        secret_key=firebase_config["DATABASE_SECRET"],
    )

    # Widget de upload
    uploaded_files = st.file_uploader(
        "Selecione os currículos (PDF ou DOCX)",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        help="Máximo 5MB por arquivo"
    )

    if uploaded_files:
        vagas = firebase.get_document("vagas") or {}
        
        if not vagas:
            st.warning("⚠️ Nenhuma vaga cadastrada! Cadastre vagas primeiro.")
            return
            
        # Seleção de vaga
        vaga_id = st.selectbox(
            "Selecione a vaga relacionada",
            options=list(vagas.keys()),
            format_func=lambda x: f"{x} - {vagas[x].get('title', 'Sem título')}",
            key="vaga_selector"
        )

        if st.button("⏳ Processar Currículos", type="primary"):
            with st.status("📤 Enviando arquivos...", expanded=True) as status:
                success_count = 0
                
                for i, file in enumerate(uploaded_files):
                    try:
                        # Validação do tamanho
                        file_size_mb = len(file.getvalue()) / (1024 * 1024)
                        if file_size_mb > MAX_SIZE_MB:
                            st.warning(f"❌ {file.name} ({file_size_mb:.2f}MB) excede o limite de {MAX_SIZE_MB}MB")
                            continue

                        # Prepara os dados
                        curriculo_id = f"cur_{uuid.uuid4().hex[:8]}"
                        candidato_nome = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', file.name.split('.')[0]).strip()
                        file_path = f"curriculos/{datetime.now().strftime('%Y-%m-%d')}/{curriculo_id}_{file.name}"
                        
                        # Faz upload
                        file_url = firebase.upload_file(
                            file=file,
                            path=file_path,
                            content_type=file.type
                        )
                        
                        # Salva metadados
                        firebase.create_document("curriculos", curriculo_id, {
                            "vaga_id": vaga_id,
                            "vaga_titulo": vagas[vaga_id].get("title", ""),
                            "candidato_nome": candidato_nome or "Não identificado",
                            "arquivo_url": file_url,
                            "formato": file.type,
                            "tamanho": f"{file_size_mb:.2f} MB",
                            "data_upload": datetime.now().isoformat(),
                            "status": "pendente"
                        })
                        
                        st.success(f"✅ {i+1}. {file.name}")
                        success_count += 1
                    
                    except Exception as e:
                        st.error(f"❌ Falha no arquivo {file.name}: {str(e)}")
                
                status.update(
                    label=f"✅ Concluído! {success_count}/{len(uploaded_files)} arquivos processados",
                    state="complete" if success_count > 0 else "error"
                )
                
                if success_count > 0:
                    st.balloons()