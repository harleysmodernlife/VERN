# src/mvp/connectors/device_connector.py

from src.mvp.connectors.base import ConnectorBase
from src.mvp.connectors.protocols import RESTHandler
from src.mvp.connectors.registry import ConnectorRegistry

class DeviceConnector(ConnectorBase):
    """
    Sample connector for device APIs (e.g., IoT, smart home).

    Uses REST protocol.

    TODO:
        - Add support for device-specific authentication
        - Add gRPC support
        - Secure credential management
        - Webhook event handling
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.rest = RESTHandler(base_url=config.get("base_url", "https://api.device.com"))

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
ConnectorRegistry.register("device", DeviceConnector)