import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
// RAG Branch Configuration: Port 3001, Backend 8001
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3001,  // RAG branch uses port 3001
    strictPort: true,  // Fail if port is already in use instead of trying another port
    proxy: {
      '/api': {
        target: 'http://localhost:8001',  // RAG branch backend on 8001
        changeOrigin: true,
      },
    },
  },
})


