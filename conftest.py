import pytest
from src.api_client import StripeClient
from config.settings import settings


@pytest.fixture(scope="session")
def api_client(): return StripeClient()


@pytest.fixture(scope="session")
def unauthenticated_client(): return StripeClient(api_key="")

@pytest.fixture(scope="session")
def invalid_auth_client(): return StripeClient(api_key="invalid_key")


@pytest.fixture
def sample_payment_intent_data():
    return {
        "amount": 2000,
        "currency": "usd",
        "description": "Test payment intent",
        "metadata": {"test_id": "pytest_001"}
    }


@pytest.fixture
def sample_customer_data():
    return {
        "email": "test@example.com",
        "name": "Test Customer",
        "phone": "+15555555555",
        "description": "Test customer",
        "metadata": {"test_id": "pytest_001"}
    }


@pytest.fixture
def sample_refund_data():
    return {
        "reason": "requested_by_customer",
        "metadata": {"test_id": "pytest_001"}
    }


@pytest.fixture(scope="function")
def created_customer(api_client, sample_customer_data):
    response = api_client.create_customer(**sample_customer_data)
    return response


@pytest.fixture(scope="function")
def created_payment_intent(api_client, sample_payment_intent_data):
    response = api_client.create_payment_intent(**sample_payment_intent_data)
    return response


@pytest.fixture(scope="function")
def created_charge(api_client):
    response = api_client.create_charge(amount=2000, currency="usd")
    return response
