// vern_frontend/components/AgentClusterViz.js
import React, { useState, useEffect } from "react";
import { joinApi } from "../lib/apiBase";
import { IntlProvider, FormattedMessage } from "react-intl";

const messages = {
  en: {
    panelTitle: "Agent/Cluster Visualization",
    desc: "This panel will visualize agent clusters, their status, and recent activity.",
    coming: "(Network graph and live status coming soon.)",
    placeholder: "Visualization placeholder",
    language: "Language"
  },
  es: {
    panelTitle: "Visualización de Agentes/Clusters",
    desc: "Este panel visualizará los clusters de agentes, su estado y actividad reciente.",
    coming: "(Gráfico de red y estado en vivo próximamente.)",
    placeholder: "Marcador de posición de visualización",
    language: "Idioma"
  }
};

// Safe browser check for SSR
const isBrowser = typeof window !== "undefined";

export default function AgentClusterViz() {
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
  }, [locale]);

  // Fetch cluster status using unified API base
  useEffect(() => {
    const url = joinApi("/agents/status");
    fetch(url)
      .then(res => res.json())
      .then((data) => {
        // In future we can visualize; for now, noop to avoid unused var warnings
        // console.debug("Cluster status", data);
      })
      .catch(() => {
        // swallow network errors in placeholder UI
      });
  }, []);

  return (
    <IntlProvider locale={locale} messages={messages[locale]}>
      <div style={{ border: "1px solid #f90", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="lang-select-cluster" style={{ marginRight: "0.5rem" }}>
            <FormattedMessage id="language" defaultMessage="Language" />:
          </label>
          <select
            id="lang-select-cluster"
            value={locale}
            onChange={e => setLocale(e.target.value)}
            aria-label="Select language"
            tabIndex={0}
            aria-describedby="lang-desc-cluster"
          >
            <option value="en">English</option>
            <option value="es">Español</option>
          </select>
          <span id="lang-desc-cluster" style={{ display: "none" }}>
            Choose your preferred language for the agent/cluster visualization panel.
          </span>
        </div>
        <h3>
          <FormattedMessage id="panelTitle" defaultMessage="Agent/Cluster Visualization" />
        </h3>
        <p>
          <FormattedMessage id="desc" defaultMessage="This panel will visualize agent clusters, their status, and recent activity." /><br />
          <FormattedMessage id="coming" defaultMessage="(Network graph and live status coming soon.)" />
        </p>
        <LiveClusterStatus locale={locale} />
        <NetworkGraph />
      </div>
    </IntlProvider>
  );
}

// Define LiveClusterStatus to avoid ReferenceError
function LiveClusterStatus({ locale }) {
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
        .catch(err => { if (!cancelled) { setError(err.message || "Failed to fetch status."); setLoading(false); } });
    };

    fetchOnce();
    const id = setInterval(fetchOnce, 5000); // poll every 5s
    return () => { cancelled = true; clearInterval(id); };
  }, []);

  if (!isBrowser) return <div>Loading...</div>;
  if (loading) return <div>Loading cluster status...</div>;
  if (error) return <div style={{ color: "red" }}>Error: {error}</div>;
  if (!status.length) return <div>No cluster status available.</div>;

  return (
    <div style={{ marginTop: "1rem" }}>
      <ul>
        {status.map((agent, i) => (
          <li key={i}><strong>{agent.name}</strong> ({agent.cluster}) - {agent.status}</li>
        ))}
      </ul>
    </div>
  );
}

// Minimal placeholder network graph to avoid ReferenceError
function NetworkGraph() {
  return (
    <div style={{ marginTop: "1rem", padding: "1rem", border: "1px dashed #aaa" }}>
      <em>Network graph placeholder</em>
    </div>
  );
}
