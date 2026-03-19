import reflex as rx

from Project_02_SmartRH.pages.add_job import add_job_page
from Project_02_SmartRH.pages.show_jobs_page import show_jobs_page
from Project_02_SmartRH.state.listjob_state import ListJobsState
from Project_02_SmartRH.pages.analisar_curriculo import analise_page
from Project_02_SmartRH.state.analise_state import AnaliseState


app = rx.App()
app.add_page(add_job_page, route="/nova-vaga")
app.add_page(show_jobs_page, route="/listar-vagas", on_load=ListJobsState.buscar_vagas)#type: ignore
app.add_page(analise_page, route="/analisar-curriculo", on_load=AnaliseState.carregar_vaga) #type: ignore