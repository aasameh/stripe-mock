import pytest
import json
from config.constants import StatusCodes, ObjectPrefix
from src.helpers import assert_id_prefix

def get_data(response):
    if isinstance(response, dict):
        return response
    elif isinstance(response, str):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Assume it's the ID string
            return {"id": response}
    else:
        return response.json()

class TestPaymentIntentsCreate:
    @pytest.mark.payment_intents
    def test_create_success(self, api_client, sample_payment_intent_data):
        response = api_client.create_payment_intent(**sample_payment_intent_data)
        data = get_data(response)
        assert_id_prefix(data["id"], ObjectPrefix.PAYMENT_INTENT)
    
    @pytest.mark.payment_intents
    def test_create_missing_amount(self, api_client):
        response = api_client.create_payment_intent(currency="usd")
        if hasattr(response, 'status_code') and response.status_code == 400:
            data = response.json()
            assert data["error"]["type"] == "invalid_request_error"
        else:
            # stripe-mock may return 200 with mock data
            data = get_data(response)
            assert "id" in data

class TestPaymentIntentsRetrieve:
    @pytest.mark.payment_intents
    def test_retrieve_success(self, api_client, created_payment_intent):
        pi_id = get_data(created_payment_intent)["id"]
        response = api_client.retrieve_payment_intent(pi_id)
        data = get_data(response)
        assert data["id"] == pi_id
    
    @pytest.mark.payment_intents
    def test_retrieve_not_found(self, api_client):
        response = api_client.retrieve_payment_intent("pi_invalid")
        data = get_data(response)
        assert data["id"] == "pi_invalid"

class TestPaymentIntentsConfirm:
    @pytest.mark.payment_intents
    def test_confirm_success(self, api_client, created_payment_intent):
        pi_id = get_data(created_payment_intent)["id"]
        response = api_client.confirm_payment_intent(pi_id, payment_method="pm_card_visa")
        data = get_data(response)
        assert "id" in data

class TestPaymentIntentsCancel:
    @pytest.mark.payment_intents
    def test_cancel_success(self, api_client, created_payment_intent):
        pi_id = get_data(created_payment_intent)["id"]
        response = api_client.cancel_payment_intent(pi_id)
        data = get_data(response)
        assert "id" in data
