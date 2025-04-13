import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
import logging

logging.basicConfig(level=logging.INFO)

if os.getenv("IS_STREAMLIT_CLOUD"):

    import streamlit as st
    cred_info = st.secrets["FIREBASE"]
    cred = credentials.Certificate(cred_info)
    logging.info("Usando chave de serviço do Streamlit Cloud")

else:
    cred = credentials.Certificate("smart_rh/serviceAccountKey.json")
    logging.info("Usando chave de serviço do arquivo local")


if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'smartrh-2025.appspot.com'
    })

db = firestore.client()
bucket = storage.bucket()
