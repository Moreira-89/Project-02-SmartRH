import reflex as rx
from Project_02_SmartRH.components.layout import base_layout


def action_card(title: str, description: str, label: str, rota: str, color: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(title, size="5", color="#f8fafc"),
            rx.text(description, color="#cbd5e1", size="2"),
            rx.button(
                label,
                on_click=rx.redirect(rota),
                width="100%",
                bg=color,
                color="white",
                size="3",
                border_radius="12px",
                _hover={"opacity": "0.9"},
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
        padding="1.1em",
        border_radius="18px",
        style={
            "background": "#111827",
            "border": "1px solid #334155",
            "@media screen and (min-width: 64em)": {
                "width": "calc(50% - 0.5rem)",
            },
        },
    )


def homepage() -> rx.Component:
    conteudo = rx.vstack(
        rx.box(
            rx.vstack(
                rx.badge("Plataforma de Recrutamento", color_scheme="blue", variant="soft"),
                rx.heading("Bem-vindo ao SmartRH", size="8", color="#f8fafc"),
                rx.text(
                    "Gerencie vagas, avalie currículos com IA e tome decisões com mais confiança.",
                    size="3",
                    color="#cbd5e1",
                ),
                spacing="3",
                align_items="start",
                width="100%",
            ),
            width="100%",
            padding="1.2em",
            border_radius="20px",
            style={
                "background": "linear-gradient(120deg, #111827 0%, #1e293b 100%)",
                "border": "1px solid #334155",
            },
        ),
        rx.flex(
            action_card(
                "Vagas em aberto",
                "Veja todas as oportunidades cadastradas e avance rapidamente para análise de candidatos.",
                "Ver Vagas",
                "/listar-vagas",
                "#0f766e",
            ),
            action_card(
                "Nova oportunidade",
                "Cadastre uma nova vaga com atividades, requisitos e diferenciais para seu time.",
                "Adicionar Vaga",
                "/nova-vaga",
                "#2563eb",
            ),
            action_card(
                "Análise de currículo",
                "Faça upload do currículo em PDF e receba score e recomendações automáticas.",
                "Analisar CV",
                "/analisar-curriculo",
                "#1d4ed8",
            ),
            action_card(
                "Histórico de análises",
                "Acompanhe avaliações anteriores e compare resultados de candidatos.",
                "Abrir Histórico",
                "/historico-analise",
                "#4f46e5",
            ),
            width="100%",
            wrap="wrap",
            gap="1rem",
        ),
        width="100%",
        spacing="5",
        align_items="start",
    )
    return base_layout(conteudo)
