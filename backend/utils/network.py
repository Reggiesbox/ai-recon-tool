"""
Network Utilities - Network interface detection and configuration
"""

import subprocess
import re
from typing import List, Dict


class NetworkUtils:
    """Utilities for network interface management"""
    
    def get_network_interfaces(self) -> List[Dict]:
        """
        Get available network interfaces using ifconfig
        
        Returns:
            List of network interfaces with their details
        """
        try:
            result = subprocess.run(
                ["ifconfig"],
                capture_output=True,
                text=True,
                check=True
            )
            
            interfaces = self._parse_ifconfig_output(result.stdout)
            return interfaces
            
        except FileNotFoundError:
            raise Exception("ifconfig command not found. Please install net-tools.")
        except subprocess.CalledProcessError as e:
            raise Exception(f"ifconfig failed: {e.stderr}")
    
    def _parse_ifconfig_output(self, output: str) -> List[Dict]:
        """Parse ifconfig output to extract interface information"""
        interfaces = []
        current_interface = None
        
        lines = output.split('\n')
        
        for line in lines:
            # Interface name (starts at beginning of line, no spaces)
            if line and not line.startswith(' ') and not line.startswith('\t'):
                if current_interface:
                    interfaces.append(current_interface)
                
                interface_name = line.split(':')[0].strip()
                current_interface = {
                    "name": interface_name,
                    "ip": None,
                    "netmask": None,
                    "mac": None,
                    "status": "down"
                }
            
            # IP address
            if current_interface:
                ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', line)
                if ip_match:
                    current_interface["ip"] = ip_match.group(1)
                    current_interface["status"] = "up"
                
                # Netmask
                netmask_match = re.search(r'netmask ([\da-fx]+)', line)
                if netmask_match:
                    current_interface["netmask"] = netmask_match.group(1)
                
                # MAC address
                mac_match = re.search(r'ether ([0-9a-f:]{17})', line)
                if mac_match:
                    current_interface["mac"] = mac_match.group(1)
        
        if current_interface:
            interfaces.append(current_interface)
        
        return interfaces

