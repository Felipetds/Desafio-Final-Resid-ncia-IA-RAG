
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import time

repo = Path("/content/repositorio1")
sys.path.insert(0, str(repo))

from src import generate, obs
from src.schema import SourceEvidence

destino = Path(sys.argv[1])
preparacao = json.loads(
    (destino / "preparacao.json").read_text(encoding="utf-8")
)
commit = subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=repo, text=True
).strip()
assert commit == preparacao["commit_executor"]

base = Path("/content/drive/MyDrive/rag_grande_desafio")
comparacao = base / "comparacao_recuperacao_20261019T181107547626Z"
arquivo_chunks = (
    base / "ENTREGA_EQUIPE_2026-10-16/pacote_v3_2172/"
    "data/processed/chunks_teste.json"
)
sha_chunks = hashlib.sha256(arquivo_chunks.read_bytes()).hexdigest()
assert sha_chunks == (
    "dcdcc7a0f8e34da1d0824b5322b6e37306c34e2d53d107c1ca067bc2771c8404"
)

chunks = json.loads(arquivo_chunks.read_text(encoding="utf-8"))
if isinstance(chunks, dict):
    chunks = chunks["chunks"]
assert isinstance(chunks, list) and len(chunks) == 2172

por_id = {}
for chunk in chunks:
    metadata = chunk.get("metadata") or {}
    identificador = (
        chunk.get("chunk_id") or chunk.get("id") or metadata.get("chunk_id")
    )
    assert identificador and identificador not in por_id
    por_id[identificador] = chunk
assert len(por_id) == 2172

logs = destino / "logs"
logs.mkdir(exist_ok=True)
obs.PASTA_LOGS = logs

assert generate.GENERATION_MODEL == "qcwind/qwen3-8b-instruct-Q4-K-M"

resultados_rankings = json.loads(
    (comparacao / "resultados.json").read_text(encoding="utf-8")
)
assert len(resultados_rankings) == 6
metodos = ("vetorial", "bm25", "rrf", "rrf_rerank")

def evidencia(identificador):
    chunk = por_id[identificador]
    metadata = dict(chunk.get("metadata") or {})

    def campo(nome, padrao=None):
        valor = chunk.get(nome)
        return valor if valor is not None else metadata.get(nome, padrao)

    texto = chunk.get("text")
    assert isinstance(texto, str) and texto.strip(), (
        f"Chunk sem campo text válido: {identificador}"
    )
    return SourceEvidence(
        chunk_id=identificador,
        text=texto,
        source_file=campo("source_file"),
        doc_type=campo("doc_type"),
        sensitivity=campo("sensitivity", "publico"),
        base_id=campo("base_id"),
        natureza=campo("natureza"),
        metadata=metadata,
    )

registros = []
interromper = False

for caso in resultados_rankings:
    for metodo in metodos:
        nome = f'{caso["caso"]}_{metodo}'
        arquivo = destino / f"{nome}.json"

        # Não repete chamadas já registradas em uma retomada.
        if arquivo.exists():
            registro = json.loads(arquivo.read_text(encoding="utf-8"))
            assert registro["commit_executor"] == commit
            assert registro["sha256_chunks"] == sha_chunks
            registros.append(registro)
            print(nome, "| resultado anterior preservado", flush=True)
            continue

        ids = caso["metodos"][metodo]["ids"][:3]
        assert len(ids) == len(set(ids)) and ids
        evidencias = [evidencia(i) for i in ids]
        rotas = list(dict.fromkeys(e.natureza for e in evidencias))
        assert all(rotas), f"Natureza ausente: {nome}"

        run_id = obs.novo_run_id()
        entrada = {
            "query": caso["pergunta"],
            "query_id": f"q_comparacao_{run_id}",
            "routes": rotas,
            "filters": {},
            "evidences": [e.model_dump() for e in evidencias],
        }

        print("Gerando:", nome, flush=True)
        inicio = time.perf_counter()
        resposta = generate.gerar_resposta(
            resultado_recuperacao=entrada,
            run_id=run_id,
            modo_extrativo=True,
        )
        saida = resposta.model_dump()

        eventos = []
        for log in logs.glob("*.jsonl"):
            for linha in log.read_text(encoding="utf-8").splitlines():
                if linha.strip():
                    evento = json.loads(linha)
                    if evento.get("run_id") == run_id:
                        eventos.append(evento)

        erros = [
            {"stage": e.get("stage"), "output": e.get("output")}
            for e in eventos if e.get("status") == "erro"
        ]
        resposta_texto = generate.mascarar_dados_pessoais(
            saida.get("answer", "")
        )
        citados = re.findall(r"\[Fonte:\s*([^\]]+)\]", resposta_texto)
        fontes_usadas = [
            e.get("chunk_id")
            for e in saida.get("sources_used", [])
            if isinstance(e, dict)
        ]

        registro = {
            "caso": caso["caso"],
            "pergunta": caso["pergunta"],
            "metodo": metodo,
            "top_k": 3,
            "commit_executor": commit,
            "sha256_chunks": sha_chunks,
            "run_id": run_id,
            "ids_entrada": ids,
            "cobertura_ranking": caso["metodos"][metodo]["top_3"],
            "protocolo": (
                "Geração extrativa real sobre ranking preservado; "
                "sem nova busca, rerank ou resgate de cobertura."
            ),
            "tempo_s": round(time.perf_counter() - inicio, 3),
            "answer": resposta_texto,
            "stage": saida.get("stage"),
            "confidence_level": saida.get("confidence_level"),
            "tokens": saida.get("tokens"),
            "citacoes": citados,
            "sources_used_ids": fontes_usadas,
            "citacoes_pertencem_a_entrada": (
                bool(citados) and set(citados).issubset(ids)
            ),
            "erros_registrados": erros,
            "avaliacao_conteudo": "pendente",
        }
        arquivo.write_text(
            json.dumps(registro, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        registros.append(registro)
        print(
            nome, "|", registro["tempo_s"], "s",
            "| citações:", len(citados),
            "| erros:", len(erros),
            flush=True,
        )

        # Falhas de serviço suspendem a rodada; não são corrigidas por repetição.
        if any(e.get("stage") == "geracao" for e in erros):
            print("Falha de geração; rodada suspensa para diagnóstico.", flush=True)
            interromper = True
            break
    if interromper:
        break

(destino / "respostas.json").write_text(
    json.dumps(registros, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print("Resultados registrados:", len(registros), "de 24.", flush=True)
print("Avaliação de conteúdo ainda pendente.", flush=True)
