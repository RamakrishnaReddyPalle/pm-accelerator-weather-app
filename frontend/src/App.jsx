// src/App.jsx

import { Routes, Route } from 'react-router-dom'
import { useEffect, useState } from 'react'
import TopNav from './components/TopNav.jsx'
import Home from './pages/Home.jsx'
import History from './pages/History.jsx'
import Admin from './pages/Admin.jsx'

export default function App() {
  // optional global theme handling (safe if TopNav ignores props)
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light')
  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem('theme', theme)
  }, [theme])
  const toggleTheme = () => setTheme(t => (t === 'dark' ? 'light' : 'dark'))

  return (
    <>
      {/* If your TopNav supports these props, great; otherwise it’ll just ignore them */}
      <TopNav theme={theme} onToggleTheme={toggleTheme} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/history" element={<History />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </>
  )
}
