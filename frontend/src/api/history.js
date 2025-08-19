// src/api/history.js
import api from './axios'

// CREATE
export const createHistory = (payload) =>
  api.post('/weather/history', payload).then(r => r.data)

// READ
export const listHistory = ({ skip = 0, limit = 100 } = {}) =>
  api.get('/weather/history', { params: { skip, limit } }).then(r => r.data)

// READ
export const listAllHistory = (max = 50000) =>
  api.get('/weather/history', { params: { skip: 0, limit: max } }).then(r => r.data)

// READ
export const searchHistory = ({ location_name, start_date, end_date }) =>
  api.get('/weather/history/search', {
    params: { location_name, start_date, end_date },
  }).then(r => r.data)

// UPDATE
export const updateHistory = (id, payload) =>
  api.put(`/weather/history/${id}`, payload).then(r => r.data)

// DELETE
export const deleteHistory = (id) =>
  api.delete(`/weather/history/${id}`).then(r => r.data)

// Utility
export const distinctLocations = async () => {
  const all = await listAllHistory()
  const names = Array.from(new Set(all.map(r => r.location_name).filter(Boolean)))
  names.sort((a, b) => a.localeCompare(b))
  return names
}
