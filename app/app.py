import os
import sys

import gradio as gr

from app.feedback_store import registrar_feedback
from app.pipeline_adapter import executar_para_interface


TITULO = "Contratações Públicas do Estado do Rio de Janeiro"

DESCRICAO = """
Sistema experimental de Adaptive RAG para consulta de informações
sobre contratações públicas do Estado do Rio de Janeiro.

A aplicação seleciona as bases adequadas, executa recuperação híbrida
e apresenta as evidências utilizadas na resposta.
"""


def limpar_feedback():
    """Limpa os componentes da avaliação."""
    return (
        None,
        "",
        "",
    )


def limpar_interface():
    """Limpa a consulta, a resposta e o formulário de feedback."""
    return (
        "",
        "Digite uma pergunta para iniciar.",
        "",
        {},
        [],
        "",
        None,
        "",
        "",
    )


def criar_interface() -> gr.Blocks:
    with gr.Blocks(
        title=TITULO,
    ) as interface:
        gr.Markdown(f"# {TITULO}")
        gr.Markdown(DESCRICAO)

        with gr.Row():
            with gr.Column(scale=4):
                pergunta = gr.Textbox(
                    label="Pergunta",
                    placeholder=(
                        "Exemplo: Quais contratações envolvem "
                        "serviços de tecnologia?"
                    ),
                    lines=4,
                )

            with gr.Column(scale=1):
                top_k = gr.Slider(
                    minimum=1,
                    maximum=5,
                    value=3,
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
            value="Digite uma pergunta para iniciar.",
        )

        status = gr.Markdown("")

        with gr.Accordion(
            "Avalie esta resposta",
            open=False,
        ):
            avaliacao_feedback = gr.Radio(
                choices=[
                    "Útil",
                    "Não útil",
                ],
                value=None,
                label="Avaliação",
            )

            comentario_feedback = gr.Textbox(
                label="Comentário opcional",
                placeholder=(
                    "Informe o que ajudou ou o que pode melhorar."
                ),
                lines=3,
            )

            enviar_feedback = gr.Button(
                "Enviar feedback",
                variant="secondary",
            )

            confirmacao_feedback = gr.Markdown("")

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

        # Limpa o feedback anterior antes de iniciar uma nova consulta.
        evento_consultar = consultar.click(
            fn=limpar_feedback,
            inputs=[],
            outputs=[
                avaliacao_feedback,
                comentario_feedback,
                confirmacao_feedback,
            ],
            queue=False,
        )

        evento_consultar.then(
            fn=executar_para_interface,
            inputs=[
                pergunta,
                top_k,
            ],
            outputs=[
                resposta,
                rotas,
                filtros,
                evidencias,
                status,
            ],
            api_name="consultar",
        )

        evento_enter = pergunta.submit(
            fn=limpar_feedback,
            inputs=[],
            outputs=[
                avaliacao_feedback,
                comentario_feedback,
                confirmacao_feedback,
            ],
            queue=False,
        )

        evento_enter.then(
            fn=executar_para_interface,
            inputs=[
                pergunta,
                top_k,
            ],
            outputs=[
                resposta,
                rotas,
                filtros,
                evidencias,
                status,
            ],
        )

        enviar_feedback.click(
            fn=registrar_feedback,
            inputs=[
                pergunta,
                avaliacao_feedback,
                comentario_feedback,
                rotas,
                evidencias,
                status,
            ],
            outputs=[
                confirmacao_feedback,
            ],
        )

        limpar.click(
            fn=limpar_interface,
            inputs=[],
            outputs=[
                pergunta,
                resposta,
                rotas,
                filtros,
                evidencias,
                status,
                avaliacao_feedback,
                comentario_feedback,
                confirmacao_feedback,
            ],
            queue=False,
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
        theme=gr.themes.Soft(),
    )
