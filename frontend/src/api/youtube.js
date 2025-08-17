import api from './axios'

export const getYouTubeForLocation = (location, params={}) =>
  api.get(`/youtube/${encodeURIComponent(location)}`, { params }).then(r => r.data)
