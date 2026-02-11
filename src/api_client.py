import requests
from typing import Optional, Dict, Any
from config.settings import settings
from config.constants import Endpoints

class StripeClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or settings.get_base_url()
        self.api_key = api_key if api_key is not None else settings.API_KEY
        self.timeout = settings.REQUEST_TIMEOUT
        self.verify_ssl = settings.VERIFY_SSL
    
    @property
    def headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        
        url = self._build_url(endpoint)
        
        return requests.request(
            method=method,
            url=url,
            headers=self.headers,
            data=data,
            params=params,
            timeout=self.timeout,
            verify=self.verify_ssl,
            **kwargs
        )
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        return self._request("GET", endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        return self._request("POST", endpoint, data=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("DELETE", endpoint, **kwargs)

    # Payment intents    
    def create_payment_intent(
        self,
        amount: int,
        currency: str,
        description: Optional[str] = None,
        customer: Optional[str] = None,
        payment_method: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:

        data = {
            "amount": amount,
            "currency": currency,
        }
        if description:
            data["description"] = description
        if customer:
            data["customer"] = customer
        if payment_method:
            data["payment_method"] = payment_method
        if metadata:
            for key, value in metadata.items():
                data[f"metadata[{key}]"] = value
        data.update(kwargs)
        
        return self.post(Endpoints.PAYMENT_INTENTS, data=data)
    
    def retrieve_payment_intent(self, payment_intent_id: str) -> requests.Response:
        endpoint = Endpoints.PAYMENT_INTENT.format(id=payment_intent_id)
        return self.get(endpoint)
    
    def update_payment_intent(
        self,
        payment_intent_id: str,
        **kwargs
    ) -> requests.Response:
        endpoint = Endpoints.PAYMENT_INTENT.format(id=payment_intent_id)
        return self.post(endpoint, data=kwargs)
    
    def list_payment_intents(
        self,
        limit: Optional[int] = None,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        **kwargs
    ) -> requests.Response:
        params = {}
        if limit:
            params["limit"] = limit
        if starting_after:
            params["starting_after"] = starting_after
        if ending_before:
            params["ending_before"] = ending_before
        params.update(kwargs)
        
        return self.get(Endpoints.PAYMENT_INTENTS, params=params)
    
    def confirm_payment_intent(
        self,
        payment_intent_id: str,
        payment_method: Optional[str] = None,
        **kwargs
    ) -> requests.Response:

        endpoint = Endpoints.CONFIRM_PAYMENT_INTENT.format(id=payment_intent_id)
        data = {}
        if payment_method:
            data["payment_method"] = payment_method
        data.update(kwargs)
        
        return self.post(endpoint, data=data if data else None)
    
    def capture_payment_intent(
        self,
        payment_intent_id: str,
        amount_to_capture: Optional[int] = None,
        **kwargs
    ) -> requests.Response:

        endpoint = Endpoints.CAPTURE_PAYMENT_INTENT.format(id=payment_intent_id)
        data = {}
        if amount_to_capture:
            data["amount_to_capture"] = amount_to_capture
        data.update(kwargs)
        
        return self.post(endpoint, data=data if data else None)
    
    def cancel_payment_intent(
        self,
        payment_intent_id: str,
        cancellation_reason: Optional[str] = None,
        **kwargs
    ) -> requests.Response:

        endpoint = Endpoints.CANCEL_PAYMENT_INTENT.format(id=payment_intent_id)
        data = {}
        if cancellation_reason:
            data["cancellation_reason"] = cancellation_reason
        data.update(kwargs)
        
        return self.post(endpoint, data=data if data else None)
    
    # Customers

    def create_customer(
        self,
        email: Optional[str] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        
        data = {}
        if email:
            data["email"] = email
        if name:
            data["name"] = name
        if phone:
            data["phone"] = phone
        if description:
            data["description"] = description
        if metadata:
            for key, value in metadata.items():
                data[f"metadata[{key}]"] = value
        data.update(kwargs)
        
        return self.post(Endpoints.CUSTOMERS, data=data if data else None)
    
    def retrieve_customer(self, customer_id: str) -> requests.Response:
        endpoint = Endpoints.CUSTOMER.format(id=customer_id)
        return self.get(endpoint)
    
    def update_customer(self, customer_id: str, **kwargs) -> requests.Response:

        endpoint = Endpoints.CUSTOMER.format(id=customer_id)
        return self.post(endpoint, data=kwargs)
    
    def delete_customer(self, customer_id: str) -> requests.Response:

        endpoint = Endpoints.CUSTOMER.format(id=customer_id)
        return self.delete(endpoint)
    
    def list_customers(
        self,
        limit: Optional[int] = None,
        email: Optional[str] = None,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        **kwargs
    ) -> requests.Response:

        params = {}
        if limit:
            params["limit"] = limit
        if email:
            params["email"] = email
        if starting_after:
            params["starting_after"] = starting_after
        if ending_before:
            params["ending_before"] = ending_before
        params.update(kwargs)
        
        return self.get(Endpoints.CUSTOMERS, params=params)
    
    def search_customers(self, query: str, **kwargs) -> requests.Response:
        params = {"query": query}
        params.update(kwargs)
        
        return self.get(Endpoints.SEARCH_CUSTOMERS, params=params)


    # Refunds
    
    def create_refund(
        self,
        charge: Optional[str] = None,
        payment_intent: Optional[str] = None,
        amount: Optional[int] = None,
        reason: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:

        data = {}
        if charge:
            data["charge"] = charge
        if payment_intent:
            data["payment_intent"] = payment_intent
        if amount:
            data["amount"] = amount
        if reason:
            data["reason"] = reason
        if metadata:
            for key, value in metadata.items():
                data[f"metadata[{key}]"] = value
        data.update(kwargs)
        
        return self.post(Endpoints.REFUNDS, data=data if data else None)
    
    def retrieve_refund(self, refund_id: str) -> requests.Response:
        endpoint = Endpoints.REFUND.format(id=refund_id)
        return self.get(endpoint)
    
    def update_refund(self, refund_id: str, **kwargs) -> requests.Response:
        endpoint = Endpoints.REFUND.format(id=refund_id)
        return self.post(endpoint, data=kwargs)
    
    def list_refunds(
        self,
        limit: Optional[int] = None,
        charge: Optional[str] = None,
        payment_intent: Optional[str] = None,
        **kwargs
    ) -> requests.Response:
        params = {}
        if limit:
            params["limit"] = limit
        if charge:
            params["charge"] = charge
        if payment_intent:
            params["payment_intent"] = payment_intent
        params.update(kwargs)
        
        return self.get(Endpoints.REFUNDS, params=params)
    
    def cancel_refund(self, refund_id: str) -> requests.Response:
        endpoint = Endpoints.CANCEL_REFUND.format(id=refund_id)
        return self.post(endpoint)
    
    # Charges
    
    def create_charge(
        self,
        amount: int,
        currency: str,
        source: Optional[str] = None,
        customer: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> requests.Response:

        data = {
            "amount": amount,
            "currency": currency,
        }
        if source:
            data["source"] = source
        if customer:
            data["customer"] = customer
        if description:
            data["description"] = description
        data.update(kwargs)
        
        return self.post(Endpoints.CHARGES, data=data)
    
    def retrieve_charge(self, charge_id: str) -> requests.Response:
        endpoint = Endpoints.CHARGE.format(id=charge_id)
        return self.get(endpoint)
