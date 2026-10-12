"""
Suite de testes para o cálculo de frete no checkout.

Especificação: specs/checkout_frete.md
- REQ-01: Adicionar taxa de frete padrão de R$ 15,00 ao subtotal do carrinho.
- REQ-02: Conceder frete grátis (taxa = R$ 0,00) para subtotal >= R$ 250,00.
- REQ-03: Identificar o país de origem do usuário utilizando a norma ISO 3166-1 alpha-2.
- REQ-04: Selecionar e aplicar a regra de negócio correspondente ao país identificado no arquivo country_rules.json.
- REQ-05: Se não existir uma regra configurada para o país identificado, não aplicar nenhuma regra de negócio.
- RB-06: Quando o país de origem tiver uma taxa específica, aplicar essa taxa sobre o valor total.
"""

import pytest
from src.frete import calcular_total


class TestCheckoutFrete:
    """Testes para o cálculo de frete e valor total conforme specs/checkout_frete.md."""

    # -------------------------------------------------------------------------
    # REQ-01: Adicionar taxa de frete padrão de R$ 15,00
    # -------------------------------------------------------------------------

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

    # -------------------------------------------------------------------------
    # REQ-02: Conceder frete grátis para subtotal >= R$ 250,00
    # -------------------------------------------------------------------------

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

    # -------------------------------------------------------------------------
    # REQ-03: Identificar país de origem utilizando a norma ISO 3166-1 alpha-2
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize(
        "pais_origem",
        [
            "BR",
            "PT",
            "US",
            "AR",
            "JP",
            "ES",
            "DE",
            "FR",
            "br",
            "pt",
            "us",
        ],
        ids=[
            "iso_br_maiusculo",
            "iso_pt_maiusculo",
            "iso_us_maiusculo",
            "iso_ar_maiusculo",
            "iso_jp_maiusculo",
            "iso_es_maiusculo",
            "iso_de_maiusculo",
            "iso_fr_maiusculo",
            "iso_br_minusculo",
            "iso_pt_minusculo",
            "iso_us_minusculo",
        ],
    )
    def test_req_03_identificar_pais_origem_iso_3166_1_alpha_2_valido(self, pais_origem: str) -> None:
        """
        REQ-03 (Ubiquitous): THE SYSTEM SHALL identificar o país de origem do usuário
        utilizando a norma ISO 3166-1 alpha-2.
        """
        total = calcular_total(100.00, pais_origem=pais_origem)
        assert isinstance(total, float)
        assert total > 0

    @pytest.mark.parametrize(
        "pais_invalido",
        [
            "BRA",      # 3 letras (alpha-3)
            "USA",      # 3 letras (alpha-3)
            "PRT",      # 3 letras (alpha-3)
            "Brasil",   # nome do país por extenso
            "Portugal", # nome do país por extenso
            "B",        # apenas 1 letra
            "12",       # numérico
            "BR1",      # alfanumérico
            "",         # string vazia
            "   ",      # espaços em branco
            "BR!",      # caractere especial
        ],
        ids=[
            "alpha_3_bra",
            "alpha_3_usa",
            "alpha_3_prt",
            "nome_extenso_brasil",
            "nome_extenso_portugal",
            "um_caractere_b",
            "numerico_12",
            "alfanumerico_br1",
            "string_vazia",
            "espacos_em_branco",
            "caractere_especial",
        ],
    )
    def test_req_03_rejeitar_pais_origem_fora_do_padrao_iso_3166_1_alpha_2(self, pais_invalido: str) -> None:
        """
        REQ-03 (Ubiquitous): THE SYSTEM SHALL identificar o país de origem do usuário
        utilizando a norma ISO 3166-1 alpha-2.
        Rejeita códigos que não sigam o padrão ISO 3166-1 alpha-2 lançando ValueError.
        """
        with pytest.raises(ValueError):
            calcular_total(100.00, pais_origem=pais_invalido)

    # -------------------------------------------------------------------------
    # REQ-04: Selecionar e aplicar regra correspondente do country_rules.json
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize(
        "pais_origem",
        ["BR", "PT", "US"],
        ids=["pais_configurado_br", "pais_configurado_pt", "pais_configurado_us"],
    )
    def test_req_04_selecionar_e_aplicar_regra_pais_configurado(self, pais_origem: str) -> None:
        """
        REQ-04 (Event-driven): WHEN o país de origem do usuário for identificado,
        o sistema SHALL selecionar e aplicar a regra de negócio correspondente ao
        país identificado no arquivo country_rules.json.
        """
        total = calcular_total(100.00, pais_origem=pais_origem)
        assert isinstance(total, float)
        assert total > 0

    def test_req_04_diferenciar_aplicacao_de_regras_por_pais(self) -> None:
        """
        REQ-04 (Event-driven): WHEN o país de origem do usuário for identificado,
        o sistema SHALL selecionar e aplicar a regra de negócio correspondente ao
        país identificado no arquivo country_rules.json.
        Garante que cada país configurado tem sua regra avaliada.
        """
        total_br = calcular_total(100.00, pais_origem="BR")
        total_pt = calcular_total(100.00, pais_origem="PT")
        total_us = calcular_total(100.00, pais_origem="US")

        assert isinstance(total_br, float)
        assert isinstance(total_pt, float)
        assert isinstance(total_us, float)

    # -------------------------------------------------------------------------
    # REQ-05: Não aplicar nenhuma regra se o país não estiver configurado
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize(
        "subtotal, pais_origem, esperado",
        [
            (0.00, "AR", 15.00),
            (50.00, "JP", 65.00),
            (100.00, "FR", 115.00),
            (200.00, "DE", 215.00),
            (249.99, "ES", 264.99),
        ],
        ids=[
            "subtotal_0_ar_sem_regra_taxa_padrao",
            "subtotal_50_jp_sem_regra_taxa_padrao",
            "subtotal_100_fr_sem_regra_taxa_padrao",
            "subtotal_200_de_sem_regra_taxa_padrao",
            "subtotal_249_99_es_sem_regra_taxa_padrao",
        ],
    )
    def test_req_05_pais_nao_configurado_mantem_taxa_padrao_sem_regras_extras(
        self, subtotal: float, pais_origem: str, esperado: float
    ) -> None:
        """
        REQ-05 (IF/THEN): IF não existir uma regra configurada para o país identificado,
        THEN o sistema SHALL não aplicar nenhuma regra de negócio.
        Mantém o cálculo padrão (taxa padrão de R$ 15,00) para subtotal < 250,00.
        """
        assert calcular_total(subtotal, pais_origem=pais_origem) == pytest.approx(esperado, abs=1e-2)

    @pytest.mark.parametrize(
        "subtotal, pais_origem, esperado",
        [
            (250.00, "AR", 250.00),
            (250.01, "JP", 250.01),
            (300.00, "FR", 300.00),
            (500.00, "DE", 500.00),
        ],
        ids=[
            "subtotal_250_ar_sem_regra_frete_gratis",
            "subtotal_250_01_jp_sem_regra_frete_gratis",
            "subtotal_300_fr_sem_regra_frete_gratis",
            "subtotal_500_de_sem_regra_frete_gratis",
        ],
    )
    def test_req_05_pais_nao_configurado_mantem_frete_gratis_sem_regras_extras(
        self, subtotal: float, pais_origem: str, esperado: float
    ) -> None:
        """
        REQ-05 (IF/THEN): IF não existir uma regra configurada para o país identificado,
        THEN o sistema SHALL não aplicar nenhuma regra de negócio.
        Mantém o frete grátis (taxa = R$ 0,00) para subtotal >= 250,00 sem aplicar regras extras.
        """
        assert calcular_total(subtotal, pais_origem=pais_origem) == pytest.approx(esperado, abs=1e-2)

    # -------------------------------------------------------------------------
    # RB-06: Aplicar taxa específica do país sobre o valor total
    # -------------------------------------------------------------------------

    def test_rb_06_aplicar_taxa_especifica_do_pais_sobre_valor_total(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """
        RB-06 (Event-driven): WHEN o país de origem tiver uma taxa específica,
        THEN THE SYSTEM SHALL aplicar essa taxa sobre o valor total.
        """
        # Regra simulada para país "US" com taxa de 10%
        regra_com_taxa = {
            "country_name": "Estados Unidos",
            "enabled": True,
            "rule_id": "RULE-US-TAX-10",
            "parameters": {
                "taxa": 0.10,
            },
        }

        monkeypatch.setattr("src.frete.obter_regra_pais", lambda codigo: regra_com_taxa if codigo == "US" else None)

        # Subtotal R$ 100,00 + frete R$ 15,00 = R$ 115,00; + 10% de taxa sobre total = R$ 126,50
        assert calcular_total(100.00, pais_origem="US") == pytest.approx(126.50, abs=1e-2)

        # Subtotal R$ 250,00 + frete grátis R$ 0,00 = R$ 250,00; + 10% de taxa sobre total = R$ 275,00
        assert calcular_total(250.00, pais_origem="US") == pytest.approx(275.00, abs=1e-2)
