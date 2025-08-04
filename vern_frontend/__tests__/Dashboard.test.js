// vern_frontend/__tests__/Dashboard.test.js
import React from "react";
import { render, screen, act } from "@testing-library/react";
import Dashboard from "../components/Dashboard";

test("renders dashboard panels and onboarding/help", () => {
  render(<Dashboard />);
  expect(screen.getByText(/Config Editor/i)).toBeInTheDocument();
  // Use getAllByText for ambiguous matches
  expect(screen.getAllByText(/Workflow Editor/i)[0]).toBeInTheDocument();
  expect(screen.getAllByText(/Plugin Marketplace/i)[0]).toBeInTheDocument();
  expect(screen.getByText(/Onboarding & Accessibility/i)).toBeInTheDocument();
  expect(screen.getByText(/Help & Troubleshooting/i)).toBeInTheDocument();
});

test("can check onboarding checklist and see completion", async () => {
  render(<Dashboard />);
  // Use getAllByLabelText for ambiguous matches
  const checklistItems = screen.getAllByLabelText(/Read the README/i);
  expect(checklistItems[0]).toBeInTheDocument();
  act(() => {
    checklistItems[0].click();
    // Ensure all checkboxes are checked (don't toggle back to unchecked)
    screen.getAllByRole("checkbox").forEach(cb => {
      if (!cb.checked) cb.click();
    });
  });
  // Wait for "Onboarding complete" message to appear
  expect(await screen.findByText(/Onboarding complete/i)).toBeInTheDocument();
});

test("help panel shows troubleshooting and FAQ", () => {
  render(<Dashboard />);
  expect(screen.getByText(/Help & Troubleshooting/i)).toBeInTheDocument();
  expect(screen.getByText(/FAQ:/i)).toBeInTheDocument();
  // Use getAllByText for ambiguous matches
  expect(screen.getAllByText(/missing config/i)[0]).toBeInTheDocument();
});
