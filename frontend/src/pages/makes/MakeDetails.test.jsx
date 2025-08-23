import { vi, it, expect, beforeEach } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import MakeDetails from './MakeDetails.jsx';
import { AuthContext } from '../../context/AuthContext.jsx';
import { MessagesProvider } from '../../context/MessageContext.jsx';
import GrumpyApi from '../../services/api.js';

// Mock API calls
vi.mock('../../services/api', () => ({
  default: {
    getMakeDetails: vi.fn(() =>
      Promise.resolve({
        id: 1,
        name: 'ARRI',
        website: 'https://www.arri.com/en',
        logo: 'arri_logo.png',
        camerasCount: 2,
        cameras: [
          {
            id: 1,
            makeId: 1,
            makeName: 'Arri',
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
          },
          {
            id: 2,
            makeId: 1,
            makeName: 'Arri',
            model: 'Alexa Mini LF',
            sensorType: 'Large Format ARRI ALEV III (A2X) CMOS sensor with Bayer pattern color filter array',
            sensorSize: 'Large Format',
            maxFilmbackWidth: 36.7,
            maxFilmbackHeight: 25.54,
            maxImageWith: 4448,
            maxImageHeight: 3096,
            minFrameRate: 0.75,
            maxFrameRate: 90,
            image: 'arri_alexa_mini.png',
          },
        ],
      })
    ),
    addCamera: vi.fn(() =>
      Promise.resolve({
        success: 'Created camera 7',
        cameraId: 7,
      })
    ),
    updateMake: vi.fn(() =>
      Promise.resolve({
        success: 'Partialy updated make',
        make: {
          id: 1,
          name: 'ARRI',
          website: 'https://www.arri.com/en',
          logo: 'arri_logo.png',
          camerasCount: 2,
          cameras: [
            {
              id: 1,
              makeId: 1,
              makeName: 'Arri',
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
            },
            {
              id: 2,
              makeId: 1,
              makeName: 'Arri',
              model: 'Alexa Mini LF',
              sensorType: 'Large Format ARRI ALEV III (A2X) CMOS sensor with Bayer pattern color filter array',
              sensorSize: 'Large Format',
              maxFilmbackWidth: 36.7,
              maxFilmbackHeight: 25.54,
              maxImageWith: 4448,
              maxImageHeight: 3096,
              minFrameRate: 0.75,
              maxFrameRate: 90,
              image: 'arri_alexa_mini.png',
            },
          ],
        },
      })
    ),
    deleteMake: vi.fn(() =>
      Promise.resolve({
        success: 'Make deleted',
      })
    ),
  },
}));

describe('MakeDetails component', () => {
  /**
   * Render the componenet with authentication context
   *
   * @returns {Component} - Makes component wrapped in MemoryRouter and AuthContext
   */

  const renderWithAuth = (authValue = { token: 'fake-token', currentUser: 'testUser' }) => {
    return render(
      <MemoryRouter initialEntries={['/makes/1']}>
        <MessagesProvider>
          <AuthContext.Provider value={authValue}>
            <Routes>
              <Route path="/makes/:makeId" element={<MakeDetails />} />
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
      expect(screen.getByText('https://www.arri.com/en')).toBeInTheDocument();
      expect(screen.getByText('Alexa 35')).toBeInTheDocument();
      expect(screen.getByText('Alexa Mini LF')).toBeInTheDocument();
    });
  });

  it('shows action bar for admin', async () => {
    renderWithAuth({
      token: 'fake-token',
      currentUser: 'admminUser',
      isAdmin: true,
    });
    await screen.findByText('ARRI');
    expect(screen.getByText('Add Camera')).toBeInTheDocument();
  });

  it('hides action bar for regular users', async () => {
    renderWithAuth({ token: 'fake-token', currentUser: 'admminUser' });
    await screen.findByText('ARRI');
    expect(screen.queryByText('Add Camera')).not.toBeInTheDocument();
  });

  it('can add a new camera when admin', async () => {
    // TODO: Might need to mock CameraForm component to speed up this test
    // Currently ~578ms due to filling out 8 form fields

    renderWithAuth({
      token: 'fake-token',
      currentUser: 'adminUser',
      isAdmin: true,
    });
    await screen.findByText('ARRI');

    // Open modal
    fireEvent.click(screen.getByText('Add Camera'));
    expect(screen.getByRole('textbox', { name: /Model/i })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: /Sensor Type/i })).toBeInTheDocument();

    // Fill out the required fields
    const modelInput = screen.getByLabelText(/Model/i);
    const sensorSizeInput = screen.getByLabelText(/Sensor Type/i);
    const maxFilmbackWidthInput = screen.getByLabelText(/Max Filmback Width/i);
    const maxFilmbackHeightInput = screen.getByLabelText(/Max Filmback Height/i);
    const maxImageWidthInput = screen.getByLabelText(/Max Image Width/i);
    const maxImageHeightInput = screen.getByLabelText(/Max Image Height/i);
    const maxFrameRateInput = screen.getByLabelText(/Max Frame Rate/i);
    const minFrameRateInput = screen.getByLabelText(/Min Frame Rate/i);

    fireEvent.change(modelInput, { target: { value: 'Alexa Amira' } });
    fireEvent.change(sensorSizeInput, {
      target: {
        value: 'Super 35 format ARRI ALEV III CMOS sensor with Bayer pattern color filter array',
      },
    });
    fireEvent.change(maxFilmbackWidthInput, {
      target: {
        value: 26.4,
      },
    });
    fireEvent.change(maxFilmbackHeightInput, {
      target: {
        value: 14.85,
      },
    });
    fireEvent.change(maxImageWidthInput, {
      target: { value: 3200 },
    });
    fireEvent.change(maxImageHeightInput, {
      target: {
        value: 1800,
      },
    });
    fireEvent.change(minFrameRateInput, {
      target: {
        value: 0.75,
      },
    });
    fireEvent.change(maxFrameRateInput, {
      target: {
        value: 200,
      },
    });

    // Submit the form
    fireEvent.click(screen.getByText('Add'));

    // Modal should close after successful submission
    await waitFor(() => {
      expect(screen.queryByText('New Camera By Arri')).not.toBeInTheDocument();
    });
  });

  it('can edit the make when admin', async () => {
    renderWithAuth({
      token: 'fake-token',
      currentUser: 'adminUser',
      isAdmin: true,
    });
    await screen.findByText('ARRI');

    // Open modal
    fireEvent.click(screen.getByText('Edit Make'));
    expect(screen.getByText('Website')).toBeInTheDocument();

    // Fill out the required fields
    const nameInput = screen.getByLabelText(/name/i);

    fireEvent.change(nameInput, { target: { value: 'Updated Make' } });

    // Submit the form
    fireEvent.click(screen.getByText('Update'));

    // Modal should close after successful submission
    await waitFor(() => {
      expect(screen.queryByText('Website')).not.toBeInTheDocument();
    });
  });

  it('can delete the make when admin', async () => {
    renderWithAuth({
      token: 'fake-token',
      currentUser: 'adminUser',
      isAdmin: true,
    });
    await screen.findByText('ARRI');

    // Open modal
    fireEvent.click(screen.getByText('Delete Make'));
    expect(screen.getByText('Delete make "ARRI"')).toBeInTheDocument();

    // Click the button
    fireEvent.click(screen.getByText('Delete'));

    // Modal should close after successful submission
    await waitFor(() => {
      expect(GrumpyApi.deleteMake).toHaveBeenCalledWith('1');
    });
  });
});
