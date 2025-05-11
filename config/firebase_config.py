import firebase_admin
from firebase_admin import credentials, db, storage
import streamlit as st

class FirebaseConfig:
    _instance = None

    def __init__(self):
        if not firebase_admin._apps:
            self._initialize_firebase()

    def _initialize_firebase(self):
        """Configuração para Realtime Database"""
        try:
            cred_dict = {
                "type": "service_account",
                "project_id": st.secrets["FIREBASE"]["PROJECT_ID"],
                "private_key": st.secrets["FIREBASE"]["DATABASE_SECRET"].replace('\\n', '\n'),
                "client_email": st.secrets["FIREBASE"]["CLIENT_EMAIL"],
                "token_uri": "https://oauth2.googleapis.com/token"
            }
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(
                cred,
                {
                    'databaseURL': st.secrets["FIREBASE"]["DATABASE_URL"],
                    'storageBucket': st.secrets["FIREBASE"]["STORAGE_BUCKET"]
                }
            )
        except Exception as e:
            raise RuntimeError(f"Erro no Firebase: {str(e)}")

    @property
    def rtdb(self):
        """Retorna a referência do Realtime Database"""
        return db.reference()

    @property
    def bucket(self):
        return storage.bucket()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = FirebaseConfig()
        return cls._instance