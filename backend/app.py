"""
AI Reconnaissance Tool - Backend API
FastAPI application for penetration testing tool integration
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import subprocess
import json
import os
import re

from services.netdiscover import NetDiscoverService
from services.nmap_scanner import NmapScanner
from services.metasploit import MetasploitService
from services.john import JohnService
from utils.network import NetworkUtils

app = FastAPI(title="AI Reconnaissance Tool API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
netdiscover = NetDiscoverService()
nmap_scanner = NmapScanner()
metasploit = MetasploitService()
john = JohnService()
network_utils = NetworkUtils()


# Request/Response Models
class NetworkDiscoveryRequest(BaseModel):
    interface: Optional[str] = None
    range: Optional[str] = None


class NmapScanRequest(BaseModel):
    target: str
    ports: Optional[str] = "21,22,80,443"
    scan_type: Optional[str] = "syn"


class MetasploitExploitRequest(BaseModel):
    exploit_name: str
    rhosts: str
    rport: Optional[int] = 21
    payload: Optional[str] = "cmd/unix/interact"


class HashExtractionRequest(BaseModel):
    session_id: str
    shadow_path: str = "/etc/shadow"


class JohnCrackRequest(BaseModel):
    hash_file: str
    wordlist: Optional[str] = None


# API Routes
@app.get("/")
async def root():
    return {"message": "AI Reconnaissance Tool API", "version": "1.0.0"}


@app.get("/api/network/interfaces")
async def get_network_interfaces():
    """Get available network interfaces using ifconfig"""
    try:
        interfaces = network_utils.get_network_interfaces()
        return {"interfaces": interfaces}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/network/discover")
async def discover_network(request: NetworkDiscoveryRequest):
    """Discover private IP addresses using netdiscover"""
    try:
        result = await netdiscover.scan(
            interface=request.interface,
            range=request.range
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/nmap/scan")
async def scan_ports(request: NmapScanRequest):
    """Scan target for open ports using nmap"""
    try:
        result = await nmap_scanner.scan(
            target=request.target,
            ports=request.ports,
            scan_type=request.scan_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metasploit/search")
async def search_exploits(query: str):
    """Search Metasploit for exploits"""
    try:
        results = await metasploit.search_exploits(query)
        return {"exploits": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/metasploit/exploit")
async def execute_exploit(request: MetasploitExploitRequest):
    """Execute Metasploit exploit"""
    try:
        result = await metasploit.exploit(
            exploit_name=request.exploit_name,
            rhosts=request.rhosts,
            rport=request.rport,
            payload=request.payload
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metasploit/sessions")
async def list_sessions():
    """List active Metasploit sessions"""
    try:
        sessions = await metasploit.list_sessions()
        return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/metasploit/command")
async def execute_command(session_id: str, command: str):
    """Execute command in Metasploit session"""
    try:
        result = await metasploit.execute_command(session_id, command)
        return {"output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/hashes/extract")
async def extract_hashes(request: HashExtractionRequest):
    """Extract password hashes from shadow file"""
    try:
        result = await metasploit.extract_shadow_hashes(
            session_id=request.session_id,
            shadow_path=request.shadow_path
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/john/crack")
async def crack_hashes(request: JohnCrackRequest):
    """Crack password hashes using John the Ripper"""
    try:
        result = await john.crack_hashes(
            hash_file=request.hash_file,
            wordlist=request.wordlist
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/john/status/{hash_file}")
async def get_crack_status(hash_file: str):
    """Get status of John the Ripper cracking process"""
    try:
        status = await john.get_status(hash_file)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    # Bind to 0.0.0.0 to allow access from host machine in VMware
    # This makes the API accessible from both VM and host when using bridged/NAT networking
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

