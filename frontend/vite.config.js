import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// If you want to proxy to backend during dev (optional), uncomment and set target.
// Otherwise we’ll use absolute URLs from an env var in Axios.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173
    // proxy: {
    //   '/api': {
    //     target: 'http://127.0.0.1:8000',
    //     changeOrigin: true
    //   }
    // }
  }
})
