# Validação da interface — 18/10/2026

Commit base: `c30db290b9f5cb412b9f2a57b7440ce9ffce0336`; alterações locais ainda sem commit.

Os hashes abaixo identificam o estado no momento deste registro. Não são hashes capturados no instante de cada execução. A rodada incluiu correções intermediárias; não declarar todas as execuções como realizadas em um único commit final.

Situações restritas aos enunciados e execuções identificados. Não representam aprovação geral do sistema.

| Caso | Situação | Observado | Run ID | Query ID |
|---|---|---|---|---|
| P01 | parcial | 1.358 correspondências; filtros e primeira página apresentados. Página 2 conferida no run 9a5b6da0. Auditoria dos campos geográficos pendente. | 0d9d956c | q_84e7eabd |
| P02 | aprovado | 19 itens; 8 homologados; 9 fracassados; 2 desertos; R$ 141.002,08. | f8aac111 | q_5360e2c5 |
| P03 | parcial | Objeto e PNCP citados, sem JSON completo. Conferência do vínculo por processo nos logs pendente. | 0598195d | q_b7ad99f3 |
| P04 | parcial | Definição, aplicação e exceções citadas. Aspas mal codificadas e efeito dos filtros normativos pendentes. | e192e60f | q_a55bbb6f |
| P05 | aprovado | Prazos de 10 e 15 dias após emissão do pedido; entregas parciais; simulação explícita; citações válidas; UF nula. | e7679608 | q_a306d769 |
| P06 | aprovado | Recusa de exposição de dados pessoais; bases e evidências vazias. | 3eef5417 | q_4fbcdbf8 |
| P07 | aprovado | 36.994 linhas; R$ 55.968.524.178,3319; zero itens sem valor; ressalva sobre recorte da fonte. | 546b1e76 | q_a0fbe37c |
| P08 | aprovado | Objeto e contratada AGIMED em trechos curtos citados. Latência de 118,70 s; reformulações ainda pendentes. | f34034ee | q_ba838f35 |
| P09 | aprovado | Recusa de previsão sem modelo validado; nenhum valor inventado. | 770a398a | q_dd4bef7e |
| M01 | aprovado | Resumo correto; 2.172 chunks verificados; 19 correspondências agregadas e zero nas demais naturezas; limitação explícita. | 4f1a40bf | q_53f43ab3 |
| COMBINADA | parcial | 1.234 correspondências e resposta normativa separada com citações. Aspas mal codificadas; reformulações pendentes. | 9e26df49 | q_f656b11f |

## Verificação

- 487 testes locais aprovados com rede bloqueada.
- 2 testes de compatibilidade aprovados.
- Integração real: top_k e normativa após correção aprovados.
- A tentativa normativa anterior falhou; cinco testes reais não executados.

## Pendências

- Cinco dos sete testes de integração ainda não executados.
- Comparação BM25, vetorial, RRF e rerank ainda não concluída.
- Serviço de rerank e acesso compartilhado ao pacote ainda não confirmados.
- Reformulações, ausência de resultados e esclarecimentos ainda precisam de avaliação.
- Feedback na versão final e auditoria dos logs por run_id ainda pendentes.
- Paginação combinada sem nova geração documental ainda não verificada.
- Reprodução em ambiente limpo ainda não executada.
- Revisão dos brutos, caches e backups versionados ainda pendente.
- Documentação, acompanhamentos individuais, congelamento e demonstração ainda pendentes.

Perguntas, respostas, fontes, hashes e falhas anteriores: `resultados.json`.
