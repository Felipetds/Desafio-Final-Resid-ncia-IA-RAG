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

def cobrir_selecao_definicao(pergunta, conteudo, evidencias, rotas):
    """Inclui definição recuperada em perguntas gerais, com seleção validada."""
    import json
    from src.grounded_quotes import preparar_selecao_extrativa

    preparar_selecao_extrativa(conteudo, evidencias)
    selecionados = list(dict.fromkeys(json.loads(conteudo)["chunk_ids"]))

    if (
        set(rotas) != {"normativa"}
        or not all(e.natureza == "normativa" for e in evidencias)
    ):
        return conteudo

    texto = normalizar(pergunta)
    if re.search(r"\b(?:artigo|art\.|arts\.)\s*\d+", texto):
        return conteudo

    pedido = re.fullmatch(
        r"o que .+ estabelece sobre "
        r"(?:(?:o|a|os|as)\s+)?([a-z]+(?:\s+[a-z]+){0,4})[?. ]*",
        texto,
    )
    if not pedido:
        return conteudo

    padrao = re.compile(
        r"(?<!\w)" + re.escape(pedido.group(1).strip()) + r"\s*:"
    )

    # Mantém a escolha do modelo quando ele já selecionou uma definição.
    por_id = {e.chunk_id: e for e in evidencias}
    if any(
        padrao.search(normalizar(por_id[i].text))
        for i in selecionados
    ):
        return conteudo

    definicao = next(
        (e for e in evidencias if padrao.search(normalizar(e.text))),
        None,
    )
    if definicao is None:
        return conteudo

    # Reserva a última vaga quando o limite de cinco já foi atingido.
    ids = selecionados[:4] + [definicao.chunk_id]
    return json.dumps({"chunk_ids": ids}, ensure_ascii=False)
