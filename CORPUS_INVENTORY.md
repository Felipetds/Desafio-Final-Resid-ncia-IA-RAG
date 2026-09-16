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
