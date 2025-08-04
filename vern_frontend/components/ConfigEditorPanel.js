import React, { useState, useEffect } from "react";

export default function ConfigEditorPanel() {
  const [envConfig, setEnvConfig] = useState({});
  const [yamlConfig, setYamlConfig] = useState({});
  const [envEdit, setEnvEdit] = useState({});
  const [yamlEdit, setYamlEdit] = useState({});
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorLogs, setErrorLogs] = useState([]);
  const [validation, setValidation] = useState({ missing: [], placeholders: [], valid: true });

  // Fetch .env config
  useEffect(() => {
    fetch("/config/env")
      .then(res => res.json())
      .then(data => {
        setEnvConfig(data);
        setEnvEdit(data);
      })
      .catch(() => setError("Failed to load .env config."));
    fetch("/config/yaml")
      .then(res => res.json())
      .then(data => {
        setYamlConfig(data);
        setYamlEdit(data);
      })
      .catch(() => setError("Failed to load YAML config."));
  }, []);

  // Fetch error logs
  useEffect(() => {
    fetch("/config/error")
      .then(res => res.json())
      .then(data => setErrorLogs(data))
      .catch(() => setErrorLogs([]));
    fetch("/config/validate")
      .then(res => res.json())
      .then(data => setValidation(data))
      .catch(() => setValidation({ missing: [], placeholders: [], valid: true }));
  }, []);

  // Handle .env input change
  const handleEnvChange = (key, value) => {
    setEnvEdit(prev => ({ ...prev, [key]: value }));
  };

  // Handle YAML input change
  const handleYamlChange = (key, value) => {
    setYamlEdit(prev => ({ ...prev, [key]: value }));
  };

  // Save .env config
  const saveEnv = () => {
    setLoading(true);
    setError("");
    setSuccess("");
    fetch("/config/env", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ values: envEdit })
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to save .env config.");
        return res.json();
      })
      .then(() => {
        setSuccess(".env config saved.");
        setEnvConfig(envEdit);
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  };

  // Save YAML config
  const saveYaml = () => {
    setLoading(true);
    setError("");
    setSuccess("");
    fetch("/config/yaml", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ values: yamlEdit })
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to save YAML config.");
        return res.json();
      })
      .then(() => {
        setSuccess("YAML config saved.");
        setYamlConfig(yamlEdit);
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  };

  return (
    <div style={{ border: "1px solid #aaa", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
      <h2>Config Editor</h2>
      <div style={{ marginBottom: "1rem", color: "#555" }}>
        <b>Need help?</b> See the <a href="/QUICKSTART.md" target="_blank" rel="noopener noreferrer">Quickstart Guide</a> for config instructions.
      </div>
      {error && <div style={{ color: "red", marginBottom: "1rem" }}>Error: {error}</div>}
      {success && <div style={{ color: "green", marginBottom: "1rem" }}>{success}</div>}
      <div>
        <h3>.env Config</h3>
        {Object.keys(envEdit).map(key => (
          <div key={key} style={{ marginBottom: "0.5rem" }}>
            <label style={{ marginRight: "0.5rem" }} htmlFor={`env-input-${key}`}>{key}:</label>
            <input
              id={`env-input-${key}`}
              type="text"
              value={envEdit[key]}
              onChange={e => handleEnvChange(key, e.target.value)}
              style={{ width: "200px" }}
              aria-label={`.env config input for ${key}`}
            />
          </div>
        ))}
        {!validation.valid && (
          <div style={{ color: "orange", marginBottom: "1rem" }} role="alert" aria-live="assertive">
            <strong>Config Validation Issues:</strong>
            {validation.missing.length > 0 && (
              <div aria-label="Missing config keys">Missing: {validation.missing.join(", ")}</div>
            )}
            {validation.placeholders.length > 0 && (
              <div aria-label="Config placeholders">Placeholders: {validation.placeholders.join(", ")}</div>
            )}
          </div>
        )}
        <button onClick={saveEnv} disabled={loading || !validation.valid}>Save .env</button>
      </div>
      <div style={{ marginTop: "2rem" }}>
        <h3>YAML Config</h3>
        {/* Backend selection UI */}
        <div style={{ marginBottom: "1rem" }}>
          <strong>ASR Backend:</strong>
          <select
            value={yamlEdit.default_asr || ""}
            onChange={e => handleYamlChange("default_asr", e.target.value)}
            title="Select Speech-to-Text backend (Whisper, Google, Espeak, etc.)"
            style={{ marginLeft: "1rem" }}
          >
            {yamlConfig.asr_backends &&
              Object.keys(yamlConfig.asr_backends).map(key => (
                <option key={key} value={key}>
                  {key} ({yamlConfig.asr_backends[key].provider})
                </option>
              ))}
          </select>
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <strong>TTS Backend:</strong>
          <select
            value={yamlEdit.default_tts || ""}
            onChange={e => handleYamlChange("default_tts", e.target.value)}
            title="Select Text-to-Speech backend (Coqui, Google, Espeak, etc.)"
            style={{ marginLeft: "1rem" }}
          >
            {yamlConfig.tts_backends &&
              Object.keys(yamlConfig.tts_backends).map(key => (
                <option key={key} value={key}>
                  {key} ({yamlConfig.tts_backends[key].provider})
                </option>
              ))}
          </select>
        </div>
        <div style={{ marginBottom: "1rem" }}>
          <strong>Vision Backend:</strong>
          <select
            value={yamlEdit.default_vision || ""}
            onChange={e => handleYamlChange("default_vision", e.target.value)}
            title="Select Vision backend (Tesseract, Google Vision, etc.)"
            style={{ marginLeft: "1rem" }}
          >
            {yamlConfig.vision_backends &&
              Object.keys(yamlConfig.vision_backends).map(key => (
                <option key={key} value={key}>
                  {key} ({yamlConfig.vision_backends[key].provider})
                </option>
              ))}
          </select>
        </div>
        {/* Advanced mode toggle */}
        <div style={{ marginBottom: "1rem" }}>
          <label>
            <input
              type="checkbox"
              checked={yamlEdit.advancedMode || false}
              onChange={e => handleYamlChange("advancedMode", e.target.checked)}
            />
            Advanced Mode
          </label>
          <span style={{ marginLeft: "1rem", color: "#888" }}>
            Toggle to edit per-agent backend overrides and advanced options.
          </span>
        </div>
        {/* Fallback to raw YAML editing in advanced mode */}
        {yamlEdit.advancedMode && (
          <div style={{ marginTop: "1rem" }}>
            <strong>Raw YAML Editor (Advanced):</strong>
            {Object.keys(yamlEdit).map(key => (
              <div key={key} style={{ marginBottom: "0.5rem" }}>
            <label style={{ marginRight: "0.5rem" }} htmlFor={`yaml-input-${key}`}>{key}:</label>
            <input
              id={`yaml-input-${key}`}
              type="text"
              value={yamlEdit[key]}
              onChange={e => handleYamlChange(key, e.target.value)}
              style={{ width: "200px" }}
              aria-label={`YAML config input for ${key}`}
            />
              </div>
            ))}
          </div>
        )}
        <button onClick={saveYaml} disabled={loading}>Save YAML</button>
      </div>
      <div style={{ marginTop: "2rem", borderTop: "1px solid #ddd", paddingTop: "1rem" }}>
        <h3>Error Logs</h3>
        {errorLogs.length === 0 ? (
          <div>No config errors reported.</div>
        ) : (
          <ul>
            {errorLogs.map((err, idx) => (
              <li key={idx} style={{ color: "red" }}>
                <strong>{err.error}</strong>
                {err.context && <span> ({err.context})</span>}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
