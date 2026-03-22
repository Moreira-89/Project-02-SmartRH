import reflex as rx
from Project_02_SmartRH.state.historico_state import HistoricoState
from Project_02_SmartRH.components.layout import base_layout 


def modal_detalhes():
    return rx.dialog.root(
        rx.dialog.content(
            rx.cond(
                HistoricoState.analise_selecionada, #type: ignore
                rx.vstack(
                    rx.text(f"{HistoricoState.analise_selecionada.job_title}", font_weight="bold"),#type: ignore 
                    rx.dialog.title(f"Candidato(a): {HistoricoState.analise_selecionada.name}"), #type: ignore
                    rx.text(f"Score: {HistoricoState.analise_selecionada.score}", color=rx.cond(HistoricoState.analise_selecionada.score >= 7, "green", "red")), #type: ignore
                    rx.dialog.description(
                        rx.vstack(
                            rx.text(f"Educação/Cursos: {HistoricoState.analise_selecionada.education}"), #type: ignore
                            rx.text(f"Skills: {HistoricoState.analise_selecionada.skills}"), #type: ignore
                            rx.text(f"Linguagens: {HistoricoState.analise_selecionada.languages}"), #type: ignore
                        ),                  
                ),
            ),
            rx.text("Carregando dados.."),
            ),
            
            rx.flex(
                rx.button("Fechar", on_click=HistoricoState.fechar_modal), #type: ignore
                justify="end",
                margin_top="4"
            )
        ),
        open=HistoricoState.on_modal, # 2. Variável booleana de controle
    )

@rx.page(title="Histórico de Análises")
def historico_page() -> rx.Component:
    conteudo = rx.vstack(
        rx.heading("Histórico de Análises de Candidatos"),
        rx.foreach(
        HistoricoState.historico_analises,
        lambda analise: rx.card(
            rx.hstack(
                rx.vstack(
                    rx.cond(
                        analise.job_title, 
                        rx.text(f"{analise.job_title}", font_weight="bold"), 
                        rx.text("Vaga não encontrada")
                    ),
                    rx.text(f"Nome do Candidato: {analise.name}"),
                    rx.text(f"Resultado: {analise.score}", color=rx.cond(analise.score >= 7, "green", "red"), font_weight="bold"),
                    align_items="start",
                    spacing="2"
                ),
                rx.button("Ver Detalhes", on_click=lambda: HistoricoState.abrir_modal(analise)), # type: ignore
                width="100%",
                justify="between",
                align="center"
            ),
            width="100%",
            margin_bottom="1em"
        )
        ),
        modal_detalhes()
    )
    return base_layout(conteudo)
