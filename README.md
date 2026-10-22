# Adaptive RAG — Contratações Públicas do Rio de Janeiro

Projeto do **Grande Desafio de IA Generativa e RAG**, da Residência TIC em Trilhas — PUC-Rio e Instituto ECOA.

O sistema identifica o tipo de evidência necessário para responder à pergunta e seleciona consultas estruturadas, cálculos sobre arquivos completos, recuperação documental ou uma combinação dessas estratégias.

> **Revisão funcional de 21/10/2026:** respostas explicativas com citações,
> planejamento analítico, cálculos sobre CSVs completos e consultas combinadas.
> As correções estão em preparação na branch
> `fix/respostas-explicativas-20261021T192459760154Z`.
> A publicação e a integração remotas ainda não foram confirmadas.
>
> **Versão anterior preservada:** [`entrega-2026-10-19`](https://github.com/rag-grande-desafio-grupo1-cenario-1/repositorio1/tree/entrega-2026-10-19),
> commit `f1efc55c81f5ee5ffa54d3d87a584e22e12484bb`.
> Essa tag não inclui as correções de 21/10.
>
> Consulte o [relatório das correções](docs/CORRECOES_RESPOSTAS_2026-10-21.md)
> para distinguir resultados atuais, avaliações históricas e pendências.

## 1. Cenário e objetivo

**Cenário 1 — Contratações Públicas do Estado do Rio de Janeiro.**

A solução permite consultar o corpus fornecido sem exigir que o usuário programe ou manipule diretamente arquivos e APIs. As respostas apresentam os filtros, fontes, recortes e evidências correspondentes à estratégia executada.

O sistema não representa uma consulta em tempo real a todas as contratações do PNCP. Seu escopo é o conjunto de arquivos identificado no manifesto e no inventário.

## 2. Corpus da entrega

O pacote preservado contém **oito arquivos brutos e 2.172 chunks**, distribuídos em quatro naturezas.

| Natureza | Conteúdo | Chunks |
|---|---|---:|
| Estruturada | 1.358 registros PNCP do recorte RJ, pregão eletrônico, março de 2026 | 1.358 |
| Normativa | Snapshot HTML da Lei nº 14.133/2021 | 217 |
| Conversacional | Três atas oficiais e uma comunicação sintética identificada | 78 |
| Agregada | PCA disponibilizado e resultados dos itens do PE 038/26/2026 | 519 |
| **Total** | | **2.172** |

A quantidade de chunks agregados indexados não corresponde à quantidade total de linhas dos arquivos. Os cálculos suportados consultam os CSVs completos.

**Pacote compartilhado:**

```text
ENTREGA_EQUIPE_2026-10-16/pacote_v3_2172
```

**SHA-256 de `data/processed/chunks_teste.json`:**

```text
dcdcc7a0f8e34da1d0824b5322b6e37306c34e2d53d107c1ca067bc2771c8404
```

Consulte:

- [Manifesto do corpus](corpus_manifest.yaml).
- [Inventário](CORPUS_INVENTORY.md).
- [Guia de restauração e integridade](docs/GUIA_RESTAURACAO_2172.md).

Não misture esse pacote com artefatos históricos de 2.125 chunks.

## 3. Funcionamento

| Estratégia | Execução |
|---|---|
| Consulta estruturada | Filtros, contagem e listagem sobre a base normalizada, com paginação |
| Consulta agregada | Resumos suportados sobre os arquivos completos |
| Consulta analítica | Plano validado, contagens, medidas, agrupamentos, listagens e comparações nos CSVs PE/PCA |
| Recuperação documental | Busca vetorial e BM25, fusão RRF, preparação do contexto e síntese explicativa com citações |
| Consulta combinada | Resultado estruturado ou analítico e explicação documental apresentados separadamente, com suas fontes |
| Esclarecimento | Interrompe pedidos ambíguos ou operações ainda não suportadas |
| Recusa | Interrompe solicitações protegidas ou fora do escopo definido |

Cada caminho valida seu plano antes de executar as operações correspondentes.
O caminho analítico exige `RAG_ANALYTICAL_ENABLED=true` e utiliza somente
fontes, campos e operações autorizados. O executor realiza os cálculos;
o modelo interpreta a pergunta e pode redigir a resposta a partir dos
resultados calculados.

Pedidos documentais adicionais reconhecidos são separados do pedido
numérico. Um resultado calculado não serve como evidência sobre a lei.
Essa separação é conservadora e não garante a interpretação correta
de toda reformulação.

A síntese explicativa é o padrão do gerador. O modo extrativo permanece
disponível quando solicitado explicitamente. Referências reconhecidas
pelo validador não comprovam, por si só, suporte semântico.

Nas consultas documentais, o `top_k` controla a quantidade de evidências apresentadas ao gerador. Ele não limita a quantidade de registros usados nas contagens e somas determinísticas.

O rerank local por cross-encoder está disponível como opção e permanece **desativado por padrão**, conforme a avaliação registrada.

## 4. Instalação

O repositório é privado e exige acesso autorizado. Não coloque tokens na URL do clone nem versione credenciais.

```bash
git clone https://github.com/rag-grande-desafio-grupo1-cenario-1/repositorio1.git
cd repositorio1
```

O clone utiliza a branch padrão do remoto. Confira o commit: enquanto as correções de 21/10 não forem integradas, o remoto pode conter a versão anterior. Para reproduzir a entrega antiga, use `git checkout entrega-2026-10-19`.

Crie e ative um ambiente virtual.

**Linux ou macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows — Prompt de Comando:**

```bat
python -m venv .venv
.venv\Scripts\activate
```

Instale as versões diretas utilizadas na validação:

```bash
python -m pip install -r docs/ambiente_validacao_2026-10-19/requirements-base.txt
python -m pip check
```

O ambiente observado utilizou Python 3.13.16 e Gradio 6.29.0.

O arquivo de versões diretas não é um lockfile completo. As dependências efetivamente instaladas na reprodução estão em [requirements-ambiente-reproduzido.txt](docs/reproducao_d31d05a_2026-10-19/requirements-ambiente-reproduzido.txt).

O `requirements.txt` da raiz mantém versões mínimas; isso não garante compatibilidade de todas as combinações permitidas.

### Configuração do serviço

As execuções registradas utilizaram:

- Geração: `qcwind/qwen3-8b-instruct-Q4-K-M`.
- Embeddings: `xagi/qwen3-embedding:0.6b-q4_k_m`.
- Endpoint compatível com OpenAI disponibilizado pela residência.

A versão auditada ainda contém endpoint e modelos definidos diretamente nos módulos. A centralização em `config.py` e a leitura consistente das opções do `.env.example` são pendências técnicas.

Não envie `.env`, tokens ou credenciais ao GitHub.

## 5. Restaurar dados e índices

Siga o [guia de restauração](docs/GUIA_RESTAURACAO_2172.md), utilizando o pacote completo e conferindo os hashes do manifesto.

A restauração deve recuperar os arquivos brutos, os dados processados e os índices correspondentes.

**Não é necessário gerar embeddings novamente para executar a versão validada.**

Ingestão e indexação são procedimentos de reconstrução. Não os execute apenas para iniciar a interface. Caso uma reconstrução seja necessária, identifique a nova versão e preserve os artefatos anteriores.

## 6. Executar a interface

Execute da raiz do repositório, após restaurar e conferir o pacote:

```bash
python scripts/iniciar_interface_colab.py
```

Antes da execução, configure conforme o guia:

- `PIPELINE_LOG_DIR`: pasta dos logs.
- `HISTORY_PATH`: arquivo do histórico SQLite.
- `FEEDBACK_PATH`: arquivo de feedback JSONL.
- `GRADIO_SERVER_PORT`: porta da interface.
- `RAG_ANALYTICAL_ENABLED=true`: habilita o caminho analítico; desativado por padrão.
- `RAG_DEMO_OFFLINE=false`: utiliza o fluxo conectado ao serviço.
- `RERANK_ENABLED=false`: configuração das validações atuais.
- `NORMATIVE_CONTEXT_MAX_CHARS=2500`: orçamento de contexto normativo.
- `DOCUMENT_CONTEXT_MAX_CHARS=2500`: orçamento de contexto de PDFs conversacionais.

Os orçamentos são medidos em caracteres, não em tokens. A preparação
não altera índices ou arquivos originais, mas pode excluir evidências
necessárias à resposta.

No Colab, use caminhos de persistência no Drive montado. Arquivos apenas em `/content` podem desaparecer quando o ambiente é encerrado.

O inicializador configura a pasta de logs antes da importação da aplicação e seleciona o frontend local. Consulte o guia para os controles de raciocínio, limite de tokens do roteador e configuração opcional de rerank.

O link público do Gradio é temporário e depende do Colab e do processo ativos. A referência permanente da entrega é a versão do código acompanhada do pacote e das evidências.

O histórico é compartilhado entre quem acessa a mesma instância. Abrir uma consulta salva reapresenta o resultado original; não representa uma nova chamada ao modelo.

## 7. Consultas avaliadas

| Consulta | Resultado observado |
|---|---|
| Pregões eletrônicos publicados no RJ em março de 2026 | 1.358 registros, com paginação |
| PE 038/26/2026 | 19 itens: 8 homologados, 9 fracassados e 2 desertos; soma homologada de R$ 141.002,08 |
| Ata nº 191/2026 da EBSERH | Objeto: peças mamógrafas (chassis); PNCP 15126437000305-1-000676/2026 |
| Pregão na Lei nº 14.133/2021 | Definição, aplicação e exceções em evidências normativas citadas |
| Processo fictício SIM-RJ-001 | Papel A4 em 10 dias e canetas em 15 dias após a emissão do pedido; simulação identificada |
| PCA RJ 2026 disponibilizado | 36.994 linhas; soma estimada de R$ 55.968.524.178,3319 no arquivo integral |
| Ata nº 137/2026 do INCA | Rodízios para camas elétricas; contratada AGIMED COMERCIO DE EQUIPAMENTOS LTDA |
| Contagem por ano da compra 2026 e explicação normativa | 1.234 registros no recorte, com parte documental separada |
| Resumo do PE com verificação de vínculos | Cálculo sobre o CSV e verificação por identificadores no corpus carregado |

As perguntas, fontes, identificadores de execução e versões estão nos relatórios. Consultas livres podem exigir esclarecimento.

### Consultas analíticas verificadas em 21/10

| Pedido | Resultado observado |
|---|---|
| Quantos itens foram homologados? Resposta em uma frase | 8 itens |
| Comparar homologados e fracassados | 8 e 9; diferença = -1 |
| Tabela de quantidade por situação | 8 homologados, 9 fracassados e 2 desertos |
| Três itens homologados de maior valor total | Itens 1, 3 e 4; valores 44.500,00, 20.646,00 e 17.120,00 |
| Valor total estimado médio por registro do PCA | Aproximadamente R$ 1.512.908,15; 36.994 valores presentes |
| Contagem ou tabela do PE e explicação normativa | Cálculo e explicação documental separados |
| Homologações anteriores à assinatura do contrato | Esclarecimento: assinatura ausente no arquivo de itens |

Consulte os identificadores e condições no
[relatório das correções](docs/CORRECOES_RESPOSTAS_2026-10-21.md).
Os casos não constituem uma taxa geral de acerto.

### Limites das operações

- O caminho analítico novo utiliza os CSVs autorizados do PE e do PCA.
  A base estruturada do PNCP mantém seu executor próprio.
- Médias simples estão disponíveis; preço por quilo, média ponderada,
  previsões e cruzamentos arbitrários não foram demonstrados.
- A proteção para condições conhecidas ausentes impede responder sobre
  assinatura, pagamento ou entrega usando somente o arquivo de itens.
  Ela não cobre automaticamente todo critério possível.
- Um plano estruturalmente válido pode interpretar incorretamente a pergunta.
  Cálculos e referências válidos não substituem a conferência da resposta.
- Homologação e registro de preços não comprovam pagamento ou entrega.

## 8. Validações registradas

**Revisão de 21/10:** a última suíte local completa informada teve
**754 testes aprovados e 7 testes de integração real desmarcados**.
Após conectar a atualização automática do histórico, os
**18 testes relacionados** passaram. Essa rodada parcial não equivale
a uma nova execução da suíte completa.

Casos reais de cálculo, esclarecimento, síntese documental e consulta
combinada estão no [relatório atual](docs/CORRECOES_RESPOSTAS_2026-10-21.md).

**As avaliações abaixo são históricas** e pertencem às versões e
condições identificadas nos respectivos relatórios.


| Avaliação | Evidência |
|---|---|
| Reprodução em clone local independente e venv isolado, no mesmo Colab | [Relatório de reprodução](docs/reproducao_d31d05a_2026-10-19/RELATORIO.md) |
| 585 testes locais, 2 de compatibilidade e 7 de integração real aprovados em execuções separadas | [Evidências da reprodução](docs/reproducao_d31d05a_2026-10-19/evidencias.json) |
| 21 casos de personas no commit `5499caf` | [Matriz das personas](docs/avaliacao_personas_5499caf_2026-10-19/RELATORIO.md) |
| Oito casos suplementares, com correções e revalidações identificadas | [Avaliação suplementar](docs/validacao_suplementares_2026-10-19/RELATORIO.md) |
| Cálculos, paginação, histórico e feedback na aplicação `fef6d7a` | [Validação da interface](docs/validacao_interface_fef6d7a_2026-10-19/RELATORIO.md) |
| Comparação de quatro métodos, em seis perguntas | [Comparação dos rankings](docs/comparacao_recuperacao_2026-10-19/RELATORIO.md) |
| 24 respostas extrativas, seis perguntas e quatro métodos, top-3 | [Avaliação das respostas](docs/avaliacao_respostas_recuperacao_2026-10-19/RELATORIO.md) |

Esses resultados pertencem aos commits e às condições descritos em cada relatório. Não constituem uma única rodada integral no commit documental da entrega.

A reprodução foi executada no commit `d31d05a`. O código da tag de entrega foi comparado ao código validado, sem diferenças nos caminhos de código, testes, inicializador e dependências conferidos.

O benchmark recebido da Janice está [preservado como avaliação complementar](docs/avaliacao_complementar_janice_2026-10-19/README.md). A identificação do commit e dos hashes utilizados nessa execução permanece pendente.

### Decisão sobre rerank

O rerank local foi avaliado e permanece desativado por padrão.
No recorte de seis perguntas com três evidências por resposta, houve ganhos
e perdas, sem melhoria consistente em relação ao RRF.

Esse experimento reutilizou rankings preservados, sem a seleção de cobertura
anterior à geração aplicada pela interface. Seus resultados não representam
a taxa de acerto do sistema completo.

A comparação dos rankings top-5 apresentou ganho de cobertura com rerank;
não foram geradas respostas top-5 nesta rodada.

Os resultados completos, critérios, falhas e limitações estão na
[avaliação das respostas](docs/avaliacao_respostas_recuperacao_2026-10-19/RELATORIO.md)
e na [comparação dos rankings](docs/comparacao_recuperacao_2026-10-19/RELATORIO.md).
A revisão das respostas foi assistida por IA, sem avaliação humana independente.

## 9. Testes

O `pytest.ini` exclui testes marcados `llm` por padrão.

```bash
python -m pytest -q -m "not llm" --ignore=testes/test_compatibilidade_artefatos.py
python -m pytest -q -m "not llm" testes/test_compatibilidade_artefatos.py
python -m pytest -v -m llm testes/teste_integracao.py
```

A compatibilidade exige o pacote restaurado. A integração real exige acesso ao serviço de modelos. Parte da suíte local também verifica arquivos do corpus disponíveis no ambiente.

Na reprodução, os sete testes de integração foram desmarcados na execução local e executados separadamente com o serviço real. Houve um aviso do pytest sobre importação prévia do `anyio` no harness, registrado no relatório.

As quantidades informadas são históricas, vinculadas à versão e aos comandos executados. Não são uma promessa do total de testes de qualquer revisão posterior.

**Ressalva da auditoria:** na tag `entrega-2026-10-19`, `testes/test_metadata.py` imprime falhas sem lançar uma asserção. Esse teste isolado não comprova o contrato de metadados. A correção e a ampliação das fixtures estavam em preparação e sua publicação posterior à tag ainda precisa ser confirmada.

## 10. Coleta e versionamento

O manifesto registra os arquivos, hashes e recortes do snapshot.

Na versão auditada, o `fetch` padrão coleta somente a base estruturada do PNCP:

```bash
python -m src.fetch_corpus fetch --manifest corpus_manifest.yaml
```

Há checkpoints e retomada explícita com `--retomar`. O destino final existente é protegido contra sobrescrita, mas não é tratado como coleta concluída com retorno de sucesso.

O fluxo de importação e atualização das demais fontes depende de arquivos locais previamente obtidos, com os caminhos e hashes esperados:

```bash
python -m src.fetch_corpus update --manifest corpus_manifest.yaml --sources /caminho/para/fontes_locais
python -m src.fetch_corpus inventory --manifest corpus_manifest.yaml --version v3
```

O fluxo local gera versões, inventário e diff. Isso não equivale à reconstrução automática das oito fontes a partir das URLs oficiais.

A coleta ainda precisa completar os contratos de limitação de taxa entre páginas bem-sucedidas e tratamento de falhas por fonte.

`data/raw/` é ignorado pelo Git. Manifesto, inventários e diffs são versionados. Para executar a aplicação validada, prefira a restauração do pacote.

## 11. Segurança e sensibilidade

**Informações permitidas:** valores, objetos, nomes de fornecedores e CNPJs de pessoas jurídicas.

**Informações a mascarar:** CPF de pessoa física, telefone pessoal, e-mail pessoal e outros dados pessoais presentes nas fontes.

**Solicitações a recusar:** dados bancários, credenciais e pedidos de acusação de fraude ou conclusão sobre a legalidade de uma contratação específica.

O sistema apresenta dados e evidências; não substitui investigação ou análise jurídica.

A sensibilidade é atribuída na ingestão. O alinhamento entre categorias do manifesto e valores efetivamente utilizados pelos módulos permanece entre as pendências da auditoria.

## 12. Observabilidade e persistência

O pipeline de consultas utiliza logs JSONL diários, com `run_id` e `query_id`.

```text
logs/pipeline-AAAA-MM-DD.jsonl
```

Os eventos registram estágio, status, latência, entrada, saída, tokens, modelo e informações adicionais. O uso de tokens é preenchido nas chamadas ao LLM quando informado pelo serviço.

Os estágios de consulta incluem:

- `query_analysis`;
- `roteamento`;
- `retrieval_denso`;
- `retrieval_bm25`;
- `fusao_rrf`;
- `geracao`;
- `validacao`;
- `consulta_estruturada`;
- `consulta_agregada`;
- `feedback`.

O schema admite `rerank`; na versão auditada, seus detalhes são registrados na fusão e no logger do módulo, sem comprovação de evento JSONL próprio por consulta.

Coleta, ingestão e indexação ainda utilizam principalmente `print`. Sua instrumentação estruturada não atende integralmente ao contrato de logging do enunciado.

Um resultado correto após fallback não elimina o timeout anterior registrado nos logs.

Logs, histórico SQLite e feedback JSONL são mecanismos distintos.
A persistência foi conferida em processos separados, preservando
resultado integral, tabelas, fontes, identificadores e vínculo do feedback.
A reabertura da consulta `4c11bd77` foi confirmada na interface,
com pergunta preenchida e sem duplicação da tabela.

A atualização automática da lista foi conectada ao botão Consultar
e à tecla Enter. Os testes relacionados passaram; a consulta `8474c27d` foi conferida na lista do histórico pelo procedimento solicitado.

Nas consultas combinadas analíticas, a execução documental possui
`documental_run_id` e `documental_query_id` próprios, referenciados no
resultado principal. Consulte também esses identificadores nos logs.

## 13. Limitações do recorte

- O sistema responde sobre os arquivos fornecidos, não sobre todo o PNCP.
- Ano da compra não equivale a ano de publicação.
- A UF da unidade administrativa não garante o local de execução do objeto.
- O cálculo do PCA utiliza o CSV integral; o recorte de ano e UF está associado à origem do arquivo.
- As agregações não são calculadas apenas sobre os resultados top-k.
- Consultas determinísticas podem apresentar proveniência por arquivo, filtros e recorte, sem citações no formato de chunk.
- Vínculos são pesquisados por identificadores; ausência de correspondência não comprova inexistência de documentos relacionados.
- Publicação, homologação, data desejada e vigência têm significados diferentes.
- A representação de vigência nos metadados precisa de adequação; não foi demonstrada comparação de versões normativas vigentes e revogadas.
- O serviço externo pode apresentar demora ou timeout.
- Histórico e interface pública dependem das condições de acesso e persistência da instância.

## 14. Estrutura e responsabilidades

```text
app/                    Interface, histórico, feedback e adaptador
src/                    Planejamento, execução, recuperação e geração
testes/                 Testes e fixtures
eval/                   Avaliações históricas
docs/                   Guias, relatórios e evidências versionadas
acompanhamento/          Relatos individuais
data/inventory/         Inventários e diffs
data/raw/               Dados brutos — ignorados pelo Git
data/processed/         Dados processados — ignorados pelo Git
data/indices/           Índices e cache — ignorados pelo Git
logs/                   Logs locais — ignorados pelo Git
```

| Área | Responsável principal |
|---|---|
| Coordenação | Maria Eduarda |
| Coleta e versionamento | Janice |
| Ingestão e indexação | Eridalgo |
| Roteamento e recuperação | Luiz Carlos |
| Geração, schemas, guardrails e testes | Felipe e Calvin |
| Observabilidade, interface e integração | Maria Eduarda |
| Documentação | Maria Eduarda, com contribuição da equipe |

A divisão por módulo não impede colaboração. Os acompanhamentos individuais devem registrar o trabalho efetivamente realizado e o uso de IA, conforme o enunciado.

## 15. Documentação da entrega

- [Correções de 21/10](docs/CORRECOES_RESPOSTAS_2026-10-21.md).
- [Fechamento histórico de 19/10](docs/FECHAMENTO_ENTREGA_2026-10-19.md).
- [Guia de restauração](docs/GUIA_RESTAURACAO_2172.md).
- [Reprodução e testes](docs/reproducao_d31d05a_2026-10-19/RELATORIO.md).
- [Comparação dos rankings](docs/comparacao_recuperacao_2026-10-19/RELATORIO.md).
- [Comparação das respostas](docs/avaliacao_respostas_recuperacao_2026-10-19/RELATORIO.md).
- [Avaliação complementar da Janice](docs/avaliacao_complementar_janice_2026-10-19/README.md).
- [Personas](PERSONAS.md).
- [Inventário](CORPUS_INVENTORY.md).
- [Manifesto](corpus_manifest.yaml).
- [Arquitetura atual e planejamento inicial](ARQUITETURA.md).

Relatórios históricos preservam os resultados de suas datas. Consulte o commit e o escopo de cada evidência antes de compará-los.

## 16. Pendências para atendimento integral ao enunciado

A versão funcional marcada ainda possui os seguintes pontos de adequação:

1. Confirmar execução e publicação da correção do teste de metadados e das vinte fixtures preparadas.
2. Completar coleta integral, idempotência operacional, limitação de taxa e registro de falhas por fonte.
3. Alinhar manifesto e ingestão quanto a sensibilidade e vigência.
4. Centralizar endpoint, modelos e configuração.
5. Instrumentar coleta, ingestão e indexação com logs estruturados.
6. Reavaliar as perguntas das personas na revisão corrigida, incluindo a rota e as evidências de P03.
7. Conferir a atualização automática da lista após nova consulta; a restauração da pergunta pelo histórico já foi confirmada.
8. Registrar reprodução por outro integrante a partir do repositório remoto.
9. Identificar a versão e os artefatos utilizados no benchmark complementar da Janice.
10. Conferir acessos dos integrantes e do mentor, acompanhamentos individuais e preparação da demonstração.

Esses itens devem ser encerrados com evidências, sem remover ressalvas apenas por decisão editorial.

Novas correções devem preservar a tag existente e gerar outra revisão identificada. A atualização deste README não altera o corpus nem exige regeneração de embeddings.

## Consolidação da validação — 21/10/2026

Após o ajuste do indicador de conclusão das consultas combinadas, a suíte local completa teve **754 testes aprovados e sete `llm` desmarcados**. Em uma execução separada, os **sete testes de integração real foram aprovados**.

A interface respondeu à pergunta simples sobre homologações com oito itens, sem exigir instrução de tamanho da resposta. A consulta `8474c27d`, `query_id=q_10d777d6`, apareceu no histórico na conferência solicitada. A reabertura e a apresentação sem tabela duplicada já haviam sido conferidas na consulta `4c11bd77`.

A rodada parcial anterior de 18 testes foi seguida pela suíte completa de 754 testes. Os sete testes reais são uma rodada separada; não constituem avaliação universal das perguntas ou nova avaliação completa das personas.

Registros: [evidências](docs/validacao_respostas_2026-10-21/evidencias.json). A publicação e a integração remotas ainda precisam ser confirmadas.
