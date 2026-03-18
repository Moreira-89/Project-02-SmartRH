import reflex as rx
from Project_02_SmartRH.state.listjob_state import ListJobsState

def desenhar_vaga(vaga):
    return rx.vstack(
        rx.heading(vaga.title),
        rx.text(vaga.main_activity),
        rx.text(vaga.prerequisites)
    )

def show_jobs_page():
    return rx.vstack(
        rx.text("Vagas Disponíveis"),
        rx.foreach(
            ListJobsState.vagas,
            desenhar_vaga
        )
    )