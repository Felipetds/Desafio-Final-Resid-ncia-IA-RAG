# Status do projeto — revisão de 21/10/2026

## Versão em preparação

- Branch: `fix/respostas-explicativas-20261021T192459760154Z`.
- Base: `746c4941171ef5b25193a259d36951bf23a8c047`.
- Publicação remota das correções ainda não confirmada.
- Tag anterior preservada: `entrega-2026-10-19`.
- Corpus e índices preservados: 2.172 chunks.

## Implementado e conferido nos casos registrados

- Síntese explicativa citada como padrão, com modo extrativo explícito preservado.
- Planejamento validado e cálculo nos CSVs autorizados do PE e PCA.
- Contagem, comparação, agrupamento, listagem e média em casos reais.
- Esclarecimento para condições conhecidas ausentes no arquivo de itens.
- Separação de pedidos numéricos e documentais nos casos combinados avaliados.
- Preparação de contexto normativo e PDF sem regenerar índices.
- Histórico e feedback preservados em processos separados.
- Reabertura visual da pergunta e resposta no histórico.
- Uma única tabela na consulta conferida.

## Testes

- Última suíte local completa informada: 754 aprovados e sete `llm` desmarcados.
- Ajuste posterior do histórico: 18 testes relacionados aprovados.
- Casos reais identificados no relatório das correções.
- Os 585 testes locais, dois de compatibilidade e sete de integração
  da reprodução anterior não substituem a validação da revisão atual.

## Falta para publicar

1. Histórico conferido com a consulta `8474c27d`.
2. Revisar alterações e arquivos novos de código e testes.
3. Concluir as verificações necessárias da versão a publicar.
4. Fazer commit, push e integração; registrar a versão publicada.

## Pendências de engenharia preservadas

- Confirmar publicação da correção de metadados e ampliação das fixtures.
- Adequar coleta integral, idempotência, pausas e falhas por fonte.
- Alinhar manifesto e ingestão quanto a sensibilidade e vigência.
- Centralizar configuração e completar logging dos módulos de preparação.
- Registrar reprodução de versão identificada por outro integrante.
- Identificar versão e artefatos do benchmark complementar da Janice.
- Conferir acessos e acompanhamentos individuais.

A revisão documental não encerra esses itens.
Os casos aprovados não garantem interpretação de qualquer pergunta
nem atendimento integral ao enunciado.

## Referências

- [README](../README.md).
- [Arquitetura](../ARQUITETURA.md).
- [Correções de 21/10](CORRECOES_RESPOSTAS_2026-10-21.md).
- [Restauração](GUIA_RESTAURACAO_2172.md).
- [Fechamento histórico](FECHAMENTO_ENTREGA_2026-10-19.md).

## Consolidação da validação — 21/10/2026

Após o ajuste do indicador de conclusão das consultas combinadas, a suíte local completa teve **754 testes aprovados e sete `llm` desmarcados**. Em uma execução separada, os **sete testes de integração real foram aprovados**.

A interface respondeu à pergunta simples sobre homologações com oito itens, sem exigir instrução de tamanho da resposta. A consulta `8474c27d`, `query_id=q_10d777d6`, apareceu no histórico na conferência solicitada. A reabertura e a apresentação sem tabela duplicada já haviam sido conferidas na consulta `4c11bd77`.

A rodada parcial anterior de 18 testes foi seguida pela suíte completa de 754 testes. Os sete testes reais são uma rodada separada; não constituem avaliação universal das perguntas ou nova avaliação completa das personas.

Registros: [evidências](validacao_respostas_2026-10-21/evidencias.json). A publicação e a integração remotas ainda precisam ser confirmadas.
