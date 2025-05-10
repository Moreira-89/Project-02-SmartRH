from config.firebase_config import FirebaseConfig
from models.job import Job
from models.resume import Resume
from typing import List, Optional, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FirebaseService:
    def __init__(self):
        self.config = FirebaseConfig.get_instance()
        self.rtdb = self.config.rtdb
        self.bucket = self.config.bucket

    def create_job(self, job: Job) -> dict:
        try:
            self.rtdb.child(f"vagas/{job.id}").set(job.dict())
            logger.info(f"Vaga {job.id} criada")
            return {"status": "success", "id": job.id}
        except Exception as e:
            logger.error(f"Erro ao criar vaga: {str(e)}")
            raise

    def get_jobs(self) -> list[Job]:
        try:
            jobs = self.rtdb.child("vagas").get()
            return [Job(**job) for job in jobs.values()] if jobs else []
        except Exception as e:
            logger.error(f"Erro ao buscar vagas: {str(e)}")
            return []

    def upload_resume(self, file, resume: Resume) -> str:
        """Faz upload do arquivo para o Storage"""
        try:
            blob = self.bucket.blob(f"curriculos/{resume.id}/{file.name}")
            blob.upload_from_string(
                file.getvalue(),
                content_type=file.type,
                timeout=300
            )
            blob.make_public()
            logger.info(f"Arquivo {file.name} enviado")
            return blob.public_url
        except Exception as e:
            logger.error(f"Erro no upload: {str(e)}")
            raise

    def create_resume_record(self, resume: Resume) -> None:
        """Salva metadados no Realtime Database"""
        try:
            self.rtdb.child(f"curriculos/{resume.id}").set(resume.dict())
            logger.info(f"Metadados salvos: {resume.id}")
        except Exception as e:
            logger.error(f"Erro ao salvar metadados: {str(e)}")
            raise

    def get_resumes_by_job(self, job_id: str) -> List[Resume]:
        """Lista currículos de uma vaga"""
        try:
            resumes = self.rtdb.child("curriculos").order_by_child("job_id").equal_to(job_id).get()
            return [Resume(**resume) for resume in resumes.values()] if resumes else []
        except Exception as e:
            logger.error(f"Erro ao buscar currículos: {str(e)}")
            return []