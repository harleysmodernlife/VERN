// vern_frontend/components/AgentManagementPanel.js
import React from "react";

/**
 * Agent Management Panel
 * Integration point: Connect to agent registry API for CRUD operations.
 * TODO: Add agent creation, editing, deletion, and cluster assignment.
 * TODO: Advanced: Search/filter agents, bulk actions, real-time status updates.
 */
export default function AgentManagementPanel() {
  return (
    <div style={{ border: "1px solid #333", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
      <h3>Agent Management</h3>
      <p>Manage agents, clusters, and assignments here.</p>
      {/* TODO: Implement agent CRUD UI */}
      {/* TODO: Add drag-and-drop for cluster assignment */}
      {/* TODO: Add contextual help and notifications */}
    </div>
  );
}