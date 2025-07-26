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

from orchestrator import Orchestrator
from dev_team import DevTeam
from admin import Admin
from message_bus import MessageBus

def capture_output(func, *args, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        func(*args, **kwargs)
    return buf.getvalue()

def test_feature_request():
    dev_team = DevTeam()
    admin = Admin()
    orchestrator = Orchestrator(dev_team, admin)
    bus = MessageBus()
    bus.register("feature_request", lambda req: dev_team.implement_feature(req))
    bus.register("meeting_request", lambda details: admin.schedule_meeting(details))

    orchestrator.log("Received feature request from user.")
    result = bus.send("feature_request", "Test Feature")
    dev_team.log(result)
    admin.notify_user(result)
    output = capture_output(lambda: admin.notify_user(result))
    assert "Notifying user: Feature 'Test Feature' implemented." in output

def test_meeting_request():
    dev_team = DevTeam()
    admin = Admin()
    orchestrator = Orchestrator(dev_team, admin)
    bus = MessageBus()
    bus.register("feature_request", lambda req: dev_team.implement_feature(req))
    bus.register("meeting_request", lambda details: admin.schedule_meeting(details))

    orchestrator.log("Received meeting request from user.")
    result = bus.send("meeting_request", "Test Meeting at 10am")
    admin.log_action(result)
    admin.notify_user(result)
    output = capture_output(lambda: admin.notify_user(result))
    assert "Notifying user: Meeting scheduled: Test Meeting at 10am" in output

def test_invalid_message_type():
    dev_team = DevTeam()
    admin = Admin()
    orchestrator = Orchestrator(dev_team, admin)
    bus = MessageBus()
    output = capture_output(lambda: bus.send("unknown_type", "payload"))
    assert "No handler for message type: unknown_type" in output

def test_escalation_stub():
    dev_team = DevTeam()
    admin = Admin()
    orchestrator = Orchestrator(dev_team, admin)
    # Simulate an escalation (stub)
    output = capture_output(lambda: orchestrator.escalate("Simulated issue"))
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
