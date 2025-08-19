// frontend/src/pages/Home.jsx

import React, { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'
import SearchBar from '../components/SearchBar.jsx'
import WeatherCard from '../components/WeatherCard.jsx'
import ForecastList from '../components/ForecastList.jsx'
import MapDisplay from '../components/MapDisplay.jsx'
import YouTubeEmbed from '../components/YouTubeEmbed.jsx'

import { getCurrentWeather, getForecast } from '../api/weather.js'
import { getMapForLocation, getMapByCoords } from '../api/maps.js'
import { getYouTubeForLocation } from '../api/youtube.js'
import { createHistory } from '../api/history.js'
import { useLastSearchStore } from '../store/lastSearch.js'

const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

// Faster defaults: fewer tiles to render, loads quicker
const MAP_W = 640
const MAP_H = 400
const MAP_ZOOM = 13

export default function Home() {
  // global store (persists via localStorage)
  const { current, forecast, map, videos, setAll, hydrateFromLS, saveToLS } = useLastSearchStore()
  // local UI flags
  const [savingPaused, setSavingPaused] = useState(false)
  const [historicalMode, setHistoricalMode] = useState(false)
  const location = useLocation()

  // hydrate store on first mount
  useEffect(() => {
    hydrateFromLS()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // re-save to localStorage whenever data changes (unless paused)
  useEffect(() => {
    if (!savingPaused) saveToLS()
  }, [current, forecast, map, videos, savingPaused, saveToLS])

  // when navigating back from History (no state), show last saved
  useEffect(() => {
    if (!location.state?.historyRecord) {
      setHistoricalMode(false)
      // store already has last values; nothing else to do
    }
  }, [location.pathname, location.state])

  // build "current" from a DB record when coming from History
  const buildCurrentFromRecord = (r) => ({
    source: 'history',
    location: { name: r.location_name, lat: r.latitude, lon: r.longitude },
    weather: r.weather_data || {
      main: { temp: r.temperature, humidity: r.humidity },
      recorded_at: r.recorded_at
    }
  })

  // if navigated with a record, render that snapshot (don’t overwrite store)
  useEffect(() => {
    const rec = location.state?.historyRecord
    if (!rec) return
    setHistoricalMode(true)

    const c = buildCurrentFromRecord(rec)
    const prime = async () => {
      let mapObj = null
      if (typeof rec.latitude === 'number' && typeof rec.longitude === 'number') {
        mapObj = await getMapByCoords(rec.latitude, rec.longitude, { zoom: MAP_ZOOM, width: MAP_W, height: MAP_H, scale: 1 })
      } else if (rec.location_name) {
        mapObj = await getMapForLocation(rec.location_name, { zoom: MAP_ZOOM, width: MAP_W, height: MAP_H, scale: 1 })
      }

      let vids = []
      if (rec.location_name) {
        try {
          const y = await getYouTubeForLocation(rec.location_name, { topic: 'travel', max_results: 6 })
          vids = y.results || []
        } catch {}
      }

      // do NOT update store; show snapshot only
      setAll({ current: c, forecast: null, map: mapObj, videos: vids })
    }
    prime()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.state])

  // normal search flow updates the store (and persists)
  const doSearch = async (payload) => {
    setSavingPaused(true)
    setHistoricalMode(false)
    setAll({ current: null, forecast: null, map: null, videos: [] })

    try {
      const c = await getCurrentWeather(payload)
      const f = await getForecast({ ...payload, days: payload.days ?? 5 })

      // best-effort DB save
      try {
        const name = c?.location?.name || payload.query || 'Unknown'
        const lat = c?.location?.lat
        const lon = c?.location?.lon
        const temp = c?.weather?.main?.temp ?? c?.weather?.temp ?? null
        const hum  = c?.weather?.main?.humidity ?? c?.weather?.humidity ?? null
        if (typeof temp === 'number' && typeof hum === 'number') {
          await createHistory({
            location_name: name,
            latitude: lat,
            longitude: lon,
            start_date: new Date().toISOString().slice(0,10),
            end_date: new Date().toISOString().slice(0,10),
            temperature: temp,
            humidity: hum,
            recorded_at: new Date().toISOString(),
            weather_data: c.weather || null
          })
        }
      } catch {}

      const { lat, lon, name } = c?.location || {}
      let mapObj = null
      let vids = []
      if (typeof lat === 'number' && typeof lon === 'number') {
        const scale = payload.hdMap ? 2 : 1
        mapObj = await getMapByCoords(lat, lon, { zoom: MAP_ZOOM, width: MAP_W, height: MAP_H, scale })
        try {
          const y = await getYouTubeForLocation(name || payload.query || `${lat},${lon}`, {
            topic: 'travel', max_results: payload.videoCount ?? 6
          })
          vids = y.results || []
        } catch {}
      }

      setAll({ current: c, forecast: f, map: mapObj, videos: vids })
    } catch (e) {
      alert(`Search failed: ${e?.response?.data?.detail || e.message}`)
    } finally {
      setSavingPaused(false)
    }
  }

  const useGeolocate = () => {
    if (!navigator.geolocation) return alert('Geolocation not supported')
    navigator.geolocation.getCurrentPosition(
      ({coords}) => doSearch({ lat: coords.latitude, lon: coords.longitude, units:'metric', days:5, videoCount:6, hdMap:false }),
      (err) => alert('Geolocation error: ' + err.message),
      { enableHighAccuracy: true, timeout: 10000 }
    )
  }

  const coords = current?.location?.lat && current?.location?.lon
    ? { lat: current.location.lat, lon: current.location.lon }
    : null

  return (
    <>
      {historicalMode && (
        <div className="container">
          <div className="card section" style={{borderColor:'var(--accent)'}}>
            Viewing a <b>saved record</b>{' '}
            {current?.weather?.recorded_at && <>from <code>{new Date(current.weather.recorded_at).toLocaleString()}</code></>}
            . Use Search to fetch live data.
          </div>
        </div>
      )}

      <SearchBar onSearch={doSearch} onGeolocate={useGeolocate} />
      <WeatherCard data={current} />
      <ForecastList data={forecast} coords={coords} backendBase={BACKEND} />

      <div className="container">
        <div className="grid-2">
          <MapDisplay map={map} height={MAP_H} />
          <YouTubeEmbed videos={videos} height={MAP_H} />
        </div>
      </div>
    </>
  )
}
