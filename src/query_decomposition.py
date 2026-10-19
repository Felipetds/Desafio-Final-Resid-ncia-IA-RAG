
"""Separação conservadora de um segundo pedido documental explícito."""

import re


def extrair_pedido_documental(pergunta):
    """Não interpreta filtros ou campos de listagem como tarefa documental."""
    for encontrado in re.finditer(
        r"(?:\s+e\s+|;\s*)"
        r"(?P<documental>"
        r"(?:o\s+que\b"
        r"|(?:informe|mostre|apresente)\s+o\s+que\b"
        r"|explique\b|descreva\b|resuma\b|esclare[cç]a\b)"
        r".+)$",
        pergunta,
        flags=re.IGNORECASE,
    ):
        documental = encontrado.group("documental").strip()
        if re.search(
            r"\b(?:lei|decretos?|resolu[cç][oõ]es?|resolu[cç][aã]o|portarias?|normas?|legisla[cç][aã]o|regras?|atas?"
            r"|comunica[cç][oõ]es|documentos?|discutid[oa]s?)\b",
            documental,
            flags=re.IGNORECASE,
        ):
            return documental
    return None
