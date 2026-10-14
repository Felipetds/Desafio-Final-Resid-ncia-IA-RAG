import json

from app.pipeline_adapter import executar_pipeline


CASOS = {
    "P03": (
        "O que a ata nº 00191/2026 da EBSERH registra sobre o "
        "objeto da aquisição e qual é o número de controle PNCP associado?"
    ),
    "P08": (
        "O que a ata nº 00137/2026 do INCA informa sobre o "
        "objeto adquirido e o fornecedor?"
    ),
}


resultados = {}

for caso, pergunta in CASOS.items():
    print("\n" + "=" * 100)
    print(caso)
    print("=" * 100)
    print("PERGUNTA:")
    print(pergunta)

    try:
        resultado = executar_pipeline(
            pergunta,
            top_k=5,
        )

        resultados[caso] = resultado

        print("\nRESPOSTA:")
        print(resultado.get("answer"))

        print("\nESTRATÉGIA:")
        print(resultado.get("estrategia"))

        print("\nROTAS:")
        print(resultado.get("routes"))

        print("\nFILTROS:")
        print(resultado.get("filters"))

        print("\nFONTES RECUPERADAS:")
        print(resultado.get("fontes_recuperadas"))

        print("\nFONTES CITADAS:")
        print(resultado.get("fontes_citadas"))

        print("\nEVIDÊNCIAS:")

        for evidencia in resultado.get("evidences", []):
            print("\n---")
            print("posição:", evidencia.get("posição"))
            print("chunk_id:", evidencia.get("chunk_id"))
            print("natureza:", evidencia.get("natureza"))
            print("fonte:", evidencia.get("fonte"))
            print("base:", evidencia.get("base"))
            print("score RRF:", evidencia.get("score_rrf"))
            print("trecho:")
            print(evidencia.get("trecho", "")[:2000])

    except Exception as erro:
        resultados[caso] = {
            "erro": f"{type(erro).__name__}: {erro}"
        }

        print("\nERRO:")
        print(type(erro).__name__, erro)


with open(
    "validacao_p03_p08.json",
    "w",
    encoding="utf-8",
) as arquivo:
    json.dump(
        resultados,
        arquivo,
        ensure_ascii=False,
        indent=2,
        default=str,
    )


print("\n" + "=" * 100)
print("Arquivo salvo em validacao_p03_p08.json")