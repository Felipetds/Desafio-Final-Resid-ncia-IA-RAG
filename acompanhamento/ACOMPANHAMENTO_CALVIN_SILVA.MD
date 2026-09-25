# Acompanhamento — Calvin Silva

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

* Compreender como relizar os testes da aplicação.


---

## Encontro 2 — 16/09/2026

### Minha contribuição


* Participei da definição da divisão de responsabilidades entre os integrantes da equipe.
* Ajudei a definir os marcos necessários para que uma etapa disponibilize os recursos necessários para o avanço da etapa seguinte.
* Acompanhei o andamento inicial das atividades da equipe, incluindo o início da coleta dos dados.

### Uso de IA

Utilizei assistente de IA como apoio na organização e revisão do `ARQUITETURA.md`, na análise das dependências entre os módulos e na organização do planejamento das atividades. Revisei e ajustei o conteúdo antes de incorporá-lo ao projeto.

### Resumo da equipe

A equipe definiu a divisão de responsabilidades do projeto e iniciou a execução das atividades. A coleta dos dados já foi iniciada e foram discutidas as dependências entre as diferentes etapas do sistema para permitir que o desenvolvimento avance de forma organizada.

### Próximos passos

* Acompanhar o andamento das atividades e identificar possíveis bloqueios entre os módulos.
* Acompanhar a integração progressiva entre os módulos do sistema.

---

## Encontro 3 — 18/09/2026

### Minha contribuição


### Apoio de IA

Utilizei ferramentas de IA para aprender a estrutura da tarefa designada auxiliando no entendimento e geração de código que pudesse ser testado.

### Atividades realizadas pela equipe

Durante o encontro, a equipe avançou na ingestão, indexação, roteamento, recuperação, documentação e integração inicial do sistema. Também foram discutidas as dependências entre os módulos e a necessidade de compreender os contratos de entrada e saída para o desenvolvimento dos testes e da geração das respostas.

### Dificuldades encontradas

* Robustes do desafio proposto pelo projeto sem devida preparação prévia.

* Dependencia quase exclusiva de ferramenta de LLM para auxiliar na resolução de debito têcnico.


### Próximas atividades

* Acompanhar a implementação dos testes unitários, de contrato e de integração.


---

## Encontro 4 — 21/09/2026

### Minha contribuição


* Realizei reparos de configurações na máquina para começar os testes.

* Realizei testes unitários nos arquivos contidos na pasta src.

### Estudos e desenvolvimento em testes

* Estudei a estrutura e a finalidade dos **fixtures** utilizados nos testes automatizados, compreendendo sua função como dados controlados para execução dos testes de forma reproduzível.
* Analisei o conteúdo do `contratacoes_fixture.json`, identificando a estrutura dos chunks de contratação e seus respectivos metadados, como `source_file`, `doc_type`, `chunk_id`, `sensitivity`, `base_id`, órgão, município, ano e valores da contratação.
* Estudei a organização da pasta `tests/` e a separação entre **testes unitários, testes de contrato e testes de integração**.
* Analisei especificamente a proposta de testes definida para o projeto, compreendendo que os testes unitários devem verificar comportamentos isolados sem depender do LLM ou de rede.
* Desenvolvi a estrutura de um teste unitário utilizando o fixture de contratações como base, buscando verificar se os dados utilizados pelo módulo seguem o contrato esperado.
* Estudei a importância da validação dos metadados obrigatórios dos chunks, relacionando essa validação aos problemas de integração encontrados entre os módulos.
* Utilizei o `pytest` para compreender como os testes são estruturados e executados no projeto.
* Relacionei os testes com a arquitetura do projeto, entendendo como a validação dos contratos entre os módulos pode identificar problemas antes da integração completa do pipeline.

### Dificuldades encontradas


O estudo dos testes também evidenciou a importância de manter uma estrutura padronizada para os dados utilizados como fixture. O `contratacoes_fixture` apresenta registros estruturados com metadados necessários para que os módulos possam realizar validações e processamento de forma consistente.

### Apoio de IA

Utilizei IA como apoio ao estudo da estrutura de testes do projeto, especialmente para compreender o conceito de fixtures, a utilização do `pytest`, a diferença entre testes unitários, de contrato e de integração e a forma de utilizar os dados do `contratacoes_fixture` nos testes.

Também utilizei IA para auxiliar na elaboração e revisão da estrutura do teste unitário e para compreender a relação entre os metadados dos chunks e os contratos esperados pelos módulos. As sugestões foram analisadas e adaptadas ao contexto e à estrutura definida para o projeto.

### Atividades realizadas pela equipe

A equipe avançou na coleta, ingestão, indexação, roteamento, recuperação, schemas, geração e testes. Também foram corrigidas incompatibilidades entre os metadados dos chunks e o módulo de recuperação, permitindo a execução do pipeline integrado com dados simulados.

### Próximas atividades

* Continuar o desenvolvimento dos testes unitários e de contrato dos módulos.
* Ampliar os fixtures conforme novos casos de teste forem identificados.
* Validar os metadados obrigatórios dos chunks.
* Executar os testes automatizados com `pytest`.
* Acompanhar a integração dos testes com os demais módulos do pipeline.
* Repetir a integração com dados reais quando a API do PNCP estiver disponível.
* Ampliar a instrumentação para registrar individualmente os demais estágios do pipeline.
* Revisar a extração de filtros realizada pelo roteador.
* Validar a interface com as perguntas definidas pelas personas.


## Encontro 6 — 25/09/2026

### Minha participação

- Configurei o ambiente local para executar os testes no VS Code e Git Bash.
- Identifiquei que os comandos do pytest precisam ser executados na raiz.
- Executei o teste offline, desconsiderando temporariamente a integração.
- Verifiquei os testes de schema, geração, roteamento, recuperação,
  metadados e inventário do corpus.
- Revisei as orientações de execução presentes na documentação.
- Documentei a diferença entre testes offline e testes de integração.

### Resultados obtidos

- A integração foi mantida separada porque depende de chunks, índices e modelos.
- O pytest encontrou 109 testes offline.
- Resultado: 109 passed, 1 warning in 4.59s.

        configfile: pytest.ini
        plugins: anyio-4.15.1
        collected 109 items                                                                                                                                                               

        testes\test_corpus_inventory_janice.py ..                                                                                                                                   [  1%]
        testes\test_metadata.py .                                                                                                                                                   [  2%]
        testes\teste_ajustes_router_retrieve.py ...........                                                                                                                         [ 12%]
        testes\teste_corpus.py ............                                                                                                                                         [ 23%]
        testes\teste_generate.py ..................                                                                                                                                 [ 40%]
        testes\teste_obs.py .                                                                                                                                                       [ 41%]
        testes\teste_retrieve.py .............................                                                                                                                      [ 67%]
        testes\teste_router.py .........................                                                                                                                            [ 90%]
        testes\teste_schema.py ..........                                                                                                                                           [100%]


### Dificuldades encontradas

Inicialmente, os testes foram executados dentro da pasta `testes`, fazendo
com que caminhos e imports não fossem encontrados. O problema foi resolvido
ao executar os comandos na raiz e definir `PYTHONPATH=.`.

### Apoio de IA

Utilizei uma ferramenta de IA para interpretar o erro, organizar os comandos
e revisar a documentação. As orientações foram verificadas no ambiente local.

### Próximas atividades

- Executar a integração quando os artefatos atualizados estiverem disponíveis.
- Validar o pipeline com consultas normais e evidências reais.
- Registrar eventuais falhas encontradas na integração.
- Continuar revisando a documentação do projeto.

