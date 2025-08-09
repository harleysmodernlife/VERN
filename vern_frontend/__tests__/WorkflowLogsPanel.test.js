// WorkflowLogsPanel.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import WorkflowLogsPanel from '../components/WorkflowLogsPanel';

describe('WorkflowLogsPanel', () => {
  it('renders workflow logs panel', () => {
    render(<WorkflowLogsPanel />);
    expect(screen.getByText(/workflow logs/i)).toBeInTheDocument();
  });

  it('displays log entries', () => {
    const logs = [
      { id: 1, message: 'Workflow started' },
      { id: 2, message: 'Step completed' }
    ];
    render(<WorkflowLogsPanel logs={logs} />);
    expect(screen.getByText('Workflow started')).toBeInTheDocument();
    expect(screen.getByText('Step completed')).toBeInTheDocument();
  });

  it('handles error state', () => {
    render(<WorkflowLogsPanel error="Failed to load logs" />);
    expect(screen.getByText(/failed to load logs/i)).toBeInTheDocument();
  });
});