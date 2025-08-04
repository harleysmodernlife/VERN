// vern_frontend/components/OnboardingPanel.js
import React, { useState, useEffect } from "react";
import { IntlProvider, FormattedMessage } from "react-intl";

const messages = {
  en: {
    panelTitle: "Onboarding & Accessibility",
    checklist: [
      "Read the README",
      "Configured .env",
      "Tested a plugin/tool",
      "Joined the Community",
      "Reviewed Security Guidelines"
    ],
    complete: "Onboarding complete! You're ready to use VERN.",
    feedback: "Feedback:",
    submit: "Submit Feedback",
    thankYou: "Thank you for your feedback!",
    language: "Language",
    neo4jMissing: "Neo4j graph memory is not available. For full features, launch with Docker Compose or start Neo4j manually.",
    backendMissing: "Backend API is not running. Please start the backend or use Docker Compose."
  },
  es: {
    panelTitle: "Introducción y Accesibilidad",
    checklist: [
      "Lea el README",
      "Configuró .env",
      "Probó un plugin/herramienta",
      "Se unió a la Comunidad",
      "Revisó las Directrices de Seguridad"
    ],
    complete: "¡Introducción completa! Ya puede usar VERN.",
    feedback: "Comentarios:",
    submit: "Enviar Comentarios",
    thankYou: "¡Gracias por sus comentarios!",
    language: "Idioma",
    neo4jMissing: "La memoria de grafo Neo4j no está disponible. Para todas las funciones, inicie con Docker Compose o inicie Neo4j manualmente.",
    backendMissing: "La API de backend no está en funcionamiento. Por favor, inicie el backend o use Docker Compose."
  }
};

export default function OnboardingPanel() {
  const [locale, setLocale] = useState(() => localStorage.getItem("vern_lang") || "en");
  const [checklist, setChecklist] = useState(() =>
    Object.fromEntries(messages[locale].checklist.map(item => [item, false]))
  );
  const [feedback, setFeedback] = useState("");
  const [submitted, setSubmitted] = useState(false);

  // Dependency status
  const [neo4jStatus, setNeo4jStatus] = useState(null);
  const [backendStatus, setBackendStatus] = useState(null);

  useEffect(() => {
    // Reset checklist when language changes
    setChecklist(Object.fromEntries(messages[locale].checklist.map(item => [item, false])));
  }, [locale]);

  useEffect(() => {
    // Check backend status
    fetch("http://localhost:8000/status")
      .then(res => res.ok ? setBackendStatus(true) : setBackendStatus(false))
      .catch(() => setBackendStatus(false));
    // Check Neo4j status (try a simple query endpoint)
    fetch("http://localhost:8000/memory/entity?entity_id=test")
      .then(res => res.ok ? setNeo4jStatus(true) : setNeo4jStatus(false))
      .catch(() => setNeo4jStatus(false));
  }, []);

  function handleCheck(item) {
    setChecklist({ ...checklist, [item]: !checklist[item] });
  }

  function handleSubmit() {
    setSubmitted(true);
    setFeedback("");
  }

  return (
    <IntlProvider locale={locale} messages={messages[locale]}>
      <div style={{ border: "1px solid #09c", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }} role="region" aria-label="Onboarding and Accessibility Panel">
        {/* Dependency notifications */}
        {backendStatus === false && (
          <div style={{ color: "red", marginBottom: "1rem", fontWeight: "bold" }}>
            <FormattedMessage id="backendMissing" defaultMessage={messages[locale].backendMissing} />
          </div>
        )}
        {neo4jStatus === false && (
          <div style={{ color: "orange", marginBottom: "1rem", fontWeight: "bold" }}>
            <FormattedMessage id="neo4jMissing" defaultMessage={messages[locale].neo4jMissing} />
          </div>
        )}
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="lang-select-onboard" style={{ marginRight: "0.5rem" }}>
            <FormattedMessage id="language" defaultMessage="Language" />:
          </label>
          <select
            id="lang-select-onboard"
            value={locale}
            onChange={e => setLocale(e.target.value)}
            aria-label="Select language"
            tabIndex={0}
            aria-describedby="lang-desc-onboard"
          >
            <option value="en">English</option>
            <option value="es">Español</option>
          </select>
          <span id="lang-desc-onboard" style={{ display: "none" }}>
            Choose your preferred language for onboarding and accessibility.
          </span>
        </div>
        {/* Backend selection guidance */}
        <div style={{ marginBottom: "1rem", background: "#f9f9f9", border: "1px solid #ccc", padding: "1rem", borderRadius: "6px" }}>
          <strong>Backend Selection Guidance:</strong>
          <ul>
            <li>
              <span role="img" aria-label="light">💡</span> For laptops with &lt; 8GB RAM, select lightweight backends (e.g. <b>espeak-asr</b>, <b>espeak-tts</b>, <b>tesseract</b>).
            </li>
            <li>
              <span role="img" aria-label="heavy">⚡</span> Whisper and Coqui require more RAM/CPU and are optional. Use only if you have sufficient resources.
            </li>
            <li>
              <span role="img" aria-label="config">🛠️</span> You can change backend options in the Config Editor panel. All backends are optional and configurable.
            </li>
            <li>
              <span role="img" aria-label="fallback">🔄</span> If a backend is not installed or resources are low, VERN will automatically fall back to a stub or lightweight backend.
            </li>
            <li>
              <span role="img" aria-label="docs">📖</span> See README and Agent Guides for details on backend options and resource requirements.
            </li>
          </ul>
        </div>
        <h3 tabIndex={0} aria-label="Onboarding and Accessibility">{<FormattedMessage id="panelTitle" defaultMessage="Onboarding & Accessibility" />}</h3>
        <ul>
          {messages[locale].checklist.map(item => (
            <li key={item} style={{ position: "relative" }}>
              <label>
                <input
                  type="checkbox"
                  checked={checklist[item]}
                  onChange={() => handleCheck(item)}
                  aria-checked={checklist[item]}
                  aria-label={`Checklist item: ${item}`}
                  title={`Learn more about "${item}"`}
                />{" "}
                {item}
                <a
                  href={
                    item === "Read the README"
                      ? "/README.md"
                      : item === "Configured .env"
                      ? "/.env"
                      : item === "Tested a plugin/tool"
                      ? "/QUICKSTART.md"
                      : item === "Joined the Community"
                      ? "https://github.com/harleysmodernlife/VERN#community"
                      : item === "Reviewed Security Guidelines"
                      ? "/SECURITY_AND_GIT_GUIDELINES.md"
                      : "#"
                  }
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    marginLeft: "0.5rem",
                    textDecoration: "underline",
                    color: "#09c",
                    fontSize: "0.9em"
                  }}
                  aria-label={`Open help for ${item}`}
                  title={`Open help for ${item}`}
                >
                  [?]
                </a>
              </label>
            </li>
          ))}
        </ul>
        {/* Persona selection and initial profile setup */}
        <PersonaSetup locale={locale} />
        {Object.values(checklist).every(Boolean) && (
          <div style={{ color: "green", fontWeight: "bold" }}>
            <FormattedMessage id="complete" defaultMessage="Onboarding complete! You're ready to use VERN." />
          </div>
        )}
        <div style={{ marginTop: "1rem" }}>
          <label>
            <FormattedMessage id="feedback" defaultMessage="Feedback:" />
            <textarea
              value={feedback}
              onChange={e => setFeedback(e.target.value)}
              style={{ width: "100%", minHeight: "60px", marginTop: "0.5rem" }}
              aria-label={messages[locale].feedback}
            />
          </label>
          <button onClick={handleSubmit} style={{ marginTop: "0.5rem" }}>
            <FormattedMessage id="submit" defaultMessage="Submit Feedback" />
          </button>
          {submitted && <div style={{ color: "green" }}><FormattedMessage id="thankYou" defaultMessage="Thank you for your feedback!" /></div>}
        </div>
      </div>
    </IntlProvider>
  );
}

// Persona selection and profile setup component
function PersonaSetup({ locale }) {
  const [persona, setPersona] = useState("default");
  const [username, setUsername] = useState("");
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  async function saveOnboarding() {
    setSaving(true);
    setMessage("");
    try {
      const res = await fetch("http://localhost:8000/users/onboard", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, persona })
      });
      const data = await res.json();
      setMessage(data.status === "success" ? "Onboarding saved!" : "Error saving onboarding");
    } catch (err) {
      setMessage("Error saving onboarding");
    }
    setSaving(false);
  }

  return (
    <div style={{ marginTop: "1rem", marginBottom: "1rem", padding: "1rem", background: "#eef", borderRadius: "6px" }}>
      <label>
        <b>{locale === "en" ? "Username:" : "Nombre de usuario:"}</b>
        <input
          type="text"
          value={username}
          onChange={e => setUsername(e.target.value)}
          style={{ marginLeft: "0.5rem", width: "200px" }}
        />
      </label>
      <div style={{ marginTop: "1rem" }}>
        <b>{locale === "en" ? "Select Persona:" : "Selecciona Persona:"}</b>
        <select value={persona} onChange={e => setPersona(e.target.value)} style={{ marginLeft: "0.5rem" }}>
          <option value="default">{locale === "en" ? "Default" : "Por defecto"}</option>
          <option value="coach">{locale === "en" ? "Health Coach" : "Entrenador de salud"}</option>
          <option value="medic">{locale === "en" ? "Medical Assistant" : "Asistente médico"}</option>
          <option value="mindfulness">{locale === "en" ? "Mindfulness Guide" : "Guía de mindfulness"}</option>
        </select>
      </div>
      <button onClick={saveOnboarding} disabled={saving || !username} style={{ marginTop: "1rem" }}>
        {saving ? "Saving..." : locale === "en" ? "Save Onboarding" : "Guardar"}
      </button>
      {message && (
        <div style={{ marginTop: "0.5rem", color: message.startsWith("Error") ? "red" : "green" }}>
          {message}
        </div>
      )}
      {message.startsWith("Error") && (
        <div style={{ color: "red", marginTop: "0.5rem" }}>
          Please check your internet connection and try again, or contact support if the problem persists.
        </div>
      )}
    </div>
  );
}
