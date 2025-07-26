"""
MVP CLI Entry Point

Simulates user interaction with the Orchestrator, Dev Team, and Admin clusters.
"""

from orchestrator import Orchestrator
from dev_team import DevTeam
from admin import Admin
from message_bus import MessageBus

def main():
    print("=== VERN MVP CLI ===")
    dev_team = DevTeam()
    admin = Admin()
    orchestrator = Orchestrator(dev_team, admin)
    bus = MessageBus()

    # Register handlers for message types
    bus.register("feature_request", lambda req: dev_team.implement_feature(req))
    bus.register("meeting_request", lambda details: admin.schedule_meeting(details))

    while True:
        print("\nOptions:")
        print("1. Request new feature")
        print("2. Schedule meeting")
        print("3. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            feature = input("Describe the feature to implement: ").strip()
            orchestrator.log("Received feature request from user.")
            result = bus.send("feature_request", feature)
            dev_team.log(result)
            admin.notify_user(result)
        elif choice == "2":
            details = input("Enter meeting details: ").strip()
            orchestrator.log("Received meeting request from user.")
            result = bus.send("meeting_request", details)
            admin.log_action(result)
            admin.notify_user(result)
        elif choice == "3":
            print("Exiting MVP CLI.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
