import React, { useState, useEffect } from "react";

export default function WorkflowEditorPanel() {
  // TODO: Add workflow import/export functionality
  // TODO: Add workflow validation and analytics
  // TODO: Improve error handling and UX for CRUD operations
  // TODO: Document backend endpoints for workflow CRUD

  const [workflows, setWorkflows] = useState({});
  const [workflowName, setWorkflowName] = useState("");
  const [steps, setSteps] = useState([{ agent: "", model: "", input: "", persona: "default", context: "" }]);
  const [runResult, setRunResult] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [resourceStatus, setResourceStatus] = useState({ cpu: "normal", ram: "normal" });

  // New: agent/model lists
  const [agents, setAgents] = useState([]);
  const [models, setModels] = useState([]);
  const [agentFetchError, setAgentFetchError] = useState("");
  const [modelFetchError, setModelFetchError] = useState("");

  // Fetch workflows
  useEffect(() => {
    fetch("/agents/workflows/list")
      .then(res => res.json())
      .then(data => setWorkflows(data))
      .catch(() => setWorkflows({}));
  }, [success]);

  // Fetch agents
  useEffect(() => {
    fetch("/agents/status")
      .then(res => res.json())
      .then(data => {
        setAgents(data.map(a => a.name));
        // Try to extract models from capabilities/meta
        const allModels = [];
        data.forEach(a => {
          if (Array.isArray(a.capabilities)) {
            a.capabilities.forEach(m => {
              if (typeof m === "string" && !allModels.includes(m)) allModels.push(m);
            });
          }
          if (a.meta && Array.isArray(a.meta.models)) {
            a.meta.models.forEach(m => {
              if (typeof m === "string" && !allModels.includes(m)) allModels.push(m);
            });
          }
        });
        setModels(allModels);
        setAgentFetchError("");
        setModelFetchError("");
      })
      .catch(() => {
        setAgents([]);
        setModels([]);
        setAgentFetchError("Failed to fetch agents.");
        setModelFetchError("Failed to fetch models.");
      });
  }, []);

  // Add step
  const addStep = () => {
    setSteps([...steps, { agent: "", model: "", input: "", persona: "default", context: "" }]);
  };

  // Update step
  const updateStep = (idx, field, value) => {
    const newSteps = steps.map((step, i) =>
      i === idx ? { ...step, [field]: value } : step
    );
    setSteps(newSteps);
  };

  // Fetch resource status (stub/demo)
  useEffect(() => {
    fetch("/system/status")
      .then(res => res.json())
      .then(data => setResourceStatus(data))
      .catch(() => setResourceStatus({ cpu: "normal", ram: "normal" }));
  }, []);

  // Create workflow
  const createWorkflow = async () => {
    setError("");
    setSuccess("");
    try {
      const res = await fetch("/agents/workflows/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: workflowName, steps })
      });
      const data = await res.json();
      if (data.error) {
        setSuccess("");
        setError(data.error);
        return;
      }
      setSuccess(data.result);
      setWorkflowName("");
      setSteps([{ agent: "", model: "", input: "" }]);
    } catch (err) {
      setSuccess("");
      setError("Failed to create workflow.");
      // eslint-disable-next-line no-console
      console.log("DEBUG: Error caught in createWorkflow", err);
    }
  };

  // Run workflow
  const runWorkflow = name => {
    setError("");
    setRunResult(null);
    fetch("/agents/workflows/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name })
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          setError(data.error);
          setRunResult(null);
        } else {
          setRunResult(data.result);
        }
      })
      .catch(() => setError("Failed to run workflow."));
  };

  return (
    <div style={{ border: "1px solid #aaa", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
      <h2>Workflow Editor</h2>
      <div style={{ marginBottom: "1rem", color: "#555" }}>
        <b>Need help?</b> See the <a href="/QUICKSTART.md" target="_blank" rel="noopener noreferrer">Quickstart Guide</a> for workflow instructions.
      </div>
      {error
        ? <div style={{ color: "red", marginBottom: "1rem" }}>Error: {error}</div>
        : success && <div style={{ color: "green", marginBottom: "1rem" }}>{success}</div>
      }
      {agentFetchError && <div style={{ color: "red", marginBottom: "1rem" }}>Agent Error: {agentFetchError}</div>}
      {modelFetchError && <div style={{ color: "red", marginBottom: "1rem" }}>Model Error: {modelFetchError}</div>}
      <div>
        <h3>Create Workflow</h3>
        <input
          type="text"
          placeholder="Workflow Name"
          value={workflowName}
          onChange={e => setWorkflowName(e.target.value)}
          style={{ marginBottom: "1rem", width: "200px" }}
        />
        {/* Resource Monitoring Bar */}
        <div style={{ marginBottom: "1rem", padding: "0.5rem", background: "#f6f6ff", borderRadius: "8px", border: "1px solid #ddd" }}>
          <strong>Resource Status:</strong> CPU: {resourceStatus.cpu}, RAM: {resourceStatus.ram}
        </div>
        {/* Visual Canvas for Drag-and-Drop Steps */}
        <div
          style={{
            border: "2px dashed #bbb",
            borderRadius: "12px",
            minHeight: "180px",
            marginBottom: "1rem",
            padding: "1rem",
            background: "#f9f9f9",
            position: "relative"
          }}
        >
          <h4>Workflow Canvas (Drag steps to reorder, links are visual only)</h4>
          {steps.map((step, idx) => (
            <div
              key={idx}
              draggable
              onDragStart={e => {
                e.dataTransfer.setData("stepIdx", idx);
              }}
              onDrop={e => {
                const fromIdx = Number(e.dataTransfer.getData("stepIdx"));
                if (fromIdx !== idx) {
                  const reordered = [...steps];
                  const [moved] = reordered.splice(fromIdx, 1);
                  reordered.splice(idx, 0, moved);
                  setSteps(reordered);
                }
              }}
              onDragOver={e => e.preventDefault()}
              style={{
                marginBottom: "0.5rem",
                padding: "0.5rem",
                background: "#fff",
                border: "1px solid #ddd",
                borderRadius: "8px",
                cursor: "grab",
                position: "relative"
              }}
            >
              {/* Agent dropdown */}
              <select
                value={step.agent}
                onChange={e => updateStep(idx, "agent", e.target.value)}
                style={{ marginRight: "0.5rem", width: "180px" }}
                aria-label="Agent selection"
              >
                <option value="">Select Agent</option>
                {agents.map(agent => (
                  <option key={agent} value={agent}>{agent}</option>
                ))}
              </select>
              {/* Model dropdown (if available) */}
              {models.length > 0 ? (
                <select
                  value={step.model}
                  onChange={e => updateStep(idx, "model", e.target.value)}
                  style={{ marginRight: "0.5rem", width: "180px" }}
                  aria-label="Model selection"
                >
                  <option value="">Select Model</option>
                  {models.map(model => (
                    <option key={model} value={model}>{model}</option>
                  ))}
                </select>
              ) : (
                <input
                  type="text"
                  placeholder="Model (optional)"
                  value={step.model}
                  onChange={e => updateStep(idx, "model", e.target.value)}
                  style={{ marginRight: "0.5rem", width: "180px" }}
                  aria-label="Model input"
                />
              )}
              <input
                type="text"
                placeholder="Input"
                value={step.input}
                onChange={e => updateStep(idx, "input", e.target.value)}
                style={{ width: "180px" }}
              />
              {/* Persona/context tuning */}
              <select
                value={step.persona}
                onChange={e => updateStep(idx, "persona", e.target.value)}
                style={{ marginLeft: "0.5rem", width: "140px" }}
                aria-label="Persona tuning"
              >
                <option value="default">Default</option>
                <option value="coach">Health Coach</option>
                <option value="medic">Medical Assistant</option>
                <option value="mindfulness">Mindfulness Guide</option>
                <option value="advisor">Advisor</option>
              </select>
              <input
                type="text"
                placeholder="Context (optional)"
                value={step.context}
                onChange={e => updateStep(idx, "context", e.target.value)}
                style={{ marginLeft: "0.5rem", width: "180px" }}
                aria-label="Context tuning"
              />
              {/* Visual arrow to next step */}
              {idx < steps.length - 1 && (
                <div
                  style={{
                    position: "absolute",
                    right: "-30px",
                    top: "50%",
                    transform: "translateY(-50%)",
                    fontSize: "2rem",
                    color: "#bbb"
                  }}
                >
                  →
                </div>
              )}
              {/* Live preview */}
              <div style={{ marginTop: "0.5rem", fontSize: "0.95rem", color: "#888" }}>
                <em>Preview:</em>{" "}
                {step.agent && step.input
                  ? `Would run agent "${step.agent}"${step.model ? ` (model "${step.model}")` : ""} with input "${step.input}", persona "${step.persona}", context "${step.context}"`
                  : "Fill in agent and input"}
              </div>
            </div>
          ))}
        </div>
        <button onClick={addStep} style={{ marginRight: "1rem" }}>Add Step</button>
        <button onClick={async () => await createWorkflow()}>Create Workflow</button>
      </div>
      <div style={{ marginTop: "2rem" }}>
        <h3>Available Workflows</h3>
        {Object.keys(workflows).length === 0 ? (
          <div>No workflows found.</div>
        ) : (
          <ul>
            {Object.entries(workflows).map(([name, steps]) => (
              <li key={name} style={{ marginBottom: "1rem" }}>
                <strong>{name}</strong>
                <ul>
                  {steps.map((step, idx) => (
                    <li key={idx}>
                      Agent: {step.agent}{step.model ? ` (Model: ${step.model})` : ""}, Input: {step.input}
                    </li>
                  ))}
                </ul>
                <button onClick={() => runWorkflow(name)}>Run Workflow</button>
              </li>
            ))}
          </ul>
        )}
      </div>
      {runResult && (
        <div style={{ marginTop: "2rem", borderTop: "1px solid #ddd", paddingTop: "1rem" }}>
          <h3>Workflow Run Result</h3>
          <pre>{JSON.stringify(runResult, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
