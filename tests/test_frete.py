"""
Suite de testes para o cálculo de frete no checkout.

Especificação: specs/checkout_frete.md
- REQ-01: Adicionar taxa de frete padrão de R$ 15,00 ao subtotal do carrinho.
- REQ-02: Conceder frete grátis (taxa = R$ 0,00) para subtotal >= R$ 250,00.
"""

import pytest
from src.frete import calcular_total


class TestCheckoutFrete:
    """Testes para o cálculo de frete e valor total conforme specs/checkout_frete.md."""

    @pytest.mark.parametrize(
        "subtotal, esperado",
        [
            (0.00, 15.00),
            (50.00, 65.00),
            (100.00, 115.00),
            (200.00, 215.00),
            (249.99, 264.99),
        ],
        ids=[
            "subtotal_zero_taxa_padrao",
            "subtotal_50_taxa_padrao",
            "subtotal_100_taxa_padrao",
            "subtotal_200_taxa_padrao",
            "subtotal_limite_inferior_249_99_taxa_padrao",
        ],
    )
    def test_req_01_calcular_valor_total_com_taxa_padrao(self, subtotal: float, esperado: float) -> None:
        """
        REQ-01 (Ubiquitous): THE SYSTEM SHALL calcular o valor total
        adicionando a taxa de frete padrão de R$ 15,00 ao subtotal do carrinho.
        """
        assert calcular_total(subtotal) == pytest.approx(esperado, abs=1e-2)

    @pytest.mark.parametrize(
        "subtotal, esperado",
        [
            (250.00, 250.00),
            (250.01, 250.01),
            (300.00, 300.00),
            (500.00, 500.00),
        ],
        ids=[
            "subtotal_limite_exato_250_frete_gratis",
            "subtotal_limite_superior_250_01_frete_gratis",
            "subtotal_300_frete_gratis",
            "subtotal_500_frete_gratis",
        ],
    )
    def test_req_02_conceder_frete_gratis_subtotal_maior_ou_igual_250(self, subtotal: float, esperado: float) -> None:
        """
        REQ-02 (IF/THEN): IF o subtotal do carrinho for maior ou igual a R$ 250,00,
        THEN THE SYSTEM SHALL conceder frete gratis (taxa = R$ 0,00).
        """
        assert calcular_total(subtotal) == pytest.approx(esperado, abs=1e-2)
