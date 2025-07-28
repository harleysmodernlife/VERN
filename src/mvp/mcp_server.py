"""
Minimal VERN-Native MCP Server

Implements two example tools:
- echo: returns the input string
- add: returns the sum of two numbers

Compatible with MCP CLI (`mcp dev src/mvp/mcp_server.py`).
Extensible: see instructions at the end of this file.

Author: VERN Team
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from mcp.server.fastmcp import FastMCP

# Import agent clusters for tool integration
from src.mvp.admin import Admin
from src.mvp.health_wellness import HealthWellness
from src.mvp.finance_resource import FinanceResource

import sqlite3
import json

# Global FastMCP server object for MCP CLI discovery
mcp = FastMCP("vern-demo")

@mcp.tool()
def echo(text: str) -> str:
    """Return the input string."""
    return text

@mcp.tool()
def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b

@mcp.tool()
def file_read(path: str, encoding: str = "utf-8") -> str:
    """
    Read the contents of a text file.
    Args:
        path: Path to the file.
        encoding: File encoding (default: utf-8).
    Returns:
        File contents as a string.
    Raises:
        FileNotFoundError if the file does not exist.
        UnicodeDecodeError if the file cannot be decoded.
    """
    with open(path, "r", encoding=encoding) as f:
        return f.read()

@mcp.tool()
def file_write(path: str, content: str, encoding: str = "utf-8", overwrite: bool = True) -> str:
    """
    Write content to a text file.
    Args:
        path: Path to the file.
        content: Text to write.
        encoding: File encoding (default: utf-8).
        overwrite: If False, will not overwrite existing files.
    Returns:
        Confirmation message.
    Raises:
        FileExistsError if overwrite is False and file exists.
    """
    import os
    if not overwrite and os.path.exists(path):
        raise FileExistsError(f"File already exists: {path}")
    with open(path, "w", encoding=encoding) as f:
        f.write(content)
    return f"Wrote to {path}"

@mcp.tool()
def file_list(directory: str = ".", glob_pattern: str = "*") -> list[str]:
    """
    List files in a directory matching a glob pattern.
    Args:
        directory: Directory to list (default: current).
        glob_pattern: Glob pattern (default: '*').
    Returns:
        List of file paths.
    """
    import glob
    import os
    pattern = os.path.join(directory, glob_pattern)
    return glob.glob(pattern)

@mcp.tool()
def file_delete(path: str) -> str:
    """
    Delete a file.
    Args:
        path: Path to the file.
    Returns:
        Confirmation message.
    Raises:
        FileNotFoundError if the file does not exist.
    """
    import os
    os.remove(path)
    return f"Deleted {path}"

@mcp.tool()
def cluster_status() -> dict:
    """
    Return the status of all agent clusters (stub/demo).
    Returns:
        Dictionary with cluster names and status.
    """
    # In a real implementation, this would query live agent/cluster objects.
    return {
        "archetype_phoenix": "online",
        "dev_team": "online",
        "admin": "online",
        "research": "online",
        "finance_resource": "online",
        "health_wellness": "online",
        "learning_education": "online",
        "social_relationship": "online",
        "security_privacy": "online",
        "environment_systems": "online",
        "legal_compliance": "online",
        "creativity_media": "online",
        "career_work": "online",
        "travel_logistics": "online",
        "orchestrator": "online",
        "emergent_agent": "online",
        "knowledge_broker": "online",
        "id10t_monitor": "online"
    }

@mcp.tool()
def schedule_event(details: str, user_id: int = None) -> str:
    """
    Schedule a meeting or event via the Admin agent.
    Args:
        details: Description of the event (who, what, when, where).
        user_id: Optional user ID for logging.
    Returns:
        Confirmation message from the Admin agent.
    """
    admin = Admin()
    return admin.schedule_meeting(details, user_id=user_id)

@mcp.tool()
def journal_entry(entry: str, user_id: int = None) -> str:
    """
    Add a health/wellness journal entry via the HealthWellness agent and log to DB.
    Args:
        entry: Journal text or prompt.
        user_id: Optional user ID for logging.
    Returns:
        Confirmation or result from the HealthWellness agent.
    """
    hw = HealthWellness()
    result = hw.handle_request(f"journal: {entry}", user_id=user_id)
    # Log journal entry to actions table for persistence
    try:
        from src.db.logger import log_action
        hw_agent_id = getattr(hw, "agent_id", 8)
        log_action(hw_agent_id, user_id, "journal_entry", {"entry": entry}, status="success")
    except Exception as e:
        result += f" [Warning: failed to log journal entry: {e}]"
    return result

@mcp.tool()
def get_user_profile(user_id: int) -> dict:
    """
    Retrieve a user profile from the database.
    Args:
        user_id: The user's ID.
    Returns:
        Dictionary of user profile data, or empty dict if not found.
    """
    try:
        conn = sqlite3.connect("db/vern.db")
        cur = conn.cursor()
        cur.execute("SELECT username, profile_data FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            username, profile_data = row
            profile = json.loads(profile_data) if profile_data else {}
            profile["username"] = username
            profile["user_id"] = user_id
            return profile
        else:
            return {}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def finance_balance(user_id: int = None) -> str:
    """
    Check finance/resource balance via the FinanceResource agent.
    Args:
        user_id: Optional user ID for logging.
    Returns:
        Balance or result from the FinanceResource agent.
    """
    fr = FinanceResource()
    return fr.handle_request("balance", user_id=user_id)

# For direct execution (optional)
if __name__ == "__main__":
    import asyncio
    async def main():
        await mcp.run_stdio()
    asyncio.run(main())

"""
How to extend this server:
How to extend this server:

1. Add a new @mcp.tool() function with your desired signature and docstring.
2. The function name becomes the tool name.
3. Input arguments become the tool's input schema.
4. The return value is sent as the tool's output.
5. Use type hints and docstrings for auto-generated schemas and docs.
6. Test with: mcp dev src/mvp/mcp_server.py

Examples: see echo, add, file_read, file_write, file_list, file_delete above.
"""
