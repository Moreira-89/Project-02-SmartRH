import reflex as rx

from Project_02_SmartRH.pages.add_job import add_job_page
from Project_02_SmartRH.pages.show_jobs_page import show_jobs_page
from Project_02_SmartRH.state.listjob_state import ListJobsState


app = rx.App()
app.add_page(add_job_page, route="/nova-vaga")
app.add_page(show_jobs_page, route="/vagas", on_load=ListJobsState.buscar_vagas)