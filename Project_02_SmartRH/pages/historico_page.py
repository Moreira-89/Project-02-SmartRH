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
                    rx.dialog.title(f"Candidato(a): {HistoricoState.analise_selecionada.name} | Score: {HistoricoState.analise_selecionada.score}/10"), #type: ignore
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

def historico_page():
    conteudo = rx.vstack(
        rx.heading("Histórico de Análises"),
        rx.foreach(
            HistoricoState.historico_analises,
            lambda analise: rx.card(
                rx.vstack(
                    rx.cond(
                        analise.job_title, 
                        rx.text(f"{analise.job_title}", font_weight="bold"), 
                        rx.text("Vaga não encontrada")
                    ),
                    rx.text(f"Nome do Candidato: {analise.name}"),
                    rx.text(f"Resultado: {analise.score}"),
                    rx.button("Ver Detalhes", on_click=lambda: HistoricoState.abrir_modal(analise)),#type: ignore
                    align_items="start",
                    spacing="2"
                ),
                width="100%",
                margin_bottom="1em"
            )
        ),
        modal_detalhes(),
        width="100%",
        max_width="800px",
        margin="auto"
    )
    return base_layout(conteudo)
