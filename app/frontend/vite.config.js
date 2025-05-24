import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => ({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,         // listen on all interfaces
    strictPort: true,
    allowedHosts: [
      'frontend-deep.apps.gapu-2.customers.k8s.co.il'
      // or simply 'all'
    ],
    proxy: {
      // any request to /api/* will be forwarded to the backend service
      '/api': {
        target: 'http://backend:8888',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        secure: false,
      },
    },
    watch: {
      usePolling: true,  // Docker-friendly file watching
    },
  },
  define: {
    // —in dev mode, use relative /api so you hit the proxy—
    // —in prod, fall back to the real backend route URL—
    'import.meta.env.VITE_API_URL': JSON.stringify(
      mode === 'development'
        ? '/api'
        : 'https://backend-deep.apps.gapu-2.customers.k8s.co.il'
    ),
  },
}));
