// Axios calls to backend
import api from './axios'

// POST /weather/current
export const getCurrentWeather = (payload) => api.post('/weather/current', payload).then(r => r.data)

// POST /weather/forecast
export const getForecast = (payload) => api.post('/weather/forecast', payload).then(r => r.data)
