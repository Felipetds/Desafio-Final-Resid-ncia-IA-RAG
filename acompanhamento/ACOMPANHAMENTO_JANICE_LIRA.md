

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

* **Coleta de dados:** etapa finalizada.
* **Ingestão de dados:** etapa finalizada.
* **Indexação:** etapa finalizada.
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


