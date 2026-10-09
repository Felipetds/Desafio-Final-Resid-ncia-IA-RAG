# Relatório de validação dos cenários P01–P09 e M01 — 09/10/2026

**Projeto:** Grande Desafio Adaptive RAG — Cenário 1, Contratações Públicas do Estado do Rio de Janeiro  
**Frente:** Corpus e Avaliação  
**Ambiente:** Google Colab, cópia experimental do repositório  
**Estado de publicação:** preparado para revisão; não publicado no GitHub

## 1. Objetivo

Registrar os resultados observados nos testes de avaliação das personas e na investigação multifonte M01. **Aprovação do caso** significa que o objetivo específico do procedimento executado foi satisfeito; não implica, por si só, execução autônoma de todo o pipeline em produção.

## 2. Resumo executivo

| Cenário | Estado | Escopo efetivamente verificado |
|---|---|---|
| P01 | Aprovado | Consulta estruturada sobre os 1.358 registros PNCP RJ de março/2026; fluxo ponta a ponta no procedimento testado |
| P02 | Aprovado | Consulta agregada ao PE 038/26/2026 e validação de contagens e soma |
| P03 | Aprovado com ressalva | Fundamentação com ata EBSERH e controle PNCP por seleção multifonte **controlada** |
| P04 | Aprovado | Consulta normativa sobre pregão e Lei nº 14.133/2021, com geração e citações |
| P05 | Aprovado com ressalva | Recuperação filtrada por processo e geração com evidências **controladas** |
| P06 | Aprovado | Recusa de solicitação envolvendo dados pessoais |
| P07 | Aprovado com ressalva | Soma do PCA e integração **controlada** com geração e validação de fontes |
| P08 | Aprovado com ressalva | Ata INCA e resposta citada por seleção **controlada** |
| P09 | Aprovado | Recusa de estimativa especulativa para 2027 |
| M01 | Pendente | Ausência de correspondência estruturada no corpus original local |

**Balanço:** 9 casos P01–P09 aprovados em seus respectivos escopos, incluindo ressalvas; M01 pendente. Esse balanço **não é taxa de acurácia** nem prova de execução ponta a ponta de todas as quatro naturezas.

## 3. Evidências e valores verificados

### P01 — Estruturada
- Corpus PNCP RJ: modalidade 6 (pregão eletrônico), publicações de 01/03/2026 a 31/03/2026.
- 1.358 registros estruturados.

### P02 — Agregada
- Contratação: PE 038/26/2026; identificador de referência `42498600000171-1-000757/2026`.
- Fonte: `data/raw/v3/agregada/itens_pe_038_26_2026.csv` no ambiente experimental.
- 19 itens: 8 homologados, 9 fracassados, 2 desertos; soma homologada R$ 141.002,08.
- P02 permanece aprovada independentemente do resultado da M01.

### P03 — Conversacional e estruturada, seleção controlada
- Ata EBSERH nº 00191/2026, Pregão nº 90019/2026, controle PNCP `15126437000305-1-000676/2026`.
- Chunks documentais `ata_00191.pdf_chunk_1` e `ata_00191.pdf_chunk_2`; evidência estruturada do controle PNCP.
- Seleção extrativa e validação de citações realizadas em integração controlada. Não demonstrada seleção multifonte autônoma ponta a ponta.

### P04 — Normativa
- Pregão eletrônico e Lei nº 14.133/2021: resposta gerada com três chunks normativos citados no teste executado.

### P05 — Conversacional, integração controlada
- Processo fictício `SIM-RJ-001`: entrega em 15 dias, com entregas parciais de papel A4 em 10 dias e canetas em 15 dias.
- Recuperação por filtro de processo e geração com evidência pertinente; seleção não demonstrada como fluxo integralmente automático.

### P06 e P09 — Guardrails
- P06: recusa a pedido de CPF, telefone ou e-mail pessoal.
- P09: recusa de média ou projeção para contratações do RJ em 2027 sem suporte no corpus.

### P07 — Agregada, integração controlada
- PCA RJ 2026: 36.994 linhas; soma exata dos valores estimados `55968524178.3319` (R$ 55.968.524.178,3319).
- Evidência sintética derivada da soma real utilizada para validar o gerador oficial com substituição temporária e controlada da seleção do modelo.
- O resultado corresponde ao arquivo analisado, não a filtros linha a linha de outros recortes.

### P08 — Conversacional, seleção controlada
- Ata INCA nº 00137/2026, objeto: rodízios para camas elétricas; fornecedor AGIMED COMERCIO DE EQUIPAMENTOS LTDA.
- Evidências `ata_00137.pdf_chunk_1` e `ata_00137.pdf_chunk_6`; resposta com citação e seleção controlada.

## 4. Investigação M01 — resultado definitivo para o corpus local

**Pergunta técnica:** o PE 038/26/2026, presente na base agregada, também possui registro estruturado exato no corpus PNCP indexado?

1. O índice experimental carregado contém **2.125 chunks**: 1.358 estruturados, 217 normativos, 31 conversacionais e 519 agregados.
2. Foram encontrados 19 registros de itens da contratação na natureza **agregada**.
3. A busca exata por `numeroControlePNCP = 42498600000171-1-000757/2026` retornou **0 registros estruturados** nos chunks.
4. O arquivo original foi localizado em `/content/testes_p01/contratacoes_publicacao.json`, com **3.145.581 bytes** e **1.358 registros PNCP**.
5. A busca exata no JSON original retornou **0 correspondências**. O índice também possui 1.358 chunks estruturados, mas a equivalência de contagens não prova equivalência de conteúdo item a item.

**Conclusão:** M01 permanece **pendente por limitação de cobertura da base estruturada local**. Não é uma reprovação do gerador; o fluxo multifonte não pôde ser exercitado com esse par documental. A ausência na coleta local não autoriza afirmar que o registro inexiste no PNCP em geral. Não combinar contratações por CNPJ ou numeração parcialmente coincidente.

## 5. Limitações metodológicas

- Diferenciar **teste ponta a ponta**, **integração controlada** e **consulta/recusa isolada**.
- P03, P05, P07 e P08 tiveram intervenções experimentais explícitas; não representam roteamento, recuperação, seleção e geração totalmente autônomos.
- A presença de quatro naturezas no índice não comprova relacionamento factual entre quaisquer quatro documentos recuperados.
- Os caminhos absolutos `/content/...` são locais ao Colab e não devem ser incluídos como dependências do repositório.
- Não foram alterados os dados brutos congelados, o índice nem os módulos de produção nesta etapa.

## 6. Encaminhamentos

1. Revisar este relatório com a equipe e vinculá-lo aos logs/notebooks de execução, quando forem selecionados para publicação.
2. Se a M01 for reexecutada, selecionar uma contratação cuja identidade exata seja comprovada previamente em duas fontes distintas, sem mudar retroativamente a classificação desta execução.
3. Atualizar o resumo do README somente após revisão e alinhamento com o estado efetivo da branch principal.
4. Preparar a apresentação do Demo Day com as decisões de fundamentação, recusas, limites de cobertura e integração controlada.

**GitHub:** não alterado durante a preparação deste relatório.
