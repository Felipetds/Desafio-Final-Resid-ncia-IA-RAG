# Validação da coleta e do inventário — Janice

## Verificações concluídas

- JSON estruturado existente: 1.358 registros.
- `numeroControlePNCP`: 1.358 preenchidos e 1.358 únicos.
- `dataPublicacaoPncp`: 1.358 datas válidas, todas entre
  02/03/2026 e 31/03/2026, dentro do período do manifesto
  (01/03/2026 a 31/03/2026).
- Inventário v2: contém os oito campos obrigatórios do contrato.
- Inventário local: 8 arquivos, distribuídos em 5 bases e
  4 naturezas (estruturada, normativa, conversacional e agregada).
- `update`: criou v2 sem alterar a v1.
- Diff por SHA-256: identificou corretamente 1 arquivo modificado
  em teste isolado e 7 idênticos.
- Testes automatizados: 2 passaram.

## Verificação pendente

A tentativa de consultar a primeira página do PNCP com os filtros
do manifesto retornou HTTP 500: "Erro na comunicação com o banco
de dados". Por isso, a reconstrução dos 1.358 registros por uma
nova execução de `fetch` ainda não foi comprovada.

## Limite dos testes

Os testes das quatro naturezas utilizaram fontes locais verificadas
por SHA-256. Eles não comprovam que todas as fontes possam ser
baixadas automaticamente por outra pessoa.

## Cuidados na integração

Preservar a coleta PNCP existente em `src/fetch_corpus.py`.
Não incluir `data/raw/` no GitHub.
