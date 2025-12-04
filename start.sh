#!/bin/bash

# AI Reconnaissance Tool - Start Script for VMware
# This script starts both backend and frontend services

echo "🚀 Starting AI Reconnaissance Tool..."

# Get VM IP address
VM_IP=$(hostname -I | awk '{print $1}')
echo "📍 VM IP Address: $VM_IP"
echo ""

# Check if backend venv exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Backend virtual environment not found!"
    echo "   Run: cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Frontend dependencies not installed!"
    echo "   Run: cd frontend && npm install"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Start backend
echo "🔧 Starting backend server..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 2

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Services started!"
echo ""
echo "📍 Access URLs:"
echo "   Backend API:  http://localhost:8000"
echo "   Frontend UI:  http://localhost:5173"
echo ""
echo "🌐 From Host Machine:"
echo "   Backend API:  http://$VM_IP:8000"
echo "   Frontend UI:  http://$VM_IP:5173"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for processes
wait

