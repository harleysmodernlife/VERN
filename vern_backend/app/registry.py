import json
import os
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/registry", tags=["registry"])

REGISTRY_PATH = "vern_backend/registry.json"

class RegistryEntry(BaseModel):
    name: str
    type: str  # "plugin", "agent", etc.
    metadata: dict = {}

def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        return []
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)

def save_registry(entries):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(entries, f, indent=2)

@router.get("/", response_model=list[RegistryEntry])
def list_registry():
    return load_registry()

@router.post("/")
def add_registry_entry(entry: RegistryEntry):
    entries = load_registry()
    entries.append(entry.dict())
    save_registry(entries)
    return {"status": "added", "name": entry.name}
