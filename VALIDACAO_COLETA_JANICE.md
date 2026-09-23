# Validação da coleta e do inventário — Janice

## Verificações concluídas

- Conferência adicional da v2: o SHA-256 do arquivo `data/raw/v2/estruturada/pncp/rj/pregao_eletronico/2026-03/contratacoes_publicacao.json` corresponde ao hash registrado em `data/inventory/v2.json` (`08e28c39c44be375afe98abb94deb0b6fffd359401753a1f9eb69af54d7832aa`).
- JSON estruturado existente: 1.358 registros.
- `numeroControlePNCP`: 1.358 preenchidos e 1.358 únicos.
- `dataPublicacaoPncp`: 1.358 datas válidas, todas entre 02/03/2026 e 31/03/2026, dentro do período do manifesto (01/03/2026 a 31/03/2026).
- Inventário v2: contém os oito campos obrigatórios do contrato.
- Inventário local: 8 arquivos, distribuídos em 5 bases e 4 naturezas (estruturada, normativa, conversacional e agregada).
- `update`: criou v2 sem alterar a v1.
- Diff por SHA-256: identificou corretamente 1 arquivo modificado em teste isolado e 7 idênticos.
- Testes automatizados: 2 passaram.
- Fontes locais: os 8 arquivos previstos no manifesto foram encontrados, e os 8 hashes SHA-256 conferiram.
- Teste isolado do `update`: terminou com código de saída 0, criou a v2 com 8 arquivos e registrou 0 falhas.
- Teste das quatro categorias do diff: identificou corretamente 1 arquivo adicionado, 1 removido, 1 alterado e 1 idêntico em inventários fictícios.

## Determinismo da coleta estruturada

Foi verificado que o corpus v2 existente contém 1.358 registros e 1.358 identificadores `numeroControlePNCP` únicos.

A ordem original dos registros no JSON v2 não estava classificada por `numeroControlePNCP`. Para tornar as coletas futuras independentes da ordem em que os registros forem retornados pela API do PNCP, foi adicionada ao `src/fetch_corpus.py` uma ordenação explícita antes da gravação final:

`registros.sort(key=lambda item: item["numeroControlePNCP"])`

Um teste controlado com os mesmos registros apresentados em ordens diferentes resultou na mesma ordem final após a aplicação da regra.

A alteração passou também pela verificação de sintaxe do Python.

O corpus v2 existente não foi modificado. Seu SHA-256 permanece:

`08e28c39c44be375afe98abb94deb0b6fffd359401753a1f9eb69af54d7832aa`

Uma cópia ordenada dos 1.358 registros foi criada apenas para teste e produziu SHA-256 diferente, como esperado devido à mudança da ordem dos registros. Essa cópia não substituiu o corpus v2.

## Verificação online do PNCP

Tentativas anteriores de reconstrução online apresentaram erro HTTP 500 e timeout.

Em nova tentativa realizada em 23/09/2026, em ambiente isolado, o comando de `fetch` consultou a primeira página do PNCP com os seguintes parâmetros:

- `dataInicial`: `20260301`
- `dataFinal`: `20260331`
- `codigoModalidadeContratacao`: `6`
- `uf`: `RJ`
- `tamanhoPagina`: `50`

A API retornou HTTP 502 (Bad Gateway). O mecanismo de retentativa realizou três tentativas, com esperas progressivas, e encerrou a execução sem gerar o JSON final.

Foi preservado apenas o checkpoint de configuração em `_progresso_fetch`, contendo os mesmos parâmetros da coleta.

Como a falha ocorreu já na primeira página, nenhuma página de dados foi salva. Portanto, ainda não foi possível realizar um teste real de retomada (`--retomar`) a partir de uma página já coletada.

A reconstrução online dos 1.358 registros continua não comprovada devido às falhas observadas na API do PNCP.

## Limite dos testes

Os testes das quatro naturezas utilizaram fontes locais verificadas por SHA-256. Eles não comprovam que todas as fontes possam ser baixadas automaticamente por outra pessoa.

A coleta online completa da base estruturada também permanece dependente da disponibilidade da API do PNCP.

## Cuidados na integração

- Preservar o corpus v2 existente e seu SHA-256.
- Preservar a coleta PNCP existente em `src/fetch_corpus.py`.
- A ordenação determinística adicionada deve ser aplicada às coletas futuras, sem reescrever versões congeladas.
- Não incluir `data/raw/` no GitHub.
