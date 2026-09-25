

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

* **Validação da nova coleta do PNCP:** Acompanhei a validação da coleta online realizada pela equipe. Apesar de ocorrências de timeout e respostas HTTP 502/503 durante a execução, o mecanismo de retentativas permitiu concluir as 28 páginas da consulta e obter 1.358 registros.

* **Validação de integridade:** Confirmei que a nova coleta contém 1.358 registros, todos com `numeroControlePNCP` preenchido, 1.358 identificadores únicos e nenhuma duplicação.

* **Comparação entre snapshots:** Restaurei e validei o snapshot v2 pelo SHA-256 e realizei a comparação registro a registro entre a v2 e a nova coleta. Foram identificados 0 IDs adicionados, 0 removidos, 1.314 registros idênticos e 44 registros alterados.

* **Análise das alterações:** As diferenças foram identificadas principalmente nos campos `dataAtualizacaoGlobal`, `dataAtualizacao`, `valorTotalHomologado`, `emendaParlamentar` e `valorTotalEstimado`, além de alterações pontuais em campos relacionados a datas e situação da compra.

* **Preservação da v2:** Confirmei que o snapshot v2 permaneceu imutável, mantendo o SHA-256 `08e28c39c44be375afe98abb94deb0b6fffd359401753a1f9eb69af54d7832aa`.

* **Preparação e validação da v3:** Preparei as fontes da nova versão mantendo sete arquivos idênticos à v2 e substituindo somente o arquivo estruturado do PNCP pela nova coleta, cujo SHA-256 é `681a935887201bf87073c0bc80979a388929adcc45f9de86e332e2e23cab565e`.

* **Teste do mecanismo de versionamento:** Executei o fluxo de `update` inicialmente em ambiente isolado. O teste permitiu identificar que o mecanismo depende da presença das versões anteriores em `data/raw/` e valida os hashes das fontes contra o `corpus_manifest.yaml`.

* **Criação da v3:** Após preparar o ambiente e o manifesto de teste com o novo SHA, o comando `update` foi executado com código de saída 0 e criou a versão v3 com 8 arquivos e 0 falhas, preservando a v2.

* **Geração do inventário e diff:** O processo gerou `data/inventory/v3.json` e `data/inventory/DIFF_v2_v3.md`. O diff por SHA-256 registrou 7 arquivos idênticos, 1 alterado, 0 adicionados e 0 removidos.

* **Atualização do repositório:** Adicionei ao repositório o inventário da v3 e o diff v2 → v3. Também atualizei o SHA-256 da coleta estruturada no `corpus_manifest.yaml`. Os arquivos brutos continuam excluídos do GitHub por meio da regra `data/raw/` no `.gitignore`.

### Uso de IA

* Utilizei um assistente de IA como apoio na elaboração e execução dos procedimentos de validação, comparação de snapshots, análise dos hashes, diagnóstico do comportamento do `corpus_cli.py` e preparação do fluxo de versionamento.
* Os comandos foram executados no Google Colab e seus resultados foram conferidos antes das alterações no repositório.
* As alterações foram realizadas de forma incremental, preservando os snapshots anteriores e evitando a inclusão dos arquivos brutos no GitHub.

### Resultados

* Coleta online: 28 páginas concluídas.
* Registros coletados: 1.358.
* IDs únicos: 1.358.
* Duplicações: 0.
* Comparação v2 → nova coleta: 1.314 registros idênticos e 44 alterados.
* SHA-256 v2 preservado: `08e28c39c44be375afe98abb94deb0b6fffd359401753a1f9eb69af54d7832aa`.
* SHA-256 da nova coleta/v3: `681a935887201bf87073c0bc80979a388929adcc45f9de86e332e2e23cab565e`.
* Versionamento v3: 8 arquivos e 0 falhas.
* Diff v2 → v3: 7 idênticos, 1 alterado, 0 adicionados e 0 removidos.

### Dificuldades e cuidados

* A API do PNCP apresentou instabilidade durante a coleta, com timeout e respostas HTTP 502/503.
* O mecanismo de `update` exige a presença da versão anterior em `data/raw/` para determinar automaticamente a próxima versão.
* O `update` também valida os hashes das fontes contra o manifesto, exigindo a atualização controlada do SHA da nova coleta.
* A v2 não foi sobrescrita.
* Os arquivos de `data/raw/` não foram enviados ao GitHub.
* O manifesto ainda contém o metadado `version: v1` e referências `data/raw/v1/...`, que serão objeto de uma última auditoria antes do encerramento definitivo da frente de Coleta e Versionamento.

### Próximos passos

* Realizar a auditoria final do `corpus_manifest.yaml`, verificando o significado de `version: v1` e das referências `data/raw/v1/...`.
* Confirmar que `v3.json`, `DIFF_v2_v3.md` e o manifesto atualizado estão consistentes no repositório.
* Registrar o encerramento da frente de Coleta e Versionamento após essa conferência.
* Disponibilizar à equipe as informações necessárias para utilização do snapshot v3 nas próximas etapas de ingestão, indexação e avaliação.
