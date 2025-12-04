import React, { useState, useEffect } from 'react'
import NetworkDiscovery from './components/NetworkDiscovery'
import PortScanner from './components/PortScanner'
import MetasploitExploit from './components/MetasploitExploit'
import HashCracker from './components/HashCracker'
import { Terminal, Network, Shield, Key } from 'lucide-react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('network')

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <Shield size={32} />
            <h1>AI Reconnaissance Tool</h1>
          </div>
          <p className="subtitle">Advanced Penetration Testing Interface</p>
        </div>
      </header>

      <nav className="tab-navigation">
        <button
          className={`tab-button ${activeTab === 'network' ? 'active' : ''}`}
          onClick={() => setActiveTab('network')}
        >
          <Network size={20} />
          Network Discovery
        </button>
        <button
          className={`tab-button ${activeTab === 'scan' ? 'active' : ''}`}
          onClick={() => setActiveTab('scan')}
        >
          <Terminal size={20} />
          Port Scanner
        </button>
        <button
          className={`tab-button ${activeTab === 'exploit' ? 'active' : ''}`}
          onClick={() => setActiveTab('exploit')}
        >
          <Shield size={20} />
          Exploitation
        </button>
        <button
          className={`tab-button ${activeTab === 'crack' ? 'active' : ''}`}
          onClick={() => setActiveTab('crack')}
        >
          <Key size={20} />
          Hash Cracking
        </button>
      </nav>

      <main className="main-content">
        {activeTab === 'network' && <NetworkDiscovery />}
        {activeTab === 'scan' && <PortScanner />}
        {activeTab === 'exploit' && <MetasploitExploit />}
        {activeTab === 'crack' && <HashCracker />}
      </main>

      <footer className="app-footer">
        <p>⚠️ For authorized security testing only. Use responsibly.</p>
      </footer>
    </div>
  )
}

export default App

