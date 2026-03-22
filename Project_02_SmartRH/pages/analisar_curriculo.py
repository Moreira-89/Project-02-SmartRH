import reflex as rx
from Project_02_SmartRH.state.analise_state import AnaliseState
from Project_02_SmartRH.components.layout import base_layout
from Project_02_SmartRH.state.listjob_state import ListJobsState


@rx.page(title="Análise de Currículo")
def analise_page() -> rx.Component:
    conteudo = rx.vstack(
        rx.badge("IA aplicada ao RH", color_scheme="blue", variant="soft"),
        rx.heading("Análise de currículo", size="8", color="#f8fafc"),
        rx.text(
            "Selecione a vaga, envie o PDF e obtenha score de aderência com recomendações acionáveis.",
            color="#cbd5e1",
            size="3",
        ),
        rx.card(
            rx.vstack(
                rx.vstack(
                    rx.text("Vaga", font_weight="600", color="#f8fafc"),
                    rx.select(
                        ListJobsState.lista_opcoes_vagas,  # type: ignore
                        placeholder="Selecione uma vaga...",
                        on_change=AnaliseState.set_vaga_pelo_titulo,  # type: ignore
                        width="100%",
                        size="3",
                        style={
                            "border_radius": "12px",
                            "border": "1px solid #334155",
                            "background": "#0b1220",
                            "color": "#e2e8f0",
                        },
                    ),
                    spacing="2",
                    width="100%",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Currículo em PDF", font_weight="600", color="#f8fafc"),
                    rx.upload(
                        rx.vstack(
                            rx.text("Arraste o arquivo aqui ou clique para selecionar", color="#e2e8f0"),
                            rx.text("Formato aceito: .pdf", size="2", color="#94a3b8"),
                            spacing="1",
                            align_items="center",
                        ),
                        id="upload_cv",
                        accept={"application/pdf": [".pdf"]},
                        width="100%",
                        padding="1.4em",
                        border_radius="14px",
                        style={
                            "border": "1px dashed #3b82f6",
                            "background": "#0b1220",
                        },
                    ),
                    rx.text(rx.selected_files("upload_cv"), size="2", color="#94a3b8"),
                    spacing="2",
                    width="100%",
                    align_items="start",
                ),
                rx.button(
                    "Analisar currículo",
                    disabled=(AnaliseState.vaga_atual == None) | AnaliseState.is_loading,  # type: ignore
                    on_click=AnaliseState.receber_e_processar_arquivo(  # type: ignore
                        rx.upload_files(upload_id="upload_cv")
                    ),
                    loading=AnaliseState.is_loading,
                    bg="#1d4ed8",
                    color="white",
                    size="3",
                    border_radius="12px",
                    width="100%",
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
        rx.cond(
            AnaliseState.resumo_cv != "",
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Resultado da análise", size="6", color="#f8fafc"),
                        rx.badge(
                            f"Score: {AnaliseState.pontuacao_final} / 10.0",
                            color_scheme=rx.cond(AnaliseState.pontuacao_final >= 7, "green", "orange"),
                            variant="solid",
                        ),
                        width="100%",
                        justify="between",
                        align="center",
                    ),
                    rx.divider(width="100%"),
                    rx.vstack(
                        rx.heading("Resumo estruturado", size="5", color="#e2e8f0"),
                        rx.markdown(AnaliseState.resumo_cv, style={"color": "#cbd5e1"}),
                        width="100%",
                        align_items="start",
                        spacing="2",
                    ),
                    rx.vstack(
                        rx.heading(
                            f"Recomendações para vaga: {AnaliseState.vaga_atual.title}",
                            size="5",
                            color="#e2e8f0",
                        ),  # type: ignore
                        rx.markdown(AnaliseState.opiniao_gerada, style={"color": "#cbd5e1"}),
                        width="100%",
                        align_items="start",
                        spacing="2",
                    ),
                    rx.flex(
                        rx.button(
                            "Salvar análise",
                            on_click=AnaliseState.salvar_analise,  # type: ignore
                            bg="#0f766e",
                            color="white",
                            border_radius="12px",
                        ),
                        rx.button(
                            "Limpar",
                            on_click=AnaliseState.limpar_analise,  # type: ignore
                            variant="soft",
                            color_scheme="red",
                            border_radius="12px",
                        ),
                        width="100%",
                        gap="0.7rem",
                        wrap="wrap",
                    ),
                    width="100%",
                    align_items="start",
                    spacing="3",
                ),
                width="100%",
                border_radius="18px",
                padding="1.2em",
                style={"background": "#111827", "border": "1px solid #334155"},
            ),
        ),
        width="100%",
        max_width="920px",
        margin="0 auto",
        spacing="4",
        align_items="start",
    )

    return base_layout(conteudo)
