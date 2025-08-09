// HelpPanel.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import HelpPanel from '../components/HelpPanel';

describe('HelpPanel', () => {
  it('renders help panel', () => {
    render(<HelpPanel />);
    expect(screen.getByText(/help/i)).toBeInTheDocument();
  });

  it('displays help topics', () => {
    const topics = ['Getting Started', 'FAQ'];
    render(<HelpPanel topics={topics} />);
    expect(screen.getByText('Getting Started')).toBeInTheDocument();
    expect(screen.getByText('FAQ')).toBeInTheDocument();
  });

  it('handles error state', () => {
    render(<HelpPanel error="Help unavailable" />);
    expect(screen.getByText(/help unavailable/i)).toBeInTheDocument();
  });
});