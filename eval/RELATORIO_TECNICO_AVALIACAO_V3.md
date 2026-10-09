# Relatório Técnico de Avaliação — Corpus V3

**Projeto:** Adaptive RAG — Contratações Públicas do Estado do Rio de Janeiro  
**Programa:** Residência TIC em Trilhas — IA Generativa e RAG (PUC-Rio / Instituto ECOA)  
**Avaliação original de roteamento:** 02/10/2026  
**Verificações complementares:** até 08/10/2026  
**Escopo:** corpus, índices, roteamento, auditorias e testes específicos; **não equivale à validação ponta a ponta**.

## 1. Objetivo e metodologia

Consolidar as evidências verificadas do corpus V3 e do roteamento adaptativo entre quatro naturezas de fontes: **estruturada, normativa, conversacional e agregada**. São distinguidos: (a) os resultados históricos da avaliação original; (b) as auditorias factuais e documentais; (c) os testes técnicos posteriores em Colab. A existência de um gabarito no corpus não demonstra, por si só, que o pipeline de recuperação e geração produz a resposta correta.

## 2. Corpus V3

O arquivo `chunks_v3_avaliacao.json` foi carregado como JSON válido e contém **38.619 chunks**. Todos apresentam os campos de metadados `chunk_id`, `source_file`, `doc_type`, `sensitivity`, `base_id`, `natureza`, `uf`, `ano`, `modalidade`, `orgao`, `municipio`, `valor`, `fornecedor` e `vigencia`.

| Natureza | Chunks |
|---|---:|
| Estruturada | 1.358 |
| Normativa | 217 |
| Conversacional | 31 |
| Agregada | 37.013 |
| **Total** | **38.619** |

A natureza agregada predomina numericamente; essa assimetria deve ser considerada ao interpretar a cobertura da recuperação.

## 3. Índices e correspondência com o corpus

Foram localizados `faiss_index.bin`, `chunk_ids.json`, `bm25_index.pkl`, `cache_embeddings.json` e `chunks_teste.json` em um conjunto de índices identificado como `indices_definitivos_2125`.

- **FAISS:** 2.125 vetores de dimensão 1.024; arquivo carregado com sucesso.
- **IDs:** 2.125 identificadores, todos únicos e todos encontrados entre os `chunk_id` do corpus V3.
- **Teste de busca vetorial:** a reconstrução e consulta do primeiro vetor retornou o próprio identificador em primeiro lugar, com distância `0.000000`.
- **BM25:** arquivo localizado, mas não foi demonstrado neste conjunto de testes um benchmark de recuperação lexical ou híbrida.

| Natureza | Chunks no corpus | IDs no índice |
|---|---:|---:|
| Estruturada | 1.358 | 1.358 |
| Normativa | 217 | 217 |
| Conversacional | 31 | 31 |
| Agregada | 37.013 | 519 |
| **Total** | **38.619** | **2.125** |

**Interpretação:** há cobertura integral, por quantidade de IDs, das naturezas estruturada, normativa e conversacional, e cobertura parcial da agregada. A correspondência dos IDs foi verificada, mas isso não comprova equivalência semântica dos embeddings nem desempenho em perguntas reais.

## 4. Avaliação original de roteamento — 02/10/2026

Foram executados dez casos: P01 a P09 e M01. O relatório consolidado original classificou **1 aprovado no roteamento, 8 em conformidade parcial e 1 com divergência de roteamento**.

| Caso | Resultado original | Principal observação |
|---|---|---|
| P01 | Conformidade parcial | Rota estruturada correta; faltaram modalidade numérica e datas como filtros. |
| P02 | Conformidade parcial | Rotas estruturada e agregada; faltou filtro de processo. |
| P03 | Conformidade parcial | Rotas conversacional e estruturada; rota adicional exigia comprovação documental. |
| P04 | Conformidade parcial | Rota normativa correta; faltaram filtros de norma e tema. |
| P05 | Conformidade parcial | Rota conversacional correta; faltou filtro de processo. |
| P06 | Aprovado no roteamento | Solicitação de dados pessoais recusada, sem rotas. |
| P07 | Conformidade parcial | Rota agregada correta; faltou filtro de documento PCA. |
| P08 | Conformidade parcial | Rota conversacional correta; faltaram filtros de órgão e ata. |
| P09 | Divergência de roteamento | Previsão de 2027 não foi recusada na execução original. |
| M01 | Conformidade parcial | Quatro rotas selecionadas, mas faltou filtro de processo e prova de vínculos. |

Esses resultados **não foram reclassificados retroativamente** após as correções posteriores.

## 5. Auditorias factuais e documentais

### P01 — PNCP estruturado

Conferidos **1.358 registros** de pregão eletrônico no RJ publicados em março de 2026; **0 fora do período** e **0 identificadores PNCP duplicados**.

### P02 — Itens do PE 038/26/2026

Conferidos **19 itens**, sendo **8 homologados, 9 fracassados e 2 desertos**. Valor total homologado: **R$ 141.002,08**. A soma foi auditada com `Decimal` sobre o CSV original.

### P03 — Ata EBSERH

Confirmada evidência documental cruzada da ata SEI nº 191/2026 com a fonte PNCP estruturada. Identificador PNCP registrado na auditoria: `15126437000305-1-000676/2026`; **uma correspondência exata** identificada pela auditoria. A recuperação automática ainda não foi demonstrada.

### P04 — Lei 14.133/2021

Dispositivos conferidos na fonte normativa: art. 6º, XLI; art. 28, I; e art. 29, caput e parágrafo único. O gabarito documental foi localizado, sem teste de geração final.

### P05 — Simulação SIM-RJ-001

Fonte conversacional **inteiramente sintética**. Auditoria de três mensagens: papel A4, 200 resmas, entrega em 10 dias; canetas, 100 caixas, entrega em 15 dias; há previsão de entregas parciais. Nenhum pedido real foi emitido. A resposta final deverá sinalizar explicitamente que é uma simulação.

### P07 — PCA 2026

Conferidos **36.994 itens**, com valor total estimado de **R$ 55.968.524.178,3319**. As **225 diferenças aritméticas** apontadas na auditoria ficaram dentro da tolerância de `0,0001`; a causa exata não foi comprovada e os dados originais não foram alterados.

### P08 — Ata INCA

Ata nº 137/2026: aquisição eventual de rodízios para camas elétricas, **1.028 unidades** a **R$ 311,00**, total de **R$ 319.708,00**, com conferência aritmética aprovada. A ata menciona publicação no PNCP em **01/04/2026**, fora do recorte estruturado de março; não se deve presumir correspondência nessa base.

### P09 — Limite temporal

A auditoria da fonte estruturada registrou **zero contratações de 2027** no conjunto examinado. O gabarito esperado é recusar previsão numérica sem evidência suficiente. A execução original não recusou; houve correção posterior descrita na seção 6.

### M01 — Cruzamento entre fontes

O resultado quantitativo do processo-alvo foi sustentado pela fonte agregada, mas a auditoria encontrou **zero correspondências exatas** do identificador da contratação na base PNCP estruturada examinada. A seleção de quatro rotas não comprova vínculo documental entre todas elas.

## 6. Correções posteriores — P06 e P09

Após o relatório original de 02/10/2026, foram aplicadas correções ao módulo `src/router.py` e realizados testes específicos no Colab:

- `analisar_consulta`: P06 e P09 recusados, sem rotas selecionadas.
- `planejar_consulta`: P06 e P09 com operação de recusa e sem bases selecionadas.
- Observabilidade: eventos de análise e roteamento registrados para os dois casos.
- Atualização informada no GitHub por meio do commit `65c53b50954b6aa9d5d1105133fb5b82a96bbf8c`.

**Limite da evidência:** os testes comprovam as decisões das funções avaliadas, não a resposta final do aplicativo em execução ponta a ponta.

## 7. Verificações complementares de ambiente

- Presença dos nove arquivos essenciais verificada (**9/9**).
- Análise sintática AST dos nove módulos aprovada (**9/9**).
- Importação de seis módulos aprovada (**6/6**) após instalação de `faiss-cpu`.
- Leitura do JSON do corpus V3 aprovada.
- Integridade referencial dos 2.125 IDs do índice frente ao corpus aprovada.
- Teste básico de recuperação FAISS aprovado.

Essas verificações ocorreram em ambiente Colab e não substituem testes de integração completos.

## 8. Limitações e pendências

1. Avaliar a recuperação de evidências e a geração de respostas finais com perguntas reais e métricas explícitas.
2. Verificar recuperação lexical BM25, fusão híbrida e reranqueamento, se utilizados na configuração final.
3. Documentar e, quando necessário, corrigir a extração de filtros específicos (processo, ata, norma, período e documento).
4. Preservar o recorte temporal da fonte estruturada e evitar associações cross-source sem correspondência demonstrada.
5. Explicitar a cobertura parcial da natureza agregada no índice FAISS examinado.
6. Validar os guardrails também na resposta final da aplicação.

## 9. Conclusão

A V3 dispõe de **corpus auditado com 38.619 chunks**, quatro naturezas identificadas, **2.125 IDs indexados e reconciliados com o corpus**, teste básico de recuperação vetorial aprovado e auditorias factuais/documentais dos casos de avaliação. Os guardrails P06 e P09 foram aprovados em testes específicos posteriores à avaliação original.

A documentação permite apresentar os resultados técnicos efetivamente observados, **sem afirmar validação ponta a ponta do Adaptive RAG**, que permanece como trabalho complementar.

## 10. Referências internas e rastreabilidade

- `avaliacao_v3/backup_auditoria_completa/data/processed/chunks_v3_avaliacao.json`
- `avaliacao_v3/backup_auditoria_completa/eval/resultados_roteamento_v3/relatorio_roteamento_v3.md`
- `avaliacao_v3/backup_auditoria_completa/eval/resultados_roteamento_v3/consolidado_roteamento_v3.json`
- `avaliacao_v3/backup_auditoria_completa/eval/resultados_roteamento_v3/auditoria_*.json`
- Conjunto de índices `indices_definitivos_2125` (`faiss_index.bin`, `chunk_ids.json`, `bm25_index.pkl`).
- Testes complementares executados no Google Colab.

> **Nota:** os caminhos de avaliação acima referem-se aos arquivos de evidência identificados no ambiente de trabalho/backup; não se pressupõe que todos estejam versionados no repositório GitHub.
