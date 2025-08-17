import { useEffect, useState } from 'react'
import { distinctLocations } from '../api/history.js'

const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export default function Admin() {
  const [loc, setLoc] = useState('')
  const [start, setStart] = useState('')
  const [end, setEnd] = useState('')
  const [suggest, setSuggest] = useState([])

  useEffect(() => {
    distinctLocations().then(setSuggest).catch(()=>setSuggest([]))
  }, [])

  const q = new URLSearchParams()
  if (loc) q.set('location_name', loc)
  if (start) q.set('start_date', start)
  if (end) q.set('end_date', end)
  q.set('limit', '50000')
  q.set('skip', '0')

  const href = (fmt) => `${BACKEND}/export/${fmt}?${q.toString()}`

  return (
    <div className="container">
      <div className="card section">
        <div className="header">
          <h2 style={{margin:0}}>Admin / Export</h2>
          <div className="muted">Export weather history</div>
        </div>

        <div className="row" style={{marginBottom:12}}>
          <input className="input" placeholder="Location (optional)" value={loc} onChange={e=>setLoc(e.target.value)} style={{flex:1}}/>
          <input className="input" type="date" value={start} onChange={e=>setStart(e.target.value)} />
          <input className="input" type="date" value={end} onChange={e=>setEnd(e.target.value)} />
        </div>

        {suggest.length > 0 && (
          <div className="muted" style={{marginBottom:12, fontSize:12}}>
            Try:&nbsp;
            {suggest.slice(0,12).map(s => (
              <button key={s} className="btn" style={{marginRight:6}} onClick={()=>setLoc(s)}>{s}</button>
            ))}
          </div>
        )}

        <div className="row">
          <a className="btn primary" href={href('csv')}>Download CSV</a>
          <a className="btn" href={href('json')}>Download JSON</a>
          <a className="btn" href={href('xml')}>Download XML</a>
          <a className="btn" href={href('pdf')}>Download PDF</a>
        </div>
      </div>
    </div>
  )
}
