import reflex as rx
from Project_02_SmartRH.state.listjob_state import ListJobsState
from Project_02_SmartRH.components.layout import base_layout


PREVIEW_STYLE = {
    "color": "#cbd5e1",
    "overflow": "hidden",
    "display": "-webkit-box",
    "-webkit-line-clamp": "3",
    "-webkit-box-orient": "vertical",
}


def bloco_preview(titulo: str, texto: str) -> rx.Component:
    return rx.vstack(
        rx.text(titulo, font_weight="600", color="#e2e8f0"),
        rx.text(texto, style=PREVIEW_STYLE, size="2"),
        spacing="1",
        align_items="start",
        width="100%",
    )


def modal_detalhes_vaga(vaga) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Ver detalhes",
                variant="soft",
                color_scheme="gray",
                border_radius="12px",
            )
        ),
        rx.dialog.content(
            rx.dialog.title(vaga.title, color="#f8fafc"),
            rx.vstack(
                rx.vstack(
                    rx.text("Atividades principais", font_weight="700", color="#e2e8f0"),
                    rx.markdown(vaga.main_activity, style={"color": "#cbd5e1"}),
                    spacing="1",
                    align_items="start",
                    width="100%",
                ),
                rx.vstack(
                    rx.text("Pré-requisitos", font_weight="700", color="#e2e8f0"),
                    rx.markdown(vaga.prerequisites, style={"color": "#cbd5e1"}),
                    spacing="1",
                    align_items="start",
                    width="100%",
                ),
                rx.cond(
                    vaga.differentials,
                    rx.vstack(
                        rx.text("Diferenciais", font_weight="700", color="#e2e8f0"),
                        rx.markdown(vaga.differentials, style={"color": "#cbd5e1"}),
                        spacing="1",
                        align_items="start",
                        width="100%",
                    ),
                ),
                spacing="3",
                align_items="start",
                width="100%",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Fechar", border_radius="12px")
                ),
                justify="end",
                margin_top="4",
            ),
            style={
                "background": "#111827",
                "border": "1px solid #334155",
                "border_radius": "16px",
            },
        ),
    )


def desenhar_vaga(vaga) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.vstack(
                rx.hstack(
                    rx.badge(
                        rx.cond(vaga.status == "active", "Ativa", "Inativa"),
                        color_scheme=rx.cond(vaga.status == "active", "green", "gray"),
                        variant="soft",
                    ),
                    rx.badge(
                        f"{vaga.requirements_count} requisitos",
                        color_scheme="blue",
                        variant="soft",
                    ),
                    rx.badge("Prioridade padrão", color_scheme="gray", variant="soft"),
                    width="100%",
                    wrap="wrap",
                    gap="0.45rem",
                ),
                rx.heading(vaga.title, size="6", color="#f8fafc"),
                bloco_preview("Atividades", vaga.main_activity),
                bloco_preview("Pré-requisitos", vaga.prerequisites),
                spacing="2",
                align_items="start",
                width="100%",
            ),
            rx.hstack(
                modal_detalhes_vaga(vaga),
                rx.button(
                    "Analisar CV desta vaga",
                    on_click=lambda: ListJobsState.analisar_vaga_selecionada(vaga.id),  # type: ignore
                    bg="#2563eb",
                    color="white",
                    border_radius="12px",
                    size="3",
                    _hover={"opacity": "0.9"},
                ),
                width="100%",
                justify="between",
                align="center",
                margin_top="auto",
                wrap="wrap",
                gap="0.6rem",
            ),
            align_items="start",
            spacing="3",
            width="100%",
            min_height="100%",
        ),
        width="100%",
        border_radius="18px",
        padding="1.2em",
        style={
            "background": "#111827",
            "border": "1px solid #334155",
            "@media screen and (min-width: 64em)": {
                "width": "calc(50% - 0.5rem)",
            },
        },
    )


def show_jobs_page() -> rx.Component:
    conteudo = rx.vstack(
        rx.badge("Banco de Vagas", color_scheme="blue", variant="soft"),
        rx.heading("Vagas disponíveis", size="8", color="#f8fafc"),
        rx.text(
            "Busque oportunidades, filtre status e analise candidatos com mais agilidade.",
            color="#cbd5e1",
            size="3",
        ),
        rx.card(
            rx.hstack(
                rx.input(
                    placeholder="Buscar por título, atividade ou requisito...",
                    value=ListJobsState.search_term,
                    on_change=ListJobsState.set_search_term,  # type: ignore
                    width="100%",
                    size="3",
                    style={
                        "background": "#0b1220",
                        "border": "1px solid #334155",
                        "color": "#e2e8f0",
                        "border_radius": "12px",
                        "_placeholder": {"color": "#94a3b8"},
                    },
                ),
                rx.select(
                    ["Todas", "Ativas"],
                    value=ListJobsState.status_filter,
                    on_change=ListJobsState.set_status_filter,  # type: ignore
                    width="220px",
                    style={
                        "background": "#0b1220",
                        "border": "1px solid #334155",
                        "color": "#e2e8f0",
                        "border_radius": "12px",
                    },
                ),
                width="100%",
                wrap="wrap",
                gap="0.7rem",
            ),
            width="100%",
            padding="1em",
            style={"background": "#111827", "border": "1px solid #334155"},
        ),
        rx.cond(
            ListJobsState.vagas_filtradas.length() > 0,
            rx.flex(
                rx.foreach(ListJobsState.vagas_filtradas, desenhar_vaga),
                width="100%",
                wrap="wrap",
                gap="1rem",
            ),
            rx.card(
                rx.text(
                    "Nenhuma vaga encontrada com os filtros atuais.",
                    color="#cbd5e1",
                ),
                width="100%",
                padding="1.2em",
                style={"background": "#111827", "border": "1px solid #334155"},
            ),
        ),
        width="100%",
        max_width="980px",
        margin="0 auto",
        spacing="4",
        align_items="start",
    )
    return base_layout(conteudo)
