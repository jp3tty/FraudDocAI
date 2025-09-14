#!/bin/bash

echo "🤖 FraudDocAI AI Service Progress Monitor"
echo "========================================"
echo ""

# Check if service is running
if pgrep -f "python app.py" > /dev/null; then
    echo "✅ AI Service is running"
    echo ""
    
    # Show current progress
    echo "📊 Current Progress:"
    tail -5 ai-service.log 2>/dev/null || echo "No log file yet"
    echo ""
    
    # Check if service is ready
    echo "🔍 Checking if service is ready..."
    if curl -s http://localhost:8001/health > /dev/null 2>&1; then
        echo "🎉 AI Service is READY!"
        echo "✅ All models loaded successfully"
        curl -s http://localhost:8001/health | python3 -m json.tool 2>/dev/null || echo "Service responding but JSON parsing failed"
    else
        echo "⏳ AI Service is still loading models..."
        echo "   This can take 2-3 minutes on first run"
        echo "   Models are being downloaded and initialized"
    fi
else
    echo "❌ AI Service is not running"
    echo "   Start it with: python app.py"
fi

echo ""
echo "📋 Commands to monitor:"
echo "   tail -f ai-service.log    # Real-time log monitoring"
echo "   curl http://localhost:8001/health  # Check service status"
echo "   ps aux | grep python      # Check if process is running"
