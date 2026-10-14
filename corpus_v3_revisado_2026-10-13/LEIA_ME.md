# Corpus v3 revisado — 13/10/2026

Pacote com dados v3 conferidos e índices alinhados.
A avaliação integrada do RAG com este pacote ainda está pendente.

## Restaurar no repositório

Copie data/raw/v3, data/processed e data/indices
para os destinos correspondentes do repositório.
Preserve um backup dos artefatos anteriores.
Utilize os chunks, IDs e índices deste mesmo pacote.

## Embeddings e cache

Os 2.125 vetores foram reutilizados após conferir
identidade, texto e correspondência com o cache anterior.
44 possuem modelo registrado; 2.081 são históricos
e não possuem modelo comprovado.

cache_embeddings.json: cache por hash, com 44 entradas
associadas ao modelo comprovado.
cache_embeddings_historico_por_id.json: 2.125 vetores
por ID, acompanhados de embedding_provenance.json.

Para restaurar e consultar, não execute novamente a indexação.
Executar o indexador pode solicitar 2.081 novos embeddings.

Consulte RELATORIO_DO_PACOTE.json e documentacao/.
