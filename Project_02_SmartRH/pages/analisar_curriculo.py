import reflex as rx
from Project_02_SmartRH.state.analise_state import AnaliseState
from Project_02_SmartRH.components.layout import base_layout 
from Project_02_SmartRH.state.listjob_state import ListJobsState

def analise_page():
    conteudo = rx.vstack(
        rx.heading("Análise de Currículo com IA", size="7"),
        rx.select(
            ListJobsState.lista_opcoes_vagas, #type: ignore
            placeholder="Selecione uma vaga...",
            on_change=AnaliseState.set_vaga_pelo_titulo, #type: ignore
        ),
        rx.upload(
            rx.text("Arraste ou clique para selecionar o currículo em PDF"),
            id="upload_cv",
            accept={"application/pdf": [".pdf"]},
        ),
        rx.text(rx.selected_files("upload_cv"), size="2", color="gray.500"),
        rx.button(
            "Analisar", 
            disabled=(AnaliseState.vaga_atual == None) | AnaliseState.is_loading, #type: ignore
            on_click=AnaliseState.receber_e_processar_arquivo(rx.upload_files(upload_id="upload_cv")), #type: ignore
            size="3",
            loading=AnaliseState.is_loading, 
        ),
        
        rx.divider(width="100%", margin_y="4"),
        rx.cond(
            AnaliseState.resumo_cv != "",
            rx.vstack(
                rx.heading(f"Pontuação Final: {AnaliseState.pontuacao_final} / 10.0", size="8", color="green"),
                rx.heading("Resumo Estruturado", size="6", margin_top="4"),
                rx.markdown(AnaliseState.resumo_cv),
                rx.heading(f"Análise e Recomendações para vaga: {AnaliseState.vaga_atual.title}", size="6", margin_top="4"),#type: ignore
                rx.markdown(AnaliseState.opiniao_gerada),
                rx.hstack(
                    rx.button("Salvar Análise", on_click=AnaliseState.salvar_analise),#type: ignore
                    rx.button("Limpar Análise", on_click=AnaliseState.limpar_analise, color_scheme="red", variant="soft"),#type: ignore
                    spacing="4"
                ),
                width="100%",
                align_items="start"
            ),
        ),
        width="100%",
        max_width="800px",
        margin="auto",
        padding="2em"
    )
    
    return base_layout(conteudo)