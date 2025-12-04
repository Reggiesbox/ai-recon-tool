#!/bin/bash

# AI Reconnaissance Tool - Setup Script
# This script helps set up the development environment

echo "🚀 Setting up AI Reconnaissance Tool..."

# Check if running on Linux/Kali
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  Warning: This tool is designed for Linux/Kali. Some features may not work on other OS."
fi

# Backend setup
echo "📦 Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
cd ..

# Check for required tools
echo "🔍 Checking for required tools..."
MISSING_TOOLS=()

command -v netdiscover >/dev/null 2>&1 || MISSING_TOOLS+=("netdiscover")
command -v nmap >/dev/null 2>&1 || MISSING_TOOLS+=("nmap")
command -v msfconsole >/dev/null 2>&1 || MISSING_TOOLS+=("metasploit-framework")
command -v john >/dev/null 2>&1 || MISSING_TOOLS+=("john")
command -v ifconfig >/dev/null 2>&1 || MISSING_TOOLS+=("net-tools")

if [ ${#MISSING_TOOLS[@]} -ne 0 ]; then
    echo "⚠️  Missing tools: ${MISSING_TOOLS[*]}"
    echo "   Install with: sudo apt-get install ${MISSING_TOOLS[*]}"
else
    echo "✅ All required tools are installed"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the backend:"
echo "  cd backend && source venv/bin/activate && python app.py"
echo ""
echo "To start the frontend:"
echo "  cd frontend && npm run dev"
echo ""

