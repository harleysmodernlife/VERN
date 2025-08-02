# Contributing to VERN

Thank you for your interest in contributing to VERN! Our goal is to build a modular, transparent, and user-friendly AI ecosystem where collaboration between humans and AI is at the forefront. Please take a few moments to review our guidelines below.

---

## Overview

VERN is an open, modular agent ecosystem that supports:
- **Persona Tuning:** Each agent can adjust its response style (e.g., coach, architect, mentor) to cater to user needs.
- **Context & Memory:** Agents utilize contextual data and past interactions (via API/back-end). Our visual Workflow Editor now lets each step include optional context inputs, although detailed per-step processing will be refined in future sprints.
- **Multi-Agent Workflows:** Users can chain commands across agents to achieve complex tasks, orchestrated by our central orchestrator.
- **Feedback & Iteration:** We have integrated a feedback system so users can report issues directly through the dashboard, helping us continuously improve the system.

Recent sprint updates have focused on:
- Enhancing the **Workflow Editor** (per-step context input added).
- Implementing a basic **Feedback System** (backend endpoint and frontend panel integrated).
- Refining the **Orchestrator** for robust error handling and multi-agent routing.
- Updating our documentation (README, QUICKSTART, TASKS_AND_TODO, etc.) to accurately reflect these changes and our future roadmap.

---

## Guidelines for Contributions

1. **Read the Documentation:**  
   - Ensure you are familiar with our [README.md](README.md), [QUICKSTART.md](QUICKSTART.md), and [TASKS_AND_TODO.md](TASKS_AND_TODO.md). They provide an overview of the system architecture, setup instructions, and our current priorities.
   - Please review the [SECURITY_AND_GIT_GUIDELINES.md](SECURITY_AND_GIT_GUIDELINES.md) for best practices regarding sensitive information and version control.

2. **Environment Setup:**  
   - Follow the instructions in the Quickstart Guide to set up the backend (FastAPI) and frontend (Next.js) environments.
   - Run tests using `pytest` for backend and `npm test` for frontend as described in our documentation.

3. **Code Style and Testing:**  
   - Ensure your code adheres to the existing style conventions.
   - Write tests for new features or bug fixes.
   - Include detailed commit messages that reference related issues or tasks.

4. **Feature Development and Bug Fixes:**  
   - For new features (e.g., further improvements to per-step context processing, enhanced error alerts, and feedback loop enhancements), please reference TASKS_AND_TODO.md to align with our sprint priorities.
   - If you introduce changes, update all relevant documentation. Our docs should always accurately reflect the current state of the code.

5. **Pull Requests:**  
   - When ready, submit a pull request for review.
   - Be sure to document your changes within the PR description and update our CHANGELOG.md if necessary.

6. **Collaboration and Communication:**  
   - Engage with the community via our [COMMUNITY.md](COMMUNITY.md) channels if you have questions or need clarifications.
   - Your contributions and suggestions are key to making VERN better. Feel free to propose improvements or report issues.

---

## Roadmap and Future Vision

Our recent sprint has "turbocharged" VERN by integrating:
- A visual Workflow Editor with per-step context inputs.
- A basic Feedback System for user-driven improvements.
- Enhanced orchestration for multi-agent communication and error handling.

Next priorities include:
- Fully refining per-step context processing so that agents receive precise, tailored context.
- Implementing real-time error alerts on the frontend.
- Expanding our dynamic feedback loop to auto-adjust agent behavior.
- Enhancing security measures and performance optimizations.
- Improving interactive onboarding with multimedia support.

For more details, see our [FUTURE_VISION_AND_ROADMAP.md](FUTURE_VISION_AND_ROADMAP.md).

---

Thank you for contributing to VERN and helping us shape the future of human-AI collaboration!
