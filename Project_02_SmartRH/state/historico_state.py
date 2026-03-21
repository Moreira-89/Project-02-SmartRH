import reflex as rx
from Project_02_SmartRH.services.firebase_service import FirebaseService
from Project_02_SmartRH.models.analysis import Analysis


class HistoricoState(rx.State):
    historico_analises: list[Analysis] = []


    def buscar_historico(self):
        self.historico_analises = FirebaseService().get_analyses() #type: ignore