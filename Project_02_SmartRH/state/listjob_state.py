import reflex as rx
from Project_02_SmartRH.models.job import Job
from Project_02_SmartRH.services.firebase_service import FirebaseService


class ListJobsState(rx.State):
    vagas: list[Job] = []
    vaga_selecionada_id: str = ""

    def buscar_vagas(self):
        self.vagas = FirebaseService().get_jobs()

    def analisar_vaga_selecionada(self, vaga_id: str):
        self.vaga_selecionada_id = vaga_id
        return rx.redirect("/analisar-curriculo")