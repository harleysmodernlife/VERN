"""
MVP CLI Entry Point

Simulates user interaction with the Orchestrator, Dev Team, Admin, Knowledge Broker, and Security/Privacy clusters.
"""

from orchestrator import Orchestrator
from dev_team import DevTeam
from admin import Admin
from knowledge_broker import KnowledgeBroker
from security_privacy import SecurityPrivacy
from message_bus import MessageBus

def main():
    print("=== VERN MVP CLI ===")
    dev_team = DevTeam()
    admin = Admin()
    knowledge_broker = KnowledgeBroker()
    security_privacy = SecurityPrivacy()
    orchestrator = Orchestrator(dev_team, admin)
    bus = MessageBus()

    # Register handlers for message types
    bus.register("feature_request", lambda req: dev_team.implement_feature(req))
    bus.register("meeting_request", lambda details: admin.schedule_meeting(details))
    bus.register("context_lookup", lambda query: knowledge_broker.context_lookup(query))
    bus.register("cross_cluster_query", lambda req: knowledge_broker.cross_cluster_query(req))
    bus.register("security_check", lambda action: security_privacy.monitor_action(action))

    while True:
        print("\nOptions:")
        print("1. Request new feature")
        print("2. Schedule meeting")
        print("3. Knowledge Broker: Context lookup")
        print("4. Knowledge Broker: Cross-cluster query")
        print("5. Security/Privacy: Monitor action")
        print("6. Exit")
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
            query = input("Enter context to look up: ").strip()
            result = bus.send("context_lookup", query)
            knowledge_broker.log(result)
        elif choice == "4":
            req = input("Enter cross-cluster query: ").strip()
            result = bus.send("cross_cluster_query", req)
            knowledge_broker.log(result)
        elif choice == "5":
            action = input("Enter action to monitor for security/privacy: ").strip()
            result = bus.send("security_check", action)
            security_privacy.log(result)
        elif choice == "6":
            print("Exiting MVP CLI.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
