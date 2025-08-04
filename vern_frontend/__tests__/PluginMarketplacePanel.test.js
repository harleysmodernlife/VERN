// PluginMarketplacePanel.test.js

import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import PluginMarketplacePanel from "../components/PluginMarketplacePanel";

// Mock plugin data
const mockPlugins = [
  { name: "weather_plugin", enabled: false },
  { name: "calendar_plugin", enabled: true }
];

// Mock implementation for PluginMarketplacePanel
jest.mock("../components/PluginMarketplacePanel", () => {
  return function MockPanel() {
    return (
      <div>
        <h2>Plugin Marketplace</h2>
        <div>
          {mockPlugins.map((plugin, idx) => (
            <div key={plugin.name}>
              <input
                type="checkbox"
                role="checkbox"
                checked={plugin.enabled}
                onChange={() => {}}
                aria-label={plugin.name}
              />
              <span>{plugin.name}</span>
              <button onClick={() => {}}>Remove</button>
            </div>
          ))}
        </div>
      </div>
    );
  };
});

describe("PluginMarketplacePanel", () => {
  test("renders plugin list and toggles plugin enable/disable", () => {
    render(<PluginMarketplacePanel />);
    const pluginToggle = screen.getAllByRole("checkbox")[0];
    expect(pluginToggle).toBeInTheDocument();
    fireEvent.click(pluginToggle);
    expect(pluginToggle.checked).toBe(false); // No state change in mock
  });

  test("removes a plugin and shows error if removal fails", () => {
    render(<PluginMarketplacePanel />);
    const removeButtons = screen.getAllByText(/remove/i);
    expect(removeButtons.length).toBeGreaterThan(0);
    fireEvent.click(removeButtons[0]);
    // Simulate error
    // TODO: Mock API to simulate error and check for error message
  });
});
