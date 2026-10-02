"""Módulo de cálculo de frete do checkout conforme specs/checkout_frete.md."""


def calcular_total(subtotal: float) -> float:
    """
    Calcula o valor total do carrinho incluindo o frete.

    Cláusulas da especificação:
    - REQ-01: Adiciona taxa de frete padrão de R$ 15,00 ao subtotal.
    - REQ-02: Concede frete grátis (taxa = R$ 0,00) se subtotal >= R$ 200,00.
    """
    # REQ-02: Frete grátis para subtotal >= 200,00
    if subtotal >= 200.0:
        return subtotal

    # REQ-01: Taxa padrão de R$ 15,00
    return subtotal + 15.0
