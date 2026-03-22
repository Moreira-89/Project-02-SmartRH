import reflex as rx
from Project_02_SmartRH.state.historico_state import HistoricoState
from Project_02_SmartRH.components.layout import base_layout


def secao_lista_modal(titulo: str, itens) -> rx.Component:
    return rx.vstack(
        rx.text(titulo, font_weight="700", color="#f8fafc"),
        rx.vstack(
            rx.foreach(
                itens,
                lambda item: rx.text(
                    f"• {item}",
                    color="#cbd5e1",
                    size="2",
                    line_height="1.5",
                ),
            ),
            spacing="1",
            width="100%",
            align_items="start",
        ),
        spacing="1",
        width="100%",
        align_items="start",
    )


def modal_detalhes() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.cond(
                HistoricoState.analise_selecionada,  # type: ignore
                rx.vstack(
                    rx.badge(
                        f"Vaga: {HistoricoState.analise_selecionada.job_title}", 
                        color_scheme="blue",
                        variant="soft",
                    ),  # type: ignore
                    rx.dialog.title(
                        f"Candidato(a): {HistoricoState.analise_selecionada.name}"
                    ),  # type: ignore
                    rx.text(
                        f"Score: {HistoricoState.analise_selecionada.score}",
                        color=rx.cond(HistoricoState.analise_selecionada.score >= 7, "#047857", "#b91c1c"),
                        font_weight="700",
                    ),  # type: ignore
                    rx.dialog.description(
                        rx.vstack(
                            secao_lista_modal(
                                "Educação/Cursos",
                                HistoricoState.analise_selecionada.education,  # type: ignore
                            ),
                            secao_lista_modal(
                                "Skills",
                                HistoricoState.analise_selecionada.skills,  # type: ignore
                            ),
                            secao_lista_modal(
                                "Idiomas",
                                HistoricoState.analise_selecionada.languages,  # type: ignore
                            ),
                            spacing="2",
                            align_items="start",
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    align_items="start",
                    width="100%",
                ),
                rx.text("Carregando dados...", color="#cbd5e1"),
            ),
            rx.flex(
                rx.button(
                    "Fechar",
                    on_click=HistoricoState.fechar_modal,  # type: ignore
                    border_radius="12px",
                ),
                justify="end",
                margin_top="4",
            ),
            style={
                "border_radius": "16px",
                "background": "#111827",
                "border": "1px solid #334155",
                "color": "#e2e8f0",
            },
        ),
        open=HistoricoState.on_modal,
    )


@rx.page(title="Histórico de Análises")
def historico_page() -> rx.Component:
    conteudo = rx.vstack(
        rx.badge("Rastreabilidade", color_scheme="blue", variant="soft"),
        rx.heading("Histórico de análises", size="8", color="#f8fafc"),
        rx.text(
            "Consulte resultados anteriores para comparar perfis e apoiar decisões de contratação.",
            color="#cbd5e1",
            size="3",
        ),
        rx.vstack(
            rx.foreach(
                HistoricoState.historico_analises,
                lambda analise: rx.card(
                    rx.hstack(
                        rx.vstack(
                            rx.cond(
                                analise.job_title,
                                rx.text(analise.job_title, font_weight="700", color="#f8fafc"),
                                rx.text("Vaga não encontrada", color="#cbd5e1"),
                            ),
                            rx.text(f"Candidato: {analise.name}", color="#cbd5e1"),
                            rx.text(
                                f"Resultado: {analise.score}",
                                color=rx.cond(analise.score >= 7, "#047857", "#b91c1c"),
                                font_weight="700",
                            ),
                            align_items="start",
                            spacing="1",
                        ),
                        rx.button(
                            "Ver detalhes",
                            on_click=lambda: HistoricoState.abrir_modal(analise),  # type: ignore
                            border_radius="12px",
                            variant="soft",
                            color_scheme="blue",
                        ),
                        width="100%",
                        justify="between",
                        align="center",
                    ),
                    width="100%",
                    border_radius="16px",
                    padding="1em",
                    style={"background": "#111827", "border": "1px solid #334155"},
                ),
            ),
            width="100%",
            spacing="3",
        ),
        modal_detalhes(),
        width="100%",
        max_width="900px",
        margin="0 auto",
        spacing="4",
        align_items="start",
    )
    return base_layout(conteudo)
