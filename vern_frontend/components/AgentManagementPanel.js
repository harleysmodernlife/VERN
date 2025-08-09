// vern_frontend/components/AgentManagementPanel.js
import React, { useState, useEffect } from "react";

/**
 * Agent Management Panel
 * Integration point: Connect to agent registry API for CRUD operations.
 */
export default function AgentManagementPanel() {
  const [agents, setAgents] = useState([]);
  const [statusMap, setStatusMap] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [newAgent, setNewAgent] = useState({ name: "", cluster: "" });
  const [editIdx, setEditIdx] = useState(-1);
  const [editAgent, setEditAgent] = useState({});
  const [clusters, setClusters] = useState([]);
  const [refreshFlag, setRefreshFlag] = useState(false);

  // Fetch agents
  useEffect(() => {
    setLoading(true);
    setError("");
    fetch("/registry/")
      .then(res => res.json())
      .then(data => {
        setAgents(data.agents || []);
        // Collect clusters from agents
        const uniqueClusters = Array.from(new Set((data.agents || []).map(a => a.cluster).filter(Boolean)));
        setClusters(uniqueClusters);
      })
      .catch(() => setError("Failed to load agents."))
      .finally(() => setLoading(false));
  }, [refreshFlag]);

  // Fetch live status
  useEffect(() => {
    fetch("/agents/status")
      .then(res => res.json())
      .then(data => setStatusMap(data.status || {}))
      .catch(() => setStatusMap({}));
  }, [agents]);

  // Add agent
  const handleAddAgent = () => {
    setLoading(true);
    setError("");
    setSuccess("");
    fetch("/registry/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newAgent)
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to add agent.");
        return res.json();
      })
      .then(() => {
        setSuccess("Agent added.");
        setNewAgent({ name: "", cluster: "" });
        setRefreshFlag(f => !f);
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  };

  // Edit agent
  const handleEditAgent = idx => {
    setEditIdx(idx);
    setEditAgent({ ...agents[idx] });
  };

  const handleSaveEdit = () => {
    setLoading(true);
    setError("");
    setSuccess("");
    fetch("/registry/", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(editAgent)
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to update agent.");
        return res.json();
      })
      .then(() => {
        setSuccess("Agent updated.");
        setEditIdx(-1);
        setEditAgent({});
        setRefreshFlag(f => !f);
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  };

  // Delete agent
  const handleDeleteAgent = name => {
    setLoading(true);
    setError("");
    setSuccess("");
    fetch(`/agents/${encodeURIComponent(name)}`, {
      method: "DELETE"
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to delete agent.");
        return res.json();
      })
      .then(() => {
        setSuccess("Agent deleted.");
        setRefreshFlag(f => !f);
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  };

  // Assign cluster
  const handleClusterChange = (idx, cluster) => {
    const agent = { ...agents[idx], cluster };
    setLoading(true);
    setError("");
    setSuccess("");
    fetch("/registry/", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(agent)
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to assign cluster.");
        return res.json();
      })
      .then(() => {
        setSuccess("Cluster assigned.");
        setRefreshFlag(f => !f);
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  };

  return (
    <div style={{ border: "1px solid #333", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
      <h3>Agent Management</h3>
      <p>Manage agents, clusters, and assignments here.</p>
      {error && <div style={{ color: "red", marginBottom: "1rem" }}>Error: {error}</div>}
      {success && <div style={{ color: "green", marginBottom: "1rem" }}>{success}</div>}
      <div style={{ marginBottom: "2rem", borderBottom: "1px solid #ccc", paddingBottom: "1rem" }}>
        <h4>Add Agent</h4>
        <input
          type="text"
          placeholder="Agent Name"
          value={newAgent.name}
          onChange={e => setNewAgent(a => ({ ...a, name: e.target.value }))}
          style={{ marginRight: "1rem" }}
        />
        <input
          type="text"
          placeholder="Cluster"
          value={newAgent.cluster}
          onChange={e => setNewAgent(a => ({ ...a, cluster: e.target.value }))}
          style={{ marginRight: "1rem" }}
        />
        <button onClick={handleAddAgent} disabled={loading || !newAgent.name}>Add</button>
      </div>
      <h4>Agents</h4>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Cluster</th>
              <th>Status</th>
              <th>Last Seen</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {agents.map((agent, idx) =>
              editIdx === idx ? (
                <tr key={agent.name} style={{ background: "#eef" }}>
                  <td>
                    <input
                      type="text"
                      value={editAgent.name}
                      onChange={e => setEditAgent(a => ({ ...a, name: e.target.value }))}
                    />
                  </td>
                  <td>
                    <select
                      value={editAgent.cluster || ""}
                      onChange={e => setEditAgent(a => ({ ...a, cluster: e.target.value }))}
                    >
                      <option value="">Unassigned</option>
                      {clusters.map(c => (
                        <option key={c} value={c}>{c}</option>
                      ))}
                    </select>
                  </td>
                  <td>{statusMap[agent.name]?.status || "unknown"}</td>
                  <td>{statusMap[agent.name]?.last_seen || "N/A"}</td>
                  <td>
                    <button onClick={handleSaveEdit} disabled={loading}>Save</button>
                    <button onClick={() => setEditIdx(-1)} disabled={loading}>Cancel</button>
                  </td>
                </tr>
              ) : (
                <tr key={agent.name}>
                  <td>{agent.name}</td>
                  <td>
                    <select
                      value={agent.cluster || ""}
                      onChange={e => handleClusterChange(idx, e.target.value)}
                    >
                      <option value="">Unassigned</option>
                      {clusters.map(c => (
                        <option key={c} value={c}>{c}</option>
                      ))}
                    </select>
                  </td>
                  <td>{statusMap[agent.name]?.status || "unknown"}</td>
                  <td>{statusMap[agent.name]?.last_seen || "N/A"}</td>
                  <td>
                    <button onClick={() => handleEditAgent(idx)} disabled={loading}>Edit</button>
                    <button onClick={() => handleDeleteAgent(agent.name)} disabled={loading}>Delete</button>
                  </td>
                </tr>
              )
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}