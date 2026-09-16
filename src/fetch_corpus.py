"""Coleta reproduzível do corpus do Grande Desafio RAG."""

import argparse
from pathlib import Path

import yaml


def carregar_manifesto(caminho: Path) -> dict:
    """Lê e valida os campos principais do manifesto."""
    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = yaml.safe_load(arquivo)

    if not isinstance(dados, dict) or not isinstance(dados.get("bases"), list):
        raise ValueError("Manifesto inválido: a seção 'bases' deve ser uma lista.")

    return dados



def verificar_destino_livre(destino: Path) -> None:
    """Impede que uma coleta substitua dados brutos já existentes."""
    if destino.exists():
        raise FileExistsError(
            f"Arquivo já existe e não será sobrescrito: {destino}"
        )


def consultar_pagina_pncp(parametros: dict) -> dict:
    """Consulta uma página do PNCP e informa falhas de forma clara."""
    import requests

    url = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"

    try:
        resposta = requests.get(
            url,
            params=parametros,
            timeout=(15, 60),
        )
        resposta.raise_for_status()
        resultado = resposta.json()
    except requests.RequestException as erro:
        raise RuntimeError(
            f"Falha na consulta ao PNCP; nenhum arquivo foi alterado: {erro}"
        ) from erro
    except ValueError as erro:
        raise RuntimeError(
            "O PNCP retornou uma resposta que não é um JSON válido."
        ) from erro

    if not isinstance(resultado, dict) or not isinstance(
        resultado.get("data"), list
    ):
        raise RuntimeError("Resposta inesperada do PNCP: campo 'data' ausente.")

    return resultado


def coletar_paginas_pncp(parametros: dict) -> list:
    """Reúne os registros de todas as páginas de uma consulta ao PNCP."""
    registros = []
    pagina = 1

    while True:
        parametros_pagina = {**parametros, "pagina": pagina}
        resultado = consultar_pagina_pncp(parametros_pagina)

        registros.extend(resultado["data"])

        total_paginas = resultado.get("totalPaginas")
        if not isinstance(total_paginas, int) or total_paginas < 1:
            raise RuntimeError("Resposta inesperada do PNCP: totalPaginas inválido.")

        if pagina >= total_paginas:
            break

        pagina += 1

    return registros

def main() -> None:
    parser = argparse.ArgumentParser(description="Ferramenta de coleta do corpus")
    parser.add_argument(
        "comando",
        choices=["inventory"],
        help="Operação a executar",
    )
    parser.add_argument(
        "--manifest",
        default="corpus_manifest.yaml",
        help="Caminho do manifesto YAML",
    )
    argumentos = parser.parse_args()

    manifesto = carregar_manifesto(Path(argumentos.manifest))
    print("Cenário:", manifesto.get("scenario_id"))
    print("Versão:", manifesto.get("version"))
    print("Bases cadastradas:")

    for base in manifesto["bases"]:
        print("-", base.get("base_id"), "|", base.get("natureza"))


if __name__ == "__main__":
    main()
