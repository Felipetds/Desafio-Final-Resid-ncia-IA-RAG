# Avaliação integrada — 09/10/2026

**Projeto:** Grande Desafio — RAG para Contratações Públicas do RJ  
**Escopo:** Testes automatizados, recuperação híbrida e observabilidade com corpus v3.

## 1. Validação automatizada

- **212 testes offline aprovados.**
- **7 testes integrados com LLM aprovados.**
- **219 testes aprovados na execução consolidada**, sem falhas, em 212,80 segundos.
- Os 28 testes de geração e schema constituem um subconjunto dos testes offline.
- Artefatos v3 consistentes: 2.125 chunks, 2.125 identificadores e 2.125 vetores FAISS.

## 2. Consultas e resultados

| Consulta | Query ID | Run ID | Resultado |
|---|---|---|---|
| O que a Lei nº 14.133 estabelece sobre o pregão? | `q_a5e16d7e` | `b28f1d65` | Recuperação normativa parcialmente relevante; artigo 29 recuperado, mas outros trechos pouco pertinentes |
| No PE 038/26/2026, quantos itens foram homologados, fracassados e desertos e qual foi a soma dos valores homologados? | `q_6a3341d9` | `1a57d663` | Evidências insuficientes para calcular os totais completos |
| Quantas contratações têm ano da compra 2026 e o que a Lei nº 14.133 estabelece sobre o pregão? | `q_fa5f2507` | `06d8083d` | Recuperação exclusivamente estruturada, sem evidências normativas entre os cinco resultados finais |

As consultas foram executadas pelo módulo de recuperação. **Não representam respostas finais geradas pelo LLM.**

## 3. Observabilidade e rastreabilidade

**Arquivo:** `logs/pipeline-2026-10-09.jsonl`

| Run ID | Linhas | Estágios | Status |
|---|---|---|---|
| `b28f1d65` | 153–157 | 5 | Todos `ok` |
| `1a57d663` | 158–162 | 5 | Todos `ok` |
| `06d8083d` | 163–167 | 5 | Todos `ok` |

Os estágios registrados são `query_analysis`, `roteamento`, `retrieval_denso`, `retrieval_bm25` e `fusao_rrf`.

**Latências acumuladas dos estágios registrados:**
- Normativa: aproximadamente 25,46 segundos.
- Agregada: aproximadamente 52,02 segundos.
- Combinada: aproximadamente 57,30 segundos.

Os identificadores foram localizados no arquivo de log e os 15 registros apresentam status `ok`.

## 4. Falhas e limitações

**REC-01 — Filtro de ano em documentos normativos.** Um chunk normativo com metadado `ano` vazio é excluído quando o filtro exige `ano=2026`. A causa foi identificada na função `chunk_atende_filtros()`.

**REC-02 — Agregações incompletas.** A recuperação limitada a cinco chunks não disponibiliza todos os registros necessários para contagens e somatórios completos.

**REC-03 — Cobertura multirrota insuficiente.** A consulta combinada não preservou evidências normativas entre os resultados finais.

**OBS-01 — Latência.** O roteamento e a recuperação densa apresentaram custos elevados nas consultas analisadas.

## 5. Bloqueios e pendências

- Corrigir a aplicação dos filtros de ano às bases normativas.
- Implementar ou validar agregações determinísticas sobre o conjunto completo de dados.
- Garantir cobertura adequada das diferentes rotas nas consultas combinadas.
- Criar testes de regressão para os problemas identificados.
- Validar separadamente a rastreabilidade das etapas de geração e validação, não presentes nesses 15 registros.

## 6. Conclusão

A suíte automatizada foi integralmente aprovada, com **219 testes passando**. A rastreabilidade das três consultas de recuperação foi confirmada por `run_id`, `query_id`, estágio e status.

Apesar disso, os testes manuais identificaram limitações funcionais de recuperação e agregação. Portanto, a aprovação automatizada não equivale à aprovação funcional irrestrita do sistema.
