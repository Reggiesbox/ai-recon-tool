"""
NetDiscover Service - Network discovery using netdiscover command
"""

import subprocess
import asyncio
import re
from typing import List, Dict, Optional


class NetDiscoverService:
    """Service for discovering private IP addresses on the network"""
    
    def __init__(self):
        self.default_range = "192.168.1.0/24"
    
    async def scan(self, interface: Optional[str] = None, range: Optional[str] = None) -> Dict:
        """
        Scan network for private IP addresses
        
        Args:
            interface: Network interface to use (optional)
            range: IP range to scan (e.g., "192.168.1.0/24")
        
        Returns:
            Dictionary with discovered hosts
        """
        ip_range = range or self.default_range
        
        # Build netdiscover command
        cmd = ["netdiscover", "-r", ip_range, "-P"]
        
        if interface:
            cmd.extend(["-i", interface])
        
        try:
            # Run netdiscover
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                raise Exception(f"Netdiscover failed: {error_msg}")
            
            # Parse output
            output = stdout.decode()
            hosts = self._parse_output(output)
            
            return {
                "success": True,
                "hosts": hosts,
                "count": len(hosts),
                "range": ip_range
            }
            
        except FileNotFoundError:
            raise Exception("netdiscover command not found. Please install netdiscover.")
        except Exception as e:
            raise Exception(f"Network discovery failed: {str(e)}")
    
    def _parse_output(self, output: str) -> List[Dict]:
        """Parse netdiscover output to extract host information"""
        hosts = []
        
        # Netdiscover output format:
        # IP            At MAC Address     Count     Len  MAC Vendor
        # 192.168.1.1   08:00:27:xx:xx:xx    1    42    PCS Systemtechnik GmbH
        
        lines = output.strip().split('\n')
        
        for line in lines:
            # Skip header and empty lines
            if not line.strip() or 'IP' in line and 'MAC' in line:
                continue
            
            # Match IP address pattern
            ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
            if ip_match:
                ip = ip_match.group(1)
                
                # Extract MAC address if present
                mac_match = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', line)
                mac = mac_match.group(0) if mac_match else "Unknown"
                
                # Extract vendor if present
                parts = line.split()
                vendor = " ".join(parts[4:]) if len(parts) > 4 else "Unknown"
                
                hosts.append({
                    "ip": ip,
                    "mac": mac,
                    "vendor": vendor
                })
        
        return hosts

