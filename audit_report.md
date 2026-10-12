# Relatório de Auditoria e Rastreabilidade

## Requisitos e Cláusulas EARS

| Cláusula EARS | Status | Teste Coberto | Arquivo:linha |
| -------- | -------- | -------- | -------- |
| REQ-01  | Sim  | test_frete.py:44  | frete.py:100 |
| REQ-02  | Sim  | test_frete.py:68  | frete.py:96  |
| REQ-03  | Sim  | test_frete.py:112 | frete.py:19  |
| REQ-04  | Sim  | test_frete.py:175 | frete.py:38  |
| REQ-05  | Sim  | test_frete.py:222 | frete.py:60  |
| RB-06   | Sim  | test_frete.py:261 | frete.py:64  |

## Casos de Teste Funcionais

| ID | Req. | Cenário de negócio | Pré-condição | Passos | Resultado esperado | Status | Teste |
| -- | ---- | ------------------ | ------------ | ------ | ------------------ | ------ | ----- |
| CT-F01 | REQ-01, REQ-02 | Cliente do Brasil adiciona um item de R$ 10,00 e cruza o limite do frete grátis | `country_rules.json` real do repositório | 1) `calcular_total(240.00, "BR")`; 2) `calcular_total(250.00, "BR")`; frete = total − subtotal | 1) total 255,00, frete 15,00. 2) total 250,00, frete 0,00 | Passou | test_funcional.py:18 |
| CT-F02 | REQ-03, REQ-04, REQ-05, RB-06 | Mesmo carrinho de R$ 100,00 comprado por clientes de países diferentes | arquivo de regras temporário com BR sem taxa e US com `"taxa": 0.10` | calcular o total do carrinho para BR, JP e US | BR 115,00; JP 115,00 (país sem regra); US 126,50 (taxa de 10% sobre o total) | Passou | test_funcional.py:46 |
