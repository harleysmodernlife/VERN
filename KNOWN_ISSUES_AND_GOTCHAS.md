# Known Issues & Gotchas

**Purpose:**  
Track architectural risks, integration pitfalls, and recurring “gotchas” for VERN. Update this file as new issues are discovered or resolved.

---

## Integration Complexity

- **Description:** Modular agents require robust orchestration and message passing. Integration bugs or unclear protocols can cause agents to “talk past each other.”
- **Example:** Dev Team and Admin both update a schedule, but changes are not synchronized.
- **Mitigation:** Start with a minimal working system (MVP). Add complexity gradually. Test integration points early and often.
- **Status:** MVP validated (manual and automated tests passed).

---

## Context Loss & Escalation Loops

- **Description:** Agents may escalate too often or not enough, leading to bottlenecks or missed context.
- **Example:** Admin cluster escalates every permission check, overwhelming the Orchestrator.
- **Mitigation:** Log and review all escalations. Tune escalation protocols based on real usage.
- **Status:** MVP validated (manual and automated tests passed).

---

## Doc/Code Drift

- **Description:** Documentation and code can get out of sync, especially with many prompt/behavior specs.
- **Example:** Prompt spec for Dev Team is updated, but main guide is not.
- **Mitigation:** Require doc updates in every PR/code change. Enforce with CONTRIBUTING.md and PR templates.
- **Status:** Protocol in place.

---

## AI Shortcutting or Hallucination

- **Description:** AI agents may ignore cross-links, invent context, or “cheat” on protocols.
- **Example:** Agent answers a prompt without referencing the required guide.
- **Mitigation:** Build in sanity checks (id10t Monitor, Knowledge Broker). Require explicit doc references in agent outputs.
- **Status:** Protocol in place; validated in MVP.

---

## Onboarding & Complexity

- **Description:** The system is complex; new contributors may be overwhelmed.
- **Example:** New dev skips onboarding docs and breaks escalation logic.
- **Mitigation:** Keep QUICKSTART.md and onboarding docs simple and up to date. Add “Doc Discipline” reminders everywhere.
- **Status:** Ongoing.

---

## Performance & Scaling

- **Description:** Many agents, logs, and escalations could slow down the system.
- **Example:** Excessive logging or escalations cause delays in user response.
- **Mitigation:** Profile early. Optimize only after a working baseline is established.
- **Status:** To be monitored after MVP.

---

## Lessons Learned from MVP

- Manual and automated tests both passed, confirming workflows and error handling.
- CLI experience matches documentation and user expectations.
- Invalid input is handled gracefully.

## Lessons Learned from DB Logging Integration

- DB logging is robust and enables traceability for actions, notifications, and gotchas.
- Automated and manual DB inspection confirmed correct data capture.
- Relative imports in agent files must be robust to working directory.
- Next: Use DB logs for analytics, dashboards, and cross-cluster learning.

**Update this file after every major integration, bug, or lesson learned. Ruthlessly document all gotchas and solutions.**
