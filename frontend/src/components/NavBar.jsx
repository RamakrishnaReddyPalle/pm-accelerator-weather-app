// frontend/src/components/NavBar.jsx

import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'

export default function NavBar({ theme, onToggleTheme }) {
  const [open, setOpen] = useState(false)

  return (
    <header className="topbar">
      <div className="container topbar__inner">
        {/* Left: Hamburger (mobile) + Title */}
        <div className="topbar__left">
          <button
            className="iconbtn topbar__burger"
            aria-label="Open menu"
            onClick={()=>setOpen(o=>!o)}
          >
            {/* simple hamburger */}
            <span className="burger-lines" />
          </button>
          <Link to="/" className="topbar__brand">
            PM Accelerator – Ram
          </Link>
        </div>

        {/* Right: Theme + Desktop Menu */}
        <div className="topbar__right">
          <button
            className="iconbtn"
            aria-label="Toggle theme"
            title="Toggle theme"
            onClick={onToggleTheme}
          >
            {/* sun/moon glyph via emoji for simplicity */}
            <span role="img" aria-label="theme">{theme === 'dark' ? '🌙' : '☀️'}</span>
          </button>

          <nav className="topbar__menu topbar__menu--desktop">
            <NavLink to="/" end className="topbar__link">Home</NavLink>
            <NavLink to="/history" className="topbar__link">History</NavLink>
            <NavLink to="/admin" className="topbar__link">Admin/Export</NavLink>
          </nav>
        </div>
      </div>

      {/* Mobile dropdown */}
      {open && (
        <nav className="topbar__menu topbar__menu--mobile container">
          <NavLink to="/" end className="topbar__link" onClick={()=>setOpen(false)}>Home</NavLink>
          <NavLink to="/history" className="topbar__link" onClick={()=>setOpen(false)}>History</NavLink>
          <NavLink to="/admin" className="topbar__link" onClick={()=>setOpen(false)}>Admin/Export</NavLink>
        </nav>
      )}
    </header>
  )
}
