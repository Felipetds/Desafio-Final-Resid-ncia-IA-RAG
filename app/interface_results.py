"""Apresentação dos resultados e contexto da consulta exibida."""

from copy import deepcopy
import json
import time


def preparar_estruturado(resultado, *, latencia_ms=None):
    saida = deepcopy(resultado)

    saida.update({
        "filters": resultado.get("filtros_aplicados", {}),
        "routes": ["estruturada"],
        "fontes_estruturadas": list(resultado.get("fontes", [])),
        "evidences": [],
        "tokens": {},
        "executado": True,
        "latency_ms": (
            latencia_ms
            if latencia_ms is not None
            else resultado.get("latencia_ms", 0)
        ),
    })

    total = resultado["total"]
    total_formatado = f"{total:,}".replace(",", ".")
    filtros = json.dumps(
        resultado.get("filtros_aplicados", {}),
        ensure_ascii=False,
    )

    partes = [
        f"**Total de correspondências: {total_formatado}**",
        (
            f"**Recorte:** {resultado['total_base']} registros "
            "disponíveis na base carregada."
        ),
        f"**Filtros aplicados:** `{filtros}`",
    ]

    if resultado.get("criterio_objeto"):
        partes.append(
            f"**Critério do objeto:** {resultado['criterio_objeto']}"
        )

    if resultado.get("campo_valor"):
        minimo = (
            "inclusivo"
            if resultado.get("minimo_inclusivo", True)
            else "estrito"
        )
        maximo = (
            "inclusivo"
            if resultado.get("maximo_inclusivo", True)
            else "estrito"
        )

        partes.append(
            f"**Campo de valor:** {resultado['campo_valor']}. "
            f"Limite mínimo {minimo}; máximo {maximo}."
        )

    if resultado["operacao"] == "listar" and total:
        partes.append(
            f"**Página:** {resultado['pagina']} de "
            f"{resultado['total_paginas']} — "
            f"{len(resultado['registros'])} registros exibidos."
        )

    fontes = resultado.get("fontes", [])

    partes.append(
        "**Fontes correspondentes:** "
        + ("; ".join(fontes) if fontes else "Nenhuma correspondência.")
    )

    if resultado.get("fonte_data_publicacao"):
        partes.append(
            "**Campo utilizado para publicação:** "
            f"`{resultado['fonte_data_publicacao']}`"
        )

    if resultado.get("observacao"):
        partes.append(resultado["observacao"])

    saida["answer"] = "\n\n".join(partes)
    return saida


def status_consulta(resultado):
    if resultado.get("is_refusal"):
        modo = "Consulta recusada"
    elif resultado.get("necessita_esclarecimento"):
        modo = "Esclarecimento necessário"
    elif resultado.get("estrategia") == "combinada":
        modo = "Consulta combinada: cálculo estruturado e documentos"
    elif resultado.get("estrategia") == "consulta_estruturada":
        modo = "Consulta estruturada calculada sobre a base"
    else:
        modo = "Consulta documental com recuperação híbrida"

    partes = [
        f"**Modo:** {modo}",
        f"**Run ID:** {resultado.get('run_id', '')}",
        f"**Query ID:** {resultado.get('query_id', '')}",
        (
            "**Latência desta execução:** "
            f"{resultado.get('latency_ms', 0)} ms"
        ),
    ]

    if resultado.get("estrategia") in {
        "recuperacao_hibrida", "combinada"
    }:
        partes.extend([
            (
                "**Confiança:** "
                f"{resultado.get('confidence_level', 'baixa')}"
            ),
            (
                "**Tokens de geração:** "
                f"{resultado.get('tokens', {}).get('total', 0)}"
            ),
            f"**Evidências solicitadas:** {resultado.get('top_k')}",
            f"**Candidatos por busca:** {resultado.get('fetch_k')}",
        ])

    if resultado.get("paginacao_run_id"):
        partes.extend([
            "**Documentos:** mantidos da consulta original.",
            f"**Run ID da paginação:** {resultado['paginacao_run_id']}",
            (
                "**Latência da paginação:** "
                f"{resultado['paginacao_latency_ms']} ms"
            ),
        ])

    return "\n\n".join(partes)


def tabela_consulta(resultado):
    campos = resultado.get("campos", [])

    return {
        "headers": campos,
        "data": [
            [registro.get(campo) for campo in campos]
            for registro in resultado.get("registros", [])
        ],
    }


def feedback_da_consulta(resultado, avaliacao, comentario):
    if (
        not resultado
        or not resultado.get("query_id")
        or not resultado.get("run_id")
    ):
        return "Faça uma consulta antes de enviar o feedback."

    from app.feedback_store import registrar_feedback

    evidencias = [
        *resultado.get("evidences", []),
        *[
            {"fonte": fonte}
            for fonte in resultado.get("fontes", [])
        ],
    ]

    return registrar_feedback(
        pergunta=resultado.get("query", ""),
        avaliacao=avaliacao,
        comentario=comentario,
        rota=", ".join(resultado.get("routes", [])),
        evidencias=evidencias,
        status=status_consulta(resultado),
    )


def mudar_pagina(resultado, direcao, *, executor=None):
    if not resultado or resultado.get("operacao") != "listar":
        raise ValueError(
            "Faça uma consulta de listagem antes de navegar."
        )

    if direcao not in (-1, 1):
        raise ValueError("Direção inválida.")

    pagina = resultado["pagina"] + direcao

    if not 1 <= pagina <= resultado["total_paginas"]:
        return deepcopy(resultado)

    from src.obs import novo_run_id

    if executor is None:
        from src.query_executor import executar_plano
        executor = executar_plano

    plano = deepcopy(resultado["plano"])
    plano["pagina"] = pagina
    plano["query_id"] = resultado["query_id"]

    combinada = resultado.get("estrategia") == "combinada"

    if combinada:
        plano["estrategia"] = "consulta_estruturada"
        plano["bases"] = ["estruturada"]

    inicio = time.perf_counter()

    nova = executor(
        resultado["query"],
        plano,
        run_id=novo_run_id(),
    )

    if (
        nova["total"] != resultado["total"]
        or nova["total_base"] != resultado["total_base"]
    ):
        raise ValueError(
            "A base mudou. Execute a consulta novamente "
            "antes de navegar."
        )

    nova.update({
        "plano": plano,
        "executado": True,
    })

    latencia = round(
        (time.perf_counter() - inicio) * 1000, 2
    )

    if combinada:
        consulta = {
            "estruturada": nova,
            "plano": {
                **deepcopy(resultado["plano"]),
                "pagina": pagina,
            },
            "routes": resultado.get("routes", []),
        }
        documental = deepcopy(resultado)
        documental["answer"] = resultado["resposta_documental"]

        saida = preparar_combinado(consulta, documental)
        saida["paginacao_run_id"] = nova.get("run_id")
        saida["paginacao_latency_ms"] = latencia
        return saida

    return preparar_estruturado(nova, latencia_ms=latencia)


def preparar_combinado(consulta, documental):
    """Preserva os cálculos e apresenta a resposta documental separadamente."""
    estruturado = preparar_estruturado(consulta["estruturada"])
    saida = deepcopy(documental)

    # Copia somente os campos da consulta estruturada usados na apresentação.
    for campo in (
        "operacao", "total", "total_base", "registros", "campos",
        "referencias", "pagina", "tamanho_pagina", "total_paginas",
        "filtros_aplicados", "campo_valor", "minimo_inclusivo",
        "maximo_inclusivo", "criterio_objeto", "fonte_data_publicacao",
        "observacao",
    ):
        if campo in estruturado:
            saida[campo] = deepcopy(estruturado[campo])

    fontes_estruturadas = estruturado.get("fontes", [])
    saida.update({
        "estrategia": "combinada",
        "plano": deepcopy(consulta["plano"]),
        "routes": consulta.get("routes", []),
        "filters": estruturado.get("filters", {}),
        "estruturada": deepcopy(consulta["estruturada"]),
        "fontes_estruturadas": fontes_estruturadas,
        "fontes": sorted(set(
            fontes_estruturadas + documental.get("fontes", [])
        )),
        "resposta_documental": documental.get("answer", ""),
        "documental_query_id": documental.get("query_id"),
        "documental_run_id": documental.get("run_id"),
    })

    saida["answer"] = (
        "**Resultado calculado sobre a base estruturada**\n\n"
        + estruturado["answer"]
        + "\n\n**Resposta baseada nos documentos recuperados**\n\n"
        + documental.get("answer", "")
    )
    return saida
