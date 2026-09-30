import sys
import os
from unittest import mock
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import rerank

@pytest.fixture
def mock_candidatos():
    return [
        {"id": "doc1", "text": "texto A", "metadata": {"natureza": "normativa"}},
        {"id": "doc2", "text": "texto B", "metadata": {"natureza": "estruturada"}},
        {"id": "doc3", "text": "texto C", "metadata": {"natureza": "conversacional"}},
        {"id": "doc4", "text": "texto D", "metadata": {"natureza": "agregada"}},
    ]

def test_rerank_disabled_fallback_rrf_e_top_k(mock_candidatos):
    rerank.RERANK_ENABLED = False
    rerank.TOP_K = 2
    resultado = rerank.executar_rerank("teste", mock_candidatos)
    
    assert len(resultado) == 2  # Respeita o Top K
    assert resultado[0][0]["id"] == "doc1"  # Fallback: Mantém ordem do RRF
    assert "metadata" in resultado[0][0]  # Manutenção de metadados

def test_rerank_lista_vazia():
    assert rerank.executar_rerank("teste", []) == []

@mock.patch("rerank.RERANK_ENABLED", True)
def test_rerank_reordenacao_simulada(mock_candidatos):
    rerank.TOP_K = 3
    resultado = rerank.executar_rerank("teste", mock_candidatos)
    
    # Nossa simulação inverte a lista. O doc4 passa para primeiro.
    assert resultado[0][0]["id"] == "doc4"
    assert resultado[1][0]["id"] == "doc3"

@mock.patch("rerank.RERANK_ENABLED", True)
@mock.patch("logging.Logger.warning")
def test_rerank_timeout_resposta_invalida_com_fallback(mock_logger, mock_candidatos):
    # Força uma falha simulando Timeout/Resposta Inválida
    with mock.patch("builtins.list", side_effect=TimeoutError("Conexao perdida")):
        rerank.TOP_K = 3
        resultado = rerank.executar_rerank("teste", mock_candidatos)
        
        # Em caso de erro, deve logar o problema e acionar o fallback do RRF
        assert mock_logger.called
        assert resultado[0][0]["id"] == "doc1"
