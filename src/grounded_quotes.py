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




def _recortar_campos_ata(pergunta, evidencia):
    """Extrai campos literais em pedidos explícitos de objeto e PNCP."""
    from src.document_scope import normalizar

    original = evidencia.text
    consulta = normalizar(pergunta or "")
    if not (
        re.search(r"\bata\b", consulta)
        and re.search(r"\bobjeto\b", consulta)
        and re.search(r"\bpncp\b", consulta)
    ):
        return original

    texto = _normalizar_espacos(original)

    # JSON: mostra somente o campo solicitado, mantendo texto literal.
    if texto.startswith("{"):
        try:
            dados = json.loads(original)
        except (TypeError, ValueError):
            return original
        if not isinstance(dados, dict):
            return original
        valor = dados.get("numeroControlePNCP")
        if not isinstance(valor, str) or not valor.strip():
            return original
        campos = list(re.finditer(
            r'"numeroControlePNCP"\s*:\s*"[^"]+"', texto
        ))
        if len(campos) == 1:
            return campos[0].group(0)
        return original

    # Ata: mantém o objeto e o destinatário até a referência ao anexo.
    # Na ausência de limites reconhecidos, preserva o texto completo.
    objetos = list(re.finditer(
        r"\btem\s+por\s+objeto\b.+?"
        r"(?=,\s*conforme\s+especificado\b)",
        texto,
        flags=re.IGNORECASE,
    ))
    if len(objetos) == 1:
        return objetos[0].group(0)
    return original

def _recortar_definicao_normativa(pergunta, evidencia):
    """Recorta um inciso completo; preserva o original em caso de dúvida."""
    from src.document_scope import normalizar

    original = evidencia.text
    if not pergunta or getattr(evidencia, "natureza", None) != "normativa":
        return original

    consulta = normalizar(pergunta)
    if re.search(r"\b(?:artigo|art\.|arts\.)\s*\d+", consulta):
        return original

    pedido = re.fullmatch(
        r"o que .+ estabelece sobre "
        r"(?:(?:o|a|os|as)\s+)?"
        r"([a-z]+(?:\s+[a-z]+){0,4})[?. ]*",
        consulta,
    )
    if not pedido:
        return original

    texto = _normalizar_espacos(original)
    if not re.match(r"Art\.\s*6\s*[º°o]?", texto, re.IGNORECASE):
        return original

    # Inciso completo até o próximo inciso: não corta por caracteres.
    incisos = re.finditer(
        r"(?<!\w)[IVXLCDM]+\s*[-–—]\s*.*?"
        r"(?=\s+[IVXLCDM]+\s*[-–—]\s*|$)",
        texto,
    )
    assunto = pedido.group(1).strip()
    encontrados = []
    for inciso in incisos:
        trecho = inciso.group(0)
        definicao = re.sub(
            r"^[IVXLCDM]+\s*[-–—]\s*", "", trecho
        )
        if normalizar(definicao).startswith(assunto + ":"):
            encontrados.append(trecho)

    return encontrados[0] if len(encontrados) == 1 else original

def preparar_selecao_extrativa(conteudo, evidencias, *, pergunta=None):
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
            "trecho": (
                _recortar_campos_ata(pergunta, por_id[identificador])
                if _recortar_campos_ata(
                    pergunta, por_id[identificador]
                ) != por_id[identificador].text
                else _recortar_definicao_normativa(
                    pergunta, por_id[identificador]
                )
            ),
        })

    return preparar_resposta_extrativa(
        json.dumps({"trechos": trechos}, ensure_ascii=False),
        evidencias,
    )
