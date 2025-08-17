import api, { API_BASE } from './axios';

const absolutize = (u) => (u && !u.startsWith('http') ? `${API_BASE}${u}` : u);

export const getMapForLocation = (location, params = {}) =>
  api.get(`/maps/${encodeURIComponent(location)}`, { params }).then((r) => {
    const d = r.data || {};
    d.static_map_url = absolutize(d.static_map_url);
    d.proxy_image_url = absolutize(d.proxy_image_url);
    return d;
  });

export const getMapByCoords = (lat, lon, params = {}) =>
  api
    .get(`/maps/by-coords`, { params: { lat, lon, ...params } })
    .then((r) => {
      const d = r.data || {};
      d.static_map_url = absolutize(d.static_map_url);
      d.proxy_image_url = absolutize(d.proxy_image_url);
      return d;
    });
