"""Decomposição limitada de consultas estruturadas e normativas."""

import re


def extrair_pedido_documental(pergunta):
    """Reconhece uma forma explícita; não divide conjunções arbitrárias."""
    encontrado = re.fullmatch(
        r"\s*Quantas\s+contratações\s+têm\s+ano\s+da\s+compra"
        r"\s+\d{4}\s+e\s+"
        r"(?P<documental>o\s+que\s+a\s+Lei\b.+)",
        pergunta,
        flags=re.IGNORECASE,
    )
    return encontrado.group("documental").strip() if encontrado else None
