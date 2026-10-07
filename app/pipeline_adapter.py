"""Integra o executor das consultas à interface."""

import os
import re
import time
from typing import Any, Callable, Dict, List

import gradio as gr

from src.generate import GENERATION_MODEL, gerar_resposta
from src.obs import novo_run_id, observar_etapa
from src.query_executor import executar_consulta
from src.schema import RAGResponse

from app.interface_results import (
    preparar_estruturado,
    preparar_agregado,
    preparar_combinado,
    status_consulta,
)


ProgressCallback = Callable[[float, str], None]


def _converter_dict(valor: Any) -> Dict[str, Any]:
    if isinstance(valor, dict):
        return valor

    if hasattr(valor, "model_dump"):
        return valor.model_dump()

    if hasattr(valor, "dict"):
        return valor.dict()

    raise TypeError(
        f"Não foi possível converter {type(valor).__name__}."
    )


def _formatar_evidencias(
    evidencias: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    return [
        {
            "posição": posicao,
            "chunk_id": evidencia.get("chunk_id"),
            "trecho": evidencia.get("text", ""),
            "fonte": evidencia.get("source_file"),
            "tipo_documento": evidencia.get("doc_type"),
            "base": evidencia.get("base_id"),
            "natureza": evidencia.get("natureza"),
            "score_rrf": evidencia.get("rrf_score"),
            "métodos": evidencia.get("retrieval_sources", []),
        }
        for posicao, evidencia in enumerate(evidencias, start=1)
    ]


def _obter_fetch_k() -> int:
    try:
        valor = int(os.getenv("RAG_FETCH_K", "50"))
    except (TypeError, ValueError):
        valor = 50

    return max(20, min(valor, 200))


def _notificar_progresso(callback, percentual, descricao):
    if callback is not None:
        callback(percentual, descricao)


def _preparar_entrada_geracao(recuperacao, *, combinada):
    """Prepara a tarefa documental sem alterar o contexto original."""
    from copy import deepcopy
    import re

    entrada = deepcopy(recuperacao)

    if not combinada:
        return entrada

    pergunta_original = entrada.get("query", "")

    # Decomposição limitada a uma forma explícita e conhecida.
    # Não divide perguntas arbitrariamente pela palavra "e".
    correspondencia = re.fullmatch(
        r"\s*Quantas\s+contratações\s+têm\s+ano\s+da\s+compra"
        r"\s+\d{4}\s+e\s+"
        r"(?P<documental>o\s+que\s+a\s+Lei\b.+)",
        pergunta_original,
        flags=re.IGNORECASE,
    )

    if correspondencia:
        entrada["query"] = correspondencia.group("documental").strip()
    else:
        entrada["query"] = (
            "Responda exclusivamente ao pedido documental. "
            "A operação estruturada será apresentada separadamente. "
            "Não responda novamente à contagem ou listagem.\n\n"
            + pergunta_original
        )

    return entrada



def executar_pipeline(
    pergunta: str,
    top_k: int = 3,
    on_progress: ProgressCallback | None = None,
) -> Dict[str, Any]:
    pergunta = str(pergunta or "").strip()

    if not pergunta:
        raise ValueError("Digite uma pergunta antes de consultar.")

    top_k = max(1, min(int(top_k), 5))
    fetch_k = _obter_fetch_k()
    run_id = novo_run_id()
    inicio = time.perf_counter()

    _notificar_progresso(
        on_progress,
        0.05,
        "Preparando a consulta...",
    )
    _notificar_progresso(
        on_progress,
        0.15,
        "Interpretando e executando a consulta...",
    )

    consulta = executar_consulta(
        pergunta=pergunta,
        top_k=top_k,
        fetch_k=fetch_k,
        run_id=run_id,
    )

    plano = consulta.get("plano", {})
    query_id = consulta.get("query_id") or plano.get("query_id")

    if not consulta.get("executado", True):
        _notificar_progresso(
            on_progress,
            1.0,
            "Consulta encerrada.",
        )

        return {
            "answer": (
                consulta.get("mensagem")
                or "Esclareça os critérios da pergunta."
            ),
            "query": pergunta,
            "query_id": query_id,
            "run_id": run_id,
            "routes": plano.get("bases", []),
            "filters": plano.get("filtros", {}),
            "plano": plano,
            "executado": False,
            "estrategia": plano.get("estrategia"),
            "is_refusal": plano.get("is_refusal", False),
            "necessita_esclarecimento": plano.get(
                "necessita_esclarecimento",
                False,
            ),
            "evidences": [],
            "tokens": {},
            "latency_ms": round(
                (time.perf_counter() - inicio) * 1000,
                2,
            ),
        }

    if consulta.get("estrategia") == "consulta_estruturada":
        _notificar_progresso(
            on_progress,
            1.0,
            "Consulta estruturada concluída.",
        )

        return preparar_estruturado(
            consulta,
            latencia_ms=round(
                (time.perf_counter() - inicio) * 1000,
                2,
            ),
        )

    if consulta.get("estrategia") == "consulta_agregada":
        _notificar_progresso(
            on_progress,
            1.0,
            "Consulta agregada concluída.",
        )
        return preparar_agregado(
            consulta,
            latencia_ms=round(
                (time.perf_counter() - inicio) * 1000,
                2,
            ),
        )

    combinada = consulta.get("estrategia") == "combinada"
    recuperacao = consulta["hibrida"] if combinada else consulta

    entrada_geracao = _preparar_entrada_geracao(
        recuperacao,
        combinada=combinada,
    )

    _notificar_progresso(
        on_progress,
        0.60,
        "Evidências recuperadas. Gerando a resposta...",
    )

    with observar_etapa(
        run_id=run_id,
        query_id=query_id,
        stage="geracao",
        input_data={
            "pergunta": pergunta,
            "quantidade_evidencias": len(
                recuperacao.get("evidences", [])
            ),
        },
        modelo=GENERATION_MODEL,
        extra={
            "rotas": consulta.get("routes", []),
            "top_k": top_k,
            "fetch_k": fetch_k,
        },
    ) as observacao:
        resposta_dict = _converter_dict(
            gerar_resposta(
                resultado_recuperacao=entrada_geracao,
                run_id=run_id,
            )
        )

        observacao["output"] = {
            "resposta_gerada": bool(resposta_dict.get("answer")),
            "nivel_confianca": resposta_dict.get(
                "confidence_level"
            ),
            "quantidade_fontes": len(
                resposta_dict.get("sources_used", [])
            ),
            "recusa": resposta_dict.get("is_refusal", False),
        }
        observacao["tokens"] = resposta_dict.get("tokens", {})

    _notificar_progresso(
        on_progress,
        0.90,
        "Validando a resposta e organizando as fontes...",
    )

    with observar_etapa(
        run_id=run_id,
        query_id=query_id,
        stage="validacao",
        input_data={"tipo": "RAGResponse"},
    ) as observacao:
        resposta_dict = RAGResponse.model_validate(
            resposta_dict
        ).model_dump()

        observacao["output"] = {
            "valido": True,
            "is_refusal": resposta_dict.get(
                "is_refusal",
                False,
            ),
            "quantidade_fontes": len(
                resposta_dict.get("sources_used", [])
            ),
        }

    _notificar_progresso(
        on_progress,
        1.0,
        "Consulta concluída.",
    )

    evidencias = _formatar_evidencias(
        recuperacao.get("evidences", [])
    )
    fontes_recuperadas = sorted({
        evidencia["fonte"]
        for evidencia in evidencias
        if evidencia.get("fonte")
    })

    # Uma fonte recuperada não é automaticamente uma fonte citada.
    citacoes = re.findall(
        r"\[Fonte:\s*([^\]]+)\]",
        resposta_dict["answer"],
        flags=re.IGNORECASE,
    )
    citacoes = {citacao.strip() for citacao in citacoes}

    fontes_citadas = sorted({
        evidencia["fonte"]
        for evidencia in evidencias
        if evidencia.get("fonte")
        and (
            evidencia["fonte"] in citacoes
            or evidencia.get("chunk_id") in citacoes
        )
    })

    resultado = {
        "answer": resposta_dict["answer"],
        "query": pergunta,
        "query_id": query_id,
        "run_id": run_id,
        "executado": True,
        "estrategia": "recuperacao_hibrida",
        "plano": plano,
        "routes": consulta.get("routes", []),
        "filters": consulta.get("filters", {}),
        "evidences": evidencias,
        "fontes": fontes_recuperadas,
        "fontes_recuperadas": fontes_recuperadas,
        "fontes_citadas": fontes_citadas,
        "is_refusal": resposta_dict.get("is_refusal", False),
        "refusal_reason": resposta_dict.get("refusal_reason"),
        "generation_available": True,
        "latency_ms": round(
            (time.perf_counter() - inicio) * 1000,
            2,
        ),
        "confidence_level": resposta_dict.get(
            "confidence_level",
            "baixa",
        ),
        "tokens": resposta_dict.get("tokens", {}),
        "modelo": resposta_dict.get("modelo"),
        "retrieval_summary": recuperacao.get(
            "retrieval_summary",
            {},
        ),
        "fetch_k": fetch_k,
        "top_k": top_k,
    }

    if combinada:
        return preparar_combinado(consulta, resultado)

    return resultado


def executar_para_interface(
    pergunta: str,
    top_k: int,
    progress=gr.Progress(),
):
    """Compatibilidade com consumidores dos cinco campos anteriores."""
    try:
        resultado = executar_pipeline(
            pergunta,
            top_k,
            on_progress=lambda valor, texto: progress(
                valor,
                desc=texto,
            ),
        )

        return (
            resultado["answer"],
            ", ".join(resultado.get("routes", [])),
            resultado.get("filters", {}),
            resultado.get("evidences", []),
            status_consulta(resultado),
        )

    except Exception as erro:
        return (
            f"Não foi possível concluir a consulta: {erro}",
            "Erro",
            {},
            [],
            "**Status:** falha na execução",
        )
