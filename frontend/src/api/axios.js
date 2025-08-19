// frontend/src/api/axios.js

import axios from 'axios'

export const API_BASE =
  import.meta.env.VITE_API_BASE ||
  'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 40000,
})

if (typeof window !== 'undefined') {
  console.log('[axios] baseURL =', API_BASE)
}

export default api
