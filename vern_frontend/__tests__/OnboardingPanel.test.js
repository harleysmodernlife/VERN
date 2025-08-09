// OnboardingPanel.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import OnboardingPanel from '../components/OnboardingPanel';

describe('OnboardingPanel', () => {
  it('renders onboarding panel', () => {
    render(<OnboardingPanel />);
    expect(screen.getByText(/onboarding/i)).toBeInTheDocument();
  });

  it('shows onboarding steps', () => {
    const steps = ['Step 1', 'Step 2'];
    render(<OnboardingPanel steps={steps} />);
    expect(screen.getByText('Step 1')).toBeInTheDocument();
    expect(screen.getByText('Step 2')).toBeInTheDocument();
  });

  it('handles completion and error states', () => {
    render(<OnboardingPanel error="Onboarding failed" />);
    expect(screen.getByText(/onboarding failed/i)).toBeInTheDocument();
  });
});