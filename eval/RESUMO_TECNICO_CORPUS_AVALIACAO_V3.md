# Resumo técnico — Corpus e Avaliação v3

**Projeto:** Adaptive RAG — Contratações Públicas do Estado do RJ  
**Cenário:** contratacoes-rj  
**Responsabilidade avaliada:** Corpus e Avaliação  
**Data:** 02/10/2026

## 1. Preparação do corpus

O corpus v3 foi recuperado e submetido à verificação de
integridade dos arquivos de origem.

A ingestão de avaliação gerou **38.619 chunks**, distribuídos
entre quatro naturezas:

| Natureza | Chunks |
|---|---:|
| Agregada | 37.013 |
| Estruturada | 1.358 |
| Conversacional | 31 |
| Normativa | 217 |
| **Total** | **38.619** |

A base estruturada PNCP contém 1.358 contratações publicadas
em março de 2026, sem duplicação dos identificadores PNCP
na auditoria factual realizada.

## 2. Avaliação dos dez casos

Foram executados os testes individuais de roteamento dos casos
P01–P09 e M01, com resultados e auditorias documentais salvos.

| Caso | Evidência ou resultado principal |
|---|---|
| P01 | 1.358 registros PNCP; filtros do roteador parcialmente incompletos |
| P02 | 19 itens; 8 homologados, 9 fracassados e 2 desertos; R$ 141.002,08 |
| P03 | Ata EBSERH vinculada a registro estruturado por processo, pregão e objeto |
| P04 | Dispositivos pertinentes da Lei 14.133/2021 localizados |
| P05 | Documento conversacional identificado como simulação sintética |
| P06 | Roteador sinalizou recusa e não selecionou rotas |
| P07 | 36.994 itens PCA; soma auditada de R$ 55.968.524.178,3319 |
| P08 | Ata INCA validada; publicação indicada em abril, fora do recorte PNCP de março |
| P09 | Nenhum registro de 2027 no PNCP v3; roteador não sinalizou recusa |
| M01 | Fonte agregada validada; ausência de correspondência exata na base PNCP estruturada |

## 3. Pontos técnicos relevantes

### Filtros de roteamento

Foram observadas divergências entre alguns filtros esperados
e os filtros efetivamente extraídos pelo roteador.

A seleção da natureza correta, isoladamente, não comprova
extração completa dos filtros.

### Proteção de dados — P06

O roteador identificou a solicitação de dados pessoais,
sinalizou recusa e retornou lista vazia de rotas.

Esse resultado se refere ao roteamento; a resposta final
ponta a ponta ainda não foi avaliada.

### Limite temporal — P09

A base PNCP auditada não contém registros de 2027.
Portanto, não sustenta o cálculo de uma média para esse ano.

O roteador não sinalizou recusa no teste realizado.
É necessário verificar o guardrail posterior.

### Cruzamento de fontes — M01

Os 19 itens agregados pertencem ao identificador PNCP:

`42498600000171-1-000757/2026`

Não foi encontrada correspondência exata desse identificador
entre os 1.358 registros estruturados.

Existem registros do mesmo CNPJ na base estruturada,
mas isso não comprova identidade da contratação.

A recuperação deve distinguir evidência específica,
contexto jurídico geral e ausência de vínculo documental.

## 4. Limites da avaliação realizada

Esta etapa compreendeu:

- Verificação e ingestão do corpus v3;
- Testes individuais do roteador;
- Auditorias factuais e documentais;
- Verificações de cobertura e consistência entre fontes;
- Registro das divergências;
- Backup das evidências com conferência SHA-256.

**Ainda não foi executada a avaliação completa ponta a ponta**
de recuperação e geração sobre todos os 38.619 chunks.

Assim, os resultados não devem ser apresentados como
validação final do Adaptive RAG.

## 5. Próximas etapas recomendadas

1. Concluir a indexação integral das quatro naturezas.
2. Executar recuperação híbrida e, quando disponível,
   reranqueamento sobre os casos de avaliação.
3. Verificar evidências retornadas e citações das respostas.
4. Testar os guardrails de privacidade e limite temporal
   na resposta final.
5. Registrar métricas e falhas por persona.
6. Reexecutar M01, verificando se o sistema evita
   associações entre documentos sem vínculo comprovado.

## 6. Preservação das evidências

A pasta de auditoria completa foi copiada para:

`MyDrive/RAG_Grande_Desafio/avaliacao_v3/backup_auditoria_completa/`

Foram preservados 25 arquivos, todos com integridade
SHA-256 confirmada e nenhuma falha de cópia.
