import os
import yaml
from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, ValidationError
from typing import Dict, Any

router = APIRouter(prefix="/config", tags=["config"])

ENV_PATH = ".env"
YAML_PATH = "config/agent_backends.yaml"

class EnvConfig(BaseModel):
    values: Dict[str, str]

class YamlConfig(BaseModel):
    values: Dict[str, Any]

def read_env():
    if not os.path.exists(ENV_PATH):
        return {}
    with open(ENV_PATH, "r") as f:
        lines = f.readlines()
    env = {}
    for line in lines:
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.strip().split("=", 1)
            env[k] = v
    return env

def write_env(values):
    backup_path = ENV_PATH + ".bak"
    if os.path.exists(ENV_PATH):
        os.rename(ENV_PATH, backup_path)
    try:
        with open(ENV_PATH, "w") as f:
            for k, v in values.items():
                f.write(f"{k}={v}\n")
    except Exception as e:
        if os.path.exists(backup_path):
            os.rename(backup_path, ENV_PATH)
        raise e
    if os.path.exists(backup_path):
        os.remove(backup_path)

def read_yaml():
    if not os.path.exists(YAML_PATH):
        return {}
    with open(YAML_PATH, "r") as f:
        return yaml.safe_load(f)

def write_yaml(values):
    backup_path = YAML_PATH + ".bak"
    if os.path.exists(YAML_PATH):
        os.rename(YAML_PATH, backup_path)
    try:
        with open(YAML_PATH, "w") as f:
            yaml.safe_dump(values, f)
    except Exception as e:
        if os.path.exists(backup_path):
            os.rename(backup_path, YAML_PATH)
        raise e
    if os.path.exists(backup_path):
        os.remove(backup_path)

@router.get("/env")
def get_env():
    return read_env()

@router.post("/env")
def post_env(config: EnvConfig):
    # Only allow updates to whitelisted keys
    WHITELISTED_ENV_KEYS = [
        "OPENAI_API_KEY",
        "GEMINI_API_KEY",
        "OPENWEATHERMAP_API_KEY",
        "GOOGLE_CALENDAR_CLIENT_ID",
        "GOOGLE_CALENDAR_CLIENT_SECRET",
        "GOOGLE_CALENDAR_ID",
        "GOOGLE_CALENDAR_CREDENTIALS_JSON",
        "SQLITE_DB_PATH",
        "CHROMA_DB_PATH"
    ]
    if not config.values:
        raise HTTPException(status_code=400, detail="No config values provided.")
    for k in config.values.keys():
        if k not in WHITELISTED_ENV_KEYS:
            raise HTTPException(status_code=403, detail=f"Key '{k}' is not allowed.")
    try:
        write_env(config.values)
        # Audit log entry
        config_audit_log.append({
            "action": "env_update",
            "keys": list(config.values.keys()),
            "values": {k: config.values[k] for k in config.values},
            "user": "unknown",  # Replace with user info if available
        })
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write .env: {str(e)}")

@router.get("/yaml")
def get_yaml():
    return read_yaml()

@router.post("/yaml")
def post_yaml(config: YamlConfig):
    # Only allow updates to whitelisted keys
    WHITELISTED_YAML_KEYS = [
        "agent_backends", "default_backend", "agents", "settings"
    ]
    if not config.values:
        raise HTTPException(status_code=400, detail="No config values provided.")
    for k in config.values.keys():
        if k not in WHITELISTED_YAML_KEYS:
            raise HTTPException(status_code=403, detail=f"Key '{k}' is not allowed.")
    try:
        write_yaml(config.values)
        # Audit log entry
        config_audit_log.append({
            "action": "yaml_update",
            "keys": list(config.values.keys()),
            "values": {k: config.values[k] for k in config.values},
            "user": "unknown",  # Replace with user info if available
        })
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write YAML: {str(e)}")

# In-memory error log for config actions
config_errors = []
config_audit_log = []

class ConfigError(BaseModel):
    error: str
    context: str = ""

@router.post("/error")
def log_config_error(err: ConfigError):
    config_errors.append({"error": err.error, "context": err.context})
    return {"status": "logged"}

@router.get("/error")
def get_config_errors():
    return config_errors

@router.get("/audit")
def get_config_audit():
    return config_audit_log

@router.get("/validate")
def validate_env_config():
    required_keys = [
        "OPENAI_API_KEY",
        "GEMINI_API_KEY",
        "OPENWEATHERMAP_API_KEY",
        "GOOGLE_CALENDAR_CLIENT_ID",
        "GOOGLE_CALENDAR_CLIENT_SECRET",
        "GOOGLE_CALENDAR_ID",
        "GOOGLE_CALENDAR_CREDENTIALS_JSON",
        "SQLITE_DB_PATH",
        "CHROMA_DB_PATH"
    ]
    env = read_env()
    missing = []
    placeholders = []
    for key in required_keys:
        val = env.get(key, "")
        if not val:
            missing.append(key)
        elif "your-" in val or val.endswith("-here"):
            placeholders.append(key)
    return {
        "missing": missing,
        "placeholders": placeholders,
        "valid": len(missing) == 0 and len(placeholders) == 0
    }
