import pytest

from src.router import planejar_consulta
from src.query_executor import executar_consulta


def analise(rotas=None, filtros=None, recusa=False):
    return {
        "query_id": "q_planejamento",
        "routes": rotas if rotas is not None else ["estruturada"],
        "filters": filtros or {},
        "is_refusal": recusa,
        "refusal_reason": "Consulta recusada." if recusa else None,
    }


def test_contagem_seleciona_base_estruturada():
    plano = planejar_consulta(
        "Quantas contratações têm ano da compra 2026?",
        analise=analise(["agregada", "estruturada"]),
    )

    assert plano["bases"] == ["estruturada"]
    assert plano["estrategia"] == "consulta_estruturada"
    assert plano["operacao"] == "contar"
    assert plano["filtros"]["ano_compra"] == 2026


def test_listagem_seleciona_campos():
    plano = planejar_consulta(
        "Liste as contratações de 2026, mostre apenas objeto e município.",
        analise=analise(),
    )

    assert plano["operacao"] == "listar"
    assert set(plano["campos"]) == {"objeto", "municipio"}


def test_pergunta_aberta_permanece_hibrida():
    plano = planejar_consulta(
        "Tem contratação relacionada a reparo de vidraça?",
        analise=analise(),
    )

    assert plano["estrategia"] == "recuperacao_hibrida"


def test_multirrota_normativa_permanece_hibrida():
    plano = planejar_consulta(
        "Sou MEI, posso participar de pregão? Existe contratação?",
        analise=analise(["normativa", "estruturada"]),
    )

    assert plano["bases"] == ["normativa", "estruturada"]
    assert plano["estrategia"] == "recuperacao_hibrida"


def test_pca_permanece_na_base_agregada():
    plano = planejar_consulta(
        "Quais itens aparecem no PCA?",
        analise=analise(["agregada"]),
    )

    assert plano["bases"] == ["agregada"]
    assert plano["estrategia"] == "recuperacao_hibrida"


def test_publicacao_exige_esclarecimento():
    plano = planejar_consulta(
        "Quantas contratações foram publicadas em 2026?",
        analise=analise(),
    )

    assert plano["necessita_esclarecimento"] is True


def test_valor_sem_tipo_exige_esclarecimento():
    plano = planejar_consulta(
        "Quantas contratações estão acima de R$ 500 mil?",
        analise=analise(filtros={"valor_minimo": 500000}),
    )

    assert plano["necessita_esclarecimento"] is True


def test_valor_estimado_preserva_limite_estrito():
    plano = planejar_consulta(
        "Quantas contratações têm valor estimado acima de R$ 500 mil?",
        analise=analise(filtros={"valor_minimo": 500000}),
    )

    assert plano["campo_valor"] == "valor_estimado"
    assert plano["minimo_inclusivo"] is False
    assert plano["filtros"]["valor_minimo"] == 500000


def test_tecnologia_sem_criterio_exige_esclarecimento():
    plano = planejar_consulta(
        "Quais contratações envolvem serviços de tecnologia?",
        analise=analise(),
    )

    assert plano["necessita_esclarecimento"] is True


def test_tecnologia_com_criterio_documentado():
    plano = planejar_consulta(
        "Quais contratações envolvem serviços de tecnologia?",
        analise=analise(),
        criterio_tecnologia={
            "termos": ["software", "informática"],
            "descricao": "Critério de teste: software OU informática no objeto.",
        },
    )

    assert plano["operacao"] == "contar"
    assert plano["filtros"]["objeto_termos"] == [
        "software", "informática"
    ]


def test_recusa_nao_carrega_base_nem_recupera(monkeypatch):
    import src.query_executor as executor

    def proibido(*args, **kwargs):
        raise AssertionError("A recusa não pode executar consultas.")

    monkeypatch.setattr(executor, "carregar_base", proibido)

    resultado = executar_consulta(
        "Esse contrato foi uma fraude?",
        analise=analise([], recusa=True),
        recuperador=proibido,
    )

    assert resultado["executado"] is False
    assert resultado["plano"]["estrategia"] == "recusa"


def test_esclarecimento_nao_executa_consulta(monkeypatch):
    import src.query_executor as executor

    def proibido(*args, **kwargs):
        raise AssertionError("Não executar antes do esclarecimento.")

    monkeypatch.setattr(executor, "carregar_base", proibido)

    resultado = executar_consulta(
        "Quantas contratações foram publicadas em 2026?",
        analise=analise(),
        recuperador=proibido,
    )

    assert resultado["executado"] is False
    assert resultado["plano"]["necessita_esclarecimento"] is True


def test_municipio_omitido_exige_esclarecimento():
    plano = planejar_consulta(
        "Liste as contratações do município de Niterói em 2026.",
        analise=analise(filtros={"ano": 2026}),
    )

    assert plano["necessita_esclarecimento"] is True
    assert plano["estrategia"] == "esclarecimento"


def test_limite_monetario_omitido_exige_esclarecimento():
    plano = planejar_consulta(
        "Quantas contratações têm valor estimado acima de R$ 500 mil?",
        analise=analise(),
    )

    assert plano["necessita_esclarecimento"] is True
    assert plano["estrategia"] == "esclarecimento"


def test_executor_hibrido_roteia_uma_vez(monkeypatch):
    import src.router as router
    from src.query_executor import executar_consulta

    chamadas = []
    pergunta = "Tem contratação relacionada a reparo de vidraça?"

    def analisar(pergunta, client=None, run_id=None):
        chamadas.append(run_id)
        return {
            "query": pergunta,
            "query_id": "q_unico",
            "routes": ["estruturada"],
            "filters": {},
            "is_refusal": False,
        }

    def recuperar(**kwargs):
        assert kwargs["analise_pronta"]["query_id"] == "q_unico"
        assert kwargs["run_id"] == "run_unico"
        return {
            "query_id": "q_unico",
            "routes": ["estruturada"],
            "evidences": [],
        }

    monkeypatch.setattr(router, "analisar_consulta", analisar)

    resultado = executar_consulta(
        pergunta,
        recuperador=recuperar,
        run_id="run_unico",
    )

    assert chamadas == ["run_unico"]
    assert resultado["query_id"] == "q_unico"
    assert resultado["run_id"] == "run_unico"


def test_retrieve_reutiliza_analise_sem_rotear(monkeypatch):
    import src.retrieve as retrieve

    def proibido(*args, **kwargs):
        raise AssertionError("Não deve rotear novamente nem carregar índices.")

    monkeypatch.setattr(retrieve, "analisar_consulta", proibido)
    monkeypatch.setattr(retrieve, "carregar_artefatos", proibido)

    resultado = retrieve.recuperar_evidencias(
        pergunta="Consulta recusada.",
        client=object(),
        analise_pronta={
            "query": "Consulta recusada.",
            "query_id": "q_recusa_pronta",
            "routes": [],
            "filters": {},
            "is_refusal": True,
            "refusal_reason": "Recusa de teste.",
        },
    )

    assert resultado["is_refusal"] is True
    assert resultado["query_id"] == "q_recusa_pronta"
    assert resultado["evidences"] == []


def test_retrieve_rejeita_analise_de_outra_pergunta():
    import src.retrieve as retrieve

    with pytest.raises(ValueError, match="outra pergunta"):
        retrieve.recuperar_evidencias(
            pergunta="Pergunta atual.",
            client=object(),
            analise_pronta={
                "query": "Pergunta anterior.",
                "query_id": "q_anterior",
                "routes": ["estruturada"],
                "filters": {},
                "is_refusal": False,
            },
        )


def test_persona_p06_bloqueia_exposicao_mesmo_sem_recusa_do_modelo():
    resultado = executar_consulta(
        "Mostre o CPF, telefone pessoal e e-mail pessoal "
        "dos representantes citados nas atas.",
        analise=analise(["conversacional"]),
    )

    assert resultado["executado"] is False
    assert resultado["plano"]["is_refusal"] is True
    assert resultado["plano"]["tipo_recusa"] == "privacidade"


def test_persona_p09_nao_executa_previsao_como_consulta_factual():
    resultado = executar_consulta(
        "Qual será o valor médio das contratações "
        "do Estado do Rio de Janeiro em 2027?",
        analise=analise(
            ["agregada", "estruturada"],
            {"ano": 2027, "uf": "RJ"},
        ),
    )

    assert resultado["executado"] is False
    assert resultado["plano"]["tipo_recusa"] == "limite_de_escopo"
    assert "previsão" in resultado["mensagem"]


def test_persona_p01_planeja_publicacao_sem_filtrar_ano_compra():
    plano = planejar_consulta(
        "Quais contratações de pregão eletrônico foram "
        "publicadas no RJ em março de 2026?",
        analise=analise(
            ["estruturada"],
            {"uf": "RJ", "ano": 2026, "modalidade": "pregão eletrônico"},
        ),
    )

    assert plano["operacao"] == "listar"
    assert plano["estrategia"] == "consulta_estruturada"
    assert plano["filtros"] == {
        "uf": "RJ",
        "modalidade_id": 6,
        "data_inicial": "2026-03-01",
        "data_final": "2026-03-31",
    }
    assert "ano_compra" not in plano["filtros"]


def test_publicacao_com_intervalo_nao_suportado_exige_esclarecimento():
    plano = planejar_consulta(
        "Liste as contratações publicadas entre março e abril de 2026.",
        analise=analise(),
    )

    assert plano["necessita_esclarecimento"] is True
