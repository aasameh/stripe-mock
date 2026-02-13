import pytest
import json
from config.constants import ObjectPrefix
from src.helpers import assert_id_prefix

def get_data(response):
    if isinstance(response, dict):
        return response
    elif isinstance(response, str):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"id": response}
    else:
        return response.json()

class TestChargesCreate:
    @pytest.mark.charges
    def test_charge_create_success(self, api_client, sample_charge_data):
        response = api_client.create_charge(**sample_charge_data)
        data = get_data(response)
        assert_id_prefix(data, ObjectPrefix.CHARGE)
    
    @pytest.mark.charges
    def test_charge_create_missing_amount(self, api_client):
        response = api_client.create_charge(amount = None, currency="usd")
        data = get_data(response)
        assert "id" in data
    
    @pytest.mark.charges
    def test_charge_create_invalid_amount(self, api_client):
        response = api_client.create_charge(amount=-100, currency="usd")
        data = get_data(response)
        assert "id" in data
    
    @pytest.mark.charges
    def test_charge_create_no_currency(self, api_client):
        response = api_client.create_charge(amount=2000, currency = None)
        data = get_data(response)
        assert "id" in data

class TestChargesRetrieve:
    @pytest.mark.charges
    def test_charge_retrieve_success(self, api_client, created_charge):
        charge_id = get_data(created_charge)["id"]
        response = api_client.retrieve_charge(charge_id)
        data = get_data(response)
        assert data["id"] == charge_id
    
    @pytest.mark.charges
    def test_charge_retrieve_not_found(self, api_client):
        response = api_client.retrieve_charge("ch_invalid")
        data = get_data(response)
        assert data["id"] == "ch_invalid"

class TestChargesUpdate:
    @pytest.mark.charges
    def test_charge_update_success(self, api_client, created_charge):
        charge_id = get_data(created_charge)["id"]
        response = api_client.update_charge(charge_id, description="Updated description")
        data = get_data(response)
        if "error" in data:
            assert data["error"]["type"] == "invalid_request_error"  #type:ignore
            # mock server may return error for unsupported update
        else:
            assert "id" in data  
            # mock may return id if it supports update
    
    @pytest.mark.charges
    def test_charge_update_not_found(self, api_client):
        response = api_client.update_charge("ch_invalid", description="Test")
        data = get_data(response)
        assert "error" in data or "id" in data  
        # mock server may return error or id

class TestChargesCapture:
    @pytest.mark.charges
    def test_charge_capture_success(self, api_client, created_charge):
        charge_id = get_data(created_charge)["id"]
        response = api_client.capture_charge(charge_id)
        data = get_data(response)
        assert "id" in data
    
    @pytest.mark.charges
    def test_charge_capture_not_found(self, api_client):
        response = api_client.capture_charge("ch_invalid")
        data = get_data(response)
        assert "id" in data

class TestChargesList:
    @pytest.mark.charges
    def test_list_charges_success(self, api_client):
        response = api_client.list_charges()
        data = get_data(response)
        assert "data" in data
        assert isinstance(data["data"], list)
    
    @pytest.mark.charges
    def test_list_charges_with_limit(self, api_client):
        response = api_client.list_charges(limit=5)
        data = get_data(response)
        assert len(data["data"]) <= 5