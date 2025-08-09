// FeedbackPanel.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import FeedbackPanel from '../components/FeedbackPanel';

describe('FeedbackPanel', () => {
  it('renders feedback panel', () => {
    render(<FeedbackPanel />);
    expect(screen.getByText(/feedback/i)).toBeInTheDocument();
  });

  it('accepts user feedback input', () => {
    render(<FeedbackPanel />);
    const input = screen.getByPlaceholderText(/enter feedback/i);
    fireEvent.change(input, { target: { value: 'Great job!' } });
    expect(input.value).toBe('Great job!');
  });

  it('handles submit and error states', () => {
    render(<FeedbackPanel error="Submission failed" />);
    expect(screen.getByText(/submission failed/i)).toBeInTheDocument();
  });
});