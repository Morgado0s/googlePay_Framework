from flask import Flask, request, jsonify, render_template
from typing import Dict
from .config import GooglePayConfig
from .exceptions import PaymentValidationError

class GooglePayProcessor:
    def __init__(self, config: GooglePayConfig):
        self.config = config
        self.app = Flask(__name__, 
                        template_folder='templates')
        self._register_routes()

    def _register_routes(self):
        self.app.add_url_rule('/', 'home', self.serve_index)
        self.app.add_url_rule('/api/process-payment', 
                             'process_payment', 
                             self.process_payment, 
                             methods=['POST'])
        self.app.add_url_rule('/api/payment-config', 
                             'get_payment_config', 
                             self.get_payment_config, 
                             methods=['GET'])

    def serve_index(self):
        return render_template('test.html')

    def get_payment_config(self):
        try:
            return jsonify({
                "apiVersion": 2,
                "apiVersionMinor": 0,
                "allowedPaymentMethods": [{
                    "type": "CARD",
                    "parameters": {
                        "allowedAuthMethods": self.config.allowed_auth_methods,
                        "allowedCardNetworks": self.config.allowed_card_networks
                    },
                    "tokenizationSpecification": {
                        "type": "PAYMENT_GATEWAY",
                        "parameters": {
                            "gateway": self.config.gateway_name,
                            "gatewayMerchantId": self.config.merchant_id
                        }
                    }
                }],
                "merchantInfo": {
                    "merchantId": self.config.merchant_id,
                    "merchantName": self.config.merchant_name
                },
                "transactionInfo": {
                    "totalPriceStatus": "FINAL",
                    "totalPrice": "1.00",
                    "currencyCode": self.config.currency_code,
                    "countryCode": self.config.country_code
                }
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def process_payment(self):
        try:
            payment_data = request.get_json()
            if not self.validate_payment_data(payment_data):
                return jsonify({"success": False, "error": "Dados inválidos"}), 400

            token_data = self._extract_payment_token(payment_data)
            success = self._process_with_gateway(token_data)

            if success:
                return jsonify({"success": True})
            return jsonify({"success": False, "error": "Falha no processamento"})

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    def validate_payment_data(self, payment_data: Dict) -> bool:
        required_fields = {'apiVersion', 'apiVersionMinor', 'paymentMethodData'}
        return all(field in payment_data for field in required_fields)

    def _extract_payment_token(self, payment_data: Dict) -> Dict:
        token_data = payment_data["paymentMethodData"]["tokenizationData"]
        return {
            "token": token_data["token"],
            "type": token_data["type"],
            "gateway": self.config.gateway_name
        }

    def _process_with_gateway(self, token_data: Dict) -> bool:
        print(f"Processando pagamento com gateway {self.config.gateway_name}")
        print(f"Token data: {token_data}")
        return True

    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = True):
        self.app.run(host=host, port=port, debug=debug) 