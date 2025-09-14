#!/bin/bash

# FraudDocAI Setup Script
echo "🚀 Setting up FraudDocAI Development Environment..."

# Check if required tools are installed
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install it first."
        return 1
    else
        echo "✅ $1 is installed"
        return 0
    fi
}

echo "📋 Checking prerequisites..."
check_command "docker" || exit 1
check_command "docker-compose" || exit 1

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed."
    echo "Please install Node.js from: https://nodejs.org/"
    echo "Or use a version manager like nvm: https://github.com/nvm-sh/nvm"
    exit 1
else
    echo "✅ Node.js is installed ($(node --version))"
fi

# Check for Go
if ! command -v go &> /dev/null; then
    echo "❌ Go is not installed."
    echo "Please install Go from: https://golang.org/dl/"
    exit 1
else
    echo "✅ Go is installed ($(go version))"
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "Please install Python 3 from: https://python.org/"
    exit 1
else
    echo "✅ Python 3 is installed ($(python3 --version))"
fi

echo ""
echo "🐳 Starting Docker services..."
docker-compose up -d

echo ""
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "🐍 Setting up Python AI service..."
cd ai-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo ""
echo "🔧 Setting up Go backend..."
cd backend
go mod tidy
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Start the development servers:"
echo "   ./scripts/start-dev.sh"
echo ""
echo "2. Or start services individually:"
echo "   Frontend: cd frontend && npm start"
echo "   Backend:  cd backend && go run main.go"
echo "   AI Service: cd ai-service && source venv/bin/activate && python app.py"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8080"
echo "   AI Service: http://localhost:8001"
echo "   Database: localhost:5432"
echo ""
echo "📚 For more information, see README.md"
