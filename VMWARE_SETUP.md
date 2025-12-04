# VMware Setup Guide

This guide provides detailed instructions for setting up and running the AI Reconnaissance Tool in a VMware Linux VM.

## VM Requirements

- **VMware Workstation** (Pro/Player) or **VMware Fusion** (Mac)
- **Kali Linux** VM (recommended) or other Linux distribution
- Minimum 2GB RAM allocated to VM
- Network adapter configured

## Step 1: VM Network Configuration

### Option A: Bridged Networking (Recommended for Network Scanning)

1. **VMware Settings**:
   - Right-click VM → Settings
   - Select Network Adapter
   - Choose **Bridged** mode
   - Check "Replicate physical network connection state"

2. **Benefits**:
   - VM gets its own IP on your physical network
   - Can scan other devices on the network
   - Direct network access

3. **Verify Connection**:
   ```bash
   ifconfig
   # Should show an IP on your network (e.g., 192.168.1.x)
   ping 8.8.8.8
   ```

### Option B: NAT Networking (Isolated Testing)

1. **VMware Settings**:
   - Network Adapter → **NAT** mode

2. **Benefits**:
   - VM is isolated from physical network
   - Can still access internet
   - Safer for testing

3. **Limitations**:
   - Cannot directly scan physical network devices
   - Use internal VM network for testing

## Step 2: Install Required Tools in VM

### Kali Linux (Most Tools Pre-installed)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install missing tools if needed
sudo apt install -y netdiscover nmap metasploit-framework john net-tools

# Verify installations
netdiscover --version
nmap --version
msfconsole --version
john --version
```

### Other Linux Distributions

```bash
# Install tools
sudo apt install -y netdiscover nmap john net-tools

# Install Metasploit (if not available in repos)
# Follow official Metasploit installation guide
```

## Step 3: Project Setup in VM

```bash
# Clone or copy project to VM
cd ~
git clone <repository-url>
cd ai-recon-tool

# Or use shared folders/VMware Tools to copy files
```

## Step 4: Network Interface Identification

```bash
# List all network interfaces
ifconfig -a

# Common VMware interfaces:
# - eth0 (older VMware)
# - ens33 (newer VMware)
# - ens160 (some configurations)

# Get your VM's IP address
ip addr show
# or
ifconfig | grep "inet "
```

**Note the interface name** - you'll need it for network discovery.

## Step 5: Firewall Configuration

```bash
# Check firewall status (Kali usually has firewall disabled)
sudo ufw status

# If firewall is active, allow ports
sudo ufw allow 8000/tcp
sudo ufw allow 5173/tcp
sudo ufw reload
```

## Step 6: Start the Application

### Terminal 1 - Backend

```bash
cd ~/ai-recon-tool/backend
source venv/bin/activate
python app.py
```

Backend will start on `0.0.0.0:8000` (accessible from host if configured).

### Terminal 2 - Frontend

```bash
cd ~/ai-recon-tool/frontend
npm run dev
```

Frontend will start on `localhost:5173`.

## Step 7: Access from Host Machine

### Method 1: Direct Access (Bridged Network)

1. Find VM IP address:
   ```bash
   ifconfig | grep inet
   # Example: 192.168.1.105
   ```

2. Update frontend to allow external access:
   - Edit `frontend/vite.config.js`:
     ```js
     server: {
       host: '0.0.0.0',  // Allow external access
       port: 5173
     }
     ```

3. Access from host browser:
   - `http://VM_IP_ADDRESS:5173`
   - `http://VM_IP_ADDRESS:8000` (API)

### Method 2: SSH Port Forwarding

On your host machine:

```bash
# Windows (PowerShell or Git Bash)
ssh -L 5173:localhost:5173 -L 8000:localhost:8000 kali@VM_IP

# Mac/Linux
ssh -L 5173:localhost:5173 -L 8000:localhost:8000 kali@VM_IP
```

Then access `http://localhost:5173` on host.

### Method 3: VMware NAT Port Forwarding

1. VM Settings → Network Adapter → NAT Settings
2. Click "Port Forwarding"
3. Add rules:
   - **Host Port**: 5173 → **Guest Port**: 5173
   - **Host Port**: 8000 → **Guest Port**: 8000
4. Access `http://localhost:5173` on host

## Troubleshooting

### Network Discovery Not Working

```bash
# Check network interface
ifconfig

# Try different interface
# In the web UI, select the correct interface (eth0, ens33, etc.)

# Check if you have permission
sudo netdiscover -r 192.168.1.0/24
```

### Cannot Access from Host

1. **Check VM IP**:
   ```bash
   ifconfig
   ```

2. **Check Firewall**:
   ```bash
   sudo ufw status
   sudo ufw allow 8000/tcp
   ```

3. **Test Connection**:
   ```bash
   # From host, test if port is open
   telnet VM_IP 8000
   ```

### Metasploit Not Working

```bash
# Initialize Metasploit database
sudo msfdb init

# Start PostgreSQL (if needed)
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Permission Issues

Some commands require root access:

```bash
# For network scanning, you may need sudo
sudo nmap -sS target_ip

# The application handles this automatically, but if issues occur:
sudo python app.py
```

## Network Scanning Tips

1. **Identify Your Network**:
   ```bash
   # Find your network range
   ip route | grep default
   ifconfig | grep "inet "
   # Use the network range in netdiscover (e.g., 192.168.1.0/24)
   ```

2. **Test Network Connectivity**:
   ```bash
   # Ping gateway
   ping 192.168.1.1
   
   # Scan local network
   nmap -sn 192.168.1.0/24
   ```

3. **VMware Network Modes**:
   - **Bridged**: Best for scanning physical network
   - **NAT**: Isolated, good for testing with other VMs
   - **Host-only**: Completely isolated, only VM-to-VM

## Security Notes

⚠️ **Important**: 
- Only scan networks you own or have explicit permission to test
- Running in a VM provides isolation but doesn't make unauthorized scanning legal
- Use bridged mode carefully - your VM will appear as a device on your network
- Consider using NAT or host-only for practice/testing

## Quick Reference

```bash
# Find VM IP
ifconfig | grep inet

# Check network interface
ip addr show

# Test API
curl http://localhost:8000

# Test from host (replace VM_IP)
curl http://VM_IP:8000
```

