# Validação da coleta do corpus

## Escopo conferido

- PNCP, RJ, pregão eletrônico, março de 2026: v1 e v2 em JSON legível, com 1.358 registros cada.
- Lei nº 14.133/2021: arquivo HTML presente.
- Atas: três PDFs legíveis, totalizando 30 páginas.
- Comunicações sintéticas: TXT legível, com três mensagens identificadas e aviso de simulação.

## Comparação do PNCP

Os inventários `data/inventory/v1.json` e `data/inventory/v2.json`
registram as duas coletas. O relatório `data/inventory/DIFF_v1_v2.md`
documenta os mesmos 1.358 IDs nas duas versões e sete registros
com alterações de conteúdo. O relatório não atribui causa às alterações.

## Armazenamento

Os dados brutos estão em `data/raw/`, que não deve ser enviado ao GitHub.
A coleta v2 foi preservada separadamente da v1.

## Verificações ainda pendentes

- Conferir a redação vigente da lei na fonte oficial.
- Conferir a correspondência de cada PDF com sua fonte oficial no PNCP.
- Verificar e mascarar dados pessoais de contato antes de disponibilizar
  trechos das atas nas respostas do RAG.
- Confirmar que a equipe dispõe de cópia de segurança de todos os dados
  brutos, não apenas do JSON da v2.
