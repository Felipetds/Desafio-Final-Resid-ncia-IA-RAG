import json
import re
import time
import uuid
from typing import Any, Dict, List

from openai import OpenAI


OLLAMA_URL = "http://ecoa-llm.duckdns.org:11434/v1"
GENERATION_MODEL = "qcwind/qwen3-8b-instruct-Q4-K-M"

ROTAS_VALIDAS = {
    "normativa",
    "estruturada",
    "conversacional",
    "agregada",
}


PROMPT_ROTEADOR = """
Você é o roteador de um sistema Adaptive RAG sobre contratações públicas
do Estado do Rio de Janeiro.

Sua tarefa não é decidir apenas pelo assunto da pergunta. Você deve decidir
qual tipo de evidência é necessário para respondê-la.

As bases disponíveis são:

1. normativa:
   Leis, decretos, editais, regras, requisitos, permissões, proibições,
   modalidades e vigência de normas.

2. estruturada:
   Contratos, fornecedores, órgãos, municípios, CNPJ, valores, datas,
   situação da contratação e objeto contratado.

3. conversacional:
   Atas, e-mails, manifestações, reclamações, dúvidas e comunicações.

4. agregada:
   Médias, totais, somas, séries históricas, comparações estatísticas
   e valores agrupados.

Uma pergunta pode exigir mais de uma base.

Exemplos:

Pergunta:
"Sou MEI, posso participar de pregão eletrônico? Existe algum aberto?"
Rotas:
["normativa", "estruturada"]

Pergunta:
"Qual foi o valor médio do arroz contratado em 2025?"
Rotas:
["agregada", "estruturada"]

Pergunta:
"Quantos contratos foram assinados por modalidade em 2025?"
Rotas:
["agregada", "estruturada"]

Pergunta:
"Quais contratos de software ficaram acima de R$ 500 mil?"
Rotas:
["estruturada"]

Pergunta:
"O que foi discutido nas atas sobre a compra de equipamentos?"
Rotas:
["conversacional"]

Importante:
- Perguntas que pedem quantidade, média, total, soma, percentual ou agrupamento
  exigem a base agregada.
- Quando a pergunta pedir especificamente o conteúdo de atas, e-mails,
  reclamações ou manifestações, use a base conversacional.
- Não adicione uma base somente porque a pergunta menciona compra,
  contrato ou modalidade. Identifique qual tipo de evidência foi solicitado.

Regras de segurança:

- Não faça acusações de fraude ou ilegalidade.
- Não exponha CPF, dados bancários, credenciais, telefone pessoal ou e-mail pessoal.
- Perguntas que pedem acusação ou conclusão jurídica devem ser marcadas
  para recusa parcial ou total.
- O sistema pode apresentar dados públicos e explicar normas.
- Não responda à pergunta. Apenas analise e classifique.

Retorne exclusivamente JSON válido no formato:

{
  "routes": ["estruturada"],
  "filters": {
    "uf": "RJ",
    "ano": 2025,
    "valor_minimo": null,
    "valor_maximo": null,
    "modalidade": null,
    "municipio": null,
    "fornecedor": null
  },
  "is_refusal": false,
  "refusal_reason": null,
  "justification": "Explicação curta da escolha das rotas."
}
"""


def _extrair_json(texto: str) -> Dict[str, Any]:
    """
    Extrai um objeto JSON mesmo quando o modelo inclui marcação Markdown.
    """
    texto = texto.strip()
    texto = texto.replace("```json", "").replace("```", "").strip()

    inicio = texto.find("{")
    fim = texto.rfind("}")

    if inicio == -1 or fim == -1:
        raise ValueError("O modelo não retornou um objeto JSON.")

    return json.loads(texto[inicio : fim + 1])


def _normalizar_rotas(rotas: Any) -> List[str]:
    """
    Mantém somente as quatro rotas permitidas, sem repetição.
    """
    if not isinstance(rotas, list):
        return []

    resultado = []

    for rota in rotas:
        rota_normalizada = str(rota).strip().lower()

        if rota_normalizada in ROTAS_VALIDAS:
            if rota_normalizada not in resultado:
                resultado.append(rota_normalizada)

    return resultado


def _roteamento_fallback(pergunta: str) -> Dict[str, Any]:
    """
    Roteamento emergencial utilizado somente quando o modelo não responde.

    O roteamento principal deve ser feito pelo LLM, pois a classificação
    somente por palavras-chave não é suficiente para o Adaptive RAG.
    """
    texto = pergunta.lower()
    rotas = []

    termos_agregados = [
        "média",
        "media",
        "total",
        "quantos",
        "quantas",
        "soma",
        "comparação",
        "comparar",
        "percentual",
    ]

    termos_normativos = [
        "lei",
        "decreto",
        "norma",
        "pode participar",
        "permitido",
        "proibido",
        "obrigatório",
        "obrigatorio",
        "regra",
        "vigente",
    ]

    termos_conversacionais = [
        "reclamação",
        "reclamacao",
        "e-mail",
        "email",
        "ata",
        "manifestação",
        "manifestacao",
        "ouvidoria",
    ]

    termos_estruturados = [
        "contrato",
        "fornecedor",
        "cnpj",
        "empresa",
        "órgão",
        "orgao",
        "município",
        "municipio",
        "valor",
        "licitação",
        "licitacao",
        "pregão",
        "pregao",
    ]

    if any(termo in texto for termo in termos_agregados):
        rotas.append("agregada")

    if any(termo in texto for termo in termos_normativos):
        rotas.append("normativa")

    if any(termo in texto for termo in termos_conversacionais):
        rotas.append("conversacional")

    if any(termo in texto for termo in termos_estruturados):
        rotas.append("estruturada")

    if not rotas:
        rotas = ["estruturada"]

    ano_encontrado = re.search(r"\b(20\d{2})\b", texto)

    valor_minimo = None
    valor_encontrado = re.search(
        r"(?:acima|superior|mais de)\s+(?:r\$\s*)?([\d.,]+)\s*(mil|milhão|milhoes|milhões)?",
        texto,
    )

    if valor_encontrado:
        numero = valor_encontrado.group(1).replace(".", "").replace(",", ".")
        valor_minimo = float(numero)

        unidade = valor_encontrado.group(2)

        if unidade == "mil":
            valor_minimo *= 1_000
        elif unidade in {"milhão", "milhoes", "milhões"}:
            valor_minimo *= 1_000_000

    return {
        "routes": rotas,
        "filters": {
            "uf": "RJ",
            "ano": int(ano_encontrado.group(1)) if ano_encontrado else None,
            "valor_minimo": valor_minimo,
            "valor_maximo": None,
            "modalidade": None,
            "municipio": None,
            "fornecedor": None,
        },
        "is_refusal": False,
        "refusal_reason": None,
        "justification": "Roteamento de contingência aplicado porque o modelo não respondeu.",
    }


def analisar_consulta(
    pergunta: str,
    client: OpenAI | None = None,
) -> Dict[str, Any]:
    """
    Analisa a pergunta e retorna rotas, filtros e decisão de segurança.
    """
    inicio = time.perf_counter()
    query_id = f"q_{uuid.uuid4().hex[:8]}"

    if not pergunta or not pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")

    if client is None:
        client = OpenAI(
            base_url=OLLAMA_URL,
            api_key="ollama",
        )

    try:
        resposta = client.chat.completions.create(
            model=GENERATION_MODEL,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": PROMPT_ROTEADOR,
                },
                {
                    "role": "user",
                    "content": pergunta.strip(),
                },
            ],
        )

        conteudo = resposta.choices[0].message.content
        resultado = _extrair_json(conteudo)

        resultado["routes"] = _normalizar_rotas(
            resultado.get("routes", [])
        )

        if not resultado["routes"] and not resultado.get("is_refusal"):
            resultado["routes"] = ["estruturada"]

        resultado.setdefault("filters", {})
        resultado.setdefault("is_refusal", False)
        resultado.setdefault("refusal_reason", None)
        resultado.setdefault("justification", "")

        uso = getattr(resposta, "usage", None)

        tokens = {
            "prompt": getattr(uso, "prompt_tokens", 0) if uso else 0,
            "completion": getattr(uso, "completion_tokens", 0) if uso else 0,
            "total": getattr(uso, "total_tokens", 0) if uso else 0,
        }

        resultado["router_fallback"] = False

    except Exception as erro:
        resultado = _roteamento_fallback(pergunta)
        resultado["router_fallback"] = True
        resultado["router_error"] = str(erro)

        tokens = {
            "prompt": 0,
            "completion": 0,
            "total": 0,
        }

    resultado["query"] = pergunta.strip()
    resultado["query_id"] = query_id
    resultado["stage"] = "roteamento"
    resultado["latencia_ms"] = round(
        (time.perf_counter() - inicio) * 1000,
        2,
    )
    resultado["tokens"] = tokens
    resultado["modelo"] = GENERATION_MODEL

    return resultado


if __name__ == "__main__":
    consulta = input("Digite uma pergunta: ")
    saida = analisar_consulta(consulta)
    print(json.dumps(saida, ensure_ascii=False, indent=2))
