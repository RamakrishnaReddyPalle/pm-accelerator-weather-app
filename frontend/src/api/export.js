import api from './axios'

// helpers for download
const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  window.URL.revokeObjectURL(url)
}

// CSV / JSON / XML / PDF
export const exportCSV = async (params) => {
  const { data } = await api.get('/export/csv', { params, responseType: 'blob' })
  downloadBlob(data, 'weather_history.csv')
}
export const exportJSON = async (params) => {
  const { data } = await api.get('/export/json', { params, responseType: 'blob' })
  downloadBlob(data, 'weather_history.json')
}
export const exportXML = async (params) => {
  const { data } = await api.get('/export/xml', { params, responseType: 'blob' })
  downloadBlob(data, 'weather_history.xml')
}
export const exportPDF = async (params) => {
  const { data } = await api.get('/export/pdf', { params, responseType: 'blob' })
  downloadBlob(data, 'weather_history.pdf')
}
