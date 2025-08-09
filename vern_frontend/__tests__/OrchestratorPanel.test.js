// OrchestratorPanel.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import OrchestratorPanel from '../components/OrchestratorPanel';

describe('OrchestratorPanel', () => {
  it('renders orchestrator panel', () => {
    render(<OrchestratorPanel />);
    expect(screen.getByText(/orchestrator/i)).toBeInTheDocument();
  });

  it('displays orchestrator controls', () => {
    const controls = ['Start', 'Stop'];
    render(<OrchestratorPanel controls={controls} />);
    expect(screen.getByText('Start')).toBeInTheDocument();
    expect(screen.getByText('Stop')).toBeInTheDocument();
  });

  it('handles error state', () => {
    render(<OrchestratorPanel error="Orchestrator error" />);
    expect(screen.getByText(/orchestrator error/i)).toBeInTheDocument();
  });
});