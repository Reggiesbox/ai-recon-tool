# Project Structure

```
ai-recon-tool/
│
├── README.md                 # Main project documentation
├── LICENSE                   # MIT License
├── CONTRIBUTING.md          # Contribution guidelines
├── .gitignore               # Git ignore rules
├── setup.sh                 # Setup script
│
├── backend/                  # Python FastAPI backend
│   ├── app.py               # Main FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables example
│   │
│   ├── services/            # Service layer
│   │   ├── __init__.py
│   │   ├── netdiscover.py   # Network discovery service
│   │   ├── nmap_scanner.py  # Port scanning service
│   │   ├── metasploit.py    # Metasploit integration
│   │   └── john.py          # John the Ripper integration
│   │
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── network.py       # Network utilities
│
└── frontend/                 # React frontend
    ├── package.json         # Node.js dependencies
    ├── vite.config.js       # Vite configuration
    ├── index.html           # HTML entry point
    │
    └── src/
        ├── main.jsx         # React entry point
        ├── App.jsx          # Main app component
        ├── App.css          # Main app styles
        ├── index.css        # Global styles
        │
        ├── components/      # React components
        │   ├── NetworkDiscovery.jsx
        │   ├── NetworkDiscovery.css
        │   ├── PortScanner.jsx
        │   ├── PortScanner.css
        │   ├── MetasploitExploit.jsx
        │   ├── MetasploitExploit.css
        │   ├── HashCracker.jsx
        │   └── HashCracker.css
        │
        └── services/        # API services
            └── api.js       # Axios API client
```

## Architecture Overview

### Backend (FastAPI)
- **app.py**: Main API server with all endpoints
- **services/**: Business logic for each tool integration
- **utils/**: Helper functions for network operations

### Frontend (React + Vite)
- **Components**: Modular UI components for each feature
- **Services**: API communication layer
- **Styling**: Dark mode theme with cool blues and aqua colors

## Workflow Integration

The tool follows this workflow:

1. **Network Discovery** → Find private IPs using netdiscover
2. **Interface Selection** → Use ifconfig to identify network interface
3. **Port Scanning** → Use nmap to find open ports (vsftpd on port 21)
4. **Exploitation** → Use Metasploit to exploit vulnerabilities
5. **Hash Extraction** → Access shadow file and extract hashes
6. **Hash Cracking** → Use John the Ripper to crack passwords

