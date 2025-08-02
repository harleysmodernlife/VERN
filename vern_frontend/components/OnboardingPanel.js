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
    language: "Language"
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
    language: "Idioma"
  }
};

export default function OnboardingPanel() {
  const [locale, setLocale] = useState(() => localStorage.getItem("vern_lang") || "en");
  const [checklist, setChecklist] = useState(() =>
    Object.fromEntries(messages[locale].checklist.map(item => [item, false]))
  );
  const [feedback, setFeedback] = useState("");
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    // Reset checklist when language changes
    setChecklist(Object.fromEntries(messages[locale].checklist.map(item => [item, false])));
  }, [locale]);

  function handleCheck(item) {
    setChecklist({ ...checklist, [item]: !checklist[item] });
  }

  function handleSubmit() {
    setSubmitted(true);
    setFeedback("");
  }

  return (
    <IntlProvider locale={locale} messages={messages[locale]}>
      <div style={{ border: "1px solid #09c", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
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
        <h3>
          <FormattedMessage id="panelTitle" defaultMessage="Onboarding & Accessibility" />
        </h3>
        <ul>
          {messages[locale].checklist.map(item => (
            <li key={item}>
              <label>
                <input
                  type="checkbox"
                  checked={checklist[item]}
                  onChange={() => handleCheck(item)}
                  aria-checked={checklist[item]}
                  aria-label={item}
                />{" "}
                {item}
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
    </div>
  );
}
