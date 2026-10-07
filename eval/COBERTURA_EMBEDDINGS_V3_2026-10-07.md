# Cobertura de Embeddings — Corpus v3

**Data:** 07/10/2026  
**Projeto:** Grande Desafio — Adaptive RAG  
**Cenário:** Contratações Públicas do Estado do RJ  
**Frente:** Corpus, personas e avaliação  

## 1. Objetivo

Registrar a cobertura disponível dos embeddings do corpus v3 e a ampliação
prioritária realizada para apoiar os casos de avaliação das personas.

A estratégia adotada foi orientada pelos casos de avaliação, reutilizando
o cache existente e evitando a geração indiscriminada de embeddings para
todo o corpus.

## 2. Corpus v3

- Chunks únicos: 38.619
- Naturezas: estruturada, normativa, conversacional e agregada
- Dimensão dos embeddings: 1.024
- Modelo utilizado: `xagi/qwen3-embedding:0.6b-q4_k_m`

## 3. Situação inicial

O cache experimental utilizado como ponto de partida continha:

- 140 embeddings
- 110 estruturados
- 10 normativos
- 10 conversacionais
- 10 agregados
- cobertura global aproximada: 0,36%

O cache original foi preservado em:

`cache_embeddings_v3_trabalho.json`

## 4. Ampliação realizada por Janice

Foram produzidos 228 novos embeddings:

### Conversacional

Foram adicionados 21 embeddings:

- 8 — `ata_00001.pdf`
- 10 — `ata_00137.pdf`
- 2 — `ata_00191.pdf`
- 1 — `troca_mensagens_material_escritorio_001.txt`

Resultado:

- cobertura conversacional: 31/31
- cobertura: 100%

### Normativa

Foram adicionados 207 embeddings da:

`lei_14133_2021.html`

Resultado:

- cobertura normativa: 217/217
- cobertura: 100%

## 5. Cache ampliado de Janice

Arquivo:

`cache_embeddings_v3_janice_2026-10-07.json`

Resultado da auditoria:

| Natureza | Total de chunks | Embeddings | Pendentes | Cobertura |
|---|---:|---:|---:|---:|
| Agregada | 37.013 | 10 | 37.003 | 0,03% |
| Conversacional | 31 | 31 | 0 | 100,00% |
| Estruturada | 1.358 | 110 | 1.248 | 8,10% |
| Normativa | 217 | 217 | 0 | 100,00% |
| **Total** | **38.619** | **368** | **38.251** | **0,95%** |

Validações:

- 368 embeddings presentes;
- todos possuem dimensão 1.024;
- zero vetores inválidos;
- zero IDs do cache fora do corpus;
- cache original de 140 embeddings preservado.

## 6. Ampliação coordenada com Eridalgo

A ampliação prioritária foi dividida da seguinte forma:

- Janice: 228 embeddings — concluído;
- Eridalgo: 19 embeddings da base
  `itens_pe_038_26_2026.csv`.

A parcela de Eridalgo permanece separada deste cache até que sua execução
e validação sejam confirmadas.

Se os 19 embeddings forem incorporados posteriormente ao cache compartilhado,
a expansão prioritária conjunta prevista será de 247 novos embeddings,
totalizando 387 embeddings.

## 7. Recortes não expandidos integralmente

### Base agregada — PCA 2026

A base contém 36.994 chunks referentes ao PCA.

A expansão integral não foi priorizada nesta etapa porque o caso de avaliação
associado envolve principalmente cálculo determinístico de contagem e soma
sobre os registros completos.

### Base estruturada — PNCP

A natureza estruturada possui:

- 1.358 chunks;
- 110 embeddings disponíveis;
- 1.248 ainda sem embedding.

A expansão estruturada deverá ser orientada pelos casos de avaliação e pelas
necessidades da recuperação, evitando geração indiscriminada sem validação
de benefício.

## 8. Conclusão

A ampliação realizada priorizou as naturezas diretamente relevantes para a
avaliação documental.

A cobertura conversacional passou a 100% e a cobertura normativa passou a
100%, mantendo o cache experimental original preservado.

A cobertura global disponível no cache ampliado de Janice é de 368/38.619
chunks, equivalente a aproximadamente 0,95%.

Este resultado não representa cobertura integral do corpus v3. As limitações
das naturezas estruturada e agregada devem permanecer explícitas nos testes
e nos relatórios de avaliação.
