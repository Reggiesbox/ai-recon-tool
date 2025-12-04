"""
John the Ripper Service - Hash cracking integration
"""

import subprocess
import asyncio
import os
from typing import Dict, Optional, List


class JohnService:
    """Service for cracking password hashes using John the Ripper"""
    
    def __init__(self):
        self.default_wordlist = "/usr/share/wordlists/rockyou.txt"
    
    async def crack_hashes(self, hash_file: str, wordlist: Optional[str] = None) -> Dict:
        """
        Crack password hashes using John the Ripper
        
        Args:
            hash_file: Path to file containing hashes
            wordlist: Path to wordlist file (optional)
        
        Returns:
            Dictionary with cracking results
        """
        if not os.path.exists(hash_file):
            raise Exception(f"Hash file not found: {hash_file}")
        
        wordlist_path = wordlist or self.default_wordlist
        
        # Build john command
        cmd = ["john", "--format=sha512crypt", hash_file]
        
        if wordlist and os.path.exists(wordlist_path):
            cmd.extend(["--wordlist", wordlist_path])
        
        try:
            # Run john in background (it can take a while)
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Don't wait for completion, return immediately
            # User can check status later
            
            return {
                "success": True,
                "message": "John the Ripper started",
                "hash_file": hash_file,
                "process_id": process.pid
            }
            
        except FileNotFoundError:
            raise Exception("john command not found. Please install john.")
        except Exception as e:
            raise Exception(f"John the Ripper failed: {str(e)}")
    
    async def get_status(self, hash_file: str) -> Dict:
        """
        Get status of hash cracking process
        
        Args:
            hash_file: Path to hash file
        
        Returns:
            Dictionary with current status and cracked passwords
        """
        try:
            # Use john --show to get cracked passwords
            cmd = ["john", "--show", "--format=sha512crypt", hash_file]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            output = stdout.decode() if stdout else ""
            error_output = stderr.decode() if stderr else ""
            
            # Parse output
            cracked = self._parse_cracked_output(output)
            
            return {
                "success": True,
                "cracked_count": len(cracked),
                "cracked_passwords": cracked,
                "output": output
            }
            
        except Exception as e:
            raise Exception(f"Failed to get status: {str(e)}")
    
    def _parse_cracked_output(self, output: str) -> List[Dict]:
        """Parse john --show output to extract cracked passwords"""
        cracked = []
        
        for line in output.split('\n'):
            if ':' in line and not line.startswith('#'):
                parts = line.split(':')
                if len(parts) >= 2:
                    username = parts[0]
                    password = parts[1] if len(parts) > 1 else ""
                    cracked.append({
                        "username": username,
                        "password": password
                    })
        
        return cracked

