import json
from typing import Any, Dict, List, Optional
from jsonschema import validate, ValidationError #type:ignore


def assert_status_code(response, expected_code: int, message: Optional[str] = None):

    actual_code = response.status_code
    error_msg = message or f"Expected status code {expected_code}, got {actual_code}"
    if actual_code != expected_code:
        try:
            body = response.json()
            error_msg += f"\nResponse body: {json.dumps(body, indent=2)}"
        except:
            error_msg += f"\nResponse text: {response.text}"
    assert actual_code == expected_code, error_msg


def assert_response_contains(response, key: str, expected_value: Any = None):
    data = response.json()
    assert key in data, f"Response missing key '{key}'. Response: {data}"
    if expected_value is not None:
        assert data[key] == expected_value, f"Expected {key}={expected_value}, got {data[key]}"


def assert_object_type(response, expected_type: str):
    data = response.json()
    assert "object" in data, f"Response missing 'object' field. Response: {data}"
    assert data["object"] == expected_type, f"Expected object type '{expected_type}', got '{data['object']}'"


def assert_id_prefix(response, expected_prefix: str):
    data = response.json()
    assert "id" in data, f"Response missing 'id' field. Response: {data}"
    assert data["id"].startswith(expected_prefix), f"Expected ID prefix '{expected_prefix}', got ID '{data['id']}'"


def assert_is_list_response(response, expected_object_type: Optional[str] = None):
    data = response.json()
    assert "object" in data and data["object"] == "list", "Response is not a list object"
    assert "data" in data, "List response missing 'data' field"
    assert isinstance(data["data"], list), "'data' field is not a list"
    
    if expected_object_type and len(data["data"]) > 0:
        for item in data["data"]:
            assert item.get("object") == expected_object_type, f"List item type mismatch: {item}"


def assert_error_response(response, expected_type: Optional[str] = None):
    data = response.json()
    assert "error" in data, f"Response is not an error response. Response: {data}"
    
    if expected_type:
        error = data["error"]
        assert error.get("type") == expected_type, f"Expected error type '{expected_type}', got '{error.get('type')}'"


def validate_json_schema(response, schema: Dict[str, Any]):
    try:
        data = response.json()
        validate(instance=data, schema=schema)
    except ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e.message}")


def assert_field_types(response, field_types: Dict[str, type]):
    """
    Assert that response fields have the expected types.
    
    Args:
        response: requests.Response object
        field_types: Dictionary mapping field names to expected types
    """
    data = response.json()
    for field, expected_type in field_types.items():
        assert field in data, f"Response missing field '{field}'"
        actual_value = data[field]
        if actual_value is not None:  # Allow None values
            assert isinstance(actual_value, expected_type), \
                f"Field '{field}' expected {expected_type.__name__}, got {type(actual_value).__name__}"


def assert_required_fields(response, required_fields: List[str]):
    data = response.json()
    missing_fields = [field for field in required_fields if field not in data]
    assert not missing_fields, f"Response missing required fields: {missing_fields}"


def get_response_json(response) -> Dict[str, Any]:
    try:
        return response.json()
    except json.JSONDecodeError:
        raise AssertionError(f"Response is not valid JSON: {response.text}")


def extract_id(response) -> str:
    data = response.json()
    assert "id" in data, f"Response missing 'id' field. Response: {data}"
    return data["id"]
