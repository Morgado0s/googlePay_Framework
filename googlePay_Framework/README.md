# Google Pay Framework Python

Um framework Python elegante e flexível para integração do Google Pay em aplicações Flask.

## 🚀 Características

- Configuração simplificada do Google Pay
- Integração automática com Flask
- Suporte a múltiplas moedas e países
- Gerenciamento flexível de bandeiras de cartão
- Processamento seguro de pagamentos
- Ambiente de teste e produção

## 📋 Pré-requisitos

- Python 3.7+
- Flask 2.0+
- Conta Google Pay para Comerciantes
- ID de comerciante do Google Pay
- Gateway de pagamento configurado

## 💻 Instalação

```bash
pip install google_pay_framework

🔧 Configuração Básica

from flask import Flask
from google_pay_framework import GooglePayConfig, GooglePayProcessor

# Configuração do Google Pay
config = GooglePayConfig(
    merchant_id="SEU_MERCHANT_ID",
    merchant_name="NOME_DA_SUA_LOJA",
    gateway_name="seu_gateway"  # exemplo: "stripe", "adyen", etc.
)

# Personalizações opcionais
config.set_currency("BRL", "BR")  # Configura para Real brasileiro
config.update_price("100.00")     # Define o preço
config.add_card_network("ELO")    # Adiciona bandeira de cartão

🛠️ Integração com Flask

app = Flask(__name__)

# Inicializa o processador
processor = GooglePayProcessor(config)

# Registra as rotas necessárias
app.add_url_rule('/api/payment-config', 'get_payment_config', 
                 processor.get_payment_config, methods=['GET'])
app.add_url_rule('/api/process-payment', 'process_payment', 
                 processor.process_payment, methods=['POST'])

📝 Frontend Integration
Adicione o botão do Google Pay em seu HTML:

<div id="google-pay-button"></div>

<script>
    let paymentsClient = null;

    async function onGooglePayLoaded() {
        try {
            const response = await fetch('/api/payment-config');
            const config = await response.json();
            initializeGooglePay(config);
        } catch (err) {
            console.error('Erro:', err);
        }
    }

    function initializeGooglePay(config) {
        paymentsClient = new google.payments.api.PaymentsClient({
            environment: 'TEST'  // ou 'PRODUCTION' para produção
        });

        paymentsClient.isReadyToPay(config)
            .then(response => {
                if (response.result) {
                    createButton();
                }
            });
    }

    function createButton() {
        const button = paymentsClient.createButton({
            onClick: onGooglePaymentButtonClicked,
            buttonColor: 'black'  // ou 'white'
        });
        document.getElementById('google-pay-button').appendChild(button);
    }

    async function onGooglePaymentButtonClicked() {
        try {
            const response = await fetch('/api/payment-config');
            const config = await response.json();
            
            const paymentData = await paymentsClient.loadPaymentData(config);
            
            const result = await fetch('/api/process-payment', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(paymentData)
            });

            const jsonResult = await result.json();
            if (jsonResult.success) {
                alert('Pagamento bem-sucedido!');
            } else {
                throw new Error(jsonResult.error);
            }
        } catch (err) {
            console.error('Erro:', err);
            alert('Erro no pagamento: ' + err.message);
        }
    }
</script>

<script async src="https://pay.google.com/gp/p/js/pay.js" 
        onload="onGooglePayLoaded()">
</script>

⚙️ Configurações Avançadas
Personalização de Bandeiras de Cartão

config = GooglePayConfig(
    merchant_id="SEU_ID",
    merchant_name="SUA_LOJA",
    allowed_card_networks=["VISA", "MASTERCARD", "ELO"]
)

Configuração de Ambiente

config = GooglePayConfig(
    merchant_id="SEU_ID",
    merchant_name="SUA_LOJA",
    environment="PRODUCTION"  # Use "TEST" para testes
)

Manipulação de Preços

# Atualiza preço
config.update_price("199.99")

# Muda moeda
config.set_currency("EUR", "FR")

🔍 Validação e Tratamento de Erros
O framework inclui validação automática para:

Dados do pagamento

Tokens de autenticação

Configurações do gateway

Respostas do Google Pay

Exemplo de tratamento de erros:

from google_pay_framework import GooglePayError

try:
    result = processor.process_payment(payment_data)
except GooglePayError as e:
    print(f"Erro no processamento: {e}")

🔒 Segurança
Validação automática de tokens

Suporte a 3D Secure

Criptografia de dados sensíveis

Conformidade com PCI DSS

🤝 Contribuindo
Fork o projeto

Crie sua Feature Branch (git checkout -b feature/AmazingFeature)

Commit suas mudanças (git commit -m 'Add some AmazingFeature')

Push para a Branch (git push origin feature/AmazingFeature)

Abra um Pull Request

📄 Licença
Este projeto está sob a licença MIT - veja o arquivo LICENSE.md para detalhes

📧 Suporte
Para suporte, envie um email para gabrielmorgado797@gmail.com ou abra uma issue no GitHub.
