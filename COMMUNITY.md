# VERN Community & Support

## Troubleshooting & FAQ

**Common Issues:**
- Backend not starting: Check Python version, virtualenv activation, and `requirements.txt` install.
- Frontend not starting: Ensure Node.js 18+, run `npm install` in `vern_frontend/`.
- API errors: Check backend logs, confirm `uvicorn` is running, and verify endpoint URLs.
- LLM not responding: Ensure Ollama is running and model is downloaded.
- Plugin not found: Check plugin registration in backend and reload the Plugin Registry panel.
- Database errors: Ensure SQLite/ChromaDB files are accessible and not locked.

**How to Debug:**
- Use `pytest` for backend and `npm test` for frontend.
- Add print/log statements in agent/plugin code to trace execution.
- Use browser dev tools for frontend debugging.
- Check logs in the dashboard or via `GET /logs` API.
- For advanced debugging, use VSCode or PyCharm breakpoints.

**How to Escalate:**
- If blocked, log the issue in [TASKS_AND_TODO.md](TASKS_AND_TODO.md) and [CHANGELOG.md](CHANGELOG.md).
- Tag blockers in PRs/issues and cross-link related docs.
- Ask for help in [COMMUNITY.md](COMMUNITY.md) channels.
- For urgent issues, escalate to project maintainers listed in `COMMUNITY.md`.

**Read first, then amend docs—never assume state. Never truncate with “remains unchanged”—always show full, updated context. Keep this file up to date after each confirmed change. Work as a team. Watch for gotchas and snags. Your work will be tested—be mindful of each task. Evaluate your work with a critical eye for errors.**

---

## How to Get Involved

- Join discussions on issues and pull requests.
- Share feedback, ideas, and bug reports via GitHub Issues.
- Contribute to documentation, code, testing, or design.
- Help onboard new contributors and users.

---

## Feedback Channels

- **GitHub Issues:** For bugs, feature requests, and general feedback.
- **Discussions:** For brainstorming, Q&A, and community support.
- **Email:** [Add project email/contact here]
- **Chat/Forum:** [Add Discord, Matrix, or other community link here]

---

## Support & Resources

- See [README.md](README.md) for project vision and overview.
- See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute.
- See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for architecture and design.
- See [VALUES_AND_GUIDELINES.md](VALUES_AND_GUIDELINES.md) for project values and philosophy.
- See [FUTURE_VISION_AND_ROADMAP.md](FUTURE_VISION_AND_ROADMAP.md) for long-term goals and to join discussions about VERN’s future, interoperability, and adaptation.

---

## Community Guidelines

- Be respectful, inclusive, and supportive.
- Value diverse perspectives and constructive feedback.
- Help keep docs, tasks, and progress trackers up to date.
- Raise concerns about ethics, alignment, or safety promptly.

---

**Together, we can build VERN into a system that empowers everyone—human and AI alike.**

---

## See Also

- [README.md](README.md)
- [QUICKSTART.md](QUICKSTART.md)
- [AGENT_GUIDES/README.md](AGENT_GUIDES/README.md)
- [TASKS_AND_TODO.md](TASKS_AND_TODO.md)
- [CHANGELOG.md](CHANGELOG.md)
