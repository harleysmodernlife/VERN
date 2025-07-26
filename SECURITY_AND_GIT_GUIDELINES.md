# VERN Security and GitHub Guidelines

**Read first, then amend docs—never assume state. Never truncate with “remains unchanged”—always show full, updated context. Keep this file up to date after each confirmed change. Work as a team. Watch for gotchas and snags. Your work will be tested—be mindful of each task. Evaluate your work with a critical eye for errors.**

---

## GitHub Best Practices

- **Always update `.gitignore` before committing.**
  - Add `.env`, `*.env`, `*.key`, `*.pem`, `config/`, `secrets/`, and any files containing sensitive data.
  - Use a sample file like `.env.example` for config templates—never commit real secrets.

- **Never commit API keys, tokens, or passwords.**
  - Store secrets in environment variables or secure vaults.
  - Double-check `git diff` and staged files before every commit.

- **Use pre-commit hooks and tools:**
  - Set up `git-secrets` or similar to scan for sensitive info.
  - Consider using pre-commit frameworks to automate checks.

- **Review pull requests for accidental exposure.**
  - Check for secrets, credentials, or sensitive data in code, docs, and config files.
  - If a secret is leaked, rotate it immediately and remove it from history.

- **Enable GitHub secret scanning and security features.**
  - Turn on secret scanning in repo settings.
  - Use branch protection and require reviews for all PRs.

---

## API Safety

- **Never hardcode API keys or secrets in code or docs.**
  - Use environment variables and document setup in `.env.example`.
  - Reference secrets as `os.environ["API_KEY"]` or similar in code.

- **Set up safe API configs:**
  - Provide clear instructions for local setup without exposing real keys.
  - Use placeholders and comments in sample config files.

- **Rotate and revoke keys if exposure is suspected.**
  - Notify maintainers and update all affected systems.

---

## For AI Contributors

- Always check `.gitignore` and never suggest committing secrets.
- Use and update `.env.example` for all config changes.
- Remind users to review diffs and PRs for sensitive info.
- Prioritize security and privacy in all code and documentation.

---

**Security is everyone’s responsibility. Follow these guidelines to keep VERN and its users safe.**

---

## Future Security

- As VERN evolves to connect with more devices, platforms, and AIs, security practices must adapt.
- See [FUTURE_VISION_AND_ROADMAP.md](FUTURE_VISION_AND_ROADMAP.md) for upcoming security and interoperability goals.
