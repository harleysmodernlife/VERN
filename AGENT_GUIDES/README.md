# Agent Guides Overview

This folder contains guides for each major agent cluster and monitor in VERN. Each guide covers the agent’s role, protocols, gotchas, and best practices.

**Core Design Pillars:**  
- Interoperability: Agents and clusters must be able to connect with diverse devices, platforms, and AIs.
- Continuous Adaptation: Agents should red-team, self-improve, and stay up to date with new threats and discoveries.
- Intentionality: All actions should align with user goals, values, and ethical principles.

**Context, Logging, and Learning:**  
- Each cluster/agent maintains its own log (actions, errors, feedback) and only accesses the data needed for its role.
- Sensitive data is compartmentalized; agents escalate to the Knowledge Broker or Orchestrator for broader context.
- Local learning happens per agent/cluster; system-wide learning and adaptation are managed by meta-agents and orchestrator.
- All learning and adaptation steps are logged for transparency and debugging.

## Current Guides

- ARCHETYPE_PHOENIX.md — Human reasoning, values, synthesis (13 archetypes)
- INTERACTION_ENGINE.md — Adaptive, engaging, context-aware personality (Firebird layer)
- DEV_TEAM.md — Coding, debugging, automation
- ADMIN.md — Scheduling, file management, logistics
- RESEARCH.md — Information retrieval, summarization
- FINANCE_RESOURCE.md — Budgeting, resource allocation
- HEALTH_WELLNESS.md — Habit tracking, health data, wellness
- LEARNING_EDUCATION.md — Personalized learning, skill mapping
- SOCIAL_RELATIONSHIP.md — Contacts, communication, social support
- SECURITY_PRIVACY.md — Threat monitoring, permissions, privacy
- ENVIRONMENT_SYSTEMS.md — Device/system health, automation, IoT
- LEGAL_COMPLIANCE.md — Policy tracking, contracts, compliance
- CREATIVITY_MEDIA.md — Idea generation, content creation, media
- CAREER_WORK.md — Job search, networking, performance
- TRAVEL_LOGISTICS.md — Trip planning, booking, navigation

## All Clusters & Monitors Documented

All major agent clusters and system monitors are now documented.

**Doc Discipline & Cross-Referencing:**  
- Every cluster guide (e.g., DEV_TEAM.md) is paired with a PROMPTS.md file (e.g., DEV_TEAM_PROMPTS.md).
- Always read both the main guide and its PROMPTS.md before acting—never shortcut or skip linked files.
- All guides and prompt specs link to [PROJECT_OVERVIEW.md](../PROJECT_OVERVIEW.md), [VALUES_AND_GUIDELINES.md](../VALUES_AND_GUIDELINES.md), and [SECURITY_AND_GIT_GUIDELINES.md](../SECURITY_AND_GIT_GUIDELINES.md).
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for doc discipline rules and enforcement.

Contributors: Update guides as protocols evolve or new clusters/monitors are added. Follow the template and reinforce project values and safety protocols.
