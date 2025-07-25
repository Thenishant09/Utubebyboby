import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
  server: {
    port: 3000,
    host: '0.0.0.0', // ensures accessibility from LAN and Docker
    open: true,      // automatically opens browser on server start
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    emptyOutDir: true, // cleans output dir before build
  },
});