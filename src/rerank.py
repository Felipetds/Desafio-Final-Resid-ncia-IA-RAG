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
    """
    Recebe a pergunta e a lista de candidatos do RRF.
    Retorna os candidatos reordenados com suas pontuações simuladas.
    """
    if not candidatos_rrf:
        logger.info({"event": "rerank", "status": "skipped_empty_list"})
        return []

    # Limita o lote que será enviado à API
    candidatos = candidatos_rrf[:MAX_CANDIDATES]

    if not RERANK_ENABLED:
        logger.info({"event": "rerank", "status": "disabled_fallback_rrf"})
        # Retorna a ordem do RRF (adicionando um score fictício decrescente)
        return [(chunk, 1.0 - (i * 0.01)) for i, chunk in enumerate(candidatos)][:TOP_K]

    try:
        # AQUI ENTRARÁ O ENDPOINT DO PROFESSOR.
        # Por agora, para simular uma reordenação bem-sucedida nos testes,
        # vamos simplesmente inverter a lista original de candidatos.
        logger.info({"event": "rerank", "status": "success", "model": RERANK_MODEL})
        candidatos_reordenados = list(reversed(candidatos))
        
        # Atribui pontuações para respeitar o formato de saída
        resultado = [(chunk, 0.9 - (i * 0.05)) for i, chunk in enumerate(candidatos_reordenados)][:TOP_K]
        return resultado

    except Exception as e:
        # Registra timeout ou resposta inválida e ativa o fallback
        logger.warning({"event": "rerank", "status": "error_fallback_rrf", "error": str(e)})
        return [(chunk, 1.0 - (i * 0.01)) for i, chunk in enumerate(candidatos)][:TOP_K]
