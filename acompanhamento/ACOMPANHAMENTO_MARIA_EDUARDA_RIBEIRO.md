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
