"""
Validação final da frente do Luiz.

Como usar:
1) Salve este arquivo na RAIZ do repositório.
2) Ative a .venv.
3) Execute:
       python validar_entrega_luiz.py

O script NÃO altera o código do projeto.
Ele executa P02, P07, M01 offline e tenta:
- uma consulta combinada;
- uma busca de vidraçaria;
- uma consulta normativa.

Se o endpoint não responder, o caso online é registrado como BLOQUEIO/TIMEOUT,
sem ser tratado como aprovação.
"""

from __future__ import annotations

import json
import re
import time
import traceback
import unicodedata
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from openai import OpenAI

from src.query_executor import executar_consulta
from src.router import OLLAMA_URL


RAIZ = Path.cwd()
TOP_KS_OFFLINE = (1, 3)
TIMEOUT_ENDPOINT = 60.0

P02 = (
    "No PE 038/26/2026, quantos itens foram homologados, "
    "fracassados e desertos e qual foi a soma dos valores homologados?"
)

P07 = (
    "Quantos itens constam no Plano de Contratações Anual "
    "do Estado do Rio de Janeiro para 2026 "
    "e qual é o valor total estimado informado?"
)

M01 = (
    "Com base no PE 038/26/2026, informe quantos itens foram homologados, "
    "fracassados e desertos, calcule o valor total homologado e verifique "
    "se existe alguma informação relacionada a essa contratação nas demais "
    "naturezas de evidência disponíveis no corpus."
)

COMBINADA = (
    "Quantas contratações têm ano da compra 2026 "
    "e o que a Lei nº 14.133 estabelece sobre o pregão?"
)

VIDRACARIA = "Existe contratação para reparo de vidraça?"

NORMATIVA = "O que a Lei nº 14.133/2021 estabelece sobre o pregão?"


def analise(
    nome: str,
    pergunta: str,
    routes: list[str],
    filters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "query": pergunta,
        "query_id": f"q_validacao_{nome.lower()}",
        "routes": routes,
        "filters": filters or {},
        "is_refusal": False,
        "refusal_reason": None,
        "justification": "Análise fixa usada apenas na validação da entrega.",
    }


def decimal_igual(valor: Any, esperado: str) -> bool:
    try:
        return Decimal(str(valor)) == Decimal(esperado)
    except Exception:
        return False


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto or "")
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.casefold()


def evidencia_resumida(e: dict[str, Any]) -> dict[str, Any]:
    texto = e.get("text") or e.get("trecho") or ""
    return {
        "chunk_id": e.get("chunk_id"),
        "natureza": e.get("natureza"),
        "base_id": e.get("base_id"),
        "source_file": e.get("source_file") or e.get("fonte"),
        "rrf_score": e.get("rrf_score"),
        "rerank_score": e.get("rerank_score"),
        "texto_inicio": texto[:500],
    }


def imprimir_titulo(titulo: str) -> None:
    print("\n" + "=" * 88)
    print(titulo)
    print("=" * 88)


def executar_offline(nome: str, pergunta: str) -> list[dict[str, Any]]:
    resultados = []

    for top_k in TOP_KS_OFFLINE:
        inicio = time.perf_counter()
        try:
            resultado = executar_consulta(
                pergunta,
                analise=analise(
                    nome,
                    pergunta,
                    ["agregada"],
                    {"ano": 2026, "uf": "RJ"},
                ),
                top_k=top_k,
                run_id=f"run_validacao_{nome.lower()}_k{top_k}",
            )
            resultados.append(
                {
                    "top_k": top_k,
                    "status": "EXECUTADO",
                    "duracao_s": round(time.perf_counter() - inicio, 3),
                    "resultado": resultado,
                }
            )
        except Exception as erro:
            resultados.append(
                {
                    "top_k": top_k,
                    "status": "ERRO",
                    "duracao_s": round(time.perf_counter() - inicio, 3),
                    "erro": f"{type(erro).__name__}: {erro}",
                    "traceback": traceback.format_exc(),
                }
            )

    return resultados


def validar_p02(resultado: dict[str, Any]) -> list[str]:
    problemas = []
    esperado = {
        "itens_total": 19,
        "homologados": 8,
        "fracassados": 9,
        "desertos": 2,
    }

    for campo, valor in esperado.items():
        if resultado.get(campo) != valor:
            problemas.append(
                f"{campo}: esperado {valor}, obtido {resultado.get(campo)!r}"
            )

    if not decimal_igual(
        resultado.get("valor_total_homologado"),
        "141002.08",
    ):
        problemas.append(
            "valor_total_homologado: esperado 141002.08, "
            f"obtido {resultado.get('valor_total_homologado')!r}"
        )

    return problemas


def validar_p07(resultado: dict[str, Any]) -> list[str]:
    problemas = []

    if resultado.get("total_itens") != 36994:
        problemas.append(
            "total_itens: esperado 36994, "
            f"obtido {resultado.get('total_itens')!r}"
        )

    if not decimal_igual(
        resultado.get("valor_total_estimado"),
        "55968524178.3319",
    ):
        problemas.append(
            "valor_total_estimado: esperado 55968524178.3319, "
            f"obtido {resultado.get('valor_total_estimado')!r}"
        )

    return problemas


def validar_m01(resultado: dict[str, Any]) -> list[str]:
    problemas = validar_p02(resultado)

    if resultado.get("total_chunks_verificados") != 2125:
        problemas.append(
            "total_chunks_verificados: esperado 2125, "
            f"obtido {resultado.get('total_chunks_verificados')!r}"
        )

    if resultado.get("total_vinculos_complementares") != 0:
        problemas.append(
            "total_vinculos_complementares: esperado 0, "
            f"obtido {resultado.get('total_vinculos_complementares')!r}"
        )

    return problemas


def consolidar_offline(
    nome: str,
    execucoes: list[dict[str, Any]],
    validador,
) -> dict[str, Any]:
    problemas_gerais = []
    detalhes = []

    for execucao in execucoes:
        if execucao["status"] != "EXECUTADO":
            problemas = [execucao.get("erro", "Erro não especificado.")]
        else:
            problemas = validador(execucao["resultado"])

        detalhes.append(
            {
                "top_k": execucao["top_k"],
                "status_execucao": execucao["status"],
                "problemas": problemas,
            }
        )
        problemas_gerais.extend(problemas)

    totais = []
    for execucao in execucoes:
        if execucao["status"] == "EXECUTADO":
            r = execucao["resultado"]
            totais.append(
                (
                    r.get("itens_total"),
                    r.get("homologados"),
                    r.get("fracassados"),
                    r.get("desertos"),
                    r.get("valor_total_homologado"),
                    r.get("total_itens"),
                    r.get("valor_total_estimado"),
                    r.get("total_chunks_verificados"),
                    r.get("total_vinculos_complementares"),
                )
            )

    independencia_top_k = len(set(map(str, totais))) <= 1 if totais else False

    return {
        "caso": nome,
        "situacao": (
            "APROVADO"
            if not problemas_gerais and independencia_top_k
            else "REVISAR"
        ),
        "independente_top_k_1_e_3": independencia_top_k,
        "detalhes": detalhes,
        "execucoes": execucoes,
    }


def cliente_endpoint() -> OpenAI:
    return OpenAI(
        base_url=OLLAMA_URL,
        api_key="ollama",
        timeout=TIMEOUT_ENDPOINT,
        max_retries=0,
    )


def executar_online(
    nome: str,
    pergunta: str,
    routes: list[str],
    filters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    inicio = time.perf_counter()

    try:
        resultado = executar_consulta(
            pergunta,
            analise=analise(nome, pergunta, routes, filters),
            client=cliente_endpoint(),
            top_k=3,
            fetch_k=50,
            run_id=f"run_validacao_{nome.lower()}",
        )

        evidencias = resultado.get(
            "evidences",
            resultado.get("evidencias", []),
        )

        return {
            "caso": nome,
            "situacao": "EXECUTADO",
            "duracao_s": round(time.perf_counter() - inicio, 3),
            "resultado": resultado,
            "evidencias_resumidas": [
                evidencia_resumida(e) for e in evidencias
            ],
        }

    except Exception as erro:
        mensagem = f"{type(erro).__name__}: {erro}"
        texto = mensagem.casefold()
        timeout = (
            "timeout" in texto
            or "timed out" in texto
            or "tempo" in texto
        )

        return {
            "caso": nome,
            "situacao": "BLOQUEIO_ENDPOINT" if timeout else "ERRO",
            "duracao_s": round(time.perf_counter() - inicio, 3),
            "erro": mensagem,
            "traceback": traceback.format_exc(),
        }


def avaliar_combinada(caso: dict[str, Any]) -> dict[str, Any]:
    if caso["situacao"] != "EXECUTADO":
        return caso

    r = caso["resultado"]
    evidencias = r.get("evidences", r.get("evidencias", []))
    plano = r.get("plano", {})

    problemas = []
    if plano.get("estrategia") != "combinada":
        problemas.append(
            "O plano não usou estrategia='combinada'."
        )
    if r.get("total") != 1234:
        problemas.append(
            f"Total estruturado esperado 1234, obtido {r.get('total')!r}."
        )
    if not evidencias:
        problemas.append("Nenhuma evidência documental foi retornada.")

    tem_normativa = any(
        (e.get("natureza") == "normativa")
        or "normativa" in str(e.get("base_id", "")).casefold()
        for e in evidencias
    )
    if not tem_normativa:
        problemas.append("Não apareceu evidência de natureza normativa.")

    caso["avaliacao"] = {
        "situacao": "APROVADO" if not problemas else "REVISAR",
        "problemas": problemas,
        "total_estruturado": r.get("total"),
        "quantidade_evidencias": len(evidencias),
        "fontes": sorted({
            str(e.get("source_file") or e.get("fonte"))
            for e in evidencias
            if e.get("source_file") or e.get("fonte")
        }),
    }
    return caso


def avaliar_vidracaria(caso: dict[str, Any]) -> dict[str, Any]:
    if caso["situacao"] != "EXECUTADO":
        return caso

    r = caso["resultado"]
    evidencias = r.get("evidences", r.get("evidencias", []))

    avaliadas = []
    for e in evidencias:
        texto = e.get("text") or e.get("trecho") or ""
        texto_n = normalizar(texto)
        relevante = bool(
            re.search(r"\bvidrac", texto_n)
            or "vidro" in texto_n
        )
        avaliadas.append(
            {
                "chunk_id": e.get("chunk_id"),
                "fonte": e.get("source_file") or e.get("fonte"),
                "relevante_por_termo": relevante,
                "texto_inicio": texto[:500],
            }
        )

    quantidade_relevantes = sum(
        1 for x in avaliadas if x["relevante_por_termo"]
    )

    caso["avaliacao"] = {
        "situacao": (
            "APROVADO_PARA_INSPECAO_HUMANA"
            if quantidade_relevantes
            else "RELEVANCIA_INSUFICIENTE"
        ),
        "evidencias_retornadas": len(evidencias),
        "evidencias_com_indicio_de_vidracaria": quantidade_relevantes,
        "detalhes": avaliadas,
        "observacao": (
            "A presença do termo é apenas triagem. "
            "A relevância final deve ser confirmada pela leitura dos trechos."
        ),
    }
    return caso


def avaliar_normativa(caso: dict[str, Any]) -> dict[str, Any]:
    if caso["situacao"] != "EXECUTADO":
        return caso

    r = caso["resultado"]
    evidencias = r.get("evidences", r.get("evidencias", []))

    avaliadas = []
    for e in evidencias:
        texto = e.get("text") or e.get("trecho") or ""
        n = normalizar(texto)
        tem_pregao = "pregao" in n
        tem_dispositivo = any(
            termo in n
            for termo in (
                "art. 29",
                "artigo 29",
                "art. 28",
                "artigo 28",
                "xli",
            )
        )
        avaliadas.append(
            {
                "chunk_id": e.get("chunk_id"),
                "fonte": e.get("source_file") or e.get("fonte"),
                "natureza": e.get("natureza"),
                "menciona_pregao": tem_pregao,
                "menciona_dispositivo_esperado": tem_dispositivo,
                "texto_inicio": texto[:500],
            }
        )

    tem_normativa = any(
        x["natureza"] == "normativa" for x in avaliadas
    )
    tem_pregao = any(x["menciona_pregao"] for x in avaliadas)

    caso["avaliacao"] = {
        "situacao": (
            "APROVADO_PARA_INSPECAO_HUMANA"
            if evidencias and tem_normativa and tem_pregao
            else "REVISAR"
        ),
        "evidencias_retornadas": len(evidencias),
        "tem_evidencia_normativa": tem_normativa,
        "tem_mencao_pregao": tem_pregao,
        "detalhes": avaliadas,
        "observacao": (
            "Conferir manualmente se os trechos cobrem os dispositivos "
            "esperados: Art. 6º, XLI; Art. 28, I; Art. 29, caput e parágrafo único."
        ),
    }
    return caso


def resumo_markdown(relatorio: dict[str, Any]) -> str:
    linhas = [
        "# Validação final — Luiz",
        "",
        f"Data/hora: {relatorio['gerado_em']}",
        "",
        "## Suíte offline já informada",
        "",
        "- 334 testes aprovados.",
        "",
        "## Casos desta validação",
        "",
    ]

    for caso in relatorio["casos"]:
        linhas.append(
            f"- **{caso['caso']}**: "
            f"{caso.get('avaliacao', {}).get('situacao', caso.get('situacao'))}"
        )

    linhas += [
        "",
        "## Critério TIC",
        "",
        "- Validação automatizada já executada: 36 testes TIC aprovados.",
        "- Pendente exclusivamente a confirmação humana com Janice dos casos ambíguos.",
        "- Não considerar termos isolados como “eletrônico”, “digital”, “sistema” ou nome de órgão como prova suficiente de TIC.",
        "",
        "## Observação",
        "",
        "Se normativa/combinada/vidraçaria retornarem BLOQUEIO_ENDPOINT, registrar o timeout como bloqueio e não como aprovação.",
        "",
    ]
    return "\n".join(linhas)


def mostrar_offline(nome: str, consolidado: dict[str, Any]) -> None:
    imprimir_titulo(nome)
    print("Situação:", consolidado["situacao"])
    print(
        "Independência de top_k 1 e 3:",
        consolidado["independente_top_k_1_e_3"],
    )

    for execucao in consolidado["execucoes"]:
        print(f"\n  top_k={execucao['top_k']} -> {execucao['status']}")
        if execucao["status"] != "EXECUTADO":
            print("  Erro:", execucao.get("erro"))
            continue

        r = execucao["resultado"]
        print("  Estratégia:", r.get("estrategia"))
        print("  Operação:", r.get("operacao"))
        print("  Filtros:", r.get("filtros_aplicados"))

        for campo in (
            "itens_total",
            "homologados",
            "fracassados",
            "desertos",
            "valor_total_homologado",
            "total_itens",
            "valor_total_estimado",
            "total_chunks_verificados",
            "total_vinculos_complementares",
        ):
            if campo in r:
                print(f"  {campo}: {r[campo]}")

        if r.get("fontes"):
            print("  Fontes:", r["fontes"])


def mostrar_online(caso: dict[str, Any]) -> None:
    imprimir_titulo(caso["caso"])
    print("Situação de execução:", caso["situacao"])

    if caso["situacao"] != "EXECUTADO":
        print("Erro/bloqueio:", caso.get("erro"))
        return

    r = caso["resultado"]
    print("Estratégia:", r.get("plano", {}).get("estrategia", r.get("estrategia")))
    print("Operação:", r.get("plano", {}).get("operacao", r.get("operacao")))
    if "total" in r:
        print("Total:", r.get("total"))
    print("Rotas:", r.get("routes"))
    print("Filtros:", r.get("filters") or r.get("plano", {}).get("filtros"))
    print("Avaliação:", caso.get("avaliacao"))

    print("\nEvidências:")
    for i, e in enumerate(caso.get("evidencias_resumidas", []), 1):
        print(f"\n  [{i}] chunk_id={e.get('chunk_id')}")
        print("      natureza:", e.get("natureza"))
        print("      base:", e.get("base_id"))
        print("      fonte:", e.get("source_file"))
        print("      trecho:", e.get("texto_inicio", "").replace("\n", " ")[:500])


def main() -> None:
    if not (RAIZ / "src").exists():
        raise SystemExit(
            "Execute este arquivo na RAIZ do repositório, onde existe a pasta src/."
        )

    relatorio = {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "raiz_repositorio": str(RAIZ),
        "casos": [],
    }

    p02 = consolidar_offline(
        "P02",
        executar_offline("P02", P02),
        validar_p02,
    )
    relatorio["casos"].append(p02)
    mostrar_offline("P02", p02)

    p07 = consolidar_offline(
        "P07",
        executar_offline("P07", P07),
        validar_p07,
    )
    relatorio["casos"].append(p07)
    mostrar_offline("P07", p07)

    m01 = consolidar_offline(
        "M01",
        executar_offline("M01", M01),
        validar_m01,
    )
    relatorio["casos"].append(m01)
    mostrar_offline("M01", m01)

    combinada = avaliar_combinada(
        executar_online(
            "COMBINADA",
            COMBINADA,
            ["estruturada", "normativa"],
            {"ano": 2026, "tema": "pregão"},
        )
    )
    relatorio["casos"].append(combinada)
    mostrar_online(combinada)

    vidracaria = avaliar_vidracaria(
        executar_online(
            "VIDRACARIA",
            VIDRACARIA,
            ["estruturada"],
            {},
        )
    )
    relatorio["casos"].append(vidracaria)
    mostrar_online(vidracaria)

    normativa = avaliar_normativa(
        executar_online(
            "NORMATIVA",
            NORMATIVA,
            ["normativa"],
            {"norma": "Lei 14.133/2021", "tema": "pregão"},
        )
    )
    relatorio["casos"].append(normativa)
    mostrar_online(normativa)

    carimbo = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_saida = RAIZ / f"validacao_luiz_{carimbo}.json"
    md_saida = RAIZ / f"validacao_luiz_{carimbo}.md"

    json_saida.write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    md_saida.write_text(
        resumo_markdown(relatorio),
        encoding="utf-8",
    )

    imprimir_titulo("ARQUIVOS DE EVIDÊNCIA")
    print("JSON:", json_saida)
    print("Resumo:", md_saida)
    print(
        "\nIMPORTANTE: falta apenas a confirmação HUMANA com Janice "
        "dos critérios TIC/casos ambíguos."
    )


if __name__ == "__main__":
    main()
