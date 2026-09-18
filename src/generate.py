"""
generate.py
Responsabilidades:
- Receber o resultado produzido pelo retrieve.py.
- Respeitar recusas definidas anteriormente pelo roteador.
- Montar o contexto a partir das evidências recuperadas.
- Gerar uma resposta fundamentada usando o LLM.
- Evitar respostas quando não houver evidências suficientes.
- Aplicar proteção de dados pessoais na saída.
- Registrar fontes, tokens e latência.
- Validar a resposta final utilizando RAGResponse.
"""

import re
import time
from typing import List
from openai import OpenAI
from schema import RAGResponse, RetrievalResult, SourceEvidence, TokenUsage

# Configurações

OLLAMA_URL = "http://ecoa-llm.duckdns.org:11434/v1"

GENERATION_MODEL = "qcwind/qwen3-8b-instruct-Q4-K-M"

# Prompt para gerar respostas

PROMPT_GERADOR = """
Você é o módulo de geração de um sistema Adaptive RAG especializado
em contratações públicas do Estado do Rio de Janeiro.

Responda à pergunta utilizando SOMENTE as evidências fornecidas no contexto.

Regras obrigatórias:

1. Não invente informações.

2. Não utilize conhecimento externo para completar informações ausentes.

3. Quando as evidências não forem suficientes para responder à pergunta,
   informe claramente que não foram encontradas informações suficientes.

4. Combine informações de diferentes evidências quando necessário.

5. Não conclua que houve fraude, ilegalidade ou irregularidade em uma
   contratação específica.

6. Não exponha CPF, RG, telefone pessoal, e-mail pessoal, dados bancários,
   senhas, tokens, credenciais ou outras informações pessoais sensíveis.

7. CNPJ, valores de contratos, fornecedores, órgãos públicos, modalidades
   e objetos de contratação podem ser apresentados quando estiverem
   presentes nas evidências públicas.

8. Não altere valores, datas, nomes, números de processos ou outras
   informações presentes nas evidências.

9. Quando houver divergência entre as fontes, informe que existe
   divergência em vez de escolher arbitrariamente uma delas.

10. Cite as fontes utilizadas no corpo da resposta utilizando o formato:

    [Fonte: nome_do_arquivo]

11. Não cite uma fonte que não esteja presente no contexto.

12. Responda em português brasileiro.

Retorne apenas a resposta final destinada ao usuário.
"""

# Proteção de dados

def mascarar_dados_pessoais(texto: str) -> str:
# Aplica uma camada adicional de proteção à resposta gerada.
# Esta função funciona como guardrail de saída.
# Ela não substitui a classificação de sensibilidade realizada anteriormente no pipeline.

    padroes = [
        (
            r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
            "[CPF_OCULTO]",
        ),
        (
            r"\b\d{1,2}\.?\d{3}\.?\d{3}-?[0-9Xx]\b",
            "[RG_OCULTO]",
        ),
        (
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\."
            r"[A-Za-z]{2,}\b",
            "[EMAIL_OCULTO]",
        ),
        (
            r"(?<!\d)"
            r"(?:\+?55\s*)?"
            r"(?:\(?\d{2}\)?[\s.-]*)?"
            r"(?:9\d{4}|\d{4})[-.\s]?\d{4}"
            r"(?!\d)",
            "[TELEFONE_OCULTO]",
        ),
        (
            r"(?i)\b(?:senha|password)\s*[:=]\s*[^\s,;]+",
            "senha: [CREDENCIAL_OCULTA]",
        ),
        (
            r"(?i)\b(?:token|access_token|api_key|apikey)"
            r"\s*[:=]\s*[^\s,;]+",
            "token: [CREDENCIAL_OCULTA]",
        ),
        (
            r"(?i)\b(?:ag[eê]ncia|ag\.)\s*[:=]?\s*\d{3,6}"
            r"(?:-\d)?\b",
            "[AGENCIA_BANCARIA_OCULTA]",
        ),
        (
            r"(?i)\b(?:conta(?:\s+corrente)?|c/c)"
            r"\s*[:=]?\s*\d{3,15}(?:-\d)?\b",
            "[CONTA_BANCARIA_OCULTA]",
        ),
    ]

    texto_seguro = texto

    for padrao, substituicao in padroes:
        texto_seguro = re.sub(
            padrao,
            substituicao,
            texto_seguro,
        )

    return texto_seguro

# Contexto

def montar_contexto(
    evidencias: List[SourceEvidence],
) -> str:
  # Converte as evidências recuperadas em contexto para o LLM.

    blocos = []

    for numero, evidencia in enumerate(
        evidencias,
        start=1,
    ):
        fonte = evidencia.source_file or "fonte_desconhecida"

        base = evidencia.base_id or evidencia.natureza or "desconhecida"

        bloco = (
            f"EVIDÊNCIA {numero}\n"
            f"Fonte: {fonte}\n"
            f"Base: {base}\n"
            f"Chunk ID: {evidencia.chunk_id}\n"
            f"Conteúdo:\n{evidencia.text.strip()}"
        )

        blocos.append(bloco)

    return "\n\n---\n\n".join(blocos)

# Confiança

def calcular_confianca(
    evidencias: List[SourceEvidence],
) -> str:
    # Define um nível simples de confiança com base na quantidade e na diversidade das evidências recuperadas.
    # Não representa uma probabilidade estatística.

    if not evidencias:
        return "baixa"

    fontes = {
        evidencia.source_file
        for evidencia in evidencias
        if evidencia.source_file
    }

    if len(evidencias) >= 3 and len(fontes) >= 2:
        return "alta"

    if len(evidencias) >= 2:
        return "media"

    return "baixa"

# Resposta em caso de recusa

def gerar_resposta_recusa(
    resultado: RetrievalResult,
) -> RAGResponse:
    # Gera uma resposta determinística quando o roteador já classificou a consulta como uma solicitação que deve ser recusada.

    motivo = (
        resultado.refusal_reason
        or "A solicitação envolve informação que não pode ser fornecida."
    )

    resposta = (
        "Não posso fornecer a informação solicitada porque "
        f"{motivo}"
    )

    return RAGResponse(
        query=resultado.query,
        query_id=resultado.query_id,
        answer=resposta,
        confidence_level="alta",
        sources_used=[],
        is_refusal=True,
        refusal_reason=motivo,
        tokens=TokenUsage(),
        modelo=None,
        latencia_ms=0.0,
    )

# Resposta em caso de não ter evidencias

def gerar_resposta_sem_evidencias(
    resultado: RetrievalResult,
) -> RAGResponse:
  # Retorna uma resposta determinística quando nenhuma evidência relevante foi recuperada.

    return RAGResponse(
        query=resultado.query,
        query_id=resultado.query_id,
        answer=(
            "Não encontrei informações suficientes nas fontes "
            "disponíveis para responder a essa pergunta."
        ),
        confidence_level="baixa",
        sources_used=[],
        is_refusal=False,
        refusal_reason=None,
        tokens=TokenUsage(),
        modelo=None,
        latencia_ms=0.0,
    )

# Geração com LLM

def chamar_llm(
    pergunta: str,
    contexto: str,
    client: OpenAI,
):
    # Executa a chamada ao modelo de geração.

    mensagem_usuario = f"""
PERGUNTA:

{pergunta}

CONTEXTO RECUPERADO:

{contexto}

Produza a resposta final utilizando somente o contexto acima.
"""

    return client.chat.completions.create(
        model=GENERATION_MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": PROMPT_GERADOR,
            },
            {
                "role": "user",
                "content": mensagem_usuario,
            },
        ],
    )

# Contagem de Tokens

def extrair_tokens(resposta_llm) -> TokenUsage:
    # Extrai informações de tokens quando fornecidas pelo servidor.

    uso = getattr(
        resposta_llm,
        "usage",
        None,
    )

    if uso is None:
        return TokenUsage()

    return TokenUsage(
        prompt=getattr(
            uso,
            "prompt_tokens",
            0,
        ) or 0,
        completion=getattr(
            uso,
            "completion_tokens",
            0,
        ) or 0,
        total=getattr(
            uso,
            "total_tokens",
            0,
        ) or 0,
    )

# Geração principal

def gerar_resposta(
    resultado_recuperacao,
    client: OpenAI | None = None,
) -> RAGResponse:
    # Executa a etapa completa de geração.

    #Fluxo:

    #RetrievalResult
    #    -> verificação de recusa
    #    -> verificação de evidências
    #    -> montagem do contexto
    #    -> chamada ao LLM
    #    -> guardrail de saída
    #    -> RAGResponse

    inicio = time.perf_counter()

    # Validação do contrato recebido do retrieve.py

    if isinstance(
        resultado_recuperacao,
        RetrievalResult,
    ):
        resultado = resultado_recuperacao

    else:
        resultado = RetrievalResult.model_validate(
            resultado_recuperacao
        )

    # Recusa definida anteriormente pelo pipeline

    if resultado.is_refusal:
        resposta = gerar_resposta_recusa(
            resultado
        )

        resposta.latencia_ms = round(
            (time.perf_counter() - inicio) * 1000,
            2,
        )

        return resposta

    # Nenhuma evidência recuperada

    if not resultado.evidences:
        resposta = gerar_resposta_sem_evidencias(
            resultado
        )

        resposta.latencia_ms = round(
            (time.perf_counter() - inicio) * 1000,
            2,
        )

        return resposta

    # Cliente do modelo

    if client is None:
        client = OpenAI(
            base_url=OLLAMA_URL,
            api_key="ollama",
        )

    # Construção do contexto

    contexto = montar_contexto(
        resultado.evidences
    )

    # Chamada ao modelo

    try:
        resposta_llm = chamar_llm(
            pergunta=resultado.query,
            contexto=contexto,
            client=client,
        )

        conteudo = (
            resposta_llm
            .choices[0]
            .message
            .content
        )

        if not conteudo or not conteudo.strip():
            raise ValueError(
                "O modelo retornou uma resposta vazia."
            )

        tokens = extrair_tokens(
            resposta_llm
        )

    except Exception as erro:
        return RAGResponse(
            query=resultado.query,
            query_id=resultado.query_id,
            answer=(
                "Não foi possível gerar a resposta neste momento "
                "devido a uma falha no modelo de geração."
            ),
            confidence_level="baixa",
            sources_used=[],
            is_refusal=False,
            refusal_reason=None,
            tokens=TokenUsage(),
            modelo=GENERATION_MODEL,
            latencia_ms=round(
                (time.perf_counter() - inicio) * 1000,
                2,
            ),
            stage="geracao",
        )

    # Guardrail final

    resposta_segura = mascarar_dados_pessoais(
        conteudo.strip()
    )

    # Confiança

    confianca = calcular_confianca(
        resultado.evidences
    )

    # Contrato final

    resposta_final = RAGResponse(
        query=resultado.query,
        query_id=resultado.query_id,
        answer=resposta_segura,
        confidence_level=confianca,
        sources_used=resultado.evidences,
        is_refusal=False,
        refusal_reason=None,
        tokens=tokens,
        modelo=GENERATION_MODEL,
        latencia_ms=round(
            (time.perf_counter() - inicio) * 1000,
            2,
        ),
        stage="geracao",
    )

    return resposta_final
