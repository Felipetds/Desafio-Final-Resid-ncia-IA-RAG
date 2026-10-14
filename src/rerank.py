import os
import logging

# Configuração de logging para registrar o evento 'rerank'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações do Rerank via variáveis de ambiente (com fallbacks seguros)
RERANK_ENABLED = os.getenv("RERANK_ENABLED", "false").lower() == "true"
RERANK_URL = os.getenv("RERANK_URL", "http://localhost/rerank")
RERANK_AUTH = os.getenv("RERANK_AUTH", "")
RERANK_MODEL = os.getenv("RERANK_MODEL", "modelo-padrao")
RERANK_TIMEOUT = int(os.getenv("RERANK_TIMEOUT", "5"))
MAX_CANDIDATES = int(os.getenv("MAX_CANDIDATES", "20"))
TOP_K = int(os.getenv("TOP_K", "3"))

def executar_rerank(pergunta, candidatos_rrf):
    """Preserva o RRF enquanto não houver integração real de rerank.

    Não gera scores fictícios nem trunca os candidatos antes da
    seleção multirrota realizada pelo recuperador.
    """
    if not candidatos_rrf:
        logger.info({
            "event": "rerank",
            "status": "skipped_empty_list",
            "applied": False,
        })
        return []

    if RERANK_ENABLED:
        logger.warning({
            "event": "rerank",
            "status": "not_implemented_fallback_rrf",
            "applied": False,
        })
    else:
        logger.info({
            "event": "rerank",
            "status": "disabled_fallback_rrf",
            "applied": False,
        })

    return [(candidato, None) for candidato in candidatos_rrf]
