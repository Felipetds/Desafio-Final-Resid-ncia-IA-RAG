import os
import json
import time
import faiss
import numpy as np
import pickle
from openai import OpenAI
from rank_bm25 import BM25Okapi

# Configuração da API do curso (Ollama compatível com OpenAI)
OLLAMA_URL = "http://ecoa-llm.duckdns.org:11434/v1"
EMBEDDING_MODEL = "xagi/qwen3-embedding:0.6b-q4_k_m"

def gerar_indices():
    print("Iniciando a indexação vetorial e esparsa (FAISS + BM25)...")
    
    # 1. Carregar os chunks processados pelo ingest.py
    caminho_entrada = "data/processed/chunks_teste.json"
    if not os.path.exists(caminho_entrada):
        print(f"❌ Erro: Arquivo {caminho_entrada} não encontrado. Rode o ingest.py primeiro!")
        return
        
    with open(caminho_entrada, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    print(f"Total de chunks carregados: {len(chunks)}")
    
    # CORREÇÃO: Agora busca o chunk_id corretamente dentro de 'metadata'
    textos = [c["text"] for c in chunks]
    ids_lista = [c["metadata"]["chunk_id"] for c in chunks]
    
    # 2. Configurar o cliente da API para embeddings densos
    client = OpenAI(base_url=OLLAMA_URL, api_key="ollama")
    
    embeddings_lista = []
    tamanho_lote = 50
    
    # 3. Processamento em Lotes (Batching) e Rate Limiting para o FAISS
    for i in range(0, len(chunks), tamanho_lote):
        lote_textos = textos[i:i + tamanho_lote]
        
        print(f"⏳ Processando lote densos {i//tamanho_lote + 1}...")
        try:
            response = client.embeddings.create(
                input=lote_textos,
                model=EMBEDDING_MODEL
            )
            for data in response.data:
                embeddings_lista.append(data.embedding)
        except Exception as e:
            print(f"❌ Erro ao processar lote de embeddings: {e}")
            
        if i + tamanho_lote < len(chunks):
            print("🛑 Aguardando 10 segundos (Rate Limiting)...")
            time.sleep(10)
            
    if not embeddings_lista:
        print("❌ Nenhum embedding foi gerado.")
        return
        
    # 4. Construção e Persistência do Índice FAISS (Denso)
    print("\nConstruindo o índice vetorial FAISS...")
    dimensao = len(embeddings_lista[0])
    matriz_vetores = np.array(embeddings_lista).astype('float32')
    
    indice_faiss = faiss.IndexFlatL2(dimensao)
    indice_faiss.add(matriz_vetores)
    
    # 5. Construção e Persistência do BM25 (Esparso / Palavras-chave)
    print("Construindo o índice esparso BM25...")
    # Tokenização simples baseada em espaço em branco para o BM25
    corpus_tokenizado = [texto.lower().split(" ") for texto in textos]
    indice_bm25 = BM25Okapi(corpus_tokenizado)
    
    # 6. Salvando todos os artefatos localmente
    pasta_indices = "data/indices"
    os.makedirs(pasta_indices, exist_ok=True)
    
    caminho_faiss = os.path.join(pasta_indices, "faiss_index.bin")
    caminho_bm25 = os.path.join(pasta_indices, "bm25_index.pkl")
    caminho_ids = os.path.join(pasta_indices, "chunk_ids.json")
    
    faiss.write_index(indice_faiss, caminho_faiss)
    
    # Salvando o objeto BM25 com pickle
    with open(caminho_bm25, "wb") as f:
        pickle.dump(indice_bm25, f)
        
    with open(caminho_ids, "w", encoding="utf-8") as f:
        json.dump(ids_lista, f, indent=4)
        
    print(f"✅ Sucesso absoluto!")
    print(f"   - FAISS salvo em: {caminho_faiss}")
    print(f"   - BM25 salvo em: {caminho_bm25}")
    print(f"   - IDs salvos em: {caminho_ids}")

if __name__ == "__main__":
    gerar_indices()
