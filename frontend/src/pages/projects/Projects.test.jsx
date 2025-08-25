import { vi, it, expect, beforeEach } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Projects from './Projects.jsx';
import { AuthContext } from '../../context/AuthContext.jsx';

// Formats search scrolls up when results change so we need to mock
// scrollTo
global.scrollTo = vi.fn();

// Mock API calls
vi.mock('../../services/api', () => ({
  default: {
    getProjects: vi.fn(() =>
      Promise.resolve([
        {
          id: 1,
          name: 'One Piece',
          projectType: 'episodic',
          description: 'With his straw hat and ragtag crew, young pirate Monkey D. Luffy goes on an epic voyage for treasure.',
          poster_path: 'https://www.pathtoposter1.com',
          releaseDate: '2023-08-31',
          adult: false,
          tmdb_id: 123456,
          tmdbOriginalName: 'same as the other name',
          genres: ['adventure'],
          rating: 'PG-13',
        },

        {
          id: 2,
          name: 'Daredevil',
          projectType: 'feature',
          description: 'A pretty bad movie',
          poster_path: 'https://www.pathtoposter2.com',
          releaseDate: '2010-02-01',
          adult: false,
          tmdb_id: 654321,
          tmdbOriginalName: 'Daredevil is silly',
          genres: ['action', 'adventure'],
          rating: 'R',
        },
      ])
    ),
    findProjects: vi.fn(() =>
      Promise.resolve({
        projects: {
          local: [
            {
              id: 1,
              name: 'One Piece But it is local',
              projectType: 'episodic',
              description: 'A goofy pirate adventure',
              poster_path: 'https://www.pathtoposter1.com',
              releaseDate: '2024-01-01',
              adult: false,
              tmdb_id: 123456,
              tmdbOriginalName: 'same as the other name',
              genres: ['adventure'],
              rating: 'PG-13',
            },
          ],
          remote: [
            {
              id: 2,
              name: 'Daredevil but it is remote',
              projectType: 'feature',
              description: 'A pretty bad movie',
              poster_path: 'https://www.pathtoposter2.com',
              releaseDate: '2010-02-01',
              adult: false,
              tmdb_id: 654321,
              tmdbOriginalName: 'Daredevil is silly',
              genres: ['action', 'adventure'],
              rating: 'R',
            },
          ],
        },
      })
    ),
  },
}));

describe('Projects component', () => {
  /**
   * Render the componenet with authentication context
   *
   * @returns {Component} - Makes component wrapped in MemoryRouter and AuthContext
   */

  const renderWithAuth = (authValue = { token: 'fake-token', currentUser: 'testUser' }) => {
    return render(
      <MemoryRouter>
        <AuthContext.Provider value={authValue}>
          <Projects />
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
    await screen.findAllByText('One Piece');
  });

  it('matches snapshot', async () => {
    const { asFragment } = renderWithAuth();

    await screen.findAllByText('One Piece');
    expect(asFragment()).toMatchSnapshot();
  });

  it('displays the correct info', async () => {
    renderWithAuth();
    await screen.findAllByText('In Database');

    const table = screen.getByRole('table');
    const rows = within(table).getAllByRole('row');

    await waitFor(() => {
      // Table headers
      expect(screen.getByRole('columnheader', { name: 'Image' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Name' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Type' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Release Date' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Description' })).toBeInTheDocument();
      expect(screen.getByRole('columnheader', { name: 'Action' })).toBeInTheDocument();

      // Table data
      const firstDataRow = rows[1]; // Skip header row
      expect(within(firstDataRow).getByText('One Piece')).toBeInTheDocument();
      expect(within(firstDataRow).getByText('2023-08-31')).toBeInTheDocument();
      expect(within(firstDataRow).getByText('episodic')).toBeInTheDocument();
      expect(within(firstDataRow).getByText('With his straw hat and ragtag crew, young pirate Monkey D. Luffy goes on an epic voyage for treasure.')).toBeInTheDocument();
    });
  });

  it('can search for projets', async () => {
    renderWithAuth();

    await screen.findAllByText('In Database');

    const searchInput = screen.getByPlaceholderText('Enter search term...');
    fireEvent.change(searchInput, { target: { value: 'test search' } });
    const searchButton = screen.getByRole('button', { name: 'Search!' });

    fireEvent.click(searchButton);

    await waitFor(() => {
      // Find the sections by their headings
      const localSection = screen.getByText('In Database').closest('div');
      const remoteSection = screen.getByText('Browse TMDB').closest('div');

      expect(within(localSection).getByText('One Piece But it is local')).toBeInTheDocument();
      expect(within(remoteSection).getByText('Daredevil but it is remote')).toBeInTheDocument();
    });
  });
});
