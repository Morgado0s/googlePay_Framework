from dataclasses import dataclass, field
from typing import List, Dict, Any
from decimal import Decimal

class GooglePayError(Exception):
    """Base exception for Google Pay framework"""
    pass

class PaymentValidationError(GooglePayError):
    """Raised when payment data validation fails"""
    pass

@dataclass
class GooglePayConfig:
    # Configurações obrigatórias
    merchant_id: str
    merchant_name: str
    
    # Configurações do gateway
    gateway_name: str = "example"
    environment: str = "TEST"  # TEST ou PRODUCTION
    
    # Configurações de pagamento
    currency_code: str = "BRL"  # Padrão para Real
    country_code: str = "BR"    # Padrão para Brasil
    total_price: Decimal = field(default_factory=lambda: Decimal("0.00"))
    
    # Configurações de cartões
    allowed_card_networks: List[str] = field(
        default_factory=lambda: ["VISA", "MASTERCARD", "ELO", "AMEX"]
    )
    allowed_auth_methods: List[str] = field(
        default_factory=lambda: ["PAN_ONLY", "CRYPTOGRAM_3DS"]
    )

    def update_price(self, price: str | float | Decimal) -> None:
        """Atualiza o preço total da transação"""
        self.total_price = Decimal(str(price))

    def add_card_network(self, network: str) -> None:
        """Adiciona uma nova bandeira de cartão"""
        if network not in self.allowed_card_networks:
            self.allowed_card_networks.append(network)

    def remove_card_network(self, network: str) -> None:
        """Remove uma bandeira de cartão"""
        if network in self.allowed_card_networks:
            self.allowed_card_networks.remove(network)

    def set_currency(self, currency_code: str, country_code: str = None) -> None:
        """Atualiza a moeda e opcionalmente o país"""
        self.currency_code = currency_code.upper()
        if country_code:
            self.country_code = country_code.upper()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "apiVersion": 2,
            "apiVersionMinor": 0,
            "merchantInfo": {
                "merchantId": self.merchant_id,
                "merchantName": self.merchant_name
            },
            "allowedPaymentMethods": [{
                "type": "CARD",
                "parameters": {
                    "allowedAuthMethods": self.allowed_auth_methods,
                    "allowedCardNetworks": self.allowed_card_networks
                },
                "tokenizationSpecification": {
                    "type": "PAYMENT_GATEWAY",
                    "parameters": {
                        "gateway": self.gateway_name,
                        "gatewayMerchantId": self.merchant_id
                    }
                }
            }]
        } 