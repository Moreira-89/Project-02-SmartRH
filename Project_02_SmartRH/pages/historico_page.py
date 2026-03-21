import reflex as rx
from Project_02_SmartRH.state.historico_state import HistoricoState
from Project_02_SmartRH.components.layout import base_layout 

def historico_page():
    conteudo = rx.vstack(
        rx.heading("Histórico de Análises"),
        rx.foreach(
            HistoricoState.historico_analises,
            lambda analise: rx.card(
                rx.vstack(
                    rx.text(f"Nome do Candidato: {analise.name}"),
                    rx.text(f"Resultado: {analise.score}"),
                    align_items="start",
                    spacing="2"
                ),
                width="100%",
                margin_bottom="1em"
            )
        ),
        width="100%",
        max_width="800px",
        margin="auto"
    )
    return base_layout(conteudo)
