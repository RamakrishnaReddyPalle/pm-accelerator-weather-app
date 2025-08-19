// src/store/lastSearch.js

import { create } from 'zustand'

const LS_KEY = 'weather:last' // keep the key; we’ll just store in sessionStorage now

export const useLastSearchStore = create((set, get) => ({
  current: null,
  forecast: null,
  map: null,
  videos: [],

  setAll: (payload) => set(payload),
  clear: () => set({ current: null, forecast: null, map: null, videos: [] }),

  // Read from sessionStorage (not localStorage). If nothing is there,
  // the page loads empty on first open. That’s exactly what we want.
  hydrateFromLS: () => {
    try {
      // one-time cleanup of legacy localStorage so it never autoloads again
      if (typeof localStorage !== 'undefined' && localStorage.getItem(LS_KEY)) {
        localStorage.removeItem(LS_KEY)
      }

      const raw =
        typeof sessionStorage !== 'undefined'
          ? sessionStorage.getItem(LS_KEY)
          : null
      if (!raw) return

      const data = JSON.parse(raw)
      set({
        current: data.current ?? null,
        forecast: data.forecast ?? null,
        map: data.map ?? null,
        videos: data.videos ?? [],
      })
    } catch {
      // ignore parse/storage errors
    }
  },

  // Save to sessionStorage so the data survives refresh and route changes,
  // but disappears when the tab/window is closed.
  saveToLS: () => {
    const { current, forecast, map, videos } = get()
    try {
      if (typeof sessionStorage !== 'undefined') {
        sessionStorage.setItem(
          LS_KEY,
          JSON.stringify({ current, forecast, map, videos })
        )
      }
    } catch {
      // ignore quota/storage errors
    }
  },
}))
