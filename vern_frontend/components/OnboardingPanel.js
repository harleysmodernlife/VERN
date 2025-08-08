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

// Enhanced onboarding wizard with backend triggers and TODOs
export default function OnboardingPanel() {
  const [locale, setLocale] = useState(() => localStorage.getItem("vern_lang") || "en");
  const [checklist, setChecklist] = useState(() =>
    Object.fromEntries(messages[locale].checklist.map(item => [item, false]))
  );
  const [feedback, setFeedback] = useState("");
  const [submitted, setSubmitted] = useState(false);

  // Wizard step state
  const wizardSteps = [
    "Welcome",
    "Configure Environment",
    "Initialize Database",
    "Register Agents",
    "Enable Plugins",
    "Profile Setup",
    "Finish"
  ];
  const [stepIdx, setStepIdx] = useState(0);
  const [wizardStatus, setWizardStatus] = useState({
    db: null,
    agent: null,
    plugin: null
  });

  // Dependency status
  const [neo4jStatus, setNeo4jStatus] = useState(null);
  const [backendStatus, setBackendStatus] = useState(null);

  useEffect(() => {
    setChecklist(Object.fromEntries(messages[locale].checklist.map(item => [item, false])));
  }, [locale]);

  useEffect(() => {
    fetch("http://localhost:8000/status")
      .then(res => res.ok ? setBackendStatus(true) : setBackendStatus(false))
      .catch(() => setBackendStatus(false));
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

  // Wizard navigation
  function nextStep() {
    setStepIdx(idx => Math.min(idx + 1, wizardSteps.length - 1));
  }
  function prevStep() {
    setStepIdx(idx => Math.max(idx - 1, 0));
  }

  // Backend automation triggers
  async function triggerDbInit() {
    setWizardStatus(s => ({ ...s, db: "pending" }));
    try {
      const res = await fetch("http://localhost:8000/admin/db/verify");
      const data = await res.json();
      setWizardStatus(s => ({ ...s, db: data.ok ? "success" : "fail" }));
    } catch {
      setWizardStatus(s => ({ ...s, db: "fail" }));
    }
  }
  async function triggerAgentRegistration() {
    setWizardStatus(s => ({ ...s, agent: "pending" }));
    try {
      const res = await fetch("http://localhost:8000/agents/heartbeat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: "admin", cluster: "Admin" })
      });
      const data = await res.json();
      setWizardStatus(s => ({ ...s, agent: data.ok ? "success" : "fail" }));
    } catch {
      setWizardStatus(s => ({ ...s, agent: "fail" }));
    }
  }
  async function triggerPluginEnable() {
    setWizardStatus(s => ({ ...s, plugin: "pending" }));
    try {
      const res = await fetch("http://localhost:8000/plugins/espeak-tts/enable", { method: "POST" });
      const data = await res.json();
      setWizardStatus(s => ({ ...s, plugin: data.status === "enabled" ? "success" : "fail" }));
    } catch {
      setWizardStatus(s => ({ ...s, plugin: "fail" }));
    }
  }

  // TODO: Add analytics for onboarding completion
  // TODO: Add more backend checks and plugin options
  // TODO: Refactor wizard steps for extensibility

  return (
    <IntlProvider locale={locale} messages={messages[locale]}>
      <div style={{ border: "1px solid #09c", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }} role="region" aria-label="Onboarding and Accessibility Panel">
        {/* Progress bar */}
        <div style={{ marginBottom: "1rem" }}>
          <div style={{ width: "100%", background: "#eee", height: "8px", borderRadius: "4px" }}>
            <div style={{
              width: `${((stepIdx + 1) / wizardSteps.length) * 100}%`,
              background: "#09c",
              height: "8px",
              borderRadius: "4px"
            }} />
          </div>
          <div style={{ marginTop: "0.5rem", fontWeight: "bold" }}>
            Step {stepIdx + 1} of {wizardSteps.length}: {wizardSteps[stepIdx]}
          </div>
        </div>
        {/* Wizard step content */}
        {stepIdx === 0 && (
          <div>
            <h3>Welcome to VERN Onboarding</h3>
            <p>This wizard will guide you through initial setup and configuration.</p>
            <button onClick={nextStep}>Start Setup</button>
          </div>
        )}
        {stepIdx === 1 && (
          <div>
            <h3>Configure Environment</h3>
            <ul>
              <li>Review <a href="/README.md" target="_blank">README</a></li>
              <li>Configure <a href="/.env" target="_blank">.env</a> variables</li>
              <li>Review <a href="/SECURITY_AND_GIT_GUIDELINES.md" target="_blank">Security Guidelines</a></li>
            </ul>
            <button onClick={prevStep}>Back</button>
            <button onClick={nextStep}>Next</button>
          </div>
        )}
        {stepIdx === 2 && (
          <div>
            <h3>Initialize Database</h3>
            <button onClick={triggerDbInit} disabled={wizardStatus.db === "pending"}>
              {wizardStatus.db === "success" ? "DB Initialized" : wizardStatus.db === "fail" ? "Retry DB Init" : "Initialize DB"}
            </button>
            {wizardStatus.db === "success" && <span style={{ color: "green", marginLeft: "1rem" }}>Success!</span>}
            {wizardStatus.db === "fail" && <span style={{ color: "red", marginLeft: "1rem" }}>Failed</span>}
            <button onClick={prevStep} style={{ marginLeft: "1rem" }}>Back</button>
            <button onClick={nextStep} style={{ marginLeft: "1rem" }} disabled={wizardStatus.db !== "success"}>Next</button>
          </div>
        )}
        {stepIdx === 3 && (
          <div>
            <h3>Register Admin Agent</h3>
            <button onClick={triggerAgentRegistration} disabled={wizardStatus.agent === "pending"}>
              {wizardStatus.agent === "success" ? "Agent Registered" : wizardStatus.agent === "fail" ? "Retry Registration" : "Register Agent"}
            </button>
            {wizardStatus.agent === "success" && <span style={{ color: "green", marginLeft: "1rem" }}>Success!</span>}
            {wizardStatus.agent === "fail" && <span style={{ color: "red", marginLeft: "1rem" }}>Failed</span>}
            <button onClick={prevStep} style={{ marginLeft: "1rem" }}>Back</button>
            <button onClick={nextStep} style={{ marginLeft: "1rem" }} disabled={wizardStatus.agent !== "success"}>Next</button>
          </div>
        )}
        {stepIdx === 4 && (
          <div>
            <h3>Enable Default Plugin</h3>
            <button onClick={triggerPluginEnable} disabled={wizardStatus.plugin === "pending"}>
              {wizardStatus.plugin === "success" ? "Plugin Enabled" : wizardStatus.plugin === "fail" ? "Retry Enable" : "Enable Plugin"}
            </button>
            {wizardStatus.plugin === "success" && <span style={{ color: "green", marginLeft: "1rem" }}>Success!</span>}
            {wizardStatus.plugin === "fail" && <span style={{ color: "red", marginLeft: "1rem" }}>Failed</span>}
            <button onClick={prevStep} style={{ marginLeft: "1rem" }}>Back</button>
            <button onClick={nextStep} style={{ marginLeft: "1rem" }} disabled={wizardStatus.plugin !== "success"}>Next</button>
          </div>
        )}
        {stepIdx === 5 && (
          <div>
            <h3>Profile Setup</h3>
            <PersonaSetup locale={locale} />
            <button onClick={prevStep}>Back</button>
            <button onClick={nextStep} style={{ marginLeft: "1rem" }}>Next</button>
          </div>
        )}
        {stepIdx === 6 && (
          <div>
            <h3>Finish</h3>
            <p>Onboarding complete! You're ready to use VERN.</p>
            <button onClick={() => setStepIdx(0)}>Restart Wizard</button>
          </div>
        )}
        {/* Checklist and feedback remain for accessibility */}
        <div style={{ marginTop: "2rem" }}>
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
