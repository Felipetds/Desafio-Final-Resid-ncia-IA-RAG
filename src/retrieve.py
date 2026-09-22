import json
import os
import pickle
import re
import time
from typing import Any, Dict, List, Optional, Set

import faiss
import numpy as np
from openai import OpenAI

from src.router import OLLAMA_URL, analisar_consulta

try:
    from . import obs
    from .schema import RetrievalResult
except ImportError:  # permite "python src/retrieve.py" direto, sem pacote.
    import obs
    from schema import RetrievalResult


EMBEDDING_MODEL = "xagi/qwen3-embedding:0.6b-q4_k_m"

CAMINHO_CHUNKS = "data/processed/chunks_teste.json"
CAMINHO_FAISS = "data/indices/faiss_index.bin"
CAMINHO_BM25 = "data/indices/bm25_index.pkl"
CAMINHO_IDS = "data/indices/chunk_ids.json"

ROTAS_VALIDAS = {
    "normativa",
    "estruturada",
    "conversacional",
    "agregada",
}


def tokenizar(texto: str) -> List[str]:
    """
    Tokenização simples para consultas BM25 em português.
    """
    return re.findall(
        r"\b[\wÀ-ÿ]+\b",
        texto.lower(),
        flags=re.UNICODE,
    )


def carregar_artefatos(
    caminho_chunks: str = CAMINHO_CHUNKS,
    caminho_faiss: str = CAMINHO_FAISS,
    caminho_bm25: str = CAMINHO_BM25,
    caminho_ids: str = CAMINHO_IDS,
):
    """
    Carrega chunks e índices já persistidos.
    Não refaz a indexação.
    """
    caminhos = [
        caminho_chunks,
        caminho_faiss,
        caminho_bm25,
        caminho_ids,
    ]

    faltando = [caminho for caminho in caminhos if not os.path.exists(caminho)]

    if faltando:
        raise FileNotFoundError(
            "Artefatos não encontrados: "
            + ", ".join(faltando)
            + ". Execute primeiro ingest.py e index.py."
        )

    with open(caminho_chunks, "r", encoding="utf-8") as arquivo:
        chunks = json.load(arquivo)

    with open(caminho_ids, "r", encoding="utf-8") as arquivo:
        ids = json.load(arquivo)

    indice_faiss = faiss.read_index(caminho_faiss)

    # O pickle deve ser carregado somente de arquivo criado pela própria equipe.
    with open(caminho_bm25, "rb") as arquivo:
        indice_bm25 = pickle.load(arquivo)

    if len(ids) != len(chunks):
        raise ValueError(
            f"Inconsistência: {len(ids)} IDs e {len(chunks)} chunks."
        )

    if indice_faiss.ntotal != len(ids):
        raise ValueError(
            f"Inconsistência: FAISS possui {indice_faiss.ntotal} vetores, "
            f"mas existem {len(ids)} IDs."
        )

    chunks_por_id = {}

    for chunk in chunks:
        chunk_id = (
            chunk.get("metadata", {}).get("chunk_id")
            or chunk.get("chunk_id")
        )

        if not chunk_id:
            raise ValueError(
                "Chunk sem chunk_id no nível principal ou em metadata."
            )

        chunks_por_id[chunk_id] = chunk

    return chunks, chunks_por_id, ids, indice_faiss, indice_bm25


def identificar_natureza(chunk: Dict[str, Any]) -> Optional[str]:
    """
    Descobre a natureza pelo metadado ou pelo nome da base.
    """
    metadata = chunk.get("metadata", {})

    natureza = str(metadata.get("natureza", "")).lower().strip()

    if natureza in ROTAS_VALIDAS:
        return natureza

    base_id = str(metadata.get("base_id", "")).lower()

    for rota in ROTAS_VALIDAS:
        if rota in base_id:
            return rota

    return None


def _converter_numero(valor: Any) -> Optional[float]:
    if valor is None:
        return None

    if isinstance(valor, (int, float)):
        return float(valor)

    texto = str(valor).strip()
    texto = texto.replace("R$", "").replace(" ", "")

    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")

    try:
        return float(texto)
    except ValueError:
        return None


def chunk_atende_rotas(
    chunk: Dict[str, Any],
    rotas: List[str],
    exigir_natureza: bool = False,
) -> bool:
    """
    exigir_natureza=False (padrão): mantém o comportamento atual, usado
    pelas fixtures e pelos testes — chunk sem "natureza" continua elegível.

    exigir_natureza=True: para uso com os dados reais das quatro bases.
    Um chunk sem "natureza" identificável é bloqueado (não passa no
    filtro de rota), em vez de ser aceito por padrão. Ativar isso deve
    ser combinado com a Janice e o Eridalgo assim que o corpus real
    estiver disponível, pois hoje ele bloquearia toda a fixture de teste.
    """
    if not rotas:
        return True

    natureza = identificar_natureza(chunk)

    if natureza is None:
        return not exigir_natureza

    return natureza in rotas


def chunk_atende_filtros(
    chunk: Dict[str, Any],
    filtros: Dict[str, Any],
) -> bool:
    metadata = chunk.get("metadata", {})

    sensitivity = str(
        metadata.get("sensitivity", "publico")
    ).lower()

    if sensitivity not in {"publico", "público"}:
        return False

    uf = filtros.get("uf")

    if uf and metadata.get("uf"):
        if str(metadata["uf"]).upper() != str(uf).upper():
            return False

    ano = filtros.get("ano")

    if ano and metadata.get("ano") is not None:
        try:
            if int(metadata["ano"]) != int(ano):
                return False
        except (TypeError, ValueError):
            return False

    valor = _converter_numero(
        metadata.get("valor", metadata.get("valor_total"))
    )

    valor_minimo = _converter_numero(filtros.get("valor_minimo"))
    valor_maximo = _converter_numero(filtros.get("valor_maximo"))

    if valor_minimo is not None and valor is not None:
        if valor < valor_minimo:
            return False

    if valor_maximo is not None and valor is not None:
        if valor > valor_maximo:
            return False

    campos_textuais = [
        "modalidade",
        "municipio",
        "fornecedor",
    ]

    for campo in campos_textuais:
        procurado = filtros.get(campo)
        existente = metadata.get(campo)

        if procurado and existente:
            if str(procurado).lower() not in str(existente).lower():
                return False

    return True


def gerar_embedding_consulta(
    pergunta: str,
    client: OpenAI,
) -> np.ndarray:
    resposta = client.embeddings.create(
        input=[pergunta],
        model=EMBEDDING_MODEL,
    )

    vetor = np.array(
        [resposta.data[0].embedding],
        dtype="float32",
    )

    return vetor


def busca_densa(
    pergunta: str,
    client: OpenAI,
    indice_faiss,
    ids: List[str],
    fetch_k: int = 50,
) -> List[Dict[str, Any]]:
    vetor = gerar_embedding_consulta(pergunta, client)

    quantidade = min(fetch_k, indice_faiss.ntotal)

    distancias, posicoes = indice_faiss.search(
        vetor,
        quantidade,
    )

    resultados = []

    for distancia, posicao in zip(distancias[0], posicoes[0]):
        if posicao < 0 or posicao >= len(ids):
            continue

        resultados.append(
            {
                "chunk_id": ids[posicao],
                "dense_distance": float(distancia),
            }
        )

    return resultados


def busca_bm25(
    pergunta: str,
    indice_bm25,
    ids: List[str],
    fetch_k: int = 50,
) -> List[Dict[str, Any]]:
    tokens = tokenizar(pergunta)
    scores = indice_bm25.get_scores(tokens)

    posicoes = np.argsort(scores)[::-1][: min(fetch_k, len(ids))]

    resultados = []

    for posicao in posicoes:
        resultados.append(
            {
                "chunk_id": ids[int(posicao)],
                "bm25_score": float(scores[int(posicao)]),
            }
        )

    return resultados


def filtrar_resultados(
    resultados: List[Dict[str, Any]],
    chunks_por_id: Dict[str, Dict[str, Any]],
    rotas: List[str],
    filtros: Dict[str, Any],
    exigir_natureza: bool = False,
) -> List[Dict[str, Any]]:
    saida = []

    for resultado in resultados:
        chunk = chunks_por_id.get(resultado["chunk_id"])

        if not chunk:
            continue

        if not chunk_atende_rotas(chunk, rotas, exigir_natureza=exigir_natureza):
            continue

        if not chunk_atende_filtros(chunk, filtros):
            continue

        saida.append(resultado)

    return saida


def fusao_rrf(
    resultados_densos: List[Dict[str, Any]],
    resultados_bm25: List[Dict[str, Any]],
    k_rrf: int = 60,
) -> List[Dict[str, Any]]:
    """
    Reciprocal Rank Fusion:

        score = soma(1 / (k + posição_no_ranking))
    """
    scores: Dict[str, float] = {}
    origens: Dict[str, Set[str]] = {}
    detalhes: Dict[str, Dict[str, Any]] = {}

    for posicao, item in enumerate(resultados_densos, start=1):
        chunk_id = item["chunk_id"]

        scores[chunk_id] = scores.get(chunk_id, 0.0) + (
            1.0 / (k_rrf + posicao)
        )

        origens.setdefault(chunk_id, set()).add("dense")
        detalhes.setdefault(chunk_id, {}).update(item)

    for posicao, item in enumerate(resultados_bm25, start=1):
        chunk_id = item["chunk_id"]

        scores[chunk_id] = scores.get(chunk_id, 0.0) + (
            1.0 / (k_rrf + posicao)
        )

        origens.setdefault(chunk_id, set()).add("bm25")
        detalhes.setdefault(chunk_id, {}).update(item)

    ranking = sorted(
        scores.items(),
        key=lambda elemento: elemento[1],
        reverse=True,
    )

    return [
        {
            "chunk_id": chunk_id,
            "rrf_score": score,
            "retrieval_sources": sorted(origens[chunk_id]),
            **detalhes.get(chunk_id, {}),
        }
        for chunk_id, score in ranking
    ]


def _validar_com_retrieval_result(resultado: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valida explicitamente a saída de recuperar_evidencias contra o schema
    RetrievalResult (src/schema.py) antes de devolvê-la para quem chamou
    (por exemplo o generate.py). Isso garante que campos obrigatórios,
    tipos e as regras de consistência do schema (como "recusa não pode
    ter evidências") sejam sempre respeitados na saída real do pipeline,
    e não só nos testes.
    """
    validado = RetrievalResult(**resultado)
    return validado.model_dump()


def recuperar_evidencias(
    pergunta: str,
    top_k: int = 5,
    fetch_k: int = 50,
    client: OpenAI | None = None,
    exigir_natureza: bool = False,
) -> Dict[str, Any]:
    """
    Executa roteamento, Dense, BM25, filtros e RRF.

    exigir_natureza: repassado para filtrar_resultados/chunk_atende_rotas.
    Mantém-se False por padrão para não quebrar a fixture atual (chunks
    sem "natureza" continuam elegíveis). Deve ser ativado como True ao
    validar com os dados reais das quatro bases (ver Janice/Eridalgo),
    quando um chunk sem natureza identificável deve ser bloqueado em vez
    de passar por padrão.
    """
    inicio = time.perf_counter()
    run_id = obs.novo_run_id()

    if client is None:
        client = OpenAI(
            base_url=OLLAMA_URL,
            api_key="ollama",
        )

    analise = analisar_consulta(
        pergunta=pergunta,
        client=client,
    )

    query_id = analise["query_id"]

    if analise.get("is_refusal"):
        resultado = {
            "query": pergunta,
            "query_id": query_id,
            "routes": analise["routes"],
            "filters": analise["filters"],
            "is_refusal": True,
            "refusal_reason": analise.get("refusal_reason"),
            "evidences": [],
            "stage": "fusao_rrf",
            "latencia_ms": round(
                (time.perf_counter() - inicio) * 1000,
                2,
            ),
        }
        return _validar_com_retrieval_result(resultado)

    (
        chunks,
        chunks_por_id,
        ids,
        indice_faiss,
        indice_bm25,
    ) = carregar_artefatos()

    with obs.observar_etapa(
        run_id=run_id,
        query_id=query_id,
        stage="retrieval_denso",
        input_data={"pergunta": pergunta, "fetch_k": fetch_k},
    ) as observacao_densa:
        resultados_densos = busca_densa(
            pergunta=pergunta,
            client=client,
            indice_faiss=indice_faiss,
            ids=ids,
            fetch_k=fetch_k,
        )
        observacao_densa["output"] = {
            "candidatos": len(resultados_densos),
        }

    with obs.observar_etapa(
        run_id=run_id,
        query_id=query_id,
        stage="retrieval_bm25",
        input_data={"pergunta": pergunta, "fetch_k": fetch_k},
    ) as observacao_bm25:
        resultados_bm25 = busca_bm25(
            pergunta=pergunta,
            indice_bm25=indice_bm25,
            ids=ids,
            fetch_k=fetch_k,
        )
        observacao_bm25["output"] = {
            "candidatos": len(resultados_bm25),
        }

    rotas = analise.get("routes", [])
    filtros = analise.get("filters", {})

    with obs.observar_etapa(
        run_id=run_id,
        query_id=query_id,
        stage="fusao_rrf",
        input_data={
            "routes": rotas,
            "filters": filtros,
            "top_k": top_k,
        },
    ) as observacao_fusao:
        resultados_densos = filtrar_resultados(
            resultados=resultados_densos,
            chunks_por_id=chunks_por_id,
            rotas=rotas,
            filtros=filtros,
            exigir_natureza=exigir_natureza,
        )

        resultados_bm25 = filtrar_resultados(
            resultados=resultados_bm25,
            chunks_por_id=chunks_por_id,
            rotas=rotas,
            filtros=filtros,
            exigir_natureza=exigir_natureza,
        )

        ranking_rrf = fusao_rrf(
            resultados_densos=resultados_densos,
            resultados_bm25=resultados_bm25,
        )

        evidencias = []

        for item in ranking_rrf[:top_k]:
            chunk = chunks_por_id[item["chunk_id"]]
            metadata = chunk.get("metadata", {})

            evidencias.append(
                {
                    "chunk_id": item["chunk_id"],
                    "text": chunk.get("text", ""),
                    "rrf_score": round(item["rrf_score"], 6),
                    "retrieval_sources": item["retrieval_sources"],
                    "dense_distance": item.get("dense_distance"),
                    "bm25_score": item.get("bm25_score"),
                    "source_file": metadata.get("source_file"),
                    "doc_type": metadata.get("doc_type"),
                    "sensitivity": metadata.get(
                        "sensitivity",
                        "publico",
                    ),
                    "base_id": metadata.get("base_id"),
                    "natureza": identificar_natureza(chunk),
                    "metadata": metadata,
                }
            )

        observacao_fusao["output"] = {
            "dense_candidates": len(resultados_densos),
            "bm25_candidates": len(resultados_bm25),
            "rrf_candidates": len(ranking_rrf),
            "returned": len(evidencias),
        }

    resultado = {
        "query": pergunta,
        "query_id": query_id,
        "routes": rotas,
        "filters": filtros,
        "router_justification": analise.get("justification"),
        "router_fallback": analise.get("router_fallback", False),
        "is_refusal": False,
        "refusal_reason": None,
        "evidences": evidencias,
        "retrieval_summary": {
            "dense_candidates": len(resultados_densos),
            "bm25_candidates": len(resultados_bm25),
            "rrf_candidates": len(ranking_rrf),
            "returned": len(evidencias),
        },
        "stage": "fusao_rrf",
        "latencia_ms": round(
            (time.perf_counter() - inicio) * 1000,
            2,
        ),
    }

    return _validar_com_retrieval_result(resultado)


if __name__ == "__main__":
    consulta = input("Digite uma pergunta: ")

    resultado = recuperar_evidencias(
        pergunta=consulta,
        top_k=5,
    )

    print(json.dumps(resultado, ensure_ascii=False, indent=2))
