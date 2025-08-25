import { vi, it, expect, beforeEach } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import ProjectDetails from './ProjectDetails.jsx';
import { AuthContext } from '../../context/AuthContext.jsx';
import { MessagesProvider } from '../../context/MessageContext.jsx';
import GrumpyApi from '../../services/api.js';

// When adding a format to a project we need some format functions like
// scrollTo
global.scrollTo = vi.fn();

// Mock API calls
vi.mock('../../services/api', () => ({
  default: {
    getProjectDetails: vi.fn(() =>
      Promise.resolve({
        id: 1,
        name: 'One Piece',
        projectType: 'episodic',
        description: 'With his straw hat and ragtag crew, young pirate Monkey D. Luffy goes on an epic voyage for treasure.',
        posterPath: 'https://www.pathtoposter1.com',
        releaseDate: '2023-08-31',
        adult: false,
        tmdb_id: 123456,
        tmdbOriginalName: 'same as the other name',
        genres: ['adventure'],
        rating: 'PG-13',
        cameras: [
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
        ],
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
            upVotes: 3,
            downVotes: 0,
            totalVotes: 3,
            score: 3,
            userVote: 'up',
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
            upVotes: 0,
            downVotes: 2,
            totalVotes: 2,
            score: -2,
            userVote: 'down',
          },
        ],
      })
    ),
    addFormat: vi.fn(() =>
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
    deleteProject: vi.fn(() =>
      Promise.resolve({
        success: 'Project deleted',
      })
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
  },
}));

describe('ProjectDetails component', () => {
  /**
   * Render the componenet with authentication context
   *
   * @returns {Component} - Makes component wrapped in MemoryRouter and AuthContext
   */

  const renderWithAuth = (authValue = { token: 'fake-token', currentUser: 'testUser' }) => {
    return render(
      <MemoryRouter initialEntries={['/projects/1']}>
        <MessagesProvider>
          <AuthContext.Provider value={authValue}>
            <Routes>
              <Route path="/projects/:projectId" element={<ProjectDetails />} />
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
    await screen.findByText('One Piece (2023)');
  });

  it('matches snapshot', async () => {
    const { asFragment } = renderWithAuth();

    await screen.findByText('One Piece (2023)');
    expect(asFragment()).toMatchSnapshot();
  });

  it('displays the correct info', async () => {
    renderWithAuth();

    await waitFor(() => {
      expect(screen.getByText('One Piece (2023)')).toBeInTheDocument();
      expect(screen.getByText('With his straw hat and ragtag crew, young pirate Monkey D. Luffy goes on an epic voyage for treasure.')).toBeInTheDocument();
      expect(screen.getByText('episodic')).toBeInTheDocument();
      // expect(screen.getByText('4.6K 3:2 Open Gate')).toBeInTheDocument();
    });
  });

  it('shows action bar for admin', async () => {
    renderWithAuth({
      token: 'fake-token',
      currentUser: 'admminUser',
      isAdmin: true,
    });
    await screen.findByText('One Piece (2023)');
    expect(screen.getByText('Delete Project')).toBeInTheDocument();
  });

  it('shows action bar for regular users', async () => {
    renderWithAuth({ token: 'fake-token', currentUser: 'regularUser' });
    await screen.findByText('One Piece (2023)');
    expect(screen.queryByText('Delete Project')).not.toBeInTheDocument();
    expect(screen.getByText('Add Format')).toBeInTheDocument();
  });
});
