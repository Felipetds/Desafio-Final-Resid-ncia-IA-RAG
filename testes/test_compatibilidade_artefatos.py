import json
import faiss
import numpy as np
import pytest
import pickle

def test_alinhamento_e_unicidade():
    with open('data/v3_definitivo/chunk_ids.json', 'r') as f:
        chunk_ids = json.load(f)
    with open('data/v3_definitivo/chunks_teste.json', 'r') as f:
        chunks = json.load(f)
        
    index = faiss.read_index('data/v3_definitivo/faiss_index.bin')
    
    # Regra do plano: "Quantidade igual, sozinha, não comprova alinhamento"
    # Por isso, verificamos a quantidade E a ordem posicional
    assert len(chunk_ids) == len(chunks), "Erro: Quantidade de IDs difere dos chunks."
    assert len(chunk_ids) == index.ntotal, "Erro: Quantidade de IDs difere do índice FAISS."
    
    # Regra do plano: "não há conflitos entre vetores associados ao mesmo ID" (Unicidade)
    assert len(set(chunk_ids)) == len(chunk_ids), "Conflito: IDs duplicados encontrados!"
    
    # Regra do plano: correspondência da ordem
    assert chunks[0]["metadata"]["chunk_id"] == chunk_ids[0], "Desalinhamento na ordem dos metadados!"
    assert chunks[-1]["metadata"]["chunk_id"] == chunk_ids[-1], "Desalinhamento no final do índice!"

def test_vetores_dimensao_e_valores_finitos():
    index = faiss.read_index('data/v3_definitivo/faiss_index.bin')
    
    # Regra do plano: "vetores têm dimensão consistente e valores finitos"
    dimensao = index.d
    assert dimensao > 0, f"Dimensão inválida: {dimensao}"
    
    # Extrai os vetores originais armazenados no índice Flat
    # (reconstruct_n funciona em índices FlatL2)
    vetores = index.reconstruct_n(0, index.ntotal)
    
    # Verifica se existe algum Not-a-Number (NaN) ou Infinito (Inf)
    assert np.all(np.isfinite(vetores)), "Erro: Vetores contêm valores não finitos (NaN ou Inf)!"
