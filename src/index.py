import os
import json
import time
import faiss
import numpy as np
import pickle
from openai import OpenAI
from rank_bm25 import BM25Okapi

OLLAMA_URL = "http://ecoa-llm.duckdns.org:11434/v1"
EMBEDDING_MODEL = "xagi/qwen3-embedding:0.6b-q4_k_m"
CACHE_FILE = "data/indices/cache_embeddings.json"

def carregar_cache():
    """Carrega o cache do disco, se existir."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_cache(cache):
    """Salva o dicionário de cache no disco."""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f)

def gerar_indices():
    print("Iniciando a indexação com CACHE DE EMBEDDINGS (FAISS + BM25)...")
    
    caminho_entrada = "data/processed/chunks_teste.json"
    if not os.path.exists(caminho_entrada):
        print(f"❌ Erro: Arquivo {caminho_entrada} não encontrado.")
        return
        
    with open(caminho_entrada, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    print(f"Total de chunks para processar: {len(chunks)}")
    
    # 1. Gerenciamento do Cache
    cache_embeddings = carregar_cache()
    
    textos = []
    ids_lista = []
    chunks_para_api = []
    
    for c in chunks:
        chunk_id = c["metadata"]["chunk_id"]
        texto = c["text"]
        textos.append(texto)
        ids_lista.append(chunk_id)
        
        # Filtra: Só enviamos para a API se não estiver no cache em disco
        if chunk_id not in cache_embeddings:
            chunks_para_api.append({"id": chunk_id, "text": texto})
            
    print(f"Chunks já carregados do cache local: {len(chunks) - len(chunks_para_api)}")
    print(f"Chunks novos enviados para a API: {len(chunks_para_api)}")
    
    # 2. Processar na API apenas os chunks novos (Batching + Rate Limiting)
    if chunks_para_api:
        client = OpenAI(base_url=OLLAMA_URL, api_key="ollama")
        tamanho_lote = 50
        
        for i in range(0, len(chunks_para_api), tamanho_lote):
            lote = chunks_para_api[i:i + tamanho_lote]
            lote_textos = [item["text"] for item in lote]
            
            print(f"⏳ Processando lote novo na API ({len(lote)} embeddings)...")
            try:
                response = client.embeddings.create(
                    input=lote_textos,
                    model=EMBEDDING_MODEL
                )
                for j, data in enumerate(response.data):
                    # Grava no dicionário usando o chunk_id como chave única
                    cache_embeddings[lote[j]["id"]] = data.embedding
            except Exception as e:
                print(f"❌ Erro ao consultar a API: {e}")
                
            # Rate limiting respeitado conforme o checklist
            if i + tamanho_lote < len(chunks_para_api):
                print("🛑 Aguardando 10 segundos (Rate Limiting)...")
                time.sleep(10)
                
        # Persiste o cache atualizado no Drive
        salvar_cache(cache_embeddings)
        print("💾 Arquivo de cache em disco atualizado com sucesso!")
        
    # 3. Reconstruir a matriz final garantindo a ordem dos IDs originais
    embeddings_finais = []
    for chunk_id in ids_lista:
        if chunk_id in cache_embeddings:
            embeddings_finais.append(cache_embeddings[chunk_id])
        else:
            print(f"⚠️ Erro fatal: Embedding de {chunk_id} sumiu!")
            return
            
    # 4. Construção e Persistência do Índice FAISS e BM25
    print("\nConstruindo os índices finais...")
    dimensao = len(embeddings_finais[0])
    matriz_vetores = np.array(embeddings_finais).astype('float32')
    
    indice_faiss = faiss.IndexFlatL2(dimensao)
    indice_faiss.add(matriz_vetores)
    
    corpus_tokenizado = [texto.lower().split(" ") for texto in textos]
    indice_bm25 = BM25Okapi(corpus_tokenizado)
    
    pasta_indices = "data/indices"
    caminho_faiss = os.path.join(pasta_indices, "faiss_index.bin")
    caminho_bm25 = os.path.join(pasta_indices, "bm25_index.pkl")
    caminho_ids = os.path.join(pasta_indices, "chunk_ids.json")
    
    faiss.write_index(indice_faiss, caminho_faiss)
    with open(caminho_bm25, "wb") as f: pickle.dump(indice_bm25, f)
    with open(caminho_ids, "w", encoding="utf-8") as f: json.dump(ids_lista, f, indent=4)
        
    print(f"✅ Pipeline otimizado finalizado com sucesso!")

if __name__ == "__main__":
    gerar_indices()
