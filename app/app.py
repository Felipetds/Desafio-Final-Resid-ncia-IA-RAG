"""Interface para consultas estruturadas e documentais."""

import os
import sys

import gradio as gr

from app.pipeline_adapter import executar_pipeline
from app.interface_results import (
    feedback_da_consulta,
    mudar_pagina,
    status_consulta,
    tabela_consulta,
)


TITULO = "Contratações Públicas do Estado do Rio de Janeiro"

DESCRICAO = (
    "Contagens e listagens sobre a base disponível "
    "e respostas documentais com fontes."
)


def apresentar(resultado):
    lista = (
        resultado.get("operacao") == "listar"
        and resultado.get("executado", False)
    )

    estruturada = (
        resultado.get("estrategia") == "consulta_estruturada"
    )

    pagina = resultado.get("pagina") or 1
    paginas = resultado.get("total_paginas", 0)

    detalhes = {
        "plano": resultado.get("plano", {}),
        "fontes": resultado.get("fontes", []),
        "fontes_estruturadas": resultado.get("fontes_estruturadas", []),
        "fontes_recuperadas": resultado.get("fontes_recuperadas", []),
        "fontes_citadas": resultado.get("fontes_citadas", []),
        "documental_query_id": resultado.get("documental_query_id"),
        "documental_run_id": resultado.get("documental_run_id"),
        "paginacao_run_id": resultado.get("paginacao_run_id"),
        "referencias": resultado.get("referencias", []),
        "evidencias": resultado.get("evidences", []),
    }

    return (
        resultado.get("answer", ""),
        gr.update(
            value=tabela_consulta(resultado),
            visible=lista,
        ),
        gr.update(visible=lista),
        gr.update(interactive=lista and pagina > 1),
        gr.update(interactive=lista and pagina < paginas),
        ", ".join(resultado.get("routes", [])),
        resultado.get("filters", {}),
        detalhes,
        status_consulta(resultado),
        resultado,
        None,
        "",
        "",
        gr.update(interactive=not estruturada),
    )


def executar(pergunta, top_k, progress=gr.Progress()):
    try:
        resultado = executar_pipeline(
            pergunta,
            top_k,
            on_progress=lambda valor, texto: progress(
                valor,
                desc=texto,
            ),
        )

        return apresentar(resultado)

    except Exception as erro:
        return apresentar({
            "answer": (
                "Não foi possível concluir a consulta: "
                f"{erro}"
            ),
        })


def navegar(resultado, direcao):
    try:
        return apresentar(
            mudar_pagina(resultado, direcao)
        )

    except Exception as erro:
        gr.Warning(str(erro))
        return apresentar(resultado or {})


def limpar_interface():
    return (
        "",
        *apresentar({
            "answer": "Digite uma pergunta para iniciar.",
        }),
    )


def criar_interface():
    with gr.Blocks(title=TITULO) as interface:
        gr.Markdown(f"# {TITULO}")
        gr.Markdown(DESCRICAO)

        gr.Markdown(
            "A quantidade de evidências vale apenas para "
            "consultas documentais. Não limita contagens "
            "ou listagens. O progresso indica etapas, "
            "não uma estimativa exata do tempo restante."
        )

        contexto = gr.State({})

        pergunta = gr.Textbox(
            label="Pergunta",
            lines=3,
            placeholder=(
                "Quantas contratações têm ano da compra 2026?"
            ),
        )

        top_k = gr.Slider(
            minimum=1,
            maximum=5,
            value=3,
            step=1,
            label="Evidências para consultas documentais",
        )

        with gr.Row():
            consultar = gr.Button(
                "Consultar",
                variant="primary",
            )
            limpar = gr.Button("Limpar")

        resposta = gr.Markdown(
            "Digite uma pergunta para iniciar."
        )

        tabela = gr.Dataframe(
            headers=None,
            value=[],
            interactive=False,
            visible=False,
            label="Registros da página",
        )

        with gr.Row(visible=False) as paginacao:
            anterior = gr.Button(
                "Página anterior",
                interactive=False,
            )
            proxima = gr.Button(
                "Próxima página",
                interactive=False,
            )

        status = gr.Markdown()

        with gr.Accordion(
            "Avalie esta resposta",
            open=False,
        ):
            avaliacao = gr.Radio(
                choices=["Útil", "Não útil"],
                label="Avaliação",
                value=None,
            )
            comentario = gr.Textbox(
                label="Comentário opcional",
                lines=2,
            )
            enviar = gr.Button("Enviar feedback")
            confirmacao = gr.Markdown()

        with gr.Accordion(
            "Plano fontes e evidências",
            open=False,
        ):
            rotas = gr.Textbox(
                label="Bases selecionadas",
                interactive=False,
            )
            filtros = gr.JSON(
                label="Filtros aplicados",
            )
            detalhes = gr.JSON(
                label="Plano fontes referências e evidências",
            )

        saidas = [
            resposta,
            tabela,
            paginacao,
            anterior,
            proxima,
            rotas,
            filtros,
            detalhes,
            status,
            contexto,
            avaliacao,
            comentario,
            confirmacao,
            top_k,
        ]

        opcoes = {
            "concurrency_id": "consultas",
            "concurrency_limit": 1,
        }

        clique = consultar.click(
            fn=executar,
            inputs=[pergunta, top_k],
            outputs=saidas,
            api_name="consultar",
            **opcoes,
        )

        enter = pergunta.submit(
            fn=executar,
            inputs=[pergunta, top_k],
            outputs=saidas,
            **opcoes,
        )

        volta = anterior.click(
            fn=lambda resultado: navegar(resultado, -1),
            inputs=[contexto],
            outputs=saidas,
            **opcoes,
        )

        avanca = proxima.click(
            fn=lambda resultado: navegar(resultado, 1),
            inputs=[contexto],
            outputs=saidas,
            **opcoes,
        )

        feedback = enviar.click(
            fn=feedback_da_consulta,
            inputs=[contexto, avaliacao, comentario],
            outputs=[confirmacao],
            **opcoes,
        )

        # Permite escolher evidências para uma nova pergunta.
        pergunta.input(
            fn=lambda: gr.update(interactive=True),
            outputs=[top_k],
            queue=False,
        )

        limpar.click(
            fn=limpar_interface,
            outputs=[pergunta, *saidas],
            queue=False,
            cancels=[clique, enter, volta, avanca, feedback],
        )

    return interface


demo = criar_interface()


if __name__ == "__main__":
    demo.queue().launch(
        server_name=os.getenv(
            "GRADIO_SERVER_NAME",
            "0.0.0.0",
        ),
        server_port=int(
            os.getenv("GRADIO_SERVER_PORT", "7860")
        ),
        share="google.colab" in sys.modules,
        show_error=True,
        theme=gr.themes.Soft(),
    )
