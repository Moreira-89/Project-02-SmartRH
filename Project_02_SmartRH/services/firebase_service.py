from Project_02_SmartRH.config.firebase_config import FirebaseConfig
from Project_02_SmartRH.models.job import Job
from Project_02_SmartRH.models.resume import Resume
from Project_02_SmartRH.models.analysis import Analysis
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
            return [Job(**dict(job)) for job in jobs.values()] if jobs else [] #type: ignore
        except Exception as e:
            logger.error(f"Erro ao buscar vagas: {str(e)}")
            return []
        
    def get_job(self, job_id: str) -> Job | None:
        try:
            job = self.rtdb.child(f"vagas/{job_id}").get()
            return Job(**dict(job)) if job else None
        except Exception as e:
            logger.error(f"Erro ao buscar vaga: {str(e)}")
            return None
        
    def get_analyses(self) -> list[Analysis]:
        try:
            analyses = self.rtdb.child("analises").get()
            return [Analysis(**dict(analysis)) for analysis in analyses.values()] if analyses else [] #type: ignore
        except Exception as e:
            logger.error(f"Erro ao buscar análises: {str(e)}")
            return []


    def upload_resume_file(self, file, resume_id: str) -> str:
        """Faz upload do arquivo para o Storage e retorna a URL"""
        try:
            file_extension = file.name.split('.')[-1]
            file_path = f"curriculos/{resume_id}/curriculo.{file_extension}"
            
            blob = self.bucket.blob(file_path)
            blob.upload_from_string(
                file.getvalue(),
                content_type=file.type,
                timeout=300
            )
            blob.make_public()
            return blob.public_url
        except Exception as e:
            logger.error(f"Erro no upload: {str(e)}")
            raise

    def create_resume(self, resume: Resume) -> dict:
        """Salva os metadados do currículo"""
        try:
            self.rtdb.child(f"curriculos/{resume.id}").set(resume.dict())
            return {"status": "success", "id": resume.id}
        except Exception as e:
            logger.error(f"Erro ao salvar currículo: {str(e)}")
            raise

    def create_analysis(self, analysis: Analysis) -> dict:
        try:
            analysis_data = analysis.dict()
            self.rtdb.child(f"analises/{analysis.id}").set(analysis_data)
            logger.info(f"Dados salvos: {str(analysis_data)[:200]}...")
            return {"status": "success", "id": analysis.id}
        except Exception as e:
            logger.error(f"Erro completo ao salvar: {str(e)}")
            raise