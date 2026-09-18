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

## Encontro 3 — 18/09/2026**

### Minha contribuição**

* Iniciei o desenvolvimento do schema.py para padronizar e validar os dados entre as etapas do RAG, definindo estruturas para roteamento, evidências, filtros, tokens e respostas, além de regras para recusas e consistência dos dados.

* Também iniciei o desenvolvimento do generate.py, responsável por gerar respostas fundamentadas nas evidências recuperadas, utilizando o Qwen3. Implementei tratamento de recusas, ausência de evidências, controle de tokens e latência, nível de confiança e guardrails para proteção de dados sensíveis.

* Por fim, iniciamos a pesquisa e estruturação da estratégia de testes unitários, de contrato e de integração, utilizando pytest. Também iniciei o planejamento de fixtures baseadas no corpus para permitir testes controlados, reproduzíveis e sem dependência de rede.

### Uso de IA

Utilizei IA para duvidas sobre o funcionamento do Regex e para aplicabilidade dele no guardrails e para o planejamento da etapa de testes.

### Resumo da equipe

Estamos finalizando a parte de gerar as perguntas e iremos iniciar os testes no próximo encontro. Tivemos dificuldades em consultar a API PNCP, ela retornava 502 Server Error: Bad Gateway. Iremos realizar mais testes para entender o motivo do erro.

### Próximos passos

Iremos iniciar o desenvolvimentos dos teste no próximo encontro.