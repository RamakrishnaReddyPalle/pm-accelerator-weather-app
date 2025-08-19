// frontend/src/components/ForecastList.jsx

export default function ForecastList({ data }) {
  const name = data?.location?.name || '—'
  const list = data?.forecast || []

  return (
    <div className="container">
      <div className="card section">
        <div className="header">
          <h3 style={{margin:0}}>Forecast: <span className="mono">{name}</span></h3>
          <div className="muted">{list.length} day(s)</div>
        </div>

        <div className="scroll-x">
          {list.length === 0 ? (
            <div className="skeleton" style={{height:120, minWidth:180, borderRadius:12}}/>
          ) : list.map((d, idx) => <DayCard key={idx} d={d} />)}
        </div>
      </div>
    </div>
  )
}

function DayCard({ d }) {
  const icon = d.icon ? `https://openweathermap.org/img/wn/${d.icon}.png` : null
  return (
    <div className="forecast-card">
      <div className="muted mono" style={{fontSize:12}}>{d.date}</div>
      <div style={{display:'flex', alignItems:'center', gap:10, marginTop:6}}>
        {icon && <img src={icon} width={36} height={36} alt={d.description} />}
        <div style={{fontWeight:700}}>{Math.round(d.temp)}°</div>
      </div>
      <div className="muted" style={{marginTop:6, fontSize:13}}>{d.condition} — {d.description}</div>

      <div className="row" style={{gap:8, marginTop:10}}>
        <Chip label="Feels" v={d.feels_like} s="°" />
        <Chip label="Hum" v={d.humidity} s="%" />
        <Chip label="Wind" v={d.wind_speed} s=" m/s" />
        <Chip label="Clouds" v={d.clouds} s="%" />
      </div>
    </div>
  )
}
function Chip({label, v, s=''}) {
  const show = typeof v === 'number' ? v : '—'
  return (
    <div className="muted" style={{fontSize:12, border:'1px solid var(--border)', padding:'4px 8px', borderRadius:999}}>
      {label}: <span className="mono">{show}</span>{show!=='—'? s : ''}
    </div>
  )
}
