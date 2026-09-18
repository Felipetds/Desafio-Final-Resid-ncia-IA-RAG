import os
import sys

import gradio as gr

from app.pipeline_adapter import executar_para_interface


TITULO = "Contratações Públicas do Estado do Rio de Janeiro"

DESCRICAO = """
Sistema experimental de Adaptive RAG para consulta de informações
sobre contratações públicas do Estado do Rio de Janeiro.

A aplicação seleciona as bases adequadas, executa recuperação híbrida
e apresenta as evidências utilizadas. Enquanto o módulo de geração não
estiver integrado, a interface funcionará no modo provisório de recuperação.
"""


def criar_interface() -> gr.Blocks:
    with gr.Blocks(
        title=TITULO,
        theme=gr.themes.Soft(),
    ) as interface:
        gr.Markdown(f"# {TITULO}")
        gr.Markdown(DESCRICAO)

        with gr.Row():
            with gr.Column(scale=4):
                pergunta = gr.Textbox(
                    label="Pergunta",
                    placeholder=(
                        "Exemplo: Quais contratações de serviços "
                        "de tecnologia foram encontradas?"
                    ),
                    lines=4,
                )

            with gr.Column(scale=1):
                top_k = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=5,
                    step=1,
                    label="Quantidade de evidências",
                )

        with gr.Row():
            consultar = gr.Button(
                "Consultar",
                variant="primary",
            )
            limpar = gr.Button("Limpar")

        resposta = gr.Markdown(
            label="Resposta",
            value="Digite uma pergunta para iniciar.",
        )

        status = gr.Markdown()

        with gr.Accordion(
            "Detalhes do roteamento e da recuperação",
            open=False,
        ):
            rotas = gr.Textbox(
                label="Bases selecionadas",
                interactive=False,
            )

            filtros = gr.JSON(
                label="Filtros identificados",
            )

            evidencias = gr.JSON(
                label="Evidências recuperadas",
            )

        consultar.click(
            fn=executar_para_interface,
            inputs=[pergunta, top_k],
            outputs=[
                resposta,
                rotas,
                filtros,
                evidencias,
                status,
            ],
            api_name="consultar",
        )

        pergunta.submit(
            fn=executar_para_interface,
            inputs=[pergunta, top_k],
            outputs=[
                resposta,
                rotas,
                filtros,
                evidencias,
                status,
            ],
        )

        limpar.click(
            fn=lambda: (
                "",
                "Digite uma pergunta para iniciar.",
                "",
                {},
                [],
                "",
            ),
            inputs=[],
            outputs=[
                pergunta,
                resposta,
                rotas,
                filtros,
                evidencias,
                status,
            ],
        )

    return interface


demo = criar_interface()


if __name__ == "__main__":
    esta_no_colab = "google.colab" in sys.modules

    demo.queue().launch(
        server_name=os.getenv(
            "GRADIO_SERVER_NAME",
            "0.0.0.0",
        ),
        server_port=int(
            os.getenv(
                "GRADIO_SERVER_PORT",
                "7860",
            )
        ),
        share=esta_no_colab,
        show_error=True,
    )
