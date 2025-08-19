// frontend/src/components/MapDisplay.jsx

import { useEffect, useMemo, useState } from 'react'
import { API_BASE } from '../api/axios'

export default function MapDisplay({ map, height = 500, width = 800 }) {
  const [src, setSrc] = useState(null)

  const absolutize = (url) => (url && !url.startsWith('http') ? `${API_BASE}${url}` : url)

  const withParam = (url, key, val) => {
    if (!url) return url
    const u = new URL(absolutize(url), window.location.origin)
    u.searchParams.set(key, `${val}`)
    return u.toString()
  }

  const urls = useMemo(() => {
    if (!map?.static_map_url) return {}
    const png1x = withParam(map.static_map_url, 'scale', 1)
    const fallback1 = map.proxy_image_url ? withParam(map.proxy_image_url, 'scale', 1) : null
    return { png1x, fallback1 }
  }, [map])

  useEffect(() => {
    setSrc(urls.png1x || null)
  }, [urls.png1x])

  if (!map?.static_map_url) {
    return (
      <div className="card section" style={{ height }}>
        <div className="skeleton" style={{ borderRadius: 12, width: '100%', height: '100%' }} />
      </div>
    )
  }

  const { label, attribution, lat, lon } = map
  const googleMapsUrl =
    (typeof lat === 'number' && typeof lon === 'number')
      ? `https://www.google.com/maps/search/?api=1&query=${lat},${lon}`
      : (label ? `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(label)}` : '#')

  const onError = (e) => {
    if (urls.fallback1 && src !== urls.fallback1) return setSrc(urls.fallback1)
    e.currentTarget.alt = 'Map failed to load'
    e.currentTarget.style.opacity = 0.5
  }

  return (
    <div className="card section" style={{ height, display: 'flex', flexDirection: 'column' }}>
      <div className="header" style={{ flex: '0 0 auto' }}>
        <h3 style={{ margin: 0 }}>Map {label ? `– ${label}` : ''}</h3>
        {attribution && <div className="muted" style={{ fontSize: 12 }}>{attribution}</div>}
      </div>

      <a
        href={googleMapsUrl}
        target="_blank"
        rel="noreferrer"
        title="Open in Google Maps"
        style={{ flex: '1 1 auto', width: '100%', display: 'block' }}
      >
        <img
          src={src}
          alt={label || 'Map'}
          onError={onError}
          loading="lazy"
          decoding="async"
          referrerPolicy="no-referrer"
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            borderRadius: 12,
            border: '1px solid var(--border)',
            display: 'block',
          }}
        />
      </a>
    </div>
  )
}
