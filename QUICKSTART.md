# VERN Quickstart Guide

**Read first, then amend docs—never assume state. Never truncate with “remains unchanged”—always show full, updated context.**

---

## 1. Prerequisites

- Python 3.8+ installed
- Git installed
- Basic terminal/command line familiarity

---

## 2. Setup

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/vern.git
   cd vern
   ```

2. **Create and activate a virtual environment:**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies (to be added in requirements.txt):**
   ```
   pip install -r requirements.txt
   ```

4. **Copy and configure environment variables:**
   ```
   cp .env.example .env
   # Edit .env to add your API keys and config
   ```

5. **Initialize the database:**
   ```
   python3 src/db/init_db.py
   ```
   - This will create `db/vern.db` using the schema in `src/db/schema.sql`.
   - Inspect or manage the DB with the `sqlite3` CLI or a GUI tool.

---

## 3. Running the MVP

### Manual Testing

1. Navigate to the MVP directory:
   ```
   cd src/mvp/
   ```
2. Run the CLI:
   ```
   python3 cli.py
   ```
   - Option 1: Request new feature (type a feature description and watch the workflow/logs)
   - Option 2: Schedule meeting (type meeting details and watch the workflow/logs)
   - Option 3: Knowledge Broker: Context lookup
   - Option 4: Knowledge Broker: Cross-cluster query
   - Option 5: Security/Privacy: Monitor action
   - Option 6: Exit
   - Try invalid options to check error handling.

### Automated Testing

1. From the project root, run:
   ```
   python3 tests/test_mvp.py
   python3 tests/test_db_logging.py
   python3 tests/test_agents_extended.py
   python3 tests/test_cross_cluster_handoff.py
   python3 tests/test_agents_horizontal.py
   ```
   - Confirms feature request, meeting scheduling, error handling, escalation stubs, Knowledge Broker and Security/Privacy agent workflows, and cross-cluster handoff logging all work as intended.

2. Review logs and outputs to confirm system behavior matches documentation.

---

## 4. Accessibility & Internationalization

- VERN aims to support keyboard navigation, screen readers, and multiple languages.
- See GOALS_AND_MILESTONES.md for progress and plans.

---

## 5. Getting Help

- See COMMUNITY.md for support channels.
- Read CONTRIBUTING.md and SECURITY_AND_GIT_GUIDELINES.md before making changes.

---

**Welcome to VERN! Your feedback and contributions are valued.**

---

## Learn More

- See [FUTURE_VISION_AND_ROADMAP.md](FUTURE_VISION_AND_ROADMAP.md) for VERN’s long-term goals, modular design, and future direction.
