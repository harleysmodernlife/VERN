// vern_frontend/components/Dashboard.js
import React, { useState, useEffect } from "react";
import { getApiBase, joinApi } from "../lib/apiBase";
import { IntlProvider, FormattedMessage } from "react-intl";
import ConfigEditorPanel from "./ConfigEditorPanel";
import WorkflowEditorPanel from "./WorkflowEditorPanel";
import PluginMarketplacePanel from "./PluginMarketplacePanel";
import HelpPanel from "./HelpPanel";
import OnboardingPanel from "./OnboardingPanel";
import IntegrationManagerPanel from "./IntegrationManagerPanel";

const messages = {
  en: {
    dashboard: "Dashboard (Coming Soon)",
    panelDesc: "This panel will show agent/cluster status, plugin management, workflow visualization, and more.",
    language: "Language"
  },
  es: {
    dashboard: "Panel de Control (Próximamente)",
    panelDesc: "Este panel mostrará el estado de agentes/clusters, gestión de plugins, visualización de flujos de trabajo y más.",
    language: "Idioma"
  }
};

import AgentManagementPanel from "./AgentManagementPanel";
import FeedbackPanel from "./FeedbackPanel";

/**
 * Unified Dashboard UI
 * Integration points:
 * - AgentManagementPanel: Connect to agent registry API for CRUD, status, cluster assignment.
 * - WorkflowEditorPanel: Integrate workflow builder, drag-and-drop, persistence.
 * - PluginMarketplacePanel/PluginRegistryPanel: Plugin install, enable/disable, invoke.
 * - OnboardingPanel: User onboarding, persona/profile setup, dependency checks.
 * TODO: Implement drag-and-drop workflow builder in WorkflowEditorPanel.
 * TODO: Add contextual help and notifications in all panels.
 * TODO: Sidebar: highlight active panel, keyboard navigation, accessibility.
 */

export default function Dashboard() {
  const isBrowser = typeof window !== "undefined";
  const [locale, setLocale] = useState(() => {
    if (isBrowser) {
      try { return localStorage.getItem("vern_lang") || "en"; } catch { return "en"; }
    }
    return "en";
  });

  useEffect(() => {
    if (isBrowser) {
      try { localStorage.setItem("vern_lang", locale); } catch {}
    }
  }, [locale, isBrowser]);

  // Sidebar navigation state
  const panels = [
    { key: "agents", label: "Agents", component: <AgentManagementPanel /> },
    { key: "workflows", label: "Workflows", component: <WorkflowEditorPanel /> },
    { key: "plugins", label: "Plugins", component: <PluginMarketplacePanel /> },
    { key: "integrations", label: "Integrations", component: <IntegrationManagerPanel /> },
    { key: "feedback", label: "Feedback", component: <FeedbackPanel /> },
    { key: "help", label: "Help", component: <HelpPanel /> },
    { key: "onboarding", label: "Onboarding", component: <OnboardingPanel /> }
  ];
  const [activePanel, setActivePanel] = useState("agents");

  // TODO: Add keyboard navigation for sidebar (accessibility)
  // TODO: Add notification system for panel actions

  return (
    <IntlProvider locale={locale} messages={messages[locale]}>
      <div
        style={{
          display: "flex",
          border: "2px solid #333",
          borderRadius: "12px",
          background: "#fff",
          maxWidth: "1100px",
          margin: "0 auto",
          minHeight: "600px"
        }}
        aria-label="VERN Dashboard"
        tabIndex={0}
      >
        {/* Sidebar Navigation */}
        <nav
          style={{
            width: "220px",
            background: "#f7f7fa",
            borderRight: "1px solid #ddd",
            padding: "2rem 1rem",
            display: "flex",
            flexDirection: "column",
            gap: "1rem"
          }}
          aria-label="Dashboard Sidebar"
        >
          <div style={{ marginBottom: "2rem" }}>
            <label htmlFor="lang-select" style={{ marginRight: "0.5rem" }}>
              <FormattedMessage id="language" defaultMessage="Language" />:
            </label>
            <select
              id="lang-select"
              value={locale}
              onChange={e => setLocale(e.target.value)}
              aria-label="Select language"
              tabIndex={0}
              aria-describedby="lang-desc"
            >
              <option value="en">English</option>
              <option value="es">Español</option>
            </select>
            <span id="lang-desc" style={{ display: "none" }}>
              Choose your preferred language for the dashboard.
            </span>
          </div>
          {panels.map(panel => (
            <button
              key={panel.key}
              onClick={() => setActivePanel(panel.key)}
              style={{
                padding: "0.75rem 1rem",
                borderRadius: "6px",
                border: activePanel === panel.key ? "2px solid #0070f3" : "1px solid #ccc",
                background: activePanel === panel.key ? "#e6f0ff" : "#fff",
                fontWeight: activePanel === panel.key ? "bold" : "normal",
                cursor: "pointer",
                outline: "none"
              }}
              aria-current={activePanel === panel.key ? "page" : undefined}
              tabIndex={0}
            >
              {panel.label}
            </button>
          ))}
          {/* TODO: Add icons for each panel */}
        </nav>
        {/* Main Panel Content */}
        <main style={{ flex: 1, padding: "2rem", minHeight: "600px" }}>
          <h2>
            <FormattedMessage id="dashboard" defaultMessage="Dashboard" />
          </h2>
          <p>
            <FormattedMessage id="panelDesc" defaultMessage="Live agent/cluster status, plugin management, and workflow visualization." />
          </p>
          {/* Live Agent/Cluster Status Panel (polls registry, container-aware base) */}
          <AgentClusterStatus locale={locale} />
          {/* Render selected panel */}
          <div style={{ marginTop: "2rem" }}>
            {panels.find(p => p.key === activePanel)?.component}
          </div>
          {/* Accessibility & i18n Status Panel */}
          <div
            style={{
              marginTop: "2rem",
              padding: "1rem",
              background: "#f5f5f5",
              borderRadius: "6px",
              fontSize: "0.95rem"
            }}
            aria-live="polite"
          >
            <strong>
              <FormattedMessage id="a11yStatus" defaultMessage="Accessibility & Language Status" />
            </strong>
            <ul>
              <li>
                <FormattedMessage id="a11yKeyboard" defaultMessage="Keyboard navigation: enabled" />
              </li>
              <li>
                <FormattedMessage id="a11yScreenReader" defaultMessage="Screen reader support: enabled" />
              </li>
              <li>
                <FormattedMessage id="a11yLang" defaultMessage="Current language:" /> {locale === "en" ? "English" : "Español"}
              </li>
            </ul>
          </div>
          {/* TODO: Add notifications and contextual help */}
          <div style={{ marginTop: "2rem", fontSize: "0.9em", color: "#666" }}>
            <span aria-label="Keyboard navigation tip">
              <b>Tip:</b> Use <kbd>Tab</kbd> and <kbd>Shift+Tab</kbd> to navigate between panels and controls.
            </span>
          </div>
        </main>
      </div>
    </IntlProvider>
  );
}

// Live agent/cluster status component
function AgentClusterStatus({ locale }) {
  const isBrowser = typeof window !== "undefined";
  const [status, setStatus] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!isBrowser) return;
    let cancelled = false;

    const fetchOnce = () => {
      setLoading(true);
      fetch(joinApi("/agents/status"))
        .then(res => res.json())
        .then(data => { if (!cancelled) { setStatus(data); setLoading(false); } })
        .catch(err => { if (!cancelled) { setError(err.message || "Failed to fetch agent status."); setLoading(false); } });
    };

    fetchOnce();
    const id = setInterval(fetchOnce, 5000); // poll every 5s
    return () => { cancelled = true; clearInterval(id); };
  }, [isBrowser]);

  if (!isBrowser) return <div>Loading...</div>;
  if (loading) return <div>Loading agent/cluster status...</div>;
  if (error) return <div style={{ color: "red" }}>Error: {error}</div>;
  if (!status.length) return <div>No agent/cluster status available.</div>;

  return (
    <div style={{ marginTop: "1rem" }}>
      <h3>{locale === "en" ? "Agent/Cluster Status" : "Estado de Agentes/Clusters"}</h3>
      <ul>
        {status.map((agent, idx) => (
          <li key={idx}>
            <strong>{agent.name}</strong> ({agent.cluster}) - {agent.status}
          </li>
        ))}
      </ul>
    </div>
  );
}
