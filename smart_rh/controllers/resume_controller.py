from services.firebase_service import FirebaseService
from models.resume import Resume
from typing import List
import uuid
import re
from datetime import datetime

class ResumeController:
    def __init__(self):
        self.service = FirebaseService()

    def process_upload(
        self, 
        file, 
        vaga_id: str, 
        vaga_title: str
    ) -> Resume:
        """Processa o upload de um currículo e salva os metadados"""
        try:
            if not file or not vaga_id:
                raise ValueError("Dados incompletos para upload")

            resume_id = f"cur_{uuid.uuid4().hex[:8]}"

            candidate_name = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', file.name.split('.')[0]).strip()

            resume_data = {
                "id": resume_id,
                "job_id": vaga_id,
                "candidate_name": candidate_name or "Não identificado",
                "file_url": None,
                "file_type": file.type,
                "file_size": f"{len(file.getvalue()) / (1024 * 1024):.2f} MB",
                "upload_date": datetime.now(),
                "status": "pendente",
                "vaga_titulo": vaga_title
            }

            resume = Resume(**resume_data)

            resume.file_url = self.service.upload_resume(file, resume)

            self.service.create_resume_record(resume)

            return resume

        except Exception as e:
            raise RuntimeError(f"Falha no processamento do currículo: {str(e)}")

    def get_resumes_by_job(self, job_id: str) -> List[Resume]:
        """Busca currículos associados a uma vaga"""
        try:
            return self.service.get_resumes(job_id)
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar currículos: {str(e)}")