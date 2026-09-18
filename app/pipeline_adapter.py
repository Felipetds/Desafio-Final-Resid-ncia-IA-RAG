import json
from typing import Any, Dict, List

from src.retrieve import recuperar_evidencias


def _formatar_evidencias(
    evidencias: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Seleciona os campos que serão apresentados ao usuário.
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
                "métodos": evidencia.get("retrieval_sources", []),
            }
        )

    return evidencias_formatadas


def _resposta_provisoria(
    resultado_recuperacao: Dict[str, Any],
) -> str:
    """
    Produz uma mensagem temporária enquanto generate.py não está disponível.

    Esta função não gera uma resposta final e não apresenta inferências
    que não estejam nas evidências.
    """
    evidencias = resultado_recuperacao.get("evidences", [])

    if not evidencias:
        return (
            "Nenhuma evidência foi encontrada nas bases atualmente "
            "disponíveis. O roteamento foi executado, mas o corpus desta "
            "rota pode ainda não ter sido integrado."
        )

    trechos = []

    for posicao, evidencia in enumerate(evidencias[:3], start=1):
        texto = evidencia.get("text", "").strip()
        fonte = evidencia.get("source_file") or "fonte não informada"

        trechos.append(
            f"**Evidência {posicao} — {fonte}:**\n\n{texto}"
        )

    return (
        "### Resultado provisório da recuperação\n\n"
        "O módulo de geração ainda não está disponível. "
        "Abaixo estão as evidências recuperadas pelo pipeline:\n\n"
        + "\n\n".join(trechos)
    )


def _executar_geracao(
    pergunta: str,
    resultado_recuperacao: Dict[str, Any],
) -> Dict[str, Any] | None:
    """
    Tenta executar generate.py quando o módulo estiver disponível.

    Contrato provisório esperado:

        gerar_resposta(pergunta=..., evidencias=...)

    A integração poderá ser ajustada quando Felipe e Calvin definirem
    o contrato final de generate.py.
    """
    try:
        from src.generate import gerar_resposta
    except (ImportError, ModuleNotFoundError):
        return None

    evidencias = resultado_recuperacao.get("evidences", [])

    try:
        resultado = gerar_resposta(
            pergunta=pergunta,
            evidencias=evidencias,
        )
    except TypeError:
        # O módulo existe, mas seu contrato ainda não é compatível.
        return None

    if isinstance(resultado, str):
        return {
            "answer": resultado,
            "sources_used": [],
            "is_refusal": False,
            "refusal_reason": None,
        }

    if isinstance(resultado, dict):
        return resultado

    return None


def executar_pipeline(
    pergunta: str,
    top_k: int = 5,
) -> Dict[str, Any]:
    """
    Executa o fluxo disponível e devolve um contrato estável para a interface.
    """
    pergunta = pergunta.strip()

    if not pergunta:
        raise ValueError("Digite uma pergunta antes de executar a consulta.")

    recuperacao = recuperar_evidencias(
        pergunta=pergunta,
        top_k=top_k,
    )

    rotas = recuperacao.get("routes", [])
    filtros = recuperacao.get("filters", {})
    evidencias = recuperacao.get("evidences", [])

    if recuperacao.get("is_refusal", False):
        motivo = recuperacao.get("refusal_reason")
        resposta = (
            "### Solicitação não atendida\n\n"
            + (
                motivo
                or "A consulta não pode ser respondida pelas regras de segurança."
            )
        )

        return {
            "answer": resposta,
            "routes": rotas,
            "filters": filtros,
            "evidences": [],
            "is_refusal": True,
            "generation_available": False,
            "query_id": recuperacao.get("query_id"),
            "latency_ms": recuperacao.get("latencia_ms"),
        }

    geracao = _executar_geracao(
        pergunta=pergunta,
        resultado_recuperacao=recuperacao,
    )

    if geracao is not None:
        resposta = geracao.get(
            "answer",
            "O módulo de geração não retornou uma resposta.",
        )
        geracao_disponivel = True
    else:
        resposta = _resposta_provisoria(recuperacao)
        geracao_disponivel = False

    return {
        "answer": resposta,
        "routes": rotas,
        "filters": filtros,
        "evidences": _formatar_evidencias(evidencias),
        "is_refusal": False,
        "generation_available": geracao_disponivel,
        "query_id": recuperacao.get("query_id"),
        "latency_ms": recuperacao.get("latencia_ms"),
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
    Converte a saída do pipeline para os componentes visuais.
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

        modo = (
            "Geração integrada"
            if resultado.get("generation_available")
            else "Modo provisório: somente recuperação"
        )

        if resultado.get("is_refusal"):
            modo = "Consulta recusada pelos guardrails"

        status = (
            f"**Modo:** {modo}  \n"
            f"**Query ID:** {resultado.get('query_id', 'não informado')}  \n"
            f"**Latência:** {resultado.get('latency_ms', 'não informada')} ms"
        )

        return (
            resultado["answer"],
            rotas_texto,
            resultado.get("filters", {}),
            resultado.get("evidences", []),
            status,
        )

    except Exception as erro:
        return (
            f"### Erro ao executar a consulta\n\n`{erro}`",
            "Erro",
            {},
            [],
            "**Status:** falha na execução",
        )
