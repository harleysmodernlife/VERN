# Agent Guide: Admin Cluster

**Read first, then amend docs—never assume state. Never truncate with “remains unchanged”—always show full, updated context. Keep this file up to date after each confirmed change. Work as a team. Watch for gotchas and snags. Your work will be tested—be mindful of each task. Evaluate your work with a critical eye for errors.**

---

## Role & Purpose

The Admin Cluster manages scheduling, calendar, reminders, file management, permissions, and logistics. It ensures smooth operation, organization, and resource allocation for VERN and its users.

---

## Team Structure & Roles

- **Admin Lead:** Oversees Admin cluster, coordinates with orchestrator and other clusters.
- **Scheduler:** Manages events, reminders, and deadlines.
- **File Manager:** Handles file organization, storage, and retrieval.
- **Permissions Agent:** Manages access control and user permissions.
- **Log Keeper:** Maintains records of actions, changes, and issues.

## Protocols

- Receive requests from orchestrator, clusters, or user.
- Schedule and track events, reminders, and deadlines.
- Manage files, permissions, and access control.
- Log all actions, changes, and issues for transparency.

---

## Gotchas & Edge Cases

- Avoid scheduling conflicts and resource contention.
- Watch for permission errors and unauthorized access.
- Ensure reminders and notifications are timely and reliable.
- Document all changes to schedules, files, and permissions.

---

## Integration Points

- Coordinate with Dev Team for deployment and resource scheduling.
- Interface with Research cluster for document management and knowledge sharing.
- Collaborate with Security/Privacy cluster for permission audits and compliance.
- Escalate conflicts or complex scheduling/resource issues to the orchestrator.

---

## MCP Tool: schedule_event

- The Admin cluster exposes a `schedule_event` tool via the MCP server.
- This tool allows scheduling meetings/events from the CLI, Inspector, or dashboard UI.
- All scheduled events are logged for transparency and can be integrated into cross-domain workflows.
- See [vern_dashboard.html](../vern_dashboard.html) for a prototype UI.

## Best Practices

- Maintain clear, up-to-date records of all admin actions.
- Communicate changes and conflicts to relevant clusters and users.
- Regularly audit permissions and resource usage.
- Update this guide as protocols or logic evolve.

---

**Stay aligned with VERN’s values and guidelines. The Admin Cluster is essential for organization, reliability, and user support.**
