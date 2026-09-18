# Corpus Inventory

## Base estruturada — PNCP

### Identificação

- **Cenário:** Contratações Públicas do Estado do Rio de Janeiro
- **Base:** Estruturada
- **Fonte:** Portal Nacional de Contratações Públicas (PNCP)
- **API:** Consulta PNCP
- **Endpoint:** `/v1/contratacoes/publicacao`
- **UF:** RJ
- **Modalidade:** 6 — Pregão Eletrônico
- **Período consultado:** 01/03/2026 a 31/03/2026
- **Total de registros:** 1.358
- **Registros duplicados:** 0

### Integridade

- **Primeira publicação encontrada:** 02/03/2026 07:00:59
- **Última publicação encontrada:** 31/03/2026 16:54:47
- **IDs PNCP encontrados:** 1.358
- **IDs PNCP únicos:** 1.358
- **UFs encontradas:** RJ
- **Modalidades encontradas:** 6

### Dados brutos

Os dados brutos foram coletados e armazenados localmente em:

`data/raw/v1/estruturada/pncp/rj/pregao_eletronico/2026-03/contratacoes_publicacao.json`

A pasta `data/raw/` está configurada no `.gitignore` e não deve ser versionada no GitHub.

### Principais informações disponíveis

Os registros coletados incluem informações como:

- órgão/entidade;
- CNPJ do órgão;
- unidade administrativa;
- município;
- objeto da contratação;
- modalidade;
- número da compra;
- número de controle PNCP;
- valores estimado e homologado;
- datas de publicação e atualização;
- situação da contratação;
- fornecedor e demais informações disponíveis no retorno da API.

### Observação

Este inventário documenta o recorte oficial utilizado para a base estruturada do projeto.

    
## Base normativa — Lei 14.133/2021

### Identificação

- **Cenário:** Contratações Públicas do Estado do Rio de Janeiro
- **Base:** Normativa
- **Documento:** Lei nº 14.133, de 1º de abril de 2021
- **Título:** Lei de Licitações e Contratos Administrativos
- **Fonte:** Presidência da República — Planalto
- **Formato coletado:** HTML
- **Arquivo bruto:** `data/raw/v1/normativa/federal/lei_14133_2021/lei_14133_2021.html`

### Verificação

- **Status HTTP na coleta:** 200
- **Tamanho do arquivo:** 649.705 bytes
- **Texto extraído:** 289.010 caracteres
- **Identificação do documento:** confirmada

### Observação

O documento foi coletado diretamente da fonte oficial do Governo Federal e armazenado na área de dados brutos do projeto. A página preserva as referências e indicações de alterações e regulamentações disponibilizadas na fonte oficial.

    
## Base conversacional — Ata de Registro de Preços

### Identificação

- **Cenário:** Contratações Públicas do Estado do Rio de Janeiro
- **Base:** Conversacional
- **Fonte:** Portal Nacional de Contratações Públicas (PNCP)
- **Órgão:** Fundação Oswaldo Cruz — INCQS/FIOCRUZ
- **CNPJ do órgão:** 33.781.055/0020-06
- **Ano da contratação:** 2026
- **Sequencial da contratação:** 227
- **Ata:** nº 00001
- **Objeto:** Aquisição de materiais da marca AGILENT
- **Formato:** PDF
- **Páginas:** 8
- **Caracteres extraídos:** 23.597
- **Arquivo bruto:** `data/raw/v1/conversacional/atas/fiocruz/2026/ata_00001.pdf`

### Conteúdo disponível

A ata contém informações sobre:

- processo administrativo;
- pregão eletrônico;
- objeto da contratação;
- itens e especificações;
- fornecedor;
- CNPJ da empresa;
- quantidades;
- valores unitários;
- condições de garantia ou validade.

### Sensibilidade

O documento contém dados de contato de pessoas físicas vinculadas ao fornecedor, como nome, e-mail e telefone.

Esses dados deverão ser tratados conforme as regras de sensibilidade e guardrails do projeto, evitando sua exposição desnecessária nas respostas do RAG.

### Verificação

- **Status HTTP:** 200
- **Tipo identificado:** PDF
- **Tamanho:** 117.978 bytes
- **Texto extraído:** confirmado


## Base conversacional — Ata INCA nº 00137/2026

### Identificação

- **Fonte:** Portal Nacional de Contratações Públicas (PNCP)
- **Órgão:** Ministério da Saúde — Instituto Nacional de Câncer (INCA)
- **CNPJ do órgão no PNCP:** 00.394.544/0001-85
- **Ano e sequencial da contratação:** 2026 / 359
- **Objeto:** Aquisição de rodízios para camas elétricas Stryker
- **Fornecedor identificado no documento:** AGIMED COMERCIO DE EQUIPAMENTOS LTDA
- **Formato:** PDF
- **Páginas:** 10
- **Caracteres extraídos:** 32.996
- **Arquivo bruto:** `data/raw/v1/conversacional/atas/ministerio_saude/2026/ata_00137.pdf`

### Verificação e sensibilidade

- **Status HTTP na coleta:** 200
- **Tipo identificado pelo conteúdo:** PDF
- **Texto extraído:** confirmado
- **Tratamento necessário:** verificar e mascarar dados pessoais de contato antes de disponibilizar trechos nas respostas do RAG.


## Base conversacional — Ata EBSERH nº 00191/2026

### Identificação

- **Fonte:** Portal Nacional de Contratações Públicas (PNCP)
- **Órgão:** Empresa Brasileira de Serviços Hospitalares (EBSERH)
- **Unidade:** Complexo Hospitalar da Universidade Federal do Rio de Janeiro (CH-UFRJ)
- **CNPJ do órgão no registro PNCP:** 15.126.437/0003-05
- **Ano e sequencial da contratação:** 2026 / 676
- **Número de controle PNCP:** `15126437000305-1-000676/2026-000001`
- **Objeto:** Aquisição de produtos para saúde — peças para mamógrafos (chassis)
- **Formato:** PDF
- **Páginas:** 12
- **Caracteres extraídos:** 49.243
- **Arquivo bruto:** `data/raw/v1/conversacional/atas/ebserh/2026/ata_00191.pdf`

### Verificação e sensibilidade

- **Status HTTP na coleta:** 200
- **Tipo identificado pelo conteúdo:** PDF
- **Tamanho:** 146.112 bytes
- **Texto extraído:** confirmado
- **Tratamento necessário:** verificar e mascarar dados pessoais, como identificadores funcionais e contatos, antes de disponibilizar trechos nas respostas do RAG.

## Base conversacional — Comunicações sintéticas

### Identificação

- **Natureza:** Conteúdo inteiramente fictício, criado para testes de RAG
- **Fonte:** Simulação produzida pela equipe com apoio de IA; não é documento do PNCP
- **Assunto:** Troca de mensagens sobre entrega de material de escritório
- **Processo fictício:** SIM-RJ-001
- **Quantidade de mensagens:** 3
- **Formato:** TXT
- **Arquivo bruto:** `data/raw/v1/conversacional/comunicacoes_sinteticas/troca_mensagens_material_escritorio_001.txt`

## Base agregada — Plano de Contratações Anual (PCA) 2026

### Identificação

* **Cenário:** Contratações Públicas do Estado do Rio de Janeiro
* **Base:** Agregada
* **Fonte:** Portal Nacional de Contratações Públicas (PNCP)
* **Órgão:** Estado do Rio de Janeiro
* **CNPJ do órgão:** 42.498.600/0001-71
* **Ano do PCA:** 2026
* **Data de publicação no PNCP:** 01/08/2025
* **Última atualização informada na consulta:** 18/09/2026
* **Formato coletado:** CSV
* **Quantidade de itens informada no portal:** 36.994
* **Valor total estimado informado no portal:** R$ 55.968.524.178,3319

### Dados brutos

O CSV foi baixado do PNCP e armazenado localmente em:

`data/raw/v1/agregada/pncp/rj/pca/2026/pca_2026_estado_rj.csv`

A pasta `data/raw/` está no `.gitignore` e não deve ser versionada no GitHub.

### Verificação

* **Tamanho do arquivo:** 14.469.918 bytes
* **Separador:** ponto e vírgula (`;`)
* **Quantidade de colunas:** 20
* **Linhas de dados no CSV:** 36.994
* **Conferência com a quantidade informada no PNCP:** coincidente

### Conteúdo disponível

O arquivo contém, entre outros campos, unidade responsável, identificação e descrição do item, quantidade estimada, valor unitário estimado, valor total estimado e data desejada.

### Observação

Este arquivo documenta a coleta do PCA de 2026. **Os valores homologados por item ainda precisam ser coletados e documentados separadamente** para completar a base agregada.


### Uso e limitações

O arquivo permite testar perguntas sobre prazos de entrega e informações
distribuídas entre mensagens. Seu conteúdo não deve ser citado como
evidência de uma contratação pública real. As respostas do RAG devem
identificá-lo explicitamente como simulação.
