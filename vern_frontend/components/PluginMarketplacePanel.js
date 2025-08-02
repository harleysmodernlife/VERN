// vern_frontend/components/PluginMarketplacePanel.js
import React, { useState, useEffect } from "react";

export default function PluginMarketplacePanel() {
  const [plugins, setPlugins] = useState([]);
  const [form, setForm] = useState({ name: "", description: "", code: "", author: "" });
  const [message, setMessage] = useState("");

  async function fetchSubmissions() {
    // Placeholder: would fetch from backend in production
    setPlugins([]);
  }

  async function submitPlugin(e) {
    e.preventDefault();
    setMessage("");
    try {
      const res = await fetch("http://localhost:8000/plugins/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      setMessage(data.message || "Submission sent.");
      setForm({ name: "", description: "", code: "", author: "" });
      fetchSubmissions();
    } catch (err) {
      setMessage("Error submitting plugin.");
    }
  }

  useEffect(() => {
    fetchSubmissions();
  }, []);

  return (
    <div style={{ border: "1px solid #a0a", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
      <h3>Plugin Marketplace</h3>
      <form onSubmit={submitPlugin} style={{ marginBottom: "2rem" }}>
        <label>
          Name:
          <input type="text" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} required style={{ marginLeft: "0.5rem" }} />
        </label>
        <br />
        <label>
          Description:
          <input type="text" value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} required style={{ marginLeft: "0.5rem" }} />
        </label>
        <br />
        <label>
          Author:
          <input type="text" value={form.author} onChange={e => setForm({ ...form, author: e.target.value })} required style={{ marginLeft: "0.5rem" }} />
        </label>
        <br />
        <label>
          Code:
          <textarea value={form.code} onChange={e => setForm({ ...form, code: e.target.value })} required rows={6} style={{ width: "100%", marginTop: "0.5rem" }} />
        </label>
        <br />
        <button type="submit" style={{ marginTop: "1rem" }}>Submit Plugin</button>
      </form>
      {message && <div style={{ color: message.startsWith("Error") ? "red" : "green" }}>{message}</div>}
      <h4>Pending Submissions</h4>
      <ul>
        {plugins.length === 0 ? <li>No submissions yet.</li> : plugins.map((p, idx) => (
          <li key={idx}><b>{p.name}</b> by {p.author}: {p.description}</li>
        ))}
      </ul>
    </div>
  );
}
