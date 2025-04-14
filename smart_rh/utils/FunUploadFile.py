from firebase.FirebaseAPI import FirebaseAPI
from datetime import datetime
import streamlit as st
import uuid

firebase_config = st.secrets["FIREBASE"]

@st.dialog("Upload de Currículos")
def FunUploadFile():

    firebase = FirebaseAPI(
        database_url=firebase_config["DATABASE_URL"],
        secret_key=firebase_config["DATABASE_SECRET"],
    )

    uploaded_files = st.file_uploader(
        "Selecione os currículos (PDF ou DOCX)",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if uploaded_files:
        vagas = firebase.get_document("vagas") or {}
        
        if not vagas:
            st.warning("Nenhuma vaga cadastrada! Cadastre vagas primeiro.")
            return
            
        opcoes_vagas = list(vagas.keys())
        
        vaga_id = st.selectbox(
            "Selecione a vaga relacionada",
            options=opcoes_vagas,
            format_func=lambda x: f"{x} - {vagas[x].get('title', 'Sem título')}"
        )

        if st.button("Processar Currículos"):
            with st.status("Enviando arquivos...", expanded=True) as status:
                for i, file in enumerate(uploaded_files):
                    try:
                        # Gera um ID único para o currículo
                        curriculo_id = f"cur_{uuid.uuid4().hex[:8]}"
                        
                        # Nome do arquivo no storage
                        file_path = f"curriculos/{datetime.now().strftime('%Y-%m-%d')}/{curriculo_id}_{file.name}"
                        
                        # Upload para Firebase Storage
                        file_url = firebase.upload_file(
                            file=file,
                            path=file_path,
                            content_type=file.type
                        )
                        
                        # Salva metadados no Realtime Database
                        firebase.create_document("curriculos", curriculo_id, {
                            "vaga_id": vaga_id,
                            "vaga_titulo": vagas[vaga_id].get("title", ""),
                            "candidato_nome": file.name.split('.')[0],
                            "arquivo_url": file_url,
                            "formato": file.type,
                            "tamanho": f"{len(file.getvalue()) / 1024:.2f} KB",
                            "data_upload": datetime.now().isoformat(),
                            "status": "pendente"
                        })
                        
                        st.write(f"✅ {i+1}/{len(uploaded_files)}: {file.name} (ID: {curriculo_id})")
                        st.progress((i + 1) / len(uploaded_files))
                    
                    except Exception as e:
                        st.error(f"❌ Erro no arquivo {file.name}: {str(e)}")
                
                status.update(label=f"✅ Upload completo! {len(uploaded_files)} arquivos processados", state="complete")

