# Adaptive RAG para Contratações Públicas do Estado do Rio de Janeiro

> Estado avaliado em 19/10/2026: pacote de 2.172 chunks. Reprodução final e congelamento ainda pendentes. [Guia atual](docs/GUIA_RESTAURACAO_2172.md).


Projeto desenvolvido no **Grande Desafio de IA Generativa e RAG**, da Residência TIC em Trilhas — PUC-Rio e Instituto ECOA.

O sistema utiliza uma arquitetura de **Adaptive RAG** para responder perguntas sobre contratações públicas do Estado do Rio de Janeiro. Antes de recuperar documentos, o sistema analisa a consulta e decide quais tipos de evidência são necessários.

---

## 1. Cenário escolhido

**Cenário 1 — Contratações Públicas do Estado do Rio de Janeiro**

O cenário foi escolhido por utilizar dados públicos provenientes de fontes oficiais e permitir a integração de bases com naturezas diferentes. As consultas podem exigir busca semântica, correspondência lexical, filtros estruturados, análise normativa e informações agregadas.

---

## 2. Bases de conhecimento

O pacote atual contém oito arquivos brutos e quatro naturezas:

| Natureza | Conteúdo disponível |
|---|---|
| Normativa | Snapshot HTML da Lei nº 14.133/2021 |
| Estruturada | 1.358 registros PNCP da coleta RJ, pregão eletrônico, março/2026 |
| Conversacional | Três atas oficiais e uma comunicação sintética identificada |
| Agregada | CSV completo do PCA disponibilizado e itens do PE 038/26/2026 |

Origem, hashes e limitações constam no inventário e no guia do pacote.

## 3. Funcionamento do sistema

O planejamento distingue consultas estruturadas, agregadas, documentais
e combinadas. Contagens, listagens e resumos suportados são calculados
nos arquivos completos. Pedidos documentais usam recuperação híbrida,
seleção de evidências e validação de citações.

A combinação exige pedido documental explícito. Recusas e esclarecimentos
podem encerrar a consulta antes de acessar as bases.

A recuperação documental utiliza busca vetorial, recuperação lexical e RRF.
O rerank local é opcional. Mecanismos de cobertura procuram preservar os
campos solicitados antes da apresentação dos trechos.

## 4. Implementação e validação

Estão implementados: planejamento de consultas, operações estruturadas
e agregadas suportadas, recuperação híbrida, seleção documental, citações,
guardrails, logs, interface, histórico persistente e feedback.

A documentação registra separadamente:

- 21 casos de personas avaliados no commit 5499caf;
- oito suplementares, incluindo revalidação de S05 e S06 após correções;
- cálculos, paginação, feedback e histórico na aplicação fef6d7a;
- comparação de seis rankings com rerank local.

Esses registros pertencem às versões e condições descritas em cada relatório.
Não constituem uma rodada única de toda a entrega final.

Permanecem pendentes: avaliação de respostas com rerank, reprodução final,
consolidação das verificações na versão congelada e preparação da entrega.

## 5. Estrutura do repositório
```text
├── testes/                  # Testes e fixtures
├── acompanhamento/          # Relatos individuais dos integrantes
├── app/                     # Interface e adaptador do pipeline
├── data/
│   ├── inventory/           # Inventários versionados
│   ├── processed/           # Chunks processados, ignorados pelo Git
│   └── indices/             # Índices persistidos, ignorados pelo Git
├── docs/                    # Guias complementares
├── eval/                    # Resultados de avaliação
├── logs/                    # Logs locais, ignorados pelo Git
├── src/                     # Módulos do pipeline
├── ARQUITETURA.md
├── CORPUS_INVENTORY.md
├── PERSONAS.md
├── corpus_manifest.yaml
├── requirements.txt
└── README.md
```

---

## 6. Módulos principais

| Módulo | Responsabilidade |
|---|---|
| `src/fetch_corpus.py` | Coleta, atualização, versionamento e inventário |
| `src/ingest.py` | Extração, chunking e metadados |
| `src/index.py` | Embeddings, FAISS, BM25 e persistência |
| `src/router.py` | Análise da consulta, filtros e roteamento |
| `src/retrieve.py` | Recuperação híbrida, filtros e fusão RRF |
| `src/generate.py` | Geração das respostas e guardrails |
| `src/schema.py` | Modelos e contratos compartilhados |
| `src/obs.py` | Logging estruturado e tokens |
| `app/pipeline_adapter.py` | Integração da interface com o pipeline |
| `app/app.py` | Interface Gradio |

Alguns módulos podem ainda estar em desenvolvimento.

---

## 7. Pré-requisitos

É necessário Git, Python, dependências instaladas e acesso autorizado ao
pacote de artefatos. As consultas reais dependem do serviço de modelos
disponibilizado à equipe.

O ambiente observado nas validações usa Python 3.13.16 e Gradio 6.29.0.
requirements.txt define versões mínimas; não é um lockfile nem comprova
compatibilidade de todas as combinações permitidas.

## 8. Instalação

Clone o repositório:

```bash
git clone https://github.com/rag-grande-desafio-grupo1-cenario-1/repositorio1.git
cd repositorio1
```

Crie um ambiente virtual.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Copie o arquivo de exemplo das variáveis de ambiente:

### Windows

```bash
copy .env.example .env
```

### Linux ou macOS

```bash
cp .env.example .env
```

Preencha somente as configurações necessárias. Não envie o arquivo `.env` ao GitHub.

---

## 9. Coleta do corpus — reconstrução opcional

A coleta é controlada pelo arquivo `corpus_manifest.yaml`.

Coleta inicial:

```bash
python -m src.fetch_corpus fetch --manifest corpus_manifest.yaml
```


Criação de uma nova versão:

```bash
python -m src.fetch_corpus update --manifest corpus_manifest.yaml --sources /caminho/para/fontes_locais
```


Geração ou atualização do inventário:

```bash
python -m src.fetch_corpus inventory --version v3
```

A pasta `data/raw/` não é versionada no Git.

---

## 10. Restaurar os artefatos atuais

Para executar a aplicação avaliada, restaure o pacote completo de
**2.172 chunks**, com seus índices correspondentes.

Siga o [guia de restauração](docs/GUIA_RESTAURACAO_2172.md).
Não é necessário gerar embeddings novamente.

Ingestão e indexação são procedimentos de reconstrução. Uma nova coleta ou
reconstrução deve gerar outra versão identificada. Os artefatos de 2.125
chunks e os relatórios anteriores permanecem históricos.

## 11. Executar a interface

Restaure e confira os artefatos antes de iniciar a aplicação.
Em ambiente local, execute da raiz: `python -m app.app`.

No Colab, configure explicitamente logs, histórico e feedback antes de
importar a aplicação. Use `criar_interface()` e inicie a fila da interface
com compartilhamento quando necessário.

Consulte o [guia](docs/GUIA_RESTAURACAO_2172.md) para configuração e ocorrências
do frontend. O link público da Gradio é temporário e depende do processo ativo.
O histórico é compartilhado entre quem acessa a instância.

## 12. Consultas avaliadas e limites

| Pergunta ou recorte | Comportamento esperado |
|---|---|
| Pregões eletrônicos publicados no RJ em março/2026 | Listagem de 1.358 registros, paginada |
| Resumo completo do PE 038/26/2026 | 19 itens; 8 homologados, 9 fracassados, 2 desertos; R$ 141.002,08 |
| Regras sobre pregão na Lei nº 14.133/2021 | Evidências normativas citadas |
| Contagem por ano da compra 2026 e explicação normativa | 1.234 registros no recorte e parte documental separada |
| Prazo no processo fictício SIM-RJ-001 | 10/15 dias após emissão do pedido; simulação identificada |
| Exposição de CPF e telefone pessoal | Recusa |

Médias monetárias, preço por quilo e filtros de assinatura não estão
implementados. Pedidos ambíguos ou intervalos de publicação não suportados
exigem esclarecimento.

As perguntas exatas, fontes, resultados e versões constam nas matrizes
de avaliação em docs. Consultas livres podem exigir esclarecimento.

## 13. Limitação temporária das evidências

A ausência de evidências não significa necessariamente erro da interface.

Isso pode ocorrer quando:

- a base correspondente ainda não foi coletada;
- a base ainda não passou pela ingestão;
- a base ainda não foi indexada;
- a fixture disponível contém somente dados de outra natureza;
- os filtros eliminam os resultados existentes.

Por exemplo, uma pergunta normativa pode ser roteada corretamente e ainda retornar zero evidências se os documentos normativos não estiverem indexados.

---

## 14. Testes e evidências

O pytest.ini exclui testes llm por padrão. Execute separadamente os testes
sem LLM, a compatibilidade dos artefatos e a integração real:

```bash
python -m pytest -q -m "not llm" --ignore=testes/test_compatibilidade_artefatos.py
python -m pytest -q -m "not llm" testes/test_compatibilidade_artefatos.py
python -m pytest -v -m llm testes/teste_integracao.py
```

A compatibilidade exige o pacote restaurado. A integração exige o serviço
de modelos. Registre commit, pacote, comando, resultados e logs.

A bateria anterior registrou 587 aprovações com 7 testes llm desmarcados,
com artefatos disponíveis. Isso não equivale a 587 testes unitários isolados.
Os resultados da versão final devem ser registrados na reprodução.

## 15. Política de sensibilidade

A classificação de sensibilidade deve ocorrer durante a ingestão.

### Informações permitidas

O sistema pode responder com:

- valores de contratos;
- objetos contratados;
- nomes de empresas fornecedoras;
- CNPJ de pessoas jurídicas;
- modalidades e órgãos públicos.

### Informações que devem ser mascaradas

O sistema deve mascarar:

- CPF de pessoa física;
- telefone pessoal;
- e-mail pessoal;
- outros dados pessoais encontrados em atas ou comunicações.

### Solicitações que devem ser recusadas

O sistema deve recusar:

- dados bancários;
- credenciais;
- informações restritas;
- acusações de fraude;
- julgamentos sobre a legalidade de contratos específicos.

O sistema apresenta evidências públicas, mas não substitui investigação ou análise jurídica.

---

## 16. Observabilidade

O pipeline utiliza logs estruturados no formato JSONL:

```text
logs/pipeline-AAAA-MM-DD.jsonl
```

Os eventos podem registrar:

- `ts`;
- `run_id`;
- `query_id`;
- `stage`;
- `status`;
- `latencia_ms`;
- `input`;
- `output`;
- `tokens`;
- `modelo`;
- `extra`.

Estágios padronizados:

- `query_analysis`;
- `roteamento`;
- `retrieval_denso`;
- `retrieval_bm25`;
- `fusao_rrf`;
- `rerank`;
- `geracao`;
- `validacao`;
- `feedback`.

---

## 17. Responsabilidades

| Área | Responsável |
|---|---|
| Coordenação | Maria Eduarda |
| Coleta e versionamento | Janice |
| Ingestão e indexação | Eridalgo |
| Roteamento e recuperação | Luiz Carlos |
| Geração, schemas, guardrails e testes | Felipe e Calvin |
| Observabilidade, interface e integração | Maria Eduarda |
| Documentação | Maria Eduarda, com contribuição da equipe |

A responsabilidade principal por um módulo não impede a colaboração dos demais integrantes.

---

## 18. Documentação complementar

- [`ARQUITETURA.md`](ARQUITETURA.md): arquitetura e divisão de responsabilidades;
- [`PERSONAS.md`](PERSONAS.md): personas e perguntas de referência;
- [`CORPUS_INVENTORY.md`](CORPUS_INVENTORY.md): inventário do corpus;
- [`corpus_manifest.yaml`](corpus_manifest.yaml): definição declarativa das bases;
- [`docs/GUIA_DO_PIPELINE.md`](docs/GUIA_DO_PIPELINE.md): explicação do fluxo e dos testes.

---

## 19. Equipe

Projeto desenvolvido pelo Grupo 1 no cenário de Contratações Públicas do Estado do Rio de Janeiro.

## Status do desenvolvimento

Consulte o [Status atual do projeto](docs/STATUS_DO_PROJETO.md) para visualizar a arquitetura, os módulos implementados, os dados processados, os testes realizados, as limitações conhecidas e as próximas atividades.
