import React, { useEffect, useState } from "react";

function IntegrationManagerPanel() {
  const [integrations, setIntegrations] = useState([]);
  const [selectedProvider, setSelectedProvider] = useState(null);
  const [config, setConfig] = useState({});
  const [status, setStatus] = useState({});
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("/integrations/")
      .then(res => res.json())
      .then(setIntegrations)
      .catch(() => setMessage("Failed to load integrations."));
  }, []);

  const handleSelect = provider => {
    setSelectedProvider(provider);
    setMessage("");
    fetch(`/integrations/${provider}/status`)
      .then(res => res.json())
      .then(data => {
        setStatus(data);
        setConfig(data.config || {});
      })
      .catch(() => setMessage("Failed to load provider status."));
  };

  const handleConfigChange = (key, value) => {
    setConfig(cfg => ({ ...cfg, [key]: value }));
  };

  const handleSave = () => {
    fetch(`/integrations/${selectedProvider}/configure`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ config })
    })
      .then(res => res.json())
      .then(data => {
        setMessage(data.configured ? "Integration configured!" : "Missing required keys.");
        setStatus(data);
      })
      .catch(() => setMessage("Failed to save config."));
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Integration Manager</h2>
      {message && <div style={{ color: "red", marginBottom: "1rem" }}>{message}</div>}
      <ul>
        {integrations.map(i => (
          <li key={i.provider} style={{ marginBottom: "1rem" }}>
            <b>{i.name}</b> — {i.description}
            <span style={{ marginLeft: "1rem", color: i.configured ? "green" : "orange" }}>
              {i.configured ? "Configured" : "Not Configured"}
            </span>
            <a href={i.docs_url} target="_blank" rel="noopener noreferrer" style={{ marginLeft: "1rem" }}>
              Docs
            </a>
            <button style={{ marginLeft: "1rem" }} onClick={() => handleSelect(i.provider)}>
              Configure
            </button>
          </li>
        ))}
      </ul>
      {selectedProvider && (
        <div style={{ border: "1px solid #aaa", padding: "1rem", marginTop: "2rem" }}>
          <h3>Configure {selectedProvider}</h3>
          {integrations
            .find(i => i.provider === selectedProvider)
            .required_keys.map(key => (
              <div key={key} style={{ marginBottom: "1rem" }}>
                <label>
                  {key}:{" "}
                  <input
                    type="text"
                    value={config[key] || ""}
                    onChange={e => handleConfigChange(key, e.target.value)}
                    style={{ width: "300px" }}
                  />
                </label>
                <a
                  href={
                    integrations.find(i => i.provider === selectedProvider).docs_url
                  }
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ marginLeft: "1rem", textDecoration: "underline", color: "#09c" }}
                >
                  Get API Key
                </a>
              </div>
            ))}
          <button onClick={handleSave}>Save</button>
        </div>
      )}
    </div>
  );
}

export default IntegrationManagerPanel;
