# src/mvp/connectors/base.py

from abc import ABC, abstractmethod
from typing import Optional

class ConnectorBase(ABC):
    """
    Abstract base class for all cloud API connectors.

    Integration points:
        - Protocol handlers (see protocols.py)
        - Registry (see registry.py)
        - Credential management (TODO: secure storage)
        - Event hooks (TODO: webhooks)
    """

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def connect(self):
        """Establish connection to the API."""
        pass

    @abstractmethod
    def fetch(self, endpoint: str, params: Optional[dict] = None):
        """Fetch data from the API."""
        pass

    @abstractmethod
    def disconnect(self):
        """Clean up resources."""
        pass

    # TODO: Add gRPC support
    # TODO: Add webhook event handling
    # TODO: Integrate secure credential management