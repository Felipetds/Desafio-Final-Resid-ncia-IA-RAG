import json
import re
import time
import uuid
from typing import Any, Dict, List

from openai import OpenAI

try:
    from . import obs  # funciona como src.router ou repositorio1.src.router
except ImportError:  # permite "python src/router.py" direto, sem pacote.
    import obs


OLLAMA_URL = "http://ecoa-llm.duckdns.org:11434/v1"
GENERATION_MODEL = "qcwind/qwen3-8b-instruct-Q4-K-M"

ROTAS_VALIDAS = {
    "normativa",
    "estruturada",
    "conversacional",
    "agregada",
}

# Campos de filtro que só devem ser aceitos se aparecerem
# explicitamente no texto da pergunta (evita filtro inventado pelo LLM).
CAMPOS_FILTRO_VALIDADOS_NO_TEXTO = [
    "ano",
    "modalidade",
    "municipio",
    "fornecedor",
]


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
- Perguntas sobre o Plano de Contratações Anual ou PCA devem usar
  a base agregada. Inclua também a estruturada somente se a pergunta
  exigir comparação com contratos efetivamente realizados.
- Quando a pergunta pedir especificamente o conteúdo de atas, e-mails,
  reclamações ou manifestações, use a base conversacional.
- Não adicione uma base somente porque a pergunta menciona compra,
  contrato ou modalidade. Identifique qual tipo de evidência foi solicitado.

Regras de extração de filtros:
- Extraia um filtro SOMENTE se o valor estiver explícito na pergunta.
- "serviços de tecnologia" é o OBJETO da contratação, não uma modalidade.
  Modalidade só deve ser preenchida se a pergunta citar termos como
  "pregão eletrônico", "concorrência", "dispensa", "inexigibilidade" etc.
- Nunca preencha "ano" se a pergunta não mencionar um ano explicitamente.
- Se não houver evidência textual de um filtro, retorne null para esse campo.

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


def _normalizar_texto_para_comparacao(texto: str) -> str:
    """
    Remove pontuação e espaços repetidos antes de comparar.

    O LLM costuma normalizar valores (ex.: "Pregão - Eletrônico"),
    enquanto a pergunta original vem sem essa formatação
    (ex.: "pregão eletrônico"). Sem essa normalização, a comparação
    literal descarta filtros válidos por engano.
    """
    texto = texto.lower()
    texto = re.sub(r"[^\wà-ÿ\s]", " ", texto, flags=re.UNICODE)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def _converter_valor_monetario(
    numero_texto: str,
    unidade: str | None,
) -> float:
    """
    Converte valores monetários escritos em formato brasileiro.

    Exemplos:
    500 mil -> 500000
    1 milhão -> 1000000
    1,5 milhão -> 1500000
    750.000 -> 750000
    """
    numero_texto = numero_texto.strip()

    if "," in numero_texto:
        numero_normalizado = (
            numero_texto
            .replace(".", "")
            .replace(",", ".")
        )
    elif re.fullmatch(r"\d{1,3}(?:\.\d{3})+", numero_texto):
        numero_normalizado = numero_texto.replace(".", "")
    else:
        numero_normalizado = numero_texto

    valor = float(numero_normalizado)
    unidade = (unidade or "").lower().strip()

    if unidade == "mil":
        valor *= 1_000
    elif unidade in {
        "milhão",
        "milhao",
        "milhões",
        "milhoes",
    }:
        valor *= 1_000_000

    return valor


def _extrair_filtros_monetarios(
    pergunta: str,
) -> Dict[str, float | None]:
    """
    Extrai limites monetários diretamente da pergunta.

    A extração determinística impede que o LLM transforme,
    por exemplo, R$ 500 mil em R$ 500 milhões.
    """
    texto = pergunta.lower()

    numero = r"([\d]+(?:[.,][\d]+)*)"
    unidade = (
        r"(milhões|milhoes|milhão|milhao|mil)?"
    )

    padrao_minimo = re.search(
        rf"(?:acima\s+de|superior(?:es)?\s+a|mais\s+de)"
        rf"\s+(?:r\$\s*)?{numero}\s*{unidade}",
        texto,
    )

    padrao_maximo = re.search(
        rf"(?:abaixo\s+de|inferior(?:es)?\s+a|menos\s+de|"
        rf"até|ate)\s+(?:r\$\s*)?{numero}\s*{unidade}",
        texto,
    )

    valor_minimo = None
    valor_maximo = None

    if padrao_minimo:
        valor_minimo = _converter_valor_monetario(
            padrao_minimo.group(1),
            padrao_minimo.group(2),
        )

    if padrao_maximo:
        valor_maximo = _converter_valor_monetario(
            padrao_maximo.group(1),
            padrao_maximo.group(2),
        )

    return {
        "valor_minimo": valor_minimo,
        "valor_maximo": valor_maximo,
    }


def _extrair_uf_explicita(pergunta: str) -> str | None:
    """Retorna RJ somente quando a localização aparece na pergunta."""
    texto = _normalizar_texto_para_comparacao(pergunta)

    if re.search(r"\brj\b", texto) or "rio de janeiro" in texto:
        return "RJ"

    return None


def _validar_filtros_contra_pergunta(
    pergunta: str,
    filtros: Dict[str, Any] | None,
) -> Dict[str, Any]:
    """
    Remove filtros inventados pelo modelo e corrige valores
    monetários utilizando diretamente o texto da pergunta.
    """
    if not isinstance(filtros, dict):
        filtros = {}

    filtros = dict(filtros)
    texto = _normalizar_texto_para_comparacao(pergunta)

    for campo in CAMPOS_FILTRO_VALIDADOS_NO_TEXTO:
        valor = filtros.get(campo)

        if (
            valor
            and _normalizar_texto_para_comparacao(
                str(valor)
            ) not in texto
        ):
            filtros[campo] = None

    limites = _extrair_filtros_monetarios(pergunta)

    # Se a pergunta não contém limite explícito, qualquer
    # valor sugerido pelo modelo é descartado.
    filtros["valor_minimo"] = limites["valor_minimo"]
    filtros["valor_maximo"] = limites["valor_maximo"]

    # A UF só pode ser aplicada quando estiver explícita na pergunta.
    filtros["uf"] = _extrair_uf_explicita(pergunta)
    filtros.setdefault("ano", None)
    filtros.setdefault("modalidade", None)
    filtros.setdefault("municipio", None)
    filtros.setdefault("fornecedor", None)

    return filtros


def _roteamento_fallback(pergunta: str) -> Dict[str, Any]:
    """
    Roteamento emergencial utilizado somente quando o modelo não responde.

    O roteamento principal deve ser feito pelo LLM, pois a classificação
    somente por palavras-chave não é suficiente para o Adaptive RAG.
    """
    texto = pergunta.lower()
    rotas = []

    termos_recusa = [
        "foi uma fraude",
        "é uma fraude",
        "e uma fraude",
        "contrato fraudulento",
        "foi ilegal",
        "é ilegal",
        "e ilegal",
        "houve corrupção",
        "houve corrupcao",
    ]

    if any(termo in texto for termo in termos_recusa):
        return {
            "routes": [],
            "filters": {
                "uf": None,
                "ano": None,
                "valor_minimo": None,
                "valor_maximo": None,
                "modalidade": None,
                "municipio": None,
                "fornecedor": None,
            },
            "is_refusal": True,
            "refusal_reason": (
                "Pergunta envolve acusação de fraude ou "
                "ilegalidade, que não pode ser determinada "
                "pelo sistema."
            ),
            "justification": (
                "Recusa aplicada pelas regras de segurança."
            ),
        }

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
        "plano de contratações anual",
        "plano de contratacoes anual",
        "pca",
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

    consulta_conversacional = (
        any(
            termo in texto
            for termo in termos_conversacionais
        )
        or re.search(r"\batas?\b", texto) is not None
    )

    if consulta_conversacional:
        rotas.append("conversacional")

    if any(termo in texto for termo in termos_estruturados):
        rotas.append("estruturada")

    if not rotas:
        rotas = ["estruturada"]

    ano_encontrado = re.search(r"\b(20\d{2})\b", texto)

    valor_minimo = None
    valor_encontrado = re.search(
        r"(?:acima\s+de|superior(?:es)?\s+a|mais\s+de)\s+"
        r"(?:r\$\s*)?([\d.,]+)\s*(milhões|milhoes|milhão|mil)?",
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
            "uf": _extrair_uf_explicita(pergunta),
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
    run_id: str | None = None,
) -> Dict[str, Any]:
    """
    Analisa a pergunta e retorna rotas, filtros e decisão de segurança.

    run_id agrupa, no log JSONL do obs.py, as etapas "query_analysis" e
    "roteamento" desta mesma chamada. É opcional: quando quem chama (por
    exemplo o retrieve.py ou os testes) não informa um run_id, um novo é
    gerado aqui mesmo, então nada quebra em quem já usava a função sem
    esse parâmetro.
    """
    inicio = time.perf_counter()
    query_id = f"q_{uuid.uuid4().hex[:8]}"

    if not pergunta or not pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")

    run_id = run_id or obs.novo_run_id()
    pergunta_limpa = pergunta.strip()

    # Etapa "query_analysis": registra a pergunta recebida antes de decidir
    # rotas. Não envolve chamada ao LLM, então dificilmente falha; mesmo
    # assim fica dentro do observar_etapa para logar erro caso ocorra.
    with obs.observar_etapa(
        run_id=run_id,
        query_id=query_id,
        stage="query_analysis",
        input_data={"pergunta": pergunta_limpa},
    ) as observacao_analise:
        observacao_analise["output"] = {
            "tamanho_pergunta": len(pergunta_limpa),
        }

    if client is None:
        client = OpenAI(
            base_url=OLLAMA_URL,
            api_key="ollama",
        )

    try:
        with obs.observar_etapa(
            run_id=run_id,
            query_id=query_id,
            stage="roteamento",
            input_data={"pergunta": pergunta_limpa},
            modelo=GENERATION_MODEL,
        ) as observacao_roteamento:
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
                        "content": pergunta_limpa,
                    },
                ],
            )

            conteudo = resposta.choices[0].message.content
            resultado = _extrair_json(conteudo)

            resultado["routes"] = _normalizar_rotas(
                resultado.get("routes", [])
            )

            # Importante: setdefault ANTES de validar, senão resultado["filters"]
            # pode não existir (KeyError) ou vir como null (AttributeError).
            resultado.setdefault("filters", {})

            resultado["filters"] = _validar_filtros_contra_pergunta(
                pergunta,
                resultado["filters"],
            )

            resultado.setdefault("is_refusal", False)
            resultado.setdefault("refusal_reason", None)
            resultado.setdefault("justification", "")

            texto_consulta = (
                _normalizar_texto_para_comparacao(
                    pergunta_limpa
                )
            )

            consulta_pca = (
                "plano de contratações anual"
                in texto_consulta
                or "plano de contratacoes anual"
                in texto_consulta
                or re.search(
                    r"\bpca\b",
                    texto_consulta,
                )
            )

            if consulta_pca:
                termos_cross_source = [
                    "contratos assinados",
                    "contratacoes realizadas",
                    "contratações realizadas",
                    "fornecedores contratados",
                    "comparar com contratos",
                ]

                if any(
                    termo in texto_consulta
                    for termo in termos_cross_source
                ):
                    resultado["routes"] = [
                        "agregada",
                        "estruturada",
                    ]
                else:
                    resultado["routes"] = ["agregada"]

            if resultado["is_refusal"]:
                resultado["routes"] = []

                resultado["filters"] = {
                    "uf": None,
                    "ano": None,
                    "valor_minimo": None,
                    "valor_maximo": None,
                    "modalidade": None,
                    "municipio": None,
                    "fornecedor": None,
                }

            elif not resultado["routes"]:
                resultado["routes"] = ["estruturada"]

            uso = getattr(resposta, "usage", None)

            tokens = {
                "prompt": getattr(uso, "prompt_tokens", 0) if uso else 0,
                "completion": getattr(uso, "completion_tokens", 0) if uso else 0,
                "total": getattr(uso, "total_tokens", 0) if uso else 0,
            }

            resultado["router_fallback"] = False

            observacao_roteamento["output"] = {
                "routes": resultado["routes"],
                "filters": resultado["filters"],
                "is_refusal": resultado["is_refusal"],
            }
            observacao_roteamento["tokens"] = tokens

    except Exception as erro:
        resultado = _roteamento_fallback(pergunta)
        resultado["router_fallback"] = True
        resultado["router_error"] = str(erro)

        tokens = {
            "prompt": 0,
            "completion": 0,
            "total": 0,
        }

    resultado["query"] = pergunta_limpa
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