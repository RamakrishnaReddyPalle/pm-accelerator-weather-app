import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { listAllHistory, updateHistory, deleteHistory, distinctLocations } from '../api/history.js'

export default function History() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [q, setQ] = useState('')
  const [suggest, setSuggest] = useState([])
  const nav = useNavigate()

  const load = async () => {
    setLoading(true)
    try {
      const data = await listAllHistory(50000) // show all
      setItems(data)
      try { setSuggest(await distinctLocations()) } catch {}
    } catch (e) {
      alert('Load failed: ' + (e?.response?.data?.detail || e.message))
    } finally {
      setLoading(false)
    }
  }
  useEffect(() => { load() }, [])

  const filtered = useMemo(() => {
    const s = q.trim().toLowerCase()
    if (!s) return items
    return items.filter(r =>
      (r.location_name || '').toLowerCase().includes(s) ||
      String(r.id).includes(s)
    )
  }, [items, q])

  const onUpdate = async (id) => {
    const temperature = prompt('New temperature (leave blank to skip):')
    const humidity = prompt('New humidity (leave blank to skip):')
    const payload = {}
    if (temperature) payload.temperature = parseFloat(temperature)
    if (humidity) payload.humidity = parseFloat(humidity)
    if (!Object.keys(payload).length) return
    try {
      await updateHistory(id, payload)
      await load()
    } catch (e) {
      alert('Update failed: ' + (e?.response?.data?.detail || e.message))
    }
  }

  const onDelete = async (id) => {
    if (!confirm('Delete this record?')) return
    try {
      await deleteHistory(id)
      await load()
    } catch (e) {
      alert('Delete failed: ' + (e?.response?.data?.detail || e.message))
    }
  }

  return (
    <div className="container">
      <div className="card section">
        <div className="header">
          <h2 style={{margin:0}}>History</h2>
          {loading && <div className="muted">Loading…</div>}
        </div>

        <div className="row" style={{marginBottom:10, alignItems:'center'}}>
          <input className="input" placeholder="Filter by location or ID…" value={q} onChange={e=>setQ(e.target.value)} style={{flex:1}}/>
          {suggest.length > 0 && (
            <div className="muted" style={{fontSize:12}}>
              Suggestions:&nbsp;
              {suggest.slice(0,8).map(s => (
                <button key={s} className="btn" style={{marginRight:6}} onClick={()=>setQ(s)}>{s}</button>
              ))}
            </div>
          )}
        </div>

        <div style={{overflowX:'auto'}}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{borderBottom:'1px solid var(--border)'}}>
                {['ID','Location','Start','End','Temp','Humidity','Recorded At','Actions'].map(h => (
                  <th key={h} style={{ textAlign:'left', padding: 8, color:'var(--muted)' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map(r => (
                <tr key={r.id} style={{ borderBottom:'1px solid var(--border)' }}>
                  <td style={{ padding: 8, whiteSpace:'nowrap' }}>
                    <button className="btn" onClick={()=>nav('/', { state: { historyRecord: r }})} title="Open snapshot in Home">
                      #{r.id}
                    </button>
                  </td>
                  <td style={{ padding: 8 }}>{r.location_name || '—'}</td>
                  <td style={{ padding: 8 }}>{r.start_date || '—'}</td>
                  <td style={{ padding: 8 }}>{r.end_date || '—'}</td>
                  <td style={{ padding: 8 }}>{r.temperature ?? '—'}</td>
                  <td style={{ padding: 8 }}>{r.humidity ?? '—'}</td>
                  <td style={{ padding: 8 }}>
                    {r.recorded_at ? new Date(r.recorded_at).toLocaleString() : '—'}
                  </td>
                  <td style={{ padding: 8, whiteSpace:'nowrap' }}>
                    <button className="btn" onClick={()=>onUpdate(r.id)} style={{ marginRight: 6 }}>Update</button>
                    <button className="btn" onClick={()=>onDelete(r.id)}>Delete</button>
                  </td>
                </tr>
              ))}
              {!filtered.length && (
                <tr><td colSpan={8} style={{ padding: 12, color: 'var(--muted)' }}>No matching records</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
