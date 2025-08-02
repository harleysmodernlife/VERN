// vern_frontend/components/OrchestratorPanel.js
import React, { useState, useEffect } from "react";
import { IntlProvider, FormattedMessage } from "react-intl";

const messages = {
  en: {
    panelTitle: "Orchestrator Test Panel",
    inputPlaceholder: "Ask VERN anything...",
    send: "Send",
    sending: "Sending...",
    response: "Response:",
    language: "Language"
  },
  es: {
    panelTitle: "Panel de Prueba del Orquestador",
    inputPlaceholder: "Pregunta lo que sea a VERN...",
    send: "Enviar",
    sending: "Enviando...",
    response: "Respuesta:",
    language: "Idioma"
  }
};

export default function OrchestratorPanel() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [locale, setLocale] = useState(() => localStorage.getItem("vern_lang") || "en");

  useEffect(() => {
    localStorage.setItem("vern_lang", locale);
  }, [locale]);

  async function handleSend() {
    setLoading(true);
    setResponse("");
    try {
      const res = await fetch("http://localhost:8000/agents/orchestrator/respond", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: input }),
      });
      const data = await res.json();
      setResponse(data.response || JSON.stringify(data));
    } catch (err) {
      setResponse("Error: " + err.message);
    }
    setLoading(false);
  }

  return (
    <IntlProvider locale={locale} messages={messages[locale]}>
      <div style={{ border: "1px solid #0070f3", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="lang-select-orch" style={{ marginRight: "0.5rem" }}>
            <FormattedMessage id="language" defaultMessage="Language" />:
          </label>
          <select
            id="lang-select-orch"
            value={locale}
            onChange={e => setLocale(e.target.value)}
            aria-label="Select language"
            tabIndex={0}
            aria-describedby="lang-desc-orch"
          >
            <option value="en">English</option>
            <option value="es">Español</option>
          </select>
          <span id="lang-desc-orch" style={{ display: "none" }}>
            Choose your preferred language for the orchestrator panel.
          </span>
        </div>
        <h3>
          <FormattedMessage id="panelTitle" defaultMessage="Orchestrator Test Panel" />
        </h3>
        <div style={{ marginBottom: "1rem" }}>
          <label>
            <b>Context:</b>
            <input
              type="text"
              value={context}
              onChange={e => setContext(e.target.value)}
              placeholder="Context (optional)"
              style={{ width: "40%", marginLeft: "0.5rem" }}
            />
          </label>
          <label style={{ marginLeft: "1rem" }}>
            <b>Persona:</b>
            <input
              type="text"
              value={persona}
              onChange={e => setPersona(e.target.value)}
              placeholder="Persona (optional)"
              style={{ width: "20%", marginLeft: "0.5rem" }}
            />
          </label>
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <label>
            <b>Agent Clusters:</b>
            <select multiple value={selectedClusters} onChange={e => setSelectedClusters(Array.from(e.target.selectedOptions, o => o.value))} style={{ width: "40%", marginLeft: "0.5rem" }}>
              {clusters.map(cluster => (
                <option key={cluster} value={cluster}>{cluster}</option>
              ))}
            </select>
          </label>
          <label style={{ marginLeft: "1rem" }}>
            <b>Plugins:</b>
            <select multiple value={selectedPlugins} onChange={e => setSelectedPlugins(Array.from(e.target.selectedOptions, o => o.value))} style={{ width: "30%", marginLeft: "0.5rem" }}>
              {plugins.map(plugin => (
                <option key={plugin} value={plugin}>{plugin}</option>
              ))}
            </select>
          </label>
        </div>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder={messages[locale].inputPlaceholder}
          style={{ width: "60%", marginRight: "1rem" }}
          aria-label={messages[locale].inputPlaceholder}
        />
        <button onClick={handleSend} disabled={loading || !input}>
          {loading ? <FormattedMessage id="sending" defaultMessage="Sending..." /> : <FormattedMessage id="send" defaultMessage="Send" />}
        </button>
        <div style={{ marginTop: "1rem", minHeight: "2rem" }}>
          {workflowPlan && (
            <div style={{ marginBottom: "1rem", background: "#eef", padding: "1rem", borderRadius: "6px" }}>
              <b>Workflow Plan:</b> {workflowPlan}
            </div>
          )}
          {response && <b><FormattedMessage id="response" defaultMessage="Response:" /></b>} {response}
        </div>
      </div>
    </IntlProvider>
  );
}

// Add state and logic for advanced features
const [context, setContext] = useState("");
const [persona, setPersona] = useState("");
const [clusters, setClusters] = useState([
  "research", "finance", "health", "admin", "learning", "social", "environment", "legal", "creativity", "career", "travel", "security", "archetype", "emergent", "knowledge_broker", "id10t_monitor"
]);
const [plugins, setPlugins] = useState([
  "weather", "calendar", "fileops", "chromadb"
]);
const [selectedClusters, setSelectedClusters] = useState([]);
const [selectedPlugins, setSelectedPlugins] = useState([]);
const [workflowPlan, setWorkflowPlan] = useState("");

async function handleSend() {
  setLoading(true);
  setResponse("");
  setWorkflowPlan("");
  try {
    const res = await fetch("http://localhost:8000/agents/orchestrator/respond", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_input: input,
        context,
        agent_status: "All agents online",
        user_id: "default_user",
        verbose: true
      }),
    });
    const data = await res.json();
    // Try to extract workflow plan from response
    const planMatch = data.response.match(/\(plan:([^)]+)\)/);
    setWorkflowPlan(planMatch ? planMatch[1].trim() : "");
    setResponse(data.response || JSON.stringify(data));
  } catch (err) {
    setResponse("Error: " + err.message);
  }
  setLoading(false);
}
