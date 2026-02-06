"""
Global pytest fixtures for stripe-mock API testing.
"""
import pytest
from src.api_client import StripeClient
from config.settings import settings


@pytest.fixture(scope="session")
def api_client():
    """Create a shared API client for the test session."""
    return StripeClient()


@pytest.fixture(scope="session")
def unauthenticated_client():
    """Create an API client without authentication."""
    return StripeClient(api_key=None)


@pytest.fixture(scope="session")
def invalid_auth_client():
    """Create an API client with invalid authentication."""
    return StripeClient(api_key="invalid_key")


@pytest.fixture
def sample_payment_intent_data():
    """Sample data for creating a payment intent."""
    return {
        "amount": 2000,
        "currency": "usd",
        "description": "Test payment intent",
        "metadata": {"test_id": "pytest_001"}
    }


@pytest.fixture
def sample_customer_data():
    """Sample data for creating a customer."""
    return {
        "email": "test@example.com",
        "name": "Test Customer",
        "phone": "+15555555555",
        "description": "Test customer",
        "metadata": {"test_id": "pytest_001"}
    }


@pytest.fixture
def sample_refund_data():
    """Sample data for creating a refund."""
    return {
        "reason": "requested_by_customer",
        "metadata": {"test_id": "pytest_001"}
    }


@pytest.fixture(scope="function")
def created_customer(api_client, sample_customer_data):
    """Create a customer and return its data."""
    response = api_client.create_customer(**sample_customer_data)
    return response


@pytest.fixture(scope="function")
def created_payment_intent(api_client, sample_payment_intent_data):
    """Create a payment intent and return its data."""
    response = api_client.create_payment_intent(**sample_payment_intent_data)
    return response


@pytest.fixture(scope="function")
def created_charge(api_client):
    """Create a charge and return its data."""
    response = api_client.create_charge(amount=2000, currency="usd")
    return response
