# Agent Guides

Welcome to the VERN Agent Guides!  
This directory contains documentation and prompts for each agent cluster, as well as general onboarding and extension instructions.

---

## Cluster/Agent Onboarding & Self-Check

If you are a new agent (AI or human) or need to re-orient:

- **Read [PROJECT_OVERVIEW.md](../PROJECT_OVERVIEW.md)** for the big picture and cluster/team structure.
- **Review [TASKS_AND_TODO.md](../TASKS_AND_TODO.md)** for the current sprint, blockers, and context.
- **Summarize the current cluster goal** before acting or making changes.
- **Update TASKS_AND_TODO.md** after each confirmed change.
- **If unsure, ask for review or clarification before proceeding.**

---

## Agent Cluster Structure

- Each cluster (Dev, Admin, Research, etc.) has its own guide and prompt file.
- Clusters are modular and can be extended or swapped as needed.
- See each `AGENT_GUIDES/<CLUSTER>.md` for role-specific info and prompts.

---

## Adding or Updating Agents/Clusters

1. Add a new Python module in `src/mvp/` for your agent/cluster.
2. Create or update the corresponding guide in `AGENT_GUIDES/`.
3. Register new tools in `src/mvp/mcp_server.py` using `@mcp.tool()`.
4. Update documentation and tests as needed.
5. **To add LLM-powered reasoning to an agent:**
   - Add a response function that calls the LLM (see `src/mvp/orchestrator.py` for an example).
   - Pass recent chat history, agent status, and relevant context to the LLM.
   - Document the agent’s prompt, context, and tool-calling logic in the cluster guide.

---

## Multi-Agent Orchestration & Delegation

- The Orchestrator agent uses the LLM to decide which clusters to involve for any user input.
- Sub-tasks are delegated to relevant clusters, which each use their own LLM-powered logic and tools.
- Results are aggregated and summarized for the user.
- All agent modules are modular and extensible for future plugins and new clusters.

---

## Modular LLM Provider/Model Selection

- **Config-driven:**  
  - LLM provider/model selection is now driven by `config/agent_backends.yaml`.
  - The LLM router (`src/mvp/llm_router.py`) reads the config and routes agent calls to the selected backend/model.
  - Future GUI will allow users to select providers/models interactively.
- **How to change models/providers:**  
  - Edit `config/agent_backends.yaml` to set the default backend/model.
  - Supported: Ollama (local), OpenAI (cloud, planned), fake_llm (testing), and more.
  - See QUICKSTART.md for details.

---

## Best Practices

- Keep guides and prompts up to date with code and workflow changes.
- Use clear, descriptive language—assume the reader is new to the project.
- Document any gotchas, caveats, or lessons learned in the relevant guide.
- Reference [KNOWN_ISSUES_AND_GOTCHAS.md](../KNOWN_ISSUES_AND_GOTCHAS.md) for system-wide caveats.
- **For LLM-powered agents:**  
  - Document how context is passed and managed.
  - Describe fallback/error handling for LLM failures.
  - Note how tool-calling is triggered from LLM plans (if implemented).

---

## See Also

- [README.md](../README.md)
- [PROJECT_OVERVIEW.md](../PROJECT_OVERVIEW.md)
- [QUICKSTART.md](../QUICKSTART.md)
- [TASKS_AND_TODO.md](../TASKS_AND_TODO.md)
- [MVP_IMPLEMENTATION_PLAN.md](../MVP_IMPLEMENTATION_PLAN.md)
- [KNOWN_ISSUES_AND_GOTCHAS.md](../KNOWN_ISSUES_AND_GOTCHAS.md)
