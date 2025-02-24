class GooglePayError(Exception):
    """Base exception for Google Pay framework"""
    pass

class PaymentValidationError(GooglePayError):
    """Raised when payment data validation fails"""
    pass 