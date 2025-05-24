import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => ({
  plugins: [react()],
  server: {
    port: 3000,
    host: true, // Listen on all network interfaces
    strictPort: true,
    proxy: {
      // Proxy API requests to the backend
      '/api': {
        target: 'http://backend:8888',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        secure: false,
      },
    },
    watch: {
      usePolling: true, // For file watching in Docker
    },
  },
  // Environment variables
  define: {
    'import.meta.env.VITE_API_URL': JSON.stringify(
      mode === 'development' 
        ? 'http://localhost:8888' 
        : 'http://localhost:8888' // Change this in production
    ),
  },
}));
