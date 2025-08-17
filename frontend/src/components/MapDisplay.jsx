import { useEffect, useState } from 'react'

export default function MapDisplay({ map, height=500, width=800 }) {
  const [src, setSrc] = useState(null)
  useEffect(() => {
    setSrc(map?.static_map_url || null)
  }, [map])

  if (!map?.static_map_url) {
    return (
      <div className="card section" style={{height}}>
        <div className="skeleton" style={{borderRadius:12, width:'100%', height:'100%'}}/>
      </div>
    )
  }

  const { label, proxy_image_url, attribution, lat, lon } = map
  const googleMapsUrl =
    (typeof lat === 'number' && typeof lon === 'number')
      ? `https://www.google.com/maps/search/?api=1&query=${lat},${lon}`
      : (label ? `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(label)}` : '#')

  const handleError = (e) => {
    if (proxy_image_url && src !== proxy_image_url) setSrc(proxy_image_url)
    else { e.currentTarget.alt='Map failed to load'; e.currentTarget.style.opacity=.5 }
  }

  return (
    <div className="card section" style={{height}}>
      <div className="header">
        <h3 style={{margin:0}}>Map {label ? `– ${label}` : ''}</h3>
        {attribution && <div className="muted" style={{fontSize:12}}>{attribution}</div>}
      </div>
      <a href={googleMapsUrl} target="_blank" rel="noreferrer" title="Open in Google Maps" className="center" style={{height: height-64}}>
        <img
          src={src}
          alt={label || 'Map'}
          width={width} height={height-64}
          style={{maxWidth:'100%', maxHeight:'100%', borderRadius:12, border:'1px solid var(--border)', objectFit:'cover'}}
          onError={handleError}
          referrerPolicy="no-referrer"
        />
      </a>
    </div>
  )
}
