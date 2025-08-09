// index.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import IndexPage from '../pages/index';

describe('IndexPage', () => {
  it('renders main dashboard', () => {
    render(<IndexPage />);
    expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
  });

  it('shows key panels and handles errors', () => {
    render(<IndexPage error="Failed to load" />);
    expect(screen.getByText(/failed to load/i)).toBeInTheDocument();
  });

  // Add more integration tests as needed for main page logic
});