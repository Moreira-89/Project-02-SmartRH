import reflex as rx
from Project_02_SmartRH.state.job_state import JobFormState


def add_job_page():
    return rx.vstack(
        rx.heading("Adicionar Nova Vaga"),
        rx.input(
            placeholder="Digite o titulo da vaga",
            value=JobFormState.title,
            on_change=JobFormState.set_title #type: ignore
        ),
        rx.button("Cadastrar Vaga", 
                  on_click=JobFormState.salvar_vaga #   type: ignore
                  )
    )
