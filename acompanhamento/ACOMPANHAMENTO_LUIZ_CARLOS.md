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

## Encontro 3 — 21/09/2026

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

