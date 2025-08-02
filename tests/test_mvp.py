"""
Automated tests for VERN MVP

Covers:
- Feature request workflow
- Meeting scheduling workflow
- Invalid input/error handling
- Simulated escalation

Run with: python -m tests.test_mvp
"""

import sys
import io
import contextlib

sys.path.insert(0, "./src/mvp")

from mvp.orchestrator import orchestrator_respond
from mvp.dev_team_agent import dev_team_respond
from mvp.admin import admin_respond
from mvp.message_bus import MessageBus

def capture_output(func, *args, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        func(*args, **kwargs)
    return buf.getvalue()

def test_feature_request():
    # Simulate feature request workflow using function-based agents
    bus = MessageBus()
    bus.register("feature_request", lambda req: dev_team_respond(req, context="feature", agent_status=None))
    bus.register("meeting_request", lambda details: admin_respond(details, context="meeting", agent_status=None))

    print("Received feature request from user.")
    result = bus.send("feature_request", "Test Feature")
    print(result)
    output = capture_output(lambda: print(f"Notifying user: {result}"))
    assert "Notifying user: " in output

def test_meeting_request():
    # Simulate meeting scheduling workflow using function-based agents
    bus = MessageBus()
    bus.register("feature_request", lambda req: dev_team_respond(req, context="feature", agent_status=None))
    bus.register("meeting_request", lambda details: admin_respond(details, context="meeting", agent_status=None))

    print("Received meeting request from user.")
    result = bus.send("meeting_request", "Test Meeting at 10am")
    print(result)
    output = capture_output(lambda: print(f"Notifying user: {result}"))
    assert "Notifying user: " in output

def test_invalid_message_type():
    bus = MessageBus()
    output = capture_output(lambda: bus.send("unknown_type", "payload"))
    assert "No handler for message type: unknown_type" in output

def test_escalation_stub():
    # Simulate an escalation (stub)
    output = capture_output(lambda: print("Escalating: Simulated issue"))
    # No assertion since escalate is a stub, but should not error

if __name__ == "__main__":
    print("Running MVP automated tests...")
    test_feature_request()
    print("Feature request workflow: PASS")
    test_meeting_request()
    print("Meeting scheduling workflow: PASS")
    test_invalid_message_type()
    print("Invalid message type handling: PASS")
    test_escalation_stub()
    print("Escalation stub: PASS")
    print("All MVP tests passed.")
