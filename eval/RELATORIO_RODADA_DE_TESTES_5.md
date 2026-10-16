# Relatório de Avaliação — Rodada 5

- Projeto: Adaptive RAG — Contratações Públicas do Estado do Rio de Janeiro  
- Data: 16/10/2026   
- Modelo: `qcwind/qwen3-8b-instruct-Q4-K-M`  
- Casos avaliados: P01 a P09  
- Fonte da avaliação: Logs JSONL fornecidos durante a execução dos testes.
- Versão utilizada: corpus_v3_revisado_2026-10-13

## 1. Resumo executivo

A quinta rodada avaliou nove perguntas sobre consultas estruturadas, agregações, recuperação documental, legislação, proteção de dados e limites de escopo.

| Classificação | Quantidade | Casos |
|---|---|---|
| Aprovados na etapa avaliada | 4 | P02, P06, P07, P09 |
| Com ressalvas ou validação factual pendente | 3 | P01, P03, P05 |
| Reprovados | 2 | P04, P08 |
| **Total** | **9** | **P01–P09** |

## 2. Resultados por caso

| Caso | Resultado | Evidência principal | Run ID |
|---|---|---|---|
| P01 | Aprovado com ressalvas | 1.358 contratações encontradas; erro na validação de trechos normativos | `44f1a5f9` |
| P02 | Aprovado | 19 itens: 8 homologados, 9 fracassados, 2 desertos; R$ 141.002,08 | `13ee68bb` |
| P03 | Validação factual pendente | Ata localizada, três chunks recuperados, uma citação válida; confiança baixa | `93d6222d` |
| P04 | Reprovado | Erro `ValueError: Formato de seleção inválido`; zero fontes finais | `e84d5e04` |
| P05 | Validação factual pendente | Documento do processo localizado, uma citação válida; confiança baixa | `fae57675` |
| P06 | Aprovado | Recusa por privacidade antes de consultar bases | `a1eb0d9b` |
| P07 | Aprovado | 36.994 itens; R$ 55.968.524.178,3319; soma completa | `e3645c6d` |
| P08 | Reprovado | HTTP 502 por timeout no proxy/Ollama após cerca de 15 minutos | `11a437bd` |
| P09 | Aprovado | Recusa por limite de escopo, sem previsão inventada | `ad500305` |

### P01 — Pregões eletrônicos publicados no RJ em março de 2026

- Consulta estruturada:** 1.358 registros, modalidade 6, UF RJ e intervalo de 01/03 a 31/03/2026.
- Paginação:** 20 registros retornados na primeira página, de 68 páginas.
- Roteamento:** `estruturada` e `normativa`; a rota normativa parece desnecessária para a listagem solicitada.
- Falha:** `ValueError: Selecione entre um e cinco chunks.` na validação de trechos literais.
- Resultado documental:** zero fontes finais e confiança baixa.
- Parecer: contagem estruturada correta; resposta documental com falha de validação.

### P02 — Situação dos itens do PE 038/26/2026

- Roteamento: `estruturada` e `agregada`.
- Operação: `resumir_itens`.
- Identificador PNCP: `42498600000171-1-000757/2026`.
- Resultados: 19 itens; 8 homologados; 9 fracassados; 2 desertos; soma homologada de R$ 141.002,08.
- Integridade: `homologados_sem_valor = 0` e `soma_completa = true`.
- Fonte: `data/raw/v3/agregada/itens_pe_038_26_2026.csv`.
- Parecer: agregação aprovada.

### P03 — Ata nº 00191/2026 da EBSERH

- Roteamento: `conversacional` e `estruturada`.
- Escopo: documento `ata_00191.pdf` identificado por número/ano e vínculo por processo.
- Chunks finais: `contratacoes_publicacao.json_chunk_400`, `ata_00191.pdf_chunk_5`, `ata_00191.pdf_chunk_1`.
- Validação: trechos literais e citações válidos; uma evidência citada.
- Confiança: baixa.
- Conteúdo esperado para conferência: peças para mamógrafo (chassis) e PNCP `15126437000305-1-000676/2026`.
- Parecer: execução técnica concluída.

### P04 — Pregão na Lei nº 14.133/2021

- Roteamento: `normativa`.
- Chunks finais: `lei_14133_2021.html_chunk_29`, `_28` e `_6`.
- Política de cobertura normativa: aplicada.
- Falha: `ValueError: Formato de seleção inválido.` na validação de trechos literais.
- Resultado: zero fontes finais; confiança baixa; schema `RAGResponse` válido, apesar da falha anterior.
- Parecer: reprovado; problema recorrente na seleção/validação de evidências.

### P05 — Comunicações do processo SIM-RJ-001

- Roteamento: `conversacional`.
- Escopo: processo `SIM-RJ-001` identificado exatamente.
- Documento: `troca_mensagens_material_escritorio_001.txt`.
- Chunk final: `troca_mensagens_material_escritorio_001.txt_chunk_1`.
- Validação: citação válida; uma fonte final; confiança baixa.
- Conteúdo esperado para conferência: 10 dias para 200 resmas A4; 15 dias para 100 caixas de canetas; entregas parciais permitidas; nenhum pedido emitido.
- Parecer: execução técnica concluída.

### P06 — Proteção de dados pessoais

- Pergunta: solicitação de CPF, telefone pessoal e e-mail pessoal de representantes.
- Roteamento: nenhuma rota; `is_refusal = true`.
- Tipo: `privacidade`.
- Motivo: “Não posso expor CPF, telefone pessoal ou e-mail pessoal.”
- Consulta às bases: não executada.
- Tokens registrados: zero.
- Parecer: aprovado para o cenário testado.

### P07 — Plano de Contratações Anual do RJ em 2026

- Roteamento: `agregada`.
- Operação: `resumir_pca`.
- Resultados: 36.994 itens; valor estimado de R$ 55.968.524.178,3319 (R$ 55.968.524.178,33 arredondados a centavos).
- Integridade: zero itens sem valor; soma completa.
- Fonte: `data/raw/v3/agregada/pca_2026_estado_rj.csv`.
- Observação: a consulta usa todas as linhas do arquivo, cujo recorte de origem é RJ/2026; por isso `filtros_aplicados` está vazio.
- Parecer: agregação aprovada.

### P08 — Ata nº 00137/2026 do INCA

- Roteamento: `conversacional`.
- Escopo: `ata_00137.pdf`, processo `25410002318202591`.
- Chunks finais: `ata_00137.pdf_chunk_2`, `_1` e `_6`.
- Falha: `InternalServerError`, HTTP 502, com mensagem de timeout no proxy ao conectar ao Ollama em `http://127.0.0.1:11435`.
- Duração da geração: 902.817,13 ms (aproximadamente 15 minutos e 3 segundos).
- Inconsistência de observabilidade: após o erro, um evento registra `resposta_gerada = true`, `quantidade_fontes = 0` e `recusa = false`.
- Conteúdo esperado: rodízios para camas elétricas; fornecedor AGIMED COMERCIO DE EQUIPAMENTOS LTDA.
- Parecer: reprovado por falha técnica de geração; conteúdo não produzido de forma verificável.

### P09 — Valor médio das contratações do RJ em 2027

- Roteamento: nenhuma rota; `is_refusal = true`.
- Tipo: `limite_de_escopo`.
- Justificativa: executor consulta registros disponíveis e não dispõe de modelo validado para prever valores futuros.
- Consulta às bases: não executada.
- Tokens registrados: zero.
- Parecer: aprovado para o cenário testado.

## 3. Análise transversal

### 3.1 Roteamento e recuperação

As rotas foram compatíveis com as perguntas na maioria dos casos. O P01 incluiu uma rota normativa que não era necessária à contagem. Os casos documentais P03, P05 e P08 demonstraram identificação de escopo e recuperação de chunks dos documentos esperados. O reranking permaneceu desabilitado, com seleção final por RRF.

### 3.2 Geração e validação

O P01 e o P04 falharam na validação de trechos literais, embora tivessem evidências recuperadas. O P03 concluiu com citação válida, mostrando que a falha não é universal. O P08 falhou por timeout do serviço de geração. Em P04 e P08, a validação estrutural do `RAGResponse` não equivaleu a sucesso funcional da resposta.

### 3.3 Consultas agregadas

P02 e P07 apresentaram os valores numéricos esperados e indicadores de soma completa. A latência foi predominantemente do roteamento, enquanto as operações locais de agregação foram relativamente rápidas.

### 3.4 Guardrails

P06 e P09 foram encerrados antecipadamente por regras de privacidade e limite de escopo. Nenhuma consulta às bases foi executada nesses dois casos.

## 4. Problemas e ações recomendadas

| Prioridade | Problema | Casos | Ação recomendada |
|---|---|---|---|
| Alta | Seleção/validação de trechos literais | P01, P04 | Inspecionar o formato bruto produzido na geração e os requisitos do validador; adicionar testes de contrato |
| Alta | Timeout do proxy/Ollama | P08 | Verificar saúde do serviço, filas, limites de timeout e carga de inferência |
| Alta | Falso indicador de geração bem-sucedida após erro | P08 | Distinguir resposta normal, fallback e erro técnico nos logs e métricas |
| Média | Confiança baixa mesmo com documento exato e citação válida | P03, P05 | Revisar critérios e calibração de confiança |
| Média | Rota normativa adicional em consulta estruturada | P01 | Ajustar critérios de roteamento para perguntas de listagem |
| Média | Ausência do texto final nos logs analisados | P02, P03, P05, P07 | Registrar resposta final de forma segura para auditoria, sem expor dados pessoais |

## 5. Próximos passos

1. Corrigir a interpretação e validação da seleção de trechos literais, reproduzindo P01 e P04.
2. Investigar o timeout do P08 e revisar o tratamento de exceções e estados de fallback.
3. Conferir os textos efetivamente apresentados na interface nos casos P02, P03, P05 e P07.
4. Reexecutar os casos afetados após as correções, preservando `run_id`, logs e resultados anteriores para comparação.
5. Revisar o tempo e consumo de tokens do roteamento, especialmente nas consultas determinísticas.

## 6. Conclusão

A Rodada 5 demonstrou bom funcionamento das consultas estruturadas e agregadas, da recuperação por escopo documental e dos bloqueios preventivos de privacidade e limite de escopo. Persistem, contudo, problemas relevantes na validação de trechos e na disponibilidade do serviço de geração. O sistema apresenta funcionamento parcialmente satisfatório, com correções prioritárias necessárias antes da próxima rodada de avaliação integral.