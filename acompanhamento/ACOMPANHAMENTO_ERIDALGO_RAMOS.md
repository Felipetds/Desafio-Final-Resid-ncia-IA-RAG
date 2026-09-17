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
