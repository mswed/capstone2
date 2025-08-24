import { vi, it, expect, beforeEach } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Cameras from './Cameras.jsx';
import { AuthContext } from '../../context/AuthContext.jsx';
import { Component } from 'react';

// Mock API calls
vi.mock('../../services/api', () => ({
  default: {
    getCameras: vi.fn(() =>
      Promise.resolve([
        {
          id: 1,
          make: 1,
          makeName: 'ARRI',
          model: 'Alexa 35',
          sensorType: 'Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array',
          sensorSize: 'Super 35',
          maxFilmbackWidth: 27.99,
          maxFilmbackHeight: 19.22,
          maxImageWidth: 4608,
          maxImageHeight: 3164,
          minFrameRate: 0.75,
          maxFrameRate: 120,
          notes: 'sample notes',
        },
      ])
    ),
    findCameras: vi.fn(() =>
      Promise.resolve([
        {
          id: 2,
          make: 2,
          makeName: 'RED',
          model: 'KOMODO-X',
          sensorType: 'KOMODO-X™ 19.9MP Super 35mm Global Shutter CMOS',
          sensorSize: 'Super 35',
          maxFilmbackWidth: 27.03,
          maxFilmbackHeight: 14.26,
          maxImageWidth: 6144,
          maxImageHeight: 3240,
          minFrameRate: 24,
          maxFrameRate: 240,
        },
      ])
    ),
  },
}));

describe('Cameras component', () => {
  /**
   * Render the componenet with authentication context
   *
   * @returns {Component} - Makes component wrapped in MemoryRouter and AuthContext
   */

  const renderWithAuth = (authValue = { token: 'fake-token', currentUser: 'testUser' }) => {
    return render(
      <MemoryRouter>
        <AuthContext.Provider value={authValue}>
          <Cameras />
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
      // Table headers
      expect(screen.getByText('Image')).toBeInTheDocument();
      expect(screen.getByText('Make')).toBeInTheDocument();
      expect(screen.getByText('Model')).toBeInTheDocument();
      expect(screen.getByText('Sensor Type')).toBeInTheDocument();
      expect(screen.getByText('Max Filmback Size')).toBeInTheDocument();
      expect(screen.getByText('Max Resolution')).toBeInTheDocument();

      // Table data
      expect(screen.getByText('ARRI')).toBeInTheDocument();
      expect(screen.getByText('Alexa 35')).toBeInTheDocument();
      expect(screen.getByText('Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array')).toBeInTheDocument();
      expect(screen.getByText('27.99mm x 19.22mm')).toBeInTheDocument();
      expect(screen.getByText('4608 x 3164')).toBeInTheDocument();
    });
  });

  it('can search for cameras', async () => {
    renderWithAuth();

    await screen.findByText('ARRI');

    // Fill out the required fields
    const searchInput = screen.getByPlaceholderText('Enter search term...');
    const searchButton = screen.getByRole('button', { name: /search/i });

    fireEvent.change(searchInput, { target: { value: 'RED' } });
    fireEvent.click(searchButton);

    await waitFor(() => {
      // Table headers
      expect(screen.getByText('Image')).toBeInTheDocument();
      expect(screen.getByText('Make')).toBeInTheDocument();
      expect(screen.getByText('Model')).toBeInTheDocument();
      expect(screen.getByText('Sensor Type')).toBeInTheDocument();
      expect(screen.getByText('Max Filmback Size')).toBeInTheDocument();
      expect(screen.getByText('Max Resolution')).toBeInTheDocument();

      // Table data
      expect(screen.getByText('RED')).toBeInTheDocument();
    });
  });
});
