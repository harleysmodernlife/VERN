import os
from pathlib import Path
from typing import Optional

DEFAULT_DB_PATH = "./data/vern.sqlite"

def get_sqlite_path(env_var: str = "SQLITE_DB_PATH", default: Optional[str] = None) -> str:
    """
    Resolve the canonical SQLite DB path.
    - Reads env var SQLITE_DB_PATH when set.
    - Defaults to ./data/vern.sqlite unless an explicit default is provided.
    - Ensures parent directory exists (best-effort).
    """
    path = os.environ.get(env_var, default or DEFAULT_DB_PATH)
    # Normalize to absolute path
    p = Path(path).expanduser().resolve()
    parent = p.parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        # Non-fatal: creation may fail in read-only environments; caller will handle errors on connect
        pass
    return str(p)