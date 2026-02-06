class Endpoints:

    PAYMENT_INTENTS = "/v1/payments_intents"
    PAYMENT_INTENT = "/v1/payments_indents/:id"
    CONFIRM_PAYMENT_INTENT = "/v1/payments_indents/:id/confirm"
    CAPTURE_PAYMENT_INTENT = "/v1/payments_indents/:id/capture"
    CANCEL_PAYMENT_INTENT = "/v1/payments_indents/:id/cancel"

    CUSTOMERS= "/v1/customers"
    CUSTOMER = "/v1/customers/:id"
    SEARCH_CUSTOMERS = "v1/customers/search"

    REFUNDS = "/v1/refunds"
    REFUND = "/v1/refunds/:id"
    CANCEL_REFUND = "/v1/refunds/:id/cancel"

    CHARGES = "/v1/charges"
    CHARGE = "/v1/charges/:id"
    CAPTURE_CHARGE = "/v1/charges/:id/capture"
    SEARCH_CHARGES = "/v1/charges/search"

# Valid Status Codes
class StatusCodes:
    """Expected HTTP status codes."""
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    REQUEST_FAILED = 402
    RATE_LIMITED = 429
    SERVER_ERROR = 500


# Payment Intent Statuses
class PaymentIntentStatus:
    REQUIRES_PAYMENT_METHOD = "requires_payment_method"
    REQUIRES_CONFIRMATION = "requires_confirmation"
    REQUIRES_ACTION = "requires_action"
    PROCESSING = "processing"
    REQUIRES_CAPTURE = "requires_capture"
    CANCELED = "canceled"
    SUCCEEDED = "succeeded"
    
    ALL = [
        REQUIRES_PAYMENT_METHOD,
        REQUIRES_CONFIRMATION,
        REQUIRES_ACTION,
        PROCESSING,
        REQUIRES_CAPTURE,
        CANCELED,
        SUCCEEDED,
    ]


# Refund Statuses
class RefundStatus:
    PENDING = "pending"
    REQUIRES_ACTION = "requires_action"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
    
    ALL = [PENDING, REQUIRES_ACTION, SUCCEEDED, FAILED, CANCELED]


# Refund Reasons
class RefundReason:
    DUPLICATE = "duplicate"
    FRAUDULENT = "fraudulent"
    REQUESTED_BY_CUSTOMER = "requested_by_customer"
    
    ALL = [DUPLICATE, FRAUDULENT, REQUESTED_BY_CUSTOMER]


# Currency Codes
class Currency:
    USD = "usd"
    EUR = "eur"
    GBP = "gbp"
    JPY = "jpy"
    CAD = "cad"
    AUD = "aud"
    
    ALL = [USD, EUR, GBP, JPY, CAD, AUD]


# Object Type Prefixes
class ObjectPrefix:
    PAYMENT_INTENT = "pi_"
    CUSTOMER = "cus_"
    REFUND = "re_"
    CHARGE = "ch_"
    PAYMENT_METHOD = "pm_"


# Error Types
class ErrorType:
    INVALID_REQUEST = "invalid_request_error"
    AUTHENTICATION = "authentication_error"
    CARD_ERROR = "card_error"
    RATE_LIMIT = "rate_limit_error"
    API_ERROR = "api_error"


# Test Data
class TestData:
    
    # Payment Intent test data
    VALID_AMOUNT = 2000  # $20.00 in cents
    VALID_CURRENCY = "usd"
    MIN_AMOUNT = 50  # Minimum charge amount
    MAX_AMOUNT = 99999999  # Maximum amount
    
    # Customer test data
    VALID_EMAIL = "test@example.com"
    VALID_NAME = "Test Customer"
    VALID_PHONE = "+15555555555"
    
    # Invalid data for negative tests
    INVALID_CURRENCY = "invalid"
    INVALID_EMAIL = "not-an-email"
    NEGATIVE_AMOUNT = -100