"""
Nmap Scanner Service - Port scanning using nmap
"""

import subprocess
import asyncio
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional


class NmapScanner:
    """Service for scanning ports using nmap"""
    
    async def scan(self, target: str, ports: str = "21,22,80,443", scan_type: str = "syn") -> Dict:
        """
        Scan target for open ports
        
        Args:
            target: IP address or hostname to scan
            ports: Comma-separated list of ports or port ranges
            scan_type: Type of scan (syn, tcp, udp)
        
        Returns:
            Dictionary with scan results
        """
        # Build nmap command
        cmd = ["nmap", "-sS", "-p", ports, "-oX", "-", target]
        
        # Adjust scan type
        if scan_type == "tcp":
            cmd[1] = "-sT"
        elif scan_type == "udp":
            cmd[1] = "-sU"
        
        try:
            # Run nmap
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                raise Exception(f"Nmap scan failed: {error_msg}")
            
            # Parse XML output
            xml_output = stdout.decode()
            results = self._parse_xml(xml_output)
            
            # Check for vsftpd specifically
            vsftpd_found = False
            for port in results.get("ports", []):
                if port.get("number") == 21 and port.get("state") == "open":
                    vsftpd_found = True
                    break
            
            return {
                "success": True,
                "target": target,
                "ports": results.get("ports", []),
                "host_state": results.get("host_state", "unknown"),
                "vsftpd_detected": vsftpd_found,
                "open_ports_count": len([p for p in results.get("ports", []) if p.get("state") == "open"])
            }
            
        except FileNotFoundError:
            raise Exception("nmap command not found. Please install nmap.")
        except Exception as e:
            raise Exception(f"Nmap scan failed: {str(e)}")
    
    def _parse_xml(self, xml_string: str) -> Dict:
        """Parse nmap XML output"""
        try:
            root = ET.fromstring(xml_string)
            results = {
                "ports": [],
                "host_state": "unknown"
            }
            
            # Get host state
            host = root.find("host")
            if host is not None:
                status = host.find("status")
                if status is not None:
                    results["host_state"] = status.get("state", "unknown")
                
                # Get ports
                ports_elem = host.find("ports")
                if ports_elem is not None:
                    for port in ports_elem.findall("port"):
                        port_num = port.get("portid")
                        state = port.find("state")
                        service = port.find("service")
                        
                        port_info = {
                            "number": int(port_num),
                            "protocol": port.get("protocol", "tcp"),
                            "state": state.get("state", "unknown") if state is not None else "unknown"
                        }
                        
                        if service is not None:
                            port_info["service"] = service.get("name", "unknown")
                            port_info["product"] = service.get("product", "")
                            port_info["version"] = service.get("version", "")
                        
                        results["ports"].append(port_info)
            
            return results
            
        except ET.ParseError as e:
            raise Exception(f"Failed to parse nmap XML output: {str(e)}")

