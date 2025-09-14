# FraudDocAI Setup Guide

## 🚀 Quick Start

You now have a complete FraudDocAI project structure! Here's how to get started:

## 📋 Prerequisites

Before running the setup, ensure you have these installed:

### Required Software
- **Docker & Docker Compose** - For database and services
- **Node.js 18+** - For React frontend
- **Python 3.9+** - For AI service
- **Go 1.21+** - For backend API

### Installation Links
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js](https://nodejs.org/) (or use [nvm](https://github.com/nvm-sh/nvm))
- [Python](https://python.org/)
- [Go](https://golang.org/dl/)

## 🛠️ Setup Instructions

### Option 1: Automated Setup (Recommended)
```bash
cd /Users/jeremypetty/Documents/projects/FraudDocAI
./scripts/setup.sh
```

### Option 2: Manual Setup

1. **Start Docker Services**
   ```bash
   docker-compose up -d
   ```

2. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

3. **Setup Python AI Service**
   ```bash
   cd ai-service
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cd ..
   ```

4. **Setup Go Backend**
   ```bash
   cd backend
   go mod tidy
   cd ..
   ```

## 🚀 Running the Application

### Start All Services
```bash
./scripts/start-dev.sh
```

### Or Start Individually

**Terminal 1 - AI Service:**
```bash
cd ai-service
source venv/bin/activate
python app.py
```

**Terminal 2 - Backend:**
```bash
cd backend
go run main.go
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm start
```

## 🌐 Access Points

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8080
- **AI Service:** http://localhost:8001
- **Database:** localhost:5432 (user: frauddocai, password: frauddocai123)

## 📁 Project Structure

```
FraudDocAI/
├── frontend/          # React + TypeScript frontend
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Main application pages
│   │   └── App.tsx        # Main app component
│   └── package.json
├── backend/           # Go API server
│   ├── main.go        # Main server file
│   └── go.mod         # Go dependencies
├── ai-service/        # Python AI/ML service
│   ├── app.py         # FastAPI application
│   ├── requirements.txt
│   └── venv/          # Python virtual environment
├── database/          # Database schemas
│   └── init.sql       # Database initialization
├── scripts/           # Setup and utility scripts
└── docker-compose.yml # Docker services configuration
```

## 🎯 What's Already Built

### ✅ Completed Features
- **Project Structure** - Complete microservices architecture
- **Database Schema** - PostgreSQL with fraud detection tables
- **Frontend UI** - React app with 4 main pages:
  - Dashboard with statistics
  - Document upload with drag-drop
  - Fraud analysis with pattern detection
  - Reports with data visualization
- **Backend API** - Go server with REST endpoints
- **AI Service** - Python FastAPI with mock fraud detection
- **Docker Setup** - PostgreSQL, Redis, Kafka, MinIO

### 🔄 Next Steps (Week 3-4)
1. **Integrate Real AI Models** - Replace mock responses with Hugging Face models
2. **Document Processing** - Implement OCR and text extraction
3. **Fraud Detection** - Add real fraud pattern detection
4. **Database Integration** - Connect services to PostgreSQL
5. **File Upload** - Implement actual document upload and storage

## 🧪 Testing the Setup

1. **Check Docker Services:**
   ```bash
   docker-compose ps
   ```

2. **Test Backend API:**
   ```bash
   curl http://localhost:8080/health
   ```

3. **Test AI Service:**
   ```bash
   curl http://localhost:8001/health
   ```

4. **Access Frontend:**
   Open http://localhost:3000 in your browser

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Find and kill process using port
lsof -ti:3000 | xargs kill -9
lsof -ti:8080 | xargs kill -9
lsof -ti:8001 | xargs kill -9
```

**Docker Issues:**
```bash
# Reset Docker services
docker-compose down
docker-compose up -d
```

**Node.js Issues:**
```bash
# Clear npm cache
npm cache clean --force
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Python Issues:**
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📚 Next Development Phase

Now that you have the foundation, you can:

1. **Start with AI Integration** - Add real Hugging Face models
2. **Implement Document Processing** - Add OCR and text extraction
3. **Connect Services** - Wire up the database and APIs
4. **Add Real Fraud Detection** - Implement actual fraud algorithms
5. **Enhance UI** - Add more interactive features

## 🎉 Congratulations!

You now have a professional-grade project structure that demonstrates:
- **Full-stack development** (React, Go, Python)
- **Microservices architecture**
- **Modern DevOps practices** (Docker, scripts)
- **AI/ML integration** (Hugging Face, fraud detection)
- **Real-world application** (financial fraud detection)

This foundation will impress recruiters and hiring managers!
