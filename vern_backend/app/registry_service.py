import os
import sqlite3
import threading
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

# Persistence path centralized via helper (env SQLITE_DB_PATH or default '/app/data/vern.sqlite')
from vern_backend.app.db_path import get_sqlite_path
# Preserve explicit environment override if provided, else use helper
DB_PATH = os.environ.get("SQLITE_DB_PATH") or get_sqlite_path()

# Dual thresholds for agent TTL/heartbeat
DEFAULT_ONLINE_TTL = int(os.environ.get("AGENT_ONLINE_TTL", "60"))    # online if age < 60s
DEFAULT_OFFLINE_TTL = int(os.environ.get("AGENT_OFFLINE_TTL", "300")) # offline if age ≥ 300s


@dataclass
class AgentRecord:
    name: str                  # unique agent name (e.g., 'research', 'finance', 'orchestrator')
    cluster: str               # logical grouping (e.g., 'Research', 'Finance')
    status: str                # 'online' | 'offline' | 'stale'
    capabilities: Optional[str] = None  # JSON/text description (optional)
    last_seen: Optional[float] = None   # epoch seconds
    meta: Optional[str] = None          # JSON/text metadata


class AgentRegistry:
    """
    In-memory cache with optional SQLite persistence for agent status/metadata.
    Thread-safe with a simple lock. Intended to be used as a singleton per-process.
    """
    def __init__(self, db_path: str = DB_PATH, online_ttl: int = DEFAULT_ONLINE_TTL, offline_ttl: int = DEFAULT_OFFLINE_TTL):
        self.db_path = db_path
        # Ensure sane ordering of thresholds
        self.online_ttl = max(1, int(online_ttl))
        self.offline_ttl = max(self.online_ttl + 1, int(offline_ttl))
        self._lock = threading.RLock()
        self._agents: Dict[str, AgentRecord] = {}
        self._ensure_db()

    # --- SQLite setup & helpers ---

    def _ensure_parent_dir(self, path: str):
        parent = os.path.dirname(path or "")
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)

    def _ensure_db(self):
        self._ensure_parent_dir(self.db_path)
        con = sqlite3.connect(self.db_path)
        try:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS agents (
                    name TEXT PRIMARY KEY,
                    cluster TEXT,
                    status TEXT,
                    capabilities TEXT,
                    last_seen REAL,
                    meta TEXT
                )
                """
            )
            con.execute("CREATE INDEX IF NOT EXISTS idx_agents_cluster ON agents(cluster)")
            con.commit()
        finally:
            con.close()
        # Warm in-memory cache from DB
        self._load_from_db()

    def _load_from_db(self):
        with self._connect() as con, self._lock:
            cur = con.execute("SELECT name, cluster, status, capabilities, last_seen, meta FROM agents")
            rows = cur.fetchall()
            self._agents.clear()
            for name, cluster, status, capabilities, last_seen, meta in rows:
                rec = AgentRecord(
                    name=name,
                    cluster=cluster,
                    status=status,
                    capabilities=capabilities,
                    last_seen=last_seen,
                    meta=meta,
                )
                # Cache raw; status is derived on read via _apply_ttl
                self._agents[name] = rec

    def _connect(self):
        return sqlite3.connect(self.db_path)

    # --- Public API ---

    def heartbeat(self, name: str, cluster: str, capabilities: Optional[str] = None, meta: Optional[str] = None) -> AgentRecord:
        """
        Upsert an agent on heartbeat, setting status to 'online' and updating last_seen.
        """
        ts = time.time()
        rec = AgentRecord(name=name, cluster=cluster, status="online", capabilities=capabilities, last_seen=ts, meta=meta)
        with self._connect() as con, self._lock:
            con.execute(
                """
                INSERT INTO agents (name, cluster, status, capabilities, last_seen, meta)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    cluster=excluded.cluster,
                    status=excluded.status,
                    capabilities=COALESCE(excluded.capabilities, agents.capabilities),
                    last_seen=excluded.last_seen,
                    meta=COALESCE(excluded.meta, agents.meta)
                """,
                (rec.name, rec.cluster, rec.status, rec.capabilities, rec.last_seen, rec.meta),
            )
            con.commit()
            self._agents[rec.name] = rec
        return rec

    def set_status(self, name: str, status: str):
        """
        Manually set an agent's status (online/offline/stale). Updates DB and cache.
        """
        with self._connect() as con, self._lock:
            con.execute("UPDATE agents SET status=? WHERE name=?", (status, name))
            con.commit()
            if name in self._agents:
                self._agents[name].status = status

    def get(self, name: str) -> Optional[AgentRecord]:
        with self._lock:
            rec = self._agents.get(name)
            if not rec:
                return None
            return self._apply_ttl(rec)

    def list(self, cluster: Optional[str] = None) -> List[AgentRecord]:
        with self._lock:
            records = list(self._agents.values())
            if cluster:
                records = [r for r in records if r.cluster == cluster]
            # Apply TTL on the fly
            return [self._apply_ttl(r) for r in records]

    def _apply_ttl(self, rec: AgentRecord) -> AgentRecord:
        if rec.last_seen is None:
            return rec
        age = time.time() - float(rec.last_seen)
        status: str
        if age < self.online_ttl:
            status = "online"
        elif age < self.offline_ttl:
            status = "stale"
        else:
            status = "offline"
        # Return a copy with derived status
        return AgentRecord(**{**asdict(rec), "status": status})

    def delete(self, name: str):
        with self._connect() as con, self._lock:
            con.execute("DELETE FROM agents WHERE name=?", (name,))
            con.commit()
            self._agents.pop(name, None)

    def clear(self):
        with self._connect() as con, self._lock:
            con.execute("DELETE FROM agents")
            con.commit()
            self._agents.clear()

    # Convenience for API JSON
    @staticmethod
    def to_dict(rec: AgentRecord) -> Dict[str, object]:
        d = asdict(rec)
        # Ensure types are JSON-friendly
        if rec.last_seen is not None:
            d["last_seen"] = float(rec.last_seen)
        return d


# Singleton instance
registry = AgentRegistry()