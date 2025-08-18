import axios from 'axios'

const RAW = import.meta.env.VITE_API_BASE || ''
// strip trailing slashes so we don't end up with `//` in URLs
export const API_BASE = RAW.replace(/\/+$/, '') || 'http://localhost:8000'

console.log('[axios] baseURL =', API_BASE) // <-- optional: remove after verifying

const api = axios.create({
  baseURL: API_BASE,
  timeout: 20000,
})

export default api
