// ConfigEditorPanel.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ConfigEditorPanel from '../components/ConfigEditorPanel';

describe('ConfigEditorPanel', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('renders config editor', () => {
    render(<ConfigEditorPanel />);
    expect(screen.getByText(/config/i)).toBeInTheDocument();
  });

  it('shows config fields and allows editing', () => {
    const config = { apiUrl: 'http://localhost', theme: 'dark' };
    render(<ConfigEditorPanel config={config} />);
    expect(screen.getByDisplayValue('http://localhost')).toBeInTheDocument();
    fireEvent.change(screen.getByDisplayValue('http://localhost'), { target: { value: 'http://test' } });
    expect(screen.getByDisplayValue('http://test')).toBeInTheDocument();
  });

  it('handles save and error states', () => {
    render(<ConfigEditorPanel error="Save failed" />);
    expect(screen.getByText(/save failed/i)).toBeInTheDocument();
  });

  it('selects and persists Ollama model', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ models: ['llama2', 'mistral'] })
    });
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({})
    });
    render(<ConfigEditorPanel />);
    await screen.findByText(/LLM\/Ollama Model/i);
    fireEvent.change(screen.getByTitle('Select LLM/Ollama model'), { target: { value: 'llama2' } });
    fireEvent.click(screen.getByText('Save YAML'));
    expect(fetch).toHaveBeenCalledWith('/config/yaml', expect.objectContaining({ method: 'POST' }));
  });

  it('shows error on failed model persistence', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ models: ['llama2'] })
    });
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({})
    });
    render(<ConfigEditorPanel />);
    await screen.findByText(/LLM\/Ollama Model/i);
    fireEvent.change(screen.getByTitle('Select LLM/Ollama model'), { target: { value: 'llama2' } });
    fireEvent.click(screen.getByText('Save YAML'));
    await screen.findByText(/failed to save yaml config/i);
  });
});