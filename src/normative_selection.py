"""Cobertura de definição em perguntas normativas gerais."""

import re

from src.document_scope import normalizar


def cobrir_definicao(pergunta, ranking, chunks_por_id, rotas, top_k):
    """Reserva uma vaga, sem alterar scores nem acrescentar candidatos."""
    if set(rotas) != {"normativa"} or top_k < 2:
        return ranking

    texto = normalizar(pergunta)
    if re.search(r"\b(?:artigo|art\.|arts\.)\s*\d+", texto):
        return ranking

    pedido = re.fullmatch(
        r"o que .+ estabelece sobre "
        r"(?:(?:o|a|os|as)\s+)?([a-z]+(?:\s+[a-z]+){0,4})[?. ]*",
        texto,
    )
    if not pedido:
        return ranking

    assunto = pedido.group(1).strip()
    padrao = re.compile(
        r"(?<!\w)" + re.escape(assunto) + r"\s*:"
    )

    definicao = next(
        (
            item for item in ranking
            if padrao.search(normalizar(
                chunks_por_id.get(item["chunk_id"], {}).get("text", "")
            ))
        ),
        None,
    )
    if definicao is None:
        return ranking

    selecionados = ranking[:top_k]
    if any(
        item["chunk_id"] == definicao["chunk_id"]
        for item in selecionados
    ):
        return ranking

    ids = {
        item["chunk_id"] for item in ranking[:top_k - 1]
    } | {definicao["chunk_id"]}

    # Mantém a ordem relativa dentro de cada grupo.
    return (
        [item for item in ranking if item["chunk_id"] in ids]
        + [item for item in ranking if item["chunk_id"] not in ids]
    )
