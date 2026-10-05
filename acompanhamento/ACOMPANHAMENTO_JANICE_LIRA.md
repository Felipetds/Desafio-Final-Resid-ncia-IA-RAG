

**Projeto:** Grande Desafio RAG — Cenário 1: Contratações Públicas do Estado do Rio de Janeiro

### Acompanhamento Individual — Janice Lira

---

## Encontro 1 — 14/09/2026

### Minha contribuição

* **Organização inicial do projeto:** Estruturei a organização da equipe no GitHub e participei da definição dos nomes e padrões iniciais do projeto.
* **Configuração do repositório:** Realizei o fork do repositório de referência do professor, configurei o repositório oficial do grupo e organizei as permissões de acesso e a inclusão dos integrantes.
* **Análise do cenário:** Estudei os requisitos do Cenário 1 — Contratações Públicas do Estado do Rio de Janeiro — para identificar as fontes de dados, as entregas previstas e as dependências iniciais.
* **Planejamento:** Organizei o fluxo inicial de atividades e contribuí para a distribuição das responsabilidades entre os integrantes.

### Uso de IA

* Utilizei um assistente de IA como apoio à interpretação dos requisitos do desafio e à organização inicial das atividades.
* Revisei e adaptei as sugestões antes de aplicá-las ao projeto.

### Resumo das atividades da equipe

* A equipe estabeleceu sua organização no GitHub.
* Configurou o repositório e os acessos dos integrantes.
* Iniciou a análise técnica do Cenário 1.

### Próximos passos

* Elaborar o `ARQUITETURA.md` e o `PERSONAS.md`.
* Criar o `corpus_manifest.yaml`.
* Consolidar a divisão de responsabilidades da equipe.

---

## Encontro 2 — 16/09/2026

### Minha contribuição

* **Coleta e curadoria de dados:** Dei continuidade à busca, seleção e extração de dados e documentos relacionados às contratações públicas do Estado do Rio de Janeiro.
* **Organização do repositório:** Acompanhei a estrutura do repositório e os ajustes necessários para apoiar as entregas da equipe.
* **Planejamento do corpus:** Mapeei as fontes e a organização dos dados coletados, considerando sua utilização posterior na ingestão, indexação e documentação do corpus.

### Uso de IA

* Utilizei um assistente de IA para apoiar a organização dos procedimentos de coleta e a análise das estruturas de dados.
* Revisei as orientações antes de aplicá-las.

### Resumo das atividades da equipe

* A equipe avançou na coleta e na estruturação inicial dos dados do Cenário 1.
* Discutiu a documentação técnica necessária para as próximas etapas.

### Próximos passos

* Dar continuidade à coleta e à revisão dos dados.
* Avançar na elaboração do `corpus_manifest.yaml`.
* Iniciar os documentos `ARQUITETURA.md` e `PERSONAS.md`.

---

## Encontro 3 — 18/09/2026

### Minha contribuição

* **Revisão dos dados:** Iniciei a análise e a validação dos dados coletados, com atenção à consistência das informações e à preparação da base para as etapas seguintes do pipeline RAG.
* **Documentação técnica:** Atualizei o `ARQUITETURA.md` com a divisão de responsabilidades definida pela equipe.
* **README:** Elaborei uma primeira versão do `README.md`, contemplando objetivo do projeto, arquitetura, instalação, execução da interface, política de sensibilidade e estado de desenvolvimento.
* **Apoio à integração:** Acompanhei questões relacionadas à interface, à observabilidade e à conexão entre os módulos, conforme sua disponibilidade no repositório.

### Uso de IA

* Utilizei ferramentas de IA como apoio à documentação técnica, à estruturação inicial da interface e do módulo de observabilidade.
* Também utilizei IA para auxiliar no diagnóstico de dificuldades de autenticação e sincronização entre Google Colab e GitHub.
* Revisei e ajustei o material antes de incorporá-lo ao trabalho.

### Resumo das atividades da equipe

* A equipe avançou nas frentes de ingestão, indexação, roteamento, recuperação, documentação e integração inicial.
* Discutiu a necessidade de padronizar os contratos de entrada e saída dos módulos para facilitar os testes e a integração com a geração de respostas.

### Dificuldades encontradas

* Necessidade de revisão detalhada dos dados coletados.
* Ausência de evidências disponíveis para algumas rotas, cujas bases ainda estavam em processamento ou indexação.
* Dependência do módulo de geração para concluir a integração da interface.
* Ajustes de autenticação e sincronização do repositório no Google Colab.

### Próximos passos

* Prosseguir com a revisão e a validação da base de dados.
* Integrar a interface aos módulos `generate.py` e `schema.py`, quando disponíveis.
* Conectar o `obs.py` aos estágios do pipeline.
* Validar o fluxo RAG com as quatro naturezas de base.
* Acompanhar os testes unitários, de contrato e de integração.

---

## Encontro 4 — 21/09/2026

### Minha contribuição

* **Verificação da API do PNCP:** Realizei, em 20/09/2026, uma consulta para pregões eletrônicos do Estado do Rio de Janeiro, no período de março de 2026. Após corrigir o parâmetro `tamanhoPagina` para o mínimo aceito pela API, a consulta retornou **HTTP 200** e informou **1.358 registros**.
* **Teste do tratamento de timeout:** Executei um teste controlado da função de consulta do `fetch_corpus.py`, simulando falhas de timeout sem acessar a API. O teste confirmou **três tentativas**, com intervalos de espera de **1 e 2 segundos**, seguidas do encerramento com a mensagem de erro prevista.
* **Validação básica do arquivo coletado:** Verifiquei o JSON da versão **v1**, que contém **1.358 registros**, todos com o campo `numeroControlePNCP` preenchido e **1.358 identificadores únicos**.
* **Preparação da passagem de etapa:** Organizei as evidências dos testes e identifiquei o JSON v1 para disponibilização ao integrante responsável pela próxima fase. A confirmação de recebimento e abertura do arquivo permanece pendente de registro.

### Uso de IA

* Utilizei um assistente de IA para apoiar a elaboração do teste de conectividade, a simulação de timeout e a validação básica do JSON.
* Executei os testes no Google Colab e conferi as saídas apresentadas.
* O teste de timeout foi **simulado**; não corresponde a uma indisponibilidade real observada na API.

### Resumo das atividades da equipe

* **Coleta de dados:** etapa em andamento.
* **Ingestão de dados:** etapa em andamento.
* **Indexação:** etapa em andamento.
* **Testes e fixtures (`tests/fixtures`):** início da preparação dos dados e cenários de teste.
* **`schema.py`:** início da implementação do módulo.
* **`generate.py`:** início da implementação do módulo de geração de respostas.

### Dificuldades e cuidados

* A primeira consulta retornou HTTP 400 porque o parâmetro `tamanhoPagina=1` era inferior ao mínimo aceito pela API; a correção para `10` permitiu realizar a consulta.
* Foi necessário distinguir a resposta real da API do teste simulado de timeout.
* O arquivo validado corresponde à **v1** e não deve ser identificado como v2.
* A validação do JSON cobriu estrutura, contagem e unicidade dos identificadores; não constituiu uma auditoria de todos os campos dos registros.
* O caminho `/content/...` é local ao Colab e não substitui o envio do arquivo ao integrante.

### Próximos passos

* Confirmar se o segundo integrante recebeu e conseguiu abrir o JSON v1.
* Dar continuidade à implementação de `schema.py` e `generate.py`.
* Avançar na preparação dos testes e fixtures.
* Preparar a integração dos novos módulos com as etapas de coleta, ingestão e indexação já concluídas.
* Registrar os encaminhamentos e as responsabilidades definidos pela equipe para o próximo encontro.

## Encontro 5 — 23/09/2026

### Minha contribuição

* **Validação do corpus v2:** Confirmei a integridade do corpus utilizado pela equipe, composto por 8 arquivos distribuídos em 5 bases e 4 naturezas: estruturada, normativa, conversacional e agregada.
* **Validação da base estruturada:** Confirmei a existência de 1.358 registros e 1.358 valores únicos de `numeroControlePNCP`, além da compatibilidade do período de publicação com o intervalo definido no manifesto.
* **Validação de integridade:** Mantive preservado o corpus v2 existente e seu SHA-256, sem reescrever os dados brutos congelados.
* **Teste de reconstrução online:** Executei uma nova tentativa isolada de coleta pela API do PNCP. A primeira página retornou HTTP 502 (Bad Gateway), mesmo após as três tentativas previstas pelo mecanismo de retry. Nenhum JSON final foi criado.
* **Verificação de checkpoint:** Confirmei que, após a falha da API, foi preservado apenas o arquivo de configuração em `_progresso_fetch`, contendo os parâmetros da coleta: período de 01/03/2026 a 31/03/2026, modalidade 6, UF RJ e 50 registros por página.
* **Determinismo da coleta:** Identifiquei que o JSON v2 existente não estava ordenado por `numeroControlePNCP`. Foi implementada no `fetch_corpus.py` uma ordenação explícita dos registros por esse identificador para tornar determinística a ordem das coletas futuras.
* **Teste da ordenação:** Validei a regra com entradas apresentadas em ordens diferentes, obtendo a mesma ordenação final. A alteração também passou pela verificação de sintaxe do Python.
* **Documentação:** Atualizei o `VALIDACAO_COLETA_JANICE.md` com as evidências da tentativa online, limitações encontradas e validação do determinismo.
* **Integração com a equipe:** Disponibilizei o `corpus_v2_para_equipe.zip`, contendo os 8 arquivos organizados em `raw/v2/`, ao integrante responsável pela etapa seguinte. O corpus já está sendo utilizado na continuidade do trabalho.

### Uso de IA

* Utilizei um assistente de IA como apoio na preparação e revisão dos procedimentos de validação, interpretação das saídas dos testes e documentação das evidências.
* Os comandos foram executados no Google Colab e seus resultados foram conferidos antes das alterações no repositório.
* As alterações foram testadas inicialmente em ambiente isolado antes de serem incorporadas ao código do projeto.

### Resultados

* Corpus v2 preservado e validado localmente.
* 8 arquivos das quatro naturezas disponíveis para integração.
* 1.358 registros estruturados e 1.358 identificadores únicos confirmados.
* Ordenação determinística adicionada ao fluxo de coleta para execuções futuras.
* Documentação de validação atualizada.
* Corpus v2 entregue para continuidade da integração pela equipe.

### Dificuldades e limitações

* A API do PNCP retornou HTTP 502 na primeira página da nova tentativa de coleta.
* Como nenhuma página de dados foi salva, ainda não foi possível comprovar uma retomada real utilizando `--retomar`.
* A reconstrução online completa dos 1.358 registros permanece não comprovada devido às falhas observadas na API do PNCP.
* Os testes das quatro naturezas com fontes locais verificam o corpus disponível, mas não comprovam o download automático de todas as fontes por outra pessoa.

### Próximos passos

* Acompanhar a utilização do corpus v2 na etapa de ingestão/integração.
* Realizar nova tentativa de reconstrução online quando a API do PNCP estiver disponível.
* Testar `--retomar` caso uma execução futura consiga salvar pelo menos uma página antes de uma interrupção.
* Preservar as versões congeladas do corpus e manter `data/raw/` fora do GitHub.

---
## Encontro 6 — 25/09/2026

### Minha contribuição

* **Auditoria final do corpus v3:** Revisei a consistência entre o `corpus_manifest.yaml`, o inventário `data/inventory/v3.json`, o `DIFF_v2_v3.md` e a documentação do corpus.
* **Correção do manifesto:** Atualizei o `corpus_manifest.yaml` para `version: v3` e corrigi as referências dos arquivos para os caminhos correspondentes à v3, preservando os hashes dos arquivos já validados.
* **Sincronização do inventário:** Atualizei o `manifest_hash` do `data/inventory/v3.json` para corresponder ao manifesto v3 auditado, mantendo inalterados os hashes individuais dos oito arquivos inventariados.
* **Atualização da documentação:** Atualizei o `CORPUS_INVENTORY.md` para representar a versão v3 e revisei o `README.md` para refletir o estado atual do corpus e distinguir funcionalidades implementadas de etapas ainda em integração ou validação.
* **Preservação das versões:** Mantive a v2 como snapshot congelado e preservei os arquivos brutos das versões existentes, sem sobrescrever o corpus anterior.

### Uso de IA

* Utilizei um assistente de IA como apoio na revisão da consistência entre manifesto, inventário e documentação.
* As alterações foram realizadas de forma incremental, conferindo os valores e hashes antes das atualizações.
* O uso de IA foi direcionado à revisão técnica e documental, mantendo os dados e evidências produzidos pelos procedimentos executados no projeto.

### Resultados

* `corpus_manifest.yaml` atualizado para a versão v3.
* `data/inventory/v3.json` sincronizado com o manifesto atualizado.
* Corpus v3 documentado com 8 arquivos e 0 falhas no inventário.
* Base estruturada mantida com 1.358 registros e 1.358 identificadores únicos.
* Comparação v2 → v3 mantida em 7 arquivos idênticos, 1 alterado, 0 adicionados e 0 removidos.
* `CORPUS_INVENTORY.md` atualizado para a v3.
* `README.md` revisado para refletir o estado atual do projeto.
* Snapshot v2 preservado.

### Dificuldades e cuidados

* Foi necessário corrigir referências remanescentes à v1 na documentação após a criação da v3.
* O `manifest_hash` do inventário precisou ser sincronizado após a alteração do `corpus_manifest.yaml`.
* A atualização foi limitada aos arquivos de documentação e metadados necessários, evitando alterações nos dados brutos congelados.
* Foi mantida a distinção entre funcionalidades implementadas e funcionalidades cuja integração ponta a ponta ainda necessita de validação.

### Próximos passos

* Disponibilizar o estado documentado da v3 para continuidade das etapas de ingestão e indexação.
* Apoiar a integração do corpus v3 ao pipeline RAG.
* Acompanhar os testes de recuperação, geração e integração das quatro naturezas de evidência.
* Preservar a rastreabilidade das versões do corpus durante as próximas etapas do projeto.

---
## Encontro 7 — 28/09/2026

### Minha contribuição

#### Coleta e validação da API do PNCP

- Dei continuidade às atividades relacionadas à coleta e ao versionamento do corpus do Cenário 1 — Contratações Públicas do Estado do Rio de Janeiro.
- Realizei uma nova tentativa de reconstrução online da base estruturada do PNCP em ambiente isolado, sem alterar os corpora v2 e v3.
- A coleta foi concluída com sucesso, com 28 páginas processadas e 1.358 registros.
- Confirmei que os checkpoints das páginas foram persistidos durante a execução.

#### Validação do mecanismo `--retomar`

- Preparei um teste controlado de interrupção da coleta utilizando checkpoints reais.
- Mantive apenas `configuracao.json` e os checkpoints das páginas 1, 2 e 3, sem o arquivo JSON final.
- Executei novamente a coleta utilizando a opção `--retomar`.
- O sistema recuperou corretamente as páginas 1, 2 e 3 dos checkpoints existentes e continuou a consulta ao PNCP a partir da página 4.
- A retomada chegou até a página 28 e produziu novamente 1.358 registros.
- A comparação entre a coleta normal e a coleta retomada apresentou a mesma quantidade de registros e igualdade do conteúdo JSON.
- Os arquivos finais apresentaram hashes SHA-256 binários diferentes, apesar de possuírem o mesmo conteúdo JSON e o mesmo tamanho. Essa diferença não foi utilizada para alterar o corpus v3.

#### Proteção contra sobrescrita

- Também validei a proteção contra sobrescrita do arquivo final.
- Ao tentar utilizar `--retomar` quando o JSON final já existia, a execução foi bloqueada com `FileExistsError`.
- Os testes foram realizados exclusivamente em diretórios isolados e não sobrescreveram os snapshots v2 ou v3.

#### Auditoria do corpus v3

- Realizei a auditoria de consistência entre `corpus_manifest.yaml`, `data/inventory/v3.json` e `data/inventory/DIFF_v2_v3.md`.
- Confirmei que o `scenario_id` está definido como `contratacoes-rj` e a versão como `v3` tanto no manifesto quanto no inventário.
- Confirmei a presença das mesmas cinco bases no manifesto e no inventário.
- O inventário v3 registra 8 arquivos, 18.797.136 bytes e 0 falhas.
- Os caminhos dos 8 arquivos declarados no manifesto foram encontrados corretamente no inventário.
- Os hashes SHA-256 declarados no `corpus_manifest.yaml` coincidem com os hashes registrados no `v3.json`.
- A comparação automática entre `v2.json` e `v3.json` confirmou o conteúdo do `DIFF_v2_v3.md`: 0 arquivos adicionados, 0 removidos, 1 alterado e 7 idênticos.
- O único arquivo alterado entre v2 e v3 corresponde à base estruturada do PNCP.

### Uso de IA

Utilizei IA como apoio para revisar os procedimentos de teste, organizar a validação do mecanismo de retomada, preparar os comandos executados no ambiente isolado e auxiliar na auditoria de consistência entre o manifesto, os inventários e o arquivo de diferenças entre as versões.

As execuções e os resultados foram conferidos antes de considerar as validações concluídas.

### Resultados

- Coleta online do PNCP concluída com 28/28 páginas.
- 1.358 registros obtidos.
- Checkpoints por página confirmados.
- Mecanismo `--retomar` validado em cenário controlado de interrupção.
- Recuperação das páginas 1 a 3 a partir dos checkpoints confirmada.
- Continuação da coleta da página 4 até a página 28 confirmada.
- Proteção contra sobrescrita validada.
- Corpora v2 e v3 preservados durante os testes.
- `corpus_manifest.yaml` e `v3.json` consistentes quanto a cenário, versão, bases, caminhos e hashes declarados.
- `DIFF_v2_v3.md` validado automaticamente: 0 adicionados, 0 removidos, 1 alterado e 7 idênticos.
- Auditoria lógica e documental da versão v3 concluída sem inconsistências entre os artefatos verificados.

### Dificuldades e limitações

- A disponibilidade da API do PNCP pode variar entre as execuções, exigindo que os testes sejam realizados de maneira controlada.
- Na comparação entre a coleta normal e a retomada, os dois arquivos apresentaram o mesmo conteúdo JSON e o mesmo tamanho, porém SHA-256 binários diferentes.
- A auditoria realizada confirmou a consistência dos hashes declarados entre o manifesto e o inventário. Não foi realizado o recálculo físico dos hashes dos oito arquivos brutos da v3 neste ambiente.

### Próximos passos

- Manter a v2 preservada como snapshot anterior e a v3 como versão atual documentada do corpus.
- Evitar novas alterações no corpus congelado sem necessidade de uma nova versão.
- Disponibilizar a saída da coleta para continuidade das etapas de ingestão e indexação, sob responsabilidade do integrante responsável por essa frente.
- Acompanhar a integração da coleta com as demais etapas do pipeline Adaptive RAG.

## Encontro 8 — 30/09/2026

### Minha contribuição

#### Validação da coleta do PNCP

- Realizei uma nova tentativa de validação da API do PNCP em ambiente isolado, utilizando o mesmo recorte definido para a base estruturada do corpus v3: Estado do Rio de Janeiro, modalidade Pregão Eletrônico (código 6), no período de 01/03/2026 a 31/03/2026.
- Utilizei um manifesto exclusivo para o teste, direcionando a saída para `data/raw/validacao_20260930/`, sem alterar o `corpus_manifest.yaml` original e sem sobrescrever os corpora v2 ou v3.
- A API respondeu normalmente nas páginas 1 a 8, e os respectivos checkpoints foram persistidos.
- Na página 9, a API retornou HTTP 429 (`Too Many Requests`).
- O mecanismo de retry realizou as novas tentativas previstas e encerrou a execução após a permanência do erro.
- Confirmei localmente a existência de 8 checkpoints, correspondentes às páginas 1 a 8.
- Nesta execução não foi possível reconfirmar as 28 páginas e os 1.358 registros devido ao limite de requisições da API. A validação completa anterior permanece registrada com 28 páginas e 1.358 registros.

#### Revisão das personas e preparação da avaliação

- Revisei o `PERSONAS.md` considerando o corpus atual v3.
- Identifiquei perguntas anteriores que utilizavam períodos ou informações não compatíveis com o corpus disponível e substituí essas consultas por perguntas sustentadas pelas evidências existentes.
- Mantive as três personas do projeto: Eduardo (Auditor Municipal), Renata (Advogada de uma Empresa Fornecedora) e Lucas (Gestor de Compras de um Hospital Público).
- Foram definidas nove perguntas de avaliação, sendo três para cada persona.
- As perguntas contemplam as naturezas estruturada, normativa, conversacional e agregada, além de cenários de privacidade, recusa e controle de escopo.
- Também foi mantido um cenário mais complexo para avaliação de recuperação cross-source e reconhecimento dos limites das evidências disponíveis.

#### Arquivo de avaliação

- Criei o arquivo `eval/perguntas_personas.json`.
- O arquivo contém nove perguntas identificadas de P01 a P09.
- Para cada pergunta foram registrados a persona, o tipo de consulta, a rota esperada, as bases esperadas, os filtros aplicáveis e o resultado esperado.
- Foram incluídos também casos em que o sistema deve recusar a solicitação ou reconhecer que o corpus não possui evidências suficientes para responder.
- O `PERSONAS.md` e o arquivo `eval/perguntas_personas.json` foram adicionados/atualizados no repositório.

### Uso de IA

- Utilizei um assistente de IA como apoio na preparação do teste isolado da API do PNCP, na interpretação do retorno HTTP 429 e na conferência dos checkpoints persistidos.
- Utilizei IA também como apoio à revisão das perguntas das personas e à estruturação do arquivo de avaliação em JSON.
- As perguntas foram elaboradas considerando as bases e evidências efetivamente documentadas no corpus v3.
- Os resultados dos comandos executados no Google Colab foram conferidos antes do registro das conclusões.

### Resultados

- Nova tentativa de validação da API executada em ambiente isolado.
- 8 páginas coletadas e 8 checkpoints persistidos antes da ocorrência do HTTP 429 na página 9.
- Mecanismo de retry acionado corretamente.
- Corpora v2 e v3 preservados sem sobrescrita.
- `PERSONAS.md` revisado e alinhado ao corpus v3.
- Nove perguntas de avaliação definidas para as três personas.
- `eval/perguntas_personas.json` criado com rotas, filtros, bases e resultados esperados.
- Casos de privacidade, recusa e controle de escopo incluídos na avaliação.
- Tarefa de revisão das personas e preparação das perguntas de avaliação concluída.

### Dificuldades e limitações

- A tentativa de coleta realizada em 30/09/2026 foi interrompida na página 9 devido ao retorno HTTP 429 (`Too Many Requests`) da API do PNCP.
- Por esse motivo, nesta execução específica não foi possível reconfirmar as 28 páginas e os 1.358 registros obtidos na validação completa anterior.
- Foi necessário revisar as perguntas das personas para evitar consultas que dependessem de informações não sustentadas pelo corpus atual.
- A criação das perguntas de avaliação foi limitada às evidências disponíveis no corpus v3, evitando definir resultados esperados sem suporte nas bases existentes.

### Próximos passos

- Disponibilizar as nove perguntas de avaliação para utilização nos testes do pipeline RAG.
- Acompanhar a execução das perguntas P01 a P09 nos módulos de roteamento, recuperação, geração e guardrails.
- Comparar as respostas produzidas pelo sistema com as rotas, bases, filtros e resultados esperados registrados em `eval/perguntas_personas.json`.
- Preservar o corpus v3 como referência atual e evitar alterações nos dados brutos congelados.
- Realizar novas consultas à API somente quando necessárias, respeitando as limitações de requisição observadas.

---
## Encontro 9 — 02/10/2026

### Minha contribuição

#### Auditoria e preparação do corpus v3

- Dei continuidade à frente de Corpus e Avaliação, verificando a integridade do corpus processado, composto por **38.619 chunks**, distribuídos nas quatro naturezas: estruturada, normativa, conversacional e agregada.
- Confirmei a unicidade dos identificadores dos chunks, sem duplicidades.
- Revisei os resultados das perguntas de avaliação das personas, considerando as rotas previstas, os filtros, a rastreabilidade documental e os limites das evidências disponíveis.
- Organizei e preservei os artefatos de auditoria no Google Drive, realizando a conferência de integridade por SHA-256.

#### Diagnóstico e geração incremental de embeddings

- Analisei os módulos `src/index.py` e `src/retrieve.py` para compreender a estrutura atual da indexação e da recuperação.
- Identifiquei um cache inicial com **60 embeddings**, utilizando vetores de dimensão 1.024.
- Executei a geração incremental de novos embeddings por lotes, ampliando o cache experimental para **140 vetores**.
- Mantive o cache original preservado e criei um cache de trabalho separado, com checkpoints no Google Drive.
- Distribuí a amostra experimental em 110 chunks estruturados, 10 normativos, 10 conversacionais e 10 agregados.

#### Construção e validação do índice híbrido experimental

- Construí um índice experimental isolado, utilizando FAISS e BM25, sem sobrescrever os índices de produção.
- Gerei os artefatos `faiss_index.bin`, `bm25_index.pkl`, `chunk_ids.json`, `chunks_experimental_v3.json` e `manifesto_experimental.json`.
- Validei a correspondência posicional entre os 140 chunks, seus identificadores, os 140 documentos BM25 e os 140 vetores FAISS.
- Testei o carregamento dos artefatos por meio da função original `carregar_artefatos()` do módulo `src/retrieve.py`.

#### Testes de recuperação híbrida e multirrota

- Executei uma consulta normativa sobre pregão eletrônico e Lei nº 14.133/2021, utilizando busca densa, BM25, filtragem por natureza e fusão RRF.
- Confirmei que, após a filtragem normativa, os resultados foram limitados aos dez chunks normativos disponíveis na amostra experimental.
- Realizei um teste multirrota com as quatro naturezas documentais.
- A seleção final apresentou oito evidências: cinco estruturadas, uma normativa, uma conversacional e uma agregada.
- Registrei os resultados e as limitações no arquivo `eval/RELATORIO_TECNICO_INDICE_EXPERIMENTAL_2026-10-02.md`.

### Uso de IA

- Utilizei um assistente de IA como apoio à análise dos módulos de indexação e recuperação, à preparação dos testes incrementais e à organização dos procedimentos de validação.
- Executei os códigos no Google Colab, conferindo os resultados de cada etapa antes de prosseguir.
- Utilizei IA também como apoio à elaboração do relatório técnico e à consolidação das evidências, preservando a distinção entre funcionalidades testadas e etapas ainda pendentes.

### Resultados

- Corpus processado com 38.619 chunks e identificadores únicos confirmados.
- Cache experimental ampliado de 60 para 140 embeddings.
- Índice híbrido experimental FAISS + BM25 construído e validado.
- Correspondência entre chunks, IDs, BM25 e FAISS confirmada.
- Carregamento dos artefatos pelo módulo original `retrieve.py` aprovado.
- Busca híbrida com filtragem normativa e fusão RRF executada com sucesso.
- Recuperação multirrota validada na amostra experimental, contemplando as quatro naturezas documentais.
- Relatório técnico produzido e copiado para o Google Drive.
- Acompanhamento diário preservado com verificação de integridade SHA-256.

### Dificuldades e limitações

- O índice experimental contempla apenas 140 dos 38.619 chunks disponíveis; portanto, ainda não representa a indexação integral do corpus v3.
- Permanecem 38.479 embeddings pendentes de geração.
- A cobertura normativa parcial limita a avaliação da relevância das respostas para consultas específicas sobre a Lei nº 14.133/2021.
- A seleção multirrota comprovou a presença das quatro naturezas, mas não demonstrou, isoladamente, uma relação factual entre todos os documentos recuperados.
- Os testes realizados não constituem validação ponta a ponta da geração de respostas, das regras de recusa e dos guardrails.
- O trabalho foi executado sobre uma cópia extraída do repositório, sendo necessária a sincronização posterior dos entregáveis com o GitHub oficial.

### Próximos passos

- Dar continuidade à geração incremental de embeddings, mantendo checkpoints e cópias de segurança.
- Ampliar a cobertura das quatro naturezas documentais no índice.
- Avaliar a relevância e a rastreabilidade das evidências recuperadas.
- Integrar os testes de recuperação à suíte de avaliação das personas.
- Validar os cenários cross-source, as recusas e os guardrails, respeitando os limites do corpus.
- Sincronizar os relatórios e os artefatos selecionados com o repositório oficial do grupo, preservando o trabalho dos demais integrantes.
--- 
## Encontro 10 — 05/10/2026

### Minha contribuição

#### Consolidação dos casos de avaliação das personas

- Dei continuidade à frente de Corpus e Avaliação, revisando os nove casos P01–P09 definidos para as personas Eduardo (Auditor), Renata (Advogada) e Lucas (Gestor Hospitalar).
- Para cada caso, consolidei o objetivo da pergunta, o tipo de resposta esperada, os filtros aplicáveis, os campos necessários, as fontes do corpus e a resposta esperada verificável.
- Registrei a cobertura da base estruturada do PNCP utilizada na avaliação: Estado do Rio de Janeiro, modalidade Pregão Eletrônico (código 6), período de 01/03/2026 a 31/03/2026 e 1.358 registros.
- Defini o critério para classificação de contratações relacionadas à Tecnologia/TIC, priorizando evidências presentes no objeto, descrição do item, serviço e especificação, evitando classificar automaticamente casos apenas pela presença de termos genéricos como “digital”, “eletrônico”, “sistema” ou “tecnologia”.
- Consolidei essas informações no arquivo `eval/CASOS_AVALIACAO_PERSONAS_V3.json`.

#### Preparação do ambiente experimental

- Utilizei uma cópia do repositório em ambiente isolado no Google Colab para evitar alterações indevidas no repositório oficial durante os testes.
- Preparei um subconjunto experimental com 47 chunks diretamente relacionados aos casos de avaliação que dependem de recuperação documental.
- O subconjunto contém 19 chunks agregados, 23 conversacionais, 2 estruturados e 3 normativos.
- Foram gerados 47 embeddings com dimensão 1.024 e construídos os índices FAISS e BM25 correspondentes.
- Validei a integridade entre os 47 chunks, 47 identificadores, 47 embeddings e 47 vetores registrados no índice FAISS.

#### Validação dos casos P03 e P08

- Executei o caso P03, referente à ata 00191/2026 da EBSERH, e o caso P08, referente à ata 00137/2026 do INCA.
- Identifiquei que os chunks conversacionais das duas atas eram aceitos pela rota esperada, porém eram eliminados pela aplicação do filtro temporal `ano=2026`.
- No P03, os 12 chunks da ata 00191 atendiam à rota, mas nenhum atendia ao filtro.
- No P08, os 10 chunks da ata 00137 atendiam à rota, mas nenhum atendia ao filtro.
- O diagnóstico mostrou que esses chunks possuem o metadado `ano=''`. A string vazia era considerada presente e sua conversão para inteiro falhava, fazendo com que o chunk fosse rejeitado.
- Realizei uma simulação exclusivamente em memória, tratando `ano=''` como metadado ausente, sem modificar os arquivos ou índices originais.
- Após a normalização simulada, o P03 passou de 0/12 para 12/12 chunks elegíveis e o P08 passou de 0/10 para 10/10.

#### Teste do retrieval após a correção simulada

- Executei novamente o retrieval utilizando a correção temporária apenas em memória.
- No P08, o sistema passou a recuperar cinco evidências da ata 00137/2026. Entre as evidências recuperadas estavam informações sobre o item A50372, rodízio com freio, fabricante TENTE, quantidade de 1.028 unidades, valor unitário de R$ 311,00 e valor total de R$ 319.708,00.
- No P03, o sistema recuperou corretamente o `contratacoes_publicacao.json_chunk_400`, relacionado à EBSERH e ao controle PNCP esperado.
- Entretanto, no P03 também foram recuperados chunks pertencentes à ata 00137/2026, evidenciando uma limitação adicional de precisão documental no ranking.
- A partir desse resultado, registrei como recomendação o uso de identificadores como número da ata, processo, número da compra, órgão/entidade e identificador PNCP como filtros ou sinais adicionais de reranqueamento.

#### Documentação e publicação

- Produzi o arquivo `eval/RELATORIO_FINAL_AVALIACAO_PERSONAS_JANICE.md`, consolidando os casos P01–P09, os resultados esperados, a cobertura do corpus, o critério Tecnologia/TIC, os testes realizados, as falhas identificadas e as recomendações técnicas.
- Mantive os arquivos originais preservados durante os testes.
- Publiquei `CASOS_AVALIACAO_PERSONAS_V3.json` no repositório oficial.
- Publiquei `RELATORIO_FINAL_AVALIACAO_PERSONAS_JANICE.md` na pasta `eval/` da branch `main`.
- O relatório final foi registrado no commit `543d18d`, com a mensagem `docs: adiciona relatório final`.
- Compartilhei com a equipe os dois arquivos principais da entrega e os pontos técnicos que precisam ser considerados na continuidade da integração.

### Uso de IA

- Utilizei um assistente de IA como apoio à organização e revisão dos casos P01–P09, à análise dos módulos de recuperação, à preparação dos testes controlados e à interpretação das saídas obtidas.
- Utilizei IA para apoiar o diagnóstico do comportamento do filtro temporal e a preparação da simulação em memória.
- Os comandos foram executados no Google Colab e os resultados foram conferidos antes do registro das conclusões.
- A correção de `ano=''` foi apenas simulada em memória; não foi aplicada ao código oficial do pipeline.
- Utilizei IA também como apoio à consolidação do relatório técnico final e à preparação da comunicação dos resultados para a equipe.

### Resultados

- Nove casos de avaliação P01–P09 consolidados com objetivos, tipos de resposta, filtros, campos, fontes e respostas esperadas verificáveis.
- Critério de classificação Tecnologia/TIC definido e documentado.
- Cobertura temporal da base estruturada documentada.
- Subconjunto experimental de 47 chunks preparado e indexado.
- 47 embeddings de dimensão 1.024 gerados e validados.
- Índices FAISS e BM25 do subconjunto experimental construídos e validados.
- Falha sistemática relacionada ao metadado `ano=''` comprovada nos casos P03 e P08.
- Simulação de normalização validada: P03 passou de 0/12 para 12/12 e P08 de 0/10 para 10/10 chunks elegíveis.
- Retrieval do P08 recuperado após a simulação.
- Evidência estruturada correta do P03 recuperada, porém com mistura de chunks de outra ata.
- Necessidade de melhoria da precisão documental registrada.
- `CASOS_AVALIACAO_PERSONAS_V3.json` publicado no repositório.
- `RELATORIO_FINAL_AVALIACAO_PERSONAS_JANICE.md` publicado no repositório.
- Entregável individual de Corpus e Personas concluído e comunicado à equipe.

### Dificuldades e limitações

- Os metadados dos documentos conversacionais apresentam o campo `ano` como string vazia em alguns casos, causando rejeição indevida quando o filtro temporal é aplicado.
- A correção desse comportamento foi validada apenas em memória e ainda precisa ser avaliada pela equipe antes de eventual alteração no código oficial.
- No P03, o retrieval recuperou a evidência estruturada correta, mas também retornou chunks pertencentes a outra ata, indicando necessidade de melhorar a precisão documental.
- O subconjunto de 47 chunks foi utilizado especificamente para os testes de avaliação e não representa a indexação integral dos 38.619 chunks do corpus v3.
- Os testes realizados tiveram como objetivo validar a recuperação e diagnosticar falhas; não representam, isoladamente, a validação completa de todo o pipeline em produção.

### Próximos passos

- Compartilhar com a equipe os resultados da avaliação e os dois arquivos produzidos.
- Avaliar em conjunto a correção do tratamento de metadados vazios no filtro temporal.
- Avaliar o uso de número da ata, processo, número da compra, órgão e identificador PNCP para melhorar a precisão da recuperação e do reranqueamento.
- Reexecutar P03 e P08 caso a equipe incorpore as correções ao pipeline oficial.
- Acompanhar a integração dos resultados da avaliação com as demais etapas do Adaptive RAG.
- Manter os casos P01–P09 como referência para os testes finais e para a preparação da apresentação do projeto.
