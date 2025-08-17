// POST /locations/search
import api from './axios';

export const searchLocations = (query) =>
  api.post('/locations/search', { query }).then(r => r.data?.candidates || []);
