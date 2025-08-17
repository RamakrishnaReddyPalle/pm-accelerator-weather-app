export default function WeatherCard({ data }) {
  const name = data?.location?.name || '—'
  const w = data?.weather || {}

  // normalize fields
  const temp = w.main?.temp ?? w.temp ?? '—'
  const feels = w.main?.feels_like ?? w.feels_like ?? '—'
  const humidity = w.main?.humidity ?? w.humidity ?? '—'
  const pressure = w.main?.pressure ?? w.pressure ?? '—'
  const wind = w.wind_speed ?? '—'
  const windDeg = w.wind_deg ?? '—'
  const visibility = w.visibility ?? '—'
  const clouds = w.clouds ?? '—'
  const condition = w.condition || '—'
  const description = w.description || '—'
  const icon = w.icon ? `https://openweathermap.org/img/wn/${w.icon}@2x.png` : null

  return (
    <div className="container">
      <div className="card section">
        <div className="header">
          <h2 style={{margin:0}}>Current weather at <span className="mono">{name}</span></h2>
          {icon && <img src={icon} width={64} height={64} alt={description} title={description} style={{imageRendering:'-webkit-optimize-contrast'}}/>}
        </div>

        <div className="row" style={{alignItems:'baseline'}}>
          <div style={{fontSize:48, fontWeight:700, lineHeight:1}}>{typeof temp === 'number' ? Math.round(temp) : temp}°</div>
          <div className="muted" style={{marginLeft:8}}>{condition} — {description}</div>
        </div>

        <div className="kpi-row">
          <KPI label="Feels like" value={feels} suffix="°" />
          <KPI label="Humidity" value={humidity} suffix="%" />
          <KPI label="Pressure" value={pressure} suffix="hPa" />
          <KPI label="Wind" value={wind} suffix=" m/s" icon={<span style={{display:'inline-block', transform:`rotate(${windDeg||0}deg)`}}>🧭</span>} />
          <KPI label="Visibility" value={visibility} suffix=" m" />
          <KPI label="Clouds" value={clouds} suffix="%" />
        </div>
      </div>
    </div>
  )
}

function KPI({label, value, suffix='', icon=null}) {
  const show = (v) => (typeof v === 'number' ? v : '—')
  return (
    <div className="kpi">
      {icon ?? <span>🌡️</span>}
      <div>
        <div className="muted" style={{fontSize:12}}>{label}</div>
        <div className="mono" style={{fontSize:16, fontWeight:600}}>
          {show(value)}{show(value)!=='—' ? suffix : ''}
        </div>
      </div>
    </div>
  )
}
