// frontend/src/components/YouTubeEmbed.jsx

export default function YouTubeEmbed({ videos = [], height = 500 }) {
  if (!videos?.length) return null

  const headerH = 44 // px

  return (
    <div className="card section" style={{ height, display: 'flex', flexDirection: 'column' }}>
      <div className="header" style={{ flex: '0 0 auto', minHeight: headerH, display: 'flex', alignItems: 'center' }}>
        <h3 style={{ margin: 0 }}>YouTube</h3>
      </div>

      <div
        style={{
          flex: '1 1 auto',
          overflow: 'auto',
          paddingRight: 4,
        }}
      >
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
            gap: 12,
          }}
        >
          {videos.map((v, i) => {
            const url = v.url || (v.videoId ? `https://www.youtube.com/watch?v=${v.videoId}` : '#')
            const thumb =
              v.thumbnail ||
              v.thumbnails?.medium?.url ||
              v.thumbnails?.default?.url ||
              v.snippet?.thumbnails?.medium?.url ||
              ''
            const title = v.title || v.snippet?.title || 'Video'
            const channel = v.channelTitle || v.snippet?.channelTitle || ''

            return (
              <a
                key={v.id || v.videoId || i}
                href={url}
                target="_blank"
                rel="noreferrer"
                className="card"
                style={{ textDecoration: 'none' }}
                title={title}
              >
                {thumb ? (
                  <img
                    src={thumb}
                    alt={title}
                    style={{
                      width: '100%',
                      aspectRatio: '16 / 9',
                      objectFit: 'cover',
                      borderRadius: 8,
                      marginBottom: 8,
                      display: 'block',
                    }}
                    loading="lazy"
                    referrerPolicy="no-referrer"
                  />
                ) : (
                  <div
                    style={{
                      width: '100%',
                      aspectRatio: '16 / 9',
                      background: 'var(--card)',
                      border: '1px solid var(--border)',
                      borderRadius: 8,
                      marginBottom: 8,
                      display: 'grid',
                      placeItems: 'center',
                      color: 'var(--muted)',
                      fontSize: 12,
                    }}
                  >
                    No thumbnail
                  </div>
                )}
                <div style={{ fontWeight: 600, color: 'var(--text)' }}>
                  {title.length > 70 ? title.slice(0, 67) + '…' : title}
                </div>
                {channel && (
                  <div className="muted" style={{ fontSize: 12, marginTop: 2 }}>
                    {channel}
                  </div>
                )}
              </a>
            )
          })}
        </div>
      </div>
    </div>
  )
}
