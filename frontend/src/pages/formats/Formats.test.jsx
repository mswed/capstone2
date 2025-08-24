import { vi, it, expect, beforeEach } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Formats from './Formats.jsx';
import { AuthContext } from '../../context/AuthContext.jsx';

// Formats search scrolls up when results change so we need to mock
// scrollTo
global.scrollTo = vi.fn();

// Mock API calls
vi.mock('../../services/api', () => ({
  default: {
    getFormats: vi.fn(() =>
      Promise.resolve([
        {
          id: 1,
          camera: 1,
          cameraModel: 'Alexa 35',
          makeName: 'ARRI',
          imageFormat: '4.6K',
          imageAspect: '3:2',
          formatName: 'Open Gate',
          sensorWidth: 28.0,
          sensorHeight: 19.2,
          imageWidth: 4608,
          imageHeight: 3164,
          pixelAspect: 1.0,
          isAnamorphic: false,
          isDesqueezed: false,
          anamorphicSqueeze: null,
          filmbackWidth3de: 28.0,
          filmbackHeight3de: 19.2,
          isDownsampled: false,
          isUpscaed: false,
          codec: 'ARRIRAW',
          rawReordingAvailable: true,
          source: 1,
          notes: 'sample notes',
          makeNotes:
            '4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.',
          trackingWorkflow: 'Do this then that',
        },
        {
          id: 2,
          camera: 1,
          cameraModel: 'Alexa 35',
          makeName: 'ARRI',
          imageFormat: '4K',
          imageAspect: '16:9',
          sensorWidth: 28.0,
          sensorHeight: 15.7,
          imageWidth: 4096,
          imageHeight: 2304,
          pixelAspect: 1.0,
          isAnamorphic: false,
          isDesqueezed: false,
          anamorphicSqueeze: null,
          filmbackWidth3de: 28.0,
          filmbackHeight3de: 19.2,
          isDownsampled: true,
          isUpscaed: false,
          codec: 'ProRes',
          rawReordingAvailable: true,
          source: 1,
          notes: 'Downsampled from 4.6K 16:9',
          makeNotes:
            '4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.',
          trackingWorkflow: 'Do that then this',
        },
      ])
    ),
    findFormats: vi.fn(() =>
      Promise.resolve([
        {
          id: 3,
          camera: 3,
          cameraModel: 'KOMODO',
          makeName: 'RED',
          imageFormat: '6K',
          imageAspect: '2.4:1',
          sensorWidth: 27.03,
          sensorHeight: 11.4,
          imageWidth: 6144,
          imageHeight: 2592,
          codec: 'R3D',
          source: 5,
          notes: 'There is a discrapency in the documentation the height is either 2592 or 2574',
          pixelAspect: 1.0,
          isAnamorphic: false,
          isDesqueezed: false,
          anamorphicSqueeze: null,
          filmbackWidth3de: 28.0,
          filmbackHeight3de: 19.2,
          isDownsampled: true,
          isUpscaed: false,
          rawReordingAvailable: true,
          makeNotes: '10 out of 10, no notes',
          trackingWorkflow: 'Do that then this',
        },
      ])
    ),
    getStats: vi.fn(() =>
      Promise.resolve({
        projects: 30,
        cameras: 10,
        makes: 3,
        formats: 200,
      })
    ),
  },
}));

describe('Formats component', () => {
  /**
   * Render the componenet with authentication context
   *
   * @returns {Component} - Makes component wrapped in MemoryRouter and AuthContext
   */

  const renderWithAuth = (authValue = { token: 'fake-token', currentUser: 'testUser' }) => {
    return render(
      <MemoryRouter>
        <AuthContext.Provider value={authValue}>
          <Formats />
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
    await screen.findAllByText('ARRI');
  });

  it('matches snapshot', async () => {
    const { asFragment } = renderWithAuth();

    await screen.findAllByText('ARRI');
    expect(asFragment()).toMatchSnapshot();
  });

  it('displays the correct info', async () => {
    renderWithAuth();
    await screen.findAllByText('ARRI');

    const table = screen.getByRole('table');
    const rows = within(table).getAllByRole('row');

    await waitFor(() => {
      // Table headers
      expect(screen.getByRole('columnheader', { name: 'Make' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Model' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Format' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Resolution' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Filmback' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'PAR' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Anamorphic?' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Desqueezed?' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Action' })).toBeInTheDocument();

      // Table data
      const firstDataRow = rows[1]; // Skip header row
      expect(within(firstDataRow).getByText('ARRI')).toBeInTheDocument();
      expect(within(firstDataRow).getByText('Alexa 35')).toBeInTheDocument();
      expect(within(firstDataRow).getByText('4.6K 3:2 Open Gate')).toBeInTheDocument();
      expect(within(firstDataRow).getByText('4608 x 3164')).toBeInTheDocument();
      expect(within(firstDataRow).getByText('28mm x 19.2mm')).toBeInTheDocument();
    });
  });

  it('can search for formats', async () => {
    renderWithAuth();

    await screen.findAllByText('ARRI');

    // Fill out the required fields
    const searchButton = screen.getByRole('button', { name: /search/i });

    fireEvent.click(searchButton);

    await waitFor(() => {
      // Table headers
      expect(screen.getByRole('columnheader', { name: 'Make' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Model' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Format' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Resolution' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Filmback' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'PAR' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Anamorphic?' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Desqueezed?' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Action' })).toBeInTheDocument();

      // Table data
      expect(screen.getByText('RED')).toBeInTheDocument();
    });
  });
});
