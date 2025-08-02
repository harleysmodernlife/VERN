import Head from 'next/head';
import Dashboard from '../components/Dashboard';
import OrchestratorPanel from '../components/OrchestratorPanel';
import PluginRegistryPanel from '../components/PluginRegistryPanel';
import UserProfilePanel from '../components/UserProfilePanel';
import AgentClusterViz from '../components/AgentClusterViz';
import OnboardingPanel from '../components/OnboardingPanel';
import PluginMarketplacePanel from '../components/PluginMarketplacePanel';
import WorkflowLogsPanel from '../components/WorkflowLogsPanel';
import WorkflowEditorPanel from '../components/WorkflowEditorPanel';

export default function Home() {
  return (
    <>
      <Head>
        <title>VERN Dashboard</title>
        <meta name="description" content="VERN - Modular AI OS Dashboard" />
      </Head>
      <main style={{ padding: "2rem" }}>
        <h1>VERN - Modular AI OS Dashboard</h1>
        <p>
          Welcome to the bleeding-edge VERN frontend!<br />
          This Next.js app will become the modular dashboard, plugin marketplace, agent/cluster visualizer, and more.
        </p>
        <Dashboard />
        <OrchestratorPanel />
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
