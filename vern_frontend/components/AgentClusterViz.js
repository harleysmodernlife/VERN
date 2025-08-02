// vern_frontend/components/AgentClusterViz.js
import React, { useState, useEffect } from "react";
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

export default function AgentClusterViz() {
  const [locale, setLocale] = useState(() => localStorage.getItem("vern_lang") || "en");

  useEffect(() => {
    localStorage.setItem("vern_lang", locale);
  }, [locale]);

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
