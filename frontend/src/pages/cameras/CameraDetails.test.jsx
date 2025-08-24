import { vi, it, expect, beforeEach } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import CameraDetails from './CameraDetails.jsx';
import { AuthContext } from '../../context/AuthContext.jsx';
import { MessagesProvider } from '../../context/MessageContext.jsx';
import GrumpyApi from '../../services/api.js';

// Mock API calls
vi.mock('../../services/api', () => ({
  default: {
    getCameraDetails: vi.fn(() =>
      Promise.resolve({
        id: 1,
        makeId: 1,
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
        image: 'arri_alexa_35.png',
        formats: [
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
        ],
      })
    ),
    addFormat: vi.fn(() =>
      Promise.resolve({
        success: 'Created format 7',
        formatId: 7,
      })
    ),
    updateCamera: vi.fn(() =>
      Promise.resolve({
        success: 'Partialy updated camera',
        camera: {
          id: 1,
          makeId: 1,
          makeName: 'ARRI',
          model: 'Updated Alexa 35',
          sensorType: 'Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array',
          sensorSize: 'Super 35',
          maxFilmbackWidth: 27.99,
          maxFilmbackHeight: 19.22,
          maxImageWidth: 4608,
          maxImageHeight: 3164,
          minFrameRate: 0.75,
          maxFrameRate: 120,
          image: 'arri_alexa_35.png',
          formats: [
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
          ],
        },
      })
    ),
    deleteCamera: vi.fn(() =>
      Promise.resolve({
        success: 'Camera deleted',
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

describe('CameraDetails component', () => {
  /**
   * Render the componenet with authentication context
   *
   * @returns {Component} - Makes component wrapped in MemoryRouter and AuthContext
   */

  const renderWithAuth = (authValue = { token: 'fake-token', currentUser: 'testUser' }) => {
    return render(
      <MemoryRouter initialEntries={['/cameras/1']}>
        <MessagesProvider>
          <AuthContext.Provider value={authValue}>
            <Routes>
              <Route path="/cameras/:cameraId" element={<CameraDetails />} />
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
      expect(screen.getByText('Super 35 format ARRI ALEV 4 CMOS sensor with Bayer pattern color filter array')).toBeInTheDocument();
      expect(screen.getByText('4.6K 3:2 Open Gate')).toBeInTheDocument();
    });
  });

  it('shows action bar for admin', async () => {
    renderWithAuth({
      token: 'fake-token',
      currentUser: 'admminUser',
      isAdmin: true,
    });
    await screen.findByText('ARRI');
    expect(screen.getByText('Add Format')).toBeInTheDocument();
  });

  it('hides action bar for regular users', async () => {
    renderWithAuth({ token: 'fake-token', currentUser: 'admminUser' });
    await screen.findByText('ARRI');
    expect(screen.queryByText('Add Format')).not.toBeInTheDocument();
  });

  it('can add a new format when admin', async () => {
    renderWithAuth({
      token: 'fake-token',
      currentUser: 'adminUser',
      isAdmin: true,
    });
    await screen.findByText('ARRI');

    // Open modal
    fireEvent.click(screen.getByText('Add Format'));
    expect(screen.getByRole('textbox', { name: /Image Format/i })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: /Image Aspect/i })).toBeInTheDocument();

    // Fill out the required fields
    const sourceInput = screen.getByLabelText(/Source/i);
    const imageFormatInput = screen.getByLabelText(/Image Format/i);
    const imageAspecInput = screen.getByLabelText(/Image Aspect/i);
    const imageWidthInput = screen.getByLabelText(/Image Width/i);
    const imageHeightInput = screen.getByLabelText(/Image Height/i);
    const sensorWidthInput = screen.getByLabelText(/Sensor Width/i);
    const sensorHeightInput = screen.getByLabelText(/Sensor Height/i);

    fireEvent.change(sourceInput, { target: { value: 'Fake Source' } });
    fireEvent.change(imageFormatInput, {
      target: {
        value: '5K',
      },
    });
    fireEvent.change(imageAspecInput, {
      target: {
        value: '3:2',
      },
    });
    fireEvent.change(imageWidthInput, {
      target: {
        value: 4608,
      },
    });
    fireEvent.change(imageHeightInput, {
      target: { value: 3164 },
    });
    fireEvent.change(sensorWidthInput, {
      target: {
        value: 28.0,
      },
    });
    fireEvent.change(sensorHeightInput, {
      target: {
        value: 19.2,
      },
    });

    // Submit the form
    fireEvent.click(screen.getByText('Add'));

    // Modal should close after successful submission
    await waitFor(() => {
      expect(screen.queryByText('Add format to Arri Alexa 35')).not.toBeInTheDocument();
    });
  });

  it('can edit the camera when admin', async () => {
    renderWithAuth({
      token: 'fake-token',
      currentUser: 'adminUser',
      isAdmin: true,
    });
    await screen.findByText('ARRI');

    // Open modal
    fireEvent.click(screen.getByText('Edit Camera'));
    expect(screen.getByText('Edit ARRI Alexa 35')).toBeInTheDocument();

    // Fill out the required fields
    const nameInput = screen.getByLabelText(/model/i);

    fireEvent.change(nameInput, { target: { value: 'Updated Camera' } });

    // Submit the form
    fireEvent.click(screen.getByText('Update'));

    // Modal should close after successful submission
    await waitFor(() => {
      expect(screen.queryByText('Edit ARRI Alexa 35')).not.toBeInTheDocument();
    });
  });

  it('can delete the camera when admin', async () => {
    renderWithAuth({
      token: 'fake-token',
      currentUser: 'adminUser',
      isAdmin: true,
    });
    await screen.findByText('ARRI');

    // Open modal
    fireEvent.click(screen.getByText('Delete Camera'));
    expect(screen.getByText('Delete camera "Alexa 35"')).toBeInTheDocument();

    // Click the button
    fireEvent.click(screen.getByText('Delete'));

    // Modal should close after successful submission
    await waitFor(() => {
      expect(GrumpyApi.deleteCamera).toHaveBeenCalledWith('1');
    });
  });
});
