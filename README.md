# Adaptive RAG para Contratações Públicas do Estado do Rio de Janeiro

Projeto desenvolvido no **Grande Desafio de IA Generativa e RAG**, da Residência TIC em Trilhas — PUC-Rio e Instituto ECOA.

O sistema utiliza uma arquitetura de **Adaptive RAG** para responder perguntas sobre contratações públicas do Estado do Rio de Janeiro. Antes de recuperar documentos, o sistema analisa a consulta e decide quais tipos de evidência são necessários.

---

## 1. Cenário escolhido

**Cenário 1 — Contratações Públicas do Estado do Rio de Janeiro**

O cenário foi escolhido por utilizar dados públicos provenientes de fontes oficiais e permitir a integração de bases com naturezas diferentes. As consultas podem exigir busca semântica, correspondência lexical, filtros estruturados, análise normativa e informações agregadas.

---

## 2. Bases de conhecimento

O sistema trabalha com quatro tipos de base:

| Natureza | Conteúdo |
|---|---|
| Normativa | Lei nº 14.133/2021, decretos e editais |
| Estruturada | Contratos e contratações públicas |
| Conversacional | Atas e comunicações relacionadas às compras |
| Agregada | Indicadores, totais e valores agrupados |

Uma consulta pode utilizar somente uma base ou combinar múltiplas bases.

---

## 3. Funcionamento do sistema

Fluxo resumido:

```text
Pergunta do usuário
        |
        v
Análise da consulta
        |
        v
Roteamento
        |
        v
Recuperação densa + BM25
        |
        v
Fusão RRF
        |
        v
Geração e guardrails
        |
        v
Validação
        |
        v
Resposta e evidências
```

Principais etapas:

1. análise da pergunta;
2. seleção de uma ou mais bases;
3. extração de filtros;
4. recuperação densa e lexical;
5. fusão dos resultados com RRF;
6. geração da resposta;
7. aplicação de guardrails;
8. exibição da resposta e das evidências;
9. registro das etapas em logs estruturados.

Para uma descrição mais detalhada, consulte:

- [`ARQUITETURA.md`](ARQUITETURA.md);
- [`PERSONAS.md`](PERSONAS.md);
- [`docs/GUIA_DO_PIPELINE.md`](docs/GUIA_DO_PIPELINE.md).

---

## 4. Atualmente, o repositório possui implementações para:
- coleta e versionamento do corpus;
- corpus v3 com inventário e hashes SHA-256;
- ingestão e preparação de documentos;
- geração de embeddings;
- índice vetorial FAISS;
- índice lexical BM25;
- persistência dos índices;
- roteamento adaptativo;
- extração de filtros;
- regras de recusa;
- recuperação híbrida;
- fusão RRF;
- geração de respostas e guardrails;
- schemas compartilhados;
- logging estruturado e observabilidade;
- interface desenvolvida com Gradio;
- testes unitários, de contrato e de integração;
- documentação da arquitetura e do pipeline.

Ainda estão em consolidação e validação:

- reranqueamento por cross-encoder;
- integração ponta a ponta das quatro naturezas de evidência;
- execução da suíte completa de testes no ambiente com todas as dependências e artefatos;
- avaliação sistemática do pipeline e ablações;
- validação final da geração, guardrails e comportamento cross-source.

A existência de um módulo no repositório não significa, isoladamente, que sua integração ponta a ponta já tenha sido validada. O projeto diferencia implementação, integração e validação experimental.


---

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

Recomenda-se utilizar:

- Python 3.10 ou superior;
- Git;
- ambiente virtual Python;
- acesso ao endpoint de modelos disponibilizado pela residência.

---

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

## 9. Coleta do corpus

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

## 10. Ingestão e indexação

Execute a ingestão a partir da raiz do repositório:

```bash
python -m src.ingest
```

Depois, gere os índices:

```bash
python -m src.index
```

A indexação pode gerar:

```text
data/processed/chunks_teste.json
data/indices/faiss_index.bin
data/indices/bm25_index.pkl
data/indices/chunk_ids.json
```

Os nomes poderão ser ajustados conforme a integração das bases reais.

Como o endpoint de embeddings é compartilhado, os índices devem ser persistidos e reutilizados. A indexação não deve ser executada novamente sem necessidade.

---

## 11. Executar a interface

Antes de iniciar a interface, confirme que as dependências foram instaladas e que os chunks e índices necessários existem.

### Google Colab

Entre na pasta do repositório:

```python
%cd /content/repositorio1
```

Instale as dependências:

```python
!pip install -q -r requirements.txt
```

Inicie a interface:

```python
from app.app import criar_interface

demo = criar_interface()
demo.launch(share=True, debug=True)
```

O Gradio fornecerá um endereço público temporário.

### VS Code

No terminal aberto na raiz do repositório, execute:

```bash
python -m app.app
```

Abra o endereço mostrado no terminal, normalmente:

```text
http://127.0.0.1:7860
```

---

## 12. Perguntas para testar a interface

### Consulta estruturada

```text
Quais contratações de serviços de tecnologia foram encontradas?
```

Rota esperada:

```python
["estruturada"]
```

### Consulta normativa

```text
O que a Lei nº 14.133/2021 estabelece sobre o pregão eletrônico?
```

Rota esperada:

```python
["normativa"]
```

### Consulta agregada e estruturada

```text
Quantos contratos foram assinados por modalidade em 2025?
```

Rotas esperadas:

```python
["agregada", "estruturada"]
```

### Consulta conversacional

```text
O que foi discutido nas atas sobre a compra de equipamentos?
```

Rota esperada:

```python
["conversacional"]
```

### Consulta cross-source

```text
Sou MEI, posso participar de pregão eletrônico e existe algum aberto para material de escritório?
```

Rotas esperadas:

```python
["estruturada", "normativa"]
```

### Consulta que deve ser recusada

```text
Esse contrato foi uma fraude?
```

Resultado esperado:

- nenhuma rota selecionada;
- nenhuma evidência utilizada;
- indicação de recusa;
- apresentação do motivo.

---

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

## 14. Testes

Os testes são organizados em três camadas:

| Camada | Objetivo | Utiliza LLM |
|---|---|---|
| Unitária | Funções determinísticas e isoladas | Não |
| Contrato | Formatos, schemas e regras obrigatórias | Não |
| Integração | Pipeline completo com perguntas conhecidas | Sim |

Executar os testes offline:

```bash
pytest -m "not llm" -v
```

## Execução dos testes

Os comandos devem ser executados na raiz do repositório.

### Testes offline

Os testes offline validam os módulos sem exigir a execução completa do
pipeline, o acesso ao modelo ou os artefatos de indexação.

```bash
export PYTHONPATH=.
python -m pytest -q --ignore=testes/teste_integracao.py
```

### Testes de integração

```bash
export PYTHONPATH=.
python -m pytest -q testes/teste_integracao.py
```

A execução completa pode depender destes artefatos:

- `data/processed/chunks_teste.json`;
- `data/indices/faiss_index.bin`;
- `data/indices/bm25_index.pkl`;
- `data/indices/chunk_ids.json`;
- acesso ao endpoint dos modelos.

Se esses recursos não estiverem disponíveis, os testes offline podem ser
executados separadamente.


Executar testes que utilizam o endpoint do LLM:

```bash
pytest -m llm -v
```

Executar todos os testes:

```bash
pytest -v
```

Os testes de integração devem ser marcados com `@pytest.mark.llm`.

---

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
