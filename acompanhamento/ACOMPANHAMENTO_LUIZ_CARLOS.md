# Acompanhamento — Luiz Carlos

## Encontro 1 — 14/09/2026

### Minha participação

- Acompanhei a preparação inicial do repositório e a organização dos acessos dos membros da equipe.
- Realizei a leitura e análise do Cenário 1, relacionado às Contratações Públicas do Estado do Rio de Janeiro.
- Contribuí para a definição das primeiras tarefas e para a organização do trabalho do grupo.
- Também revisei as orientações do Grande Desafio para entender melhor os documentos e artefatos que deverão ser produzidos ao longo do projeto.

### Apoio de IA

Utilizei ferramentas de IA como suporte para esclarecer alguns pontos das instruções do desafio e para organizar melhor as atividades iniciais. O conteúdo gerado foi revisado antes de ser considerado no desenvolvimento do projeto.

### Atividades realizadas pela equipe

Durante o encontro, a equipe organizou o acesso ao repositório, alinhou as primeiras etapas do trabalho e começou a estudar o Cenário 1 para definir como o projeto será desenvolvido.

### Próximas atividades

- Iniciar a elaboração do `ARQUITETURA.md`.
- Desenvolver o `PERSONAS.md`.
- Estruturar o arquivo `corpus_manifest.yaml`.
- Distribuir as responsabilidades entre os integrantes da equipe.

---

## Encontro 2 — 16/09/2026

### Minha participação

- Participei do alinhamento da equipe sobre a sequência de desenvolvimento do pipeline.
- Fiquei responsável pela implementação do roteamento das consultas e pela recuperação das evidências.
- Analisei como minha etapa dependeria dos resultados produzidos pelos módulos de ingestão e indexação.
- Organizei o planejamento inicial dos arquivos `router.py` e `retrieve.py`, considerando o contrato de entrada e saída necessário para as etapas seguintes.
- Verifiquei os requisitos de recuperação híbrida estabelecidos no desafio, incluindo busca densa, BM25, aplicação de filtros e fusão RRF.
- Combinei com a equipe que o roteamento poderia ser iniciado com exemplos e fixtures, enquanto a recuperação com dados reais dependeria da disponibilização dos índices persistidos.

### Apoio de IA

Utilizei ferramentas de IA para compreender melhor o funcionamento do Adaptive RAG, organizar a sequência de implementação e analisar como deveriam funcionar o roteamento, a recuperação densa, o BM25 e a fusão RRF. As sugestões foram revisadas e adaptadas às necessidades do projeto e à divisão de responsabilidades definida pela equipe.

### Atividades realizadas pela equipe

Durante o encontro, a equipe definiu a ordem de execução das próximas etapas. Janice ficou responsável pela coleta e organização das bases; Eridalgdo, pela ingestão e indexação; eu fiquei responsável pelo roteamento e pela recuperação; Felipe e Calvin, pela geração das respostas, guardrails, avaliação e testes; e Maria Eduarda, pela integração com a interface, coordenação e atualização da documentação. Também foram identificadas as dependências entre os módulos para evitar bloqueios durante o desenvolvimento.

### Próximas atividades

- Implementar o arquivo `router.py`.
- Definir a estrutura de saída do roteador.
- Implementar o arquivo `retrieve.py`.
- Integrar a busca densa com o índice FAISS.
- Integrar a busca esparsa com o índice BM25.
- Implementar a fusão dos rankings por RRF.
- Utilizar fixtures enquanto os índices reais não estiverem disponíveis.
- Disponibilizar uma saída estruturada para a etapa de geração das respostas.

---

## Encontro 3 — 18/09/2026

### Minha participação

- Implementei a primeira versão do arquivo `router.py`, responsável por analisar as consultas e decidir quais bases devem ser utilizadas.
- Estruturei o roteador para reconhecer as rotas `normativa`, `estruturada`, `conversacional` e `agregada`.
- Adicionei suporte a consultas que exigem mais de uma rota e à extração de filtros, como ano, unidade federativa, valor mínimo, valor máximo, modalidade, município e fornecedor.
- Incluí no roteador uma verificação para perguntas que exigem recusa, como solicitações para acusar diretamente um contrato de fraude.
- Implementei o arquivo `retrieve.py`, responsável por receber a consulta e recuperar os chunks e as evidências disponíveis.
- Integrei a recuperação densa com FAISS e a recuperação esparsa com BM25.
- Implementei filtros por rota, metadados e sensibilidade dos documentos.
- Implementei a fusão dos resultados utilizando Reciprocal Rank Fusion — RRF.
- Estruturei a saída da recuperação com a pergunta, as rotas selecionadas, os filtros identificados, as evidências, as fontes, os metadados e os scores de recuperação.
- Executei testes com doze perguntas envolvendo rotas simples, consultas cross-source, informações agregadas, atas, normas e recusa.
- Identifiquei dois comportamentos que precisavam de ajuste: uma pergunta de contagem que não acionava a base agregada e uma pergunta sobre atas que selecionava uma rota estruturada desnecessária.
- Ajustei o prompt do roteador e repeti os testes.
- Confirmei o funcionamento da recuperação com a fixture disponível, obtendo duas evidências nas consultas relacionadas à base estruturada.
- Organizei as dependências utilizadas pelos módulos no arquivo `requirements.txt`.

### Apoio de IA

Utilizei ferramentas de IA como apoio na estruturação inicial dos arquivos `router.py` e `retrieve.py`, na elaboração das perguntas de teste e na análise dos resultados obtidos. Durante os testes, revisei as rotas retornadas e identifiquei ajustes necessários no prompt. As sugestões geradas foram analisadas, modificadas e testadas antes de serem incorporadas ao projeto. Também acompanhei a execução dos códigos para compreender o funcionamento de cada etapa e verificar se a implementação estava de acordo com o planejamento da equipe.

### Atividades realizadas pela equipe

Durante o encontro, a equipe avançou nas etapas iniciais do pipeline. Os módulos de ingestão e indexação foram utilizados como base para a implementação do roteamento e da recuperação. A primeira versão dos módulos sob minha responsabilidade passou a fornecer uma saída estruturada que já pode ser utilizada por Felipe e Calvin no desenvolvimento do `generate.py`. A equipe também manteve registrada a dependência dos índices e do corpus real para a validação definitiva da recuperação.

### Resultados alcançados

- `router.py` implementado com suporte às quatro naturezas de base.
- Consultas simples e consultas com múltiplas rotas classificadas.
- Filtros estruturados extraídos da pergunta.
- Situação de recusa identificada corretamente.
- `retrieve.py` implementado.
- Recuperação densa com FAISS funcionando.
- Recuperação esparsa com BM25 funcionando.
- Aplicação de filtros e verificação de sensibilidade implementadas.
- Fusão RRF implementada.
- Evidências retornadas em formato estruturado.
- Doze perguntas utilizadas na validação do roteamento.
- Problemas encontrados durante os testes corrigidos.
- Etapa de geração das respostas liberada para Felipe e Calvin.

### Dificuldades e bloqueios

A recuperação ainda foi testada com uma fixture pequena, contendo somente documentos da base estruturada. Por isso, perguntas normativas, conversacionais e agregadas puderam ter o roteamento validado, mas ainda não retornaram evidências específicas dessas bases. A validação completa permanece dependente da disponibilização do corpus real e dos índices definitivos produzidos nas etapas anteriores.

### Próximas atividades

- Confirmar a instalação do projeto pelo arquivo `requirements.txt`.
- Integrar o recuperador aos índices definitivos quando forem disponibilizados.
- Validar a recuperação com documentos das quatro bases.
- Criar testes unitários e de contrato para `router.py` e `retrieve.py`.
- Integrar os módulos ao sistema de logging estruturado em JSONL.
- Comparar os resultados da busca densa e do BM25 com o ranking produzido pelo RRF.
- Apoiar Felipe e Calvin na integração da saída do recuperador com o `generate.py`.
- Documentar o contrato de entrada e saída dos módulos no repositório.

---

## Encontro 4 — 21/09/2026

### Minha participação

- Participei da validação dos módulos `router.py` e `retrieve.py` com os chunks gerados pelo `ingest.py`.
- Verifiquei o funcionamento do roteamento por meio de consultas normais e de uma consulta que exigia recusa por envolver acusação de fraude.
- Durante o teste de integração, identifiquei uma incompatibilidade entre o formato atual dos chunks e o módulo de recuperação.
- O `ingest.py` passou a armazenar o `chunk_id` dentro de `metadata`, enquanto o `retrieve.py` ainda priorizava a leitura desse identificador no nível principal do chunk.
- Atualizei o `retrieve.py` para buscar primeiro o `chunk_id` em `metadata`, mantendo compatibilidade com o formato anterior.
- A correção foi enviada ao repositório para permitir que os testes de integração realizados por Felipe continuem.

### Dificuldades encontradas

A principal dificuldade foi a incompatibilidade entre os contratos dos módulos após a correção dos metadados da ingestão. O teste de recuperação apresentou um `KeyError` porque o `retrieve.py` esperava o `chunk_id` em uma posição diferente daquela produzida pelo `ingest.py`.

Também foi necessário diferenciar o teste de recusa do teste completo de recuperação. A consulta sobre fraude validou o roteamento e a regra de recusa, mas não executou a recuperação densa, o BM25 e a fusão RRF, pois o pipeline foi interrompido corretamente antes dessas etapas.

### Apoio de IA

Utilizei uma ferramenta de IA para auxiliar na interpretação do erro apresentado durante a integração e na revisão da compatibilidade entre `ingest.py`, `index.py` e `retrieve.py`. A sugestão foi revisada antes da aplicação, e a alteração foi limitada à leitura do `chunk_id`, preservando as demais funções já implementadas no módulo.

### Atividades realizadas pela equipe

A equipe avançou na integração entre ingestão, indexação, roteamento, recuperação, schemas e geração. Felipe desenvolveu testes de schema e corpus e iniciou os testes do módulo de geração. A correção do `retrieve.py` foi disponibilizada para que o teste de integração possa ser executado novamente.

### Próximas atividades

- Repetir o teste de recuperação após atualizar o repositório.
- Confirmar a recuperação de evidências em uma consulta que não seja de recusa.
- Verificar a execução da busca densa, do BM25 e da fusão RRF.
- Validar o resultado da recuperação com os schemas definidos.
- Corrigir outras incompatibilidades que apareçam durante o teste de integração.

---

## Encontro 5 — 23/09/2026

### Minha participação

- Validei o funcionamento dos módulos `router.py` e `retrieve.py` com os artefatos de ingestão e indexação disponíveis.
- Corrigi o tratamento dos filtros monetários, evitando que valores como “R$ 500 mil” fossem interpretados incorretamente.
- Ajustei o roteamento das consultas relacionadas ao Plano de Contratações Anual para a base agregada.
- Corrigi o comportamento das consultas que exigem recusa, garantindo que perguntas envolvendo acusações de fraude não prossigam para a recuperação.
- Ajustei o roteamento de contingência para evitar a seleção incorreta da base conversacional.
- Criei testes para validar o roteamento, os filtros, as recusas e a compatibilidade da recuperação.
- Organizei as alterações em uma branch própria e realizei a integração com a branch `main` por meio de Pull Request.

### Resultados obtidos

- Os 11 testes específicos dos ajustes de roteamento e recuperação foram executados com sucesso.
- Após a integração das alterações, a suíte completa apresentou 106 testes aprovados.
- A busca densa, o BM25 e a fusão RRF permaneceram funcionando após as correções.
- O Pull Request foi mesclado e encerrado com sucesso.

### Apoio de IA

Utilizei ferramentas de IA como apoio para analisar os resultados dos testes, identificar inconsistências no roteamento e auxiliar na elaboração das correções. As alterações foram revisadas e validadas com testes automatizados antes da integração à branch principal.

### Atividades realizadas pela equipe

A equipe acompanhou a validação dos módulos, corrigiu imports incompatíveis com a execução a partir da raiz do repositório e configurou o `pytest` para reconhecer arquivos `test_*.py` e `teste_*.py`. Após esses ajustes, todos os 106 testes disponíveis foram executados com sucesso.

### Dificuldades encontradas

Foram identificadas inconsistências na interpretação de valores monetários, no roteamento de consultas sobre o PCA e nos imports utilizados por alguns módulos e testes. Esses problemas foram corrigidos e validados.

A validação definitiva dos filtros estruturados ainda depende do preenchimento dos metadados específicos durante a ingestão, como ano, modalidade, órgão, município, valor e vigência.

### Próximas atividades

- Aguardar a atualização do `ingest.py` com o preenchimento correto dos metadados específicos.
- Regerar os chunks e os índices após a atualização da ingestão.
- Validar os filtros estruturados com os dados corrigidos.
- Executar uma nova verificação integrada de `router.py` e `retrieve.py` com os artefatos definitivos.

---

## Encontro 6 — 25/09/2026

### Minha participação

- Validei os módulos `router.py` e `retrieve.py` após a atualização do repositório.
- Executei os testes offline relacionados ao roteamento e à recuperação.
- Testei o roteamento de contingência para consultas estruturadas, normativas, conversacionais e agregadas.
- Validei a recusa de perguntas que envolvem acusação de fraude.
- Testei a extração de filtros monetários.
- Validei o funcionamento da fusão RRF.

### Resultados obtidos

- Os 65 testes offline de roteamento e recuperação foram aprovados.
- As quatro rotas foram identificadas corretamente.
- Os quatro casos de filtros monetários foram aprovados.
- A fusão RRF funcionou sem duplicações e priorizou o chunk presente nos dois métodos.
- A consulta envolvendo fraude foi recusada e não selecionou rotas.

### Dificuldades encontradas

Os artefatos `faiss_index.bin`, `bm25_index.pkl` e `chunk_ids.json` não estavam disponíveis no ambiente. Por esse motivo, a recuperação híbrida com os índices reais não foi executada.

A validação definitiva também depende da correção dos metadados da base agregada e da regeneração dos índices.

### Apoio de IA

Utilizei uma ferramenta de IA para organizar os casos de teste, interpretar os resultados e diferenciar as validações offline das etapas que dependem dos artefatos de indexação.

### Próximas atividades

- Validar a recuperação Dense e BM25 com os índices regenerados.
- Testar consultas relacionadas ao Plano de Contratações Anual.
- Validar os filtros da base agregada.
- Executar a recuperação com as quatro bases definitivas.

---

## Encontro 7 — 28/09/2026

### Minha participação

- Atualizei a branch principal e criei branches específicas para as correções de roteamento e recuperação.
- Reproduzi a consulta conversacional que anteriormente não retornava evidências.
- Confirmei que a consulta era encaminhada corretamente para a rota `conversacional`, mas recebia indevidamente o filtro `uf: RJ`, mesmo sem mencionar localização.
- Corrigi o roteador para aplicar a UF somente quando a pergunta mencionar explicitamente `RJ` ou `Rio de Janeiro`.
- Corrigi também o roteamento de contingência, que anteriormente adicionava `uf: RJ` automaticamente.
- Criei testes automatizados para validar a remoção de UF inventada e o reconhecimento das formas explícitas da localização.
- Testei consultas estruturadas com e sem indicação de UF para confirmar a preservação dos filtros corretos.
- Após a correção do filtro geográfico, investiguei por que a consulta conversacional ainda retornava zero evidências.
- Confirmei que os 31 chunks conversacionais estavam presentes nos chunks e nos índices.
- Identifiquei que os candidatos eram eliminados pela política de sensibilidade, pois os documentos conversacionais estavam classificados como `restrito`.
- Ajustei a recuperação para permitir conteúdos restritos somente quando pertencem à base conversacional.
- Mantive bloqueados os conteúdos restritos das demais naturezas.
- Implementei a sanitização dos textos conversacionais antes de sua exposição como evidência.
- Criei testes para validar a ocultação de e-mail, telefone e CPF.
- Restaurei o corpus v2, regenerei os 2.125 chunks e carreguei os índices definitivos salvos no Google Drive.
- Validei a correspondência entre chunks, vetores FAISS, documentos BM25 e IDs persistidos.
- Executei uma consulta conversacional completa com busca densa, BM25 e fusão RRF.

### Resultados obtidos

- A consulta conversacional sem localização passou a retornar `uf: null`.
- Consultas que mencionam `RJ` ou `Rio de Janeiro` continuam retornando `uf: RJ`.
- A consulta estruturada com ano e sem localização preservou `ano: 2026` e retornou `uf: null`.
- Os quatro testes do filtro de UF foram aprovados.
- A suíte offline apresentou 118 testes aprovados após a inclusão dos testes de sanitização.
- Os 2.125 chunks, vetores FAISS, documentos BM25 e IDs persistidos apresentaram quantidades consistentes.
- A consulta conversacional recuperou 31 candidatos na busca densa e 31 candidatos no BM25.
- A fusão RRF reuniu 31 candidatos e retornou três evidências.
- Todas as evidências retornadas pertenciam à natureza `conversacional`.
- As evidências foram identificadas como `restrito_sanitizado`.
- A validação confirmou que os padrões testados de e-mail e CPF não foram expostos nos textos retornados.

### Dificuldades encontradas

A primeira dificuldade foi identificar que o filtro geográfico não era validado da mesma forma que os demais filtros. Além disso, o roteamento de contingência utilizava `RJ` como valor fixo.

Depois da correção do roteamento, a consulta ainda não retornava evidências. A investigação mostrou que os chunks conversacionais estavam presentes nos índices, mas eram eliminados pela regra que permitia apenas conteúdos classificados como públicos.

Também foi necessário restaurar o corpus e os índices depois que os artefatos locais foram perdidos com a reinicialização do ambiente do Google Colab.

### Apoio de IA

Utilizei uma ferramenta de IA para apoiar a reprodução dos problemas, a inspeção da validação dos filtros, a identificação da etapa que eliminava os candidatos conversacionais e a elaboração dos testes automatizados. Todas as alterações foram verificadas por testes específicos, pela suíte offline e por uma consulta real utilizando os índices definitivos.

### Atividades realizadas pela equipe

A equipe corrigiu os metadados conversacionais, o preenchimento da UF, a proteção contra ingestão vazia e o roteamento de consultas sem localização explícita. Com os artefatos definitivos restaurados, também foi possível validar a recuperação conversacional e a sanitização das evidências restritas.

### Próximas atividades

- Integrar a correção da recuperação por meio de Pull Request.
- Executar novamente os testes de integração após o merge.
- Validar a consulta conversacional pela interface Gradio.
- Confirmar que a resposta final utiliza somente evidências sanitizadas.
- Revalidar as quatro rotas e a recusa após a integração.

---

## Encontro 8 — 30/09/2026

### Minha participação

- Atualizei a branch de trabalho a partir da versão mais recente da `main`.
- Validei o suporte já existente para consultas com múltiplas rotas nos módulos `router.py`, `retrieve.py` e `schema.py`.
- Testei uma consulta cross-source envolvendo uma dúvida normativa sobre a participação de MEI em pregão eletrônico e a busca por uma contratação relacionada a material de escritório.
- Identifiquei que o roteamento de contingência reconhecia somente a rota `estruturada`, deixando de identificar a intenção `normativa`.
- Corrigi os termos utilizados pelo fallback para reconhecer consultas relacionadas a MEI, requisitos e permissão para participação.
- Ajustei os termos estruturados para reconhecer as variações de contrato e contratação.
- Mantive o funcionamento das consultas que exigem somente uma rota.
- Implementei uma seleção multirrota após a fusão RRF.
- A seleção passou a garantir, quando disponíveis, evidências de cada rota solicitada.
- Mantive a ordem relativa produzida pelo RRF e o limite global definido por `top_k`.
- Implementei tratamento para situações em que uma das rotas não possui evidências.
- Adicionei três testes de fallback e cinco testes específicos da recuperação multirrota.
- Organizei as alterações em uma branch própria e enviei o commit técnico ao repositório.

### Resultados obtidos

- A consulta sobre participação de MEI passou a selecionar somente a rota `normativa`.
- A consulta sobre contratação passou a selecionar somente a rota `estruturada`.
- A consulta cross-source passou a selecionar simultaneamente as rotas `normativa` e `estruturada`.
- A recuperação passou a preservar evidências das duas rotas quando elas estão disponíveis.
- A seleção multirrota respeitou o limite global de resultados.
- A ausência de evidências em uma das rotas não interrompeu o pipeline.
- Os 5 testes específicos de múltiplas rotas foram aprovados.
- Os 73 testes relacionados ao roteamento e à recuperação foram aprovados.
- A suíte offline foi concluída com 130 testes aprovados e 7 testes dependentes do LLM desmarcados.
- A branch `feat/multiplas-rotas-luiz` foi enviada ao repositório para abertura do Pull Request.

### Dificuldades encontradas

O roteador principal já possuía suporte a múltiplas rotas, mas o roteamento de contingência baseado em palavras-chave não reconhecia a intenção normativa da consulta sobre MEI. Além disso, embora a recuperação aceitasse uma lista de rotas, a seleção final utilizava apenas as primeiras posições do ranking RRF, sem garantir a presença de evidências de todas as naturezas solicitadas.

Também foi necessário reinstalar as dependências do projeto no ambiente do Colab após a reinicialização do runtime.

### Apoio de IA

Utilizei uma ferramenta de IA para revisar o fluxo existente de roteamento e recuperação, identificar quais partes do suporte multirrota já estavam implementadas, organizar os novos casos de teste e analisar os resultados. As alterações sugeridas foram aplicadas de forma controlada, revisadas no `git diff` e validadas pela suíte automatizada antes do envio ao repositório.

### Próximas atividades

- Abrir e revisar o Pull Request da recuperação multirrota.
- Validar a consulta cross-source utilizando os chunks e índices definitivos.
- Confirmar a presença de pelo menos uma evidência normativa e uma estruturada no pipeline completo.
- Verificar se a etapa de geração apresenta separadamente a regra normativa e as contratações encontradas.
- Confirmar a exibição das fontes das duas bases na interface.
- Apoiar a equipe na validação da demonstração ponta a ponta.

---

## Encontro 9 — 05/10/2026

### Minha participação

- Revisei o feedback do professor sobre consultas estruturadas e adaptei o sistema para decidir não apenas qual base utilizar, mas também qual estratégia de consulta executar.
- Implementei consultas estruturadas sobre o conjunto completo de registros, permitindo contagem e listagem sem dependência do `top_k`.
- Mantive a recuperação híbrida para perguntas abertas e semânticas.
- Implementei filtros por ano, município, UF, modalidade, valores e período de publicação, além de paginação e seleção de campos.
- Ajustei o roteador para interpretar corretamente operações de contagem e listagem.
- Corrigi consultas do tipo “quais contratações...” para serem tratadas como listagem.
- Implementei a estratégia `combinada`, permitindo utilizar consulta estruturada e recuperação híbrida na mesma pergunta quando necessário.
- Refatorei o `router.py` e o `query_executor.py`, separando responsabilidades e reduzindo funções muito extensas sem alterar suas interfaces principais.
- O `query_executor.py` passou a separar a execução em consulta estruturada, recuperação híbrida e execução combinada.
- Mantive a reutilização da análise do roteador, evitando roteamento duplicado.
- Mantive os mecanismos de esclarecimento, recusa e observabilidade já implementados.
- Atualizei os testes de planejamento e execução para validar as novas estratégias.
- As alterações foram limitadas aos arquivos sob minha responsabilidade, evitando mudanças em módulos desenvolvidos por outros integrantes.

### Resultados obtidos

- Contagem e listagem passaram a considerar toda a base estruturada, independentemente do `top_k`.
- A base utilizada possui 1.358 registros com IDs únicos.
- A consulta por ano de compra 2026 retornou 1.234 registros.
- A consulta por município do Rio de Janeiro e ano 2026 retornou 665 registros.
- A consulta de valor estimado superior a R$ 500 mil retornou 560 registros.
- A paginação funcionou sem duplicação de registros.
- O sistema passou a trabalhar com três estratégias explícitas:
  - `consulta_estruturada`;
  - `recuperacao_hibrida`;
  - `combinada`.
- Os testes adicionados para o `query_executor.py` foram executados com sucesso.
- O Pull Request da consulta estruturada foi incorporado à `main`.

### Apoio de IA

Utilizei ferramentas de IA como apoio na análise do feedback do professor, refatoração do código e elaboração dos testes. As alterações foram revisadas e mantidas somente dentro do escopo da minha responsabilidade no projeto.

### Próximas atividades

- Validar a estratégia combinada no ambiente completo do projeto.
- Reexecutar a suíte completa após integração com a versão mais recente da `main`.
- Apoiar a integração do executor com a interface junto à integrante responsável.
- Acompanhar com os responsáveis pela recuperação a melhoria da relevância de perguntas abertas, como o caso de reparo de vidraça.