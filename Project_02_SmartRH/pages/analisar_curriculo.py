import reflex as rx
from Project_02_SmartRH.state.analise_state import AnaliseState

def analise_page():
    return rx.vstack(
        rx.heading("Análise de Currículo com IA", size="7"),
        rx.upload(
            rx.text("Arraste ou clique para selecionar o currículo em PDF"),
            id="upload_cv",
            accept={"application/pdf": [".pdf"]},
        ),
        rx.text(rx.selected_files("upload_cv"), size="2", color="gray.500"),
        rx.button(
            "Analisar", 
            on_click=AnaliseState.receber_e_processar_arquivo(rx.upload_files(upload_id="upload_cv")),#type: ignore
            size="3",
            loading=AnaliseState.is_loading, 
        ),
        
        rx.divider(width="100%", margin_y="4"),
        
        # Exibe os resultados apenas após a análise ter sido processada
        rx.cond(
            AnaliseState.resumo_cv != "",
            rx.vstack(
                rx.heading(
                    f"Pontuação Final: {AnaliseState.pontuacao_final} / 10.0", 
                    size="8", 
                    color="green"
                ),
                rx.heading("Resumo Estruturado", size="6", margin_top="4"),
                rx.markdown(AnaliseState.resumo_cv),
                rx.heading("Análise e Recomendações", size="6", margin_top="4"),
                rx.markdown(AnaliseState.opiniao_gerada),
                width="100%",
                align_items="start"
            )
        ),
        width="100%",
        max_width="800px",
        margin="auto",
        padding="2em"
    )