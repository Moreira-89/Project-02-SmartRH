from services.firebase_service import FirebaseService
from models.job import Job

class JobController:
    def __init__(self):
        self.service = FirebaseService()

    def create_job(self, job_data: dict) -> Job:
        job = Job(**job_data)
        return self.service.create_job(job)

    def get_all_jobs(self) -> list[Job]:
        return self.service.get_jobs()