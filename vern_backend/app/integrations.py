from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Optional

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
def get_integration_status(provider: str):
    if provider not in INTEGRATIONS:
        raise HTTPException(status_code=404, detail="Provider not found")
    return {
        "provider": provider,
        "configured": INTEGRATIONS[provider]["configured"],
        "config": INTEGRATIONS[provider]["config"]
    }

@router.post("/integrations/{provider}/configure")
def configure_integration(provider: str, cfg: IntegrationConfig):
    if provider not in INTEGRATIONS:
        raise HTTPException(status_code=404, detail="Provider not found")
    # Save config (in-memory for now; persist in DB or file for production)
    INTEGRATIONS[provider]["config"] = cfg.config
    # Mark as configured if all required keys are present
    required = INTEGRATIONS[provider]["required_keys"]
    INTEGRATIONS[provider]["configured"] = all(k in cfg.config and cfg.config[k] for k in required)
    return {"provider": provider, "configured": INTEGRATIONS[provider]["configured"]}
