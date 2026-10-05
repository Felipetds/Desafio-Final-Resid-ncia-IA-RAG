"""Consulta determinística aos registros normalizados do PNCP."""

import json
import unicodedata
from decimal import Decimal, InvalidOperation
from pathlib import Path

CAMINHO_BASE = Path("data/processed/base_estruturada_normalizada.json")

CAMPOS = {
    "id_pncp", "orgao", "municipio", "uf", "objeto",
    "modalidade", "ano_compra", "data_publicacao",
    "valor_estimado", "valor_homologado", "fornecedor",
    "fonte_original",
}

FILTROS = {
    "uf", "municipio", "orgao", "modalidade", "fornecedor",
    "ano_compra", "objeto_termos",
    "valor_minimo", "valor_maximo",
}

CAMPOS_PADRAO = ["id_pncp", "orgao", "objeto"]


def normalizar_texto(valor):
    texto = unicodedata.normalize("NFKD", str(valor or ""))
    return " ".join(
        "".join(c for c in texto if not unicodedata.combining(c))
        .casefold().split()
    )


def converter_numero(valor):
    """Aceita números JSON e textos brasileiros; ausência não vira zero."""
    if valor is None or isinstance(valor, bool):
        return None

    texto = str(valor).strip().replace("R$", "").replace(" ", "")
    if not texto:
        return None

    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")

    try:
        numero = Decimal(texto)
        return numero if numero.is_finite() else None
    except InvalidOperation:
        return None


def carregar_base(caminho=CAMINHO_BASE):
    caminho = Path(caminho)
    if not caminho.is_file():
        raise FileNotFoundError(f"Base normalizada ausente: {caminho}")

    base = json.loads(caminho.read_text(encoding="utf-8"))
    if not isinstance(base, list):
        raise ValueError("A base precisa ser uma lista de registros.")

    validar_base(base)
    return base


def validar_base(base):
    ids = []
    for registro in base:
        if not isinstance(registro, dict):
            raise ValueError("Registro inválido na base.")

        identificador = registro.get("id_pncp")
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("Registro sem ID PNCP válido.")
        ids.append(identificador)

    if len(ids) != len(set(ids)):
        raise ValueError("A base possui IDs PNCP duplicados.")


def consultar_registros(
    base,
    operacao="contar",
    filtros=None,
    campos=None,
    pagina=1,
    tamanho_pagina=20,
    campo_valor=None,
    minimo_inclusivo=True,
    maximo_inclusivo=True,
    criterio_objeto=None,
):
    """
    Consulta toda a base e pagina apenas a apresentação.

    objeto_termos usa correspondência textual OU no objeto.
    Não é classificação semântica de tecnologia.
    Limites podem ser inclusivos ou estritos.
    """
    validar_base(base)

    if operacao not in {"contar", "listar"}:
        raise ValueError("Operação suportada: contar ou listar.")

    if (
        type(pagina) is not int or pagina < 1
        or type(tamanho_pagina) is not int
        or not 1 <= tamanho_pagina <= 100
    ):
        raise ValueError("Página positiva e tamanho entre 1 e 100.")

    if not isinstance(minimo_inclusivo, bool) or not isinstance(
        maximo_inclusivo, bool
    ):
        raise ValueError("Inclusividade dos limites deve ser booleana.")

    filtros = dict(filtros or {})
    desconhecidos = set(filtros) - FILTROS
    if desconhecidos:
        raise ValueError(
            f"Filtros não suportados: {sorted(desconhecidos)}. "
            "Não serão ignorados silenciosamente."
        )

    campos = list(CAMPOS_PADRAO if campos is None else campos)
    if not campos or set(campos) - CAMPOS:
        raise ValueError("Campos solicitados inválidos ou vazios.")
    campos = list(dict.fromkeys(campos))

    termos = filtros.get("objeto_termos") or []
    if not isinstance(termos, list) or any(
        not isinstance(t, str) or not t.strip() for t in termos
    ):
        raise ValueError("objeto_termos deve ser uma lista de termos.")

    if termos and not criterio_objeto:
        raise ValueError("Informe a descrição do critério usado no objeto.")

    limites = {}
    for nome in ("valor_minimo", "valor_maximo"):
        bruto = filtros.get(nome)
        numero = converter_numero(bruto)
        if bruto is not None and numero is None:
            raise ValueError(f"Limite numérico inválido: {nome}")
        limites[nome] = numero

    minimo = limites["valor_minimo"]
    maximo = limites["valor_maximo"]

    if minimo is not None and maximo is not None and minimo > maximo:
        raise ValueError("Valor mínimo superior ao máximo.")

    tem_limite = minimo is not None or maximo is not None
    if tem_limite and campo_valor not in {
        "valor_estimado", "valor_homologado"
    }:
        raise ValueError(
            "Escolha valor_estimado ou valor_homologado para filtrar."
        )

    ano = filtros.get("ano_compra")
    if ano is not None:
        texto_ano = str(ano)
        if len(texto_ano) != 4 or not texto_ano.isdigit():
            raise ValueError("Ano da compra deve possuir quatro dígitos.")

    selecionados = []

    for registro in base:
        atende = True

        for campo in (
            "uf", "municipio", "orgao", "modalidade", "fornecedor"
        ):
            esperado = filtros.get(campo)
            if esperado is not None:
                existente = normalizar_texto(registro.get(campo))
                if not existente or existente != normalizar_texto(esperado):
                    atende = False
                    break

        if not atende:
            continue

        if ano is not None and str(registro.get("ano_compra")) != str(ano):
            continue

        objeto = normalizar_texto(registro.get("objeto"))
        if termos and not any(normalizar_texto(t) in objeto for t in termos):
            continue

        if tem_limite:
            valor = converter_numero(registro.get(campo_valor))
            if valor is None:
                continue

            if minimo is not None:
                if valor < minimo or (
                    valor == minimo and not minimo_inclusivo
                ):
                    continue

            if maximo is not None:
                if valor > maximo or (
                    valor == maximo and not maximo_inclusivo
                ):
                    continue

        selecionados.append(registro)

    selecionados.sort(key=lambda r: r["id_pncp"])
    total = len(selecionados)
    total_paginas = (
        (total + tamanho_pagina - 1) // tamanho_pagina
        if operacao == "listar" else 0
    )

    inicio = (pagina - 1) * tamanho_pagina
    apresentados = (
        selecionados[inicio:inicio + tamanho_pagina]
        if operacao == "listar" else []
    )

    return {
        "estrategia": "consulta_estruturada",
        "operacao": operacao,
        "filtros_aplicados": filtros,
        "campo_valor": campo_valor if tem_limite else None,
        "minimo_inclusivo": minimo_inclusivo,
        "maximo_inclusivo": maximo_inclusivo,
        "criterio_objeto": criterio_objeto,
        "total_base": len(base),
        "total": total,
        "campos": campos if operacao == "listar" else [],
        "registros": [
            {campo: registro.get(campo) for campo in campos}
            for registro in apresentados
        ],
        "referencias": [
            {
                "id_pncp": registro["id_pncp"],
                "fonte": registro.get("fonte_original"),
            }
            for registro in apresentados
        ],
        "fontes": sorted({
            str(r["fonte_original"])
            for r in selecionados if r.get("fonte_original")
        }),
        "pagina": pagina if operacao == "listar" else None,
        "tamanho_pagina": tamanho_pagina if operacao == "listar" else None,
        "total_paginas": total_paginas,
        "observacao": (
            "Resultado restrito aos registros fornecidos. "
            "Ano da compra não representa ano de publicação."
        ),
    }
