# Avaliação integrada — 09/10/2026 (versão atualizada)

**Projeto:** Grande Desafio — IA Generativa e RAG para Contratações Públicas do RJ  
**Escopo:** integridade dos artefatos v3, testes automatizados, recuperação híbrida, execução integrada da interface e observabilidade.  
**Atualização:** inclusão dos logs da execução integrada compartilhados por Eduarda (`b49c1873`).

## 1. Objetivo e critérios de entrega

Registrar perguntas, resultados, identificadores de execução, falhas e bloqueios de forma que outra pessoa consiga localizar as evidências nos logs. Distinguir aprovação de testes automatizados, comportamento da recuperação isolada e comportamento da execução integrada; o sucesso de uma etapa não comprova, isoladamente, a correção da resposta final.

## 2. Resumo executivo

- **Suíte automatizada:** 219 testes aprovados, 0 falhas, em 212,80 segundos (3min32s). Inclui **212 testes offline** e **7 testes integrados com LLM**. Os **28 testes de geração e schema** são subconjunto dos 212, não testes adicionais.
- **Corpus/índices v3:** consistência estrutural verificada para **2.125 chunks, 2.125 IDs e 2.125 vetores FAISS**, com dimensão 1.024; índice BM25 com 2.125 documentos.
- **Três consultas manuais de recuperação:** executadas e rastreadas no arquivo `logs/pipeline-2026-10-09.jsonl`, mas apresentaram limitações funcionais de relevância, cobertura multirrota e agregação.
- **Execução integrada fornecida por Eduarda:** consulta combinada retornou contagem estruturada **1.234 contratações de ano da compra 2026**, recuperou evidências normativas, gerou resposta e registrou validações bem-sucedidas; a confiança final foi **baixa**.
- **Conclusão:** testes automatizados aprovados e rastreabilidade de recuperação demonstrada. A correção funcional irrestrita do sistema **não** está comprovada; permanecem limitações e verificações pendentes.

## 3. Testes automatizados

| Verificação | Resultado | Observação |
|---|---|---|
| Suíte offline (`-m "not llm"`) | **212 aprovados** | Execução anterior à integração das alterações remotas da equipe |
| Geração e schema (`-k "generate or schema"`) | **28 aprovados** | Incluídos nos 212 testes offline |
| Integração com LLM | **7 aprovados** | Executados individualmente e em grupo |
| Suíte completa (`python -m pytest -q`) | **219 aprovados**, em **212,80 s** | Executada antes do rebase com as alterações mais recentes de `origin/main` |

Os sete testes integrados cobriram: persona Marina (arroz), persona Rodrigo (software), consulta normativa, correspondência de fontes com recuperação, respeito a `top_k`, não exposição de dados pessoais e consulta sensível. Os resultados `PASSED` confirmam o atendimento às asserções implementadas, não necessariamente a completude semântica de toda resposta.

## 4. Consultas manuais de recuperação — execução local

**Origem:** módulo de recuperação, sem geração de resposta final.  
**Arquivo de logs:** `logs/pipeline-2026-10-09.jsonl`.

| Caso | Pergunta | `query_id` | `run_id` | Linhas do log | Resultado observado |
|---|---|---|---|---|---|
| R1 — Normativa | O que a Lei nº 14.133 estabelece sobre o pregão? | `q_a5e16d7e` | `b28f1d65` | 153–157 | Art. 29 recuperado, mas parte dos trechos finais apresentou baixa pertinência |
| R2 — Agregada | No PE 038/26/2026, quantos itens foram homologados, fracassados e desertos e qual foi a soma dos valores homologados? | `q_6a3341d9` | `1a57d663` | 158–162 | Apenas dois chunks pertinentes ao processo entre os cinco resultados finais; insuficiente para agregação completa |
| R3 — Combinada | Quantas contratações têm ano da compra 2026 e o que a Lei nº 14.133 estabelece sobre o pregão? | `q_fa5f2507` | `06d8083d` | 163–167 | Cinco chunks finais estruturados, nenhum normativo; contagem não produzida por essa execução |

**Referências de conferência dos dados:** no arquivo de itens do PE 038/26/2026, foram identificados 19 itens: **8 homologados, 9 fracassados e 2 desertos**, com soma homologada de **R$ 141.002,08**. Na base estruturada normalizada, **1.234 dos 1.358 registros** têm `ano_compra=2026`. Esses números são referências de comparação, **não resultados calculados a partir dos cinco chunks finais de R2 ou R3**.

### 4.1 Estágios e latências dos três casos locais

Todos os 15 registros encontrados apresentaram `status=ok`, distribuídos entre `query_analysis`, `roteamento`, `retrieval_denso`, `retrieval_bm25` e `fusao_rrf`.

| Caso | Roteamento | Retrieval denso | BM25 | RRF | Soma aproximada dos estágios registrados |
|---|---:|---:|---:|---:|---:|
| R1 | 24.949,26 ms | 497,20 ms | 12,64 ms | 1,26 ms | **25,46 s** |
| R2 | 29.249,97 ms | 22.746,10 ms | 19,19 ms | 1,10 ms | **52,02 s** |
| R3 | 17.270,01 ms | 40.008,19 ms | 22,45 ms | 1,68 ms | **57,30 s** |

As somas representam apenas as latências registradas nos estágios, não uma medição independente do tempo de ponta a ponta. Essas execuções **não contêm** `geracao`, `validacao` ou `feedback`.

## 5. Execução integrada compartilhada por Eduarda

**Fonte recebida:** `log_combinada_b49c1873.json` (arquivo fornecido na conversa).  
**Data/hora inicial registrada:** 09/10/2026, 11:06:07 (UTC−03:00).  
**`run_id`:** `b49c1873`  
**`query_id`:** `q_28c8ccef`  
**Pergunta:** “Quantas contratações têm ano da compra 2026 e o que a Lei nº 14.133 estabelece sobre o pregão?”

### 5.1 Roteamento e contagem estruturada

O roteador registrou as rotas `agregada`, `estruturada` e `normativa`, com filtro `ano=2026` e `is_refusal=false`. A etapa `consulta_estruturada` executou `operacao=contar` com filtro `ano_compra=2026`, registrando **`total_base=1358`** e **`total=1234`**. Essa contagem coincide com a referência de conferência dos dados.

### 5.2 Recuperação normativa

A recuperação normativa foi realizada separadamente, com `routes=["normativa"]` e `filters={}`:

| Etapa | Candidatos | Destaques |
|---|---:|---|
| `retrieval_denso` | 50 | Chunks 202, 213 e 209 entre os primeiros |
| `retrieval_bm25` | 23 | Chunk 29 em primeiro, seguido dos chunks 137 e 44 |
| `fusao_rrf` | 67 candidatos combinados; **3 retornados** | `top_k=3`; rerank desabilitado |

O log mostra que a busca normativa **não aplicou o filtro `ano=2026`** nesta execução. Isso contrasta com o problema observado na recuperação isolada R3. Não é possível concluir, somente com esses registros, que todas as rotas e consultas do sistema já foram corrigidas.

### 5.3 Geração e validação

| Campo/etapa | Resultado registrado |
|---|---|
| `geracao` | `resposta_gerada=true` |
| Evidências fornecidas à geração | 3 |
| Validação de trechos literais | `trechos_validos=true` |
| Validação de citações | `citacoes_validas=true`; **1 evidência citada** |
| Validação de `RAGResponse` | `valido=true`; `is_refusal=false` |
| Resposta consolidada | `nivel_confianca="baixa"`; `quantidade_fontes=1` |
| Modelo | `qcwind/qwen3-8b-instruct-Q4-K-M` |
| Tokens de geração informados | 3.179 prompt + 369 completion = **3.548 total** |

O arquivo possui **dois registros de `geracao`**, com 3.548 tokens em ambos e latências de 15.157,04 ms e 15.246,29 ms. Parecem representar a mesma operação em níveis distintos de instrumentação; **não somar os tokens ou as duas latências** sem confirmação no código.

**Limite da evidência:** o JSON informa que a resposta foi gerada e validada, mas **não inclui o texto final da resposta**. Portanto, a fundamentação jurídica específica, a apresentação final da contagem e a suficiência da única citação não puderam ser auditadas a partir desse arquivo.

### 5.4 Latências registradas na execução integrada

| Estágio | Latência |
|---|---:|
| `roteamento` | 17.279,24 ms |
| `consulta_estruturada` | 158,13 ms |
| `retrieval_denso` | 985,60 ms |
| `retrieval_bm25` | 137,97 ms |
| `fusao_rrf` | 0,98 ms |
| `geracao` (registro da chamada) | 15.157,04 ms |
| `geracao` (registro consolidado) | 15.246,29 ms |
| Validações | 0,30 ms; 0,07 ms; 0,10 ms |

O roteamento e a geração são os maiores componentes observados nessa execução. A duplicidade dos registros de geração impede uma soma ingênua das latências.

## 6. Falhas, limitações e bloqueios

| ID | Achado | Evidência | Situação / encaminhamento |
|---|---|---|---|
| **REC-01** | Filtro de ano pode excluir documentos normativos com metadado `ano` vazio | R3: recuperação final sem chunks normativos; diagnóstico anterior em `chunk_atende_filtros()` | Verificar na versão atual do código e acrescentar teste de regressão. A execução da Eduarda usou recuperação normativa sem filtro de ano, mas não comprova correção universal |
| **REC-02** | Top-5 de chunks insuficiente para cálculos sobre todos os itens | R2: apenas dois chunks pertinentes entre cinco | Garantir agregação determinística sobre registros completos e testar contra os totais de referência |
| **REC-03** | Recuperação multirrota não preservou cobertura normativa | R3: cinco chunks finais estruturados | Testar cobertura por rota e comportamento após atualizações da equipe |
| **OBS-01** | Latência elevada em roteamento e, em alguns casos, recuperação densa | R1–R3 e execução Eduarda | Investigar tempos por estágio e estabelecer metas de desempenho |
| **OBS-02** | Registros potencialmente duplicados de geração | Execução Eduarda: duas entradas `geracao` com mesmos tokens | Verificar se são eventos complementares; evitar dupla contagem em métricas |
| **VAL-01** | Confiança final baixa apesar de validações estruturais aprovadas | Execução Eduarda: `nivel_confianca="baixa"`, citações e `RAGResponse` válidos | Inspecionar texto final, evidências citadas e critério de confiança |
| **VAL-02** | Texto da resposta final ausente do arquivo recebido | Log registra apenas indicadores de geração | Obter resposta final, se necessária avaliação semântica e jurídica |
| **OBS-03** | Rastreabilidade da execução Eduarda no log compartilhado ainda não verificada | Arquivo JSON recebido contém IDs, mas não foi localizado no `pipeline-2026-10-09.jsonl` desta estação | Confirmar onde a equipe armazena os logs dessa execução e permitir consulta por `run_id` |
| **TEST-01** | Suíte consolidada executada antes da atualização recente da `main` | 219 aprovados antes do rebase | Reexecutar testes na versão atualizada quando o ambiente estiver pronto |

Nenhuma falha automatizada foi observada nas execuções informadas. Os itens acima são **limitações funcionais, de evidência ou de observabilidade**, não testes Pytest reprovados.

## 7. Instruções para reprodução e rastreabilidade

### 7.1 Localizar as três execuções locais

Na raiz do repositório, em PowerShell:

```powershell
Get-Content .\logs\pipeline-2026-10-09.jsonl |
    ConvertFrom-Json |
    Where-Object { $_.run_id -in @('b28f1d65', '1a57d663', '06d8083d') } |
    Select-Object run_id, query_id, stage, status, latencia_ms |
    Format-Table -AutoSize
```

**Resultado observado:** 15 registros, cinco por `run_id`, todos com `status=ok`; linhas 153–167 no arquivo verificado em 09/10/2026. As posições das linhas podem mudar caso o arquivo seja alterado; os IDs são a referência estável.

### 7.2 Inspecionar a execução integrada da Eduarda

Com o arquivo `log_combinada_b49c1873.json` disponível localmente:

```powershell
Get-Content .\log_combinada_b49c1873.json -Raw |
    ConvertFrom-Json |
    Where-Object { $_.run_id -eq 'b49c1873' } |
    Select-Object run_id, query_id, stage, status, latencia_ms |
    Format-Table -AutoSize
```

O arquivo recebido contém **11 registros**, todos com `status=ok`, incluindo `consulta_estruturada`, `geracao` e `validacao`. O caminho acima é ilustrativo: ajuste-o ao local em que o JSON for salvo. **Não foi confirmado que esse arquivo integra os logs versionados ou compartilhados da equipe.**

## 8. Entregas e versionamento

- Relatório original: `eval/avaliacao_integrada_2026-10-09.md`, enviado à `main` no commit **`301e680`**.
- Esta versão atualizada incorpora o arquivo enviado por Eduarda e **ainda requer substituição/atualização do relatório no repositório**; sua criação neste ambiente não altera automaticamente o GitHub.
- Commit sugerido após revisão: `docs: complementa avaliacao integrada com logs da interface`.
- Não incluir a pasta `data/`, os artefatos de índices, inventários ou arquivos temporários no commit de documentação.
- O commit sugerido `test: valida fluxo integrado e observabilidade` só se justifica se houver modificações reais em testes ou instrumentação; a aprovação de testes já existentes, isoladamente, não exige novo commit `test:`.

## 9. Conclusão

A avaliação de 09/10/2026 registra **219 testes automatizados aprovados** e comprova a localização de três execuções locais de recuperação por identificadores nos logs. A execução integrada enviada por Eduarda acrescenta evidências de **contagem determinística correta (1.234 registros de 2026), recuperação normativa separada, geração e validação estrutural**, mas terminou com **confiança baixa** e não disponibilizou o texto final para auditoria semântica.

A entrega de documentação fica mais completa com essas evidências, mas as limitações de recuperação, agregação, observabilidade e revalidação após atualizações da equipe permanecem registradas. A avaliação deve ser considerada **aprovada quanto aos testes automatizados executados e parcialmente validada quanto ao comportamento funcional de ponta a ponta**.
