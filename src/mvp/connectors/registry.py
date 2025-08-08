# src/mvp/connectors/registry.py

from typing import Dict, Type, Optional
from src.mvp.connectors.base import ConnectorBase

class ConnectorRegistry:
    """
    Registry for dynamic discovery and configuration of connectors.

    Integration points:
        - Used by VERN to list, configure, and instantiate connectors
        - Supports plugin-like extensibility

    TODO:
        - Add support for loading connectors from external packages
        - Add secure credential management
        - Add webhook event registration
    """

    _registry: Dict[str, Type[ConnectorBase]] = {}

    @classmethod
    def register(cls, name: str, connector_cls: Type[ConnectorBase]):
        """Register a connector class."""
        cls._registry[name] = connector_cls

    @classmethod
    def get_connector(cls, name: str) -> Optional[Type[ConnectorBase]]:
        """Retrieve a connector class by name."""
        return cls._registry.get(name)

    @classmethod
    def list_connectors(cls):
        """List all registered connector names."""
        return list(cls._registry.keys())

# Example usage:
# (Google connector registration removed)