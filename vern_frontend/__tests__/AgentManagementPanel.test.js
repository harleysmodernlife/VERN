// AgentManagementPanel.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import AgentManagementPanel from '../components/AgentManagementPanel';

describe('AgentManagementPanel', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('renders without crashing', () => {
    render(<AgentManagementPanel />);
    expect(screen.getByText(/agent/i)).toBeInTheDocument();
  });

  it('displays agent list and handles selection', () => {
    const agents = [{ id: 1, name: 'Agent One', cluster: '' }, { id: 2, name: 'Agent Two', cluster: '' }];
    render(<AgentManagementPanel agents={agents} />);
    expect(screen.getByText('Agent One')).toBeInTheDocument();
    expect(screen.getByText('Agent Two')).toBeInTheDocument();
    fireEvent.click(screen.getByText('Agent One'));
    // Add assertion for selection logic if applicable
  });

  it('handles API errors gracefully', () => {
    render(<AgentManagementPanel error="Failed to load agents" />);
    expect(screen.getByText(/failed to load agents/i)).toBeInTheDocument();
  });

  it('creates a new agent', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({})
    });
    render(<AgentManagementPanel />);
    fireEvent.change(screen.getByPlaceholderText('Agent Name'), { target: { value: 'NewAgent' } });
    fireEvent.change(screen.getByPlaceholderText('Cluster'), { target: { value: 'Alpha' } });
    fireEvent.click(screen.getByText('Add'));
    expect(fetch).toHaveBeenCalledWith('/registry/', expect.objectContaining({ method: 'POST' }));
  });

  it('edits an agent', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ agents: [{ name: 'Agent One', cluster: '' }] })
    });
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({})
    });
    render(<AgentManagementPanel />);
    await screen.findByText('Agent One');
    fireEvent.click(screen.getByText('Edit'));
    fireEvent.change(screen.getAllByDisplayValue('Agent One')[0], { target: { value: 'Agent One Edited' } });
    fireEvent.click(screen.getByText('Save'));
    expect(fetch).toHaveBeenCalledWith('/registry/', expect.objectContaining({ method: 'PATCH' }));
  });

  it('deletes an agent', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ agents: [{ name: 'Agent One', cluster: '' }] })
    });
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({})
    });
    render(<AgentManagementPanel />);
    await screen.findByText('Agent One');
    fireEvent.click(screen.getByText('Delete'));
    expect(fetch).toHaveBeenCalledWith('/agents/Agent%20One', expect.objectContaining({ method: 'DELETE' }));
  });

  it('assigns a cluster to an agent', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ agents: [{ name: 'Agent One', cluster: '' }], status: {} })
    });
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({})
    });
    render(<AgentManagementPanel />);
    await screen.findByText('Agent One');
    fireEvent.change(screen.getAllByDisplayValue('')[0], { target: { value: 'Alpha' } });
    expect(fetch).toHaveBeenCalledWith('/registry/', expect.objectContaining({ method: 'PATCH' }));
  });

  it('shows error on failed agent creation', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({})
    });
    render(<AgentManagementPanel />);
    fireEvent.change(screen.getByPlaceholderText('Agent Name'), { target: { value: 'NewAgent' } });
    fireEvent.click(screen.getByText('Add'));
    await screen.findByText(/failed to add agent/i);
  });
});