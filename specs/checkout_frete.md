# Requisitos Funcionais

*   **REQ-01** (Ubiquitous): THE SYSTEM SHALL calcular o valor total adicionando a taxa de frete padrão de R$ 15,00 ao subtotal do
carrinho.
*   **REQ-02** (IF/THEN): IF o subtotal do carrinho for maior ou igual a R\$ 250,00, THEN THE SYSTEM SHALL conceder frete gratis (taxa = R$ 0,00).
*   **REQ-03** (Ubiquitous): THE SYSTEM SHALL identificar o país de origem do usuário utilizando a norma ISO 3166-1 alpha-2.
*   **REQ-04** (Event-driven): WHEN o país de origem do usuário for identificado, o sistema SHALL selecionar e aplicar a regra de negócio correspondente ao país identificado no arquivo country_rules.json.
*   **REQ-05** (IF/THEN): IF não existir uma regra configurada para o país identificado, THEN o sistema SHALL não aplicar nenhuma regra de negócio.

# Requisitos de Negócio

*   **RB-06** (Event-driven): WHEN o país de origem tiver uma taxa específica, THEN THE SYSTEM SHALL aplicar essa taxa sobre o valor total