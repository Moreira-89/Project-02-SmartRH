import reflex as rx
from Project_02_SmartRH.state.listjob_state import ListJobsState
from Project_02_SmartRH.components.layout import base_layout


def desenhar_vaga(vaga) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(vaga.title, size="6", color="#f8fafc"),
                rx.badge("Ativa", color_scheme="green", variant="soft"),
                width="100%",
                justify="between",
                align="center",
            ),
            rx.vstack(
                rx.text("Atividades principais", font_weight="600", color="#e2e8f0"),
                rx.markdown(vaga.main_activity, style={"color": "#cbd5e1"}),
                spacing="1",
                align_items="start",
                width="100%",
            ),
            rx.vstack(
                rx.text("Pré-requisitos", font_weight="600", color="#e2e8f0"),
                rx.markdown(vaga.prerequisites, style={"color": "#cbd5e1"}),
                spacing="1",
                align_items="start",
                width="100%",
            ),
            rx.cond(
                vaga.differentials,
                rx.vstack(
                    rx.text("Diferenciais", font_weight="600", color="#e2e8f0"),
                    rx.markdown(vaga.differentials, style={"color": "#cbd5e1"}),
                    spacing="1",
                    align_items="start",
                    width="100%",
                ),
            ),
            rx.button(
                "Analisar CV desta vaga",
                on_click=lambda: ListJobsState.analisar_vaga_selecionada(vaga.id),  # type: ignore
                bg="#2563eb",
                color="white",
                border_radius="12px",
                size="3",
                _hover={"opacity": "0.9"},
            ),
            align_items="start",
            spacing="3",
            width="100%",
        ),
        width="100%",
        border_radius="18px",
        padding="1.2em",
        style={"background": "#111827", "border": "1px solid #334155"},
    )


def show_jobs_page() -> rx.Component:
    conteudo = rx.vstack(
        rx.badge("Banco de Vagas", color_scheme="blue", variant="soft"),
        rx.heading("Vagas disponíveis", size="8", color="#f8fafc"),
        rx.text(
            "Acesse os detalhes das oportunidades e inicie a análise de currículos em um clique.",
            color="#cbd5e1",
            size="3",
        ),
        rx.vstack(
            rx.foreach(ListJobsState.vagas, desenhar_vaga),
            width="100%",
            spacing="4",
        ),
        width="100%",
        max_width="900px",
        margin="0 auto",
        spacing="4",
        align_items="start",
    )
    return base_layout(conteudo)
