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
    """Consulta uma página, repetindo apenas falhas temporárias."""
    import time
    import requests

    url = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
    max_tentativas = 3

    for tentativa in range(1, max_tentativas + 1):
        try:
            resposta = requests.get(
                url,
                params=parametros,
                timeout=(15, 60),
            )
            resposta.raise_for_status()
            resultado = resposta.json()
        except requests.RequestException as erro:
            status = getattr(getattr(erro, "response", None), "status_code", None)
            temporario = (
                isinstance(erro, (requests.Timeout, requests.ConnectionError))
                or status in (429, 500, 502, 503, 504)
            )

            if not temporario or tentativa == max_tentativas:
                raise RuntimeError(
                    f"Falha na consulta ao PNCP após {tentativa} tentativa(s); "
                    f"nenhum arquivo foi alterado: {erro}"
                ) from erro

            espera = 2 ** (tentativa - 1)
            print(
                f"Falha temporária na página {parametros.get('pagina')}. "
                f"Nova tentativa em {espera} segundo(s) "
                f"({tentativa}/{max_tentativas}).",
                flush=True,
            )
            time.sleep(espera)
            continue
        except ValueError as erro:
            raise RuntimeError(
                "O PNCP retornou uma resposta que não é um JSON válido."
            ) from erro

        if not isinstance(resultado, dict) or not isinstance(
            resultado.get("data"), list
        ):
            raise RuntimeError(
                "Resposta inesperada do PNCP: campo 'data' ausente."
            )

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

def executar_fetch(manifesto: dict, raiz: Path) -> None:
    """Coleta a base estruturada sem substituir arquivos existentes."""
    import json
    import os
    import tempfile

    base = next(
        (
            item for item in manifesto["bases"]
            if item.get("base_id") == "estruturada_pncp_rj"
        ),
        None,
    )
    if base is None:
        raise ValueError("Base estruturada não encontrada no manifesto.")

    destino = raiz / base["arquivo_local"]

    # Esta verificação acontece ANTES de qualquer consulta à API.
    verificar_destino_livre(destino)

    filtros = base["selecao_deterministica"]
    parametros = {
        "dataInicial": filtros["dataInicial"],
        "dataFinal": filtros["dataFinal"],
        "codigoModalidadeContratacao": filtros["codigoModalidadeContratacao"],
        "uf": filtros["uf"],
        "tamanhoPagina": 50,
    }

    registros = coletar_paginas_pncp(parametros)
    if not registros:
        raise RuntimeError("A consulta não retornou registros; nada foi salvo.")

    destino.parent.mkdir(parents=True, exist_ok=True)
    temporario = None

    try:
        # Grava primeiro em arquivo temporário. Só publica ao terminar.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".json.tmp",
            dir=destino.parent,
            delete=False,
        ) as arquivo:
            temporario = Path(arquivo.name)
            json.dump(registros, arquivo, ensure_ascii=False, indent=2)

        # Falha se outro processo tiver criado o destino nesse intervalo.
        os.link(temporario, destino)
        print(f"Coleta concluída: {len(registros)} registros")
        print(f"Arquivo salvo: {destino}")
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ferramenta de coleta do corpus")
    parser.add_argument(
        "comando",
        choices=["inventory", "fetch"],
        help="Operação a executar",
    )
    parser.add_argument(
        "--manifest",
        default="corpus_manifest.yaml",
        help="Caminho do manifesto YAML",
    )
    argumentos = parser.parse_args()

    caminho_manifesto = Path(argumentos.manifest).resolve()
    manifesto = carregar_manifesto(caminho_manifesto)

    if argumentos.comando == "fetch":
        executar_fetch(manifesto, caminho_manifesto.parent)
        return

    print("Cenário:", manifesto.get("scenario_id"))
    print("Versão:", manifesto.get("version"))
    print("Bases cadastradas:")

    for base in manifesto["bases"]:
        print("-", base.get("base_id"), "|", base.get("natureza"))


if __name__ == "__main__":
    main()
