/**
 * Dashboard AgentClusterStatus fetch tests
 * - Uses jsdom environment and fetch mocking
 */
import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";

jest.mock("../lib/apiBase", () => ({
  getApiBase: () => "http://test-backend:8000",
  joinApi: (path) => "http://test-backend:8000" + path,
}));

jest.mock("../components/ConfigEditorPanel", () => () => <div>ConfigEditorPanel</div>);
jest.mock("../components/WorkflowEditorPanel", () => () => <div>WorkflowEditorPanel</div>);
jest.mock("../components/PluginMarketplacePanel", () => () => <div>PluginMarketplacePanel</div>);
jest.mock("../components/HelpPanel", () => () => <div>HelpPanel</div>);
jest.mock("../components/OnboardingPanel", () => () => <div>OnboardingPanel</div>);
jest.mock("../components/IntegrationManagerPanel", () => () => <div>IntegrationManagerPanel</div>);

// Import the component after mocks so it picks up the mocked getApiBase
import Dashboard from "../components/Dashboard";

describe("Dashboard AgentClusterStatus fetch", () => {
  beforeEach(() => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => [
        { name: "research", cluster: "Research", status: "online" },
        { name: "orchestrator", cluster: "Orchestrator", status: "online" },
      ],
    });
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  test("renders cluster items from API", async () => {
    render(<Dashboard />);
    // Expect loading state first
    expect(screen.getByText(/Loading agent\/cluster status/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /Agent\/Cluster Status/i })).toBeInTheDocument();
    });

    // Items rendered
    const listItems = screen.getAllByRole('listitem');
    expect(listItems[0]).toHaveTextContent('research (Research) - online');
    expect(listItems[1]).toHaveTextContent('orchestrator (Orchestrator) - online');

    // Called correct URL (with getApiBase())
    expect(global.fetch).toHaveBeenCalledWith("http://test-backend:8000/agents/status");
  });
});