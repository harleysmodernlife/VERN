# VERN Goals and Milestones

**Read first, then amend docs—never assume state. Never truncate with “remains unchanged”—always show full, updated context. Keep this list up to date after each confirmed change. Work as a team. Watch for gotchas and snags. Your work will be tested—be mindful of each task. Evaluate your work with a critical eye for errors.**

---

## Vision

Empower humans and AI to collaborate, learn, and thrive—together—by building a modular, accessible, and ethical agent ecosystem.

**See [FUTURE_VISION_AND_ROADMAP.md](FUTURE_VISION_AND_ROADMAP.md) for long-term direction, including interoperability, adaptation, and intentionality as core goals.**

---

## Current Goals

- Establish robust, modular architecture for agent clusters and orchestrators
- Implement unified memory (SQLite, ChromaDB) and RAG
- Provide configurable AI provider/model selection
- Ensure accessibility, privacy, and transparency from the start
- Build clear onboarding, documentation, and contribution guides
- Enable plugin/agent marketplace and community feedback channels
- Lay groundwork for interoperability with devices, platforms, and AIs
- Build in continuous adaptation (red-teaming, self-improvement)
- Align all actions and features with user goals, values, and ethical principles

---

## Accessibility & Internationalization Checklist

- [x] Keyboard navigation for all dashboard panels and forms
- [x] ARIA labels and roles for all interactive elements
- [x] Sufficient color contrast and font scaling options
- [x] Screen reader support for major workflows
- [ ] Language selector and translation support (in progress)
    - [ ] Add a language selector dropdown to the dashboard UI (see `vern_frontend/components/Dashboard.js`)
    - [ ] Integrate [React Intl](https://formatjs.io/docs/react-intl/) for i18n in all frontend components
    - [ ] Provide at least one additional language (e.g., Spanish) for all UI strings
    - [ ] Store user language preference in local storage or user profile
    - [ ] Document translation workflow in `README.md` and `vern_frontend/README.md`
- [ ] Alt text for all images and icons
    - [ ] Add descriptive `alt` attributes to all `<img>` and icon components in the frontend
    - [ ] Audit all SVGs and dashboard panels for missing alt text
    - [ ] Test with screen readers for coverage
- [ ] Accessible onboarding wizard and checklist
    - [ ] Ensure all onboarding steps are keyboard navigable and have ARIA roles/labels
    - [ ] Add screen reader instructions to onboarding UI
    - [ ] Provide alt text for all onboarding illustrations/icons
- [ ] Mobile and responsive design for all UIs
- [ ] Documentation available in multiple languages (planned)
    - [ ] Translate `README.md`, `QUICKSTART.md`, and onboarding docs to at least one additional language
    - [ ] Add language toggle to docs site if applicable
- [ ] Accessibility testing in CI/CD pipeline (planned)
    - [ ] Add automated accessibility checks (e.g., axe-core, pa11y) to GitHub Actions workflows
    - [ ] Document accessibility test results in PRs
- [ ] User feedback channel for accessibility issues
    - [ ] Add accessibility feedback form or email to dashboard and docs

---

## Milestones

### MVP

- [ ] Core orchestrator and message bus
- [ ] Archetype/Phoenix, Dev, and Admin clusters
- [ ] Unified memory (SQLite, ChromaDB)
- [ ] Configurable AI provider/model selection
- [ ] Minimal UI (CLI or web)
- [ ] Documentation: README, CONTRIBUTING, PROJECT_OVERVIEW, AGENT_GUIDES

### Phase 2

- [ ] Additional clusters (research, finance, health, etc.)
- [ ] Emergent agent, knowledge broker, id10t monitor
- [ ] Plugin/agent system and marketplace
- [ ] Accessibility and internationalization features
- [ ] Automated and manual testing suite

### Phase 3

- [ ] Advanced UI (desktop/web)
- [ ] Backup, sync, and offline-first support
- [ ] Community tools, feedback, and support docs
- [ ] Continuous improvement and feedback integration

---

## Progress Tracking

- Update this file after each confirmed task or milestone.
- Use checkboxes, dates, and owner tags for clarity.
- Link related issues, PRs, and docs as needed.

---

**Stay aligned with the vision, values, and critical reminders at the top of this file.**
