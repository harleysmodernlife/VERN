# src/mvp/connectors/finance_connector.py

from src.mvp.connectors.base import ConnectorBase
from src.mvp.connectors.protocols import RESTHandler
from src.mvp.connectors.registry import ConnectorRegistry

class FinanceConnector(ConnectorBase):
    """
    Sample connector for finance APIs (e.g., stock, banking).

    Uses REST protocol.

    TODO:
        - Add support for OAuth2 for secure APIs
        - Add gRPC support
        - Secure credential management
        - Webhook event handling
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.rest = RESTHandler(base_url=config.get("base_url", "https://api.finance.com"))

    def connect(self):
        # TODO: Authenticate if needed
        pass

    def fetch(self, endpoint: str, params=None):
        # TODO: Add authentication, error handling
        return self.rest.get(endpoint, params)

    def disconnect(self):
        # TODO: Cleanup resources
        pass

# Register connector
ConnectorRegistry.register("finance", FinanceConnector)