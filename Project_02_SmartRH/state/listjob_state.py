import reflex as rx
from models.job import Job
from services.firebase_service import FirebaseService


class ListJobsState(rx.State):
    vagas: list[Job] = []


    def buscar_vagas(self):
        self.vagas = FirebaseService().get_jobs()