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

export default function Dashboard() {
  // Guard against SSR for localStorage
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

  // Example: fetch cluster status using unified API base
  useEffect(() => {
    const url = joinApi("/agents/status");
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        // no-op store; future: show in a panel
        // console.debug("Cluster status", data);
      })
      .catch(() => {
        // swallow for now; dashboard is placeholder UI
      });
  }, []);

  return (
    <IntlProvider locale={locale} messages={messages[locale]}>
      <div
        style={{
          border: "2px solid #333",
          padding: "2rem",
          borderRadius: "12px",
          background: "#fff",
          maxWidth: "900px",
          margin: "0 auto"
        }}
        aria-label="VERN Dashboard"
        tabIndex={0}
      >
        <div style={{ marginBottom: "1rem" }}>
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
        <h2>
          <FormattedMessage id="dashboard" defaultMessage="Dashboard" />
        </h2>
        <p>
          <FormattedMessage id="panelDesc" defaultMessage="Live agent/cluster status, plugin management, and workflow visualization." />
        </p>
        {/* Live Agent/Cluster Status Panel (polls registry, container-aware base) */}
        <AgentClusterStatus locale={locale} />
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
        {/* Example image/icon with alt text for future use */}
        {/* <img src="/static/vern_logo.png" alt="VERN project logo" style={{marginTop: "1rem", width: 80}} /> */}
        <ConfigEditorPanel />
        <WorkflowEditorPanel />
        <PluginMarketplacePanel />
        <IntegrationManagerPanel />
        <OnboardingPanel />
        <HelpPanel />
        <div style={{ marginTop: "2rem", fontSize: "0.9em", color: "#666" }}>
          <span aria-label="Keyboard navigation tip">
            <b>Tip:</b> Use <kbd>Tab</kbd> and <kbd>Shift+Tab</kbd> to navigate between panels and controls.
          </span>
        </div>
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
