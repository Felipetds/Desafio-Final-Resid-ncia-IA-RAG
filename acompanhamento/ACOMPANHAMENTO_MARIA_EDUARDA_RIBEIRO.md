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


---

## Encontro 2 — 16/09/2026

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

---

## Encontro 4 — 21/09/2026

### Minha participação

- Acompanhei a integração dos módulos desenvolvidos pela equipe e auxiliei na identificação de incompatibilidades entre `ingest.py`, `retrieve.py` e `generate.py`.
- Integrei o `obs.py` ao fluxo principal para registrar as etapas de recuperação, geração e validação em logs JSONL.
- Atualizei o `pipeline_adapter.py` para conectar `retrieve.py`, `generate.py`, `schema.py` e a interface Gradio.
- Realizei um teste integrado com consulta normal, obtendo roteamento para a base estruturada, recuperação Dense + BM25, fusão RRF, duas evidências, resposta gerada pelo LLM, fontes, latência e contagem de tokens.
- Auxiliei Luiz na correção do `retrieve.py`, que ainda esperava o `chunk_id` fora de `metadata`.
- Orientei a equipe sobre dependências, testes, atualização dos acompanhamentos e continuidade das atividades.

### Dificuldades encontradas

Durante a integração, ocorreram incompatibilidades entre os contratos dos módulos, ausência dos índices locais no Colab e conflitos de rebase causados por alterações simultâneas no repositório. As correções foram realizadas preservando as versões mais recentes enviadas pela equipe.

O teste atual ainda utiliza fixtures, portanto existem limitações nos dados simulados, como diferenças entre o ano identificado na consulta e o ano presente no nome do arquivo.

### Apoio de IA

Utilizei IA para auxiliar na análise dos erros de integração, na revisão dos contratos entre os módulos e na estruturação do adaptador do pipeline. Revisei as sugestões antes da aplicação e adaptei o código ao formato já utilizado no projeto.

### Atividades realizadas pela equipe

A equipe avançou na coleta, ingestão, indexação, roteamento, recuperação, schemas, geração e testes. Também foram corrigidas incompatibilidades entre os metadados dos chunks e o módulo de recuperação, permitindo a execução do pipeline integrado com dados simulados.

### Próximas atividades

- Repetir a integração com dados reais quando a API do PNCP estiver disponível.
- Ampliar a instrumentação para registrar individualmente os demais estágios do pipeline.
- Revisar a extração de filtros realizada pelo roteador.
- Executar os testes automatizados e validar a interface com as perguntas das personas.

---

## Encontro 5 — 23/09/2026

### Minha participação

- Acompanhei o andamento das entregas da equipe e revisei as atividades concluídas, pendentes e dependentes de outros módulos.
- Auxiliei na validação das correções realizadas em `router.py` e `retrieve.py`, incluindo filtros monetários, roteamento de consultas sobre o PCA e regras de recusa.
- Acompanhei a integração das correções de roteamento e recuperação à branch `main` por meio de Pull Request.
- Validei os testes específicos de roteamento e recuperação e acompanhei a execução da suíte de testes offline do projeto.
- Analisei o teste de integração ponta a ponta desenvolvido por Felipe, verificando os cenários de recuperação, geração, fontes, `top_k`, guardrails e recusa.
- Identifiquei uma incompatibilidade de import no teste de integração e a ausência dos artefatos locais necessários para a execução completa após o reinício do ambiente do Colab.
- Testei a interface Gradio com uma consulta de recusa e confirmei a aplicação dos guardrails, a ausência de evidências e a exibição de confiança, latência, tokens, `query_id` e `run_id`.
- Melhorei o tratamento da interface quando os artefatos de ingestão e indexação não estão disponíveis, substituindo a mensagem técnica por uma orientação compreensível ao usuário.
- Validei os logs JSONL e confirmei a presença dos campos obrigatórios em todos os registros analisados.
- Identifiquei que uma mesma consulta utilizava dois valores diferentes de `run_id` e corrigi a propagação desse identificador entre o adaptador, a recuperação e o roteamento.
- Atualizei os mocks dos testes de recuperação para manter compatibilidade com o parâmetro opcional `run_id`.

### Resultados obtidos

- A interface executou corretamente uma consulta recusada pelos guardrails.
- A ausência dos índices passou a ser apresentada de forma amigável, sem interromper a interface.
- Os registros analisados apresentaram todos os campos obrigatórios definidos na arquitetura.
- As etapas `query_analysis`, `roteamento`, `fusao_rrf`, `geracao` e `validacao` passaram a utilizar o mesmo `run_id`.
- O teste de integração enviado por Felipe contém sete testes, incluindo mais de três cenários ponta a ponta.
- A execução completa das consultas que utilizam recuperação ficou pendente devido à ausência local dos chunks e índices após o reinício do Colab.

### Apoio de IA

Utilizei ferramentas de IA como apoio para revisar os resultados dos testes, interpretar falhas de integração, identificar a duplicidade do `run_id` e organizar as correções no adaptador e no módulo de recuperação. As sugestões foram conferidas por meio da execução da interface, da inspeção dos logs e dos testes disponíveis antes de serem consideradas no projeto.

### Atividades realizadas pela equipe

A equipe avançou na ingestão, indexação, roteamento, recuperação, geração e testes. Luiz concluiu os ajustes de roteamento e recuperação. Eridalgo validou a ingestão das quatro bases, a geração dos chunks e a persistência dos índices, mantendo como próxima etapa o aprimoramento dos metadados específicos. Felipe adicionou os testes de integração ponta a ponta. Também acompanhei as pendências e dependências necessárias para a continuação das atividades.

### Dificuldades encontradas

- Ausência dos chunks e índices locais após o reinício do ambiente do Google Colab.
- Incompatibilidade de import no teste de integração.
- Utilização de valores diferentes de `run_id` entre etapas pertencentes à mesma consulta.
- Necessidade de atualizar mocks após a alteração do contrato do recuperador.
- Dependência dos artefatos regenerados para validar consultas normais na interface e executar os testes ponta a ponta completos.
- Necessidade de acompanhar entregas da equipe que ainda não receberam retorno ou commit correspondente.

### Próximas atividades

- Validar novamente a suíte de testes offline após as correções.
- Repetir os testes ponta a ponta quando os chunks e índices estiverem disponíveis.
- Validar a interface com consultas normais, múltiplas bases, fontes e evidências.
- Conferir os logs completos das etapas de recuperação com os artefatos definitivos.
- Acompanhar a correção do teste de integração e o registro do marcador `llm`.
- Realizar a integração final após a atualização dos metadados e a regeneração dos índices.

---

## Encontro 6 — 25/09/2026

### Minha participação

- Acompanhei e validei as atualizações realizadas pela equipe nos módulos de coleta, ingestão, roteamento, recuperação e testes.
- Testei a coleta da base estruturada diretamente pela API do PNCP.
- Durante o teste, identifiquei instabilidade temporária na API, com timeout e respostas HTTP 502 e 503.
- Confirmei que o mecanismo de retentativas funcionou e permitiu concluir a coleta das 28 páginas.
- Validei a obtenção de 1.358 registros estruturados, com 1.358 IDs únicos e nenhum registro duplicado.
- Identifiquei que a coleta atual possui hash diferente do snapshot registrado no manifesto, apesar de manter a mesma quantidade de registros.
- Preservei a nova coleta no Google Drive para permitir a comparação com a versão anterior.
- Validei as correções realizadas nos separadores e metadados dos dois arquivos CSV da base agregada.
- Confirmei o preenchimento de UF, ano, órgão, valor e vigência nos 500 chunks utilizados como amostra do PCA.
- Confirmei o preenchimento dos metadados disponíveis nos itens homologados, incluindo ano, valor, fornecedor e data de homologação.
- Verifiquei que a ingestão gerou 2.102 chunks, todos com IDs preenchidos e únicos, sem textos vazios.
- Analisei o tamanho dos chunks da base conversacional e identifiquei que os três PDFs foram processados como chunks únicos excessivamente grandes.
- Validei o fluxo de recusa do pipeline com uma consulta envolvendo acusação de fraude.
- Confirmei que a consulta recusada não retornou evidências e apresentou resposta compatível com os guardrails.
- Verifiquei que as etapas `query_analysis`, `roteamento`, `fusao_rrf`, `geracao` e `validacao` utilizaram o mesmo `run_id`.
- Validei a mensagem amigável apresentada pela interface quando os artefatos de indexação não estão disponíveis.
- Executei 29 testes específicos de observabilidade, geração e schema, todos aprovados.
- Executei a suíte offline disponível, obtendo 109 testes aprovados.
- Confirmei que o commit responsável pela unificação do `run_id` e pelo tratamento da falha da interface está presente na branch remota `main`.

### Resultados obtidos

- A coleta automatizada conseguiu recuperar os 1.358 registros mesmo diante da instabilidade temporária da API.
- Os registros coletados apresentaram 1.358 IDs únicos e nenhuma duplicação.
- Os separadores e os principais metadados da base agregada foram corrigidos.
- A ingestão manteve 2.102 chunks válidos antes da revisão do fatiamento dos PDFs.
- O fluxo de recusa, os guardrails e a ausência de evidências em consultas recusadas funcionaram corretamente.
- Todas as etapas registradas para a consulta testada utilizaram um único `run_id`.
- A interface apresentou uma orientação compreensível quando os índices estavam ausentes.
- Os 29 testes específicos e os 109 testes offline foram aprovados.

### Dificuldades encontradas

- A API do PNCP apresentou timeout e respostas HTTP 502 e 503 durante as primeiras tentativas.
- O conteúdo coletado atualmente apresentou hash diferente do snapshot anterior, indicando alteração na fonte pública.
- Os três PDFs conversacionais foram transformados em chunks únicos com aproximadamente 23 mil, 32 mil e 49 mil caracteres.
- Os índices FAISS, BM25 e a lista de IDs ainda não estavam disponíveis no ambiente atual do Google Colab.
- A suíte de testes apresentou um aviso de configuração relacionado ao `testpaths`, embora todos os testes offline tenham sido aprovados.

### Apoio de IA

Utilizei ferramentas de IA como apoio para organizar os procedimentos de validação, interpretar os resultados da coleta, analisar os metadados gerados, identificar o tamanho inadequado dos chunks conversacionais e revisar os registros de observabilidade. Todos os resultados foram conferidos por meio da execução dos comandos, inspeção dos arquivos gerados e testes automatizados.

### Atividades realizadas pela equipe

A equipe avançou na coleta e validação do corpus, no preenchimento dos metadados específicos, nos testes de roteamento e recuperação e na preparação dos testes de integração. A correção da base agregada foi validada, mantendo como pendência a melhoria do fatiamento dos PDFs conversacionais. Também foram revisados os resultados da suíte offline e as dependências necessárias para a futura validação ponta a ponta.

### Próximas atividades

- Acompanhar a divisão dos três PDFs conversacionais em chunks menores, com sobreposição e preservação dos metadados.
- Regenerar os chunks após a correção do fatiamento.
- Reconstruir os índices FAISS e BM25 utilizando o cache de embeddings.
- Validar a consistência entre a quantidade de chunks, vetores, documentos BM25 e IDs persistidos.
- Executar os testes de integração com os artefatos definitivos.
- Validar consultas normais, agregadas, conversacionais, normativas e de recusa na interface.
- Preparar uma atualização objetiva do andamento do projeto para o próximo encontro com o professor.

---

## Encontro 7 — 28/09/2026

### Minha participação

- Atualizei a documentação geral do projeto e disponibilizei um arquivo de status para facilitar o acompanhamento das entregas e a apresentação do andamento ao professor.
- Acompanhei a correção do roteamento realizada por Luiz, verificando o comportamento do filtro de UF em perguntas com e sem localização explícita.
- Confirmei que perguntas sem localização passaram a retornar `uf: null`, enquanto consultas com `RJ` ou `Rio de Janeiro` mantiveram `uf: RJ`.
- Acompanhei a criação de testes específicos para o filtro geográfico e validei a execução de 114 testes offline.
- Validei as atualizações realizadas por Eridalgo na ingestão, incluindo a extração de ano, o preenchimento da UF conversacional e a proteção contra a geração de arquivos de chunks vazios.
- Restaurei o corpus bruto no ambiente do Google Colab e executei novamente a ingestão.
- Confirmei a geração de 2.125 chunks, com 2.125 IDs únicos e nenhum texto vazio.
- Verifiquei que os 519 chunks agregados não apresentaram anos em formato inválido.
- Testei o roteamento de consultas estruturadas, conversacionais, normativas, agregadas e de recusa, confirmando as rotas esperadas nos cinco casos.
- Restaurei os índices persistidos e executei a interface Gradio com consultas das quatro bases e uma consulta sensível.
- Confirmei o funcionamento das respostas estruturada, normativa e agregada e da recusa por guardrails.
- Investiguei a ausência de evidências na consulta conversacional e identifiquei o ponto exato em que os resultados eram eliminados.
- Confirmei que a busca densa e o BM25 localizam os 31 chunks conversacionais, mas a filtragem remove todos porque estão classificados com sensibilidade `restrito`.
- Registrei a necessidade de revisar a política de sensibilidade antes de liberar evidências conversacionais, evitando a exposição de nomes, telefones, e-mails ou outros dados pessoais.

### Resultados obtidos

- A documentação de status do projeto foi integrada à branch principal.
- O filtro geográfico deixou de ser aplicado quando a pergunta não menciona localização.
- As cinco consultas de validação foram encaminhadas para as rotas esperadas.
- A ingestão gerou 2.125 chunks válidos.
- Os 114 testes offline foram aprovados.
- A interface executou consultas estruturadas, normativas, agregadas e de recusa.
- A causa da ausência de evidências conversacionais foi identificada na regra de sensibilidade, e não no roteamento, nos índices ou nos métodos Dense e BM25.

### Dificuldades encontradas

- O ambiente do Colab voltou para uma versão anterior da branch `main` após o reinício da sessão, exigindo nova atualização do repositório.
- O corpus bruto e os índices precisaram ser restaurados do Google Drive.
- Algumas consultas apresentaram demora elevada devido ao servidor dos modelos.
- A base conversacional possui documentos marcados como restritos, e a regra atual bloqueia todos antes da fusão RRF.
- A liberação desses documentos exige mascaramento ou sanitização das evidências para evitar exposição de dados pessoais.

### Apoio de IA

Utilizei ferramentas de IA para organizar os procedimentos de validação, interpretar os resultados do roteamento, investigar a recuperação conversacional e localizar a etapa responsável pela eliminação das evidências. Todas as conclusões foram verificadas por meio da execução do código, inspeção dos metadados, análise das funções e testes automatizados.

### Atividades realizadas pela equipe

Luiz corrigiu o filtro de UF no roteador e adicionou testes automatizados. Eridalgo atualizou a ingestão para preencher metadados conversacionais e impedir a sobrescrita por uma saída vazia. A equipe também avançou na documentação, nos testes offline e na validação integrada da interface.

### Próximas atividades

- Revisar a política de sensibilidade da base conversacional.
- Implementar mascaramento de dados pessoais nos textos e evidências.
- Permitir a recuperação apenas de conteúdo conversacional sanitizado.
- Repetir a busca densa, o BM25 e a fusão RRF após a correção.
- Validar novamente a consulta conversacional na interface.
- Executar a suíte de integração após a estabilização das quatro rotas.
---

## Encontro 8 — 30/09/2026

### Minha participação

- Abri e validei novamente a interface integrada do projeto no Google Colab.
- Executei consultas estruturadas e normativas para conferir o funcionamento do pipeline ponta a ponta.
- Confirmei a apresentação da resposta, rota selecionada, filtros, fontes, evidências, `chunk_id`, latência, tokens, `query_id` e `run_id`.
- Utilizei como consulta principal de demonstração: “Quais contratações envolvem serviços de tecnologia?”.
- Mantive como consulta alternativa: “O que a Lei nº 14.133 estabelece sobre licitações?”.
- Implementei um formulário de avaliação com as opções “Útil” e “Não útil”.
- Adicionei um campo de comentário opcional e um botão específico para enviar o feedback.
- Implementei a persistência dos feedbacks em arquivo JSONL.
- Corrigi a extração de `query_id` e `run_id` apresentados no status da interface em formato Markdown.
- Corrigi o botão “Limpar” para apagar também a avaliação, o comentário e a confirmação de salvamento.
- Configurei a limpeza do feedback anterior sempre que uma nova consulta é iniciada.
- Adicionei um indicador de progresso para mostrar as etapas de preparação, recuperação, geração e validação.
- Reduzi a quantidade padrão de evidências de cinco para três.
- Configurei um limite seguro de candidatos analisados na recuperação, com `fetch_k` padrão igual a 50.
- Adicionei testes automatizados para validar a persistência do feedback.
- Configurei o `.gitignore` para impedir o versionamento dos arquivos JSONL produzidos durante o uso da interface.
- Organizei as alterações em uma branch própria e preparei um Pull Request para revisão antes da integração com a `main`.

### Resultados obtidos

- A interface executou consultas completas e apresentou respostas acompanhadas de fontes e evidências.
- O formulário de feedback passou a exigir a seleção de uma avaliação antes do envio.
- Os feedbacks foram registrados em `data/feedback/feedback.jsonl`.
- Os registros válidos apresentaram pergunta, avaliação, comentário, rota, fonte, `query_id` e `run_id`.
- O arquivo de feedback permaneceu disponível após o reinício da interface no mesmo ambiente.
- O botão “Limpar” removeu corretamente os dados da consulta e do formulário de feedback.
- O indicador de progresso tornou o processamento mais compreensível para o usuário.
- A consulta passou a utilizar três evidências por padrão e até 50 candidatos por mecanismo de busca.
- O tempo observado em uma das consultas ficou em aproximadamente 20 segundos, representando melhoria em relação às execuções anteriores de aproximadamente 60 segundos.
- O código foi validado com `py_compile`.
- A suíte offline foi concluída com **132 testes aprovados**.

### Dificuldades encontradas

- O feedback registrado antes da correção não apresentava `query_id` e `run_id`, pois a marcação Markdown impedia a extração correta desses campos.
- Foi necessário preservar o formato textual da rota para manter compatibilidade com os testes existentes.
- Algumas portas do Gradio permaneceram ocupadas por execuções anteriores da interface no Google Colab.
- O tempo de resposta continua sujeito à disponibilidade do endpoint compartilhado de geração e embeddings.
- A porcentagem de progresso indica etapas reais do pipeline, mas pode permanecer mais tempo na etapa de geração, que depende da resposta do modelo externo.
- Os arquivos de feedback armazenados localmente permanecem disponíveis após reiniciar a interface, mas podem ser perdidos se o runtime completo do Colab for apagado.

### Apoio de IA

Utilizei uma ferramenta de IA como apoio para revisar a estrutura da interface, organizar a persistência dos feedbacks, interpretar a falha do teste automatizado e planejar a apresentação do progresso do pipeline. Todas as alterações foram verificadas por inspeção dos registros JSONL, execução da interface, compilação dos arquivos e testes automatizados.

### Atividades realizadas pela equipe

A equipe continuou trabalhando na reprodutibilidade, ingestão, recuperação e preparação da demonstração ponta a ponta. Calvin iniciou a validação do projeto em ambiente limpo e identificou a necessidade de documentar a restauração local do corpus em `data/raw/v2`. As demais correções integradas anteriormente permitiram utilizar os chunks, índices e rotas na interface.

### Próximas atividades

- Aguardar a revisão do Pull Request da funcionalidade de feedback e progresso.
- Integrar a alteração à branch `main` somente após a conferência dos arquivos modificados.
- Atualizar `docs/STATUS_DO_PROJETO.md` em um commit separado.
- Conferir os Pull Requests e acompanhamentos dos integrantes.
- Validar a demonstração depois que as alterações de reprodutibilidade forem integradas.
- Preparar um plano alternativo com resultado previamente registrado caso o endpoint compartilhado apresente lentidão.
- Avaliar o armazenamento do histórico de feedback em local persistente para evitar perda após o encerramento do runtime do Colab.

---

## Encontro 9 — 02/10/2026

### Minha participação

- Atualizei o arquivo `docs/STATUS_DO_PROJETO.md` para organizar as informações utilizadas na apresentação do andamento do projeto.
- Preparei um roteiro de apresentação com explicação do corpus, arquitetura, verificações técnicas, demonstração da interface e limitações conhecidas.
- Organizei o notebook do Colab com seções identificadas para conferência dos artefatos, testes, consulta ao pipeline, logs e abertura da interface.
- Após a reinicialização do ambiente, reinstalei as dependências necessárias e restaurei o corpus e os índices disponíveis no Google Drive.
- Executei novamente a ingestão, concluída sem erro.
- Testei consultas na interface com diferentes quantidades de evidências.
- Validei uma consulta sobre contratações de tecnologia com três evidências, conferindo a correspondência entre a resposta e os registros recuperados.
- Identifiquei desvios na resposta de uma consulta de tecnologia com cinco evidências, incluindo afirmações sem apoio suficiente nos trechos apresentados.
- Testei consultas normativas e identifiquei uma resposta que tratou de outro artigo, apesar de o art. 4º estar presente nas evidências.
- Repeti a pergunta específica sobre o art. 4º com uma evidência e obtive uma resposta alinhada ao trecho, mantendo como ressalva a precisão da descrição dos limites.
- Testei consultas sobre o PCA e conferi os valores e unidades responsáveis dos registros recuperados.
- Identifiquei evidências irrelevantes nas consultas agregadas, embora a consulta específica sobre seguros tenha apresentado corretamente os dois registros pertinentes.
- Registrei os identificadores, latências, tokens e fontes exibidos nas consultas realizadas.
- Recebi e organizei o feedback do professor sobre a necessidade de adequar a estratégia de consulta à intenção do usuário.
- Preparei o planejamento de segunda-feira, com entregas individuais, dependências, critérios de validação e commits separados.

### Resultados obtidos

- O ambiente foi recuperado após a reinicialização do Colab e a ingestão voltou a executar com sucesso.
- A consulta estruturada sobre tecnologia apresentou três exemplos pertinentes com citações verificáveis.
- A consulta normativa específica com uma evidência apresentou uma resposta correspondente ao art. 4º recuperado.
- A consulta agregada sobre seguros apresentou corretamente os valores estimados de R$ 46.903,50 e R$ 2.160,24 e as respectivas unidades responsáveis.
- Foram identificadas limitações na relevância das evidências e na fidelidade das respostas, especialmente em consultas com múltiplos trechos.
- O feedback do professor foi convertido em um planejamento para consulta estruturada, revisão das personas e adaptação da interface.

### Dificuldades encontradas

- A reinicialização do Colab exigiu reinstalação de dependências e restauração dos arquivos necessários.
- O arquivo de chunks não estava disponível no Drive consultado, sendo necessário regenerá-lo a partir do corpus.
- Algumas respostas apresentaram desvios ou afirmações não sustentadas pelas evidências.
- A recuperação agregada incluiu registros que não correspondiam ao assunto solicitado.
- O fluxo atual baseado em `top_k` apresenta exemplos recuperados, mas não permite responder com segurança a contagens ou listagens completas da base.
- A latência variou entre as consultas, permanecendo necessária a análise do tempo por etapa.

### Feedback do professor

O professor orientou que o sistema considere o que o usuário realmente deseja obter, utilizando as personas para definir respostas úteis.

Para consultas estruturadas, o sistema deve aplicar filtros sobre os registros disponíveis e calcular resultados, como contagens, em vez de utilizar apenas os primeiros trechos recuperados. Pedidos mais específicos devem apresentar os registros e os campos solicitados pelo usuário.

Para perguntas abertas, a busca semântica ou híbrida continua pertinente. O roteador deverá identificar não apenas a base, mas também a estratégia, a operação, os filtros e os campos de saída.

As respostas deverão informar o recorte consultado, evitando apresentar os dados coletados em março de 2026 como cobertura de todo o ano.

### Apoio de IA

Utilizei uma ferramenta de IA para apoiar a organização do roteiro, dos procedimentos de recuperação do ambiente, da análise das respostas e do planejamento das próximas atividades. A avaliação dos resultados foi realizada comparando as respostas com os trechos e metadados apresentados pelo sistema.

### Atividades realizadas pela equipe

As próximas entregas foram reorganizadas a partir do feedback do professor. Foram definidas responsabilidades para revisão das personas e critérios de avaliação, preparação dos dados, roteamento por estratégia, consulta estruturada, testes, observabilidade, reprodutibilidade e adaptação da interface.

### Próximas atividades

- Revisar com a equipe os casos prioritários das personas.
- Definir os critérios de classificação de tecnologia e o significado dos filtros de ano e valor.
- Integrar um fluxo de contagem e listagem sobre os registros estruturados, sem limitação por `top_k`.
- Adaptar a interface para apresentar total, critérios, recorte e tabelas paginadas com os campos solicitados.
- Manter a busca híbrida para consultas abertas.
- Investigar os desvios de geração e a seleção de evidências irrelevantes.
- Alinhar a versão do corpus utilizada pelo pipeline com a documentação e os artefatos.
- Validar os novos fluxos com testes e resultados conhecidos.

---

## Encontro 10 — 05/10/2026

### Minha participação

- Adaptei a interface às orientações do professor, distinguindo contagens, listagens e consultas documentais.
- Integrei o adaptador ao executor de consultas implementado por Luiz.
- Implementei a apresentação de contagens com total calculado, filtros, recorte da base e fonte.
- Implementei tabelas com somente os campos solicitados e controles de paginação, mantendo o total visível durante a navegação.
- Mantive a quantidade de evidências restrita à recuperação documental, sem limitar contagens ou listagens.
- Integrei à minha branch as atualizações de Luiz e os novos casos de avaliação de Janice, preservando minha implementação.
- Adaptei a interface à estratégia combinada, separando o resultado estruturado calculado da resposta documental.
- Corrigi a apresentação das fontes, distinguindo fontes estruturadas, recuperadas e citadas.
- Preservei os identificadores de consulta e execução e as referências dos registros apresentados.
- Validei o feedback persistido e seu vínculo com a resposta exibida, mesmo após editar a pergunta sem executar outra consulta.
- Criei testes automatizados para apresentação, paginação, preservação dos resultados e feedback.
- Atualizei `docs/STATUS_DO_PROJETO.md` com os resultados e as pendências identificadas.
- Enviei os commits de implementação e documentação em uma branch própria.

### Resultados obtidos

- Os 12 testes específicos da interface foram aprovados.
- A suíte offline foi concluída com 204 testes aprovados, excluindo os testes de integração dessa execução.
- A verificação de sintaxe e o `git diff --check` foram concluídos sem erros.
- A contagem de contratações com ano da compra 2026 apresentou 1.234 registros.
- A listagem com ano da compra 2026 e valor estimado estritamente acima de R$ 500 mil apresentou 560 correspondências.
- A tabela exibiu somente objeto e valor estimado, com 20 registros por página e 28 páginas.
- A navegação até a página 3 preservou o total, os filtros, os campos e as referências PNCP.
- A consulta documental sobre o art. 4º da Lei nº 14.133 recuperou o trecho pertinente e apresentou fontes recuperadas e citadas com uma evidência.
- O envio de feedback e a limpeza dos campos da interface foram verificados.
- O JSONL confirmou que o feedback permaneceu associado à pergunta original após a edição da caixa de pergunta, preservando `query_id`, `run_id` e fonte.
- Os testes simulados da apresentação combinada verificaram a preservação dos cálculos, das fontes e da resposta documental durante a paginação.
- Na consulta combinada real, a interface preservou o total de 1.234 e informou a ausência de evidências documentais, sem inventar uma explicação normativa.

### Dificuldades encontradas

A inicialização da tabela apresentou incompatibilidade entre os cabeçalhos vazios e a quantidade padrão de colunas do Gradio. Corrigi a configuração e validei a exibição dos campos solicitados.

Também identifiquei que o adaptador não preenchia o campo de fontes documentais. Corrigi a apresentação para distinguir as fontes recuperadas das fontes efetivamente citadas na resposta.

Durante a validação da consulta combinada, os logs mostraram que o filtro de ano das contratações também foi enviado à recuperação normativa. As buscas encontraram candidatos, mas nenhum permaneceu após os filtros. A separação dos filtros por estratégia ficou registrada como pendência para alinhamento com Luiz.

Na consulta normativa com três evidências, a geração desviou do tema solicitado, apesar de recuperar o art. 4º em primeiro lugar. Com uma evidência, respondeu ao tema, mas simplificou a distinção entre valor do item e valor da licitação. Essas limitações foram registradas e não foram corrigidas nesta implementação da interface.

As consultas iniciais também apresentaram latência elevada. Na execução combinada analisada, o roteamento consumiu aproximadamente 17,94 segundos, enquanto o cálculo estruturado levou cerca de 90 milissegundos.

### Apoio de IA

Utilizei uma ferramenta de IA para apoiar a adaptação da interface, a análise do formato dos resultados do executor, a elaboração dos testes e a interpretação dos logs. As alterações foram verificadas por testes automatizados, inspeção do diff e consultas reais na interface. Diferenciei os resultados comprovados das etapas ainda pendentes.

### Atividades realizadas pela equipe

Luiz disponibilizou a estratégia combinada de consulta estruturada e recuperação híbrida, que integrei à interface.

Janice acrescentou os casos de avaliação das personas para o corpus v3, com filtros, campos, respostas esperadas, cobertura temporal e critério contextual para Tecnologia/TIC.

Minha validação foi realizada com o corpus v2 restaurado, contendo 1.358 registros estruturados e artefatos de recuperação com 2.125 chunks. Portanto, os resultados não representam aprovação integral dos casos de avaliação do corpus v3.

### Próximas atividades

- Concluir a revisão e o merge da branch da interface.
- Alinhar com Luiz a separação dos filtros estruturados e documentais nas consultas combinadas.
- Repetir a validação real da estratégia combinada após a correção do executor.
- Encaminhar as falhas de fidelidade da resposta normativa para revisão da geração e da recuperação.
- Executar os casos das personas com o corpus e os artefatos correspondentes à versão v3.
- Validar a integração do critério contextual de Tecnologia/TIC definido por Janice.
- Manter o status do projeto atualizado com resultados, limitações e pendências.

## Encontro 10 — 07/10/2026

### Minha participação

- Participei da reunião de feedback com o professor e registrei as orientações para a continuidade do projeto.
- Organizei as prioridades da equipe, distinguindo atividades concluídas, pendências e dependências entre os integrantes.
- Apoiei Luiz na execução e conferência das consultas estruturadas, agregadas e combinadas, dos testes e dos registros de observabilidade.
- Auxiliei na integração das alterações de Luiz com os logs implementados por Felipe e na resolução do conflito em `retrieve.py`.

### Resultados obtidos

- O professor reforçou a necessidade de demonstrar na sexta-feira o fluxo integrado: pergunta, decisão da base e estratégia, consulta, resultado e logs.
- Foi destacada a importância de utilizar perguntas das personas na validação e de todos compreenderem o fluxo completo e a integração das responsabilidades.
- Após a integração das alterações nas branches, foram aprovados 296 testes, com exclusão da suíte de integração.
- A validação real do recuperador atualizado ficou pendente devido a timeout no endpoint de embeddings.
- Foram identificadas as próximas validações da interface, especialmente a apresentação dos novos resultados agregados.

### Apoio de IA

Utilizei ferramentas de IA como apoio na organização do feedback, revisão das pendências, elaboração de orientações e análise dos resultados apresentados durante as execuções.

### Próximas atividades

- Atualizar a interface para apresentar os resultados agregados.
- Validar as perguntas das personas na versão integrada, conferindo números, fontes, evidências e feedback.
- Atualizar o status do projeto com os resultados e as limitações.
- Organizar com a equipe a demonstração do fluxo e dos logs para sexta-feira.
