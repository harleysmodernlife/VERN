import React, { useState, useEffect } from "react";

export default function PluginMarketplacePanel() {
  const [plugins, setPlugins] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [configModal, setConfigModal] = useState({ open: false, plugin: null });
  const [pluginConfigs, setPluginConfigs] = useState({});

  // Fetch plugins
  useEffect(() => {
    fetch("/plugins/")
      .then(res => res.json())
      .then(data => setPlugins(data))
      .catch(() => setPlugins([]));
  }, [success]);

  // Enable/disable plugin
  const togglePlugin = (name, enable) => {
    setError("");
    setSuccess("");
    fetch(`/plugins/${name}/${enable ? "enable" : "disable"}`, { method: "POST" })
      .then(res => res.json())
      .then(data => setSuccess(data.status))
      .catch(() => setError("Failed to update plugin status."));
  };

  // Remove plugin
  const removePlugin = name => {
    setError("");
    setSuccess("");
    fetch(`/plugins/${name}/remove`, { method: "POST" })
      .then(res => res.json())
      .then(data => setSuccess(data.message))
      .catch(() => setError("Failed to remove plugin."));
  };

  // Update plugin (stub/demo)
  const updatePlugin = name => {
    setError("");
    setSuccess("");
    // For demo, just send a dummy update
    fetch(`/plugins/${name}/update`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        description: "Updated plugin",
        code: "// updated code",
        author: "system"
      })
    })
      .then(res => res.json())
      .then(data => setSuccess(data.message))
      .catch(() => setError("Failed to update plugin."));
  };

  // Save plugin config (stub/demo)
  const savePluginConfig = name => {
    setSuccess("Config saved for " + name);
    setConfigModal({ open: false, plugin: null });
    // TODO: Send config to backend if needed
  };

  return (
    <div style={{ border: "1px solid #aaa", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
      <h2>Plugin Marketplace</h2>
      <div style={{ marginBottom: "1rem", color: "#555" }}>
        <b>Need help?</b> See the <a href="/QUICKSTART.md" target="_blank" rel="noopener noreferrer">Quickstart Guide</a> for plugin setup and troubleshooting.
        <br />
        Only supported plugins (weather, calendar, etc.) are available. Legacy plugins are not included.
      </div>
      {/* Add New Backend/Plugin Button */}
      <div style={{ marginBottom: "1rem", background: "#f9f9f9", border: "1px solid #ccc", padding: "1rem", borderRadius: "6px" }}>
        <strong>Add New Backend/Plugin:</strong>
        <button
          style={{
            background: "#eaffea",
            color: "#0a0",
            border: "none",
            borderRadius: "6px",
            padding: "0.5rem 1rem",
            cursor: "pointer",
            marginRight: "1rem"
          }}
          onClick={() => window.open("https://github.com/harleysmodernlife/VERN/blob/main/AGENT_GUIDES/PLUGIN_REGISTRY.md", "_blank")}
        >
          Contributor Guide
        </button>
        <span style={{ marginLeft: "1rem", color: "#888" }}>
          Register new backends/models/APIs via config or plugin registry. See docs for extension patterns.
        </span>
      </div>
      {error && <div style={{ color: "red", marginBottom: "1rem" }}>Error: {error}</div>}
      {success && <div style={{ color: "green", marginBottom: "1rem" }}>{success}</div>}
      <div>
        {plugins.length === 0 ? (
          <div>No plugins found.</div>
        ) : (
          <div style={{ display: "flex", flexWrap: "wrap", gap: "2rem" }}>
            {plugins.map(plugin => (
              <div
                key={plugin.name}
                style={{
                  border: "1px solid #ccc",
                  borderRadius: "12px",
                  padding: "1.5rem",
                  width: "320px",
                  boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "flex-start",
                  background: plugin.enabled ? "#f8fff8" : "#fff8f8"
                }}
              >
                <div style={{ display: "flex", alignItems: "center", marginBottom: "0.5rem" }}>
                  <span
                    style={{
                      display: "inline-block",
                      width: "32px",
                      height: "32px",
                      background: "#eee",
                      borderRadius: "50%",
                      marginRight: "1rem"
                    }}
                  >
                    {/* Placeholder for plugin icon */}
                    <span style={{ fontSize: "1.5rem", color: "#888" }}>🔌</span>
                  </span>
                  <strong style={{ fontSize: "1.2rem" }}>{plugin.name}</strong>
                </div>
                <div style={{ marginBottom: "0.5rem", color: "#555" }}>{plugin.description}</div>
                <div style={{ marginBottom: "0.5rem" }}>
                  <span
                    style={{
                      padding: "0.25rem 0.75rem",
                      borderRadius: "8px",
                      background: plugin.enabled ? "#d4ffd4" : "#ffd4d4",
                      color: plugin.enabled ? "#0a0" : "#a00",
                      fontWeight: "bold"
                    }}
                  >
                    {plugin.enabled ? "Enabled" : "Disabled"}
                  </span>
                </div>
                <div style={{ display: "flex", gap: "0.5rem" }}>
                  <button
                    onClick={() => togglePlugin(plugin.name, !plugin.enabled)}
                    style={{
                      background: plugin.enabled ? "#ffecec" : "#eaffea",
                      color: plugin.enabled ? "#a00" : "#0a0",
                      border: "none",
                      borderRadius: "6px",
                      padding: "0.5rem 1rem",
                      cursor: "pointer"
                    }}
                  >
                    {plugin.enabled ? "Disable" : "Enable"}
                  </button>
                  <button
                    onClick={() => updatePlugin(plugin.name)}
                    style={{
                      background: "#eef",
                      color: "#00a",
                      border: "none",
                      borderRadius: "6px",
                      padding: "0.5rem 1rem",
                      cursor: "pointer"
                    }}
                  >
                    Update
                  </button>
                  <button
                    onClick={() => removePlugin(plugin.name)}
                    style={{
                      background: "#fee",
                      color: "#a00",
                      border: "none",
                      borderRadius: "6px",
                      padding: "0.5rem 1rem",
                      cursor: "pointer"
                    }}
                  >
                    Remove
                  </button>
                  <button
                    onClick={() => setConfigModal({ open: true, plugin })}
                    style={{
                      background: "#ffd",
                      color: "#a60",
                      border: "none",
                      borderRadius: "6px",
                      padding: "0.5rem 1rem",
                      cursor: "pointer"
                    }}
                  >
                    Config
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
        {configModal.open && (
          <div
            style={{
              position: "fixed",
              top: 0,
              left: 0,
              width: "100vw",
              height: "100vh",
              background: "rgba(0,0,0,0.3)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              zIndex: 1000
            }}
            onClick={() => setConfigModal({ open: false, plugin: null })}
          >
            <div
              style={{
                background: "#fff",
                borderRadius: "12px",
                padding: "2rem",
                minWidth: "340px",
                boxShadow: "0 2px 16px rgba(0,0,0,0.15)",
                position: "relative"
              }}
              onClick={e => e.stopPropagation()}
            >
              <h3>Configure {configModal.plugin.name}</h3>
              {/* Example config fields, replace with real plugin config */}
              <div style={{ marginBottom: "1rem" }}>
                <label style={{ marginRight: "0.5rem" }}>API Key:</label>
                <input
                  type="text"
                  value={pluginConfigs[configModal.plugin.name]?.apiKey || ""}
                  onChange={e =>
                    setPluginConfigs(prev => ({
                      ...prev,
                      [configModal.plugin.name]: {
                        ...prev[configModal.plugin.name],
                        apiKey: e.target.value
                      }
                    }))
                  }
                  style={{ width: "220px" }}
                />
              </div>
              <button
                onClick={() => savePluginConfig(configModal.plugin.name)}
                style={{
                  background: "#eaffea",
                  color: "#0a0",
                  border: "none",
                  borderRadius: "6px",
                  padding: "0.5rem 1rem",
                  cursor: "pointer",
                  marginRight: "1rem"
                }}
              >
                Save
              </button>
              <button
                onClick={() => setConfigModal({ open: false, plugin: null })}
                style={{
                  background: "#fee",
                  color: "#a00",
                  border: "none",
                  borderRadius: "6px",
                  padding: "0.5rem 1rem",
                  cursor: "pointer"
                }}
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
