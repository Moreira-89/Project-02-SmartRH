import os
import firebase_admin
from firebase_admin import credentials, db, storage
from dotenv import load_dotenv

class FirebaseConfig:
    _instance = None
    def __init__(self):
        load_dotenv()
        if not firebase_admin._apps:
            self._initialize_firebase()

    def _initialize_firebase(self):
        """Configuração para Realtime Database"""
        try:
            cred_dict = {
                "type": "service_account",
                "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
                "private_key": os.environ.get("FIREBASE_DATABASE_SECRET", "").replace('\\n', '\n'),
                "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
                "token_uri": "https://oauth2.googleapis.com/token"
            }
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(
                cred,
                {
                    'databaseURL': os.environ.get("FIREBASE_DATABASE_URL"),
                    'storageBucket': os.environ.get("FIREBASE_STORAGE_BUCKET")
                }
            )
        except Exception as e:
            print(f"Erro ao inicializar o Firebase: {e}")
            raise

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