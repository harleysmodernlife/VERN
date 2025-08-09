// IntegrationManagerPanel.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import IntegrationManagerPanel from '../components/IntegrationManagerPanel';

describe('IntegrationManagerPanel', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('renders integration manager panel', () => {
    render(<IntegrationManagerPanel />);
    expect(screen.getByText(/integration/i)).toBeInTheDocument();
  });

  it('lists integrations and allows activation', () => {
    const integrations = [{ id: 1, name: 'Slack', provider: 'slack', configured: false, description: '', docs_url: '', required_keys: [] }, { id: 2, name: 'GitHub', provider: 'github', configured: false, description: '', docs_url: '', required_keys: [] }];
    render(<IntegrationManagerPanel integrations={integrations} />);
    expect(screen.getByText('Slack')).toBeInTheDocument();
    expect(screen.getByText('GitHub')).toBeInTheDocument();
    fireEvent.click(screen.getByText('Slack'));
    // Add assertion for activation logic if applicable
  });

  it('handles error state', () => {
    render(<IntegrationManagerPanel error="Failed to load integrations" />);
    expect(screen.getByText(/failed to load integrations/i)).toBeInTheDocument();
  });

  it('selects and persists Ollama model', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ([{ provider: 'ollama', name: 'Ollama', configured: true, description: '', docs_url: '', required_keys: ['model'] }])
    });
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ models: ['llama2', 'mistral'] })
    });
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ config: { model: 'llama2' } })
    });
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ configured: true })
    });
    render(<IntegrationManagerPanel />);
    await screen.findByText('Ollama');
    fireEvent.click(screen.getByText('Configure'));
    await screen.findByText(/LLM\/Ollama Model/i);
    fireEvent.change(screen.getByTitle('Select LLM/Ollama model'), { target: { value: 'llama2' } });
    fireEvent.click(screen.getByText('Save'));
    expect(fetch).toHaveBeenCalledWith('/integrations/ollama/configure', expect.objectContaining({ method: 'POST' }));
  });

  it('shows error on failed Ollama model persistence', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ([{ provider: 'ollama', name: 'Ollama', configured: true, description: '', docs_url: '', required_keys: ['model'] }])
    });
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ models: ['llama2'] })
    });
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ config: { model: 'llama2' } })
    });
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({})
    });
    render(<IntegrationManagerPanel />);
    await screen.findByText('Ollama');
    fireEvent.click(screen.getByText('Configure'));
    await screen.findByText(/LLM\/Ollama Model/i);
    fireEvent.change(screen.getByTitle('Select LLM/Ollama model'), { target: { value: 'llama2' } });
    fireEvent.click(screen.getByText('Save'));
    await screen.findByText(/Failed to save config/i);
  });
});