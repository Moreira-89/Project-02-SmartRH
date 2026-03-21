import reflex as rx
from Project_02_SmartRH.services.firebase_service import FirebaseService
from Project_02_SmartRH.models.analysis import Analysis


class HistoricoState(rx.State):
    historico_analises: list[Analysis] = []
    on_modal: bool = False
    analise_selecionada: Analysis | None = None

    def buscar_historico(self):
        analises = FirebaseService().get_analyses() #type: ignore

        jobs = FirebaseService().get_jobs() #type: ignore

        mapa_vagas = {job.id: job.title for job in jobs}

        for analise in analises:
            
            titulo_encontrado = mapa_vagas.get(analise.job_id)
            if titulo_encontrado:
                analise.job_title = titulo_encontrado

        self.historico_analises = analises

    def abrir_modal(self, analise: Analysis):
        self.on_modal = True
        self.analise_selecionada = analise

    def fechar_modal(self):
        self.on_modal = False
        self.analise_selecionada = None
