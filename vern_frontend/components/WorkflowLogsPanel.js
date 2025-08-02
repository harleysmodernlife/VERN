// vern_frontend/components/WorkflowLogsPanel.js
import React, { useEffect, useState } from "react";

export default function WorkflowLogsPanel() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch("http://localhost:8000/agents/workflows/logs")
      .then(res => res.json())
      .then(data => {
        setLogs(data);
        setLoading(false);
      })
      .catch(() => {
        setLogs([]);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ border: "1px solid #09c", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
      <h3>Workflow Logs</h3>
      {loading ? <p>Loading workflow logs...</p> : (
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Workflow</th>
              <th>Steps</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr><td colSpan={4}>No logs available.</td></tr>
            ) : logs.map((log, idx) => (
              <tr key={idx}>
                <td>{log.timestamp}</td>
                <td>{log.workflow}</td>
                <td>{log.steps.join(" → ")}</td>
                <td>{log.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
