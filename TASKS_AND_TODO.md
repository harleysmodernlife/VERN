# VERN Tasks & TODO

---

# Context Checkpoint (2025-07-27)

**Current Sprint:**  
- Refactor agent and chat code to use direct Python tool calls (not MCP).
- Document MCP limitations and future plans for integration.
- Continue building modular clusters, persistent memory, and logging.

**Blockers:**  
- MCP proxy/server does not support direct tool invocation from Python/browser clients.
- Browser-based UIs (Inspector, dashboard) may fail to connect to MCP proxy due to missing CORS headers.

**Next Steps:**  
- [x] Update README.md to reflect new MVP approach (direct Python tool calls).
- [ ] Refactor tool definitions to Python functions (e.g., in src/mvp/tool_interface.py).
- [ ] Update agent/chat code (src/mvp/cli.py) to call tool functions directly.
- [ ] Test agent+tools end-to-end in CLI chat.
- [ ] Update docs and logs after each confirmed change.
- [ ] Add to KNOWN_ISSUES_AND_GOTCHAS.md: MCP limitations, CORS issues, and future plans.
- [ ] Plan for future MCP integration when ecosystem matures.

---

# AI Contributor Workflow & Sprint Protocol

- **Sprint Planning:**  
  - Break work into atomic, testable chunks (feature, test, doc, or bugfix).
  - Use TASKS_AND_TODO.md to track sprint goals, blockers, and context.
  - Summarize sprint plan and context at the top of this file.

- **Local Commits:**  
  - Commit after each working feature, test, or doc update.
  - Use clear, descriptive commit messages (e.g., "feat: refactor tool invocation to Python functions").
  - Do NOT push to remote until milestone is reached and all tests pass.

- **Push to Remote:**  
  - Only push after a sprint milestone (e.g., agent+tools working, all tests green).
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

# Known Issues & Gotchas

- MCP proxy/server does not support direct tool invocation from Python/browser clients.
- Browser-based UIs (Inspector, dashboard) may fail to connect to MCP proxy due to missing CORS headers.
- For MVP, tools are called directly in Python.
- See README.md and KNOWN_ISSUES_AND_GOTCHAS.md for details.

---

## Completed/Ongoing (2025-07)

- [x] Expose agent/cluster actions as MCP tools (schedule_event, journal_entry, finance_balance, get_user_profile, etc.)
- [x] Integrate context/memory: journal_entry logs to DB, get_user_profile fetches from DB.
- [x] Create minimal cockpit/dashboard UI prototype (vern_dashboard.html).
- [x] Update README and AGENT_GUIDES for new tools and context features.
- [x] Add/adjust integration tests for all MCP tools.
- [ ] Gather feedback on dashboard UI and context-aware tools.

## Immediate Next Steps

- [ ] Refactor tool code and agent logic for direct Python calls.
- [ ] Test agent+tools end-to-end in CLI chat.
- [ ] Update docs and logs after each confirmed change.
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
