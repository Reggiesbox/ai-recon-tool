import React, { useState } from 'react'
import { Key, FileText, Loader, AlertCircle, CheckCircle } from 'lucide-react'
import { apiService } from '../services/api'
import './HashCracker.css'

function HashCracker() {
  const [hashFile, setHashFile] = useState('hashes.txt')
  const [wordlist, setWordlist] = useState('/usr/share/wordlists/rockyou.txt')
  const [loading, setLoading] = useState(false)
  const [cracked, setCracked] = useState([])
  const [error, setError] = useState(null)

  const handleCrack = async () => {
    if (!hashFile.trim()) {
      setError('Please enter a hash file path')
      return
    }

    setLoading(true)
    setError(null)
    setCracked([])

    try {
      const response = await apiService.crackHashes({
        hash_file: hashFile.trim(),
        wordlist: wordlist.trim() || null
      })

      if (response.data.success) {
        // Start polling for results
        setTimeout(() => checkStatus(), 5000)
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Hash cracking failed')
      setLoading(false)
    }
  }

  const checkStatus = async () => {
    try {
      const response = await apiService.getCrackStatus(hashFile)
      setCracked(response.data.cracked_passwords || [])
      setLoading(false)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get status')
      setLoading(false)
    }
  }

  return (
    <div className="hash-cracker">
      <div className="section-header">
        <Key size={24} />
        <h2>Hash Cracking</h2>
      </div>

      <div className="cracker-panel">
        <div className="form-group">
          <label>
            <FileText size={18} />
            Hash File Path
          </label>
          <input
            type="text"
            value={hashFile}
            onChange={(e) => setHashFile(e.target.value)}
            placeholder="hashes.txt"
            className="input-field"
          />
        </div>

        <div className="form-group">
          <label>Wordlist (Optional)</label>
          <input
            type="text"
            value={wordlist}
            onChange={(e) => setWordlist(e.target.value)}
            placeholder="/usr/share/wordlists/rockyou.txt"
            className="input-field"
          />
        </div>

        <button
          onClick={handleCrack}
          disabled={loading}
          className="primary-button"
        >
          {loading ? (
            <>
              <Loader className="spinner" size={20} />
              Cracking...
            </>
          ) : (
            <>
              <Key size={20} />
              Start Cracking
            </>
          )}
        </button>

        <button
          onClick={checkStatus}
          className="secondary-button"
        >
          Check Status
        </button>

        {error && (
          <div className="error-message">
            <AlertCircle size={20} />
            {error}
          </div>
        )}
      </div>

      {cracked.length > 0 && (
        <div className="results-panel">
          <div className="results-header">
            <h3>Cracked Passwords ({cracked.length})</h3>
            <CheckCircle size={20} className="success-icon" />
          </div>

          <div className="cracked-list">
            {cracked.map((item, index) => (
              <div key={index} className="cracked-item">
                <div className="cracked-username">{item.username}</div>
                <div className="cracked-password">{item.password || 'No password found'}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default HashCracker

