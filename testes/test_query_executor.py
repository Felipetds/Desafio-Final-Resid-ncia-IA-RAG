import pytest

from src.query_executor import executar_plano


@pytest.fixture
def base():
    return [
        {
            "id_pncp": str(numero),
            "objeto": "Serviço de teste",
            "ano_compra": "2026",
            "fonte_original": "teste.json",
        }
        for numero in range(1, 6)
    ]


def test_contagem_independente_de_top_k(base):
    plano = {
        "bases": ["estruturada"],
        "estrategia": "consulta_estruturada",
        "operacao": "contar",
        "filtros": {},
    }

    resultados = [
        executar_plano(
            "Quantas contratações existem?",
            plano,
            base=base,
            top_k=limite,
        )
        for limite in (1, 3, 5)
    ]

    assert [r["total"] for r in resultados] == [5, 5, 5]
    assert all(r["registros"] == [] for r in resultados)


def test_listagem_usa_paginacao_e_campos_do_plano(base):
    resultado = executar_plano(
        "Liste os objetos das contratações de 2026.",
        {
            "bases": ["estruturada"],
            "estrategia": "consulta_estruturada",
            "operacao": "listar",
            "filtros": {"ano_compra": 2026},
            "campos": ["objeto"],
            "pagina": 1,
            "tamanho_pagina": 4,
        },
        base=base,
        top_k=1,
    )

    assert resultado["total"] == 5
    assert len(resultado["registros"]) == 4
    assert all(
        set(registro) == {"objeto"}
        for registro in resultado["registros"]
    )


def test_pergunta_aberta_segue_para_recuperacao():
    chamadas = []

    def recuperador(**kwargs):
        chamadas.append(kwargs)
        return {
            "routes": ["estruturada"],
            "evidences": [{"chunk_id": "vidraca_1"}],
        }

    pergunta = "Tem contratação relacionada a reparo de vidraça?"

    resultado = executar_plano(
        pergunta,
        {
            "estrategia": "recuperacao_hibrida",
            "operacao": "buscar",
        },
        top_k=3,
        fetch_k=50,
        recuperador=recuperador,
    )

    assert len(chamadas) == 1
    assert chamadas[0]["pergunta"] == pergunta
    assert chamadas[0]["top_k"] == 3
    assert resultado["evidences"][0]["chunk_id"] == "vidraca_1"
    assert resultado["estrategia"] == "recuperacao_hibrida"


def test_rejeita_estrategia_desconhecida():
    with pytest.raises(ValueError):
        executar_plano(
            "Uma pergunta.",
            {"estrategia": "inventada"},
        )


def test_rejeita_base_incompativel(base):
    with pytest.raises(ValueError):
        executar_plano(
            "Quantos registros?",
            {
                "bases": ["normativa"],
                "estrategia": "consulta_estruturada",
                "operacao": "contar",
            },
            base=base,
        )
