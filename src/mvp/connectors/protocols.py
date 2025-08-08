# src/mvp/connectors/protocols.py

import requests
from typing import Optional

class OAuth2Handler:
    """
    Handles OAuth2 authentication for connectors.

    Usage:
        - Used by connectors requiring OAuth2 (e.g., Google)
        - Integrates with ConnectorBase

    TODO:
        - Support token refresh
        - Secure credential management
        - Add gRPC protocol support
    """

    def __init__(self, client_id, client_secret, auth_url, token_url, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url
        self.token_url = token_url
        self.redirect_uri = redirect_uri
        self.access_token = None

    def authenticate(self, code: str):
        """Exchange code for access token."""
        # TODO: Implement full OAuth2 flow
        pass

    def get_access_token(self):
        """Return current access token."""
        return self.access_token

class RESTHandler:
    """
    Handles REST API requests for connectors.

    Usage:
        - Used by connectors for standard REST APIs
        - Integrates with ConnectorBase

    TODO:
        - Add retry logic
        - Support for webhooks
        - Add gRPC protocol support
    """

    def __init__(self, base_url: str, headers: Optional[dict] = None):
        self.base_url = base_url
        self.headers = headers or {}

    def get(self, endpoint: str, params: Optional[dict] = None):
        """Perform GET request."""
        # TODO: Add error handling, retries
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return requests.get(url, headers=self.headers, params=params)

    def post(self, endpoint: str, data: Optional[dict] = None):
        """Perform POST request."""
        # TODO: Add error handling, retries
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return requests.post(url, headers=self.headers, json=data)