# AI Reconnaissance Tool - Web Interface

A modern, dark-mode web interface for penetration testing and reconnaissance operations. This tool provides an intuitive interface for network discovery, port scanning, exploitation, and hash cracking.

## ⚠️ Legal Disclaimer

**This tool is for authorized security testing and educational purposes only.** Unauthorized access to computer systems is illegal. Users are responsible for ensuring they have proper authorization before using this tool.

## Features

- 🌐 **Network Discovery**: Automated private IP address discovery using netdiscover
- 🔍 **Port Scanning**: Nmap integration for comprehensive port scanning
- 🎯 **Exploitation**: Metasploit integration for vulnerability exploitation
- 🔐 **Hash Cracking**: John the Ripper integration for password hash analysis
- 🎨 **Modern UI**: Dark mode interface with cool blue and aqua color scheme
- 🤖 **AI-Powered**: Intelligent workflow automation and recommendations

## Prerequisites

- **VMware Workstation/Player** with a Linux VM (Kali Linux recommended)
- **Kali Linux** or similar penetration testing distribution installed in the VM
- Python 3.9+
- Node.js 18+
- Required tools installed:
  - `netdiscover`
  - `nmap`
  - `metasploit-framework`
  - `john` (John the Ripper)
  - `ifconfig` (net-tools)

## VMware Setup

> 📖 **Detailed Setup Guide**: See [VMWARE_SETUP.md](VMWARE_SETUP.md) for comprehensive VMware configuration instructions.

### VM Network Configuration

For proper network discovery and scanning, configure your VM network adapter:

1. **VMware Network Settings**:
   - Open VM Settings → Network Adapter
   - Select **Bridged** mode (recommended) or **NAT** mode
   - Bridged mode allows direct access to your physical network
   - NAT mode isolates the VM but still allows network access

2. **VM Network Interface**:
   ```bash
   # Check available interfaces
   ifconfig
   
   # Or use ip command
   ip addr show
   
   # Typically eth0 or ens33 in VMware
   ```

3. **Firewall Configuration** (if needed):
   ```bash
   # Allow API access (if firewall is active)
   sudo ufw allow 8000/tcp
   sudo ufw allow 5173/tcp
   ```

### Accessing from Host Machine

If you want to access the web interface from your host machine:

1. **Find VM IP Address**:
   ```bash
   ifconfig | grep inet
   # Note the IP address (e.g., 192.168.1.105)
   ```

2. **Update Frontend API URL** (if accessing from host):
   - Create `frontend/.env` file:
     ```
     VITE_API_URL=http://VM_IP_ADDRESS:8000
     ```
   - Replace `VM_IP_ADDRESS` with your VM's IP

3. **Start Services**:
   - Backend binds to `0.0.0.0:8000` (accessible from host)
   - Frontend runs on `localhost:5173` (use port forwarding if needed)

## Installation

### 1. Clone the Repository (Inside VM)

```bash
# Inside your VMware Linux VM
git clone https://github.com/yourusername/ai-recon-tool.git
cd ai-recon-tool
```

### 2. Install System Dependencies (Kali Linux)

```bash
# Update package list
sudo apt update

# Install required tools
sudo apt install -y netdiscover nmap metasploit-framework john net-tools

# Install Python and Node.js if not already installed
sudo apt install -y python3 python3-pip python3-venv nodejs npm
```

### 3. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Frontend Setup

```bash
cd ../frontend
npm install
```

### 5. Quick Setup (Alternative)

Use the provided setup script:

```bash
chmod +x setup.sh
./setup.sh
```

## Usage

### Start the Backend Server

```bash
cd backend
source venv/bin/activate
python app.py
```

The API will be available at:
- **Inside VM**: `http://localhost:8000`
- **From Host**: `http://VM_IP_ADDRESS:8000` (if using bridged networking)

### Start the Frontend Development Server

```bash
cd frontend
npm run dev
```

The web interface will be available at:
- **Inside VM**: `http://localhost:5173`
- **From Host**: Requires port forwarding or use VM's IP if configured

### Accessing from Host Machine

To access the web interface from your Windows/Mac host:

1. **Option 1: Use VM's IP Address**
   - Find VM IP: `ifconfig | grep inet`
   - Access: `http://VM_IP:5173` (if frontend is configured for external access)

2. **Option 2: Use SSH Port Forwarding**
   ```bash
   # On host machine
   ssh -L 5173:localhost:5173 -L 8000:localhost:8000 user@VM_IP
   # Then access http://localhost:5173 on host
   ```

3. **Option 3: Use VMware NAT Port Forwarding**
   - VM Settings → Network Adapter → NAT Settings → Port Forwarding
   - Add rules for ports 8000 and 5173

## Workflow

1. **Network Discovery**: Use netdiscover to find all private IP addresses on the network
2. **Network Configuration**: Use ifconfig to identify and configure the correct network interface
3. **Port Scanning**: Run nmap scans to identify open ports (specifically targeting vsftpd on port 21)
4. **Exploitation**: Use Metasploit to search for exploits, set target hosts, and execute exploits
5. **Hash Extraction**: Access the shadow file, extract password hashes, and clean the data
6. **Hash Cracking**: Use John the Ripper to crack the extracted hashes

## Project Structure

```
ai-recon-tool/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── services/
│   │   ├── netdiscover.py     # Network discovery service
│   │   ├── nmap_scanner.py    # Port scanning service
│   │   ├── metasploit.py      # Metasploit integration
│   │   └── john.py            # John the Ripper integration
│   ├── utils/
│   │   └── network.py         # Network utilities
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API services
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## Quick Start (VMware)

For a quick start in VMware:

```bash
# 1. Make scripts executable
chmod +x setup.sh start.sh

# 2. Run setup
./setup.sh

# 3. Start services
./start.sh
```

See [VMWARE_SETUP.md](VMWARE_SETUP.md) for detailed instructions.

## Security Considerations

- Always run in isolated environments (VMs, containers)
- Never use on networks without explicit authorization
- Review all commands before execution
- Keep tools and dependencies updated
- **VMware provides isolation but doesn't make unauthorized scanning legal**

## Contributing

Contributions are welcome! Please read the contributing guidelines and code of conduct before submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for educational and authorized security testing purposes
- Uses industry-standard penetration testing tools

