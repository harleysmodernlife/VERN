# VERN Tasks & TODO

---

# Context Checkpoint (2025-07-28)

**Current Sprint:**  
- Multi-agent orchestration and delegation is now complete and stable.
- CLI chat routes user input through the Orchestrator, which delegates to all LLM-powered clusters and aggregates results.
- Update docs and guides for multi-agent orchestration, context management, and troubleshooting.
- Plan next blocks: tool-calling, RAG (retrieval-augmented generation), agent specialization, and plugin API.

**Blockers:**  
- No real-time tool-calling or RAG yet (LLM-only knowledge).
- MCP proxy/server does not support direct tool invocation from Python/browser clients.
- LLM backend (Ollama/Qwen3) may be slow or error-prone on low-resource hardware.

**Next Steps:**  
- [x] Implement LLM-powered response functions for all clusters.
- [x] Update Orchestrator to parse plans and delegate to clusters.
- [x] Integrate CLI with orchestrator_respond for multi-agent workflows.
- [x] Update README.md, AGENT_GUIDES/README.md, and QUICKSTART.md for multi-agent orchestration.
- [x] Add to KNOWN_ISSUES_AND_GOTCHAS.md: LLM-only knowledge, agent confusion, Ollama troubleshooting.
- [x] Plan for future tool-calling, RAG, and plugin API.
- [ ] Plan and document next sprint: tool-calling, RAG, agent specialization, plugin API, and polish.
- [ ] Update CHANGELOG.md for all recent changes.

---

# AI Contributor Workflow & Sprint Protocol

- **Sprint Planning:**  
  - Break work into atomic, testable chunks (feature, test, doc, or bugfix).
  - Use TASKS_AND_TODO.md to track sprint goals, blockers, and context.
  - Summarize sprint plan and context at the top of this file.

- **Local Commits:**  
  - Commit after each working feature, test, or doc update.
  - Use clear, descriptive commit messages (e.g., "feat: multi-agent orchestration and CLI integration").
  - Do NOT push to remote until milestone is reached and all tests pass.

- **Push to Remote:**  
  - Only push after a sprint milestone (e.g., multi-agent orchestration working, all tests green).
  - Before push:  
    - Run all tests (manual and automated).
    - Update docs and context summary.
    - Human review/approval if possible.
    - Tag the commit with the sprint/milestone (e.g., "sprint-3-multi-agent-orchestration").

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

- No real-time tool-calling or RAG yet (LLM-only knowledge).
- MCP proxy/server does not support direct tool invocation from Python/browser clients.
- LLM backend (Ollama/Qwen3) may be slow or error-prone on low-resource hardware.
- Some agent confusion/overlap may occur (e.g., Finance agent answering weather questions).
- See README.md, QUICKSTART.md, and KNOWN_ISSUES_AND_GOTCHAS.md for details.

---

## Completed/Ongoing (2025-07)

- [x] Expose agent/cluster actions as MCP tools (schedule_event, journal_entry, finance_balance, get_user_profile, etc.)
- [x] Integrate context/memory: journal_entry logs to DB, get_user_profile fetches from DB.
- [x] Create minimal cockpit/dashboard UI prototype (vern_dashboard.html).
- [x] Update README and AGENT_GUIDES for new tools and context features.
- [x] Add/adjust integration tests for all MCP tools.
- [x] Gather feedback on dashboard UI and context-aware tools.
- [x] LLM-powered CLI chat and Orchestrator agent.
- [x] Multi-agent orchestration and delegation.

## Immediate Next Steps

- [ ] Plan and document next sprint: tool-calling, RAG, agent specialization, plugin API, and polish.
- [ ] Update CHANGELOG.md for all recent changes.
- [ ] Add/expand cross-domain workflows (e.g., "plan my week", "daily health check-in").
- [ ] Update AGENT_GUIDES/CLUSTER.md files with new orchestration and context info.
- [ ] Review and update KNOWN_ISSUES_AND_GOTCHAS.md for LLM/tool/RAG caveats.

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
