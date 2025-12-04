import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const apiService = {
  // Network interfaces
  getNetworkInterfaces: () => api.get('/api/network/interfaces'),

  // Network discovery
  discoverNetwork: (data) => api.post('/api/network/discover', data),

  // Port scanning
  scanPorts: (data) => api.post('/api/nmap/scan', data),

  // Metasploit
  searchExploits: (query) => api.get('/api/metasploit/search', { params: { query } }),
  executeExploit: (data) => api.post('/api/metasploit/exploit', data),
  listSessions: () => api.get('/api/metasploit/sessions'),
  executeCommand: (sessionId, command) =>
    api.post('/api/metasploit/command', null, {
      params: { session_id: sessionId, command }
    }),
  extractHashes: (data) => api.post('/api/hashes/extract', data),

  // John the Ripper
  crackHashes: (data) => api.post('/api/john/crack', data),
  getCrackStatus: (hashFile) => api.get(`/api/john/status/${hashFile}`)
}

export default api

