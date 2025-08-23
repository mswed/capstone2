import { vi, it, expect, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import Home from './Home';

// Mock API calls
vi.mock('../services/api', () => ({
  default: {
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

describe('Home component', () => {
  beforeEach(() => {
    // Clear mocks
    vi.clearAllMocks();
  });

  it('renders without crashing', async () => {
    render(<Home />);
    await screen.findByText('30 Projects');
  });

  it('matches snapshot', async () => {
    const { asFragment } = render(<Home />);

    await screen.findByText('30 Projects');
    expect(asFragment()).toMatchSnapshot();
  });

  it('displays the correct stats', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText('30 Projects')).toBeInTheDocument();
      expect(screen.getByText('3 Makes')).toBeInTheDocument();
      expect(screen.getByText('10 Cameras')).toBeInTheDocument();
      expect(screen.getByText('200 Formats')).toBeInTheDocument();
      expect(screen.getByText('Endless complaints...')).toBeInTheDocument();
    });
  });
});
