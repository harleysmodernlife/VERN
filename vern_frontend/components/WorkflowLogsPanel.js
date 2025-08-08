// vern_frontend/components/WorkflowLogsPanel.js
import React, { useEffect, useState } from "react";

export default function WorkflowLogsPanel() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  // Privacy audit log state
  const [showPrivacyLog, setShowPrivacyLog] = useState(false);
  const [privacyAuditLog, setPrivacyAuditLog] = useState([]);
  const [privacyLoading, setPrivacyLoading] = useState(false);

  async function fetchPrivacyAuditLog() {
    setPrivacyLoading(true);
    try {
      const res = await fetch("http://localhost:8000/privacy/audit/log");
      if (res.ok) {
        const data = await res.json();
        setPrivacyAuditLog(data);
      } else {
        setPrivacyAuditLog([]);
      }
    } catch {
      setPrivacyAuditLog([]);
    }
    setPrivacyLoading(false);
  }

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
      <div style={{ marginBottom: "1rem" }}>
        <button
          onClick={() => setShowPrivacyLog(false)}
          disabled={!showPrivacyLog}
          style={{ marginRight: "1rem" }}
        >
          Workflow Logs
        </button>
        <button
          onClick={() => {
            setShowPrivacyLog(true);
            fetchPrivacyAuditLog();
          }}
          disabled={showPrivacyLog}
        >
          Privacy Audit Trail
        </button>
      </div>
      {!showPrivacyLog ? (
        <>
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
        </>
      ) : (
        <>
          <h3>Privacy Audit Trail</h3>
          {privacyLoading ? <p>Loading privacy audit log...</p> : (
            <table>
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Action</th>
                  <th>Allowed</th>
                  <th>User</th>
                  <th>Reason</th>
                </tr>
              </thead>
              <tbody>
                {privacyAuditLog.length === 0 ? (
                  <tr><td colSpan={5}>No privacy decisions recorded.</td></tr>
                ) : privacyAuditLog.map((entry, idx) => (
                  <tr key={idx}>
                    <td>{new Date(entry.decided_at * 1000).toLocaleString()}</td>
                    <td>{entry.action}</td>
                    <td>{entry.allowed ? "✅" : "❌"}</td>
                    <td>{entry.user_id || "?"}</td>
                    <td>{entry.reason}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}
    </div>
  );
}
