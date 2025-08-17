// src/store/lastSearch.js
import { create } from 'zustand'

const LS_KEY = 'weather:last'

export const useLastSearchStore = create((set, get) => ({
  current: null,
  forecast: null,
  map: null,
  videos: [],

  setAll: (payload) => set(payload),
  clear: () => set({ current: null, forecast: null, map: null, videos: [] }),

  hydrateFromLS: () => {
    try {
      const raw = localStorage.getItem(LS_KEY)
      if (!raw) return
      const data = JSON.parse(raw)
      set({
        current: data.current ?? null,
        forecast: data.forecast ?? null,
        map: data.map ?? null,
        videos: data.videos ?? [],
      })
    } catch {}
  },

  saveToLS: () => {
    const { current, forecast, map, videos } = get()
    try {
      localStorage.setItem(LS_KEY, JSON.stringify({ current, forecast, map, videos }))
    } catch {}
  },
}))
