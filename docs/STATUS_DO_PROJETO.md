# Status do Projeto — Adaptive RAG para Contratações Públicas do RJ

**Grupo:** 1
**Residência:** TIC em Trilhas — PUC-Rio / Instituto ECOA
**Cenário:** Contratações Públicas do Estado do Rio de Janeiro
**Última atualização:** 02/10/2026

Este documento reúne os resultados já demonstrados pela equipe e as
pendências informadas até esta atualização. As novas entregas em branches
devem ser diferenciadas das funcionalidades integradas à versão utilizada
na demonstração.

## 1. Objetivo

Desenvolver um sistema que responda perguntas sobre contratações públicas
em linguagem natural, selecionando as bases necessárias e apresentando
evidências verificáveis.

| Natureza | Conteúdo utilizado |
|---|---|
| Estruturada | Contratações publicadas no PNCP |
| Normativa | Lei nº 14.133/2021 |
| Conversacional | Três atas em PDF e uma comunicação sintética |
| Agregada | Plano de Contratações Anual e resultados por item |

## 2. Resumo dos dados preparados

O corpus de referência possui **8 arquivos** distribuídos nas quatro
naturezas.

A coleta estruturada foi concluída com:

- **28 páginas coletadas**;
- **1.358 registros**;
- **1.358 identificadores PNCP preenchidos e únicos**;
- **nenhuma duplicação de identificadores**.

As 28 páginas são páginas da API, e não 28 registros.

A ingestão validada produziu:

| Natureza | Chunks |
|---|---:|
| Estruturada | 1.358 |
| Normativa | 217 |
| Conversacional | 31 |
| Agregada | 519 |
| **Total** | **2.125** |

A base agregada processada contém uma **amostra de 500 itens do PCA**
e **19 itens de uma contratação específica**. Essa amostra não representa
todo o PCA nem todas as contratações do Estado.

## 3. Funcionamento do pipeline

O fluxo implementado realiza:

1. análise da pergunta e verificação das regras de recusa;
2. seleção das bases e extração dos filtros;
3. busca densa por embeddings e busca lexical BM25;
4. filtragem dos candidatos;
5. fusão dos rankings por RRF;
6. geração da resposta com evidências;
7. validação da estrutura de saída;
8. apresentação na interface e registro dos eventos.

O módulo de rerank está em desenvolvimento e permanece desativado por
padrão. Sua validação real depende do endpoint disponibilizado pelo
professor.

## 4. Funcionalidades já validadas

| Frente | Resultado confirmado |
|---|---|
| Coleta | Coleta estruturada concluída com retentativas e progresso salvo |
| Versionamento | Comparação entre snapshots e preservação da versão anterior |
| Ingestão | 2.125 chunks com IDs preenchidos e únicos, sem textos vazios |
| PDFs | Fatiamento em blocos de aproximadamente 2.000 caracteres |
| Indexação | FAISS, BM25 e lista de IDs persistidos |
| Cache | Reexecução da indexação com 2.125 embeddings em cache e zero novos envios |
| Roteamento | Seleção das quatro naturezas e tratamento de recusa |
| Recuperação | Busca Dense, BM25 e fusão RRF |
| Conversacional | Recuperação de três evidências sanitizadas em consulta real |
| Geração | Resposta sobre contratações de tecnologia com referências aos chunks |
| Interface | Resposta, rotas, filtros, evidências e informações da execução |
| Feedback | Avaliação e comentário registrados em JSONL |
| Observabilidade | Eventos identificados por query_id e run_id |

A igualdade de quantidades e a correspondência dos IDs foram verificadas.
Essas verificações não substituem a conferência da compatibilidade entre
o conteúdo dos chunks e os índices sempre que os dados forem alterados.

## 5. Correções concluídas desde o documento anterior

### Filtro de UF

O roteador deixou de adicionar `uf: RJ` automaticamente a perguntas sem
localização explícita.

Foram confirmados os comportamentos:

- pergunta sem localização: `uf: null`;
- pergunta mencionando RJ ou Rio de Janeiro: `uf: RJ`;
- preservação do filtro de ano quando informado.

### Ano da base agregada

A extração passou a utilizar reconhecimento de ano por regex.

Na verificação dos 519 chunks agregados, não foram encontrados anos
preenchidos fora do formato de quatro dígitos.

Essa verificação de formato deve ser complementada pela comparação com
as datas e os identificadores de origem.

### Metadados conversacionais

Os 31 chunks conversacionais passaram a apresentar UF RJ conforme o
mapeamento implementado para os arquivos do cenário.

### Recuperação conversacional

A investigação identificou que a política de sensibilidade bloqueava
os chunks classificados como restritos.

Foi implementado o encaminhamento dos chunks conversacionais restritos
para mascaramento antes da apresentação das evidências.

Na consulta validada, foram obtidos:

- rota `conversacional`;
- UF não inventada;
- 31 candidatos Dense após filtragem;
- 31 candidatos BM25 após filtragem;
- 31 candidatos na fusão RRF;
- 3 evidências retornadas;
- classificação de saída `restrito_sanitizado`.

O mascaramento possui testes para CPF, telefone e e-mail. A classificação
de saída não garante, por si só, a remoção de todo tipo de dado pessoal.

### Proteção contra ingestão vazia

A ingestão passou a lançar uma exceção quando nenhum chunk é produzido,
evitando a substituição da saída por um arquivo vazio.

O comportamento foi testado em diretório temporário sem o corpus.

## 6. Interface e feedback

A interface Gradio apresenta:

- campo para pergunta;
- seleção da quantidade de evidências;
- resposta gerada;
- bases selecionadas;
- filtros;
- evidências e fontes;
- query_id e run_id;
- latência e tokens;
- indicador de progresso por etapas;
- avaliação Útil ou Não útil;
- comentário opcional;
- botão de envio do feedback;
- confirmação do salvamento.

O indicador de progresso utiliza marcos das etapas do pipeline.
Ele não representa uma estimativa exata do tempo restante.

O feedback é armazenado, por padrão, em:

`data/feedback/feedback.jsonl`

O caminho pode ser configurado pela variável `FEEDBACK_PATH`.

Cada registro inclui:

- data e hora;
- pergunta;
- avaliação;
- comentário;
- query_id;
- run_id;
- rota;
- fontes.

Foram conferidos registros de feedback com os identificadores da consulta
e as fontes correspondentes.

O arquivo permanece disponível após reiniciar a interface no mesmo
ambiente. No Colab, a persistência entre runtimes depende de preservar
o arquivo em armazenamento externo, como o Drive.

O histórico completo de perguntas e respostas ainda deve ser concluído.
O arquivo de feedback não substitui esse histórico.

## 7. Versionamento do corpus

A comparação entre a v2 e a nova coleta estruturada apresentou:

| Resultado | Quantidade |
|---|---:|
| Registros na v2 | 1.358 |
| Registros na nova coleta | 1.358 |
| IDs adicionados | 0 |
| IDs removidos | 0 |
| Registros idênticos | 1.314 |
| Registros alterados | 44 |

A atualização isolada gerou a v3 com **8 arquivos e zero falhas**
no inventário, preservando a v2.

Na comparação dos arquivos:

- 7 permaneceram idênticos;
- 1 foi alterado;
- nenhum foi adicionado ou removido.

O arquivo alterado foi `contratacoes_publicacao.json`.

Os inventários e o diff estão registrados no repositório.
Os dados brutos permanecem fora do Git.

**Atenção à versão utilizada:** os testes de ingestão e recuperação
descritos neste documento foram realizados com o corpus restaurado em
`data/raw/v2`. A existência da v3 não significa que ela já esteja sendo
utilizada pela ingestão e pelos índices da demonstração.

## 8. Testes e evidências de validação

Os resultados abaixo pertencem a momentos e versões de trabalho
diferentes. Eles não devem ser somados.

| Validação | Resultado informado |
|---|---|
| Correção do filtro de UF | 4 testes específicos aprovados |
| Sanitização, recuperação e geração | 51 testes aprovados |
| Suíte offline após a sanitização | 118 testes aprovados |
| Suíte offline após feedback e progresso | 132 testes aprovados |
| Integração executada por Felipe em 30/09 | 9 testes aprovados |
| Suíte completa informada por Felipe em 30/09 | 139 testes aprovados |
| Módulo de rerank com testes simulados | 4 testes aprovados |

Os números representam os resultados registrados pela equipe.
Antes de apresentar um total como resultado da versão atual, é necessário
associar a execução ao commit e ao ambiente utilizados.

Testes aprovados não substituem a avaliação da qualidade das respostas,
da relevância das evidências e da correção das fontes.

## 9. Entregas recentes e situação

| Responsável | Entrega | Situação registrada |
|---|---|---|
| Eduarda | Feedback persistido e progresso na interface | Integrado pelo PR #9 e validado na suíte offline |
| Janice | Personas revisadas e nove perguntas de avaliação | Arquivos disponibilizados no repositório |
| Luiz | Ajustes do fallback e seleção de evidências multirrota | Implementação e testes informados; confirmar integração e validação real na versão atual |
| Eridalgo | Estrutura configurável de rerank | Módulo e testes simulados informados; integração e endpoint real pendentes de confirmação |
| Felipe | Testes de integração e complementação dos logs | Testes executados; campos adicionais e testes de observabilidade em andamento |
| Calvin | Reprodutibilidade | Verificações iniciadas; execução completa do guia ainda não comprovada |

## 10. Limitações e próximas atividades

- Confirmar e validar a recuperação multirrota na versão integrada.
- Concluir a integração do rerank e testar o endpoint real quando disponível.
- Complementar os logs Dense e BM25 com rotas, bases, candidatos e IDs.
- Executar e registrar os resultados das nove perguntas das personas.
- Comparar métodos de recuperação por meio de avaliação e ablação.
- Concluir o histórico persistido de consultas.
- Validar a execução em ambiente limpo seguindo somente o guia existente.
- Alinhar manifesto, versão do corpus, ingestão e índices.
- Medir a latência por etapa antes de definir otimizações.
- Revisar relevância, fidelidade e correspondência das fontes nas respostas.
- Concluir a documentação e a preparação da entrega final.

A latência varia entre consultas e depende das chamadas aos serviços de
modelos. O indicador de progresso melhora a visualização das etapas,
mas não comprova redução do tempo de execução.

## 11. Demonstração de atualização

### Pergunta principal

> Quais contratações envolvem serviços de tecnologia?

Conferir e mostrar:

- resposta baseada nas evidências;
- rota estruturada;
- filtros;
- pelo menos uma fonte;
- chunk_id da evidência;
- query_id e run_id;
- latência e tokens;
- envio e confirmação do feedback.

### Pergunta alternativa

> O que a Lei nº 14.133 estabelece sobre licitações?

Conferir a rota normativa e a correspondência entre as afirmações
da resposta e os trechos da lei recuperados.

### Controle de escopo

> Esse contrato foi uma fraude?

O comportamento já validado é a recusa da acusação, acompanhada da
explicação da limitação e de uma lista vazia de evidências.

Se o endpoint estiver indisponível, utilizar um resultado previamente
salvo e identificá-lo como execução anterior. Não apresentar uma saída
salva como se fosse uma consulta ao vivo.

## 12. Arquivos de referência

| Arquivo | Responsabilidade |
|---|---|
| corpus_manifest.yaml | Fontes, arquivos, hashes e critérios do corpus |
| src/fetch_corpus.py | Coleta, inventário e atualização |
| src/ingest.py | Extração, metadados e chunks |
| src/index.py | Cache e índices FAISS/BM25 |
| src/router.py | Rotas, filtros e recusas |
| src/retrieve.py | Recuperação, filtragem e RRF |
| src/generate.py | Geração com evidências |
| src/schema.py | Validação das estruturas |
| src/obs.py | Logs estruturados |
| app/app.py | Interface |
| app/pipeline_adapter.py | Integração do pipeline com a interface |
| app/feedback_store.py | Registro persistido de feedback |
| eval/perguntas_personas.json | Casos de avaliação |
| docs/GUIA_DO_PIPELINE.md | Preparação e execução do projeto |

Para a atualização ao professor, utilizar o objetivo, os dados preparados,
as funcionalidades validadas, uma consulta na interface e as pendências.
Os arquivos técnicos ficam disponíveis para perguntas específicas.

## Validação da interface — 05/10/2026

### Implementação

- Interface integrada ao executor de consultas estruturadas e documentais.
- Contagens apresentam total calculado, filtros, recorte e fonte.
- Listagens apresentam somente os campos solicitados e permitem paginação.
- O total permanece visível durante a navegação.
- A quantidade de evidências limita somente a recuperação documental.
- Consultas combinadas apresentam separadamente o cálculo estruturado e a resposta documental.
- Fontes estruturadas, recuperadas e citadas são identificadas separadamente.
- Feedback persistido permanece associado à resposta exibida, mesmo após editar a pergunta sem executar outra consulta.

### Validação realizada

Ambiente: Colab, com corpus v2 restaurado, 1.358 registros estruturados
e artefatos de recuperação com 2.125 chunks.

- 12 testes específicos da interface aprovados.
- 204 testes offline aprovados; testes de integração excluídos dessa execução.
- Verificação de sintaxe e `git diff --check` sem erros.
- Contagem por ano da compra 2026: 1.234 registros.
- Listagem por ano da compra 2026 e valor estimado estritamente acima de R$ 500 mil: 560 correspondências.
- Tabela com apenas objeto e valor estimado, 20 registros por página e 28 páginas.
- Navegação até a página 3 preservou total, filtros e campos.
- Consulta documental do art. 4º recuperou o chunk pertinente e exibiu fontes recuperadas e citadas com uma evidência.
- Envio de feedback e limpeza da interface verificados.
- Vínculo do feedback após editar a pergunta confirmado no JSONL:
  query_id q_98f92df4 e run_id 0a353c48.

### Pendências e limitações

- Consulta combinada preservou o total de 1.234, mas não recuperou evidências normativas.
- Os logs da execução 96d4e6c9 mostram o filtro ano 2026 aplicado à recuperação normativa. A separação dos filtros por estratégia precisa ser corrigida e validada com Luiz.
- A apresentação combinada e sua paginação foram verificadas por testes simulados; a validação real completa com evidências documentais permanece pendente.
- Com três evidências, a geração da resposta sobre o art. 4º desviou do tema, apesar de recuperar o trecho pertinente.
- Com uma evidência, a resposta apresentou uma simplificação sobre valor do item versus valor da licitação.
- Essas falhas de conteúdo permanecem pendentes de revisão da geração e da recuperação.
- Os casos de avaliação da Janice se referem ao corpus v3. Esta execução com v2 não representa aprovação integral desses casos.
- O critério textual anterior de tecnologia não equivale à classificação contextual de TIC definida na avaliação.
