# Instruções de Geração e Carregamento de Artefatos (v3)

## 1. Geração dos Artefatos
Para reproduzir a ingestão e indexação do zero, garantindo a integridade do cache:
1. **Ingestão:** Execute `python src/ingest.py`. O script processa os arquivos brutos v3 e gera `chunks_teste.json`.
2. **Indexação:** Execute `python src/index.py`. O sistema criará as chaves de cache (SHA-256) para cada chunk. Os embeddings só serão recalculados via API se o texto ou o modelo sofrerem alterações.
3. **Saída:** Os artefatos finais (`faiss_index.bin`, `bm25_index.pkl`, `chunk_ids.json` e `cache_embeddings.json`) são consolidados no disco.

## 2. Carregamento (Recuperação)
Durante as consultas, o módulo `src/retrieve.py` utiliza a função `carregar_artefatos()` para carregar os índices vetoriais e léxicos diretamente da memória persistente. **Nenhum índice é recriado em tempo de execução**, garantindo baixa latência e preservando os artefatos em disco.
