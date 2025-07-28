import httpx

MCP_URL = "http://127.0.0.1:6277"

def call_tool(tool, params):
    resp = httpx.post(f"{MCP_URL}/tools/{tool}/invoke", json={"input": params})
    resp.raise_for_status()
    return resp.json().get("output")

def main():
    print("Testing MCP tools via HTTP API...")

    # Echo
    assert call_tool("echo", {"text": "hello"}) == "hello"
    print("echo: PASS")

    # Add
    assert call_tool("add", {"a": 2, "b": 3}) == 5
    print("add: PASS")

    # Cluster status
    status = call_tool("cluster_status", {})
    assert isinstance(status, dict) and "dev_team" in status
    print("cluster_status: PASS")

    # Schedule event
    result = call_tool("schedule_event", {"details": "Team sync at 10am"})
    assert "Meeting scheduled" in result
    print("schedule_event: PASS")

    # Journal entry
    result = call_tool("journal_entry", {"entry": "Today I felt great"})
    assert "Health/Wellness result" in result or "journal" in result.lower()
    print("journal_entry: PASS")

    # Finance balance
    result = call_tool("finance_balance", {})
    assert "Finance/Resource result" in result or "balance" in result.lower()
    print("finance_balance: PASS")

    # Get user profile (may be empty if no user 1)
    profile = call_tool("get_user_profile", {"user_id": 1})
    assert isinstance(profile, dict)
    print("get_user_profile: PASS")

    print("All MCP tool HTTP tests passed.")

if __name__ == "__main__":
    main()
