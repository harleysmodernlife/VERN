// vern_frontend/__tests__/WorkflowEditorPanel.test.js

import React from "react";
import { render, screen, fireEvent, act } from "@testing-library/react";
import WorkflowEditorPanel from "../components/WorkflowEditorPanel";

// Mock fetch for workflow API calls
beforeAll(() => {
  global.fetch = jest.fn((url, opts) => {
    if (url.endsWith("/agents/workflows/list")) {
      return Promise.resolve({
        json: () => Promise.resolve({ test_workflow: [{ agent: "planner", input: "Plan a trip" }] })
      });
    }
    if (url.endsWith("/agents/workflows/create")) {
      return Promise.resolve({
        json: () => Promise.resolve({ result: "Workflow created" })
      });
    }
    if (url.endsWith("/agents/workflows/run")) {
      return Promise.resolve({
        json: () => Promise.resolve({ result: { steps: ["Plan a trip"], results: ["Executed: Plan a trip"], critiques: ["Critique: Executed: Plan a trip"] } })
      });
    }
    return Promise.reject(new Error("Unknown endpoint"));
  });
});

afterAll(() => {
  global.fetch.mockRestore && global.fetch.mockRestore();
});

describe("WorkflowEditorPanel", () => {
  test("renders workflow editor and allows workflow creation", async () => {
    render(<WorkflowEditorPanel />);
    expect(screen.getByText(/Workflow Editor/i)).toBeInTheDocument();
    // Simulate adding steps
    const addStepBtn = screen.getByText(/Add Step/i);
    fireEvent.click(addStepBtn);
    // Fill in agent and input
    const agentInputs = screen.getAllByPlaceholderText(/Agent/i);
    fireEvent.change(agentInputs[0], { target: { value: "planner" } });
    const inputFields = screen.getAllByPlaceholderText(/Input/i);
    fireEvent.change(inputFields[0], { target: { value: "Plan a trip" } });
    // Create workflow
    const createBtns = screen.getAllByText(/Create Workflow/i);
    fireEvent.click(createBtns[1]); // Click the button, not the heading
    // Wait for workflow to appear in list
    try {
      expect(await screen.findByText(/test_workflow/i)).toBeInTheDocument();
    } catch (e) {
      // Print debug output
      // eslint-disable-next-line no-console
      console.log("Rendered HTML:", document.body.innerHTML);
      throw e;
    }
  }, 15000);

  test("runs workflow and displays results", async () => {
    render(<WorkflowEditorPanel />);
    // Simulate selecting workflow and running it
    const workflowItem = await screen.findByText(/test_workflow/i);
    // Find the parent li and its Run Workflow button
    const workflowLi = workflowItem.closest("li");
    const runBtn = workflowLi.querySelector("button");
    await act(async () => {
      fireEvent.click(runBtn);
    });
    // Wait for results to appear
    expect(await screen.findByText(/Workflow Run Result/i)).toBeInTheDocument();
    // "Plan a trip" appears in multiple places; check at least one
    expect(screen.getAllByText(/Plan a trip/i).length).toBeGreaterThan(0);
  });

  test("handles workflow errors gracefully", async () => {
    // Mock fetch to fail for create, succeed for list
    global.fetch.mockImplementation((url, opts) => {
      if (url.endsWith("/agents/workflows/create")) {
        return Promise.reject(new Error("Failed to create workflow."));
      }
      if (url.endsWith("/agents/workflows/list")) {
        return Promise.resolve({
          json: () => Promise.resolve({ test_workflow: [{ agent: "planner", input: "Plan a trip" }] })
        });
      }
      return Promise.resolve({
        json: () => Promise.resolve({})
      });
    });
    render(<WorkflowEditorPanel />);
    // Simulate running a workflow with missing steps
    const createBtns = screen.getAllByText(/Create Workflow/i);
    await act(async () => {
      fireEvent.click(createBtns[1]);
    });
    // Wait for either error or success message
    const errorOrSuccess = await screen.findByText(
      (content) =>
        content.includes("Error: Failed to create workflow") ||
        content.includes("Workflow created")
    );
    // Print debug output
    // eslint-disable-next-line no-console
    console.log("DEBUG: Message rendered:", errorOrSuccess.textContent);
    expect(errorOrSuccess.textContent).toMatch(/Error: Failed to create workflow/);
  });
});
