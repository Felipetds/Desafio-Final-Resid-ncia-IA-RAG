"""Executa um plano explícito de consulta."""

from typing import Any, Callable

from src.structured_query import (
    carregar_base,
    consultar_registros,
)


def executar_plano(
    pergunta: str,
    plano: dict[str, Any],
    *,
    base: list[dict[str, Any]] | None = None,
    top_k: int = 3,
    fetch_k: int = 50,
    client=None,
    recuperador: Callable | None = None,
    analise_pronta: dict[str, Any] | None = None,
    run_id: str | None = None,
) -> dict[str, Any]:
    if not isinstance(pergunta, str) or not pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")

    if not isinstance(plano, dict):
        raise ValueError("O plano deve ser um dicionário.")

    estrategia = plano.get("estrategia")

    if estrategia == "consulta_estruturada":
        if plano.get("bases") != ["estruturada"]:
            raise ValueError(
                "A consulta estruturada exige apenas a base estruturada."
            )

        operacao = plano.get("operacao")

        if operacao not in {"contar", "listar"}:
            raise ValueError("Operação estruturada inválida.")

        import time
        import uuid
        from src import obs

        run_id = run_id or obs.novo_run_id()
        query_id = (
            (analise_pronta or {}).get("query_id")
            or plano.get("query_id")
            or f"q_{uuid.uuid4().hex[:8]}"
        )

        inicio_execucao = time.perf_counter()

        with obs.observar_etapa(
            run_id=run_id,
            query_id=query_id,
            stage="consulta_estruturada",
            input_data={
                "operacao": operacao,
                "filtros": plano.get("filtros", {}),
                "campos": plano.get("campos"),
                "pagina": plano.get("pagina", 1),
                "tamanho_pagina": plano.get("tamanho_pagina", 20),
                "campo_valor": plano.get("campo_valor"),
                "minimo_inclusivo": plano.get("minimo_inclusivo", True),
                "maximo_inclusivo": plano.get("maximo_inclusivo", True),
                "criterio_objeto": plano.get("criterio_objeto"),
            },
        ) as observacao:
            registros = carregar_base() if base is None else base

            resultado = consultar_registros(
                registros,
                operacao=operacao,
                filtros=plano.get("filtros", {}),
                campos=plano.get("campos"),
                pagina=plano.get("pagina", 1),
                tamanho_pagina=plano.get("tamanho_pagina", 20),
                campo_valor=plano.get("campo_valor"),
                minimo_inclusivo=plano.get("minimo_inclusivo", True),
                maximo_inclusivo=plano.get("maximo_inclusivo", True),
                criterio_objeto=plano.get("criterio_objeto"),
            )

            observacao["output"] = {
                "operacao": resultado["operacao"],
                "filtros_aplicados": resultado["filtros_aplicados"],
                "total_base": resultado["total_base"],
                "total": resultado["total"],
                "pagina": resultado["pagina"],
                "tamanho_pagina": resultado["tamanho_pagina"],
                "total_paginas": resultado["total_paginas"],
                "quantidade_retornada": len(resultado["registros"]),
                "campos": resultado["campos"],
                "registros_sem_publicacao": resultado.get(
                    "registros_sem_publicacao", 0
                ),
            }

        return {
            **resultado,
            "query": pergunta.strip(),
            "query_id": query_id,
            "run_id": run_id,
            "routes": ["estruturada"],
            "latencia_ms": round(
                (time.perf_counter() - inicio_execucao) * 1000,
                2,
            ),
        }

    if estrategia == "recuperacao_hibrida":
        if plano.get("operacao") != "buscar":
            raise ValueError("A recuperação híbrida exige operação buscar.")

        if recuperador is None:
            from src.retrieve import recuperar_evidencias
            recuperador = recuperar_evidencias

        argumentos = {
            "pergunta": pergunta.strip(),
            "top_k": top_k,
            "fetch_k": fetch_k,
            "client": client,
        }

        if analise_pronta is not None:
            argumentos["analise_pronta"] = analise_pronta
        if run_id is not None:
            argumentos["run_id"] = run_id

        resultado = recuperador(**argumentos)

        return {
            **resultado,
            "estrategia": "recuperacao_hibrida",
            "operacao": "buscar",
        }

    raise ValueError(
        "Estratégia inválida. Use consulta_estruturada "
        "ou recuperacao_hibrida."
    )



def executar_consulta(
    pergunta,
    *,
    base=None,
    client=None,
    top_k=3,
    fetch_k=50,
    criterio_tecnologia=None,
    analise=None,
    recuperador=None,
    run_id=None,
):
    from src import obs
    from src.router import analisar_consulta, planejar_consulta

    if not isinstance(pergunta, str) or not pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")

    run_id = run_id or obs.novo_run_id()

    if analise is None:
        analise = analisar_consulta(
            pergunta,
            client=client,
            run_id=run_id,
        )

    plano = planejar_consulta(
        pergunta,
        client=client,
        run_id=run_id,
        criterio_tecnologia=criterio_tecnologia,
        analise=analise,
    )

    if plano["is_refusal"] or plano["necessita_esclarecimento"]:
        return {
            "query": pergunta,
            "query_id": plano.get("query_id"),
            "run_id": run_id,
            "plano": plano,
            "executado": False,
            "mensagem": (
                plano.get("refusal_reason")
                if plano["is_refusal"]
                else plano.get("pergunta_esclarecimento")
            ),
        }

    resultado = executar_plano(
        pergunta,
        plano,
        base=base,
        client=client,
        top_k=top_k,
        fetch_k=fetch_k,
        recuperador=recuperador,
        analise_pronta=analise,
        run_id=run_id,
    )

    if plano["estrategia"] == "consulta_estruturada":
        plano["query_id"] = resultado["query_id"]

    return {
        **resultado,
        "run_id": run_id,
        "plano": plano,
        "executado": True,
    }
