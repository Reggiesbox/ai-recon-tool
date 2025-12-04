import React, { useState, useEffect } from 'react'
import { Search, Wifi, Loader, CheckCircle, AlertCircle } from 'lucide-react'
import { apiService } from '../services/api'
import './NetworkDiscovery.css'

function NetworkDiscovery() {
  const [interfaces, setInterfaces] = useState([])
  const [selectedInterface, setSelectedInterface] = useState('')
  const [ipRange, setIpRange] = useState('192.168.1.0/24')
  const [loading, setLoading] = useState(false)
  const [hosts, setHosts] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    loadInterfaces()
  }, [])

  const loadInterfaces = async () => {
    try {
      const response = await apiService.getNetworkInterfaces()
      setInterfaces(response.data.interfaces)
      if (response.data.interfaces.length > 0) {
        setSelectedInterface(response.data.interfaces[0].name)
      }
    } catch (err) {
      setError('Failed to load network interfaces')
    }
  }

  const handleScan = async () => {
    setLoading(true)
    setError(null)
    setHosts([])

    try {
      const response = await apiService.discoverNetwork({
        interface: selectedInterface,
        range: ipRange
      })
      setHosts(response.data.hosts || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Network discovery failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="network-discovery">
      <div className="section-header">
        <Wifi size={24} />
        <h2>Network Discovery</h2>
      </div>

      <div className="discovery-panel">
        <div className="form-group">
          <label>Network Interface</label>
          <select
            value={selectedInterface}
            onChange={(e) => setSelectedInterface(e.target.value)}
            className="input-field"
          >
            {interfaces.map((iface) => (
              <option key={iface.name} value={iface.name}>
                {iface.name} {iface.ip ? `(${iface.ip})` : ''}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>IP Range</label>
          <input
            type="text"
            value={ipRange}
            onChange={(e) => setIpRange(e.target.value)}
            placeholder="192.168.1.0/24"
            className="input-field"
          />
        </div>

        <button
          onClick={handleScan}
          disabled={loading}
          className="primary-button"
        >
          {loading ? (
            <>
              <Loader className="spinner" size={20} />
              Scanning...
            </>
          ) : (
            <>
              <Search size={20} />
              Start Discovery
            </>
          )}
        </button>

        {error && (
          <div className="error-message">
            <AlertCircle size={20} />
            {error}
          </div>
        )}
      </div>

      {hosts.length > 0 && (
        <div className="results-panel">
          <h3>Discovered Hosts ({hosts.length})</h3>
          <div className="hosts-grid">
            {hosts.map((host, index) => (
              <div key={index} className="host-card">
                <div className="host-header">
                  <CheckCircle size={18} className="success-icon" />
                  <span className="host-ip">{host.ip}</span>
                </div>
                <div className="host-details">
                  <div className="detail-item">
                    <span className="detail-label">MAC:</span>
                    <span className="detail-value">{host.mac}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Vendor:</span>
                    <span className="detail-value">{host.vendor}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default NetworkDiscovery

