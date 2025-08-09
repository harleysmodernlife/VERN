from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from typing import Dict

from vern_backend.app.errors import error_response

router = APIRouter()

# Example registry of supported integrations
INTEGRATIONS = {
    "google_calendar": {
        "name": "Google Calendar",
        "description": "Sync events and reminders.",
        "docs_url": "https://developers.google.com/calendar",
        "required_keys": ["GOOGLE_CALENDAR_ID", "GOOGLE_CALENDAR_CREDENTIALS_JSON"],
        "configured": False,
        "config": {}
    },
    "openweathermap": {
        "name": "OpenWeatherMap",
        "description": "Get real-time weather data.",
        "docs_url": "https://openweathermap.org/api",
        "required_keys": ["OPENWEATHERMAP_API_KEY"],
        "configured": False,
        "config": {}
    },
    "ollama": {
        "name": "Ollama (Local LLM)",
        "description": "Run local LLM models.",
        "docs_url": "https://ollama.com/",
        "required_keys": [],
        "configured": True,
        "config": {}
    },
    "openai": {
        "name": "OpenAI",
        "description": "Use OpenAI GPT models.",
        "docs_url": "https://platform.openai.com/",
        "required_keys": ["OPENAI_API_KEY"],
        "configured": False,
        "config": {}
    }
    # Add more integrations here...
}

class IntegrationConfig(BaseModel):
    config: Dict[str, str]

@router.get("/integrations/")
def list_integrations():
    return [
        {
            "provider": key,
            "name": value["name"],
            "description": value["description"],
            "docs_url": value["docs_url"],
            "required_keys": value["required_keys"],
            "configured": value["configured"]
        }
        for key, value in INTEGRATIONS.items()
    ]

@router.get("/integrations/{provider}/status")
def get_integration_status(provider: str, request: Request):
    if provider not in INTEGRATIONS:
        return error_response("NOT_FOUND", status.HTTP_404_NOT_FOUND, "Provider not found", request)
    return {
        "provider": provider,
        "configured": INTEGRATIONS[provider]["configured"],
        "config": INTEGRATIONS[provider]["config"]
    }

@router.post("/integrations/{provider}/configure")
def configure_integration(provider: str, cfg: IntegrationConfig, request: Request):
    if provider not in INTEGRATIONS:
        return error_response("NOT_FOUND", status.HTTP_404_NOT_FOUND, "Provider not found", request)
    # Save config (in-memory for now; persist in DB or file for production)
    INTEGRATIONS[provider]["config"] = cfg.config
    # Mark as configured if all required keys are present
    required = INTEGRATIONS[provider]["required_keys"]
    INTEGRATIONS[provider]["configured"] = all(k in cfg.config and cfg.config[k] for k in required)
    return {"provider": provider, "configured": INTEGRATIONS[provider]["configured"]}

from fastapi import Response
import subprocess

@router.get("/integrations/ollama/models")
def get_ollama_models(request: Request):
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        models = []
        for line in result.stdout.strip().splitlines():
            # Expected format: "model_name  tag  size  modified"
            parts = line.split()
            if len(parts) >= 1 and not line.startswith("NAME"):
                models.append({"name": parts[0]})
        return {"models": models}
    except subprocess.CalledProcessError as e:
        return error_response(
            "OLLAMA_ERROR",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Ollama command failed: {e}",
            request
        )
    except FileNotFoundError:
        return error_response(
            "OLLAMA_NOT_FOUND",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ollama executable not found",
            request
        )
    except Exception as e:
        return error_response(
            "UNKNOWN_ERROR",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Unexpected error: {e}",
            request
        )
