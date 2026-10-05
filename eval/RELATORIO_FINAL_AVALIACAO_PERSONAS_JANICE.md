# Relatório Final — Avaliação das Perguntas por Persona

**Responsável:** Janice Lira  
**Cenário:** Contratações Públicas do Estado do Rio de Janeiro  
**Arquitetura:** Adaptive RAG  
**Corpus:** v3  
**Escopo:** Avaliação das perguntas P01–P09

---

## 1. Objetivo

Este relatório consolida a revisão dos nove casos de avaliação associados
às personas do projeto.

Para cada pergunta foram considerados:

- objetivo da persona;
- tipo de resposta esperada;
- filtros necessários;
- campos necessários;
- fontes do corpus;
- resposta esperada verificável;
- necessidade de recusa;
- compatibilidade com o corpus.

Também foram realizados testes experimentais de recuperação para verificar
o comportamento do pipeline Adaptive RAG em casos representativos.

---

## 2. Cobertura do corpus

### Base estruturada PNCP

Recorte utilizado:

- UF: RJ;
- modalidade: Pregão Eletrônico;
- modalidade_id: 6;
- período: 01/03/2026 a 31/03/2026;
- quantidade de registros: 1.358;
- IDs únicos: 1.358.

As demais naturezas do corpus — normativa, conversacional e agregada —
possuem coberturas próprias e não devem ser interpretadas automaticamente
como equivalentes ao período da base estruturada.

---

## 3. Critério para categoria Tecnologia/TIC

Foi definido como critério principal classificar uma contratação como
Tecnologia/TIC quando houver evidência textual suficiente no corpus de que
o objeto corresponde à aquisição ou contratação de bem ou serviço de TIC.

### Campos prioritários

- objeto;
- descrição do item;
- descrição do serviço;
- especificação.

### Campos auxiliares

- categoria;
- classificação;
- informações complementares.

### Termos indicativos

- software;
- licença de software;
- computador;
- servidor;
- armazenamento;
- rede;
- telecomunicações;
- segurança da informação;
- cibersegurança;
- computação em nuvem;
- nuvem;
- desenvolvimento de sistemas;
- suporte de TI.

Termos genéricos como **digital**, **eletrônico**, **sistema** e
**tecnologia** não devem, isoladamente, determinar a classificação.

Casos ambíguos devem ser encaminhados para revisão, mantendo-se a
rastreabilidade do campo e do texto utilizados como evidência.

---

## 4. Casos de avaliação

| Caso | Persona | Tipo principal | Fonte | Situação |
|---|---|---|---|---|
| P01 | Eduardo — Auditor | Listagem + contagem | Estruturada/PNCP | Verificável |
| P02 | Eduardo — Auditor | Contagem + comparação | Agregada | Verificável |
| P03 | Eduardo — Auditor | Explicação | Conversacional + estruturada | Parcial no retrieval |
| P04 | Renata — Advogada | Explicação | Normativa | Verificável |
| P05 | Renata — Advogada | Explicação | Conversacional sintética | Verificável |
| P06 | Renata — Advogada | Explicação + recusa | Guardrail | Recusa esperada |
| P07 | Lucas — Gestor Hospitalar | Contagem | Agregada | Verificável |
| P08 | Lucas — Gestor Hospitalar | Explicação | Conversacional | Falha original diagnosticada |
| P09 | Lucas — Gestor Hospitalar | Explicação + recusa | Guardrail temporal | Recusa esperada |

---

## 5. Respostas esperadas verificáveis

### P01

Pergunta sobre contratações de pregão eletrônico publicadas no RJ em
março de 2026.

**Resultado esperado:** 1.358 registros.

A resposta deve respeitar:

- UF = RJ;
- modalidade_id = 6;
- período de 01/03/2026 a 31/03/2026.

---

### P02

Pergunta sobre o PE 038/26/2026.

**Resultado esperado:**

- total: 19;
- homologados: 8;
- fracassados: 9;
- desertos: 2;
- valor total: R$ 141.002,08.

Fonte agregada:
`itens_pe_038_26_2026.csv`.

---

### P03

Pergunta sobre a ata 00191/2026 da EBSERH.

**Resposta esperada:**

- Ata: SEI 191/2026;
- Pregão: 90019/2026;
- Processo: 23877.002295/2026-92;
- controle PNCP: 15126437000305-1-000676/2026;
- objeto: aquisição de Produtos para Saúde — peças mamógrafas
  (chassis), para o Complexo Hospitalar da Universidade Federal do
  Rio de Janeiro (CH-UFRJ/EBSERH).

Evidência estruturada principal:
`contratacoes_publicacao.json_chunk_400`.

### Resultado experimental do P03

Antes da simulação de correção, os 12 chunks conversacionais da ata eram
eliminados pelo filtro temporal.

Após tratar temporariamente `ano=''` como metadado ausente:

- dense candidates: 25;
- BM25 candidates: 25;
- RRF candidates: 25;
- evidências retornadas: 5;
- `contratacoes_publicacao.json_chunk_400` apareceu na posição 2.

Entretanto, o ranking também recuperou chunks da ata 00137/2026.

**Classificação:** resultado parcial.

O sistema encontra a evidência estruturada correta, mas apresenta perda de
precisão documental ao misturar atas distintas.

---

### P04

Pergunta normativa sobre pregão na Lei nº 14.133.

Evidências esperadas:

- Art. 6º, XLI;
- Art. 28, I;
- Art. 29, caput e parágrafo único.

Chunks principais:

- chunk 6;
- chunk 28;
- chunk 29.

---

### P05

Caso baseado no documento sintético `SIM-RJ-001`.

Elementos verificáveis:

- papel A4: 200 resmas;
- prazo: 10 dias após o pedido;
- canetas: 100 caixas;
- prazo: 15 dias;
- entregas parciais permitidas no cenário simulado.

A resposta deve informar explicitamente que se trata de conteúdo
**sintético/fictício**, e não de uma contratação real.

---

### P06

Pergunta envolvendo CPF, telefone pessoal ou e-mail pessoal.

**Comportamento esperado:** recusa.

O sistema não deve expor dados pessoais.

No teste anterior, o roteador aplicou corretamente a recusa para este caso.

---

### P07

Pergunta sobre o PCA RJ 2026.

**Resultado esperado:**

- 36.994 itens;
- valor total: R$ 55.968.524.178,3319.

Para esse caso, a validação determinística sobre a base agregada é mais
adequada do que depender exclusivamente de recuperação vetorial.

---

### P08

Pergunta sobre a ata 00137/2026 do INCA.

**Resposta esperada:**

- objeto relacionado à aquisição de rodízios para camas elétricas;
- item A50372;
- rodízio com freio;
- fabricante/marca: TENTE;
- quantidade: 1.028;
- valor unitário: R$ 311,00;
- valor total: R$ 319.708,00;
- fornecedor contratado:
  AGIMED COMERCIO DE EQUIPAMENTOS LTDA;
- CNPJ: 03.852.519/0001-96.

Evidência conversacional do fornecedor:
`ata_00137.pdf_chunk_6`.

Evidência estruturada complementar:
`contratacoes_publicacao.json_chunk_158`.

### Resultado original do P08

O roteador selecionou:

`conversacional`

e extraiu:

`ano = 2026`

Resultado:

- dense candidates: 0;
- BM25 candidates: 0;
- RRF candidates: 0;
- evidências retornadas: 0.

### Diagnóstico

Os 10 chunks da ata 00137 apresentavam:

- natureza = conversacional;
- sensitivity = restrito;
- UF = RJ;
- ano = string vazia (`''`).

Todos os 10 chunks atendiam à rota conversacional.

Entretanto:

- atendem à rota: 10/10;
- atendem aos filtros: 0/10.

---

## 6. Falha sistemática identificada

A investigação demonstrou que o problema não estava na classificação da
natureza nem no tratamento da sensibilidade.

O campo:

`ano=''`

era considerado presente pelo filtro.

Ao tentar converter a string vazia para inteiro, a conversão falhava e o
chunk era rejeitado.

O mesmo comportamento foi observado em:

- P03 — ata 00191/2026;
- P08 — ata 00137/2026.

### Teste controlado

Resultado antes e depois da normalização simulada:

| Caso | Antes | Depois |
|---|---:|---:|
| P03 — ata 00191 | 0/12 | 12/12 |
| P08 — ata 00137 | 0/10 | 10/10 |

A alteração foi simulada exclusivamente em memória.

Nenhum arquivo original foi modificado durante o teste.

---

## 7. P08 após correção simulada

Após tratar temporariamente campos vazios como ausentes:

- dense candidates: 23;
- BM25 candidates: 23;
- RRF candidates: 23;
- evidências retornadas: 5.

As cinco evidências retornadas pertenciam à ata 00137/2026.

A primeira evidência foi:

`ata_00137.pdf_chunk_2`

contendo, entre outros elementos:

- item A50372;
- rodízio com freio;
- fabricante TENTE;
- quantidade 1.028;
- valor unitário R$ 311,00;
- valor total R$ 319.708,00.

**Conclusão:** a normalização do metadado vazio recuperou o funcionamento
da etapa de retrieval para P08.

---

## 8. Segunda limitação identificada

O P03 revelou uma limitação adicional.

Mesmo após a correção simulada do campo `ano`, o retrieval misturou
evidências das atas 00191 e 00137.

O chunk estruturado correto:

`contratacoes_publicacao.json_chunk_400`

foi recuperado na posição 2, mas chunks da ata 00137 também apareceram
entre os primeiros resultados.

Isso indica necessidade de reforçar a precisão documental utilizando,
quando disponíveis:

- número da ata;
- número do processo;
- número da compra;
- órgão/entidade;
- identificador PNCP.

Esses identificadores podem ser utilizados como filtros, sinais de
reranqueamento ou critérios de correspondência documental.

---

## 9. P09

Pergunta sobre valor médio futuro em 2027.

A base estruturada avaliada cobre março de 2026.

Não existe evidência suficiente no corpus para responder factualmente
sobre contratações de 2027.

**Comportamento esperado:** recusar ou informar insuficiência de evidência.

O sistema não deve produzir previsão como se fosse informação observada
no corpus.

---

## 10. Conclusões

A revisão dos nove casos confirmou que as respostas esperadas podem ser
definidas de forma verificável e compatível com as fontes correspondentes.

A avaliação experimental também identificou dois pontos técnicos
relevantes.

### 1. Tratamento de metadados vazios

Strings vazias, especialmente no campo `ano`, devem ser normalizadas como
valores ausentes antes da aplicação dos filtros.

A falha foi reproduzida em P03 e P08.

A simulação em memória demonstrou que a normalização elimina a rejeição
indevida dos chunks conversacionais.

### 2. Precisão documental

Perguntas que identificam uma ata específica devem utilizar os
identificadores documentais disponíveis para evitar mistura de evidências
provenientes de documentos semelhantes.

O P03 demonstrou essa necessidade ao recuperar simultaneamente conteúdos
das atas 00191 e 00137.

---

## 11. Recomendação técnica

Recomenda-se:

1. normalizar strings vazias dos metadados para valores ausentes;
2. preservar filtros válidos de UF, ano, modalidade, município e fornecedor;
3. extrair números de ata, processo, compra e PNCP quando presentes;
4. utilizar esses identificadores no filtro ou reranqueamento;
5. manter regras explícitas de recusa para privacidade e perguntas fora da
   cobertura temporal;
6. validar novamente P03 e P08 após eventual correção no pipeline.

---

## 12. Status do entregável

O entregável individual contempla:

- nove perguntas revisadas;
- objetivos das personas;
- classificação do tipo de resposta;
- filtros;
- campos necessários;
- fontes;
- respostas esperadas verificáveis;
- cobertura temporal;
- critério Tecnologia/TIC;
- regras de recusa;
- validação experimental;
- diagnóstico das falhas encontradas;
- recomendações técnicas.

**Status: concluído.**

---

Relatório produzido a partir dos testes realizados sobre o corpus v3 e
sobre o subconjunto experimental de 47 chunks utilizado na avaliação.
