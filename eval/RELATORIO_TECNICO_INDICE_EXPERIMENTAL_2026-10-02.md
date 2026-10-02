# Relatório técnico — Corpus e Avaliação V3

**Data:** 02/10/2026  
**Projeto:** Grande Desafio — Adaptive RAG  
**Cenário:** Contratações Públicas do Estado do RJ  
**Responsabilidade:** Corpus e Avaliação  
**Status:** Validação experimental parcial concluída.

## 1. Integridade do corpus

- Corpus processado: 38,619 chunks.
- Identificadores únicos: 38.619.
- IDs duplicados: zero, conforme Passo 79.
- Naturezas: normativa, estruturada, conversacional e agregada.
- Cache inicial identificado: 60 embeddings.
- Modelo: xagi/qwen3-embedding:0.6b-q4_k_m.
- Dimensão dos vetores: 1.024.

## 2. Embeddings e persistência

- Passo 80: geração controlada de dez embeddings.
- Passo 81: mais 30 embeddings, com três checkpoints.
- Passo 83: mais 40 embeddings, distribuídos pelas quatro naturezas.
- Cache experimental atual: 140 embeddings.
- Embeddings ainda não produzidos: 38479.
- Cache original preservado.
- Cache de trabalho salvo no Google Drive.

### Distribuição experimental

| Natureza | Embeddings |
|---|---:|
| Normativa | 10 |
| Conversacional | 10 |
| Estruturada | 110 |
| Agregada | 10 |
| **Total** | **140** |

## 3. Indexação híbrida experimental

Foi construído um índice isolado em
`data/indices/experimental_v3/`, sem sobrescrever
os artefatos de produção.

Artefatos:

- `faiss_index.bin`
- `bm25_index.pkl`
- `chunk_ids.json`
- `chunks_experimental_v3.json`
- `manifesto_experimental.json`

Validações do Passo 85:

- FAISS: 140 vetores de dimensão 1.024.
- BM25: 140 documentos.
- IDs: 140.
- Chunks: 140.
- Alinhamento posicional: aprovado.

## 4. Testes funcionais

### Passo 86 — Integração

A função original `src.retrieve.carregar_artefatos()`
carregou corretamente os quatro artefatos experimentais.

A busca BM25 retornou cinco resultados rastreáveis.

### Passo 87 — Recuperação normativa

Consulta experimental sobre pregão eletrônico
e Lei 14.133/2021.

- Busca densa: 140 candidatos.
- BM25: 140 candidatos.
- Após filtro normativo: dez candidatos em cada busca.
- Fusão RRF: dez documentos normativos.
- Tempo observado: 0,67 segundo.

Observação: os primeiros documentos não foram
necessariamente os artigos mais específicos sobre pregão.
A cobertura normativa parcial limita a avaliação
de relevância.

### Passo 88 — Recuperação multirrota

- Busca densa: 140 candidatos.
- BM25: 140 candidatos.
- Ranking RRF: 140 documentos.
- Evidências finais: oito.
- Estruturada: cinco.
- Normativa: uma.
- Conversacional: uma.
- Agregada: uma.
- Tempo observado: 1,24 segundo.

A seleção multirrota contemplou as quatro naturezas.

## 5. Limitações e pendências

1. O índice experimental representa apenas 140
   dos 38.619 chunks do corpus.
2. Faltam 38479 embeddings para cobertura integral.
3. Não foi demonstrada correspondência factual
   entre todas as evidências selecionadas no Passo 88.
4. A qualidade semântica do ranking exige avaliação
   com perguntas e referências documentais.
5. A geração final, as recusas e os guardrails
   ainda precisam de validação ponta a ponta.
6. O índice experimental não deve ser apresentado
   como índice integral de produção.
7. O código original de `src/index.py` e
   `src/retrieve.py` foi preservado.

## 6. Próximas atividades

- Expandir os embeddings com checkpoints no Drive.
- Melhorar a cobertura das naturezas menos representadas.
- Testar relevância e precisão das evidências.
- Integrar a recuperação híbrida à suíte de avaliação.
- Validar casos cross-source sem criar vínculos artificiais.
- Executar testes ponta a ponta após integração.

**Conclusão:** a integração experimental FAISS + BM25,
a filtragem normativa e a seleção multirrota foram
executadas com sucesso na amostra parcial.
