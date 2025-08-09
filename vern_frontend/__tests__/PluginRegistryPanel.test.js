// PluginRegistryPanel.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import PluginRegistryPanel from '../components/PluginRegistryPanel';

describe('PluginRegistryPanel', () => {
  it('renders plugin registry panel', () => {
    render(<PluginRegistryPanel />);
    expect(screen.getByText(/plugin registry/i)).toBeInTheDocument();
  });

  it('lists plugins', () => {
    const plugins = [{ id: 1, name: 'Plugin A' }, { id: 2, name: 'Plugin B' }];
    render(<PluginRegistryPanel plugins={plugins} />);
    expect(screen.getByText('Plugin A')).toBeInTheDocument();
    expect(screen.getByText('Plugin B')).toBeInTheDocument();
  });

  it('handles error state', () => {
    render(<PluginRegistryPanel error="Failed to load plugins" />);
    expect(screen.getByText(/failed to load plugins/i)).toBeInTheDocument();
  });
});