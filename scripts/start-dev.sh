#!/bin/bash

# FraudDocAI Development Server Startup Script
echo "🚀 Starting FraudDocAI Development Servers..."

# Function to start a service in background
start_service() {
    local service_name=$1
    local command=$2
    local directory=$3
    
    echo "Starting $service_name..."
    cd $directory
    $command &
    local pid=$!
    echo $pid > "../$service_name.pid"
    cd ..
    echo "✅ $service_name started (PID: $pid)"
}

# Check if Docker services are running
if ! docker-compose ps | grep -q "Up"; then
    echo "🐳 Starting Docker services..."
    docker-compose up -d
    sleep 5
fi

# Start AI Service (Python)
start_service "ai-service" "source venv/bin/activate && python app.py" "ai-service"

# Start Backend (Go)
start_service "backend" "go run main.go" "backend"

# Start Frontend (React)
start_service "frontend" "npm start" "frontend"

echo ""
echo "🎉 All services started!"
echo ""
echo "📱 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8080"
echo "   AI Service: http://localhost:8001"
echo ""
echo "🛑 To stop all services:"
echo "   ./scripts/stop-dev.sh"
echo ""
echo "📊 To view logs:"
echo "   tail -f ai-service.log backend.log frontend.log"
