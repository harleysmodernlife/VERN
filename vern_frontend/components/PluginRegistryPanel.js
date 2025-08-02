// vern_frontend/components/PluginRegistryPanel.js
import React, { useEffect, useState } from "react";
import { IntlProvider, FormattedMessage } from "react-intl";

const messages = {
  en: {
    panelTitle: "Plugin Registry",
    loading: "Loading plugins...",
    name: "Name",
    description: "Description",
    enabled: "Enabled",
    action: "Action",
    yes: "Yes",
    no: "No",
    enable: "Enable",
    disable: "Disable",
    language: "Language"
  },
  es: {
    panelTitle: "Registro de Plugins",
    loading: "Cargando plugins...",
    name: "Nombre",
    description: "Descripción",
    enabled: "Habilitado",
    action: "Acción",
    yes: "Sí",
    no: "No",
    enable: "Habilitar",
    disable: "Deshabilitar",
    language: "Idioma"
  }
};

export default function PluginRegistryPanel() {
  const [plugins, setPlugins] = useState([]);
  const [loading, setLoading] = useState(true);
  const [locale, setLocale] = useState(() => localStorage.getItem("vern_lang") || "en");

  async function fetchPlugins() {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/plugins/");
      const data = await res.json();
      setPlugins(data);
    } catch (err) {
      setPlugins([]);
    }
    setLoading(false);
  }

  async function togglePlugin(name, enable) {
    await fetch(`http://localhost:8000/plugins/${name}/${enable ? "enable" : "disable"}`, {
      method: "POST"
    });
    fetchPlugins();
  }

  useEffect(() => {
    fetchPlugins();
  }, []);

  useEffect(() => {
    localStorage.setItem("vern_lang", locale);
  }, [locale]);

  return (
    <IntlProvider locale={locale} messages={messages[locale]}>
      <div style={{ border: "1px solid #0a0", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="lang-select-plugin" style={{ marginRight: "0.5rem" }}>
            <FormattedMessage id="language" defaultMessage="Language" />:
          </label>
          <select
            id="lang-select-plugin"
            value={locale}
            onChange={e => setLocale(e.target.value)}
            aria-label="Select language"
            tabIndex={0}
            aria-describedby="lang-desc-plugin"
          >
            <option value="en">English</option>
            <option value="es">Español</option>
          </select>
          <span id="lang-desc-plugin" style={{ display: "none" }}>
            Choose your preferred language for the plugin registry.
          </span>
        </div>
        <h3>
          <FormattedMessage id="panelTitle" defaultMessage="Plugin Registry" />
        </h3>
        {loading ? (
          <p><FormattedMessage id="loading" defaultMessage="Loading plugins..." /></p>
        ) : (
          <table>
            <thead>
              <tr>
                <th><FormattedMessage id="name" defaultMessage="Name" /></th>
                <th><FormattedMessage id="description" defaultMessage="Description" /></th>
                <th><FormattedMessage id="enabled" defaultMessage="Enabled" /></th>
                <th><FormattedMessage id="action" defaultMessage="Action" /></th>
                <th>Invoke</th>
              </tr>
            </thead>
            <tbody>
              {plugins.map(plugin => (
                <PluginRow
                  key={plugin.name}
                  plugin={plugin}
                  togglePlugin={togglePlugin}
                  locale={locale}
                />
              ))}
            </tbody>
          </table>
        )}
      </div>
    </IntlProvider>
  );
}

// Row component with plugin invocation UI
function PluginRow({ plugin, togglePlugin, locale }) {
  const [args, setArgs] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  async function invokePlugin() {
    setLoading(true);
    setResult("");
    try {
      const res = await fetch(`http://localhost:8000/plugins/${plugin.name}/call`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ args: args ? args.split(",").map(a => a.trim()) : [], kwargs: {} })
      });
      const data = await res.json();
      setResult(data.result ? JSON.stringify(data.result) : "No result");
    } catch (err) {
      setResult("Error invoking plugin");
    }
    setLoading(false);
  }

  return (
    <tr>
      <td>{plugin.name}</td>
      <td>{plugin.description}</td>
      <td>{plugin.enabled ? <FormattedMessage id="yes" defaultMessage="Yes" /> : <FormattedMessage id="no" defaultMessage="No" />}</td>
      <td>
        <button onClick={() => togglePlugin(plugin.name, !plugin.enabled)}>
          {plugin.enabled ? <FormattedMessage id="disable" defaultMessage="Disable" /> : <FormattedMessage id="enable" defaultMessage="Enable" />}
        </button>
      </td>
      <td>
        <input
          type="text"
          placeholder={locale === "en" ? "Args (comma-separated)" : "Args (separados por coma)"}
          value={args}
          onChange={e => setArgs(e.target.value)}
          style={{ width: "120px", marginRight: "0.5rem" }}
        />
        <button onClick={invokePlugin} disabled={!plugin.enabled || loading}>
          {loading ? "..." : "Invoke"}
        </button>
        {result && (
          <div style={{ marginTop: "0.5rem", fontSize: "0.9em", color: result.startsWith("Error") ? "red" : "green" }}>
            {result}
          </div>
        )}
      </td>
    </tr>
  );
}
