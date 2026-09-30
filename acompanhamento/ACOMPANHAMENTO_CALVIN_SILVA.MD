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


## Encontro 7 — 29/09/2026

### Minha participação

* Dei continuidade à validação realizada no encontro anterior, partindo do resultado dos testes offline para analisar os requisitos necessários à execução da integração do pipeline.

* Analisei quais componentes e artefatos são necessários para que os testes de integração possam ser executados, considerando especialmente o corpus, os chunks, os índices e os modelos utilizados pelo projeto.

* Revisei a documentação existente para identificar as etapas que precisam ser executadas antes da integração, verificando a relação entre preparação do ambiente, disponibilidade dos artefatos e execução do pipeline.

* Verifiquei a organização dos diretórios e arquivos utilizados pelo projeto, buscando compreender quais elementos fazem parte do código versionado e quais precisam ser restaurados ou disponibilizados separadamente.

* Analisei a necessidade de validar o estado dos artefatos antes da execução da integração, evitando utilizar dados incompletos, desatualizados ou incompatíveis com as configurações esperadas pelo projeto.

* Relacionei os resultados obtidos nos testes offline com as próximas etapas de validação, identificando que o funcionamento isolado das partes do sistema não garante, por si só, o funcionamento completo do pipeline.

### Resultados obtidos

* Os testes offline permaneceram como referência para confirmar o funcionamento das partes desacopladas do sistema antes da execução da integração.

* Foi identificado que a próxima etapa depende da disponibilidade e compatibilidade dos artefatos utilizados pelo pipeline, principalmente corpus, chunks e índices.

* A documentação passou a ser analisada também como parte do processo de validação, sendo necessário verificar se as instruções apresentadas permitem reproduzir o ambiente e recuperar os recursos exigidos pela aplicação.

* Foi estabelecida uma sequência de preparação para a integração: verificar o ambiente, confirmar as dependências, validar os artefatos e somente então executar o pipeline integrado.

* A análise realizada neste encontro serviu de base para o início dos procedimentos de reprodutibilidade posteriormente acompanhados no Encontro 8.

### Dificuldades encontradas

* A execução da integração não depende apenas dos testes automatizados, pois requer recursos que não estão necessariamente disponíveis no ambiente local após uma nova configuração.

* Foi necessário diferenciar os componentes do projeto que podem ser validados diretamente por testes offline daqueles que dependem de artefatos externos ou previamente gerados.

* A documentação apresenta informações importantes para a execução, mas precisa ser confrontada com a estrutura real do projeto para identificar possíveis lacunas, caminhos desatualizados ou etapas que não estejam suficientemente detalhadas.

* A preparação para a integração mostrou que a reprodução do projeto envolve tanto código quanto configuração, dependências, variáveis de ambiente e artefatos de dados.

### Apoio de IA

Utilizei ferramentas de IA como apoio para interpretar a relação entre os testes offline realizados anteriormente e os requisitos necessários para a execução da integração. Também utilizei a IA para organizar as etapas de preparação, revisar a documentação e auxiliar na identificação dos componentes e artefatos que deveriam ser verificados antes da execução do pipeline.

### Atividades realizadas pela equipe

A equipe avançou na identificação dos requisitos necessários para passar da validação isolada dos componentes para a execução integrada do pipeline.

Também foi iniciada a organização das verificações necessárias para garantir que o ambiente, as dependências e os artefatos estejam preparados de acordo com o funcionamento esperado do projeto.

A partir dessa análise, foi definido que a próxima etapa deveria priorizar a reprodução controlada do ambiente e a validação dos artefatos, utilizando a documentação existente como referência principal.

### Próximas atividades

* Criar e validar um ambiente virtual limpo para verificar a reprodução das dependências do projeto.

* Instalar as dependências a partir do `requirements.txt` e verificar a disponibilidade dos principais pacotes utilizados pelo pipeline.

* Configurar as variáveis de ambiente a partir do `.env.example`, mantendo as credenciais separadas do repositório.

* Restaurar e validar os artefatos necessários à execução do pipeline, incluindo corpus, chunks e índices.

* Executar a documentação do projeto passo a passo, registrando possíveis inconsistências, comandos incorretos, dependências ausentes ou arquivos desatualizados.


## Encontro 8 — 30/09/2026

### Minha participação

* Realizei o acompanhamento das etapas iniciais de reprodutibilidade do projeto
* Analisei os procedimentos necessários para preparar o ambiente de execução, incluindo a criação de um ambiente virtual limpo e a instalação das dependências exclusivamente pelo `requirements.txt`.
* Verifiquei a importância da validação das dependências essenciais utilizadas pelo projeto, incluindo `faiss`, `gradio`, `pydantic`, `rank_bm25`, `openai` e `pypdf`.
* Analisei o procedimento de seguir inicialmente o `docs/GUIA_DO_PIPELINE.md` sem utilizar recursos externos, com o objetivo de identificar comandos incorretos ou ausentes, dependências não documentadas, variáveis de ambiente não explicadas e caminhos ou arquivos desatualizados.
* Acompanhei as orientações para configuração do `.env` a partir do `.env.example`, mantendo as credenciais fora do repositório e verificando se o arquivo `.env` permanece ignorado pelo Git.
* Analisei o procedimento de restauração dos artefatos necessários para a execução do projeto, considerando a estrutura esperada para o corpus, chunks e índices.
* Verifiquei as quantidades de referência dos artefatos utilizados no projeto, incluindo o corpus v2, os chunks e os índices necessários para a execução do pipeline.
* Analisei os procedimentos de preparação do repositório e criação de uma branch específica para as alterações relacionadas à reprodutibilidade.

### Apoio de IA

Utilizei ferramentas de IA como apoio para compreender e organizar as etapas de reprodutibilidade descritas na documentação do projeto, especialmente os procedimentos relacionados à preparação do ambiente, verificação das dependências, configuração das variáveis de ambiente e restauração dos artefatos. As informações foram analisadas considerando a estrutura e os procedimentos já definidos no projeto.

### Atividades realizadas pela equipe

A equipe avançou na organização dos procedimentos necessários para tornar o projeto reproduzível. Foram analisadas as etapas relacionadas à preparação do repositório, criação de um ambiente virtual limpo, instalação e verificação das dependências, análise da documentação existente, configuração segura das variáveis de ambiente e restauração dos artefatos necessários para a execução do pipeline.

Também foi considerada a necessidade de manter os procedimentos documentados no guia existente, evitando a criação de uma documentação paralela. O objetivo é identificar eventuais lacunas no processo e corrigir o próprio `docs/GUIA_DO_PIPELINE.md`, mantendo as instruções alinhadas ao funcionamento real do projeto.

### Dificuldades encontradas

* Foi necessário considerar que a reprodutibilidade depende não apenas do código, mas também da documentação das dependências, variáveis de ambiente, caminhos dos arquivos e artefatos necessários.
* A execução em um ambiente virtual criado do zero pode revelar dependências que não estejam devidamente registradas no `requirements.txt`.
* Alguns artefatos utilizados pelo pipeline não fazem parte do fluxo normal de versionamento do código, sendo necessário documentar corretamente sua restauração.
* A documentação precisa ser validada seguindo os comandos exatamente como estão descritos, para que eventuais lacunas ou instruções desatualizadas sejam identificadas antes de serem corrigidas.

### Próximas atividades

* Validar o corpus restaurado, verificando a quantidade de arquivos por natureza e comparando com a estrutura esperada.
* Executar a etapa de validação do corpus conforme o procedimento documentado, verificando especialmente as categorias `estruturada`, `normativa`, `conversacional` e `agregada`.
* Registrar eventuais divergências encontradas na quantidade ou nos arquivos do corpus antes de prosseguir para as etapas seguintes.
