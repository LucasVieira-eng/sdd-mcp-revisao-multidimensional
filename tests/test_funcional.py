"""
Testes funcionais de cenários de negócio para o cálculo de frete no checkout.

Especificação: specs/checkout_frete.md
Casos de Teste:
- CT-F01: Cliente do Brasil adiciona um item de R$ 10,00 e cruza o limite do frete grátis (REQ-01, REQ-02).
- CT-F02: Mesmo carrinho de R$ 100,00 comprado por clientes de países diferentes (REQ-03, REQ-04, REQ-05, RB-06).
"""

import json
from pathlib import Path
import pytest
from src.frete import calcular_total


class TestFuncionalCheckoutFrete:
    """Suíte de testes funcionais para cenários de negócio do checkout de frete."""

    def test_ct_f01_cliente_brasil_cruza_limite_frete_gratis(self) -> None:
        """
        CT-F01 (REQ-01, REQ-02):
        Cenário de negócio: Cliente do Brasil adiciona um item de R$ 10,00 e cruza o limite do frete grátis.
        Pré-condição: country_rules.json real do repositório.
        Passos:
          1) calcular_total(240.00, "BR")
          2) calcular_total(250.00, "BR")
          frete = total - subtotal
        Resultado esperado:
          1) total 255.00, frete 15.00
          2) total 250.00, frete 0.00
        """
        # Passo 1: Subtotal de R$ 240,00 no Brasil (abaixo do limite de R$ 250,00)
        subtotal_1 = 240.00
        total_1 = calcular_total(subtotal_1, "BR")
        frete_1 = total_1 - subtotal_1

        assert total_1 == pytest.approx(255.00, abs=1e-2), "Total para subtotal 240.00 deve ser 255.00"
        assert frete_1 == pytest.approx(15.00, abs=1e-2), "Frete para subtotal 240.00 deve ser 15.00"

        # Passo 2: Cliente adiciona item de R$ 10,00 -> subtotal de R$ 250,00 (atinge frete grátis)
        subtotal_2 = 250.00
        total_2 = calcular_total(subtotal_2, "BR")
        frete_2 = total_2 - subtotal_2

        assert total_2 == pytest.approx(250.00, abs=1e-2), "Total para subtotal 250.00 deve ser 250.00"
        assert frete_2 == pytest.approx(0.00, abs=1e-2), "Frete para subtotal 250.00 deve ser 0.00"

    def test_ct_f02_mesmo_carrinho_clientes_paises_diferentes(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """
        CT-F02 (REQ-03, REQ-04, REQ-05, RB-06):
        Cenário de negócio: Mesmo carrinho de R$ 100,00 comprado por clientes de países diferentes.
        Pré-condição: Arquivo de regras temporário com BR sem taxa e US com 'taxa': 0.10.
        Passos:
          Calcular o total do carrinho para BR, JP e US.
        Resultado esperado:
          - BR: 115,00 (subtotal 100 + frete 15, regra configurada sem taxa)
          - JP: 115,00 (subtotal 100 + frete 15, país sem regra - REQ-05)
          - US: 126,50 (subtotal 100 + frete 15 = 115; taxa de 10% sobre total = 126,50 - REQ-04, RB-06)
        """
        # Pré-condição: Criação do arquivo temporário com regras para BR e US
        regras_teste = {
            "schema_version": "1.0",
            "country_code_standard": "ISO 3166-1 alpha-2",
            "countries": {
                "BR": {
                    "country_name": "Brasil",
                    "enabled": True,
                    "rule_id": "RULE-BR-001",
                    "rule_type": "standard",
                    "parameters": {},
                },
                "US": {
                    "country_name": "Estados Unidos",
                    "enabled": True,
                    "rule_id": "RULE-US-001",
                    "rule_type": "tax_rate",
                    "taxa": 0.10,
                    "parameters": {
                        "taxa": 0.10,
                    },
                },
            },
        }

        temp_rules_file = tmp_path / "country_rules.json"
        temp_rules_file.write_text(json.dumps(regras_teste), encoding="utf-8")

        # Configura o módulo para utilizar o arquivo de regras temporário
        monkeypatch.setattr("src.frete.RULES_PATH", temp_rules_file)

        subtotal = 100.00

        # 1) Cliente do Brasil: regra configurada sem taxa adicional
        total_br = calcular_total(subtotal, "BR")
        assert total_br == pytest.approx(115.00, abs=1e-2), "Total para BR deve ser 115.00"

        # 2) Cliente do Japão: país sem regra configurada no arquivo (REQ-05)
        total_jp = calcular_total(subtotal, "JP")
        assert total_jp == pytest.approx(115.00, abs=1e-2), "Total para JP deve ser 115.00"

        # 3) Cliente dos Estados Unidos: regra configurada com taxa de 10% sobre o total (RB-06)
        total_us = calcular_total(subtotal, "US")
        assert total_us == pytest.approx(126.50, abs=1e-2), "Total para US deve ser 126.50"
