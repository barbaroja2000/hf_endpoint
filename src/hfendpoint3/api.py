#@title: Utility class to interact with HF API
from typing import Any, Dict
import requests
from .models import EndpointPayload

class HFEndpoint:
    """A class to interact with Hugging Face API endpoints.

    Attributes:
        token (str): The API token for authorization.
        account (str): The Hugging Face account name.
        base_url (str): The base URL for the API endpoints.
    """

    def __init__(self, token: str, account: str):
        """Initializes the HFEndpoint class with API token and account name.

        Args:
            token (str): The API token for authorization.
            account (str): The Hugging Face account name.

        Raises:
            ValueError: If the token or account is not a valid string.
        """
        if not isinstance(token, str) or not token:
            raise ValueError("Invalid token provided.")
        if not isinstance(account, str) or not account:
            raise ValueError("Invalid account name provided.")

        self.token = token
        self.account = account
        self.base_url = f"https://api.endpoints.huggingface.cloud/v2/endpoint/{self.account}"

    def _headers(self) -> Dict[str, str]:
        """Private method to create request headers.

        Returns:
            Dict[str, str]: The headers for API requests.
        """
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Private method to handle API requests.

        Args:
            method (str): The HTTP method (GET, POST, DELETE).
            url (str): The URL for the API request.

        Returns:
            Dict[str, Any]: The JSON response from the API.
        """
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {'error': str(e)}

    def list(self) -> Dict[str, Any]:
        """Lists all endpoints for the account.

        Returns:
            Dict[str, Any]: The JSON response containing the list of endpoints.
        """
        return self._request("GET", self.base_url, headers=self._headers())

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new endpoint with the given payload.

        Args:
            payload (Dict[str, Any]): The data to create a new endpoint.

        Returns:
            Dict[str, Any]: The JSON response from the API.
        """
        try:
            EndpointPayload(**payload)
        except ValueError as e:
            return {'error': str(e)}

        return self._request("POST", self.base_url, headers=self._headers(), json=payload)

    def delete(self, endpoint_name: str) -> Dict[str, Any]:
        """Deletes the endpoint associated with the account.
        Args:
                endpoint_name (str): The name of the endpoint to delete.
        Returns:
            Dict[str, Any]: The JSON response from the API.
        """
        url = f"{self.base_url}/{endpoint_name}"
        return self._request("DELETE", url, headers=self._headers())

    def get(self, endpoint_name: str) -> Dict[str, Any]:
            """Retrieves details of a specific endpoint.

            Args:
                endpoint_name (str): The name of the endpoint to retrieve.

            Returns:
                Dict[str, Any]: The JSON response from the API.

            Raises:
                ValueError: If the endpoint name is not a valid string.
            """
            if not isinstance(endpoint_name, str) or not endpoint_name:
                raise ValueError("Invalid endpoint name provided.")

            url = f"{self.base_url}/{endpoint_name}"
            return self._request("GET", url, headers=self._headers())

    def status(self, endpoint_name: str) -> str:
        """Retrieves the status of a specific endpoint.

        Args:
            endpoint_name (str): The name of the endpoint to check the status.

        Returns:
            str: The status state of the endpoint.

        Raises:
            ValueError: If the endpoint name is not valid.
            KeyError: If the response does not contain the expected keys.
        """
        if not isinstance(endpoint_name, str) or not endpoint_name:
            raise ValueError("Invalid endpoint name provided.")

        response = self.get(endpoint_name)
        if 'error' in response:
            return response['error']

        try:
            return response["status"]["state"]
        except KeyError as e:
            raise KeyError(f"Response does not contain the expected keys: {e}")