import reflex as rx
import re
from Project_02_SmartRH.models.job import Job
from Project_02_SmartRH.services.firebase_service import FirebaseService


class ListJobsState(rx.State):
    vagas: list[Job] = []
    vaga_selecionada_id: str = ""
    search_term: str = ""
    status_filter: str = "Todas"

    def buscar_vagas(self):
        vagas = FirebaseService().get_jobs()
        for vaga in vagas:
            if not vaga.requirements_count:
                itens = [
                    item.strip()
                    for item in re.split(r"[\n,;]+", vaga.prerequisites)
                    if item.strip()
                ]
                vaga.requirements_count = len(itens)
        self.vagas = vagas

    def set_search_term(self, valor: str):
        self.search_term = valor

    def set_status_filter(self, valor: str):
        self.status_filter = valor

    def analisar_vaga_selecionada(self, vaga_id: str):
        self.vaga_selecionada_id = vaga_id
        return rx.redirect("/analisar-curriculo")

    @rx.var
    def vagas_filtradas(self) -> list[Job]:
        termo = self.search_term.strip().lower()
        vagas_filtradas = self.vagas

        if termo:
            vagas_filtradas = [
                vaga
                for vaga in vagas_filtradas
                if termo in vaga.title.lower()
                or termo in vaga.main_activity.lower()
                or termo in vaga.prerequisites.lower()
            ]

        if self.status_filter == "Ativas":
            vagas_filtradas = [vaga for vaga in vagas_filtradas if vaga.status == "active"]

        return vagas_filtradas
    
    @rx.var
    def lista_opcoes_vagas(self) -> list[str]:
        return [vaga.title for vaga in self.vagas]
