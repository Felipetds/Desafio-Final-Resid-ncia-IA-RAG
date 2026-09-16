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
