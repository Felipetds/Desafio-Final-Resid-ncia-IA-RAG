import json
from types import SimpleNamespace

import pytest
import src.generate as gerador


@pytest.mark.parametrize("rotas,naturezas,extrativo", [
    (["normativa"], ["normativa"], True),
    (["normativa"], ["normativa", "conversacional"], False),
    (["normativa", "conversacional"], ["normativa"], False),
    (["conversacional"], ["conversacional"], False),
])
def test_modo_depende_das_rotas_e_da_natureza(
    rotas, naturezas, extrativo, monkeypatch, tmp_path
):
    monkeypatch.setattr(gerador.obs, "PASTA_LOGS", tmp_path)
    chamadas = []

    def modelo(*, pergunta, contexto, client, modo_extrativo=False):
        chamadas.append(modo_extrativo)
        conteudo = (
            json.dumps({"chunk_ids": ["chunk_1"]})
            if modo_extrativo
            else "Regra documentada. [Fonte: chunk_1]"
        )
        return SimpleNamespace(
            choices=[SimpleNamespace(
                message=SimpleNamespace(content=conteudo),
                finish_reason="stop",
            )],
            usage=None,
        )

    monkeypatch.setattr(gerador, "chamar_llm", modelo)
    resposta = gerador.gerar_resposta(
        {
            "query": "Explique a regra.",
            "query_id": "q_modo_normativo",
            "routes": rotas,
            "filters": {},
            "is_refusal": False,
            "evidences": [
                {
                    "chunk_id": f"chunk_{numero}",
                    "text": "Regra documentada.",
                    "source_file": "documento.txt",
                    "natureza": natureza,
                }
                for numero, natureza in enumerate(naturezas, start=1)
            ],
            "stage": "fusao_rrf",
        },
        client=object(),
    )
    assert chamadas == [extrativo]
    assert resposta.sources_used
    assert resposta.stage == "geracao"
