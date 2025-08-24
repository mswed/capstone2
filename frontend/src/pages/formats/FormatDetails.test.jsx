import { vi, it, expect, beforeEach } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import FormatDetails from './FormatDetails.jsx';
import { AuthContext } from '../../context/AuthContext.jsx';
import { MessagesProvider } from '../../context/MessageContext.jsx';
import GrumpyApi from '../../services/api.js';

// Mock API calls
vi.mock('../../services/api', () => ({
  default: {
    getFormatDetails: vi.fn(() =>
      Promise.resolve({
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
      })
    ),
    updateFormat: vi.fn(() =>
      Promise.resolve({
        success: 'Partialy updated format',
        format: {
          id: 1,
          camera: 1,
          cameraModel: 'Alexa 35 Updated',
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
      })
    ),
    deleteFormat: vi.fn(() =>
      Promise.resolve({
        success: 'Format deleted',
      })
    ),
    getSources: vi.fn(() =>
      Promise.resolve([
        {
          id: 1,
          name: 'Sample Source',
          url: 'http://www.samplesource.com',
          fileName: 'sample.pdf',
          note: 'a fake source',
        },
      ])
    ),
  },
}));

describe('FormatDetails component', () => {
  /**
   * Render the componenet with authentication context
   *
   * @returns {Component} - Makes component wrapped in MemoryRouter and AuthContext
   */

  const renderWithAuth = (authValue = { token: 'fake-token', currentUser: 'testUser' }) => {
    return render(
      <MemoryRouter initialEntries={['/formats/1']}>
        <MessagesProvider>
          <AuthContext.Provider value={authValue}>
            <Routes>
              <Route path="/formats/:formatId" element={<FormatDetails />} />
            </Routes>
          </AuthContext.Provider>
        </MessagesProvider>
      </MemoryRouter>
    );
  };

  beforeEach(() => {
    // Clear mocks
    vi.clearAllMocks();
  });

  it('renders without crashing', async () => {
    renderWithAuth();
    await screen.findByText('Alexa 35');
  });

  it('matches snapshot', async () => {
    const { asFragment } = renderWithAuth();

    await screen.findByText('Alexa 35');
    expect(asFragment()).toMatchSnapshot();
  });

  it('displays the correct info', async () => {
    renderWithAuth();

    await waitFor(() => {
      expect(screen.getByText('ARRI')).toBeInTheDocument();
      expect(screen.getByText('Alexa 35')).toBeInTheDocument();
      expect(screen.getByText('4608 x 3164')).toBeInTheDocument();
      expect(screen.getByText('28mm x 19.2mm')).toBeInTheDocument();
      expect(screen.getByText('ARRIRAW')).toBeInTheDocument();
      expect(screen.getByText('sample notes')).toBeInTheDocument();
      expect(
        screen.getByText(
          '4.6K 3:2 Open Gate provides maximum image quality, resolution, and flexibility in post for many spherical and anamorphic lenses in an image area slightly larger than traditional Super 35 film specifications.'
        )
      ).toBeInTheDocument();
    });
  });

  it('shows action bar for admin', async () => {
    renderWithAuth({
      token: 'fake-token',
      currentUser: 'admminUser',
      isAdmin: true,
    });
    await screen.findByText('ARRI');
    expect(screen.getByText('Edit Format')).toBeInTheDocument();
  });

  it('hides action bar for regular users', async () => {
    renderWithAuth({ token: 'fake-token', currentUser: 'admminUser' });
    await screen.findByText('ARRI');
    expect(screen.queryByText('Edit Format')).not.toBeInTheDocument();
  });

  it('can edit the format when admin', async () => {
    renderWithAuth({
      token: 'fake-token',
      currentUser: 'adminUser',
      isAdmin: true,
    });
    await screen.findByText('ARRI');

    // Open modal
    fireEvent.click(screen.getByText('Edit Format'));
    expect(screen.getByText('Edit format 4.6K 3:2 Open Gate')).toBeInTheDocument();

    // Fill out the required fields
    const imageFormatInput = screen.getByLabelText(/image format/i);

    fireEvent.change(imageFormatInput, { target: { value: 'Updated Format' } });

    // Submit the form
    fireEvent.click(screen.getByText('Update'));

    // Modal should close after successful submission
    await waitFor(() => {
      expect(screen.queryByText('Edit format 4.6K 3:2 Open Gate')).not.toBeInTheDocument();
    });
  });

  it('can delete the format when admin', async () => {
    renderWithAuth({
      token: 'fake-token',
      currentUser: 'adminUser',
      isAdmin: true,
    });
    await screen.findByText('ARRI');

    // Open modal
    fireEvent.click(screen.getByText('Delete Format'));
    expect(screen.getByText('Delete format "4.6K 3:2 Open Gate"')).toBeInTheDocument();

    // Click the button
    fireEvent.click(screen.getByText('Delete'));

    // Modal should close after successful submission
    await waitFor(() => {
      expect(GrumpyApi.deleteFormat).toHaveBeenCalledWith('1');
    });
  });
});
