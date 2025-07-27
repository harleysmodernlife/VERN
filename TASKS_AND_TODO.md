# VERN Tasks & TODO

---

# AI Contributor Workflow & Sprint Protocol

- **Sprint Planning:**  
  - Break work into atomic, testable chunks (feature, test, doc, or bugfix).
  - Use TASKS_AND_TODO.md to track sprint goals, blockers, and context.
  - Summarize sprint plan and context at the top of this file.

- **Local Commits:**  
  - Commit after each working feature, test, or doc update.
  - Use clear, descriptive commit messages (e.g., "feat: add live dashboard tool invocation").
  - Do NOT push to remote until milestone is reached and all tests pass.

- **Push to Remote:**  
  - Only push after a sprint milestone (e.g., dashboard live, workflow working, all tests green).
  - Before push:  
    - Run all tests (manual and automated).
    - Update docs and context summary.
    - Human review/approval if possible.
    - Tag the commit with the sprint/milestone (e.g., "sprint-1-complete").

- **Branching:**  
  - Use feature branches for major new features or risky changes.
  - Merge to main only after review and test pass.

- **Checkpoints & Summaries:**  
  - After each sprint, checkpoint the context (summary of what’s done, what’s next, known issues).
  - Log in TASKS_AND_TODO.md and CHANGELOG.md.

- **Validation & Feedback:**  
  - Never push untested or unreviewed code.
  - Use integration tests and manual checks for all new features.
  - If unsure, checkpoint locally and ask for human review before push.
  - After each sprint, review what worked, what broke, and what needs to change.

- **Reference:**  
  - See SECURITY_AND_GIT_GUIDELINES.md for git hygiene and best practices.

---

# MCP Server & Tool API Feedback / TODO

- [ ] Gather feedback from users and agents on MCP tool usability (Inspector, CLI, etc.)
- [ ] Track issues, feature requests, and pain points for all tools (echo, add, file ops, cluster_status, etc.)
- [ ] Prioritize improvements and bugfixes based on feedback.
- [ ] Document UI/extension progress and integration plans.
- [ ] Keep all docs up to date as changes are made.

---

## Completed/Ongoing (2025-07)

- [x] Expose agent/cluster actions as MCP tools (schedule_event, journal_entry, finance_balance, get_user_profile, etc.)
- [x] Integrate context/memory: journal_entry logs to DB, get_user_profile fetches from DB.
- [x] Create minimal cockpit/dashboard UI prototype (vern_dashboard.html).
- [x] Update README and AGENT_GUIDES for new tools and context features.
- [x] Add/adjust integration tests for all MCP tools.
- [ ] Gather feedback on dashboard UI and context-aware tools.

## Immediate Next Steps

- [ ] Connect vern_dashboard.html to MCP server for live tool invocation (AJAX/WebSocket).
- [ ] Expand dashboard UI: show agent/cluster status, logs, and workflow history.
- [ ] Add/expand cross-domain workflows (e.g., "plan my week", "daily health check-in").
- [ ] Update AGENT_GUIDES/CLUSTER.md files with new tool and context info.
- [ ] Update CHANGELOG.md for all recent changes.
- [ ] Review and update KNOWN_ISSUES_AND_GOTCHAS.md for DB/MCP/UI caveats.

---

## Longer-Term

- [ ] Add system prompt support and agent tool-calling for advanced LLMs.
- [ ] Modularize agent tool integration (code execution, web search, etc.).
- [ ] Add web/chat UI for user experience upgrade.
- [ ] Expand automated test coverage for all agent workflows.
- [ ] Monitor Ollama and Hugging Face for new model releases and update backends as needed.
- [ ] Continue improving accessibility and internationalization.
- [ ] Design and implement plugin/extension API for third-party integrations.

---

## See Also

- [QUICKSTART.md](QUICKSTART.md)
- [AGENT_GUIDES/README.md](AGENT_GUIDES/README.md)
- [MVP_IMPLEMENTATION_PLAN.md](MVP_IMPLEMENTATION_PLAN.md)
- [KNOWN_ISSUES_AND_GOTCHAS.md](KNOWN_ISSUES_AND_GOTCHAS.md)
