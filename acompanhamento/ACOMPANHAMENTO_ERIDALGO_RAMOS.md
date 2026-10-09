Acompanhamento – Eridalgo Ramos da Silva

Encontro 1 — 14/09/2026

Minhas

Participei das definições iniciais e assumi a responsabilidade direta pelas etapas de ingestão e indexação dos dados do Cenário 1 — Contratações Públicas do Estado do Rio de Janeiro.

Configurei o ambiente de desenvolvimento no Google Colab focado na preparação e indexação do corpus para o pipeline de recuperação.

Iniciei a integração e os testes iniciais dos métodos de busca híbrida, parametrizando o uso de FAISS para a indexação vetorial e BM25 para a indexação lexical.

Atuei na resolução de problemas de importação de bibliotecas e realizei o debugging focado na geração e salvamento correto dos índices de busca que irão alimentar o RAG.

Uso de IA

Utilizei IA como suporte para depurar erros específicos de importação no ambiente do Colab e para revisar a documentação de integração entre FAISS e BM25. Todos os scripts sugeridos foram validados, ajustados e testados por mim antes da implementação.

Resumo da equipe

A equipe organizou o repositório privado, determinou os acessos e iniciou a exploração e análise do domínio do Cenário 1, estabelecendo os primeiros passos para estruturar o fluxo de dados.

Próximos passos

Elaborar o ARQUITETURA.md.

Elaborar o PERSONAS.md.

Criar o corpus_manifest.yaml.

Definir a divisão estrutural de responsabilidades da equipe.

Encontro 2 — 16/09/2026

Minhas

Além de manter o fluxo de ingestão e indexação, avancei para a etapa de estruturação da avaliação e da interface do sistema.

Configurei e testei os scripts de avaliação do pipeline utilizando o framework LLM-as-judge, realizando integrações com a API do Groq e do Gemini para validar a precisão das recuperações geradas pelos meus índices.

Iniciei o desenvolvimento da interface gráfica do projeto utilizando Streamlit, com foco em criar um layout claro para a visualização dos resultados do RAG.

Conduzi testes de execução local da interface e estruturei os artefatos de código para o versionamento no repositório.

Uso de IA

Utilizei ferramentas de IA para consultar exemplos de requisições de API no framework de avaliação (LLM-as-judge) e para buscar referências visuais de componentes no Streamlit. Todo o código gerado foi revisado e adaptado para as necessidades específicas do nosso cenário antes do commit.

Resumo da equipe

A equipe entrou em fase de execução ativa, com progressos na coleta de dados, desenvolvimento do anonimizador de dados sensíveis em regex, definição de responsabilidades (comigo focado na ingestão/indexação), esboço da arquitetura de integração e construção do frontend do sistema.

Próximos passos

Finalizar e otimizar os scripts de ingestão de dados e criação de embeddings.

Refinar a interface no Streamlit integrando com o pipeline de busca indexado.

Apoiar a finalização técnica do ARQUITETURA.md detalhando as etapas de ingestão, indexação e avaliação.


---

### Encontro — 18/09/2026

**Minhas Atividades:**

* **Ordem 2 Concluída (`src/ingest.py`):** 
  * Implementei o script de processamento e fatiamento de documentos (*chunking*).
  * Apliquei os metadados obrigatórios do contrato do projeto (`source_file`, `doc_type`, `sensitivity: publico`, `chunk_id`, `base_id`).
  * Configurei o fluxo com suporte a *fixtures* (dados de teste estruturados) para garantir resiliência frente à instabilidade temporária do portal PNCP do RJ.

* **Ordem 3 Concluída (`src/index.py`):** 
  * Integrei a API de embeddings do modelo da residência via Ollama.
  * Implementei o processamento em lotes (*batching*) com limite de 50 chunks e controle de requisições (*rate limit* de 10 segundos).
  * Construí e persisti com sucesso os índices híbridos: **FAISS** (busca densa por similaridade vetorial) e **BM25** (busca esparsa por palavras-chave).

* **Versionamento:** 
  * Códigos-fonte devidamente versionados e enviados ao repositório remoto (`commit: 11af8b7`).


---

### Atualização — 21/09/2026 

**Minhas Atividades:**
 
  * Corrigi a estrutura de metadados no `src/ingest.py`, movendo o `chunk_id` para dentro do dicionário `metadata`.
  * Atualizei a lógica de extração de IDs no `src/index.py` para refletir o novo formato.
  * Validei a reindexação completa (FAISS e BM25) com sucesso utilizando os dados simulados (*fixtures*).
* **Versionamento:**
  * Correção validada e enviada para a branch principal (`commit: db3415d`), liberando o formato final para a criação das *fixtures* pela equipe.

### Atualização — 23/09/2026

**Status das Entregas (Integração Final do Pipeline de Ingestão e Validação do Checklist):**

* **Integração do Corpus v2 Real:** Arquivos brutos recebidos da entrega da Janice (`data/raw/v2/`) descompactados e integrados ao pipeline. Substituição completa das *fixtures* temporárias.
* **Desenvolvimento de Parsers Específicos:** Implementação de lógica de leitura adaptada para as quatro naturezas do projeto:
    * **Estruturada:** Processamento do JSON (PNCP).
    * **Normativa:** Processamento de HTML (Lei 14.133) fatiado por artigos, incluindo a criação de um *fallback* de codificação para `latin-1` para contornar problemas clássicos de `UnicodeDecodeError` em bases governamentais.
    * **Conversacional:** Leitura nativa de PDFs (atas) via `pypdf` e TXT (comunicações).
    * **Agregada:** Leitura e estruturação do CSV massivo do Rio de Janeiro.
* **Estratégia de Desenvolvimento e Rate Limiting:** Conforme alinhamento com a gestão (Eduarda), implementei um limite de amostragem determinística (500 linhas) exclusivamente na base agregada. Isso evitou o estrangulamento do *endpoint* compartilhado, preservou o CSV original para produção e viabilizou um índice rápido para a equipe.
* **Validação Rigorosa e Teste Offline (Checklist):** Injeção das chaves de metadados específicos exigidas (`uf`, `ano`, `modalidade`, `orgao`, etc.) nos *chunks*. Criação e execução de rotina de teste offline (`testes/test_metadata.py`) que validou com sucesso a presença dos metadados obrigatórios em 100% da base.
* **Conclusão:** Índice de desenvolvimento gerado com sucesso com 2.102 *chunks* englobando as quatro naturezas. Todas as pendências do checklist do professor foram resolvidas. Código final testado e com *push* na *main*, liberando a equipe (Luiz, Felipe e Calvin) para iniciar os testes de integração e recuperação (RAG).

### Atualização — 25/09/2026

**Prioridades do Encontro Resolvidas:**
* **Metadados Específicos:** Correção do preenchimento das chaves (uf, ano, modalidade, orgao, municipio, valor, fornecedor, vigencia). Extração de valores reais implementada na base estruturada do PNCP, respeitando a regra de manter vazio/nulo quando inexistente.
* **Base Agregada:** Ficheiro CSV verificado, garantindo a utilização do separador `;` e que cada linha gera um *chunk* independente. Amostra determinística de 500 registos mantida para desenvolvimento.
* **Base Conversacional e Normativa:** Fatiamento revisto nos três PDFs e no TXT (separação por parágrafos longos) e na Lei (separação por artigos).
* **Regeneração de Índices:** Scripts `ingest.py` e `index.py` reexecutados. Total de 2.102 *chunks* gerados e validados no teste *offline*.
* **Otimização:** Índices FAISS e BM25 regenerados com reaproveitamento total de cache (2.102 *embeddings* carregados localmente, 0 envios para API).
* **Status:** Chunks e índices atualizados disponibilizados para os testes de recuperação e integração da equipa.

### Atualização extra — 

**Correções na Base Agregada:**
* Tratamento do BOM (`\\ufeff`) invisível no arquivo PCA utilizando a codificação `utf-8-sig`.
* Implementação de detecção dinâmica de separadores (`,` vs `;`) para abranger diferentes padrões de exportação.
* Criação de mapeamento flexível de colunas (fallback de sinónimos para `Unidade Responsável`, `Valor Total Estimado (R$)`, `valor_total_homologado`, `Data Desejada`, etc.).
* Implementação de varredura de IDs de contratação (buscando a string `/2026`) e recortes de datas para preencher anos faltantes.

**Fatiamento de PDFs (Base Conversacional):**
* Substituição de chunks únicos gigantes (até 49 mil caracteres) por uma função de fatiamento cirúrgica (`max_chars=2000`, `overlap=200`).
* Adição do metadado `pagina` iterando pelas páginas originais do PDF, garantindo rastreabilidade para a equipa.

**Regeneração e Resultados Finais:**
* O total consolidado subiu de 2.102 para **2.125 chunks** únicos e válidos.
* O sistema de cache reaproveitou 2.098 vetores antigos e chamou a API apenas para os 27 novos recortes de PDF.
* Índices reconstruídos e 109 testes da suíte offline aprovados com sucesso.
"""

### Atualização - 28/09/26

**Atividades Realizadas:**
* Refatoração da extração de ano no `ingest.py`, substituindo recortes de string por validação estrita via Regex (formatos ISO, BR e ano exato).
* Adicionada injeção de metadado `uf: RJ` nas bases conversacionais com origem conhecida (Fiocruz e Ebserh).
* Criação e aprovação do teste offline `test_extracao_ano.py` com as asserções mínimas exigidas.
* **Bloqueio Operacional:** Em conformidade com o planeamento, a regeneração dos *chunks* e índices (`ingest.py` e `index.py`) está em modo de espera, aguardando os commits de integração do resto da equipa.

### Atualização (30/09/2026) - Estrutura Configurável de Rerank
* Criado o módulo `src/rerank.py` preparado para receber perguntas e a lista de candidatos do RRF.
* O sistema possui configuração de `fallback` para manter a ordenação original e suporta variáveis como URL, autenticação e *timeout*.
* O módulo `testes/test_rerank.py` foi implementado e 4 testes simulados (lista vazia, top_k, timeout e manutenção de metadados) passaram com sucesso.
* **Nota de dependência:** A configuração `RERANK_ENABLED` está definida como `false` por defeito. A integração real no pipeline está paralisada, pois a conexão depende exclusivamente da disponibilização do endpoint pelo professor.

### Atualização (02/10/2026) - Integração do Rerank no Pipeline
* O módulo `src/rerank.py` foi ligado com sucesso ao motor principal (`src/retrieve.py`), capturando os candidatos imediatamente após a fusão RRF.
* A configuração e as variáveis de ambiente (`RERANK_ENABLED`, `RERANK_URL`, etc.) foram documentadas no código.
* Os testes locais comprovam que o pipeline continua a funcionar intacto com o rerank desativado (fallback em vigor).
* **Status de Validação:** A validação real no pipeline ponta a ponta encontra-se pendente, aguardando a disponibilização do endpoint pelo professor.

### Atualização (05/10/2026) - Preparação de Dados Estruturados
* Revistos os 1.358 registos do PNCP e implementada a normalização no `src/ingest.py` para suportar consultas estruturadas puras.
* **Mapeamento:** Adicionado suporte para `id_pncp` e `objeto`.
* **Tratamento de Datas e Valores:** Implementada a distinção entre ano da compra e data de publicação. Os valores ausentes foram tratados como nulos (`None`) em vez de convertidos para zero.
* **Integridade:** Foram mantidos os 2.125 chunks originais intactos. Não foi necessário reconstruir os embeddings.
* **Artefatos:** Gerada a base limpa `base_estruturada_normalizada.json` e o relatório de inconsistências `inconsistencias_pncp_report.json`.

### Atualização (07/10/2026) - Correção de Datas e Validação
* **Datas:** O campo `data_publicacao` foi corrigido para utilizar estritamente `dataPublicacaoPncp`. O campo `dataAtualizacao` foi preservado num campo separado. O `ano_compra` foi mantido independente.
* **Validação:** Os 1.358 registos estruturados do PNCP foram revalidados. A publicação original, os valores numéricos e a distinção entre zero e ausência foram preservados, tal como o vínculo com a fonte original. As 517 divergências decorrentes da sobreposição de datas foram resolvidas. A base normalizada afetada foi regenerada mantendo os IDs únicos (2.125 chunks no total).
* **Mapeamento:** O mapeamento dos campos normalizados e as inconsistências encontradas foram analisados e devidamente documentados.
* **Rerank:** Foi verificada a disponibilidade do endpoint de rerank do professor. Como continua indisponível, a limitação explícita e o fallback seguro no pipeline foram mantidos.


### Atualização (09/10/2026) - Alinhamento de Caches e Índices (v3)
* **19 Embeddings Pendentes:** Pertencem à base agregada do corpus v2 (arquivo `itens_pe_038_26_2026.csv`). Como não houve alterações estruturais para o v3 (confirmado via `DIFF_v2_v3.md`), o cache é compatível. Os embeddings permanecem pendentes por falha local. **IDs envolvidos:** `itens_pe_038_chunk_482` até `itens_pe_038_chunk_500`.
* **Validação de Cache:** Testes garantem que os IDs pertencem ao corpus, os vetores têm dimensão consistente (valores finitos), sem conflitos e correspondem ao texto.
* **Conjunto Aprovado:** Índices v2 originais + nova base estruturada normalizada.
* **Rerank:** Endpoint indisponível. Integração bloqueada e fallback ativo.
