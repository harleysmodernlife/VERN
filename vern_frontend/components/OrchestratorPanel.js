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
  // Guard against SSR: Next.js builds pages on the server where window/localStorage don't exist.
  const isBrowser = typeof window !== "undefined";

  // Core input/response state
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  // i18n state
  const [locale, setLocale] = useState(() => {
    if (isBrowser) {
      try { return localStorage.getItem("vern_lang") || "en"; } catch { return "en"; }
    }
    return "en";
  });

  // New state for simple feedback and connectivity
  const [connected, setConnected] = useState(null); // null=unknown, true/false
  const [lastRating, setLastRating] = useState(null);

  // Advanced controls (must be inside component)
  // Context must be an object for backend Pydantic model; store a JSON string for the input,
  // and parse to an object when sending. Default to "{}".
  const [contextText, setContextText] = useState("{}");
  const [persona, setPersona] = useState("");

  // Ensure contextText is never an empty string; if cleared, force "{}"
  useEffect(() => {
    if (contextText === "") setContextText("{}");
  }, [contextText]);
  const [clusters] = useState([
    "research", "finance", "health", "admin", "learning", "social", "environment", "legal", "creativity", "career", "travel", "security", "archetype", "emergent", "knowledge_broker", "id10t_monitor"
  ]);
  const [plugins] = useState([
    "weather", "calendar", "fileops", "chromadb"
  ]);
  const [selectedClusters, setSelectedClusters] = useState([]);
  const [selectedPlugins, setSelectedPlugins] = useState([]);
  const [workflowPlan, setWorkflowPlan] = useState("");

  useEffect(() => {
    if (isBrowser) {
      try { localStorage.setItem("vern_lang", locale); } catch {}
    }
  }, [locale, isBrowser]);

  // Ping backend health for connectivity badge (browser only)
  useEffect(() => {
    if (!isBrowser) return;
    // Try container DNS first (works inside Docker), then fall back to localhost
    const tryHealth = async () => {
      try {
        const res1 = await fetch("http://backend:8000/health");
        if (res1.ok) {
          setConnected(true);
          return;
        }
      } catch (_) { /* ignore and fall back */ }
      try {
        const res2 = await fetch("http://localhost:8000/health");
        setConnected(res2.ok);
      } catch (_) {
        setConnected(false);
      }
    };
    tryHealth();
  }, [isBrowser]);

  // Ensure contextText is never an empty string before sending
  useEffect(() => {
    if (contextText === "") setContextText("{}");
  }, [contextText]);

  async function handleSend() {
    setLoading(true);
    setResponse("");
    setWorkflowPlan("");
    setLastRating(null);
    try {
      // Prefer container DNS when running in Docker network, else localhost for host runs
      const apiBase = isBrowser && window?.location?.hostname ? (
        // If site is running inside container, backend DNS name resolves; otherwise use localhost
        (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
          ? "http://localhost:8000"
          : "http://backend:8000"
      ) : "http://localhost:8000";

      // Parse contextText into an object, falling back to {} if invalid
      let contextObj = {};
      try {
        const txt = (contextText && contextText.trim().length > 0) ? contextText : "{}";
        contextObj = JSON.parse(txt);
        if (contextObj === null || typeof contextObj !== "object" || Array.isArray(contextObj)) {
          contextObj = {};
        }
      } catch (_) {
        contextObj = {};
      }

      // POST with a FormData wrapper to eliminate any chance of stringification mismatch
      // and ensure a pure JSON body arrives to backend.
      const payload = {
        user_input: input,
        context: contextObj,
        agent_status: "All agents online",
        user_id: "default_user",
        verbose: true
      };

      // Force JSON request explicitly and log for debugging in browser
      const bodyText = JSON.stringify(payload);
      // eslint-disable-next-line no-console
      console.log("[DEBUG] Orchestrator payload:", bodyText);

      const res = await fetch(`${apiBase}/agents/orchestrator/respond`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: bodyText
      });

      // If 422, surface raw text for easier diagnosis
      if (!res.ok) {
        const raw = await res.text();
        setResponse(`HTTP ${res.status}: ${raw}`);
        setLoading(false);
        return;
      }

      const data = await res.json();

      // Privacy short-circuit handling: backend may return ONLY {policy_required,...}
      if (data && data.policy_required) {
        setResponse(""); // clear normal response area
        setPrivacyPrompt({
          policy_required: true,
          action: data.action,
          reason: data.reason,
          request_id: data.request_id,
          suggested_scope: data.suggested_scope,
          expires_at: data.expires_at,
          user_id: data.user_id,
        });
        setLoading(false);
        return;
      }

      // Try to extract workflow plan from response
      const planMatch = data.response && typeof data.response === "string" ? data.response.match(/\(plan:([^)]+)\)/) : null;
      setWorkflowPlan(planMatch ? planMatch[1].trim() : "");
      setResponse(data.response || JSON.stringify(data));
    } catch (err) {
      setResponse("Error: " + err.message);
    }
    setLoading(false);
  }

  // Privacy consent state
  const [privacyPrompt, setPrivacyPrompt] = useState(null);
  const [autoApproveSession, setAutoApproveSession] = useState(false);

  async function submitPrivacyDecision(allowed) {
    if (!privacyPrompt || !privacyPrompt.request_id) return;
    const apiBase = isBrowser && window?.location?.hostname ? (
      (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
        ? "http://localhost:8000"
        : "http://backend:8000"
    ) : "http://localhost:8000";

    const scope = {
      ...((privacyPrompt && privacyPrompt.suggested_scope) || {}),
      auto_approve_session: !!autoApproveSession
    };

    try {
      setLoading(true);
      await fetch(`${apiBase}/privacy/policy/decision`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify({
          request_id: privacyPrompt.request_id,
          allowed: !!allowed,
          scope
        })
      });
      // If approved, retry the last orchestrator call with same inputs
      if (allowed) {
        setPrivacyPrompt(null);
        await handleSend();
      } else {
        setResponse("Action denied by user.");
        setPrivacyPrompt(null);
      }
    } catch (e) {
      setResponse("Error submitting privacy decision: " + (e?.message || e));
    } finally {
      setLoading(false);
    }
  }

  async function sendFeedback(rating) {
    try {
      const payload = { feedback: rating === "up" ? "thumbs_up" : "thumbs_down" };
      const apiBase = isBrowser && window?.location?.hostname ? (
        (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
          ? "http://localhost:8000"
          : "http://backend:8000"
      ) : "http://localhost:8000";
      const res = await fetch(`${apiBase}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (res.ok) setLastRating(rating);
    } catch (_) {
      // ignore for MVP
    }
  }

  return (
    <IntlProvider locale={locale} messages={messages[locale]}>
      <div style={{ border: "1px solid #0070f3", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
        <div style={{ marginBottom: "0.5rem", fontSize: "0.9rem" }}>
          <b>API:</b>{" "}
          <code>
            {typeof window !== "undefined" && !(window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
              ? "http://backend:8000"
              : "http://localhost:8000"}
          </code>{" "}
          —{" "}
          <span style={{ color: connected === false ? "red" : connected ? "green" : "#666" }}>
            {connected === null ? "checking..." : connected ? "connected" : "unreachable"}
          </span>
        </div>
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
            <b>Context (JSON):</b>
            <input
              type="text"
              value={contextText}
              onChange={e => setContextText(e.target.value)}
              placeholder='e.g. {"topic":"travel"}'
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
        {!isBrowser && (
          <div style={{ color: "orange", marginBottom: "1rem" }}>
            Rendering on server... UI will hydrate in the browser.
          </div>
        )}
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
        {response && (
          <div style={{ marginTop: "0.75rem" }}>
            <button onClick={() => sendFeedback("up")} disabled={lastRating === "up"} aria-label="Thumbs up">👍</button>
            <button onClick={() => sendFeedback("down")} disabled={lastRating === "down"} style={{ marginLeft: "0.5rem" }} aria-label="Thumbs down">👎</button>
            {lastRating && <span style={{ marginLeft: "0.5rem" }}>Thanks for the feedback.</span>}
          </div>
        )}

        {/* Privacy Consent Dialog (inline) */}
        {privacyPrompt?.policy_required && (
          <div role="dialog" aria-modal="true" style={{ marginTop: "1rem", padding: "1rem", border: "2px solid #fa0", borderRadius: 8, background: "#fffdf5" }}>
            <h4 style={{ marginTop: 0 }}>Permission required</h4>
            <p style={{ margin: "0.25rem 0" }}>
              Action: <code>{privacyPrompt.action}</code>
            </p>
            <p style={{ margin: "0.25rem 0" }}>
              Reason: {privacyPrompt.reason}
            </p>
            <label style={{ display: "block", marginTop: "0.5rem" }}>
              <input type="checkbox" checked={autoApproveSession} onChange={e => setAutoApproveSession(e.target.checked)} /> Auto-approve for this session
            </label>
            <div style={{ marginTop: "0.75rem" }}>
              <button onClick={() => submitPrivacyDecision(true)} disabled={loading} style={{ marginRight: "0.5rem" }}>Allow</button>
              <button onClick={() => submitPrivacyDecision(false)} disabled={loading}>Deny</button>
            </div>
          </div>
        )}
      </div>
    </IntlProvider>
  );
}
