# Acompanhamento — Maria Eduarda Ribeiro da Silva

## Encontro 1 — 14/09/2026

### Minha contribuição

* Participei da configuração inicial do repositório e da organização dos acessos da equipe.
* Analisei o Cenário 1 — Contratações Públicas do Estado do Rio de Janeiro.
* Participei da organização inicial das atividades do projeto.
* Analisei as orientações do Grande Desafio e os requisitos relacionados à construção e organização do corpus.

### Uso de IA

Utilizei assistente de IA para apoiar a compreensão das instruções do desafio e a organização inicial das atividades. Revisei e ajustei as informações antes de utilizá-las no projeto.

### Resumo da equipe

A equipe configurou o repositório privado, organizou os acessos dos integrantes e iniciou a análise do Cenário 1.

### Próximos passos

* Elaborar o `ARQUITETURA.md`.
* Elaborar o `PERSONAS.md`.
* Criar o `corpus_manifest.yaml`.
* Definir a divisão de responsabilidades da equipe.


---

## Encontro 2 — 16/09/2026

### Minha contribuição

* Elaborei a versão inicial do `ARQUITETURA.md`, organizando a arquitetura proposta para o sistema e o fluxo das etapas do pipeline RAG.
* Participei da definição da divisão de responsabilidades entre os integrantes da equipe.
* Assumi a coordenação da equipe, ficando também responsável pelas atividades relacionadas à interface e à documentação do projeto.
* Organizei o planejamento das próximas atividades considerando a ordem de desenvolvimento dos módulos e as dependências existentes entre as etapas.
* Ajudei a definir os marcos necessários para que uma etapa disponibilize os recursos necessários para o avanço da etapa seguinte.
* Acompanhei o andamento inicial das atividades da equipe, incluindo o início da coleta dos dados.

### Uso de IA

Utilizei assistente de IA como apoio na organização e revisão do `ARQUITETURA.md`, na análise das dependências entre os módulos e na organização do planejamento das atividades. Revisei e ajustei o conteúdo antes de incorporá-lo ao projeto.

### Resumo da equipe

A equipe definiu a divisão de responsabilidades do projeto e iniciou a execução das atividades. A coleta dos dados já foi iniciada e foram discutidas as dependências entre as diferentes etapas do sistema para permitir que o desenvolvimento avance de forma organizada.

### Próximos passos

* Acompanhar o andamento das atividades e identificar possíveis bloqueios entre os módulos.
* Atualizar o `ARQUITETURA.md` com a divisão de responsabilidades definida pela equipe.
* Iniciar o desenvolvimento e a organização da interface.
* Acompanhar a integração progressiva entre os módulos do sistema.

## Encontro 3 — 18/09/2026

### Minha participação

- Atualizei o `ARQUITETURA.md` com a divisão de responsabilidades definida pela equipe.
- Desenvolvi a primeira versão da interface em Gradio e realizei testes de execução no Google Colab.
- Estruturei o adaptador responsável por conectar a interface aos módulos de roteamento, recuperação e, futuramente, geração.
- Implementei o módulo `src/obs.py` para registrar os eventos do pipeline em logs estruturados no formato JSONL.
- Criei o `docs/GUIA_DO_PIPELINE.md` para explicar o funcionamento geral do sistema, as entradas e saídas dos módulos e a estratégia de testes.
- Criei a primeira versão do `README.md`, incluindo objetivo, arquitetura, instalação, execução da interface, política de sensibilidade e estado atual do projeto.
- Acompanhei o andamento das responsabilidades da equipe e auxiliei na organização das próximas entregas.

### Apoio de IA

Utilizei ferramentas de IA para apoiar a estruturação inicial da interface, do módulo de observabilidade e da documentação técnica. Também utilizei esse suporte para revisar comandos de execução no Colab, organizar o guia do pipeline e identificar problemas de autenticação e sincronização com o GitHub. Todo o conteúdo foi revisado, testado e ajustado antes de ser incorporado ao repositório.

### Atividades realizadas pela equipe

Durante o encontro, a equipe avançou na ingestão, indexação, roteamento, recuperação, documentação e integração inicial do sistema. Também foram discutidas as dependências entre os módulos e a necessidade de compreender os contratos de entrada e saída para o desenvolvimento dos testes e da geração das respostas.

### Dificuldades encontradas

- Integração da interface enquanto o módulo de geração ainda está em desenvolvimento.
- Ausência de evidências para algumas rotas que ainda não possuem bases completamente processadas e indexadas.
- Problemas de autenticação e sincronização do repositório no Google Colab.
- Necessidade de alinhar as entregas e dependências entre os integrantes da equipe.

### Próximas atividades

- Integrar a interface ao `generate.py` e ao `schema.py` quando esses módulos estiverem disponíveis.
- Integrar o `obs.py` aos demais estágios do pipeline.
- Validar o funcionamento da interface com as quatro bases.
- Acompanhar a implementação dos testes unitários, de contrato e de integração.
- Atualizar o README conforme novos módulos forem finalizados.

---

## Encontro 4 — 21/09/2026

### Minha participação

- Acompanhei a integração dos módulos desenvolvidos pela equipe e auxiliei na identificação de incompatibilidades entre `ingest.py`, `retrieve.py` e `generate.py`.
- Integrei o `obs.py` ao fluxo principal para registrar as etapas de recuperação, geração e validação em logs JSONL.
- Atualizei o `pipeline_adapter.py` para conectar `retrieve.py`, `generate.py`, `schema.py` e a interface Gradio.
- Realizei um teste integrado com consulta normal, obtendo roteamento para a base estruturada, recuperação Dense + BM25, fusão RRF, duas evidências, resposta gerada pelo LLM, fontes, latência e contagem de tokens.
- Auxiliei Luiz na correção do `retrieve.py`, que ainda esperava o `chunk_id` fora de `metadata`.
- Orientei a equipe sobre dependências, testes, atualização dos acompanhamentos e continuidade das atividades.

### Dificuldades encontradas

Durante a integração, ocorreram incompatibilidades entre os contratos dos módulos, ausência dos índices locais no Colab e conflitos de rebase causados por alterações simultâneas no repositório. As correções foram realizadas preservando as versões mais recentes enviadas pela equipe.

O teste atual ainda utiliza fixtures, portanto existem limitações nos dados simulados, como diferenças entre o ano identificado na consulta e o ano presente no nome do arquivo.

### Apoio de IA

Utilizei IA para auxiliar na análise dos erros de integração, na revisão dos contratos entre os módulos e na estruturação do adaptador do pipeline. Revisei as sugestões antes da aplicação e adaptei o código ao formato já utilizado no projeto.

### Atividades realizadas pela equipe

A equipe avançou na coleta, ingestão, indexação, roteamento, recuperação, schemas, geração e testes. Também foram corrigidas incompatibilidades entre os metadados dos chunks e o módulo de recuperação, permitindo a execução do pipeline integrado com dados simulados.

### Próximas atividades

- Repetir a integração com dados reais quando a API do PNCP estiver disponível.
- Ampliar a instrumentação para registrar individualmente os demais estágios do pipeline.
- Revisar a extração de filtros realizada pelo roteador.
- Executar os testes automatizados e validar a interface com as perguntas das personas.

---

## Encontro 5 — 23/09/2026

### Minha participação

- Acompanhei o andamento das entregas da equipe e revisei as atividades concluídas, pendentes e dependentes de outros módulos.
- Auxiliei na validação das correções realizadas em `router.py` e `retrieve.py`, incluindo filtros monetários, roteamento de consultas sobre o PCA e regras de recusa.
- Acompanhei a integração das correções de roteamento e recuperação à branch `main` por meio de Pull Request.
- Validei os testes específicos de roteamento e recuperação e acompanhei a execução da suíte de testes offline do projeto.
- Analisei o teste de integração ponta a ponta desenvolvido por Felipe, verificando os cenários de recuperação, geração, fontes, `top_k`, guardrails e recusa.
- Identifiquei uma incompatibilidade de import no teste de integração e a ausência dos artefatos locais necessários para a execução completa após o reinício do ambiente do Colab.
- Testei a interface Gradio com uma consulta de recusa e confirmei a aplicação dos guardrails, a ausência de evidências e a exibição de confiança, latência, tokens, `query_id` e `run_id`.
- Melhorei o tratamento da interface quando os artefatos de ingestão e indexação não estão disponíveis, substituindo a mensagem técnica por uma orientação compreensível ao usuário.
- Validei os logs JSONL e confirmei a presença dos campos obrigatórios em todos os registros analisados.
- Identifiquei que uma mesma consulta utilizava dois valores diferentes de `run_id` e corrigi a propagação desse identificador entre o adaptador, a recuperação e o roteamento.
- Atualizei os mocks dos testes de recuperação para manter compatibilidade com o parâmetro opcional `run_id`.

### Resultados obtidos

- A interface executou corretamente uma consulta recusada pelos guardrails.
- A ausência dos índices passou a ser apresentada de forma amigável, sem interromper a interface.
- Os registros analisados apresentaram todos os campos obrigatórios definidos na arquitetura.
- As etapas `query_analysis`, `roteamento`, `fusao_rrf`, `geracao` e `validacao` passaram a utilizar o mesmo `run_id`.
- O teste de integração enviado por Felipe contém sete testes, incluindo mais de três cenários ponta a ponta.
- A execução completa das consultas que utilizam recuperação ficou pendente devido à ausência local dos chunks e índices após o reinício do Colab.

### Apoio de IA

Utilizei ferramentas de IA como apoio para revisar os resultados dos testes, interpretar falhas de integração, identificar a duplicidade do `run_id` e organizar as correções no adaptador e no módulo de recuperação. As sugestões foram conferidas por meio da execução da interface, da inspeção dos logs e dos testes disponíveis antes de serem consideradas no projeto.

### Atividades realizadas pela equipe

A equipe avançou na ingestão, indexação, roteamento, recuperação, geração e testes. Luiz concluiu os ajustes de roteamento e recuperação. Eridalgo validou a ingestão das quatro bases, a geração dos chunks e a persistência dos índices, mantendo como próxima etapa o aprimoramento dos metadados específicos. Felipe adicionou os testes de integração ponta a ponta. Também acompanhei as pendências e dependências necessárias para a continuação das atividades.

### Dificuldades encontradas

- Ausência dos chunks e índices locais após o reinício do ambiente do Google Colab.
- Incompatibilidade de import no teste de integração.
- Utilização de valores diferentes de `run_id` entre etapas pertencentes à mesma consulta.
- Necessidade de atualizar mocks após a alteração do contrato do recuperador.
- Dependência dos artefatos regenerados para validar consultas normais na interface e executar os testes ponta a ponta completos.
- Necessidade de acompanhar entregas da equipe que ainda não receberam retorno ou commit correspondente.

### Próximas atividades

- Validar novamente a suíte de testes offline após as correções.
- Repetir os testes ponta a ponta quando os chunks e índices estiverem disponíveis.
- Validar a interface com consultas normais, múltiplas bases, fontes e evidências.
- Conferir os logs completos das etapas de recuperação com os artefatos definitivos.
- Acompanhar a correção do teste de integração e o registro do marcador `llm`.
- Realizar a integração final após a atualização dos metadados e a regeneração dos índices.

---

## Encontro 6 — 25/09/2026

### Minha participação

- Acompanhei e validei as atualizações realizadas pela equipe nos módulos de coleta, ingestão, roteamento, recuperação e testes.
- Testei a coleta da base estruturada diretamente pela API do PNCP.
- Durante o teste, identifiquei instabilidade temporária na API, com timeout e respostas HTTP 502 e 503.
- Confirmei que o mecanismo de retentativas funcionou e permitiu concluir a coleta das 28 páginas.
- Validei a obtenção de 1.358 registros estruturados, com 1.358 IDs únicos e nenhum registro duplicado.
- Identifiquei que a coleta atual possui hash diferente do snapshot registrado no manifesto, apesar de manter a mesma quantidade de registros.
- Preservei a nova coleta no Google Drive para permitir a comparação com a versão anterior.
- Validei as correções realizadas nos separadores e metadados dos dois arquivos CSV da base agregada.
- Confirmei o preenchimento de UF, ano, órgão, valor e vigência nos 500 chunks utilizados como amostra do PCA.
- Confirmei o preenchimento dos metadados disponíveis nos itens homologados, incluindo ano, valor, fornecedor e data de homologação.
- Verifiquei que a ingestão gerou 2.102 chunks, todos com IDs preenchidos e únicos, sem textos vazios.
- Analisei o tamanho dos chunks da base conversacional e identifiquei que os três PDFs foram processados como chunks únicos excessivamente grandes.
- Validei o fluxo de recusa do pipeline com uma consulta envolvendo acusação de fraude.
- Confirmei que a consulta recusada não retornou evidências e apresentou resposta compatível com os guardrails.
- Verifiquei que as etapas `query_analysis`, `roteamento`, `fusao_rrf`, `geracao` e `validacao` utilizaram o mesmo `run_id`.
- Validei a mensagem amigável apresentada pela interface quando os artefatos de indexação não estão disponíveis.
- Executei 29 testes específicos de observabilidade, geração e schema, todos aprovados.
- Executei a suíte offline disponível, obtendo 109 testes aprovados.
- Confirmei que o commit responsável pela unificação do `run_id` e pelo tratamento da falha da interface está presente na branch remota `main`.

### Resultados obtidos

- A coleta automatizada conseguiu recuperar os 1.358 registros mesmo diante da instabilidade temporária da API.
- Os registros coletados apresentaram 1.358 IDs únicos e nenhuma duplicação.
- Os separadores e os principais metadados da base agregada foram corrigidos.
- A ingestão manteve 2.102 chunks válidos antes da revisão do fatiamento dos PDFs.
- O fluxo de recusa, os guardrails e a ausência de evidências em consultas recusadas funcionaram corretamente.
- Todas as etapas registradas para a consulta testada utilizaram um único `run_id`.
- A interface apresentou uma orientação compreensível quando os índices estavam ausentes.
- Os 29 testes específicos e os 109 testes offline foram aprovados.

### Dificuldades encontradas

- A API do PNCP apresentou timeout e respostas HTTP 502 e 503 durante as primeiras tentativas.
- O conteúdo coletado atualmente apresentou hash diferente do snapshot anterior, indicando alteração na fonte pública.
- Os três PDFs conversacionais foram transformados em chunks únicos com aproximadamente 23 mil, 32 mil e 49 mil caracteres.
- Os índices FAISS, BM25 e a lista de IDs ainda não estavam disponíveis no ambiente atual do Google Colab.
- A suíte de testes apresentou um aviso de configuração relacionado ao `testpaths`, embora todos os testes offline tenham sido aprovados.

### Apoio de IA

Utilizei ferramentas de IA como apoio para organizar os procedimentos de validação, interpretar os resultados da coleta, analisar os metadados gerados, identificar o tamanho inadequado dos chunks conversacionais e revisar os registros de observabilidade. Todos os resultados foram conferidos por meio da execução dos comandos, inspeção dos arquivos gerados e testes automatizados.

### Atividades realizadas pela equipe

A equipe avançou na coleta e validação do corpus, no preenchimento dos metadados específicos, nos testes de roteamento e recuperação e na preparação dos testes de integração. A correção da base agregada foi validada, mantendo como pendência a melhoria do fatiamento dos PDFs conversacionais. Também foram revisados os resultados da suíte offline e as dependências necessárias para a futura validação ponta a ponta.

### Próximas atividades

- Acompanhar a divisão dos três PDFs conversacionais em chunks menores, com sobreposição e preservação dos metadados.
- Regenerar os chunks após a correção do fatiamento.
- Reconstruir os índices FAISS e BM25 utilizando o cache de embeddings.
- Validar a consistência entre a quantidade de chunks, vetores, documentos BM25 e IDs persistidos.
- Executar os testes de integração com os artefatos definitivos.
- Validar consultas normais, agregadas, conversacionais, normativas e de recusa na interface.
- Preparar uma atualização objetiva do andamento do projeto para o próximo encontro com o professor.

---

## Encontro 7 — 28/09/2026

### Minha participação

- Atualizei a documentação geral do projeto e disponibilizei um arquivo de status para facilitar o acompanhamento das entregas e a apresentação do andamento ao professor.
- Acompanhei a correção do roteamento realizada por Luiz, verificando o comportamento do filtro de UF em perguntas com e sem localização explícita.
- Confirmei que perguntas sem localização passaram a retornar `uf: null`, enquanto consultas com `RJ` ou `Rio de Janeiro` mantiveram `uf: RJ`.
- Acompanhei a criação de testes específicos para o filtro geográfico e validei a execução de 114 testes offline.
- Validei as atualizações realizadas por Eridalgo na ingestão, incluindo a extração de ano, o preenchimento da UF conversacional e a proteção contra a geração de arquivos de chunks vazios.
- Restaurei o corpus bruto no ambiente do Google Colab e executei novamente a ingestão.
- Confirmei a geração de 2.125 chunks, com 2.125 IDs únicos e nenhum texto vazio.
- Verifiquei que os 519 chunks agregados não apresentaram anos em formato inválido.
- Testei o roteamento de consultas estruturadas, conversacionais, normativas, agregadas e de recusa, confirmando as rotas esperadas nos cinco casos.
- Restaurei os índices persistidos e executei a interface Gradio com consultas das quatro bases e uma consulta sensível.
- Confirmei o funcionamento das respostas estruturada, normativa e agregada e da recusa por guardrails.
- Investiguei a ausência de evidências na consulta conversacional e identifiquei o ponto exato em que os resultados eram eliminados.
- Confirmei que a busca densa e o BM25 localizam os 31 chunks conversacionais, mas a filtragem remove todos porque estão classificados com sensibilidade `restrito`.
- Registrei a necessidade de revisar a política de sensibilidade antes de liberar evidências conversacionais, evitando a exposição de nomes, telefones, e-mails ou outros dados pessoais.

### Resultados obtidos

- A documentação de status do projeto foi integrada à branch principal.
- O filtro geográfico deixou de ser aplicado quando a pergunta não menciona localização.
- As cinco consultas de validação foram encaminhadas para as rotas esperadas.
- A ingestão gerou 2.125 chunks válidos.
- Os 114 testes offline foram aprovados.
- A interface executou consultas estruturadas, normativas, agregadas e de recusa.
- A causa da ausência de evidências conversacionais foi identificada na regra de sensibilidade, e não no roteamento, nos índices ou nos métodos Dense e BM25.

### Dificuldades encontradas

- O ambiente do Colab voltou para uma versão anterior da branch `main` após o reinício da sessão, exigindo nova atualização do repositório.
- O corpus bruto e os índices precisaram ser restaurados do Google Drive.
- Algumas consultas apresentaram demora elevada devido ao servidor dos modelos.
- A base conversacional possui documentos marcados como restritos, e a regra atual bloqueia todos antes da fusão RRF.
- A liberação desses documentos exige mascaramento ou sanitização das evidências para evitar exposição de dados pessoais.

### Apoio de IA

Utilizei ferramentas de IA para organizar os procedimentos de validação, interpretar os resultados do roteamento, investigar a recuperação conversacional e localizar a etapa responsável pela eliminação das evidências. Todas as conclusões foram verificadas por meio da execução do código, inspeção dos metadados, análise das funções e testes automatizados.

### Atividades realizadas pela equipe

Luiz corrigiu o filtro de UF no roteador e adicionou testes automatizados. Eridalgo atualizou a ingestão para preencher metadados conversacionais e impedir a sobrescrita por uma saída vazia. A equipe também avançou na documentação, nos testes offline e na validação integrada da interface.

### Próximas atividades

- Revisar a política de sensibilidade da base conversacional.
- Implementar mascaramento de dados pessoais nos textos e evidências.
- Permitir a recuperação apenas de conteúdo conversacional sanitizado.
- Repetir a busca densa, o BM25 e a fusão RRF após a correção.
- Validar novamente a consulta conversacional na interface.
- Executar a suíte de integração após a estabilização das quatro rotas.
