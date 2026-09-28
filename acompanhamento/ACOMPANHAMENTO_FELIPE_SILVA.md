# Acompanhamento — Felipe Silva

## Encontro 1 — 14/09/2026

### Minha contribuição

* Analisei o Cenário 1 — Contratações Públicas do Estado do Rio de Janeiro.
* Participei da organização inicial das atividades do projeto.
* Realizei análises e testes com os dados disponibilizados pela API do PNCP (https://pncp.gov.br/api/consulta/v3/api-docs). Selecionei uma contratação como amostra para avaliar tanto os dados estruturados fornecidos pela API quanto os documentos associados. Analisei um edital e um despacho com o objetivo de identificar as informações relevantes que deverão ser extraídas dos arquivos PDF e utilizadas nas próximas etapas de processamento e recuperação de informações. 

### Uso de IA

Utilizei IA para entender o funcionamento da API.

### Resumo da equipe

A equipe configurou o repositório privado, organizou os acessos dos integrantes e iniciou a análise do Cenário 1.

### Próximos passos

* Elaborar o ARQUITETURA.md.
* Elaborar o PERSONAS.md.
* Criar o corpus_manifest.yaml.
* Definir a divisão de responsabilidades da equipe.

## Encontro 2 — 16/09/2026

### Minha contribuição

* Criação das Personas: Foram analisadas as personas do Cenário 1 e definida a estratégia para criação das 3 personas próprias da equipe, cada uma com contexto de uso, nível de urgência e 3 perguntas de referência. As perguntas devem contemplar diferentes comportamentos do RAG, como consultas factuais, filtros, cross-source, vigência, recusa e fora de escopo, servindo posteriormente como base para avaliação e testes.

* Anonimização: Foi desenvolvido um anonimizador baseado em expressões regulares (Regex) para identificar e ocultar dados pessoais e sensíveis, como CPF, RG, e-mail, telefone, CEP, dados bancários e credenciais. Também foram elaborados casos de teste baseados nos documentos reais do projeto, preservando informações públicas relevantes, como CNPJ, número de processo e dados da contratação. O anonimizador poderá ser utilizado como uma camada dos guardrails, ajudando a impedir a exposição de dados sensíveis nas respostas do RAG.

### Uso de IA

Utilizei IA para duvidas sobre o funcionamento do Regex e para aplicabilidade dele no guardrails.

### Resumo da equipe

* Definir a divisão de responsabilidades da equipe.

### Próximos passos

* Elaborar o ARQUITETURA.md.

## Encontro 3 — 18/09/2026

### Minha contribuição

* Iniciei o desenvolvimento do schema.py para padronizar e validar os dados entre as etapas do RAG, definindo estruturas para roteamento, evidências, filtros, tokens e respostas, além de regras para recusas e consistência dos dados.

* Também iniciei o desenvolvimento do generate.py, responsável por gerar respostas fundamentadas nas evidências recuperadas, utilizando o Qwen3. Implementei tratamento de recusas, ausência de evidências, controle de tokens e latência, nível de confiança e guardrails para proteção de dados sensíveis.

* Por fim, iniciamos a pesquisa e estruturação da estratégia de testes unitários, de contrato e de integração, utilizando pytest. Também iniciei o planejamento de fixtures baseadas no corpus para permitir testes controlados, reproduzíveis e sem dependência de rede.

### Uso de IA

Utilizei IA para duvidas sobre o funcionamento do Regex e para aplicabilidade dele no guardrails e para o planejamento da etapa de testes.

### Resumo da equipe

Estamos finalizando a parte de gerar as perguntas e iremos iniciar os testes no próximo encontro. Tivemos dificuldades em consultar a API PNCP, ela retornava 502 Server Error: Bad Gateway. Iremos realizar mais testes para entender o motivo do erro.

### Próximos passos

Iremos iniciar o desenvolvimentos dos teste no próximo encontro.

## Encontro 4 — 21/09/2026

### Minha contribuição

* Revisão da estratégia de testes: analisei os requisitos do projeto para as três camadas previstas: testes unitários, de contrato e de integração.

* Validação dos testes existentes: revisei os testes dos módulos schema.py, generate.py, router.py e retrieve.py, verificando o comportamento individual de cada componente.

* Execução dos testes de integração: executei os testes ponta a ponta para avaliar o funcionamento conjunto das etapas do pipeline com perguntas conhecidas.

* Análise das falhas: investiguei os resultados dos testes de integração e identifiquei que as falhas estavam relacionadas à estrutura dos dados utilizados nos testes, especificamente ao campo chunk_id.

* Realizei uma correção no modulo generate.py. Erro na importação de outros modulos.

### Uso de IA

Utilizei IA para entender os erros e as respostas geradas pelos testes, o uso principal foi no teste de integração.

### Resumo da equipe

Finalizamos os teste dos modulos individualmente. Observamos pontos que precisão se corrigidos na etapa de ingestão e indexação, após a correção iremos executar o teste novamente.

### Próximos passos

Vamos dar continuidade no desenvolvimentos dos teste no próximo encontro. Focar na resolução dos problemas encontrados no teste de integração.

## Encontro 5 — 23/09/2026

### Minha contribuição

* Atualização do generate.py, integração da observabilidade na etapa de geração, registro de execução bem-sucedida e falhas do LLM, manutenção dos guardrails, fontes, confiança e contagem de tokens.

* Finalização dos testes de geração, ampliação do teste_generate.py, testes de resposta com e sem evidências, testes de recusa e resposta vazia, validação de CPF, RG, telefone, e-mail, dados bancários e credenciais, preservação de CNPJ, Resultado final: 18/18 testes aprovados.

* Teste de observabilidade, simulação de falha do LLM, confirmação do registro stage="geracao" e status="erro" no JSONL, validação do funcionamento do obs.py.

* Testes de integração ponta a ponta, validação do pipeline com Router → Retrieval → Generation, testes das consultas das personas e dos guardrails, resultado: 7/7 testes aprovados.

### Uso de IA

Utilizei IA para entender os erros e as respostas geradas pelos testes, o uso principal foi no teste de integração.

### Resumo da equipe

Finalizamos os teste dos modulos individualmente.

### Próximos passos

Vamos dar continuidade no desenvolvimentos dos teste no próximo encontro. Focar na resolução dos problemas encontrados no teste de integração e Validação do checklist, pendências de geração, contratos, guardrails, integração e registro de falhas atendidas e avaliação/benchmark ficou como próxima etapa.

## Encontro 6 — 25/09/2026

### Minha contribuição

* Ajustei a configuração do pytest e organizei os testes de integração, separando os testes locais dos testes de integração/E2E que dependem do LLM.

* Validei os testes de recusa e guardrails, garantindo que solicitações recusadas não acionem o LLM, não retornem fontes ou evidências e mantenham o consumo de tokens zerado.

* Verifiquei os artefatos de recuperação, incluindo chunks, FAISS, BM25 e IDs, confirmando a consistência quantitativa entre os arquivos utilizados nos testes.

* Ajustei a propagação do run_id entre recuperação e geração, permitindo utilizar o mesmo identificador durante uma execução e melhorando a rastreabilidade do pipeline.

* Validei a observabilidade por meio dos logs, confirmando o uso do mesmo run_id nas diferentes etapas de uma consulta.

* Executei os testes após atualizar minha branch com a main, obtendo 109 testes gerais e 7 testes de integração/E2E aprovados, totalizando 116 testes sem falhas antes do merge.

### Uso de IA

* Utilizei a IA para auxiliar na utilização de comandos do git e para resumir algumas informações das atividades atividades executadas. Ex: Como explicar os resultados obtidos nos testes e avaliação dos logs gerados.

### Resumo da equipe

* Estamos avançando bem e começando a corrigir detalhes. Praticamente todas as atividades ja estão bem adiantadas. Só precisamos resolver alguns detalhes que apareceram como as consultas feitas na API.

### Próximos passos

* Criar e executar um benchmark para avaliar o RAG, utilizando um conjunto de perguntas previamente definidas. 
* Verificar se o sistema seleciona a rota correta, recupera evidências relevantes, gera respostas fundamentadas nas fontes e aplica corretamente recusas e guardrails.
* Registrar os resultados e métricas para identificar possíveis pontos de melhoria no pipeline.

## Encontro 7 — 28/09/2026

### Minha contribuição

* Baixei e instalei as bibliotecas beautifulsoup4 e pypdf.

* Executei os testes offline, com 118 testes aprovados.

* Verifiquei os testes já existentes para extração do ano e não inferência indevida de UF, evitando duplicação de testes e adicionei testes de integração para recuperação da base conversacional e para a pergunta multirrota normativa + estruturada.

* Validei novamente as regras de recusa: 7 testes passaram, mantendo consultas recusadas sem evidências. Executei os testes de integração: 8 passaram e 1 falhou. O teste multirrota passou; a falha ocorreu na recuperação conversacional, que retornou zero evidências. (Preciso corrigir)

* Não consegui avançar mais por causa de problemas de conexão, estou tentando resolver o mais rápido possível.

### Uso de IA

* Utilizei apenas pra estruturar as atividades que executei hoje de acordo com as demandas enviadar pela gerente Maria Eduarda.

### Resumo da equipe

* Estamos avançando bem e começando a corrigir detalhes. Praticamente todas as atividades ja estão bem adiantadas. Só precisamos resolver alguns detalhes que apareceram como as consultas feitas na API.

### Próximos passos

* Corrigir a falha na recuperação conversacional. 
* Criar e executar um benchmark para avaliar o RAG, utilizando um conjunto de perguntas previamente definidas. 
* Verificar se o sistema seleciona a rota correta, recupera evidências relevantes, gera respostas fundamentadas nas fontes e aplica corretamente recusas e guardrails.
* Registrar os resultados e métricas para identificar possíveis pontos de melhoria no pipeline.