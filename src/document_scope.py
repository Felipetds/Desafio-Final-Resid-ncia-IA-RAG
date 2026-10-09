"""Escopo de recuperação para atas explicitamente identificadas."""

import json
import re
import unicodedata


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", str(texto)).lower()
    texto = "".join(
        caractere for caractere in texto
        if not unicodedata.combining(caractere)
    )
    return re.sub(r"\s+", " ", texto).strip()


PADRAO_ATA = re.compile(
    r"\bata\s+"
    r"(?:(?:de\s+registro\s+de\s+precos)\s*[-–]?\s*)?"
    r"(?:(?:sei)\s*)?"
    r"(?:n(?:o|º|°|\.)?\s*)?"
    r"0*(\d+)\s*/\s*(20\d{2})(?!\d)"
)

PADRAO_PROCESSO = re.compile(
    r"\bprocesso(?:\s+administrativo)?\s*"
    r"(?:n[.\sº°o]*\s*)?"
    r"(\d{5}\s*\.\s*\d{6}\s*/\s*\d{4}\s*-\s*\d{2})"
)


def escopar_ata(pergunta, chunks_por_id, identificar_natureza):
    """Retorna None sem ata explícita, ou IDs elegíveis e sua justificativa.

    Documentos sem correspondência ou com identidade ambígua retornam
    conjunto vazio. Um vínculo estruturado exige processo exato.
    """
    pedido = PADRAO_ATA.search(normalizar(pergunta))
    if not pedido:
        return None

    identidade = tuple(int(valor) for valor in pedido.groups())
    documentos = {}

    for identificador, chunk in chunks_por_id.items():
        if identificar_natureza(chunk) != "conversacional":
            continue

        fonte = (chunk.get("metadata") or {}).get("source_file")
        if fonte:
            documentos.setdefault(fonte, []).append(
                (identificador, chunk)
            )

    fontes = []
    for fonte, paginas in documentos.items():
        identidades = {
            tuple(int(valor) for valor in achado.groups())
            for _, chunk in paginas
            for achado in PADRAO_ATA.finditer(
                normalizar(chunk.get("text", ""))
            )
        }
        if identidade in identidades:
            fontes.append(fonte)

    if len(fontes) != 1:
        return {
            "ids": set(),
            "fontes": sorted(fontes),
            "processos": [],
            "motivo": "Ata não localizada de forma unívoca.",
        }

    fonte = fontes[0]
    paginas = documentos[fonte]
    ids = {identificador for identificador, _ in paginas}

    processos = {
        re.sub(r"\D", "", achado.group(1))
        for _, chunk in paginas
        for achado in PADRAO_PROCESSO.finditer(
            normalizar(chunk.get("text", ""))
        )
    }

    for identificador, chunk in chunks_por_id.items():
        if identificar_natureza(chunk) != "estruturada":
            continue

        try:
            registro = json.loads(chunk.get("text", ""))
        except (TypeError, json.JSONDecodeError):
            continue

        if not isinstance(registro, dict):
            continue

        processo = re.sub(r"\D", "", str(registro.get("processo") or ""))
        if processo and processo in processos:
            ids.add(identificador)

    return {
        "ids": ids,
        "fontes": [fonte],
        "processos": sorted(processos),
        "motivo": "Ata identificada por número/ano; vínculo por processo exato.",
    }
