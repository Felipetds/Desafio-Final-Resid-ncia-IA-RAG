import json

from openai import OpenAI
from src.generate import chamar_llm, OLLAMA_URL


# Lê o resultado que você acabou de gerar
with open(
    "validacao_p03_p08.json",
    "r",
    encoding="utf-8",
) as arquivo:
    dados = json.load(arquivo)


caso = dados["P08"]

pergunta = (
    "O que a ata nº 00137/2026 do INCA informa "
    "sobre o objeto adquirido e o fornecedor?"
)

evidencias = caso["evidences"]


# Reconstrói exatamente o contexto enviado ao gerador
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


client = OpenAI(
    base_url=OLLAMA_URL,
    api_key="ollama",
)


print("Enviando para o modelo...")

resposta = chamar_llm(
    pergunta=pergunta,
    contexto=contexto,
    client=client,
    modo_extrativo=True,
)

conteudo = resposta.choices[0].message.content


print("\n" + "=" * 80)
print("RESPOSTA BRUTA DO MODELO")
print("=" * 80)

print(conteudo)

print("\n" + "=" * 80)
print("REPRESENTAÇÃO EXATA")
print("=" * 80)

print(repr(conteudo))