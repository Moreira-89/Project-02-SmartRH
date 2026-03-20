import reflex as rx
from Project_02_SmartRH.state.listjob_state import ListJobsState
from Project_02_SmartRH.components.layout import base_layout 

def  desenhar_vaga(vaga):
    return rx.card(
        rx.vstack(
            rx.heading(vaga.title),
            rx.text("Principais Atividades:", font_weight="bold"),
            rx.markdown(vaga.main_activity),
            rx.text("Pré-requisitos:", font_weight="bold"),
            rx.markdown(vaga.prerequisites),
            rx.button("Analisar CV", on_click=lambda: ListJobsState.analisar_vaga_selecionada(vaga.id)), #type: ignore
            align_items="start",
            spacing="3"
        ),
        width="100%",
        margin_bottom="1em"
    )


def show_jobs_page():
    conteudo = rx.vstack(
        rx.heading("Vagas Disponíveis"),
        rx.foreach(
            ListJobsState.vagas,
            desenhar_vaga
        ),
        width="100%",
        max_width="800px",
        margin="auto"
    )
    return base_layout(conteudo)