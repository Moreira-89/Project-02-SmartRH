import reflex as rx
from Project_02_SmartRH.state.job_state import JobFormState
from Project_02_SmartRH.components.layout import base_layout


INPUT_STYLE = {
    "border_radius": "12px",
    "border": "1px solid #334155",
    "bg": "#0b1220",
    "color": "#e2e8f0",
    "_placeholder": {"color": "#94a3b8"},
    "_focus": {
        "border": "1px solid #60a5fa",
        "box_shadow": "0 0 0 3px rgba(59, 130, 246, 0.18)",
    },
}


def campo_formulario(label: str, componente: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.text(label, font_weight="600", color="#f8fafc"),
        componente,
        spacing="2",
        width="100%",
        align_items="start",
    )


def add_job_page() -> rx.Component:
    conteudo = rx.vstack(
        rx.badge("Cadastro de Vaga", color_scheme="blue", variant="soft"),
        rx.heading("Adicionar nova vaga", size="8", color="#f8fafc"),
        rx.text(
            "Preencha os dados da oportunidade para disponibilizar a vaga para análise de candidatos.",
            color="#cbd5e1",
            size="3",
        ),
        rx.card(
            rx.vstack(
                campo_formulario(
                    "Título da vaga",
                    rx.input(
                        placeholder="Ex.: Analista de Dados Sênior",
                        value=JobFormState.title,
                        on_change=JobFormState.set_title,  # type: ignore
                        width="100%",
                        size="3",
                        style=INPUT_STYLE,
                    ),
                ),
                campo_formulario(
                    "Atividades principais",
                    rx.text_area(
                        placeholder="Descreva as responsabilidades e rotina principal da função.",
                        value=JobFormState.main_activity,
                        on_change=JobFormState.set_main_activity,  # type: ignore
                        width="100%",
                        min_height="140px",
                        style=INPUT_STYLE,
                    ),
                ),
                campo_formulario(
                    "Pré-requisitos",
                    rx.text_area(
                        placeholder="Ex.: Python, SQL, experiência com dashboards e BI.",
                        value=JobFormState.prerequisites,
                        on_change=JobFormState.set_prerequisites,  # type: ignore
                        width="100%",
                        min_height="120px",
                        style=INPUT_STYLE,
                    ),
                ),
                campo_formulario(
                    "Diferenciais (opcional)",
                    rx.text_area(
                        placeholder="Ex.: Certificação em cloud, inglês avançado.",
                        value=JobFormState.differentials,
                        on_change=JobFormState.set_differentials,  # type: ignore
                        width="100%",
                        min_height="100px",
                        style=INPUT_STYLE,
                    ),
                ),
                rx.button(
                    "Cadastrar vaga",
                    on_click=JobFormState.salvar_vaga,  # type: ignore
                    width="100%",
                    bg="#1d4ed8",
                    color="white",
                    size="3",
                    border_radius="12px",
                    _hover={"opacity": "0.92"},
                ),
                spacing="4",
                width="100%",
                align_items="start",
            ),
            width="100%",
            border_radius="18px",
            padding="1.2em",
            style={"background": "#111827", "border": "1px solid #334155"},
        ),
        width="100%",
        max_width="860px",
        margin="0 auto",
        spacing="4",
        align_items="start",
    )
    return base_layout(conteudo)
