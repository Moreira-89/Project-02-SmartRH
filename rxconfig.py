import reflex as rx

config = rx.Config(
    app_name="Project_02_SmartRH",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)