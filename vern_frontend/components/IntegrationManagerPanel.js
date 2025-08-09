import React, { useEffect, useState } from "react";

function IntegrationManagerPanel() {
  const [integrations, setIntegrations] = useState([]);
  const [selectedProvider, setSelectedProvider] = useState(null);
  const [config, setConfig] = useState({});
  const [status, setStatus] = useState({});
  const [message, setMessage] = useState("");

  // Ollama model selection
  const [ollamaModels, setOllamaModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState("");

  useEffect(() => {
    fetch("/integrations/")
      .then(res => res.json())
      .then(setIntegrations)
      .catch(() => setMessage("Failed to load integrations."));
    fetch("/integrations/ollama/models")
      .then(res => res.json())
      .then(data => setOllamaModels(data.models || []))
      .catch(() => setOllamaModels([]));
  }, []);

  const handleSelect = provider => {
    setSelectedProvider(provider);
    setMessage("");
    fetch(`/integrations/${provider}/status`)
      .then(res => res.json())
      .then(data => {
        setStatus(data);
        setConfig(data.config || {});
        // If Ollama, set selected model from config
        if (provider === "ollama" && data.config && data.config.model) {
          setSelectedModel(data.config.model);
        }
      })
      .catch(() => setMessage("Failed to load provider status."));
  };

  const handleConfigChange = (key, value) => {
    setConfig(cfg => ({ ...cfg, [key]: value }));
    if (selectedProvider === "ollama" && key === "model") setSelectedModel(value);
  };

  const handleModelChange = (value) => {
    setSelectedModel(value);
    setConfig(cfg => ({ ...cfg, model: value }));
  };

  const handleSave = () => {
    fetch(`/integrations/${selectedProvider}/configure`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ config: selectedProvider === "ollama" ? { ...config, model: selectedModel } : config })
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
          {/* Ollama model selection dropdown */}
          {selectedProvider === "ollama" && (
            <div style={{ marginBottom: "1rem" }}>
              <strong>LLM/Ollama Model:</strong>
              <select
                value={selectedModel}
                onChange={e => handleModelChange(e.target.value)}
                title="Select LLM/Ollama model"
                style={{ marginLeft: "1rem" }}
              >
                <option value="">Select model</option>
                {ollamaModels.map(model => (
                  <option key={model} value={model}>
                    {model}
                  </option>
                ))}
              </select>
            </div>
          )}
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
