import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  preview: {
    allowedHosts: ['wholesome-renewal-production.up.railway.app', 'localhost'],
    // No proxy configuration for preview mode
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './setupTests',
  },
});
