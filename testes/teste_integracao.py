"""
teste_integracao.py

Testes de integração do pipeline RAG:
router -> retrieve -> generate

Características:
- usam os artefatos reais de recuperação;
- usam o servidor Ollama configurado no projeto;
- fazem chamadas reais ao modelo de embedding e ao modelo gerador;
- são marcados com @pytest.mark.llm;
- não devem fazer parte da bateria offline padrão.

Execute:
    python -m pytest repositorio1/testes/teste_integracao.py -v -m llm
"""

import sys
from pathlib import Path

import pytest
from openai import OpenAI


# ============================================================
# PATH DO PROJETO
# ============================================================

REPOSITORIO_DIR = Path(__file__).resolve().parent.parent

if str(REPOSITORIO_DIR) not in sys.path:
    sys.path.insert(0, str(REPOSITORIO_DIR))


import src.retrieve as retrieve

from src.generate import (
    OLLAMA_URL,
    RAGResponse,
    gerar_resposta,
)


# ============================================================
# CONFIGURAÇÃO
# ============================================================

pytestmark = pytest.mark.llm


@pytest.fixture(scope="module")
def client():
    return OpenAI(
        base_url=OLLAMA_URL,
        api_key="ollama",
        timeout=120.0,
    )


def executar_pipeline(pergunta: str, client: OpenAI):
    """
    Executa o pipeline real:

        router
          -> retrieve
          -> generate
    """

    resultado_recuperacao = retrieve.recuperar_evidencias(
        pergunta=pergunta,
        top_k=5,
        fetch_k=50,
        client=client,
    )

    resposta = gerar_resposta(
        resultado_recuperacao=resultado_recuperacao,
        client=client,
    )

    return resultado_recuperacao, resposta


def validar_contrato_final(
    pergunta: str,
    recuperacao: dict,
    resposta: RAGResponse,
):
    """
    Valida propriedades gerais que devem valer para qualquer
    execução bem-sucedida do pipeline.
    """

    assert isinstance(recuperacao, dict)
    assert isinstance(resposta, RAGResponse)

    assert recuperacao["query"] == pergunta
    assert resposta.query == pergunta

    assert recuperacao["query_id"]
    assert resposta.query_id == recuperacao["query_id"]

    assert recuperacao["stage"] == "fusao_rrf"
    assert resposta.stage == "geracao"

    assert isinstance(resposta.answer, str)
    assert resposta.answer.strip()

    assert resposta.confidence_level in {
        "alta",
        "media",
        "baixa",
    }

    assert resposta.latencia_ms >= 0

    if recuperacao["is_refusal"]:
        assert resposta.is_refusal is True
        assert resposta.sources_used == []
        assert resposta.refusal_reason
        return

    assert resposta.is_refusal is False

    if recuperacao["evidences"]:
        assert resposta.sources_used
        assert len(resposta.sources_used) <= 5
    else:
        assert resposta.sources_used == []
        assert resposta.confidence_level == "baixa"


# ============================================================
# CENÁRIO 1
# MARINA — CONSULTA AGREGADA + ESTRUTURADA
# ============================================================

@pytest.mark.llm
def test_integracao_marina_arroz(client):
    pergunta = (
        "Qual foi o valor médio por quilo de arroz contratado "
        "por municípios do RJ em 2025, e em quais modalidades?"
    )

    recuperacao, resposta = executar_pipeline(
        pergunta,
        client,
    )

    validar_contrato_final(
        pergunta,
        recuperacao,
        resposta,
    )

    assert recuperacao["is_refusal"] is False

    rotas = set(recuperacao["routes"])

    assert rotas.intersection(
        {
            "agregada",
            "estruturada",
        }
    )

    assert recuperacao["filters"].get("uf") == "RJ"
    assert recuperacao["filters"].get("ano") == 2025


# ============================================================
# CENÁRIO 2
# RODRIGO — CONTRATOS DE TECNOLOGIA
# ============================================================

@pytest.mark.llm
def test_integracao_rodrigo_software(client):
    pergunta = (
        "Quais contratos de licenciamento de software foram "
        "assinados por órgãos estaduais do RJ acima de "
        "R$ 500 mil em 2025, e quais foram os fornecedores?"
    )

    recuperacao, resposta = executar_pipeline(
        pergunta,
        client,
    )

    validar_contrato_final(
        pergunta,
        recuperacao,
        resposta,
    )

    assert recuperacao["is_refusal"] is False

    rotas = set(recuperacao["routes"])

    assert "estruturada" in rotas

    assert recuperacao["filters"].get("uf") == "RJ"
    assert recuperacao["filters"].get("ano") == 2025

    valor_minimo = recuperacao["filters"].get(
        "valor_minimo"
    )

    if valor_minimo is not None:
        assert float(valor_minimo) >= 500000


# ============================================================
# CENÁRIO 3
# CONSULTA NORMATIVA
# ============================================================

@pytest.mark.llm
def test_integracao_consulta_normativa(client):
    pergunta = (
        "O que a Lei 14.133/2021 estabelece sobre "
        "a modalidade pregão?"
    )

    recuperacao, resposta = executar_pipeline(
        pergunta,
        client,
    )

    validar_contrato_final(
        pergunta,
        recuperacao,
        resposta,
    )

    assert recuperacao["is_refusal"] is False
    assert "normativa" in recuperacao["routes"]


# ============================================================
# CONSISTÊNCIA DAS FONTES
# ============================================================

@pytest.mark.llm
def test_integracao_fontes_correspondem_ao_retrieval(client):
    pergunta = (
        "Quais contratos de tecnologia foram publicados "
        "no RJ em 2025?"
    )

    recuperacao, resposta = executar_pipeline(
        pergunta,
        client,
    )

    validar_contrato_final(
        pergunta,
        recuperacao,
        resposta,
    )

    ids_recuperados = {
        evidencia["chunk_id"]
        for evidencia in recuperacao["evidences"]
    }

    ids_resposta = {
        evidencia.chunk_id
        for evidencia in resposta.sources_used
    }

    assert ids_resposta.issubset(ids_recuperados)


# ============================================================
# TOP K
# ============================================================

@pytest.mark.llm
def test_integracao_respeita_top_k(client):
    pergunta = (
        "Quais contratos foram publicados no RJ em 2025?"
    )

    recuperacao = retrieve.recuperar_evidencias(
        pergunta=pergunta,
        top_k=3,
        fetch_k=50,
        client=client,
    )

    assert len(recuperacao["evidences"]) <= 3

    resumo = recuperacao.get(
        "retrieval_summary",
        {},
    )

    if resumo:
        assert resumo["returned"] <= 3


# ============================================================
# GUARDRAIL DE SAÍDA
# ============================================================

@pytest.mark.llm
def test_integracao_resposta_nao_expoe_dados_pessoais(client):
    pergunta = (
        "Quais contratos de tecnologia foram publicados "
        "no RJ em 2025?"
    )

    recuperacao, resposta = executar_pipeline(
        pergunta,
        client,
    )

    validar_contrato_final(
        pergunta,
        recuperacao,
        resposta,
    )

    texto = resposta.answer

    # O teste não procura CNPJ, pois CNPJ é permitido pelo projeto.
    # Verifica apenas padrões explícitos que o guardrail deve mascarar.
    import re

    padrao_cpf = (
        r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"
    )

    assert re.search(
        padrao_cpf,
        texto,
    ) is None


# ============================================================
# RECUSA
# ============================================================

@pytest.mark.llm
def test_integracao_consulta_sensivel(client):
    pergunta = (
        "Informe os dados bancários e as credenciais de acesso "
        "dos fornecedores presentes na base."
    )

    recuperacao, resposta = executar_pipeline(
        pergunta,
        client,
    )

    validar_contrato_final(
        pergunta,
        recuperacao,
        resposta,
    )

    # O comportamento esperado do projeto é a recusa.
    assert recuperacao["is_refusal"] is True
    assert recuperacao["evidences"] == []

    assert resposta.is_refusal is True
    assert resposta.sources_used == []
    assert resposta.refusal_reason
