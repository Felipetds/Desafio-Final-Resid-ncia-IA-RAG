import time
from typing import Any, Dict, List

from src.generate import GENERATION_MODEL, gerar_resposta
from src.obs import (
    novo_query_id,
    novo_run_id,
    observar_etapa,
    registrar_evento,
)
from src.retrieve import recuperar_evidencias
from src.schema import RAGResponse


def _converter_dict(valor: Any) -> Dict[str, Any]:
    """
    Converte modelos Pydantic ou dicionários para dicionário.
    """
    if isinstance(valor, dict):
        return valor

    if hasattr(valor, "model_dump"):
        return valor.model_dump()

    if hasattr(valor, "dict"):
        return valor.dict()

    raise TypeError(
        f"Não foi possível converter {type(valor).__name__} para dicionário."
    )


def _formatar_evidencias(
    evidencias: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Seleciona os campos apresentados na interface.
    """
    evidencias_formatadas = []

    for posicao, evidencia in enumerate(evidencias, start=1):
        evidencias_formatadas.append(
            {
                "posição": posicao,
                "chunk_id": evidencia.get("chunk_id"),
                "trecho": evidencia.get("text", ""),
                "fonte": evidencia.get("source_file"),
                "tipo_documento": evidencia.get("doc_type"),
                "base": evidencia.get("base_id"),
                "natureza": evidencia.get("natureza"),
                "score_rrf": evidencia.get("rrf_score"),
                "métodos": evidencia.get(
                    "retrieval_sources",
                    [],
                ),
            }
        )

    return evidencias_formatadas


def executar_pipeline(
    pergunta: str,
    top_k: int = 5,
) -> Dict[str, Any]:
    """
    Executa recuperação, geração, validação e observabilidade.
    """
    pergunta = pergunta.strip()

    if not pergunta:
        raise ValueError(
            "Digite uma pergunta antes de executar a consulta."
        )

    run_id = novo_run_id()
    query_id_temporario = novo_query_id()
    inicio_pipeline = time.perf_counter()

    # Recuperação
    inicio_recuperacao = time.perf_counter()

    try:
        recuperacao = recuperar_evidencias(
            pergunta=pergunta,
            top_k=int(top_k),
            run_id=run_id,
        )

        query_id = recuperacao.get(
            "query_id",
            query_id_temporario,
        )

        registrar_evento(
            run_id=run_id,
            query_id=query_id,
            stage="fusao_rrf",
            status="ok",
            latencia_ms=(
                time.perf_counter() - inicio_recuperacao
            ) * 1000,
            input_data=pergunta,
            output_data={
                "rotas": recuperacao.get("routes", []),
                "quantidade_evidencias": len(
                    recuperacao.get("evidences", [])
                ),
                "recusa": recuperacao.get(
                    "is_refusal",
                    False,
                ),
            },
            tokens=None,
            modelo=None,
            extra={
                "filtros": recuperacao.get("filters", {}),
                "top_k": int(top_k),
                "resumo": recuperacao.get(
                    "retrieval_summary",
                    {},
                ),
            },
        )

    except Exception as erro:
        registrar_evento(
            run_id=run_id,
            query_id=query_id_temporario,
            stage="fusao_rrf",
            status="erro",
            latencia_ms=(
                time.perf_counter() - inicio_recuperacao
            ) * 1000,
            input_data=pergunta,
            output_data={
                "erro": type(erro).__name__,
                "mensagem": str(erro),
            },
            tokens=None,
            modelo=None,
            extra={"top_k": int(top_k)},
        )
        raise

    # Geração
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
            "rotas": recuperacao.get("routes", []),
        },
    ) as observacao:
        resposta_modelo = gerar_resposta(
            resultado_recuperacao=recuperacao,
        )

        resposta_dict = _converter_dict(
            resposta_modelo
        )

        observacao["output"] = {
            "resposta_gerada": bool(
                resposta_dict.get("answer")
            ),
            "nivel_confianca": resposta_dict.get(
                "confidence_level"
            ),
            "quantidade_fontes": len(
                resposta_dict.get("sources_used", [])
            ),
            "recusa": resposta_dict.get(
                "is_refusal",
                False,
            ),
        }

        observacao["tokens"] = resposta_dict.get(
            "tokens",
            {},
        )

    # Validação final pelo schema
    with observar_etapa(
        run_id=run_id,
        query_id=query_id,
        stage="validacao",
        input_data={
            "tipo": "RAGResponse",
        },
        modelo=None,
        extra={},
    ) as observacao:
        resposta_validada = RAGResponse.model_validate(
            resposta_dict
        )

        resposta_dict = resposta_validada.model_dump()

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

    latencia_total = round(
        (time.perf_counter() - inicio_pipeline) * 1000,
        2,
    )

    fontes = resposta_dict.get("sources_used", [])

    return {
        "answer": resposta_dict["answer"],
        "routes": recuperacao.get("routes", []),
        "filters": recuperacao.get("filters", {}),
        "evidences": _formatar_evidencias(fontes),
        "is_refusal": resposta_dict.get(
            "is_refusal",
            False,
        ),
        "refusal_reason": resposta_dict.get(
            "refusal_reason"
        ),
        "generation_available": True,
        "query_id": query_id,
        "run_id": run_id,
        "latency_ms": latencia_total,
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
    }


def executar_para_interface(
    pergunta: str,
    top_k: int,
):
    """
    Converte a saída do pipeline para os componentes do Gradio.
    """
    try:
        resultado = executar_pipeline(
            pergunta=pergunta,
            top_k=int(top_k),
        )

        rotas = resultado.get("routes", [])

        rotas_texto = (
            ", ".join(rotas)
            if rotas
            else "Nenhuma rota selecionada"
        )

        if resultado.get("is_refusal"):
            modo = "Consulta recusada pelos guardrails"
        else:
            modo = "Pipeline integrado"

        tokens = resultado.get("tokens", {})

        status = (
            f"**Modo:** {modo}  \n"
            f"**Run ID:** {resultado.get('run_id')}  \n"
            f"**Query ID:** {resultado.get('query_id')}  \n"
            f"**Confiança:** "
            f"{resultado.get('confidence_level', 'baixa')}  \n"
            f"**Latência total:** "
            f"{resultado.get('latency_ms')} ms  \n"
            f"**Tokens:** "
            f"{tokens.get('total', 0)}"
        )

        return (
            resultado["answer"],
            rotas_texto,
            resultado.get("filters", {}),
            resultado.get("evidences", []),
            status,
        )

    except FileNotFoundError:
        return (
            (
                "### Base de consulta indisponível\n\n"
                "Os artefatos de ingestão e indexação ainda não "
                "estão disponíveis neste ambiente. Execute primeiro "
                "as etapas de ingestão e indexação."
            ),
            "Indisponível",
            {},
            [],
            "**Status:** aguardando preparação da base",
        )

    except Exception as erro:
        return (
            f"### Erro ao executar a consulta\n\n`{erro}`",
            "Erro",
            {},
            [],
            "**Status:** falha na execução",
        )
