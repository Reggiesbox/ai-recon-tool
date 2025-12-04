import React, { useState } from 'react'
import { Scan, Target, Loader, AlertCircle, CheckCircle } from 'lucide-react'
import { apiService } from '../services/api'
import './PortScanner.css'

function PortScanner() {
  const [target, setTarget] = useState('')
  const [ports, setPorts] = useState('21,22,80,443')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const handleScan = async () => {
    if (!target.trim()) {
      setError('Please enter a target IP address')
      return
    }

    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const response = await apiService.scanPorts({
        target: target.trim(),
        ports: ports.trim(),
        scan_type: 'syn'
      })
      setResults(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Port scan failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="port-scanner">
      <div className="section-header">
        <Scan size={24} />
        <h2>Port Scanner</h2>
      </div>

      <div className="scanner-panel">
        <div className="form-group">
          <label>
            <Target size={18} />
            Target IP Address
          </label>
          <input
            type="text"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="192.168.1.100"
            className="input-field"
          />
        </div>

        <div className="form-group">
          <label>Ports to Scan</label>
          <input
            type="text"
            value={ports}
            onChange={(e) => setPorts(e.target.value)}
            placeholder="21,22,80,443 or 1-1000"
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
              <Scan size={20} />
              Start Scan
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

      {results && (
        <div className="results-panel">
          <div className="results-header">
            <h3>Scan Results</h3>
            <div className="results-summary">
              <span className="summary-item">
                Target: <strong>{results.target}</strong>
              </span>
              <span className="summary-item">
                Open Ports: <strong className="success-text">{results.open_ports_count}</strong>
              </span>
              {results.vsftpd_detected && (
                <span className="summary-item vsftpd-badge">
                  <CheckCircle size={16} />
                  vsftpd Detected
                </span>
              )}
            </div>
          </div>

          {results.ports && results.ports.length > 0 && (
            <div className="ports-list">
              {results.ports.map((port, index) => (
                <div
                  key={index}
                  className={`port-item ${port.state === 'open' ? 'open' : ''}`}
                >
                  <div className="port-info">
                    <span className="port-number">Port {port.number}</span>
                    <span className={`port-state ${port.state}`}>
                      {port.state.toUpperCase()}
                    </span>
                  </div>
                  {port.service && (
                    <div className="port-service">
                      Service: <strong>{port.service}</strong>
                      {port.product && ` (${port.product})`}
                      {port.version && ` ${port.version}`}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default PortScanner

