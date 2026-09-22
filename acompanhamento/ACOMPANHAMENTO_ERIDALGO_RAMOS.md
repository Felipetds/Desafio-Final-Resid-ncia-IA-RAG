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

### Atualização — 22/09/2026

**Status das Entregas (Ordens 2 e 3):**
* **Pipeline:** Ingestão adaptada para as 4 bases. Ingestão real da base estruturada (PNCP) concluída (1358 registros).
* **Otimização:** Cache de embeddings em disco comprovado e validado. Pausa de 10s e lotes de 50 respeitados.
* **Pendência Externa:** Aguardando a conclusão da Ordem 1 pela Janice para substituir as fixtures das bases normativa, conversacional e agregada.
* Código liberado para testes de integração.
