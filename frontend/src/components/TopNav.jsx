// frontend/src/components/TopNav.jsx

import { NavLink, useLocation } from 'react-router-dom'
import { useEffect, useState } from 'react'

export default function TopNav() {
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'dark')
  const [open, setOpen] = useState(false)
  const location = useLocation()

  // Apply theme
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  // Close mobile menu on route change
  useEffect(() => { setOpen(false) }, [location.pathname])

  // Close on ESC
  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') setOpen(false) }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  // Close menu if we resize to desktop
  useEffect(() => {
    const onResize = () => {
      if (window.innerWidth >= 900) setOpen(false)
    }
    window.addEventListener('resize', onResize)
    return () => window.removeEventListener('resize', onResize)
  }, [])

  return (
    <div className={`nav ${open ? 'nav--open' : ''}`}>
      <div className="nav-inner">
        {/* Hamburger (shows on mobile via CSS) */}
        <button
          className="hamburger"
          aria-label="Toggle navigation menu"
          onClick={() => setOpen(v => !v)}
        >
          {/* Simple menu icon */}
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
        </button>

        {/* Brand */}
        <div className="brand">
          <span style={{fontSize:18}}>PM Accelerator – Ram</span>
          <span className="badge">Weather</span>
        </div>

        {/* Links (collapse on mobile; CSS shows when .nav--open) */}
        <div className="nav-links">
          <NavLink to="/" end>Home</NavLink>
          <NavLink to="/history">History</NavLink>
          <NavLink to="/admin">Admin/Export</NavLink>
        </div>

        {/* Theme toggle */}
        <button
          className="toggle"
          onClick={()=>setTheme(t=> t==='dark' ? 'light' : 'dark')}
          aria-label="Toggle theme"
          title="Toggle theme"
        >
          <span style={{opacity:.8, display:'inline-flex', alignItems:'center', gap:6}}>
            {/* sun/moon icon hint */}
            {theme === 'dark' ? (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M21 12a9 9 0 1 1-9-9 7 7 0 0 0 9 9Z" stroke="currentColor" strokeWidth="2"/>
              </svg>
            ) : (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <circle cx="12" cy="12" r="5" stroke="currentColor" strokeWidth="2"/>
                <path d="M12 1v3M12 20v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M1 12h3M20 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"
                      stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            )}
            <span className="badge" style={{marginLeft:4}}>{theme === 'dark' ? 'Dark' : 'Light'}</span>
          </span>
        </button>
      </div>
    </div>
  )
}
