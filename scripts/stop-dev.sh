#!/bin/bash

# FraudDocAI Development Server Stop Script
echo "🛑 Stopping FraudDocAI Development Servers..."

# Function to stop a service
stop_service() {
    local service_name=$1
    local pid_file="$service_name.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo "Stopping $service_name (PID: $pid)..."
            kill $pid
            rm "$pid_file"
            echo "✅ $service_name stopped"
        else
            echo "⚠️  $service_name was not running"
            rm "$pid_file"
        fi
    else
        echo "⚠️  No PID file found for $service_name"
    fi
}

# Stop all services
stop_service "ai-service"
stop_service "backend"
stop_service "frontend"

# Stop Docker services
echo "🐳 Stopping Docker services..."
docker-compose down

echo ""
echo "✅ All services stopped!"
echo ""
echo "🚀 To start again:"
echo "   ./scripts/start-dev.sh"
