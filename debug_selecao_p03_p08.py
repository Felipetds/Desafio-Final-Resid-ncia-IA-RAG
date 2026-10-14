import json

from openai import OpenAI
from src.generate import chamar_llm, OLLAMA_URL


PERGUNTAS = {
    "P03": (
        "O que a ata nº 00191/2026 da EBSERH registra sobre o "
        "objeto da aquisição e qual é o número de controle PNCP associado?"
    ),
    "P08": (
        "O que a ata nº 00137/2026 do INCA informa sobre o "
        "objeto adquirido e o fornecedor?"
    ),
}


with open(
    "validacao_p03_p08.json",
    "r",
    encoding="utf-8",
) as arquivo:
    dados = json.load(arquivo)


client = OpenAI(
    base_url=OLLAMA_URL,
    api_key="ollama",
)


for caso, pergunta in PERGUNTAS.items():

    print("\n" + "=" * 100)
    print(caso)
    print("=" * 100)

    evidencias = dados[caso]["evidences"]

    blocos = []

    for numero, evidencia in enumerate(evidencias, start=1):

        fonte = evidencia.get("fonte") or "fonte_desconhecida"

        base = (
            evidencia.get("base")
            or evidencia.get("natureza")
            or "desconhecida"
        )

        chunk_id = evidencia.get("chunk_id")
        texto = evidencia.get("trecho", "")

        blocos.append(
            f"EVIDÊNCIA {numero}\n"
            f"Fonte: {fonte}\n"
            f"Base: {base}\n"
            f"Chunk ID: {chunk_id}\n"
            f"Conteúdo:\n{texto}"
        )

    contexto = "\n\n---\n\n".join(blocos)

    print("Enviando para o modelo...")

    try:

        resposta = chamar_llm(
            pergunta=pergunta,
            contexto=contexto,
            client=client,
            modo_extrativo=True,
        )

        conteudo = resposta.choices[0].message.content

        print("\nRESPOSTA BRUTA:")
        print(conteudo)

        print("\nREPRESENTAÇÃO EXATA:")
        print(repr(conteudo))

        try:
            parsed = json.loads(conteudo)

            print("\nJSON INTERPRETADO:")
            print(json.dumps(
                parsed,
                ensure_ascii=False,
                indent=2,
            ))

        except Exception as erro:
            print("\nNÃO FOI POSSÍVEL INTERPRETAR COMO JSON:")
            print(type(erro).__name__, erro)

    except Exception as erro:

        print("\nERRO NA CHAMADA:")
        print(type(erro).__name__, erro)