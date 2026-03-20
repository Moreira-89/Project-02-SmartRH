import reflex as rx
from Project_02_SmartRH.components.layout import base_layout

def homepage():
    conteudo = rx.vstack(
        rx.heading("Bem-vindo ao SmartRH!", size="7"),
        rx.text("Gerencie suas vagas e analise currículos de forma inteligente."),
        
        rx.button("Ver Vagas", on_click=rx.redirect("/listar-vagas")),
        rx.button("Adicionar Vaga", on_click=rx.redirect("/nova-vaga")),
        rx.button("Analisar CV", on_click=rx.redirect("/analisar-curriculo")),
        
        width="100%",
        max_width="800px",
        margin="auto",
        spacing="4"
    )
    
    return base_layout(conteudo)