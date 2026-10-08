# Status do Projeto — Adaptive RAG para Contratações Públicas do RJ

**Grupo:** 1
**Residência:** TIC em Trilhas — PUC-Rio / Instituto ECOA
**Atualização:** 07/10/2026
**Consolidação:** Maria Eduarda Ribeiro da Silva

## 1. Resumo

O fluxo mínimo foi demonstrado na interface:

**pergunta → análise e planejamento → consulta → resposta → logs.**

Foram executadas consultas estruturadas, agregadas, documentais e combinadas.
Resultados apresentam filtros, recortes, fontes e identificadores.
Feedback e navegação entre páginas foram validados.

A integração TIC foi implementada e validada na branch de trabalho.
Ainda falta publicar essa alteração, confirmar sua integração na main
e registrar a versão definitiva da demonstração.

Esta validação não representa aprovação integral das personas ou do corpus v3.

## 2. Integração e versões

| Entrega | Situação |
|---|---|
| Documentação de critérios e cobertura da Janice | PR #20 integrado |
| Interface com agregados e delimitação documental | PR #21 integrado |
| Validação de referências na geração | PR #22 integrado |
| Respostas normativas por seleção de chunks | PR #23 integrado |
| Critério e apresentação TIC na interface | Validado na branch; publicação pendente |

**Main remota consultada:** `5514484ba9a67aa7ef679b2d917fc9887848a053`.
**Branch atual:** `feat/criterio-tic-interface-eduarda`.
**Commit base local:** `ff13a86cd55dfea669ddda133606a035623252da`.

Registrar o commit definitivo após integrar as alterações escolhidas.
As execuções abaixo ocorreram em diferentes etapas de desenvolvimento;
seus IDs não devem ser atribuídos automaticamente ao commit final.

## 3. Dados e artefatos usados

As validações da interface utilizaram o corpus v2 restaurado no Colab.

| Natureza | Chunks |
|---|---:|
| Estruturada | 1.358 |
| Normativa | 217 |
| Conversacional | 31 |
| Agregada | 519 |
| **Total** | **2.125** |

A coleta estruturada registrou 28 páginas da API, 1.358 registros
e 1.358 IDs PNCP preenchidos e únicos.

Os chunks agregados incluem uma amostra de 500 itens do PCA e 19 itens
da contratação selecionada. Os cálculos determinísticos consultam
os arquivos completos, independentemente dessa amostra de recuperação.

FAISS, BM25, lista de IDs e cache foram anteriormente validados como
persistidos. Uma reexecução registrou 2.125 embeddings em cache e zero
novos envios naquele ambiente.

Igualdade de quantidades e IDs não substitui a conferência de compatibilidade
de conteúdo quando o corpus é alterado.

### Corpus v3

O inventário registra oito arquivos e zero falhas de integridade.
Na comparação estruturada, ambas as versões possuem 1.358 registros:
1.314 idênticos e 44 alterados, sem IDs adicionados ou removidos.

Sete arquivos permaneceram idênticos e um foi alterado:
`contratacoes_publicacao.json`. Dados brutos permanecem fora do Git.

A documentação da Janice registra 228 novos embeddings, cache de 368
vetores de 1.024 dimensões e cobertura normativa e conversacional de 100%
no recorte documentado.

Isso não comprova índices completos de todas as naturezas do v3.
Permanecem por confirmar:
- integração dos caches e situação dos 19 embeddings agregados;
- alinhamento entre manifesto v3 e caminhos da ingestão;
- disponibilidade de chunks, base normalizada e índices compatíveis com v3.

## 4. Fluxo e módulos

| Etapa | Módulos | Saída |
|---|---|---|
| Entrada | app/app.py | Pergunta e quantidade de evidências |
| Planejamento | router.py e aggregate_planning.py | Bases, estratégia, operação, filtros e paginação |
| Estruturada | query_executor.py e structured_query.py | Contagem ou listagem sobre o recorte |
| Agregada | aggregate_query.py e cross_source.py | Contagens, situações, somas e vínculos |
| Recuperação | retrieve.py e retrieval_lexical.py | Evidências e metadados |
| Geração | generate.py e grounded_quotes.py | Resposta e fontes citadas |
| Apresentação | pipeline_adapter.py e interface_results.py | Resultados, tabelas e contexto |
| Registro | obs.py e feedback_store.py | Eventos e avaliações persistidos |

Estratégias: consulta_estruturada, consulta_agregada,
recuperacao_hibrida e combinada. Recusas e esclarecimentos interrompem
a execução quando pertinentes.

Cálculos estruturados e agregados não são limitados pelo top_k.
A combinada separa os filtros estruturados dos documentais.

A decomposição da pergunta enviada à geração cobre uma forma explícita:
“Quantas contratações têm ano da compra AAAA e o que a Lei...”.
Outras formulações ainda exigem avaliação.

## 5. Resultados validados na interface

| Caso | Resultado |
|---|---|
| Contagem por ano da compra 2026 | 1.234 em 1.358 registros |
| Listagem de 2026 acima de R$ 500 mil estimados | 560; apenas objeto e valor estimado |
| Paginação | 20 por página, 28 páginas; total, filtros e campos preservados |
| Retorno à página anterior | Confirmado pela responsável |
| P02 | 19 itens: 8 homologados, 9 fracassados, 2 desertos; R$ 141.002,08 |
| P07 | 36.994 linhas; soma estimada informada de R$ 55.968.524.178,3319 |
| M01 | 2.125 chunks verificados; 19 vínculos agregados por identificador; zero nas demais naturezas |
| Documental | Texto normativo com citação do chunk correspondente |
| Combinada | 1.234 e artigo 29 apresentado separadamente |
| Controle de evidências | Com top_k 1 e 3, cálculo, filtro e fonte estruturada preservados |
| TIC | 51 propostas com critério, versão e aviso de ausência de validação humana |
| Feedback | Pergunta original, fontes e IDs preservados após paginação e edição |

P02, P07 e M01 também tiveram cálculos reais iguais com top_k 1 e 3,
usando análise fornecida, sem chamada ao modelo do roteador.

P02 usa o ID PNCP `42498600000171-1-000757/2026`.

A soma do PCA representa os valores informados no arquivo.
Não valida o orçamento estadual. Origem, recorte, duplicações e possíveis
inconsistências exigem conferência própria.

M01 procura ID PNCP completo ou URL específica do edital.
Ausência de vínculo não comprova ausência de documentos relacionados.
Não verifica vínculos exclusivamente por conteúdo ou outros processos.

## 6. Tecnologia/TIC

O adaptador fornece o critério contextual ao executor.
A interface apresenta descrição, versão e classificação proposta.
Os campos TIC são preservados no resultado principal da combinada.

| Indicador | Quantidade |
|---|---:|
| Registros no recorte | 1.358 |
| TIC proposto | 51 |
| Revisão | 217 |
| Sem indício reconhecido | 1.090 |
| Tipo indeterminado entre as propostas | 17 |

Versão: `tic-contextual-v3`. Validação humana: não confirmada.

Os 17 tipos indeterminados integram as propostas e não devem ser somados
às três categorias principais. “Sem indício” não comprova ausência de TIC.

A contagem TIC passou em execução real na interface.
A preservação dos campos na combinada foi testada automaticamente;
uma combinada TIC real não foi apresentada nesta sessão.

## 7. Recuperação, geração e proteção

A recuperação utiliza busca densa, lexical, filtros e RRF.
Busca lexical contextual foi integrada para os recortes suportados.
Não foi comprovada nesta sessão melhoria geral de ranking ou avaliação
comparativa completa de vidraçaria.

A validação de referências rejeita citações ausentes ou desconhecidas.
Uma referência existente não garante suporte semântico à afirmação.

Em recuperações exclusivamente normativas, com natureza explícita,
o modelo seleciona IDs e o código apresenta o texto original dos chunks.
Seleções vazias, IDs desconhecidos e formatos inválidos são bloqueados.
Relevância e completude da seleção ainda exigem avaliação.

As demais consultas documentais mantêm a geração textual anterior.
A proteção de dados pessoais continua aplicada.

Há testes de mascaramento de CPF, telefone e e-mail.
A indicação restrito_sanitizado não garante remoção de todo dado pessoal.

O rerank possui implementação configurável e testes simulados registrados.
Endpoint, ativação e validação real atuais permanecem por confirmar.

## 8. Logs, feedback e histórico

Eventos JSONL possuem query_id e run_id.
Complementos de recuperação com rotas, filtros, candidatos, IDs e bases,
além de testes de falha controlada, foram integrados.

Reunir os eventos completos das demonstrações escolhidas, conferindo
os mesmos IDs da interface e as bases efetivamente consultadas.

Feedback: `data/feedback/feedback.jsonl`, configurável por FEEDBACK_PATH.
Contém pergunta, avaliação, comentário, IDs, rota e fontes.

O vínculo com a resposta exibida foi conferido após paginação e edição
da pergunta sem executar outra consulta.

**Histórico completo de perguntas e respostas:** implementação própria
não identificada na inspeção; pendência registrada separadamente.
Logs e feedback não substituem esse histórico.

No Colab, preservar arquivos externamente para sobreviver à troca de runtime.
Persistência no mesmo ambiente não comprova persistência entre runtimes.

## 9. Identificadores de referência

| Caso | Query ID | Run ID |
|---|---|---|
| Contagem | q_b1c77195 | ce23bd37 |
| Listagem — página 1 | q_53ce9203 | 32845cc8 |
| Página 2 e feedback | q_53ce9203 | ade86df8 |
| P02 | q_b4e468ff | aafe7ef9 |
| P07 | q_5e3a735e | 2d6f170a |
| M01 | q_7d655c86 | a2438202 |
| Documental — formato literal anterior | q_c307e951 | 0109ff2d |
| Combinada — seleção de IDs | q_3a4f419f | a4f02cb7 |
| Combinada — top_k 1 | q_9afb9dad | c7d3bc3e |
| Combinada — top_k 3 | q_07c22ef9 | cf789d38 |
| TIC | q_74f95bea | a3b8c79b |

## 10. Testes e avaliação

Última suíte local: **332 aprovados em 7,32 segundos**, na branch TIC.

Comando: `python -m pytest -q --ignore=testes/teste_integracao.py`.

A execução específica de interface TIC, consultas TIC, interface estruturada
e combinada teve 20 testes aprovados. Git diff --check sem erros.

Após o merge, conferir a versão integrada.
Totais de versões anteriores não devem ser somados.

Há documentação e relatório v2 em eval/.
Sua existência não comprova aprovação integral das personas.
Confirmar a avaliação consolidada de P01–P09, M01 e reformulações,
com esperado, observado, fonte, IDs e situação.

## 11. Responsabilidades conhecidas

| Frente | Responsáveis | Situação |
|---|---|---|
| Interface e coordenação | Maria Eduarda | Casos validados; publicação TIC e preparação da demonstração pendentes |
| Fidelidade e citações | Maria Eduarda, com apoio a alinhar | PRs #22 e #23 integrados; avaliação mais ampla permanece |
| Planejamento e consultas | Luiz | Estruturadas, agregadas e combinadas implementadas |
| Personas e critérios | Janice | Documentação integrada; avaliação completa por confirmar |
| Ingestão, índices e caches | Eridalgo e responsáveis da frente | Integração completa v3 por confirmar |
| Observabilidade e integração | Felipe | Complementos integrados; reunir logs finais |
| Reprodutibilidade | Calvin | Confirmar execução completa em ambiente limpo |

Esta tabela registra a divisão conhecida, sem atribuir novas tarefas.

## 12. Pendências

| Frente | Critério de conclusão |
|---|---|
| Publicação TIC | PR integrado e verificação na main |
| Versão da demonstração | Commit e versão dos dados/artefatos registrados |
| Logs da demonstração | Percurso verificável com os mesmos IDs da interface |
| Roteiro e capturas | Sequência ensaiada e arquivos disponíveis |
| Personas | Casos avaliados com fontes, IDs e situação |
| Corpus v3 | Manifesto, ingestão, caches e índices compatíveis |
| Reprodutibilidade | Guia executado em ambiente limpo |
| Histórico | Persistência e recuperação de perguntas e respostas |
| Qualidade | Avaliação de relevância e completude, incluindo vidraçaria |
| Infraestrutura | Rerank real e configuração permanente de timeouts confirmados |

Timeout de 60 segundos e max_retries=0 foram configurados temporariamente
na sessão do Colab, sem alteração permanente dos arquivos.

Houve latências variáveis e timeouts. Medir etapas antes de otimizar.
O progresso da interface não estima tempo restante nem comprova aceleração.

## 13. Roteiro proposto — sexta-feira, 09/10/2026

1. Explicar fluxo, módulos e entradas/saídas.
2. Mostrar contagem estruturada, plano, recorte e fonte.
3. Mostrar consulta documental e chunk citado.
4. Mostrar combinada, separando cálculo e documento.
5. Apresentar P02 como cálculo sobre arquivo completo.
6. Apresentar TIC como classificação proposta.
7. Enviar feedback e conferir o registro.
8. Abrir logs pelos mesmos IDs da interface.
9. Declarar versão do corpus e limitações.

P07 e M01 podem ser exemplos adicionais ou capturas de reserva.
Preparar capturas de P02, P07, M01, combinada, TIC e feedback.
Salvamento das capturas e ensaio ainda não foram confirmados.

Se o endpoint falhar, identificar a saída como execução anterior.
Não apresentar captura salva como consulta ao vivo.

## 14. Referências

- corpus_manifest.yaml
- docs/GUIA_DO_PIPELINE.md
- docs/CONSULTAS_AGREGADAS.md
- eval/CRITERIOS_PERSONAS_RECORTE_CORPUS_2026-10-07.md
- eval/COBERTURA_EMBEDDINGS_V3_2026-10-07.md
- eval/relatorio_avaliacao_personas_v2.md
- docs/historico/STATUS_DO_PROJETO_ANTES_CONSOLIDACAO_2026-10-07.md

Os registros anteriores foram preservados no histórico.
Este documento não declara conclusão integral do projeto.
