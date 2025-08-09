// UserProfilePanel.test.js
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import UserProfilePanel from '../components/UserProfilePanel';

describe('UserProfilePanel', () => {
  it('renders user profile panel', () => {
    render(<UserProfilePanel />);
    expect(screen.getByText(/user profile/i)).toBeInTheDocument();
  });

  it('displays user info and allows editing', () => {
    const user = { name: 'Alice', email: 'alice@example.com' };
    render(<UserProfilePanel user={user} />);
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('alice@example.com')).toBeInTheDocument();
    fireEvent.change(screen.getByDisplayValue('Alice'), { target: { value: 'Bob' } });
    expect(screen.getByDisplayValue('Bob')).toBeInTheDocument();
  });

  it('handles error state', () => {
    render(<UserProfilePanel error="Failed to load profile" />);
    expect(screen.getByText(/failed to load profile/i)).toBeInTheDocument();
  });
});