"""Seleção controlada do novo caminho analítico da interface."""

import os
import re
import unicodedata

from src.obs import observar_etapa


def deve_usar_analitica(pergunta, consulta):
    if os.getenv("RAG_ANALYTICAL_ENABLED", "false").lower() != "true":
        return False
    if os.getenv("RAG_DEMO_OFFLINE", "false").lower() == "true":
        return False

    plano = consulta.get("plano") or {}
    if consulta.get("is_refusal") or plano.get("is_refusal"):
        return False
    if consulta.get("estrategia") == "recusa":
        return False

    # A verificação de vínculos existente continua no executor próprio.
    if (
        consulta.get("operacao") == "resumir_itens_vinculos"
        or plano.get("operacao") == "resumir_itens_vinculos"
    ):
        return False

    texto = "".join(
        c for c in unicodedata.normalize("NFD", pergunta.casefold())
        if unicodedata.category(c) != "Mn"
    )
    fonte_identificada = bool(
        re.search(r"\bpe\s*038\s*/\s*26\s*/\s*2026\b", texto)
        or re.search(r"\bpca\b|plano de contratacoes anual", texto)
    )
    pedido_analitico = bool(re.search(
        r"\b(?:quantos|quantas|quantidade|numero|total|soma|some|somar|"
        r"media|medio|medios|medias|conte|contagem|compare|comparar|"
        r"diferenca|percentual|porcentagem|percentagem|razao|"
        r"liste|listar|mostre|tabela|maiores|menores|maximo|minimo|"
        r"resuma|resumo|calcule|calcular)\b",
        texto,
    ))
    return fonte_identificada and pedido_analitico


def tentar_analitica(
    pergunta, consulta, *, run_id, on_progress=None, top_k=3
):
    if not deve_usar_analitica(pergunta, consulta):
        return None

    from app.analytical_adapter import executar_analitica_interface

    plano = consulta.get("plano") or {}
    query_id = consulta.get("query_id") or plano.get("query_id")

    with observar_etapa(
        run_id=run_id,
        query_id=query_id,
        stage="roteamento",
        input_data={
            "tipo": "selecao_caminho_analitico",
            "pergunta": pergunta,
        },
    ) as evento:
        evento["output"] = {
            "destino": "adaptador_analitico",
            "estrategia_anterior": (
                consulta.get("estrategia") or plano.get("estrategia")
            ),
        }

    def executar_documental(pedido):
        # Evita recursão quando a decomposição conserva um pedido analítico.
        if deve_usar_analitica(pedido, {}):
            return {
                "executado": False,
                "necessita_esclarecimento": True,
                "answer": (
                    "O pedido documental ainda contém uma tarefa analítica. "
                    "Não foi executada uma consulta documental independente."
                ),
                "routes": [],
                "fontes_citadas": [],
            }

        from app.pipeline_adapter import executar_pipeline
        return executar_pipeline(pedido, top_k=top_k)

    return executar_analitica_interface(
        pergunta,
        run_id=run_id,
        query_id=query_id,
        on_progress=on_progress,
        documental_executor=executar_documental,
    )
