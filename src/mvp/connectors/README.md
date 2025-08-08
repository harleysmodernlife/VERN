# VERN Modular Cloud API Connectors

This directory contains the modular connector framework for integrating cloud APIs with VERN.

## Structure

- [`base.py`](src/mvp/connectors/base.py): Abstract base class for connectors.
- [`protocols.py`](src/mvp/connectors/protocols.py): Protocol handlers (OAuth2, REST).
- [`registry.py`](src/mvp/connectors/registry.py): Connector registry for dynamic discovery/configuration.
- [`google_connector.py`](src/mvp/connectors/google_connector.py): Sample Google API connector.
- [`finance_connector.py`](src/mvp/connectors/finance_connector.py): Sample finance API connector.
- [`health_connector.py`](src/mvp/connectors/health_connector.py): Sample health API connector.
- [`device_connector.py`](src/mvp/connectors/device_connector.py): Sample device API connector.

## Integration Points

- **ConnectorBase**: All connectors inherit from this abstract class.
- **Protocol Handlers**: OAuth2Handler and RESTHandler provide authentication and request logic.
- **Registry**: Use `ConnectorRegistry` to register and discover connectors dynamically.
- **Configuration**: Pass configuration dicts to connectors for API keys, endpoints, etc.

## TODOs for Advanced Features

- gRPC protocol support
- Webhook event handling
- Secure credential management (vault integration, encrypted storage)
- External connector/plugin loading

See inline TODOs in each file for details.
