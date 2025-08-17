import { NavLink } from 'react-router-dom'
import { useEffect, useState } from 'react'

export default function TopNav() {
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'dark')

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  return (
    <div className="nav">
      <div className="nav-inner">
        <div className="brand">
          <span style={{fontSize:18}}>PM Accelerator – Ram</span>
          <span className="badge">Weather</span>
        </div>

        <div className="nav-links">
          <NavLink to="/" end>Home</NavLink>
          <NavLink to="/history">History</NavLink>
          <NavLink to="/admin">Admin/Export</NavLink>
        </div>

        <div className="toggle" onClick={()=>setTheme(t=> t==='dark' ? 'light' : 'dark')}>
          <span style={{opacity:.8}}>Theme</span>
          <span className="badge" aria-label="Toggle theme">
            {theme === 'dark' ? 'Dark' : 'Light'}
          </span>
        </div>
      </div>
    </div>
  )
}
