# Status do Projeto — Adaptive RAG para Contratações Públicas do RJ

**Residência TIC em Trilhas — PUC-Rio / Instituto ECOA**  
**Cenário:** Contratações Públicas do Estado do Rio de Janeiro  
**Período do desafio:** 14/09/2026 a 23/10/2026  
**Última atualização:** 28/09/2026

---

## 1. Objetivo do projeto

O projeto desenvolve um sistema de **Adaptive RAG** para responder perguntas sobre contratações públicas do Estado do Rio de Janeiro.

Antes de recuperar documentos, o sistema analisa a pergunta e seleciona uma ou mais bases conforme o tipo de evidência necessário.

O sistema trabalha com quatro naturezas de dados:

| Base | Conteúdo | Finalidade |
|---|---|---|
| Normativa | Lei nº 14.133/2021 e documentos legais | Regras, permissões, proibições e requisitos |
| Estruturada | Contratações publicadas no PNCP | Órgãos, municípios, modalidades, objetos, datas e valores |
| Conversacional | Atas e comunicações sintéticas | Informações registradas em documentos e comunicações |
| Agregada | PCA e valores homologados por item | Indicadores, itens planejados, valores e estatísticas |

---

## 2. Arquitetura do pipeline

```text
Pergunta do usuário
        ↓
Análise da consulta e guardrails
        ↓
Roteamento para uma ou mais bases
        ↓
Busca densa + busca BM25
        ↓
Filtros por metadados
        ↓
Fusão RRF
        ↓
Geração da resposta com fontes
        ↓
Validação do schema
        ↓
Interface e logs estruturados
```

O pipeline utiliza:

- `query_id` para identificar cada pergunta;
- `run_id` para relacionar todas as etapas da mesma execução;
- logs estruturados no formato JSONL;
- registro de latência, tokens, modelo, entrada e saída.

---

## 3. Estrutura do repositório

| Caminho | Responsabilidade |
|---|---|
| `corpus_manifest.yaml` | Declaração das bases e arquivos do corpus |
| `src/fetch_corpus.py` | Coleta, atualização e inventário |
| `src/ingest.py` | Extração, metadados e criação dos chunks |
| `src/index.py` | Cache de embeddings e índices FAISS/BM25 |
| `src/router.py` | Rotas, filtros e decisões de segurança |
| `src/retrieve.py` | Recuperação densa, BM25, filtros e RRF |
| `src/generate.py` | Geração da resposta com evidências |
| `src/schema.py` | Validação das estruturas de entrada e saída |
| `src/obs.py` | Observabilidade e logs JSONL |
| `app/pipeline_adapter.py` | Integração dos módulos |
| `app/app.py` | Interface Gradio |
| `testes/` | Testes unitários, de contrato e integração |
| `data/inventory/` | Inventários e diferenças entre versões |
| `acompanhamento/` | Registros individuais dos integrantes |
| `docs/` | Documentação técnica |

Os dados brutos, índices, cache e logs são produzidos localmente e não devem ser enviados ao GitHub.

---

## 4. Corpus utilizado

### 4.1 Arquivos disponíveis

| Natureza | Quantidade | Conteúdo |
|---|---:|---|
| Estruturada | 1 | JSON de contratações publicadas no PNCP |
| Normativa | 1 | HTML da Lei nº 14.133/2021 |
| Conversacional | 4 | Três atas em PDF e uma comunicação sintética |
| Agregada | 2 | PCA 2026 e itens homologados |
| **Total** | **8** | Arquivos distribuídos nas quatro bases |

### 4.2 Base estruturada

A coleta da base estruturada apresentou:

- 1.358 registros;
- 1.358 valores de `numeroControlePNCP` preenchidos;
- 1.358 identificadores únicos;
- nenhuma duplicação;
- 28 páginas coletadas;
- retentativas automáticas em falhas temporárias.

Durante a coleta ocorreram timeout e respostas HTTP 502 e 503. O mecanismo de retentativas permitiu concluir a operação.

---

## 5. Versionamento do corpus

O fluxo de atualização preservou a versão anterior e criou a versão v3.

### Comparação entre a v2 e a nova coleta

- 1.358 registros na v2;
- 1.358 registros na nova coleta;
- 0 IDs adicionados;
- 0 IDs removidos;
- 1.314 registros idênticos;
- 44 registros alterados.

As diferenças ocorreram principalmente em campos de atualização e valores informados pelo PNCP.

### Comparação dos arquivos da v2 com a v3

- 7 arquivos idênticos;
- 1 arquivo alterado;
- 0 arquivos adicionados;
- 0 arquivos removidos.

O arquivo alterado foi:

```text
contratacoes_publicacao.json
```

### Artefatos de versionamento

```text
corpus_manifest.yaml
CORPUS_INVENTORY.md
data/inventory/v3.json
data/inventory/DIFF_v2_v3.md
```

Os arquivos brutos continuam fora do GitHub porque `data/raw/` está no `.gitignore`.

---

## 6. Ingestão e chunks

A ingestão mais recente gerou **2.125 chunks**.

| Natureza | Quantidade |
|---|---:|
| Estruturada | 1.358 |
| Agregada | 519 |
| Normativa | 217 |
| Conversacional | 31 |
| **Total** | **2.125** |

### Validações realizadas

- 2.125 IDs preenchidos;
- 2.125 IDs únicos;
- nenhum ID duplicado;
- nenhum chunk sem texto;
- natureza registrada nos metadados;
- arquivo de origem registrado;
- tipo do documento registrado;
- sensibilidade registrada.

### Fatiamento dos PDFs

Inicialmente, os três PDFs conversacionais eram processados como chunks únicos muito grandes.

Após a correção:

- os PDFs foram divididos em chunks menores;
- o maior chunk conversacional ficou com aproximadamente 2.000 caracteres;
- não existem chunks de PDF acima de 3.000 caracteres;
- os metadados foram preservados.

---

## 7. Indexação e cache de embeddings

Os índices foram reconstruídos após a correção do fatiamento.

| Artefato | Quantidade |
|---|---:|
| Chunks | 2.125 |
| Vetores FAISS | 2.125 |
| Documentos BM25 | 2.125 |
| IDs persistidos | 2.125 |
| IDs únicos | 2.125 |

### Funcionamento do cache

Na reconstrução:

- 1.575 embeddings válidos foram inicialmente preservados;
- somente os chunks novos ou alterados foram enviados ao endpoint;
- o cache foi atualizado em disco.

Na execução seguinte:

- 2.125 embeddings foram carregados do cache;
- 0 chunks foram enviados novamente à API.

Isso confirma que o cache evita reprocessamento desnecessário.

---

## 8. Roteamento adaptativo

O roteador seleciona a base conforme o tipo de evidência necessário.

| Pergunta | Rota esperada |
|---|---|
| Quais contratações envolvem serviços de tecnologia? | Estruturada |
| O que a Lei nº 14.133 estabelece sobre licitações? | Normativa |
| O que foi registrado nas atas sobre aquisições? | Conversacional |
| Quais itens aparecem no Plano de Contratações Anual? | Agregada |
| Sou MEI e existe algum pregão aberto? | Normativa + estruturada |
| Esse contrato foi uma fraude? | Recusa |

Também foram implementados:

- normalização das rotas;
- suporte a múltiplas rotas;
- extração de filtros;
- filtros por ano, modalidade, município, fornecedor e valor;
- interpretação de valores como `R$ 500 mil`;
- interpretação de valores como `R$ 1,5 milhão`;
- fallback quando o modelo não responde;
- regras de recusa.

---

## 9. Recuperação híbrida

O recuperador combina:

1. busca densa por embeddings;
2. busca lexical BM25;
3. filtragem por metadados;
4. fusão por Reciprocal Rank Fusion — RRF;
5. seleção das melhores evidências conforme o `top_k`.

### Resultados confirmados

- recuperação estruturada com evidências estruturadas;
- recuperação normativa com evidências normativas;
- recuperação agregada com evidências agregadas;
- fusão RRF sem IDs duplicados;
- combinação de candidatos Dense e BM25;
- respeito ao limite `top_k`;
- filtragem das evidências pela natureza selecionada.

---

## 10. Geração de respostas

O pipeline recebe a pergunta, recupera evidências e gera uma resposta com as fontes utilizadas.

### Exemplo validado

```text
Pergunta:
Quais contratações envolvem serviços de tecnologia?

Rota:
estruturada

Evidências:
3

Métodos:
Dense + BM25 + RRF
```

A resposta apresentou contratações relacionadas a:

- gestão e governança de tecnologia da informação;
- inteligência artificial e chatbots;
- plataforma de comunicação integrada ao WhatsApp;
- hospedagem e suporte técnico;
- operação de infraestrutura e atendimento a usuários de TIC.

As fontes foram apresentadas por meio dos respectivos `chunk_id`.

---

## 11. Interface Gradio

A interface permite:

- inserir uma pergunta;
- escolher a quantidade de evidências;
- executar a consulta;
- visualizar a resposta;
- visualizar as bases selecionadas;
- visualizar os filtros;
- visualizar as evidências;
- consultar o status da execução.

Também apresenta:

- confiança;
- latência;
- tokens;
- `query_id`;
- `run_id`;
- fontes utilizadas;
- mensagem amigável quando os índices não estão disponíveis.

---

## 12. Segurança e guardrails

Foi validada a pergunta:

```text
Esse contrato foi uma fraude?
```

O sistema:

- marcou a consulta para recusa;
- não retornou evidências;
- não realizou acusação;
- explicou a limitação;
- registrou a decisão nos logs;
- não continuou normalmente pela recuperação.

O projeto permite responder sobre:

- valores de contratos;
- nomes de empresas;
- CNPJ de pessoa jurídica;
- objetos contratados;
- informações públicas do PNCP.

O sistema deve mascarar ou bloquear:

- CPF;
- telefone pessoal;
- e-mail pessoal;
- dados bancários;
- credenciais;
- acusações automáticas de fraude ou ilegalidade.

---

## 13. Observabilidade

Os eventos são registrados em:

```text
logs/pipeline-AAAA-MM-DD.jsonl
```

Cada registro contém:

- timestamp;
- `run_id`;
- `query_id`;
- estágio;
- status;
- latência;
- entrada;
- saída;
- tokens;
- modelo;
- informações adicionais.

### Etapas instrumentadas

```text
query_analysis
roteamento
retrieval_denso
retrieval_bm25
fusao_rrf
geracao
validacao
```

Em uma consulta de recusa, foram confirmadas as etapas:

```text
query_analysis
roteamento
fusao_rrf
geracao
validacao
```

Todas utilizaram o mesmo `run_id`.

---

## 14. Testes realizados

### Suíte offline

```text
109 passed
```

### Testes de integração

```text
7 passed in 360.83s
```

Os testes de integração cobrem:

- consultas das personas;
- recuperação normativa;
- correspondência entre fontes e evidências;
- limite `top_k`;
- proteção de dados pessoais;
- consulta sensível;
- recusa;
- funcionamento ponta a ponta.

---

## 15. Limitações identificadas

### 15.1 Recuperação conversacional

A pergunta:

```text
O que foi registrado nas atas sobre aquisições e fornecedores?
```

selecionou corretamente a rota `conversacional`, mas retornou zero evidências.

A análise indicou que o filtro `uf: RJ` foi aplicado mesmo sem a localização ter sido mencionada. Como alguns chunks conversacionais estão com UF vazia, eles foram eliminados.

### 15.2 Ano da base agregada

Algumas datas no formato `DD/MM/AAAA` geraram anos incorretos:

```text
01/01/2026 → 01/0
01/12/2026 → 01/1
09/07/2026 → 09/0
```

O resultado correto deve ser:

```text
2026
```

A correção deverá aceitar:

- `DD/MM/AAAA`;
- `AAAA-MM-DD`;
- ano fornecido diretamente.

Esses problemas foram identificados pelos testes adicionais e não anulam os resultados já aprovados nas outras rotas.

---

## 16. Correções imediatas

- corrigir a extração do ano agregado;
- impedir a criação de filtro de UF não mencionado;
- corrigir a recuperação conversacional;
- adicionar testes de regressão;
- concluir a auditoria do manifesto;
- regenerar os chunks;
- reconstruir os índices utilizando o cache;
- executar novamente os testes offline;
- executar novamente os testes de integração;
- validar as quatro bases na interface.

---

## 17. Próximas sprints

Após a estabilização atual, ainda serão desenvolvidos:

- rerank por cross-encoder;
- estágio `rerank` nos logs;
- ablação da recuperação;
- comparação entre BM25, Dense, RRF e RRF + rerank;
- feedback do usuário;
- histórico persistido;
- estágio `feedback` nos logs;
- avaliação das nove perguntas das personas;
- métricas de qualidade;
- teste de regressão entre versões do corpus;
- revisão final da documentação;
- preparação da apresentação final.

O rerank depende do endpoint que será disponibilizado no Sprint 2.

---

## 18. Como executar

### Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### Executar a ingestão

```bash
python -m src.ingest
```

### Construir os índices

```bash
python -m src.index
```

### Executar os testes offline

```bash
PYTHONPATH=. pytest -q --ignore=testes/teste_integracao.py
```

### Executar os testes de integração

```bash
PYTHONPATH=. pytest -q testes/teste_integracao.py
```

### Abrir a interface

```bash
python -m app.app
```

No Google Colab, os comandos de terminal devem utilizar `!`:

```python
!PYTHONPATH=. pytest -q --ignore=testes/teste_integracao.py
```

---

## 19. Roteiro para demonstração

### 1. Apresentar o objetivo

Explicar que o sistema permite consultar contratações públicas em linguagem natural e seleciona automaticamente as bases necessárias.

### 2. Mostrar o manifesto

Abrir:

```text
corpus_manifest.yaml
```

Explicar que o arquivo registra as quatro bases, origens, caminhos, hashes e critérios de seleção.

### 3. Mostrar os inventários

Abrir:

```text
CORPUS_INVENTORY.md
data/inventory/v3.json
data/inventory/DIFF_v2_v3.md
```

Explicar o versionamento e a preservação dos snapshots.

### 4. Mostrar os módulos

Abrir:

```text
src/fetch_corpus.py
src/ingest.py
src/index.py
src/router.py
src/retrieve.py
src/generate.py
src/obs.py
```

Explicar resumidamente a responsabilidade de cada módulo.

### 5. Mostrar os testes

Abrir:

```text
testes/
```

Informar:

```text
109 testes offline aprovados
7 testes de integração aprovados
```

### 6. Mostrar a interface

Executar:

```bash
python -m app.app
```

Demonstrar uma pergunta normal e uma pergunta de recusa.

### 7. Mostrar as limitações

Explicar que a equipe identificou:

- recuperação conversacional vazia;
- erro na extração do ano agregado.

Apresentar esses pontos como resultados da validação, com correções planejadas.

---

## 20. Resumo do estado atual

Atualmente, o projeto possui:

- quatro bases de naturezas diferentes;
- coleta automatizada e versionada;
- 1.358 registros estruturados;
- 2.125 chunks;
- cache de embeddings;
- índice FAISS;
- índice BM25;
- roteamento adaptativo;
- recuperação híbrida;
- fusão RRF;
- geração de respostas com fontes;
- guardrails;
- interface Gradio;
- logs estruturados;
- schemas;
- testes offline;
- testes de integração.

As próximas ações imediatas são corrigir a recuperação conversacional e a extração do ano agregado. Depois dessas correções, os chunks e índices serão regenerados e o pipeline será validado novamente.
