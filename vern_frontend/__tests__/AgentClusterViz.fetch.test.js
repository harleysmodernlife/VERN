/**
 * AgentClusterViz LiveClusterStatus fetch tests
 * - Uses jsdom environment and fetch mocking
 */
import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";

jest.mock("../lib/apiBase", () => ({
  getApiBase: () => "http://test-backend:8000",
  joinApi: (path) => "http://test-backend:8000" + path,
}));

// Import component after mocks
import AgentClusterViz from "../components/AgentClusterViz";

describe("AgentClusterViz LiveClusterStatus fetch", () => {
  beforeEach(() => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => [
        { name: "research", cluster: "Research", status: "online" },
        { name: "finance", cluster: "Finance", status: "stale" },
      ],
    });
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  test("renders list from API and calls getApiBase()", async () => {
    render(<AgentClusterViz />);
    // loading
    expect(screen.getByText(/Loading cluster status/i)).toBeInTheDocument();

    // items rendered
    const listItems = await screen.findAllByRole('listitem');
    expect(listItems[0]).toHaveTextContent('research (Research) - online');
    expect(listItems[1]).toHaveTextContent('finance (Finance) - stale');

    // verify API base usage
    expect(global.fetch).toHaveBeenCalledWith("http://test-backend:8000/agents/status");
  });
});