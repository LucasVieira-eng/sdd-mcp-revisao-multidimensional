"""Módulo de cálculo de frete do checkout conforme specs/checkout_frete.md."""

import json
from pathlib import Path

RULES_PATH = Path(__file__).parent / "country_rules.json"


def carregar_regras_paises() -> dict:
    """Carrega o arquivo de regras de negócio por país (country_rules.json)."""
    if RULES_PATH.exists():
        with open(RULES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def identificar_pais_origem(pais_origem: str) -> str:
    """
    Identifica e valida o país de origem segundo a norma ISO 3166-1 alpha-2.

    Cláusula da especificação:
    - REQ-03 (Ubiquitous): THE SYSTEM SHALL identificar o país de origem do usuário
      utilizando a norma ISO 3166-1 alpha-2.
    """
    if not isinstance(pais_origem, str):
        raise ValueError("País de origem deve ser uma string no padrão ISO 3166-1 alpha-2.")

    codigo_normalizado = pais_origem.strip().upper()
    if len(codigo_normalizado) != 2 or not codigo_normalizado.isalpha():
        raise ValueError(
            f"País de origem '{pais_origem}' inválido. Deve seguir a norma ISO 3166-1 alpha-2."
        )

    return codigo_normalizado


def obter_regra_pais(codigo_pais: str) -> dict | None:
    """
    Obtém a regra de negócio configurada para o país no arquivo country_rules.json.

    Cláusulas da especificação:
    - REQ-04 (Event-driven): WHEN o país de origem do usuário for identificado, o sistema
      SHALL selecionar e aplicar a regra de negócio correspondente ao país identificado
      no arquivo country_rules.json.
    - REQ-05 (IF/THEN): IF não existir uma regra configurada para o país identificado,
      THEN o sistema SHALL não aplicar nenhuma regra de negócio.
    """
    regras_data = carregar_regras_paises()
    paises = regras_data.get("countries", {})
    return paises.get(codigo_pais)


def aplicar_regra_negocio(total: float, regra_pais: dict | None) -> float:
    """
    Aplica a regra de negócio do país ao valor total calculado.

    Cláusulas da especificação:
    - REQ-04 (Event-driven): Seleciona e aplica a regra correspondente de country_rules.json.
    - REQ-05 (IF/THEN): Se não existir regra configurada, não aplica nenhuma regra de negócio.
    - RB-06 (Event-driven): WHEN o país de origem tiver uma taxa específica,
      THEN THE SYSTEM SHALL aplicar essa taxa sobre o valor total.
    """
    # REQ-05: Se não existir regra configurada para o país, não aplica nenhuma regra
    if not regra_pais or not regra_pais.get("enabled", True):
        return total

    # RB-06: Se o país tiver taxa específica, aplica sobre o valor total
    parametros = regra_pais.get("parameters", {})
    taxa = regra_pais.get("taxa") or parametros.get("taxa") or parametros.get("taxa_especifica")
    if taxa is not None and isinstance(taxa, (int, float)):
        aliquota = taxa if taxa <= 1.0 else (taxa / 100.0)
        total += total * aliquota

    return total


def calcular_total(subtotal: float, pais_origem: str = "BR") -> float:
    """
    Calcula o valor total do carrinho incluindo o frete e regras de país.

    Cláusulas da especificação:
    - REQ-01: Adiciona taxa de frete padrão de R$ 15,00 ao subtotal do carrinho.
    - REQ-02: Concede frete grátis (taxa = R$ 0,00) se subtotal >= R$ 250,00.
    - REQ-03: Identifica o país de origem do usuário utilizando a norma ISO 3166-1 alpha-2.
    - REQ-04: Seleciona e aplica a regra de negócio correspondente no arquivo country_rules.json.
    - REQ-05: Se não existir uma regra configurada para o país identificado, não aplica nenhuma regra.
    - RB-06: Aplica taxa específica do país sobre o valor total ao final das operações.
    """
    # REQ-03: Identificação do país de origem segundo a norma ISO 3166-1 alpha-2
    codigo_pais = identificar_pais_origem(pais_origem)

    # REQ-02: Frete grátis para subtotal >= 250,00
    if subtotal >= 250.0:
        total = subtotal
    else:
        # REQ-01: Taxa padrão de R$ 15,00
        total = subtotal + 15.0

    # REQ-04 e REQ-05: Seleção de regra de negócio do país em country_rules.json
    regra_pais = obter_regra_pais(codigo_pais)

    # RB-06: Aplicação de taxa específica sobre o valor total
    total = aplicar_regra_negocio(total, regra_pais)

    return total
