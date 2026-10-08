"""Validação de trechos literais vinculados aos chunks recuperados."""

import json
import re


def _normalizar_espacos(texto):
    return re.sub(r"\s+", " ", texto).strip()


def preparar_resposta_extrativa(conteudo, evidencias):
    """Aceita somente trechos presentes no chunk indicado.

    Verifica correspondência textual, não relevância ou completude.
    Não apresenta comentários livres produzidos pelo modelo.
    """
    try:
        dados = json.loads(conteudo)
    except (TypeError, ValueError) as erro:
        raise ValueError("Resposta extrativa não contém JSON válido.") from erro

    if not isinstance(dados, dict) or set(dados) != {"trechos"}:
        raise ValueError("Formato da resposta extrativa inválido.")

    trechos = dados["trechos"]
    if not isinstance(trechos, list) or not 1 <= len(trechos) <= 5:
        raise ValueError("Informe entre um e cinco trechos.")

    por_id = {}
    for evidencia in evidencias:
        if evidencia.chunk_id in por_id:
            raise ValueError("Há IDs de evidência duplicados.")
        por_id[evidencia.chunk_id] = evidencia

    partes = []
    fontes = []
    vistos = set()

    for item in trechos:
        if not isinstance(item, dict) or set(item) != {"chunk_id", "trecho"}:
            raise ValueError("Formato de trecho inválido.")

        identificador = item["chunk_id"]
        trecho = item["trecho"]

        if not isinstance(identificador, str) or identificador not in por_id:
            raise ValueError("Chunk citado não foi recuperado.")

        if not isinstance(trecho, str) or not trecho.strip():
            raise ValueError("Trecho vazio ou inválido.")

        evidencia = por_id[identificador]
        normalizado = _normalizar_espacos(trecho)

        if normalizado not in _normalizar_espacos(evidencia.text):
            raise ValueError("O trecho não está presente no chunk citado.")

        # Evita inserir marcações de citação dentro do trecho.
        if re.search(r"\[Fonte:", trecho, flags=re.IGNORECASE):
            raise ValueError("Trecho contém marcação de citação.")

        chave = (identificador, normalizado)
        if chave in vistos:
            continue
        vistos.add(chave)

        partes.append(
            f"> {normalizado}\n\n[Fonte: {identificador}]"
        )
        if identificador not in {fonte.chunk_id for fonte in fontes}:
            fontes.append(evidencia)

    resposta = (
        "Trechos das evidências recuperadas:\n\n"
        + "\n\n".join(partes)
    )
    return resposta, fontes


def preparar_selecao_extrativa(conteudo, evidencias):
    """Apresenta o texto original dos chunks selecionados pelo modelo."""
    try:
        dados = json.loads(conteudo)
    except (TypeError, ValueError) as erro:
        raise ValueError("Seleção não contém JSON válido.") from erro

    if not isinstance(dados, dict) or set(dados) != {"chunk_ids"}:
        raise ValueError("Formato de seleção inválido.")

    ids = dados["chunk_ids"]
    if not isinstance(ids, list) or not 1 <= len(ids) <= 5:
        raise ValueError("Selecione entre um e cinco chunks.")

    por_id = {}
    for evidencia in evidencias:
        if evidencia.chunk_id in por_id:
            raise ValueError("Há IDs de evidência duplicados.")
        por_id[evidencia.chunk_id] = evidencia

    trechos = []
    vistos = set()

    for identificador in ids:
        if not isinstance(identificador, str) or identificador not in por_id:
            raise ValueError("Chunk selecionado não foi recuperado.")
        if identificador in vistos:
            continue
        vistos.add(identificador)

        trechos.append({
            "chunk_id": identificador,
            "trecho": por_id[identificador].text,
        })

    return preparar_resposta_extrativa(
        json.dumps({"trechos": trechos}, ensure_ascii=False),
        evidencias,
    )
