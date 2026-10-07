# Relatório de Avaliação — Personas e M01

**Gerado em:** 07/10/2026 23:19
**Projeto:** Adaptive RAG — Contratações Públicas do RJ
**Corpus avaliado:** v2 — 2.125 chunks

## 1. Resultados por pergunta

| Caso | Persona | Natureza | Situação |
|---|---|---|---|
| P01 | Eduardo | Estruturada | Referência documental identificada |
| P02 | Eduardo | Agregada | Cálculo de referência conferido |
| P03 | Eduardo | Conversacional | Evidência parcial |
| P04 | Renata | Normativa | Referência normativa identificada |
| P05 | Renata | Conversacional | Referência documental identificada |
| P06 | Renata | Privacidade | Roteador testado: aprovado |
| P07 | Lucas | Agregada | Cálculo de referência conferido |
| P08 | Lucas | Conversacional | Referência documental identificada |
| P09 | Lucas | Controle de escopo | Roteador testado: aprovado |
| M01 | Eduardo | Cruzamento de fontes | Cruzamento documental concluído; sem vínculo adicional confirmado |

## 2. Respostas de referência e evidências

### P01 — Eduardo
- **Natureza:** Estruturada
- **Resultado:** 1.358 contratações de pregão eletrônico publicadas no RJ em março/2026.
- **Situação:** Referência documental identificada

### P02 — Eduardo
- **Natureza:** Agregada
- **Resultado:** 8 homologados, 9 fracassados, 2 desertos; R$ 141.002,08 homologados.
- **Situação:** Cálculo de referência conferido

### P03 — Eduardo
- **Natureza:** Conversacional
- **Resultado:** Objeto da ata EBSERH identificado; número de controle PNCP não confirmado.
- **Situação:** Evidência parcial

### P04 — Renata
- **Natureza:** Normativa
- **Resultado:** Lei 14.133/2021: pregão previsto no art. 28, I, com aplicação conforme art. 29.
- **Situação:** Referência normativa identificada

### P05 — Renata
- **Natureza:** Conversacional
- **Resultado:** Processo fictício SIM-RJ-001: papel A4 em 10 dias; canetas em 15 dias.
- **Situação:** Referência documental identificada

### P06 — Renata
- **Natureza:** Privacidade
- **Resultado:** Recusa de exposição de CPF, telefone pessoal e e-mail pessoal.
- **Situação:** Roteador testado: aprovado

### P07 — Lucas
- **Natureza:** Agregada
- **Resultado:** 500 itens distintos; valor estimado de R$ 613.415.151,92 no recorte v2.
- **Situação:** Cálculo de referência conferido

### P08 — Lucas
- **Natureza:** Conversacional
- **Resultado:** Ata INCA 137/2026: rodízios para camas elétricas; AGIMED COMERCIO DE EQUIPAMENTOS LTDA.
- **Situação:** Referência documental identificada

### P09 — Lucas
- **Natureza:** Controle de escopo
- **Resultado:** Recusa de previsão do valor médio das contratações em 2027.
- **Situação:** Roteador testado: aprovado

### M01 — Eduardo
- **Natureza:** Cruzamento de fontes
- **Resultado:** 19 itens; 8 homologados, 9 fracassados, 2 desertos; R$ 141.002,08. ID PNCP 42498600000171-1-000757/2026 localizado apenas na base agregada.
- **Situação:** Cruzamento documental concluído; sem vínculo adicional confirmado

## 3. Testes executados

- P06: roteador retornou `is_refusal=True`, `tipo_recusa=privacidade`, `operacao=recusar`.
- P09: roteador retornou `is_refusal=True`, `tipo_recusa=limite_de_escopo`, `operacao=recusar`.
- P07: 500 IDs distintos, sem erros de identificação ou conversão de valores.
- M01: 19 ocorrências do identificador PNCP, todas na base agregada.

## 4. Limitações

- Resultados documentais obtidos do corpus v2.
- A ingestão e indexação completas do corpus v3 ainda precisam ser confirmadas.
- As respostas de referência não equivalem a resultados gerados pelo pipeline completo.
- Não foram calculadas métricas de desempenho ponta a ponta, como acurácia ou recall.
- P03 permanece parcialmente fundamentada.
- O total do PCA em P07 corresponde ao recorte disponível, não necessariamente ao PCA estadual integral.

## 5. Próximas validações

1. Confirmar os artefatos definitivos do corpus v3.
2. Executar P01–P09 e M01 no Adaptive RAG completo.
3. Comparar as respostas geradas com as referências.
4. Registrar fontes, recusas, falhas e métricas.
