// src/App.jsx

import { Routes, Route } from 'react-router-dom'
import { useEffect, useState } from 'react'
import TopNav from './components/TopNav.jsx'
import Home from './pages/Home.jsx'
import History from './pages/History.jsx'
import Admin from './pages/Admin.jsx'

export default function App() {
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light')
  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem('theme', theme)
  }, [theme])
  const toggleTheme = () => setTheme(t => (t === 'dark' ? 'light' : 'dark'))

  return (
    <>
      {}
      <TopNav theme={theme} onToggleTheme={toggleTheme} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/history" element={<History />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </>
  )
}
