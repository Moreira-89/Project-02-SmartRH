import reflex as rx

def base_layout(conteudo_da_pagina: rx.Component) -> rx.Component:
    return rx.hstack(
        # Lado Esquerdo: O Menu Lateral (Sidebar)
        rx.vstack(
            rx.heading("SmartRH", size="6"),
            rx.link("Home", href="/"),
            rx.link("Vagas", href="/listar-vagas"),
            rx.link("Adicionar Vaga", href="/nova-vaga"),
            rx.link("Analisar CV", href="/analisar-curriculo"),
            width="250px",
            height="100vh",
            bg="gray.100",
            padding="2em"
        ),
        # Lado Direito: O conteúdo principal (a "carta")
        rx.box(
            conteudo_da_pagina,
            width="100%",
        )
    )