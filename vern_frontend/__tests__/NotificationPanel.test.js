// NotificationPanel.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import NotificationPanel from '../components/NotificationPanel';

describe('NotificationPanel', () => {
  it('renders notification panel', () => {
    render(<NotificationPanel />);
    expect(screen.getByText(/notification/i)).toBeInTheDocument();
  });

  it('displays notifications', () => {
    const notifications = [
      { id: 1, message: 'Update available' },
      { id: 2, message: 'Agent added' }
    ];
    render(<NotificationPanel notifications={notifications} />);
    expect(screen.getByText('Update available')).toBeInTheDocument();
    expect(screen.getByText('Agent added')).toBeInTheDocument();
  });

  it('handles error state', () => {
    render(<NotificationPanel error="Failed to fetch notifications" />);
    expect(screen.getByText(/failed to fetch notifications/i)).toBeInTheDocument();
  });
});