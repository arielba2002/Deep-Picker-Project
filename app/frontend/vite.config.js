import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => ({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,         // listen on all interfaces
    strictPort: true,
    allowedHosts: [ 'all' ],
    proxy: {
      '/api': {
        target: 'http://backend:8888',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        secure: false,
        ws: true,
        logLevel: 'debug',
        onProxyReq: (proxyReq, req, res) => {
          // Remove any HTTPS headers
          delete proxyReq.headers['x-forwarded-proto'];
          delete proxyReq.headers['x-forwarded-ssl'];
        }
      },
      '/v1': {
        target: 'http://backend:8888/v1',
        changeOrigin: true,
        secure: false,
        ws: true,
        logLevel: 'debug'
      }
    },
    watch: {
      usePolling: true,  // Docker-friendly file watching
    },
  },
  define: {
    // Always use relative paths for proxying
    'import.meta.env.VITE_API_URL': JSON.stringify('/api'),
  },
}));
