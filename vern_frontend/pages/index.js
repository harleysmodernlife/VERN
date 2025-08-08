import React from 'react';
import dynamic from 'next/dynamic';
import Head from 'next/head';

// Force client-side rendering for the entire page to ensure dynamic sections show up
export const config = {
  unstable_runtimeJS: true
};

// Dynamically import components that use browser-only APIs to avoid SSR/export omissions
const OrchestratorPanel = dynamic(() => import('../components/OrchestratorPanel'), { ssr: false });
const Dashboard = dynamic(() => import('../components/Dashboard'), { ssr: false });
const PluginRegistryPanel = dynamic(() => import('../components/PluginRegistryPanel'), { ssr: false });
const UserProfilePanel = dynamic(() => import('../components/UserProfilePanel'), { ssr: false });
const AgentClusterViz = dynamic(() => import('../components/AgentClusterViz'), { ssr: false });
const OnboardingPanel = dynamic(() => import('../components/OnboardingPanel'), { ssr: false });
const PluginMarketplacePanel = dynamic(() => import('../components/PluginMarketplacePanel'), { ssr: false });
const WorkflowLogsPanel = dynamic(() => import('../components/WorkflowLogsPanel'), { ssr: false });
const WorkflowEditorPanel = dynamic(() => import('../components/WorkflowEditorPanel'), { ssr: false });

export default function Home() {
  return (
    <>
      <Head>
        <title>VERN Dashboard</title>
        <meta name="description" content="VERN - Modular AI OS Dashboard" />
      </Head>
      <main style={{ padding: "2rem" }}>
        <h1>VERN - Modular AI OS Dashboard</h1>

        {/* Prominent Orchestrator Test Panel header and placement */}
        <section
          style={{
            marginTop: "1rem",
            padding: "1rem",
            border: "2px solid #0070f3",
            borderRadius: "10px",
            background: "#f0f7ff"
          }}
          aria-label="Orchestrator Test Panel Section"
        >
          <h2 style={{ marginTop: 0, marginBottom: "0.5rem" }}>Orchestrator Test Panel</h2>
          <p style={{ marginTop: 0, color: "#333" }}>
            Type a prompt below and press Send. After a response appears, use 👍 or 👎 to give quick feedback.
          </p>
          {/* Render a client-only placeholder to make presence obvious even before hydration */}
          <div style={{ marginBottom: "0.5rem", color: "#555" }}>
            If you don't see the input box below, try a hard refresh (Ctrl+Shift+R).
          </div>
          <OrchestratorPanel />
        </section>

        <p style={{ marginTop: "2rem" }}>
          Welcome to the bleeding-edge VERN frontend!<br />
          This Next.js app will become the modular dashboard, plugin marketplace, agent/cluster visualizer, and more.
        </p>

        {/* Keep the rest of the panels below the orchestrator section */}
        <Dashboard />
        <PluginRegistryPanel />
        <UserProfilePanel />
        <AgentClusterViz />
        <OnboardingPanel />
        <PluginMarketplacePanel />
        <WorkflowLogsPanel />
        <WorkflowEditorPanel />
        <ul>
          <li>Modular dashboard with sidebar/topbar navigation</li>
          <li>Real-time agent/cluster status and workflow visualization</li>
          <li>Plugin management and marketplace</li>
          <li>Workflow logs, onboarding, user settings, and more</li>
          <li>Turbo workflow editor: build, save, and run multi-agent workflows</li>
        </ul>
        <p>
          <b>Backend API:</b> <code>http://localhost:8000</code>
        </p>
      </main>
    </>
  );
}
