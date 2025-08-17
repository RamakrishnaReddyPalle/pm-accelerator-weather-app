import { useEffect, useRef, useState } from 'react'
import { searchLocations } from '../api/location.js'

export default function SearchBar({ onSearch, onGeolocate }) {
  const [query, setQuery] = useState('')
  const [units, setUnits] = useState('metric')
  const [days, setDays] = useState(5)
  const [videoCount, setVideoCount] = useState(6)
  const [hdMap, setHdMap] = useState(false)

  const [open, setOpen] = useState(false)
  const [suggestions, setSuggestions] = useState([])
  const boxRef = useRef(null)
  const debounceRef = useRef(0)

  useEffect(() => {
    const onDoc = (e) => {
      if (!boxRef.current?.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', onDoc)
    return () => document.removeEventListener('mousedown', onDoc)
  }, [])

  const onType = (val) => {
    setQuery(val)
    if (debounceRef.current) clearTimeout(debounceRef.current)
    if (val.trim().length < 2) { setSuggestions([]); setOpen(false); return }
    debounceRef.current = setTimeout(async () => {
      try {
        const list = await searchLocations(val.trim())
        setSuggestions(list.slice(0, 6))
        setOpen(true)
      } catch {
        setSuggestions([]); setOpen(false)
      }
    }, 250)
  }

  const choose = (c) => {
    const formatted = c.formatted || c.name || query
    setQuery(formatted)
    setOpen(false)
  }

  const submit = (e) => {
    e.preventDefault()
    if (!query.trim()) return
    onSearch({ query: query.trim(), units, days, videoCount, hdMap })
  }

  return (
    <form onSubmit={submit} className="container" style={{marginTop: 16}}>
      <div className="card section" ref={boxRef}>
        <div className="row">
          <div style={{position:'relative', flex: 1, minWidth: 240}}>
            <input
              className="input"
              placeholder="Search city, landmark, ZIP…"
              value={query}
              onChange={e => onType(e.target.value)}
              onFocus={() => query.length >= 2 && setOpen(true)}
            />
            {open && suggestions.length > 0 && (
              <div style={{
                position:'absolute', top:'100%', left:0, right:0, zIndex:10,
                background:'var(--panel)', border:'1px solid var(--border)', borderRadius: 12, marginTop: 6,
                boxShadow:'var(--shadow)', maxHeight: 260, overflow:'auto'
              }}>
                {suggestions.map((s, i) => (
                  <div key={i}
                    onMouseDown={() => choose(s)}
                    style={{padding:'10px 12px', cursor:'pointer', borderBottom:'1px solid var(--border)'}}
                  >
                    {s.formatted}
                  </div>
                ))}
              </div>
            )}
          </div>

          <select className="select" value={units} onChange={e=>setUnits(e.target.value)}>
            <option value="metric">Metric (°C)</option>
            <option value="imperial">Imperial (°F)</option>
            <option value="standard">Standard (K)</option>
          </select>

          <label className="row" style={{gap:6}}>
            Days:
            <select className="select" value={days} onChange={e=>setDays(parseInt(e.target.value))}>
              {[1,2,3,4,5].map(d => <option key={d} value={d}>{d}</option>)}
            </select>
          </label>

          <label className="row" style={{gap:6}}>
            Videos:
            <select className="select" value={videoCount} onChange={e=>setVideoCount(parseInt(e.target.value))}>
              {[0,3,6,9,12].map(n => <option key={n} value={n}>{n}</option>)}
            </select>
          </label>

          <label className="row" style={{gap:6}}>
            HD Map
            <input type="checkbox" checked={hdMap} onChange={e=>setHdMap(e.target.checked)} />
          </label>

          <button type="submit" className="btn primary">Search</button>
          <button type="button" className="btn ghost" onClick={onGeolocate}>Use My Location</button>
        </div>
      </div>
    </form>
  )
}
