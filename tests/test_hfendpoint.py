import pytest
from hfendpoint.src.api import HFEndpoint
from hfendpoint.src.models import EndpointPayload

def test_init_valid():
    endpoint = HFEndpoint('valid_token', 'valid_account')
    assert endpoint.token == 'valid_token'
    assert endpoint.account == 'valid_account'
    assert endpoint.base_url == 'https://api.endpoints.huggingface.cloud/v2/endpoint/valid_account'

def test_init_invalid_token():
    with pytest.raises(ValueError):
        HFEndpoint('', 'valid_account')

def test_init_invalid_account():
    with pytest.raises(ValueError):
        HFEndpoint('valid_token', '')

def test_headers():
    endpoint = HFEndpoint('valid_token', 'valid_account')
    headers = endpoint._headers()
    assert headers == {
        "Authorization": f"Bearer valid_token",
        "Content-Type": "application/json"
    }

def test_list(mocker):
    mocker.patch('requests.request', return_value=mocker.Mock(json=lambda: {'data': 'sample data'}, raise_for_status=lambda: None))
    endpoint = HFEndpoint('valid_token', 'valid_account')
    result = endpoint.list()
    assert result == {'data': 'sample data'}

def test_create(mocker):

    payload = {
        "accountId": None,
        "compute": {
            "accelerator": "gpu",
            "instanceSize": "medium",
            "instanceType": "g5.2xlarge",
            'scaling': {'minReplica': 0, 'maxReplica': 1}
        },
        "model": {
            "repository": "Intel/neural-chat-7b-v3-1",
            "revision": "af2489cde09e9d2c175622f651875e83824c4b10",
            "task": "text-generation",
            "framework": "pytorch",
            "image":{'custom': {
                'url': 'ghcr.io/huggingface/text-generation-inference:1.1.0',
                'health_route': '/health',
                'env': {
                    'MAX_BATCH_PREFILL_TOKENS': '2048',
                    'MAX_INPUT_LENGTH': '1024',
                    'MAX_TOTAL_TOKENS': '1512',
                    'MODEL_ID': '/repository'
                }
            }}
        },
        "name": "test_endpoint",
        "provider": {
            "region": "eu-west-1",
            "vendor": "aws"
        },
        "type": "protected"
        }

    return_payload = {
        "items":[
            payload
        ] 
    }

    mocker.patch('requests.request', return_value=mocker.Mock(json=lambda: return_payload, raise_for_status=lambda: None))
    endpoint = HFEndpoint('valid_token', 'valid_account')

        # Call the create method
    response = endpoint.create(payload)

    # Validate the response using the Pydantic model
    try:
        EndpointPayload(**response["items"][0])
    except ValueError as e:
        assert False, f"Response does not match the expected structure: {e}"

    # If the response matches the expected structure, the test passes
    assert True

def test_delete(mocker):
    mocker.patch('requests.request', return_value=mocker.Mock(json=lambda: {'data': 'sample data'}, raise_for_status=lambda: None))
    endpoint = HFEndpoint('valid_token', 'valid_account')
    result = endpoint.delete('endpoint_name')
    assert result == {'data': 'sample data'}

def test_get(mocker):
    mocker.patch('requests.request', return_value=mocker.Mock(json=lambda: {'data': 'sample data'}, raise_for_status=lambda: None))
    endpoint = HFEndpoint('valid_token', 'valid_account')
    result = endpoint.get('endpoint_name')
    assert result == {'data': 'sample data'}

def test_status(mocker):
    mocker.patch('requests.request', return_value=mocker.Mock(json=lambda: {'status': {'state': 'active'}}, raise_for_status=lambda: None))
    endpoint = HFEndpoint('valid_token', 'valid_account')
    result = endpoint.status('endpoint_name')
    assert result == 'active'