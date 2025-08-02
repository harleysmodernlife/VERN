// vern_frontend/components/WorkflowEditorPanel.js
import React, { useState } from "react";

// Demo agent/plugin list (replace with live backend data)
const AGENTS = [
  "dev_team", "research", "health", "finance", "admin", "creativity", "career", "social",
  "environment", "legal", "travel", "security", "archetype", "emergent", "id10t_monitor"
];
const PLUGINS = ["weather", "calendar", "fileops", "chromadb"];

export default function WorkflowEditorPanel() {
  // Add a "context" property to each agent step to hold per-step context info.
  const [steps, setSteps] = useState([]);
  const [newStep, setNewStep] = useState({
    type: "agent",
    name: AGENTS[0],
    persona: "default",
    context: "" // new field for per-step context
  });
  const [workflowName, setWorkflowName] = useState("");
  const [savedWorkflows, setSavedWorkflows] = useState([]);
  const [executing, setExecuting] = useState(false);
  const [output, setOutput] = useState("");

  function addStep() {
    setSteps([...steps, { ...newStep }]);
  }

  function removeStep(idx) {
    setSteps(steps.filter((_, i) => i !== idx));
  }

  function saveWorkflow() {
    if (!workflowName) return;
    setSavedWorkflows([...savedWorkflows, { name: workflowName, steps }]);
    setWorkflowName("");
    setSteps([]);
  }

  async function executeWorkflow() {
    setExecuting(true);
    setOutput("");
    // Prepare workflow payload including per-step context
    const workflowPayload = steps.map(s => ({
      type: s.type,
      name: s.name,
      persona: s.type === "agent" ? s.persona : undefined,
      context: s.context // include per-step context (may be blank)
    }));
    try {
      const res = await fetch("http://localhost:8000/agents/orchestrator/respond", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_input: "Run workflow: " + workflowPayload.map(s => s.name).join(" → "),
          context: { workflow: workflowPayload },
          agent_status: "All agents online",
          user_id: "default_user",
          verbose: true
        })
      });
      const data = await res.json();
      setOutput(data.response || JSON.stringify(data));
    } catch (err) {
      setOutput("Error executing workflow.");
    }
    setExecuting(false);
  }

  return (
    <div style={{ border: "2px solid #09c", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
      <h3>Workflow Editor (Turbo Mode)</h3>
      <div style={{ marginBottom: "1rem" }}>
        <b>Add Step:</b>
        <select 
          value={newStep.type} 
          onChange={e => setNewStep({ ...newStep, type: e.target.value, context: "" })} 
          style={{ marginLeft: "0.5rem" }}
        >
          <option value="agent">Agent</option>
          <option value="plugin">Plugin</option>
        </select>
        <select
          value={newStep.name}
          onChange={e => setNewStep({ ...newStep, name: e.target.value })}
          style={{ marginLeft: "0.5rem" }}
        >
          {(newStep.type === "agent" ? AGENTS : PLUGINS).map(n => (
            <option key={n} value={n}>{n}</option>
          ))}
        </select>
        {newStep.type === "agent" && (
          <>
            <input
              type="text"
              value={newStep.persona}
              onChange={e => setNewStep({ ...newStep, persona: e.target.value })}
              placeholder="Persona (default, coach, analyst, etc.)"
              style={{ marginLeft: "0.5rem", width: "160px" }}
            />
            <input
              type="text"
              value={newStep.context}
              onChange={e => setNewStep({ ...newStep, context: e.target.value })}
              placeholder="Step context (optional)"
              style={{ marginLeft: "0.5rem", width: "200px" }}
            />
          </>
        )}
        {newStep.type === "plugin" && (
          <input
            type="text"
            value={newStep.context}
            onChange={e => setNewStep({ ...newStep, context: e.target.value })}
            placeholder="Plugin parameters (optional)"
            style={{ marginLeft: "0.5rem", width: "200px" }}
          />
        )}
        <button onClick={addStep} style={{ marginLeft: "1rem" }}>Add</button>
      </div>
      
      <div style={{ marginBottom: "1rem" }}>
        <b>Workflow Steps:</b>
        <ul>
          {steps.map((step, idx) => (
            <li key={idx}>
              <span style={{ fontWeight: "bold" }}>
                {step.type === "agent" ? "Agent" : "Plugin"}:
              </span> {step.name}
              {step.type === "agent" && (
                <span> <i>({step.persona})</i></span>
              )}
              {step.context && (
                <span> - <i>Context: {step.context}</i></span>
              )}
              <button onClick={() => removeStep(idx)} style={{ marginLeft: "1rem" }}>Remove</button>
            </li>
          ))}
        </ul>
      </div>
      
      <div style={{ marginBottom: "1rem" }}>
        <input
          type="text"
          value={workflowName}
          onChange={e => setWorkflowName(e.target.value)}
          placeholder="Workflow Name"
          style={{ marginRight: "1rem" }}
        />
        <button onClick={saveWorkflow} disabled={!workflowName || steps.length === 0}>
          Save Workflow
        </button>
      </div>
      
      <div style={{ marginBottom: "1rem" }}>
        <b>Saved Workflows:</b>
        <ul>
          {savedWorkflows.length === 0 ? <li>No saved workflows.</li> : savedWorkflows.map((wf, idx) => (
            <li key={idx}>
              <span style={{ fontWeight: "bold" }}>{wf.name}:</span> {wf.steps.map(s => s.name).join(" → ")}
              <button onClick={() => setSteps(wf.steps)} style={{ marginLeft: "1rem" }}>Load</button>
            </li>
          ))}
        </ul>
      </div>
      
      <button onClick={executeWorkflow} disabled={steps.length === 0 || executing}>
        {executing ? "Executing..." : "Run Workflow"}
      </button>
      
      <div style={{ marginTop: "2rem", background: "#eef", padding: "1rem", borderRadius: "6px", minHeight: "2rem" }}>
        <b>Output:</b>
        <div>{output}</div>
      </div>
      
      <div style={{ marginTop: "2rem", fontSize: "0.95em", color: "#666" }}>
        <b>Guided Tour:</b> Drag-and-drop is coming soon. For now, build workflows step-by-step, save, load, and run them. Try experimenting with adding context to each step for more tailored responses.
      </div>
    </div>
  );
}
