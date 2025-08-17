import { Routes, Route } from 'react-router-dom'
import TopNav from './components/TopNav.jsx'
import Home from './pages/Home.jsx'
import History from './pages/History.jsx'
import Admin from './pages/Admin.jsx'

export default function App() {
  return (
    <>
      <TopNav />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/history" element={<History />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </>
  )
}
