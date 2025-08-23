import { vi, it, expect, beforeEach } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Makes from './Makes.jsx';
import { AuthContext } from '../../context/AuthContext.jsx';
import { Component } from 'react';

// Mock API calls
vi.mock('../../services/api', () => ({
  default: {
    getMakes: vi.fn(() =>
      Promise.resolve([
        {
          id: 1,
          name: 'ARRI',
          website: 'https://www.arri.com/en',
          logo: 'arri_logo.png',
          camerasCount: 5,
        },
        {
          id: 2,
          name: 'RED',
          website: 'https://www.red.com',
          logo: 'red_logo.png',
          camerasCount: 2,
        },
      ])
    ),
    addMake: vi.fn(() =>
      Promise.resolve({
        success: 'Created make 7',
        makeId: 7,
      })
    ),
  },
}));

describe('MakeList component', () => {
  /**
   * Render the componenet with authentication context
   *
   * @returns {Component} - Makes component wrapped in MemoryRouter and AuthContext
   */

  const renderWithAuth = (authValue = { token: 'fake-token', currentUser: 'testUser' }) => {
    return render(
      <MemoryRouter>
        <AuthContext.Provider value={authValue}>
          <Makes />
        </AuthContext.Provider>
      </MemoryRouter>
    );
  };

  beforeEach(() => {
    // Clear mocks
    vi.clearAllMocks();
  });

  it('renders without crashing', async () => {
    renderWithAuth();
    await screen.findByText('ARRI');
  });

  it('matches snapshot', async () => {
    const { asFragment } = renderWithAuth();

    await screen.findByText('ARRI');
    expect(asFragment()).toMatchSnapshot();
  });

  it('displays the correct info', async () => {
    renderWithAuth();

    await waitFor(() => {
      expect(screen.getByText('ARRI')).toBeInTheDocument();
      expect(screen.getByText('5 Cameras')).toBeInTheDocument();
      expect(screen.getByText('RED')).toBeInTheDocument();
      expect(screen.getByText('2 Cameras')).toBeInTheDocument();
    });
  });

  it('shows action bar for admin', async () => {
    renderWithAuth({
      token: 'fake-token',
      currentUser: 'admminUser',
      isAdmin: true,
    });
    await screen.findByText('ARRI');
    expect(screen.getByText('Add Make')).toBeInTheDocument();
  });

  it('hides action bar for regular users', async () => {
    renderWithAuth({ token: 'fake-token', currentUser: 'admminUser' });
    await screen.findByText('ARRI');
    expect(screen.queryByText('Add Make')).not.toBeInTheDocument();
  });

  it('can add a new make when admin', async () => {
    renderWithAuth({
      token: 'fake-token',
      currentUser: 'adminUser',
      isAdmin: true,
    });
    await screen.findByText('ARRI');

    // Open modal
    fireEvent.click(screen.getByText('Add Make'));
    expect(screen.getByText('Website')).toBeInTheDocument();

    // Fill out the required fields
    const nameInput = screen.getByLabelText(/name/i);
    const websiteInput = screen.getByLabelText(/website/i);

    fireEvent.change(nameInput, { target: { value: 'Sony' } });
    fireEvent.change(websiteInput, {
      target: { value: 'https://www.sony.com' },
    });

    // Submit the form
    fireEvent.click(screen.getByText('Add'));

    // Modal should close after successful submission
    await waitFor(() => {
      expect(screen.queryByText('Website')).not.toBeInTheDocument();
    });
  });
});
