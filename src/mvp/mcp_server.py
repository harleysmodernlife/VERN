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

# Removed import of finance_resource (moved to FUTURE_AGENTS)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.mcp.server.fastmcp import FastMCP

# Import agent clusters for tool integration
from src.mvp.health_wellness import health_respond
# Removed import of finance_respond (finance_resource moved to FUTURE_AGENTS)

import sqlite3
import json

# Global FastMCP server object for MCP CLI discovery
mcp = FastMCP("vern-demo")

import asyncio

@mcp.tool()
def echo(text: str) -> str:
    """Return the input string."""
    return text

@mcp.tool()
async def echo_async(text: str) -> str:
    """Async: Return the input string after a short delay."""
    await asyncio.sleep(0.01)
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
        # "finance_resource": "online",  # Removed, agent moved to FUTURE_AGENTS
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
    admin = admin()
    return admin.schedule_meeting(details, user_id=user_id)

@mcp.tool()
def journal_entry(entry: str, user_id: int = None) -> str:
    """
    Add a health/wellness journal entry via the health_respond function and log to DB.
    Args:
        entry: Journal text or prompt.
        user_id: Optional user ID for logging.
    Returns:
        Confirmation or result from the Health/Wellness agent.
    """
    # Use health_respond directly (no HealthWellness class)
    result = health_respond(f"journal: {entry}", context="", user_id=user_id)
    # Log journal entry to actions table for persistence
    try:
        from src.db.logger import log_action
        log_action("health_wellness", user_id, "journal_entry", {"entry": entry}, status="success")
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
# Removed finance_balance tool (finance_resource agent moved to FUTURE_AGENTS)

# --- MCP Plugin Tools ---

@mcp.tool()
def chromadb_query(query: str, top_k: int = 3) -> str:
    """
    Query ChromaDB for relevant documents/knowledge.
    Args:
        query: Query string.
        top_k: Number of top results to return.
    Returns:
        String with top matching documents or error.
    """
    import os
    from dotenv import load_dotenv
    import chromadb

    # Always load .env for config
    load_dotenv(dotenv_path=".env")
    db_path = os.getenv("CHROMA_DB_PATH", "./chroma_data/")
    try:
        client = chromadb.PersistentClient(path=db_path)
        collection = client.get_or_create_collection("vern_docs")
        results = collection.query(query_texts=[query], n_results=top_k)
        docs = results.get("documents", [[]])[0]
        if not docs:
            return "No relevant documents found."
        return "\n\n".join(docs)
    except Exception as e:
        return f"ChromaDB error: {e}"


@mcp.tool()
def get_weather(location: str) -> str:
    """
    Provides real weather information for a given location using OpenWeatherMap API.
    Args:
        location: Name of the city or region.
    Returns:
        Weather description string or error message.
    """
    import os
    import requests
    from dotenv import load_dotenv

    # Always load .env for config
    load_dotenv(dotenv_path=".env")

    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        return "Weather API key not set. Please set OPENWEATHERMAP_API_KEY in your .env file."

    try:
        # Step 1: Geocode city name to lat/lon
        geo_url = "https://api.openweathermap.org/geo/1.0/direct"
        geo_params = {"q": location, "limit": 1, "appid": api_key}
        geo_resp = requests.get(geo_url, params=geo_params, timeout=10)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()
        if not geo_data or "lat" not in geo_data[0] or "lon" not in geo_data[0]:
            return f"Could not find coordinates for '{location}'."
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        # Step 2: Fetch weather data
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric"
        }
        weather_resp = requests.get(weather_url, params=weather_params, timeout=10)
        weather_resp.raise_for_status()
        weather = weather_resp.json()

        # Step 3: Format output
        desc = weather["weather"][0]["description"].capitalize() if weather.get("weather") else "N/A"
        temp = weather["main"]["temp"] if "main" in weather and "temp" in weather["main"] else "N/A"
        humidity = weather["main"]["humidity"] if "main" in weather and "humidity" in weather["main"] else "N/A"
        wind = weather["wind"]["speed"] if "wind" in weather and "speed" in weather["wind"] else "N/A"
        city = weather.get("name", location)
        country = weather.get("sys", {}).get("country", "")

        return (
            f"Weather for {city}, {country}:\n"
            f"- {desc}\n"
            f"- Temperature: {temp}°C\n"
            f"- Humidity: {humidity}%\n"
            f"- Wind speed: {wind} m/s"
        )
    except requests.exceptions.RequestException as e:
        return f"Weather API error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


@mcp.tool()
def fileops_list_files(directory: str = ".") -> list:
    """
    Securely lists files in a directory under the project root.
    Args:
        directory: Directory path (relative to project root).
    Returns:
        List of filenames or error.
    """
    import os
    from pathlib import Path

    BASE_DIR = Path(os.getcwd()).resolve()
    try:
        target_dir = (BASE_DIR / directory).resolve()
        if not str(target_dir).startswith(str(BASE_DIR)):
            return [f"Access denied: directory traversal outside project root."]
        if not target_dir.is_dir():
            return [f"Not a directory: {target_dir}"]
        return [f.name for f in target_dir.iterdir()]
    except Exception as e:
        return [f"Error listing files: {e}"]

@mcp.tool()
def fileops_read_file(path: str) -> str:
    """
    Securely reads the contents of a file under the project root.
    Args:
        path: Path to the file (relative to project root).
    Returns:
        File contents as a string or error.
    """
    import os
    from pathlib import Path

    BASE_DIR = Path(os.getcwd()).resolve()
    try:
        target_file = (BASE_DIR / path).resolve()
        if not str(target_file).startswith(str(BASE_DIR)):
            return "Access denied: file traversal outside project root."
        if not target_file.is_file():
            return f"Not a file: {target_file}"
        with open(target_file, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

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
