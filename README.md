# Hugging Face API Client

This package provides a Python client for interacting with the Hugging Face Rest interfaces for Inference Endpoints `https://api.endpoints.huggingface.cloud/`

## Installation

You can install this package using pip:

```bash
pip install -i https://test.pypi.org/simple/ hfendpoint3
```

## Usage

First, import the `HFEndpoint` class from the `hfendpoint3` package:

```python
from hfendpoint3 import HFEndpoint
```

Then, create an instance of `HFEndpoint` with your API token and account name:

```python
endpoint = HFEndpoint('your_token', 'your_account')
```

Now you can use the methods on `endpoint` to interact with the Hugging Face API.

## Methods

Here are the methods available on an `HFEndpoint` instance:

- `list()`: Lists all endpoints for the account.
- `create(data)`: Creates a new endpoint with the given data.
- `delete(endpoint_name)`: Deletes the endpoint with the given name.
- `get(endpoint_name)`: Retrieves the endpoint with the given name.
- `status(endpoint_name)`: Retrieves the status of the endpoint with the given name.

## Testing

You can run the tests for this package with pytest:

```bash
pytest tests/
```
