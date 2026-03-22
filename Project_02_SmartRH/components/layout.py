import reflex as rx


SIDEBAR_LINK_STYLE = {
    "display": "block",
    "padding": "0.65em 0.9em",
    "border_radius": "12px",
    "font_weight": "500",
    "color": "#e2e8f0",
    "text_decoration": "none",
    "transition": "all 160ms ease",
    "_hover": {
        "bg": "#1e293b",
        "transform": "translateX(2px)",
    },
}


def nav_link(label: str, href: str) -> rx.Component:
    return rx.link(label, href=href, style=SIDEBAR_LINK_STYLE)


def base_layout(conteudo_da_pagina: rx.Component) -> rx.Component:
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.box(
                    rx.heading("SmartRH", size="7", color="#f8fafc"),
                    rx.text(
                        "Recrutamento inteligente com IA",
                        color="#94a3b8",
                        size="2",
                    ),
                    spacing="1",
                    width="100%",
                ),
                rx.divider(width="100%"),
                rx.vstack(
                    nav_link("Home", "/"),
                    nav_link("Vagas", "/listar-vagas"),
                    nav_link("Adicionar Vaga", "/nova-vaga"),
                    nav_link("Analisar CV", "/analisar-curriculo"),
                    nav_link("Histórico de Análises", "/historico-analise"),
                    spacing="2",
                    width="100%",
                    align_items="stretch",
                ),
                width="100%",
                min_width="100%",
                height="auto",
                position="static",
                top="0",
                bg="rgba(2, 6, 23, 0.8)",
                border="1px solid rgba(71, 85, 105, 0.55)",
                border_radius="20px",
                box_shadow="0 10px 30px rgba(2, 6, 23, 0.5)",
                backdrop_filter="blur(8px)",
                padding="1.2em",
                spacing="4",
                align_items="start",
                style={
                    "@media screen and (min-width: 64em)": {
                        "width": "280px",
                        "minWidth": "280px",
                        "height": "calc(100vh - 3rem)",
                        "position": "sticky",
                        "top": "1.5rem",
                    }
                },
            ),
            rx.box(
                conteudo_da_pagina,
                width="100%",
                min_height="calc(100vh - 3rem)",
                bg="rgba(15, 23, 42, 0.8)",
                border="1px solid rgba(71, 85, 105, 0.55)",
                border_radius="20px",
                box_shadow="0 14px 40px rgba(2, 6, 23, 0.4)",
                padding="1.4em",
            ),
            direction="column",
            gap="1rem",
            align="start",
            width="100%",
            style={
                "@media screen and (min-width: 64em)": {
                    "flexDirection": "row",
                }
            },
        ),
        width="100%",
        min_height="100vh",
        padding="1rem",
        style={
            "background": "linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%)",
            "font_family": "'Manrope', 'Segoe UI', sans-serif",
        },
    )
